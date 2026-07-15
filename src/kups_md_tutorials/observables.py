"""Observable-estimator diagnostics for post 07."""

from dataclasses import asdict, dataclass, replace
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import ObservableSystemSpec, ObservableTutorialSpec
from kups_md_tutorials.error_diagnostics import (
    _initialized_argon_velocities,
    _lennard_jones_forces,
)
from kups_md_tutorials.provenance import (
    gpu_blocking_reason,
    provenance,
    runtime_device,
    runtime_is_gpu,
    target_requests_gpu,
)
from kups_md_tutorials.systems import argon_fcc


@dataclass(frozen=True)
class ObservableSystemSummary:
    """Compact diagnostics for one finite-size observable estimate."""

    system: str
    repetitions: int
    atom_count: int
    frame_count: int
    number_density: float
    cell_length: float
    rdf_first_peak_radius: float
    rdf_first_peak_value: float
    coordination_cutoff: float
    coordination_number: float
    coordination_block_standard_error: float
    coordination_relative_standard_error: float
    finite_size_shell_fraction: float


@dataclass(frozen=True)
class ObservableVacfSummary:
    """Velocity autocorrelation diagnostics for the largest configured system."""

    system: str
    max_lag: int
    correlation_time_input: float
    normalized_integral: float
    first_zero_lag: int | None
    lag1_autocorrelation: float


@dataclass(frozen=True)
class ArgonTrajectoryObservableSummary:
    """Observable diagnostics from an actual compact argon trajectory."""

    atom_count: int
    frame_count: int
    number_density: float
    temperature: float
    rdf_first_peak_radius: float
    rdf_first_peak_value: float
    coordination_cutoff: float
    coordination_number: float
    uncertainty_block_count: int
    coordination_block_standard_error: float
    coordination_relative_standard_error: float
    uncertainty_replica_count: int
    coordination_replica_standard_error: float
    coordination_replica_min: float
    coordination_replica_max: float
    rdf_first_peak_radius_replica_std: float
    rdf_first_peak_value_replica_std: float
    mean_rdf_replica_std: float
    max_rdf_replica_std: float
    vacf_normalized_integral: float
    vacf_integral_replica_standard_error: float
    vacf_integral_replica_min: float
    vacf_integral_replica_max: float
    mean_vacf_replica_std: float
    max_vacf_replica_std: float
    vacf_first_zero_lag: int | None
    vacf_lag1_autocorrelation: float
    target_device: str
    runtime_device: str
    target_requests_gpu: bool
    production_gpu_ready: bool
    gpu_blocking_reason: str | None


@dataclass(frozen=True)
class ObservableExperimentSummary:
    """Summary table for one post/profile observable-estimator experiment."""

    post: str
    profile: str
    number_density: float
    displacement_sigma: float
    rdf_max_radius: float
    rdf_bin_width: float
    sample_every: int
    seed: int
    config_sha256: str
    systems: list[ObservableSystemSummary]
    vacf: ObservableVacfSummary
    argon_trajectory: ArgonTrajectoryObservableSummary | None = None


def _sample_positions(
    *,
    system: ObservableSystemSpec,
    number_density: float,
    displacement_sigma: float,
    frame_count: int,
    seed: int,
) -> tuple[np.ndarray, float]:
    atoms = argon_fcc(system.repetitions, number_density)
    base_positions = atoms.get_positions()
    cell_lengths = atoms.cell.lengths()
    if not np.allclose(cell_lengths, cell_lengths[0]):
        msg = "observable diagnostics expect a cubic cell"
        raise ValueError(msg)
    cell_length = float(cell_lengths[0])
    rng = np.random.default_rng(seed)
    frames = np.empty((frame_count, len(atoms), 3), dtype=float)
    for frame in range(frame_count):
        displacement = rng.normal(0.0, displacement_sigma, size=base_positions.shape)
        frames[frame] = np.mod(base_positions + displacement, cell_length)
    return frames, cell_length


def _pair_distances(positions: np.ndarray, cell_length: float) -> np.ndarray:
    deltas = positions[:, None, :] - positions[None, :, :]
    deltas -= cell_length * np.round(deltas / cell_length)
    distances = np.sqrt(np.sum(deltas * deltas, axis=-1))
    upper = np.triu_indices(len(positions), k=1)
    return distances[upper]


