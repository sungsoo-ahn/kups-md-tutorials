"""Umbrella-sampling diagnostics for post 10."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import UmbrellaProtocolSpec, UmbrellaTutorialSpec
from kups_md_tutorials.free_energies import double_well_potential
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class UmbrellaWindowSummary:
    """Diagnostics for one umbrella window."""

    center: float
    sample_mean: float
    sample_std: float
    replica_mean_difference: float
    effective_bins: int


@dataclass(frozen=True)
class UmbrellaProtocolSummary:
    """Compact diagnostics for one window-placement protocol."""

    protocol: str
    force_constant: float
    window_count: int
    reconstructed_barrier_height: float
    barrier_error: float
    pmf_rmse_vs_true: float
    min_adjacent_overlap: float
    mean_adjacent_overlap: float
    forward_reverse_pmf_rmse: float
    max_replica_mean_difference: float
    min_effective_bins: int
    windows: list[UmbrellaWindowSummary]


@dataclass(frozen=True)
class UmbrellaExperimentSummary:
    """Summary table for one post/profile umbrella experiment."""

    post: str
    profile: str
    temperature: float
    sample_count_per_window: int
    seed: int
    domain_min: float
    domain_max: float
    bin_width: float
    config_sha256: str
    true_barrier_height: float
    protocols: list[UmbrellaProtocolSummary]


def umbrella_bias(values: np.ndarray, center: float, force_constant: float) -> np.ndarray:
    """Dimensionless harmonic umbrella bias."""

    return 0.5 * force_constant * (values - center) ** 2


def _normalized_probabilities(energies: np.ndarray, temperature: float) -> np.ndarray:
    weights = np.exp(-(energies - np.min(energies)) / temperature)
    return weights / np.sum(weights)


def _sample_window(
    *,
    grid: np.ndarray,
    center: float,
    force_constant: float,
    temperature: float,
    sample_count: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    energies = double_well_potential(grid) + umbrella_bias(
        grid,
        center,
        force_constant,
    )
    probabilities = _normalized_probabilities(energies, temperature)
    return rng.choice(grid, size=sample_count, replace=True, p=probabilities)


def _histograms(
    samples_by_window: list[np.ndarray],
    *,
    domain_min: float,
    domain_max: float,
    bin_width: float,
) -> tuple[np.ndarray, np.ndarray]:
    edges = np.arange(domain_min, domain_max + bin_width, bin_width)
    centers = 0.5 * (edges[:-1] + edges[1:])
    counts = np.vstack(
        [np.histogram(samples, bins=edges)[0].astype(float) for samples in samples_by_window]
    )
    return centers, counts


def _wham_reconstruct(
    *,
    centers: np.ndarray,
    counts: np.ndarray,
    window_centers: tuple[float, ...],
    force_constant: float,
    temperature: float,
    bin_width: float,
    max_iterations: int = 10000,
    tolerance: float = 1.0e-11,
) -> np.ndarray:
    beta = 1.0 / temperature
    sample_counts = counts.sum(axis=1)
    biases = np.vstack(
        [umbrella_bias(centers, center, force_constant) for center in window_centers]
    )
    free_offsets = np.zeros(len(window_centers), dtype=float)
    total_counts = counts.sum(axis=0)

    for _ in range(max_iterations):
        denominator = np.sum(
            sample_counts[:, None] * np.exp(beta * free_offsets[:, None] - beta * biases),
            axis=0,
        )
        probability_density = np.divide(
            total_counts,
            denominator,
            out=np.zeros_like(total_counts),
            where=denominator > 0.0,
        )
        norm = np.sum(probability_density) * bin_width
        if norm <= 0.0:
            msg = "WHAM reconstruction produced zero probability"
            raise ValueError(msg)
        probability_density /= norm

        new_offsets = np.empty_like(free_offsets)
        for idx in range(len(window_centers)):
            biased_norm = np.sum(
                probability_density * np.exp(-beta * biases[idx]) * bin_width
            )
            new_offsets[idx] = -temperature * np.log(max(biased_norm, 1.0e-300))
        new_offsets -= new_offsets[0]
        if np.max(np.abs(new_offsets - free_offsets)) < tolerance:
            free_offsets = new_offsets
            break
        free_offsets = new_offsets

    with np.errstate(divide="ignore"):
        pmf = -temperature * np.log(probability_density)
    finite = np.isfinite(pmf)
    pmf = np.where(finite, pmf - np.nanmin(pmf), np.nan)
    return pmf


def _barrier_height(centers: np.ndarray, pmf: np.ndarray) -> float:
    left_mask = (centers > -1.25) & (centers < -0.75)
    right_mask = (centers > 0.75) & (centers < 1.25)
    barrier_mask = (centers > -0.15) & (centers < 0.15)
    basin = min(float(np.nanmin(pmf[left_mask])), float(np.nanmin(pmf[right_mask])))
    return float(np.nanmin(pmf[barrier_mask]) - basin)


def _pmf_rmse(centers: np.ndarray, pmf: np.ndarray) -> float:
    true_pmf = double_well_potential(centers)
    true_pmf -= np.nanmin(true_pmf)
    finite = np.isfinite(pmf)
    return float(np.sqrt(np.mean((pmf[finite] - true_pmf[finite]) ** 2)))


def _overlap_coefficients(counts: np.ndarray) -> list[float]:
    densities = counts / np.maximum(counts.sum(axis=1, keepdims=True), 1.0)
    return [
        float(np.sum(np.minimum(densities[idx], densities[idx + 1])))
        for idx in range(counts.shape[0] - 1)
    ]


def _summarize_protocol(
    *,
    protocol: UmbrellaProtocolSpec,
    grid: np.ndarray,
    temperature: float,
    domain_min: float,
    domain_max: float,
    bin_width: float,
    sample_count_per_window: int,
    seed: int,
) -> tuple[UmbrellaProtocolSummary, dict[str, np.ndarray]]:
    samples_by_window = []
    replica_samples_by_window = []
    for idx, center in enumerate(protocol.window_centers):
        samples_by_window.append(
            _sample_window(
                grid=grid,
                center=center,
                force_constant=protocol.force_constant,
                temperature=temperature,
                sample_count=sample_count_per_window,
                seed=seed + idx * 1009,
            )
        )
        replica_samples_by_window.append(
            _sample_window(
                grid=grid,
                center=center,
                force_constant=protocol.force_constant,
                temperature=temperature,
                sample_count=sample_count_per_window,
                seed=seed + 50021 + idx * 1009,
            )
        )

    centers, counts = _histograms(
        samples_by_window,
        domain_min=domain_min,
        domain_max=domain_max,
        bin_width=bin_width,
    )
    pmf = _wham_reconstruct(
        centers=centers,
        counts=counts,
        window_centers=protocol.window_centers,
        force_constant=protocol.force_constant,
        temperature=temperature,
        bin_width=bin_width,
    )

    _, replica_counts = _histograms(
        replica_samples_by_window,
        domain_min=domain_min,
        domain_max=domain_max,
        bin_width=bin_width,
    )
    replica_pmf = _wham_reconstruct(
        centers=centers,
        counts=replica_counts,
        window_centers=protocol.window_centers,
        force_constant=protocol.force_constant,
        temperature=temperature,
        bin_width=bin_width,
    )

    overlap = _overlap_coefficients(counts)
    barrier = _barrier_height(centers, pmf)
    true_barrier = float(double_well_potential(np.array([0.0]))[0])
    window_summaries = []
    for idx, center in enumerate(protocol.window_centers):
        samples = samples_by_window[idx]
        replica = replica_samples_by_window[idx]
        window_summaries.append(
            UmbrellaWindowSummary(
                center=center,
                sample_mean=float(np.mean(samples)),
                sample_std=float(np.std(samples, ddof=1)),
                replica_mean_difference=float(abs(np.mean(samples) - np.mean(replica))),
                effective_bins=int(np.count_nonzero(counts[idx])),
            )
        )

    return (
        UmbrellaProtocolSummary(
            protocol=protocol.name,
            force_constant=protocol.force_constant,
            window_count=len(protocol.window_centers),
            reconstructed_barrier_height=barrier,
            barrier_error=float(barrier - true_barrier),
            pmf_rmse_vs_true=_pmf_rmse(centers, pmf),
            min_adjacent_overlap=float(min(overlap)),
            mean_adjacent_overlap=float(np.mean(overlap)),
            forward_reverse_pmf_rmse=float(np.sqrt(np.nanmean((pmf - replica_pmf) ** 2))),
            max_replica_mean_difference=max(
                item.replica_mean_difference for item in window_summaries
            ),
            min_effective_bins=min(item.effective_bins for item in window_summaries),
            windows=window_summaries,
        ),
        {
            "centers": centers,
            "pmf": pmf,
            "replica_pmf": replica_pmf,
            "overlap": np.array(overlap, dtype=float),
            "window_centers": np.array(protocol.window_centers, dtype=float),
            "window_means": np.array(
                [item.sample_mean for item in window_summaries],
                dtype=float,
            ),
            "window_stds": np.array(
                [item.sample_std for item in window_summaries],
                dtype=float,
            ),
        },
    )


def run_umbrella_experiment(
    spec: UmbrellaTutorialSpec,
    config_sha256: str,
) -> tuple[UmbrellaExperimentSummary, dict[str, dict[str, np.ndarray]]]:
    """Run all configured umbrella-sampling diagnostics."""

    exp = spec.experiment
    grid = np.linspace(exp.domain_min, exp.domain_max, exp.grid_points)
    protocol_summaries = []
    curves = {}
    for idx, protocol in enumerate(exp.protocols):
        summary, protocol_curves = _summarize_protocol(
            protocol=protocol,
            grid=grid,
            temperature=exp.temperature,
            domain_min=exp.domain_min,
            domain_max=exp.domain_max,
            bin_width=exp.bin_width,
            sample_count_per_window=exp.sample_count_per_window,
            seed=exp.seed + idx * 1000003,
        )
        protocol_summaries.append(summary)
        curves[protocol.name] = protocol_curves

    return (
        UmbrellaExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=exp.temperature,
            sample_count_per_window=exp.sample_count_per_window,
            seed=exp.seed,
            domain_min=exp.domain_min,
            domain_max=exp.domain_max,
            bin_width=exp.bin_width,
            config_sha256=config_sha256,
            true_barrier_height=float(double_well_potential(np.array([0.0]))[0]),
            protocols=protocol_summaries,
        ),
        curves,
    )


def _write_umbrella_curves(
    path: Path,
    curves: dict[str, dict[str, np.ndarray]],
) -> None:
    protocol_names = list(curves)
    max_len = max(len(item["centers"]) for item in curves.values())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = ["true_x", "true_pmf"]
        for name in protocol_names:
            header.extend([f"{name}_x", f"{name}_pmf", f"{name}_replica_pmf"])
        writer.writerow(header)
        true_x = curves[protocol_names[0]]["centers"]
        true_pmf = double_well_potential(true_x)
        true_pmf -= np.nanmin(true_pmf)
        for idx in range(max_len):
            row = [
                f"{true_x[idx]:.12g}" if idx < len(true_x) else "",
                f"{true_pmf[idx]:.12g}" if idx < len(true_pmf) else "",
            ]
            for name in protocol_names:
                protocol = curves[name]
                if idx < len(protocol["centers"]):
                    row.extend(
                        [
                            f"{protocol['centers'][idx]:.12g}",
                            f"{protocol['pmf'][idx]:.12g}",
                            f"{protocol['replica_pmf'][idx]:.12g}",
                        ]
                    )
                else:
                    row.extend(["", "", ""])
            writer.writerow(row)


def _write_umbrella_windows(
    path: Path,
    curves: dict[str, dict[str, np.ndarray]],
) -> None:
    max_len = max(len(item["window_centers"]) for item in curves.values())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = []
        for name in curves:
            header.extend(
                [
                    f"{name}_window_center",
                    f"{name}_sample_mean",
                    f"{name}_sample_std",
                    f"{name}_adjacent_overlap",
                ]
            )
        writer.writerow(header)
        for idx in range(max_len):
            row: list[str] = []
            for protocol in curves.values():
                if idx < len(protocol["window_centers"]):
                    overlap = (
                        f"{protocol['overlap'][idx]:.12g}"
                        if idx < len(protocol["overlap"])
                        else ""
                    )
                    row.extend(
                        [
                            f"{protocol['window_centers'][idx]:.12g}",
                            f"{protocol['window_means'][idx]:.12g}",
                            f"{protocol['window_stds'][idx]:.12g}",
                            overlap,
                        ]
                    )
                else:
                    row.extend(["", "", "", ""])
            writer.writerow(row)


def write_umbrella_outputs(
    spec: UmbrellaTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-10 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, curves = run_umbrella_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "umbrella_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "umbrella_curves.csv"
    windows_path = output_dir / "umbrella_windows.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_umbrella_curves(curves_path, curves)
    _write_umbrella_windows(windows_path, curves)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "curves_file": curves_path.name,
        "windows_file": windows_path.name,
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


def load_umbrella_summary(path: Path) -> UmbrellaExperimentSummary:
    """Read a previously written post-10 umbrella summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    protocols = []
    for item in data.pop("protocols"):
        windows = [UmbrellaWindowSummary(**window) for window in item.pop("windows")]
        protocols.append(UmbrellaProtocolSummary(windows=windows, **item))
    return UmbrellaExperimentSummary(protocols=protocols, **data)
