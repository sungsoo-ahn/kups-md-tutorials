"""Free-energy estimators for post 08."""

from dataclasses import asdict, dataclass, replace
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import (
    ArgonObservableTrajectorySpec,
    FreeEnergyTutorialSpec,
)
from kups_md_tutorials.observables import _summarize_argon_trajectory
from kups_md_tutorials.observables import estimate_rdf
from kups_md_tutorials.observables import _simulate_argon_trajectory
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class FreeEnergyBinSummary:
    """Diagnostics for one histogram bin width."""

    bin_width: float
    bins: int
    occupied_bins: int
    barrier_height: float
    barrier_error: float
    rmse_vs_true: float
    bootstrap_barrier_standard_error: float


@dataclass(frozen=True)
class ArgonRdfPmfSummary:
    """RDF-derived PMF diagnostics from a compact argon trajectory."""

    atom_count: int
    frame_count: int
    number_density: float
    temperature: float
    rdf_first_peak_radius: float
    rdf_first_peak_value: float
    pmf_minimum_radius: float
    pmf_minimum_value: float
    pmf_barrier_height: float
    finite_pmf_bins: int
    masked_low_rdf_bins: int
    uncertainty_block_count: int
    uncertainty_replica_count: int
    mean_block_pmf_sem: float
    max_block_pmf_sem: float
    mean_replica_pmf_std: float
    max_replica_pmf_std: float


@dataclass(frozen=True)
class FreeEnergyExperimentSummary:
    """Summary table for one free-energy experiment."""

    post: str
    profile: str
    temperature: float
    sample_count: int
    seed: int
    domain_min: float
    domain_max: float
    bias_center: float
    bias_strength: float
    config_sha256: str
    true_barrier_height: float
    reweighted_barrier_height: float
    reweighted_barrier_error: float
    rdf_pmf_minimum_radius: float
    rdf_pmf_barrier_height: float
    argon_rdf_pmf: ArgonRdfPmfSummary | None
    bins: list[FreeEnergyBinSummary]


def double_well_potential(values: np.ndarray) -> np.ndarray:
    """Dimensionless double-well potential with minima near +/-1."""

    return (values * values - 1.0) ** 2


def bias_potential(values: np.ndarray, center: float, strength: float) -> np.ndarray:
    """Harmonic sampling bias used for simple reweighting."""

    return 0.5 * strength * (values - center) ** 2


def _normalized_probabilities(energies: np.ndarray, temperature: float) -> np.ndarray:
    weights = np.exp(-(energies - np.min(energies)) / temperature)
    return weights / np.sum(weights)


def sample_grid_distribution(
    *,
    grid: np.ndarray,
    energies: np.ndarray,
    temperature: float,
    sample_count: int,
    seed: int,
) -> np.ndarray:
    """Draw deterministic samples from a tabulated equilibrium distribution."""

    rng = np.random.default_rng(seed)
    probabilities = _normalized_probabilities(energies, temperature)
    return rng.choice(grid, size=sample_count, replace=True, p=probabilities)