def estimate_rdf(
    frames: np.ndarray,
    *,
    cell_length: float,
    number_density: float,
    max_radius: float,
    bin_width: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate the radial distribution function from periodic frames."""

    edges = np.arange(0.0, max_radius + bin_width, bin_width)
    counts = np.zeros(len(edges) - 1, dtype=float)
    for positions in frames:
        distances = _pair_distances(positions, cell_length)
        counts += np.histogram(distances, bins=edges)[0]
    radii = 0.5 * (edges[:-1] + edges[1:])
    shell_volumes = (4.0 / 3.0) * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    atom_count = frames.shape[1]
    expected_counts = 0.5 * frames.shape[0] * atom_count * number_density * shell_volumes
    rdf = np.divide(
        counts,
        expected_counts,
        out=np.zeros_like(counts),
        where=expected_counts > 0.0,
    )
    return radii, rdf


def coordination_number(
    radii: np.ndarray,
    rdf: np.ndarray,
    *,
    number_density: float,
    cutoff: float,
    bin_width: float,
) -> float:
    """Integrate RDF into a coordination number up to a radial cutoff."""

    mask = radii <= cutoff
    integrand = 4.0 * np.pi * number_density * rdf[mask] * radii[mask] ** 2
    return float(np.sum(integrand * bin_width))


def _coordination_block_standard_error(
    frames: np.ndarray,
    *,
    cell_length: float,
    number_density: float,
    max_radius: float,
    bin_width: float,
    cutoff: float,
    block_count: int = 6,
) -> float:
    block_size = max(1, frames.shape[0] // block_count)
    estimates = []
    for start in range(0, frames.shape[0] - block_size + 1, block_size):
        block = frames[start : start + block_size]
        radii, rdf = estimate_rdf(
            block,
            cell_length=cell_length,
            number_density=number_density,
            max_radius=max_radius,
            bin_width=bin_width,
        )
        estimates.append(
            coordination_number(
                radii,
                rdf,
                number_density=number_density,
                cutoff=cutoff,
                bin_width=bin_width,
            )
        )
    if len(estimates) < 2:
        return 0.0
    return float(np.std(estimates, ddof=1) / np.sqrt(len(estimates)))


def _simulate_velocities(
    *,
    frame_count: int,
    atom_count: int,
    correlation_time: float,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    phi = float(np.exp(-1.0 / correlation_time))
    noise_scale = float(np.sqrt(1.0 - phi**2))
    velocities = np.empty((frame_count, atom_count, 3), dtype=float)
    velocities[0] = rng.normal(size=(atom_count, 3))
    for frame in range(1, frame_count):
        velocities[frame] = phi * velocities[frame - 1]
        velocities[frame] += noise_scale * rng.normal(size=(atom_count, 3))
    return velocities


def _simulate_argon_trajectory(
    spec: ObservableTutorialSpec,
) -> tuple[np.ndarray, np.ndarray, float] | None:
    argon = spec.argon_trajectory
    if argon is None:
        return None

    atoms = argon_fcc(argon.repetitions, argon.number_density)
    positions = atoms.get_positions().astype(float)
    box = float(atoms.cell.lengths()[0])
    velocities = _initialized_argon_velocities(
        atom_count=len(atoms),
        temperature=argon.temperature,
        seed=argon.seed,
    )
    forces, _ = _lennard_jones_forces(
        positions,
        box_length=box,
        epsilon=argon.epsilon,
        sigma=argon.sigma,
        cutoff=argon.cutoff,
    )
    c = float(np.exp(-argon.gamma * argon.time_step))
    sigma_v = float(np.sqrt(argon.temperature * (1.0 - c**2)))
    rng = np.random.default_rng(argon.seed + 17)
    frame_positions: list[np.ndarray] = []
    frame_velocities: list[np.ndarray] = []

    for step in range(1, argon.num_steps + 1):
        velocities += 0.5 * argon.time_step * forces
        positions = (positions + 0.5 * argon.time_step * velocities) % box
        velocities = c * velocities + sigma_v * rng.normal(size=velocities.shape)
        velocities -= np.mean(velocities, axis=0)
        positions = (positions + 0.5 * argon.time_step * velocities) % box
        forces, _ = _lennard_jones_forces(
            positions,
            box_length=box,
            epsilon=argon.epsilon,
            sigma=argon.sigma,
            cutoff=argon.cutoff,
        )
        velocities += 0.5 * argon.time_step * forces

        if step >= argon.warmup_steps and (step - argon.warmup_steps) % argon.sample_every == 0:
            frame_positions.append(positions.copy())
            frame_velocities.append(velocities.copy())

    return (
        np.asarray(frame_positions, dtype=float),
        np.asarray(frame_velocities, dtype=float),
        box,
    )


def estimate_vacf(velocities: np.ndarray, max_lag: int) -> tuple[np.ndarray, np.ndarray]:
    """Estimate a normalized velocity autocorrelation function."""

    denominator = float(np.mean(np.sum(velocities * velocities, axis=-1)))
    lags = np.arange(max_lag + 1, dtype=int)
    vacf = np.empty(max_lag + 1, dtype=float)
    for lag in lags:
        products = np.sum(velocities[: len(velocities) - lag] * velocities[lag:], axis=-1)
        vacf[lag] = float(np.mean(products) / denominator)
    return lags, vacf


def _summarize_argon_trajectory(
    spec: ObservableTutorialSpec,
) -> tuple[
    ArgonTrajectoryObservableSummary | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
]:
    argon = spec.argon_trajectory
    simulated = _simulate_argon_trajectory(spec)
    if argon is None or simulated is None:
        return None, None, None, None, None
    frames, velocities, cell_length = simulated
    radii, rdf = estimate_rdf(
        frames,
        cell_length=cell_length,
        number_density=argon.number_density,
        max_radius=argon.rdf_max_radius,
        bin_width=argon.rdf_bin_width,
    )
    usable_radius = 0.5 * cell_length
    rdf = np.where(radii <= usable_radius, rdf, np.nan)
    coordination = coordination_number(
        radii,
        rdf,
        number_density=argon.number_density,
        cutoff=argon.coordination_cutoff,
        bin_width=argon.rdf_bin_width,
    )
    block_se = _coordination_block_standard_error(
        frames,
        cell_length=cell_length,
        number_density=argon.number_density,
        max_radius=argon.rdf_max_radius,
        bin_width=argon.rdf_bin_width,
        cutoff=argon.coordination_cutoff,
        block_count=argon.uncertainty_block_count,
    )
    peak_mask = (radii > 0.5 * argon.rdf_bin_width) & (radii <= usable_radius)
    peak_idx = int(np.argmax(rdf[peak_mask]))
    peak_radii = radii[peak_mask]
    peak_values = rdf[peak_mask]

    lags, vacf = estimate_vacf(velocities, argon.max_vacf_lag)
    replica_rdfs = [rdf]
    replica_vacfs = [vacf]
    replica_peak_radii = [float(peak_radii[peak_idx])]
    replica_peak_values = [float(peak_values[peak_idx])]
    replica_coordinations = [coordination]
    replica_vacf_integrals = [float(np.trapezoid(vacf, lags))]
    for replica_idx in range(1, argon.uncertainty_replica_count):
        replica_argon = replace(argon, seed=argon.seed + 1009 * replica_idx)
        replica_simulated = _simulate_argon_trajectory(
            replace(spec, argon_trajectory=replica_argon)
        )
        if replica_simulated is None:
            continue
        replica_frames, replica_velocities, replica_cell_length = replica_simulated
        replica_radii, replica_rdf = estimate_rdf(
            replica_frames,
            cell_length=replica_cell_length,
            number_density=replica_argon.number_density,
            max_radius=replica_argon.rdf_max_radius,
            bin_width=replica_argon.rdf_bin_width,
        )
        replica_usable_radius = 0.5 * replica_cell_length
        replica_rdf = np.where(replica_radii <= replica_usable_radius, replica_rdf, np.nan)
        replica_peak_mask = (
            (replica_radii > 0.5 * replica_argon.rdf_bin_width)
            & (replica_radii <= replica_usable_radius)
        )
        replica_peak_idx = int(np.argmax(replica_rdf[replica_peak_mask]))
        replica_rdfs.append(replica_rdf)
        replica_peak_radii.append(float(replica_radii[replica_peak_mask][replica_peak_idx]))
        replica_peak_values.append(float(replica_rdf[replica_peak_mask][replica_peak_idx]))
        replica_coordinations.append(
            coordination_number(
                replica_radii,
                replica_rdf,
                number_density=replica_argon.number_density,
                cutoff=replica_argon.coordination_cutoff,
                bin_width=replica_argon.rdf_bin_width,
            )
        )
        replica_lags, replica_vacf = estimate_vacf(
            replica_velocities, replica_argon.max_vacf_lag
        )
        replica_vacfs.append(replica_vacf)
        replica_vacf_integrals.append(float(np.trapezoid(replica_vacf, replica_lags)))

    rdf_stack = np.asarray(replica_rdfs, dtype=float)
    finite_count = np.count_nonzero(np.isfinite(rdf_stack), axis=0)
    rdf_replica_std = np.full(rdf_stack.shape[1], np.nan, dtype=float)
    enough_replicas = finite_count >= 2
    if np.any(enough_replicas):
        rdf_replica_std[enough_replicas] = np.nanstd(
            rdf_stack[:, enough_replicas], axis=0, ddof=1
        )
    coordination_replicas = np.asarray(replica_coordinations, dtype=float)
    vacf_stack = np.asarray(replica_vacfs, dtype=float)
    vacf_replica_std = np.std(vacf_stack, axis=0, ddof=1)
    vacf_integral_replicas = np.asarray(replica_vacf_integrals, dtype=float)
    zero_crossings = np.flatnonzero(vacf <= 0.0)
    runtime = runtime_device()
    requests_gpu = target_requests_gpu(argon.target_device)
    production_gpu_ready = requests_gpu and runtime_is_gpu(runtime)
    summary = ArgonTrajectoryObservableSummary(
        atom_count=frames.shape[1],
        frame_count=frames.shape[0],
        number_density=argon.number_density,
        temperature=argon.temperature,
        rdf_first_peak_radius=float(peak_radii[peak_idx]),
        rdf_first_peak_value=float(peak_values[peak_idx]),
        coordination_cutoff=argon.coordination_cutoff,
        coordination_number=coordination,
        uncertainty_block_count=argon.uncertainty_block_count,
        coordination_block_standard_error=block_se,
        coordination_relative_standard_error=float(block_se / coordination),
        uncertainty_replica_count=len(replica_coordinations),
        coordination_replica_standard_error=float(
            np.std(coordination_replicas, ddof=1) / np.sqrt(len(coordination_replicas))
        ),
        coordination_replica_min=float(np.min(coordination_replicas)),
        coordination_replica_max=float(np.max(coordination_replicas)),
        rdf_first_peak_radius_replica_std=float(np.std(replica_peak_radii, ddof=1)),
        rdf_first_peak_value_replica_std=float(np.std(replica_peak_values, ddof=1)),
        mean_rdf_replica_std=float(np.nanmean(rdf_replica_std)),
        max_rdf_replica_std=float(np.nanmax(rdf_replica_std)),
        vacf_normalized_integral=float(np.trapezoid(vacf, lags)),
        vacf_integral_replica_standard_error=float(
            np.std(vacf_integral_replicas, ddof=1) / np.sqrt(len(vacf_integral_replicas))
        ),
        vacf_integral_replica_min=float(np.min(vacf_integral_replicas)),
        vacf_integral_replica_max=float(np.max(vacf_integral_replicas)),
        mean_vacf_replica_std=float(np.mean(vacf_replica_std)),
        max_vacf_replica_std=float(np.max(vacf_replica_std)),
        vacf_first_zero_lag=None if len(zero_crossings) == 0 else int(zero_crossings[0]),
        vacf_lag1_autocorrelation=float(vacf[1]),
        target_device=argon.target_device,
        runtime_device=runtime,
        target_requests_gpu=requests_gpu,
        production_gpu_ready=production_gpu_ready,
        gpu_blocking_reason=gpu_blocking_reason(argon.target_device, runtime),
    )
    return summary, (radii, rdf), (lags.astype(float), vacf), (
        radii,
        rdf_replica_std,
    ), (lags.astype(float), vacf_replica_std)


def _summarize_system(
    *,
    spec: ObservableTutorialSpec,
    system: ObservableSystemSpec,
    seed_offset: int,
) -> tuple[ObservableSystemSummary, tuple[np.ndarray, np.ndarray]]:
    exp = spec.experiment
    frames, cell_length = _sample_positions(
        system=system,
        number_density=exp.number_density,
        displacement_sigma=exp.displacement_sigma,
        frame_count=exp.frame_count,
        seed=exp.seed + seed_offset,
    )
    radii, rdf = estimate_rdf(
        frames,
        cell_length=cell_length,
        number_density=exp.number_density,
        max_radius=exp.rdf_max_radius,
        bin_width=exp.rdf_bin_width,
    )
    usable_radius = 0.5 * cell_length
    rdf = np.where(radii <= usable_radius, rdf, np.nan)
    coordination = coordination_number(
        radii,
        rdf,
        number_density=exp.number_density,
        cutoff=exp.coordination_cutoff,
        bin_width=exp.rdf_bin_width,
    )
    block_se = _coordination_block_standard_error(
        frames,
        cell_length=cell_length,
        number_density=exp.number_density,
        max_radius=exp.rdf_max_radius,
        bin_width=exp.rdf_bin_width,
        cutoff=exp.coordination_cutoff,
    )
    peak_mask = (radii > 0.5 * exp.rdf_bin_width) & (radii <= usable_radius)
    peak_idx = int(np.argmax(rdf[peak_mask]))
    peak_radii = radii[peak_mask]
    peak_values = rdf[peak_mask]
    finite_size_shell_fraction = exp.rdf_max_radius / (0.5 * cell_length)
    summary = ObservableSystemSummary(
        system=system.name,
        repetitions=system.repetitions,
        atom_count=frames.shape[1],
        frame_count=frames.shape[0],
        number_density=exp.number_density,
        cell_length=cell_length,
        rdf_first_peak_radius=float(peak_radii[peak_idx]),
        rdf_first_peak_value=float(peak_values[peak_idx]),
        coordination_cutoff=exp.coordination_cutoff,
        coordination_number=coordination,
        coordination_block_standard_error=block_se,
        coordination_relative_standard_error=float(block_se / coordination),
        finite_size_shell_fraction=finite_size_shell_fraction,
    )
    return summary, (radii, rdf)


def run_observable_experiment(
    spec: ObservableTutorialSpec,
    config_sha256: str,
) -> tuple[
    ObservableExperimentSummary,
    dict[str, tuple[np.ndarray, np.ndarray]],
    tuple[np.ndarray, np.ndarray],
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
]:
    """Run all configured observable-estimator diagnostics."""

    rdf_by_system = {}
    summaries = []
    for idx, system in enumerate(spec.experiment.systems):
        summary, rdf = _summarize_system(
            spec=spec,
            system=system,
            seed_offset=idx * 1009,
        )
        summaries.append(summary)
        rdf_by_system[system.name] = rdf

    largest = max(summaries, key=lambda item: item.atom_count)
    velocities = _simulate_velocities(
        frame_count=spec.experiment.frame_count,
        atom_count=largest.atom_count,
        correlation_time=spec.experiment.velocity_correlation_time,
        seed=spec.experiment.seed + 99173,
    )
    lags, vacf = estimate_vacf(velocities, spec.experiment.max_vacf_lag)
    zero_crossings = np.flatnonzero(vacf <= 0.0)
    vacf_summary = ObservableVacfSummary(
        system=largest.system,
        max_lag=spec.experiment.max_vacf_lag,
        correlation_time_input=spec.experiment.velocity_correlation_time,
        normalized_integral=float(np.trapezoid(vacf, lags)),
        first_zero_lag=None if len(zero_crossings) == 0 else int(zero_crossings[0]),
        lag1_autocorrelation=float(vacf[1]),
    )
    argon_summary, argon_rdf, argon_vacf, argon_rdf_replica_std, argon_vacf_replica_std = (
        _summarize_argon_trajectory(spec)
    )
    return (
        ObservableExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            number_density=spec.experiment.number_density,
            displacement_sigma=spec.experiment.displacement_sigma,
            rdf_max_radius=spec.experiment.rdf_max_radius,
            rdf_bin_width=spec.experiment.rdf_bin_width,
            sample_every=spec.experiment.sample_every,
            seed=spec.experiment.seed,
            config_sha256=config_sha256,
            systems=summaries,
            vacf=vacf_summary,
            argon_trajectory=argon_summary,
        ),
        rdf_by_system,
        (lags.astype(float), vacf),
        argon_rdf,
        argon_vacf,
        argon_rdf_replica_std,
        argon_vacf_replica_std,
    )


def _write_rdf_samples(
    path: Path,
    rdf_by_system: dict[str, tuple[np.ndarray, np.ndarray]],
) -> None:
    names = list(rdf_by_system)
    radii = next(iter(rdf_by_system.values()))[0]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["radius", *[f"{name}_rdf" for name in names]])
        for idx, radius in enumerate(radii):
            writer.writerow(
                [f"{radius:.12g}"]
                + [f"{rdf_by_system[name][1][idx]:.12g}" for name in names]
            )


def _write_vacf_samples(path: Path, lags: np.ndarray, vacf: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["lag", "normalized_vacf"])
        for lag, value in zip(lags, vacf, strict=True):
            writer.writerow([f"{lag:.0f}", f"{value:.12g}"])


def _write_argon_vacf_samples(
    path: Path,
    lags: np.ndarray,
    vacf: np.ndarray,
    vacf_replica_std: np.ndarray | None = None,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        if vacf_replica_std is None:
            writer.writerow(["lag", "normalized_vacf"])
            for lag, value in zip(lags, vacf, strict=True):
                writer.writerow([f"{lag:.0f}", f"{value:.12g}"])
        else:
            writer.writerow(["lag", "normalized_vacf", "vacf_replica_std"])
            for lag, value, std in zip(lags, vacf, vacf_replica_std, strict=True):
                writer.writerow([f"{lag:.0f}", f"{value:.12g}", f"{std:.12g}"])


def _write_argon_rdf_samples(
    path: Path,
    radii: np.ndarray,
    rdf: np.ndarray,
    rdf_replica_std: np.ndarray | None = None,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        if rdf_replica_std is None:
            writer.writerow(["radius", "argon_trajectory_rdf"])
            for radius, value in zip(radii, rdf, strict=True):
                writer.writerow([f"{radius:.12g}", f"{value:.12g}"])
        else:
            writer.writerow(
                ["radius", "argon_trajectory_rdf", "argon_trajectory_rdf_replica_std"]
            )
            for radius, value, std in zip(radii, rdf, rdf_replica_std, strict=True):
                writer.writerow([f"{radius:.12g}", f"{value:.12g}", f"{std:.12g}"])


def write_observable_outputs(
    spec: ObservableTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-07 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    (
        summary,
        rdf_by_system,
        vacf,
        argon_rdf,
        argon_vacf,
        argon_rdf_replica_std,
        argon_vacf_replica_std,
    ) = run_observable_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "observable_summary.json"
    manifest_path = output_dir / "manifest.json"
    rdf_path = output_dir / "rdf_samples.csv"
    vacf_path = output_dir / "vacf_samples.csv"
    argon_rdf_path = output_dir / "argon_trajectory_rdf_samples.csv"
    argon_vacf_path = output_dir / "argon_trajectory_vacf_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_rdf_samples(rdf_path, rdf_by_system)
    _write_vacf_samples(vacf_path, *vacf)
    if argon_rdf is not None and argon_vacf is not None:
        _write_argon_rdf_samples(
            argon_rdf_path,
            argon_rdf[0],
            argon_rdf[1],
            None if argon_rdf_replica_std is None else argon_rdf_replica_std[1],
        )
        _write_argon_vacf_samples(
            argon_vacf_path,
            argon_vacf[0],
            argon_vacf[1],
            None if argon_vacf_replica_std is None else argon_vacf_replica_std[1],
        )
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "rdf_file": rdf_path.name,
        "vacf_file": vacf_path.name,
        "argon_trajectory_rdf_file": (
            argon_rdf_path.name if summary.argon_trajectory is not None else None
        ),
        "argon_trajectory_vacf_file": (
            argon_vacf_path.name if summary.argon_trajectory is not None else None
        ),
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


def load_observable_summary(path: Path) -> ObservableExperimentSummary:
    """Read a previously written post-07 observable summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    systems = [ObservableSystemSummary(**system) for system in data.pop("systems")]
    vacf = ObservableVacfSummary(**data.pop("vacf"))
    argon_trajectory = data.pop("argon_trajectory", None)
    if argon_trajectory is not None:
        argon_trajectory = ArgonTrajectoryObservableSummary(**argon_trajectory)
    return ObservableExperimentSummary(
        systems=systems,
        vacf=vacf,
        argon_trajectory=argon_trajectory,
        **data,
    )
