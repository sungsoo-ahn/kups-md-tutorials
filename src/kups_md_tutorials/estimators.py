"""Free-energy estimator diagnostics for post 09."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import (
    EstimatorCase,
    EstimatorTutorialSpec,
    MultiStateOverlapSpec,
    MultiStateProtocolSpec,
)
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class EstimatorCaseSummary:
    """Compact diagnostics for one two-state estimator comparison."""

    case: str
    mean_shift: float
    true_delta_f: float
    forward_fep_delta_f: float
    reverse_fep_delta_f: float
    bar_delta_f: float
    forward_fep_error: float
    reverse_fep_error: float
    bar_error: float
    overlap_coefficient: float
    forward_weight_ess_fraction: float
    reverse_weight_ess_fraction: float
    forward_work_mean: float
    reverse_work_mean: float
    forward_work_std: float
    reverse_work_std: float


@dataclass(frozen=True)
class EstimatorExperimentSummary:
    """Summary table for one post/profile estimator experiment."""

    post: str
    profile: str
    temperature: float
    sample_count: int
    seed: int
    config_sha256: str
    cases: list[EstimatorCaseSummary]
    multistate_protocols: list["MultiStateProtocolSummary"] | None = None


@dataclass(frozen=True)
class MultiStateProtocolSummary:
    """Compact diagnostics for one WHAM/MBAR-style bridge layout."""

    protocol: str
    window_count: int
    sample_count_per_window: int
    force_constant: float
    min_adjacent_overlap: float
    mean_adjacent_overlap: float
    disconnected_edges: int
    finite_pmf_bins: int
    pmf_rmse_vs_true: float
    max_pmf_abs_error: float


def reduced_potential_a(values: np.ndarray) -> np.ndarray:
    """Reduced potential for state A."""

    return 0.5 * values * values


def reduced_potential_b(
    values: np.ndarray,
    *,
    mean_shift: float,
    true_delta_f: float,
) -> np.ndarray:
    """Reduced potential for state B with known partition-function offset."""

    return 0.5 * (values - mean_shift) ** 2 + true_delta_f


def _fep_forward(work: np.ndarray) -> float:
    shifted = work - np.min(work)
    return float(np.min(work) - np.log(np.mean(np.exp(-shifted))))


def _fep_reverse(reverse_work: np.ndarray) -> float:
    shifted = reverse_work - np.min(reverse_work)
    return float(-(np.min(reverse_work) - np.log(np.mean(np.exp(-shifted)))))


def _ess_fraction(log_weights: np.ndarray) -> float:
    shifted = log_weights - np.max(log_weights)
    weights = np.exp(shifted)
    ess = np.sum(weights) ** 2 / np.sum(weights * weights)
    return float(ess / len(weights))


def _bar_delta_f(forward_work: np.ndarray, reverse_work: np.ndarray) -> float:
    lo = min(float(np.min(forward_work)), float(-np.max(reverse_work))) - 10.0
    hi = max(float(np.max(forward_work)), float(-np.min(reverse_work))) + 10.0

    def residual(delta_f: float) -> float:
        left = np.mean(1.0 / (1.0 + np.exp(forward_work - delta_f)))
        right = np.mean(1.0 / (1.0 + np.exp(reverse_work + delta_f)))
        return float(left - right)

    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if residual(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def _normal_pdf(values: np.ndarray, mean: float) -> np.ndarray:
    return np.exp(-0.5 * (values - mean) ** 2) / np.sqrt(2.0 * np.pi)


def _overlap_coefficient(mean_shift: float) -> float:
    grid = np.linspace(-8.0, 8.0 + mean_shift, 4000)
    overlap = np.minimum(_normal_pdf(grid, 0.0), _normal_pdf(grid, mean_shift))
    return float(np.trapezoid(overlap, grid))


def _biased_window_samples(
    *,
    center: float,
    force_constant: float,
    sample_count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    precision = 1.0 + force_constant
    mean = force_constant * center / precision
    std = np.sqrt(1.0 / precision)
    return rng.normal(mean, std, size=sample_count)


def _target_pmf(centers: np.ndarray) -> np.ndarray:
    pmf = 0.5 * centers * centers
    return pmf - np.min(pmf)


def _window_histogram(
    values: np.ndarray,
    edges: np.ndarray,
) -> np.ndarray:
    counts, _ = np.histogram(values, bins=edges)
    total = np.sum(counts)
    if total == 0:
        return np.zeros(len(edges) - 1, dtype=float)
    return counts.astype(float) / total


def _window_overlap(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.sum(np.minimum(left, right)))


def _reconstruct_target_pmf(
    *,
    samples_by_window: list[np.ndarray],
    window_centers: tuple[float, ...],
    force_constant: float,
    edges: np.ndarray,
) -> np.ndarray:
    bin_centers = 0.5 * (edges[:-1] + edges[1:])
    estimates = []
    for center, samples in zip(window_centers, samples_by_window, strict=True):
        counts, _ = np.histogram(samples, bins=edges)
        probability = counts.astype(float) / np.sum(counts)
        bias = 0.5 * force_constant * (bin_centers - center) ** 2
        bridge_constant = (1.0 / np.sqrt(1.0 + force_constant)) * np.exp(
            -0.5 * force_constant * center * center / (1.0 + force_constant)
        )
        unnormalized = probability * np.exp(bias) * bridge_constant
        estimates.append(unnormalized)

    stacked = np.vstack(estimates)
    supported = stacked > 0.0
    support_count = np.sum(supported, axis=0)
    combined = np.full(stacked.shape[1], np.nan, dtype=float)
    valid = support_count > 0
    combined[valid] = np.sum(stacked[:, valid], axis=0) / support_count[valid]
    combined_sum = np.nansum(combined)
    if combined_sum <= 0.0:
        return np.full_like(combined, np.nan)
    combined = combined / combined_sum
    pmf = np.full_like(combined, np.nan)
    positive = combined > 0.0
    pmf[positive] = -np.log(combined[positive])
    if np.any(np.isfinite(pmf)):
        pmf = pmf - np.nanmin(pmf)
    return pmf


def _summarize_multistate_protocol(
    *,
    protocol: MultiStateProtocolSpec,
    spec: MultiStateOverlapSpec,
    seed: int,
) -> tuple[MultiStateProtocolSummary, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    edges = np.arange(
        spec.domain_min,
        spec.domain_max + spec.bin_width * 0.5,
        spec.bin_width,
    )
    bin_centers = 0.5 * (edges[:-1] + edges[1:])
    samples_by_window = [
        _biased_window_samples(
            center=center,
            force_constant=spec.force_constant,
            sample_count=spec.sample_count_per_window,
            rng=rng,
        )
        for center in protocol.window_centers
    ]
    histograms = [_window_histogram(samples, edges) for samples in samples_by_window]
    adjacent_overlap = np.array(
        [
            _window_overlap(left, right)
            for left, right in zip(histograms[:-1], histograms[1:], strict=False)
        ],
        dtype=float,
    )
    reconstructed_pmf = _reconstruct_target_pmf(
        samples_by_window=samples_by_window,
        window_centers=protocol.window_centers,
        force_constant=spec.force_constant,
        edges=edges,
    )
    true_pmf = _target_pmf(bin_centers)
    finite = np.isfinite(reconstructed_pmf)
    unsupported_penalty = float(np.max(true_pmf) + 1.0)
    errors = np.full_like(true_pmf, unsupported_penalty)
    errors[finite] = reconstructed_pmf[finite] - true_pmf[finite]
    rmse = float(np.sqrt(np.mean(errors * errors)))
    max_abs = float(np.max(np.abs(errors)))
    summary = MultiStateProtocolSummary(
        protocol=protocol.name,
        window_count=len(protocol.window_centers),
        sample_count_per_window=spec.sample_count_per_window,
        force_constant=spec.force_constant,
        min_adjacent_overlap=float(np.min(adjacent_overlap)),
        mean_adjacent_overlap=float(np.mean(adjacent_overlap)),
        disconnected_edges=int(np.sum(adjacent_overlap < 0.01)),
        finite_pmf_bins=int(np.sum(finite)),
        pmf_rmse_vs_true=rmse,
        max_pmf_abs_error=max_abs,
    )
    return summary, bin_centers, true_pmf, reconstructed_pmf, adjacent_overlap


def _summarize_multistate_overlap(
    spec: MultiStateOverlapSpec,
) -> tuple[
    list[MultiStateProtocolSummary],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
]:
    summaries = []
    curves: dict[str, np.ndarray] = {}
    windows: dict[str, np.ndarray] = {}
    for idx, protocol in enumerate(spec.protocols):
        (
            summary,
            centers,
            true_pmf,
            reconstructed_pmf,
            adjacent_overlap,
        ) = _summarize_multistate_protocol(
            protocol=protocol,
            spec=spec,
            seed=spec.seed + idx * 1009,
        )
        summaries.append(summary)
        curves["coordinate"] = centers
        curves["true_pmf"] = true_pmf
        curves[f"{protocol.name}_pmf"] = reconstructed_pmf
        windows[f"{protocol.name}_center"] = np.array(protocol.window_centers, dtype=float)
        windows[f"{protocol.name}_adjacent_overlap"] = adjacent_overlap
    return summaries, curves, windows


def _summarize_case(
    *,
    case: EstimatorCase,
    sample_count: int,
    seed: int,
) -> tuple[EstimatorCaseSummary, tuple[np.ndarray, np.ndarray]]:
    rng = np.random.default_rng(seed)
    samples_a = rng.normal(0.0, 1.0, size=sample_count)
    samples_b = rng.normal(case.mean_shift, 1.0, size=sample_count)
    forward_work = reduced_potential_b(
        samples_a,
        mean_shift=case.mean_shift,
        true_delta_f=case.true_delta_f,
    ) - reduced_potential_a(samples_a)
    reverse_work = reduced_potential_a(samples_b) - reduced_potential_b(
        samples_b,
        mean_shift=case.mean_shift,
        true_delta_f=case.true_delta_f,
    )
    forward = _fep_forward(forward_work)
    reverse = _fep_reverse(reverse_work)
    bar = _bar_delta_f(forward_work, reverse_work)
    summary = EstimatorCaseSummary(
        case=case.name,
        mean_shift=case.mean_shift,
        true_delta_f=case.true_delta_f,
        forward_fep_delta_f=forward,
        reverse_fep_delta_f=reverse,
        bar_delta_f=bar,
        forward_fep_error=float(forward - case.true_delta_f),
        reverse_fep_error=float(reverse - case.true_delta_f),
        bar_error=float(bar - case.true_delta_f),
        overlap_coefficient=_overlap_coefficient(case.mean_shift),
        forward_weight_ess_fraction=_ess_fraction(-forward_work),
        reverse_weight_ess_fraction=_ess_fraction(-reverse_work),
        forward_work_mean=float(np.mean(forward_work)),
        reverse_work_mean=float(np.mean(reverse_work)),
        forward_work_std=float(np.std(forward_work, ddof=1)),
        reverse_work_std=float(np.std(reverse_work, ddof=1)),
    )
    return summary, (forward_work, reverse_work)


def run_estimator_experiment(
    spec: EstimatorTutorialSpec,
    config_sha256: str,
) -> tuple[
    EstimatorExperimentSummary,
    dict[str, tuple[np.ndarray, np.ndarray]],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
]:
    """Run all configured free-energy estimator diagnostics."""

    summaries = []
    work_samples = {}
    for idx, case in enumerate(spec.experiment.cases):
        summary, samples = _summarize_case(
            case=case,
            sample_count=spec.experiment.sample_count,
            seed=spec.experiment.seed + idx * 1009,
        )
        summaries.append(summary)
        work_samples[case.name] = samples
    multistate_summaries = None
    multistate_curves: dict[str, np.ndarray] = {}
    multistate_windows: dict[str, np.ndarray] = {}
    if spec.multistate_overlap is not None:
        (
            multistate_summaries,
            multistate_curves,
            multistate_windows,
        ) = _summarize_multistate_overlap(spec.multistate_overlap)
    return (
        EstimatorExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=spec.experiment.temperature,
            sample_count=spec.experiment.sample_count,
            seed=spec.experiment.seed,
            config_sha256=config_sha256,
            cases=summaries,
            multistate_protocols=multistate_summaries,
        ),
        work_samples,
        multistate_curves,
        multistate_windows,
    )


def _write_work_samples(
    path: Path,
    work_samples: dict[str, tuple[np.ndarray, np.ndarray]],
    max_rows: int = 900,
) -> None:
    first = next(iter(work_samples.values()))[0]
    stride = max(1, int(np.ceil(len(first) / max_rows)))
    names = list(work_samples)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        header = []
        for name in names:
            header.extend([f"{name}_forward_work", f"{name}_reverse_work"])
        writer.writerow(header)
        for idx in range(0, len(first), stride):
            row: list[str] = []
            for name in names:
                forward, reverse = work_samples[name]
                row.extend([f"{forward[idx]:.12g}", f"{reverse[idx]:.12g}"])
            writer.writerow(row)


def _write_array_table(path: Path, values: dict[str, np.ndarray]) -> None:
    names = list(values)
    if not names:
        return
    row_count = max(len(array) for array in values.values())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(names)
        for idx in range(row_count):
            row = []
            for name in names:
                array = values[name]
                if idx >= len(array) or not np.isfinite(array[idx]):
                    row.append("")
                else:
                    row.append(f"{array[idx]:.12g}")
            writer.writerow(row)


def write_estimator_outputs(
    spec: EstimatorTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-09 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, work_samples, multistate_curves, multistate_windows = (
        run_estimator_experiment(spec, prov.config_sha256)
    )

    summary_path = output_dir / "estimator_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "work_samples.csv"
    curves_path = output_dir / "multistate_curves.csv"
    windows_path = output_dir / "multistate_windows.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_work_samples(samples_path, work_samples)
    if multistate_curves:
        _write_array_table(curves_path, multistate_curves)
    if multistate_windows:
        _write_array_table(windows_path, multistate_windows)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
        "multistate_curves_file": curves_path.name if multistate_curves else None,
        "multistate_windows_file": windows_path.name if multistate_windows else None,
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


def load_estimator_summary(path: Path) -> EstimatorExperimentSummary:
    """Read a previously written post-09 estimator summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    cases = [EstimatorCaseSummary(**item) for item in data.pop("cases")]
    protocols = data.pop("multistate_protocols", None)
    multistate_protocols = (
        [MultiStateProtocolSummary(**item) for item in protocols]
        if protocols is not None
        else None
    )
    return EstimatorExperimentSummary(
        cases=cases,
        multistate_protocols=multistate_protocols,
        **data,
    )
