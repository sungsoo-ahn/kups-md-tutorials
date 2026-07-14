"""Free-energy estimator diagnostics for post 09."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import EstimatorCase, EstimatorTutorialSpec
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
    return float(np.trapezoid(np.minimum(_normal_pdf(grid, 0.0), _normal_pdf(grid, mean_shift)), grid))


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
) -> tuple[EstimatorExperimentSummary, dict[str, tuple[np.ndarray, np.ndarray]]]:
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
    return (
        EstimatorExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=spec.experiment.temperature,
            sample_count=spec.experiment.sample_count,
            seed=spec.experiment.seed,
            config_sha256=config_sha256,
            cases=summaries,
        ),
        work_samples,
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
        writer = csv.writer(handle)
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
    summary, work_samples = run_estimator_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "estimator_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "work_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_work_samples(samples_path, work_samples)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
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
    return EstimatorExperimentSummary(cases=cases, **data)