def estimate_pmf(
    samples: np.ndarray,
    *,
    temperature: float,
    domain_min: float,
    domain_max: float,
    bin_width: float,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Estimate a shifted PMF from histogrammed samples."""

    edges = np.arange(domain_min, domain_max + bin_width, bin_width)
    counts, edges = np.histogram(samples, bins=edges, weights=weights)
    centers = 0.5 * (edges[:-1] + edges[1:])
    density = counts / (np.sum(counts) * bin_width)
    with np.errstate(divide="ignore"):
        pmf = -temperature * np.log(density)
    finite = np.isfinite(pmf)
    pmf = np.where(finite, pmf - np.nanmin(pmf), np.nan)
    return centers, pmf, counts


def _barrier_height(centers: np.ndarray, pmf: np.ndarray) -> float:
    left_mask = (centers > -1.25) & (centers < -0.75)
    right_mask = (centers > 0.75) & (centers < 1.25)
    barrier_mask = (centers > -0.15) & (centers < 0.15)
    basin = min(float(np.nanmin(pmf[left_mask])), float(np.nanmin(pmf[right_mask])))
    return float(np.nanmin(pmf[barrier_mask]) - basin)


def _pmf_rmse(centers: np.ndarray, pmf: np.ndarray, temperature: float) -> float:
    true_pmf = double_well_potential(centers)
    true_pmf -= np.nanmin(true_pmf)
    finite = np.isfinite(pmf)
    return float(np.sqrt(np.mean((pmf[finite] - true_pmf[finite]) ** 2)))


def _bootstrap_barrier_se(
    samples: np.ndarray,
    *,
    temperature: float,
    domain_min: float,
    domain_max: float,
    bin_width: float,
    replicates: int,
    seed: int,
) -> float:
    rng = np.random.default_rng(seed)
    barriers = []
    for _ in range(replicates):
        resample = samples[rng.integers(0, len(samples), size=len(samples))]
        centers, pmf, _ = estimate_pmf(
            resample,
            temperature=temperature,
            domain_min=domain_min,
            domain_max=domain_max,
            bin_width=bin_width,
        )
        barriers.append(_barrier_height(centers, pmf))
    return float(np.std(barriers, ddof=1))


def _synthetic_rdf_pmf(
    radii: np.ndarray,
    *,
    temperature: float,
    peak_radius: float,
    peak_width: float,
) -> tuple[np.ndarray, np.ndarray]:
    peak = 4.5 * np.exp(-0.5 * ((radii - peak_radius) / peak_width) ** 2)
    shoulder = 1.2 * np.exp(-0.5 * ((radii - 2.0 * peak_radius) / (2.2 * peak_width)) ** 2)
    rdf = np.clip(1.0 + peak + shoulder, 1.0e-12, None)
    pmf = -temperature * np.log(rdf)
    pmf -= np.nanmin(pmf)
    return rdf, pmf


@dataclass(frozen=True)
class _ArgonTrajectoryContainer:
    argon_trajectory: ArgonObservableTrajectorySpec | None


def _rdf_to_shifted_pmf(
    rdf: np.ndarray,
    *,
    temperature: float,
    minimum_rdf: float = 0.05,
) -> tuple[np.ndarray, np.ndarray]:
    valid = np.isfinite(rdf) & (rdf >= minimum_rdf)
    pmf = np.full_like(rdf, np.nan, dtype=float)
    with np.errstate(divide="ignore"):
        pmf[valid] = -temperature * np.log(rdf[valid])
    if np.any(np.isfinite(pmf)):
        pmf -= np.nanmin(pmf)
    return pmf, valid


def _pmf_uncertainty_from_stack(stack: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(stack, dtype=float)
    finite_count = np.count_nonzero(np.isfinite(values), axis=0)
    std = np.full(values.shape[1], np.nan, dtype=float)
    sem = np.full(values.shape[1], np.nan, dtype=float)
    enough = finite_count >= 2
    if np.any(enough):
        std[enough] = np.nanstd(values[:, enough], axis=0, ddof=1)
        sem[enough] = std[enough] / np.sqrt(finite_count[enough])
    return std, sem


def _argon_rdf_pmf(
    spec: ArgonObservableTrajectorySpec | None,
) -> tuple[
    ArgonRdfPmfSummary | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
    tuple[np.ndarray, np.ndarray] | None,
]:
    if spec is None:
        return None, None, None, None, None

    container = _ArgonTrajectoryContainer(spec)
    trajectory_summary, rdf_curve, _ = _summarize_argon_trajectory(container)
    simulated = _simulate_argon_trajectory(container)
    if trajectory_summary is None or rdf_curve is None or simulated is None:
        return None, None, None, None, None

    radii, rdf = rdf_curve
    frames, _, cell_length = simulated
    pmf, valid = _rdf_to_shifted_pmf(rdf, temperature=spec.temperature)
    finite = np.isfinite(pmf)
    minimum_idx = int(np.nanargmin(pmf))

    block_pmfs: list[np.ndarray] = []
    block_size = max(1, frames.shape[0] // spec.uncertainty_block_count)
    for block_idx in range(spec.uncertainty_block_count):
        start = block_idx * block_size
        stop = frames.shape[0] if block_idx == spec.uncertainty_block_count - 1 else start + block_size
        block = frames[start:stop]
        if len(block) < 2:
            continue
        _, block_rdf = estimate_rdf(
            block,
            cell_length=cell_length,
            number_density=spec.number_density,
            max_radius=spec.rdf_max_radius,
            bin_width=spec.rdf_bin_width,
        )
        block_rdf = np.where(np.isfinite(rdf), block_rdf, np.nan)
        block_pmf, _ = _rdf_to_shifted_pmf(block_rdf, temperature=spec.temperature)
        block_pmfs.append(block_pmf)
    _, block_sem = _pmf_uncertainty_from_stack(block_pmfs)

    replica_pmfs: list[np.ndarray] = [pmf]
    for replica_idx in range(1, spec.uncertainty_replica_count):
        replica_spec = replace(spec, seed=spec.seed + 1009 * replica_idx)
        replica_simulated = _simulate_argon_trajectory(
            _ArgonTrajectoryContainer(replica_spec)
        )
        if replica_simulated is None:
            continue
        replica_frames, _, replica_cell = replica_simulated
        _, replica_rdf = estimate_rdf(
            replica_frames,
            cell_length=replica_cell,
            number_density=replica_spec.number_density,
            max_radius=replica_spec.rdf_max_radius,
            bin_width=replica_spec.rdf_bin_width,
        )
        replica_rdf = np.where(np.isfinite(rdf), replica_rdf, np.nan)
        replica_pmf, _ = _rdf_to_shifted_pmf(replica_rdf, temperature=spec.temperature)
        replica_pmfs.append(replica_pmf)
    replica_std, _ = _pmf_uncertainty_from_stack(replica_pmfs)

    summary = ArgonRdfPmfSummary(
        atom_count=trajectory_summary.atom_count,
        frame_count=trajectory_summary.frame_count,
        number_density=trajectory_summary.number_density,
        temperature=trajectory_summary.temperature,
        rdf_first_peak_radius=trajectory_summary.rdf_first_peak_radius,
        rdf_first_peak_value=trajectory_summary.rdf_first_peak_value,
        pmf_minimum_radius=float(radii[minimum_idx]),
        pmf_minimum_value=float(pmf[minimum_idx]),
        pmf_barrier_height=float(np.nanmax(pmf[finite]) - np.nanmin(pmf[finite])),
        finite_pmf_bins=int(np.count_nonzero(finite)),
        masked_low_rdf_bins=int(np.count_nonzero(np.isfinite(rdf) & ~valid)),
        uncertainty_block_count=len(block_pmfs),
        uncertainty_replica_count=len(replica_pmfs),
        mean_block_pmf_sem=float(np.nanmean(block_sem)),
        max_block_pmf_sem=float(np.nanmax(block_sem)),
        mean_replica_pmf_std=float(np.nanmean(replica_std)),
        max_replica_pmf_std=float(np.nanmax(replica_std)),
    )
    return summary, (radii, rdf), (radii, pmf), (radii, block_sem), (radii, replica_std)


def run_free_energy_experiment(
    spec: FreeEnergyTutorialSpec,
    config_sha256: str,
) -> tuple[FreeEnergyExperimentSummary, dict[str, tuple[np.ndarray, np.ndarray]]]:
    """Run all configured free-energy diagnostics."""

    exp = spec.experiment
    grid = np.linspace(exp.domain_min, exp.domain_max, exp.grid_points)
    true_energy = double_well_potential(grid)
    unbiased = sample_grid_distribution(
        grid=grid,
        energies=true_energy,
        temperature=exp.temperature,
        sample_count=exp.sample_count,
        seed=exp.seed,
    )
    biased_energy = true_energy + bias_potential(grid, exp.bias_center, exp.bias_strength)
    biased = sample_grid_distribution(
        grid=grid,
        energies=biased_energy,
        temperature=exp.temperature,
        sample_count=exp.sample_count,
        seed=exp.seed + 1009,
    )
    curves: dict[str, tuple[np.ndarray, np.ndarray]] = {"true_pmf": (grid, true_energy - np.min(true_energy))}
    true_barrier = float(double_well_potential(np.array([0.0]))[0])

    bin_summaries = []
    for idx, bin_width in enumerate(exp.bin_widths):
        centers, pmf, counts = estimate_pmf(
            unbiased,
            temperature=exp.temperature,
            domain_min=exp.domain_min,
            domain_max=exp.domain_max,
            bin_width=bin_width,
        )
        barrier = _barrier_height(centers, pmf)
        bin_summaries.append(
            FreeEnergyBinSummary(
                bin_width=bin_width,
                bins=len(centers),
                occupied_bins=int(np.count_nonzero(counts)),
                barrier_height=barrier,
                barrier_error=float(barrier - true_barrier),
                rmse_vs_true=_pmf_rmse(centers, pmf, exp.temperature),
                bootstrap_barrier_standard_error=_bootstrap_barrier_se(
                    unbiased,
                    temperature=exp.temperature,
                    domain_min=exp.domain_min,
                    domain_max=exp.domain_max,
                    bin_width=bin_width,
                    replicates=exp.bootstrap_replicates,
                    seed=exp.seed + 17 + idx,
                ),
            )
        )
        if idx == 0:
            curves["histogram_pmf"] = (centers, pmf)

    weights = np.exp(bias_potential(biased, exp.bias_center, exp.bias_strength) / exp.temperature)
    centers, reweighted_pmf, _ = estimate_pmf(
        biased,
        temperature=exp.temperature,
        domain_min=exp.domain_min,
        domain_max=exp.domain_max,
        bin_width=exp.bin_widths[0],
        weights=weights,
    )
    reweighted_barrier = _barrier_height(centers, reweighted_pmf)
    curves["reweighted_pmf"] = (centers, reweighted_pmf)

    radii = np.linspace(0.5, 3.2, 240)
    rdf, rdf_pmf = _synthetic_rdf_pmf(
        radii,
        temperature=exp.temperature,
        peak_radius=exp.rdf_peak_radius,
        peak_width=exp.rdf_peak_width,
    )
    curves["rdf"] = (radii, rdf)
    curves["rdf_pmf"] = (radii, rdf_pmf)
    argon_summary, argon_rdf, argon_pmf, argon_block_sem, argon_replica_std = _argon_rdf_pmf(
        spec.argon_rdf_pmf
    )
    if argon_rdf is not None and argon_pmf is not None:
        curves["argon_rdf"] = argon_rdf
        curves["argon_rdf_pmf"] = argon_pmf
    if argon_block_sem is not None:
        curves["argon_rdf_pmf_block_sem"] = argon_block_sem
    if argon_replica_std is not None:
        curves["argon_rdf_pmf_replica_std"] = argon_replica_std

    return (
        FreeEnergyExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=exp.temperature,
            sample_count=exp.sample_count,
            seed=exp.seed,
            domain_min=exp.domain_min,
            domain_max=exp.domain_max,
            bias_center=exp.bias_center,
            bias_strength=exp.bias_strength,
            config_sha256=config_sha256,
            true_barrier_height=true_barrier,
            reweighted_barrier_height=reweighted_barrier,
            reweighted_barrier_error=float(reweighted_barrier - true_barrier),
            rdf_pmf_minimum_radius=float(radii[int(np.nanargmin(rdf_pmf))]),
            rdf_pmf_barrier_height=float(np.nanmax(rdf_pmf) - np.nanmin(rdf_pmf)),
            argon_rdf_pmf=argon_summary,
            bins=bin_summaries,
        ),
        curves,
    )


def _write_curves(path: Path, curves: dict[str, tuple[np.ndarray, np.ndarray]]) -> None:
    names = list(curves)
    max_len = max(len(values[0]) for values in curves.values())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        header = []
        for name in names:
            header.extend([f"{name}_x", f"{name}_y"])
        writer.writerow(header)
        for idx in range(max_len):
            row: list[str] = []
            for name in names:
                x, y = curves[name]
                if idx < len(x):
                    row.extend([f"{x[idx]:.12g}", f"{y[idx]:.12g}"])
                else:
                    row.extend(["", ""])
            writer.writerow(row)


def write_free_energy_outputs(
    spec: FreeEnergyTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-08 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, curves = run_free_energy_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "free_energy_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "free_energy_curves.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_curves(curves_path, curves)
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


def load_free_energy_summary(path: Path) -> FreeEnergyExperimentSummary:
    """Read a previously written post-08 free-energy summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    bins = [FreeEnergyBinSummary(**item) for item in data.pop("bins")]
    argon_rdf_pmf = data.pop("argon_rdf_pmf", None)
    if argon_rdf_pmf is not None:
        argon_rdf_pmf = ArgonRdfPmfSummary(**argon_rdf_pmf)
    return FreeEnergyExperimentSummary(
        bins=bins,
        argon_rdf_pmf=argon_rdf_pmf,
        **data,
    )
