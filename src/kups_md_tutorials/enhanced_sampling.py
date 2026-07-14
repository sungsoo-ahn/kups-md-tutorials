"""Adaptive and nonequilibrium enhanced-sampling diagnostics for post 11."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import EnhancedSamplingTutorialSpec
from kups_md_tutorials.free_energies import double_well_potential
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class MetadynamicsSummary:
    """Compact diagnostics for adaptive bias filling."""

    deposit_count: int
    hill_height: float
    hill_width: float
    bias_factor: float
    initial_barrier_height: float
    final_bias_range: float
    reconstructed_barrier_height: float
    reconstructed_barrier_error: float
    basin_visit_fraction_left: float
    basin_visit_fraction_right: float
    barrier_visit_fraction: float
    final_histogram_flatness: float


@dataclass(frozen=True)
class PullingSummary:
    """Compact diagnostics for nonequilibrium pulling."""

    path_count: int
    path_steps: int
    trap_force_constant: float
    start_center: float
    end_center: float
    true_delta_f: float
    forward_mean_work: float
    reverse_mean_work: float
    forward_jarzynski_delta_f: float
    reverse_jarzynski_delta_f: float
    crooks_crossing_delta_f: float
    forward_dissipated_work: float
    reverse_dissipated_work: float
    forward_work_std: float
    reverse_work_std: float
    forward_ess_fraction: float
    reverse_ess_fraction: float


@dataclass(frozen=True)
class SteeredHysteresisSummary:
    """Path-level diagnostics for finite-speed steered pulling."""

    trajectory_path_count: int
    fast_path_steps: int
    slow_path_steps: int
    fast_forward_mean_work: float
    fast_reverse_mean_work: float
    slow_forward_mean_work: float
    slow_reverse_mean_work: float
    fast_hysteresis_gap: float
    slow_hysteresis_gap: float
    fast_hysteresis_gap_sem: float
    slow_hysteresis_gap_sem: float
    hysteresis_gap_ratio: float


@dataclass(frozen=True)
class EnhancedSamplingExperimentSummary:
    """Summary table for one post/profile enhanced-sampling experiment."""

    post: str
    profile: str
    temperature: float
    seed: int
    domain_min: float
    domain_max: float
    config_sha256: str
    metadynamics: MetadynamicsSummary
    pulling: PullingSummary
    steered_hysteresis: SteeredHysteresisSummary


def _normalized_probabilities(energies: np.ndarray, temperature: float) -> np.ndarray:
    weights = np.exp(-(energies - np.min(energies)) / temperature)
    return weights / np.sum(weights)


def _gaussian(grid: np.ndarray, center: float, width: float) -> np.ndarray:
    return np.exp(-0.5 * ((grid - center) / width) ** 2)


def _barrier_height(grid: np.ndarray, pmf: np.ndarray) -> float:
    left_mask = (grid > -1.25) & (grid < -0.75)
    right_mask = (grid > 0.75) & (grid < 1.25)
    barrier_mask = (grid > -0.15) & (grid < 0.15)
    basin = min(float(np.nanmin(pmf[left_mask])), float(np.nanmin(pmf[right_mask])))
    return float(np.nanmin(pmf[barrier_mask]) - basin)


def _run_metadynamics(
    spec: EnhancedSamplingTutorialSpec,
    grid: np.ndarray,
) -> tuple[MetadynamicsSummary, dict[str, np.ndarray]]:
    exp = spec.experiment
    meta = exp.metadynamics
    rng = np.random.default_rng(exp.seed)
    true_pmf = double_well_potential(grid)
    true_pmf -= np.min(true_pmf)
    bias = np.zeros_like(grid)
    visits = []
    records = []

    for step in range(meta.deposit_count):
        probabilities = _normalized_probabilities(true_pmf + bias, exp.temperature)
        sample = float(rng.choice(grid, p=probabilities))
        visits.append(sample)
        local_bias = float(np.interp(sample, grid, bias))
        tempered_height = meta.hill_height * np.exp(
            -local_bias / (meta.bias_factor * exp.temperature)
        )
        bias += tempered_height * _gaussian(grid, sample, meta.hill_width)
        if (step + 1) % meta.record_every == 0:
            records.append((step + 1, float(np.ptp(bias))))

    visits_array = np.array(visits, dtype=float)
    reconstructed = -meta.bias_factor / (meta.bias_factor - 1.0) * bias
    reconstructed -= np.nanmin(reconstructed)
    initial_barrier = _barrier_height(grid, true_pmf)
    reconstructed_barrier = _barrier_height(grid, reconstructed)
    hist, _ = np.histogram(visits_array, bins=np.linspace(-1.5, 1.5, 16))
    occupied = hist[hist > 0]
    flatness = float(np.min(occupied) / np.max(occupied)) if len(occupied) else 0.0
    summary = MetadynamicsSummary(
        deposit_count=meta.deposit_count,
        hill_height=meta.hill_height,
        hill_width=meta.hill_width,
        bias_factor=meta.bias_factor,
        initial_barrier_height=initial_barrier,
        final_bias_range=float(np.ptp(bias)),
        reconstructed_barrier_height=reconstructed_barrier,
        reconstructed_barrier_error=float(reconstructed_barrier - initial_barrier),
        basin_visit_fraction_left=float(np.mean(visits_array < -0.5)),
        basin_visit_fraction_right=float(np.mean(visits_array > 0.5)),
        barrier_visit_fraction=float(np.mean(np.abs(visits_array) < 0.25)),
        final_histogram_flatness=flatness,
    )
    return (
        summary,
        {
            "grid": grid,
            "true_pmf": true_pmf,
            "bias": bias,
            "reconstructed_pmf": reconstructed,
            "visits": visits_array,
            "record_step": np.array([item[0] for item in records], dtype=float),
            "record_bias_range": np.array([item[1] for item in records], dtype=float),
        },
    )


def _trap_bias(values: np.ndarray, center: float, force_constant: float) -> np.ndarray:
    return 0.5 * force_constant * (values - center) ** 2


def _sample_trap_equilibrium(
    *,
    grid: np.ndarray,
    center: float,
    force_constant: float,
    temperature: float,
    count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    energies = double_well_potential(grid) + _trap_bias(grid, center, force_constant)
    probabilities = _normalized_probabilities(energies, temperature)
    return rng.choice(grid, size=count, replace=True, p=probabilities)


def _equilibrium_trap_free_energy(
    grid: np.ndarray,
    center: float,
    force_constant: float,
    temperature: float,
) -> float:
    energies = double_well_potential(grid) + _trap_bias(grid, center, force_constant)
    weights = np.exp(-(energies - np.min(energies)) / temperature)
    integral = np.trapezoid(weights, grid)
    return float(np.min(energies) - temperature * np.log(integral))


def _run_pulling_direction(
    *,
    grid: np.ndarray,
    start_center: float,
    end_center: float,
    force_constant: float,
    temperature: float,
    path_count: int,
    path_steps: int,
    noise_scale: float,
    rng: np.random.Generator,
) -> np.ndarray:
    lambdas = np.linspace(start_center, end_center, path_steps + 1)
    positions = _sample_trap_equilibrium(
        grid=grid,
        center=start_center,
        force_constant=force_constant,
        temperature=temperature,
        count=path_count,
        rng=rng,
    )
    works = np.zeros(path_count, dtype=float)
    for idx in range(path_steps):
        old_center = lambdas[idx]
        new_center = lambdas[idx + 1]
        works += _trap_bias(positions, new_center, force_constant) - _trap_bias(
            positions,
            old_center,
            force_constant,
        )
        target = _sample_trap_equilibrium(
            grid=grid,
            center=new_center,
            force_constant=force_constant,
            temperature=temperature,
            count=path_count,
            rng=rng,
        )
        relaxation = 0.055
        positions = (1.0 - relaxation) * positions + relaxation * target
        if noise_scale > 0.0:
            positions += rng.normal(0.0, noise_scale, size=path_count)
        positions = np.clip(positions, grid[0], grid[-1])
    return works


def _jarzynski(work: np.ndarray, temperature: float) -> float:
    shifted = -work / temperature
    max_value = np.max(shifted)
    return float(-temperature * (max_value + np.log(np.mean(np.exp(shifted - max_value)))))


def _ess_fraction(log_weights: np.ndarray) -> float:
    shifted = log_weights - np.max(log_weights)
    weights = np.exp(shifted)
    ess = np.sum(weights) ** 2 / np.sum(weights * weights)
    return float(ess / len(weights))


def _crooks_crossing(forward_work: np.ndarray, reverse_work: np.ndarray) -> float:
    values = np.linspace(
        min(float(np.min(forward_work)), float(np.min(-reverse_work))),
        max(float(np.max(forward_work)), float(np.max(-reverse_work))),
        400,
    )
    bins = np.linspace(values[0], values[-1], 80)
    centers = 0.5 * (bins[:-1] + bins[1:])
    forward_hist, _ = np.histogram(forward_work, bins=bins, density=True)
    reverse_hist, _ = np.histogram(-reverse_work, bins=bins, density=True)
    difference = forward_hist - reverse_hist
    valid = np.isfinite(difference)
    centers = centers[valid]
    difference = difference[valid]
    sign_changes = np.where(np.signbit(difference[:-1]) != np.signbit(difference[1:]))[0]
    if len(sign_changes) == 0:
        return float(centers[np.argmin(np.abs(difference))])
    idx = int(sign_changes[np.argmin(np.abs(centers[sign_changes]))])
    x0, x1 = centers[idx], centers[idx + 1]
    y0, y1 = difference[idx], difference[idx + 1]
    if y1 == y0:
        return float(x0)
    return float(x0 - y0 * (x1 - x0) / (y1 - y0))


def _run_pulling(
    spec: EnhancedSamplingTutorialSpec,
    grid: np.ndarray,
) -> tuple[PullingSummary, dict[str, np.ndarray]]:
    exp = spec.experiment
    pull = exp.pulling
    rng = np.random.default_rng(exp.seed + 900001)
    free_start = _equilibrium_trap_free_energy(
        grid,
        pull.start_center,
        pull.trap_force_constant,
        exp.temperature,
    )
    free_end = _equilibrium_trap_free_energy(
        grid,
        pull.end_center,
        pull.trap_force_constant,
        exp.temperature,
    )
    true_delta_f = float(free_end - free_start)
    distance = abs(pull.end_center - pull.start_center)
    protocol_rate = distance / pull.path_steps
    dissipation = max(
        0.05,
        0.42
        * pull.trap_force_constant
        * distance
        * protocol_rate
        * (1.0 + pull.noise_scale),
    )
    work_std = np.sqrt(2.0 * dissipation * exp.temperature)
    forward = rng.normal(
        true_delta_f + dissipation,
        work_std,
        size=pull.path_count,
    )
    reverse = rng.normal(
        -true_delta_f + dissipation,
        work_std,
        size=pull.path_count,
    )
    forward_jarzynski = _jarzynski(forward, exp.temperature)
    reverse_jarzynski = -_jarzynski(reverse, exp.temperature)
    summary = PullingSummary(
        path_count=pull.path_count,
        path_steps=pull.path_steps,
        trap_force_constant=pull.trap_force_constant,
        start_center=pull.start_center,
        end_center=pull.end_center,
        true_delta_f=true_delta_f,
        forward_mean_work=float(np.mean(forward)),
        reverse_mean_work=float(np.mean(reverse)),
        forward_jarzynski_delta_f=forward_jarzynski,
        reverse_jarzynski_delta_f=reverse_jarzynski,
        crooks_crossing_delta_f=_crooks_crossing(forward, reverse),
        forward_dissipated_work=float(np.mean(forward) - true_delta_f),
        reverse_dissipated_work=float(np.mean(reverse) + true_delta_f),
        forward_work_std=float(np.std(forward, ddof=1)),
        reverse_work_std=float(np.std(reverse, ddof=1)),
        forward_ess_fraction=_ess_fraction(-forward / exp.temperature),
        reverse_ess_fraction=_ess_fraction(-reverse / exp.temperature),
    )
    return summary, {"forward_work": forward, "reverse_work": reverse}


def _hysteresis_gap_sem(forward: np.ndarray, reverse: np.ndarray) -> float:
    return float(
        np.sqrt(
            np.var(forward, ddof=1) / len(forward)
            + np.var(reverse, ddof=1) / len(reverse)
        )
    )


def _run_steered_hysteresis(
    spec: EnhancedSamplingTutorialSpec,
    grid: np.ndarray,
) -> tuple[SteeredHysteresisSummary, dict[str, np.ndarray]]:
    exp = spec.experiment
    pull = exp.pulling
    rng = np.random.default_rng(exp.seed + 1700003)
    trajectory_path_count = min(pull.path_count, 6000)
    fast_path_steps = max(12, pull.path_steps // 4)
    slow_path_steps = max(pull.path_steps + 1, pull.path_steps * 2)

    fast_forward = _run_pulling_direction(
        grid=grid,
        start_center=pull.start_center,
        end_center=pull.end_center,
        force_constant=pull.trap_force_constant,
        temperature=exp.temperature,
        path_count=trajectory_path_count,
        path_steps=fast_path_steps,
        noise_scale=pull.noise_scale,
        rng=rng,
    )
    fast_reverse = _run_pulling_direction(
        grid=grid,
        start_center=pull.end_center,
        end_center=pull.start_center,
        force_constant=pull.trap_force_constant,
        temperature=exp.temperature,
        path_count=trajectory_path_count,
        path_steps=fast_path_steps,
        noise_scale=pull.noise_scale,
        rng=rng,
    )
    slow_forward = _run_pulling_direction(
        grid=grid,
        start_center=pull.start_center,
        end_center=pull.end_center,
        force_constant=pull.trap_force_constant,
        temperature=exp.temperature,
        path_count=trajectory_path_count,
        path_steps=slow_path_steps,
        noise_scale=pull.noise_scale,
        rng=rng,
    )
    slow_reverse = _run_pulling_direction(
        grid=grid,
        start_center=pull.end_center,
        end_center=pull.start_center,
        force_constant=pull.trap_force_constant,
        temperature=exp.temperature,
        path_count=trajectory_path_count,
        path_steps=slow_path_steps,
        noise_scale=pull.noise_scale,
        rng=rng,
    )

    fast_gap = float(np.mean(fast_forward) + np.mean(fast_reverse))
    slow_gap = float(np.mean(slow_forward) + np.mean(slow_reverse))
    summary = SteeredHysteresisSummary(
        trajectory_path_count=trajectory_path_count,
        fast_path_steps=fast_path_steps,
        slow_path_steps=slow_path_steps,
        fast_forward_mean_work=float(np.mean(fast_forward)),
        fast_reverse_mean_work=float(np.mean(fast_reverse)),
        slow_forward_mean_work=float(np.mean(slow_forward)),
        slow_reverse_mean_work=float(np.mean(slow_reverse)),
        fast_hysteresis_gap=fast_gap,
        slow_hysteresis_gap=slow_gap,
        fast_hysteresis_gap_sem=_hysteresis_gap_sem(fast_forward, fast_reverse),
        slow_hysteresis_gap_sem=_hysteresis_gap_sem(slow_forward, slow_reverse),
        hysteresis_gap_ratio=float(fast_gap / slow_gap),
    )
    return (
        summary,
        {
            "fast_forward_steered_work": fast_forward,
            "fast_reverse_steered_work": fast_reverse,
            "slow_forward_steered_work": slow_forward,
            "slow_reverse_steered_work": slow_reverse,
        },
    )


def run_enhanced_sampling_experiment(
    spec: EnhancedSamplingTutorialSpec,
    config_sha256: str,
) -> tuple[EnhancedSamplingExperimentSummary, dict[str, np.ndarray]]:
    """Run all configured adaptive and nonequilibrium diagnostics."""

    exp = spec.experiment
    grid = np.linspace(exp.domain_min, exp.domain_max, exp.grid_points)
    meta_summary, meta_curves = _run_metadynamics(spec, grid)
    pulling_summary, pulling_curves = _run_pulling(spec, grid)
    hysteresis_summary, hysteresis_curves = _run_steered_hysteresis(spec, grid)
    curves = {**meta_curves, **pulling_curves, **hysteresis_curves}
    return (
        EnhancedSamplingExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=exp.temperature,
            seed=exp.seed,
            domain_min=exp.domain_min,
            domain_max=exp.domain_max,
            config_sha256=config_sha256,
            metadynamics=meta_summary,
            pulling=pulling_summary,
            steered_hysteresis=hysteresis_summary,
        ),
        curves,
    )


def _write_enhanced_curves(path: Path, curves: dict[str, np.ndarray]) -> None:
    max_len = max(
        len(curves["grid"]),
        len(curves["visits"]),
        len(curves["record_step"]),
        len(curves["forward_work"]),
        len(curves["fast_forward_steered_work"]),
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "grid",
                "true_pmf",
                "bias",
                "reconstructed_pmf",
                "visit",
                "record_step",
                "record_bias_range",
                "forward_work",
                "reverse_work",
                "fast_forward_steered_work",
                "fast_reverse_steered_work",
                "slow_forward_steered_work",
                "slow_reverse_steered_work",
            ]
        )
        for idx in range(max_len):
            row = []
            for key in (
                "grid",
                "true_pmf",
                "bias",
                "reconstructed_pmf",
                "visits",
                "record_step",
                "record_bias_range",
                "forward_work",
                "reverse_work",
                "fast_forward_steered_work",
                "fast_reverse_steered_work",
                "slow_forward_steered_work",
                "slow_reverse_steered_work",
            ):
                values = curves[key]
                row.append(f"{values[idx]:.12g}" if idx < len(values) else "")
            writer.writerow(row)


def write_enhanced_sampling_outputs(
    spec: EnhancedSamplingTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-11 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, curves = run_enhanced_sampling_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "enhanced_sampling_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "enhanced_sampling_curves.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_enhanced_curves(curves_path, curves)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "curves_file": curves_path.name,
        "provenance": asdict(prov),
        "versions": {
            "kups": kups.__version__,
            "numpy": np.__version__,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_dir


def load_enhanced_sampling_summary(path: Path) -> EnhancedSamplingExperimentSummary:
    """Read a previously written post-11 enhanced-sampling summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    metadynamics = MetadynamicsSummary(**data.pop("metadynamics"))
    pulling = PullingSummary(**data.pop("pulling"))
    steered_hysteresis = SteeredHysteresisSummary(**data.pop("steered_hysteresis"))
    return EnhancedSamplingExperimentSummary(
        metadynamics=metadynamics,
        pulling=pulling,
        steered_hysteresis=steered_hysteresis,
        **data,
    )
