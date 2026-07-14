"""MLIP reliability diagnostics for post 12."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import MlipCaseSpec, MlipTutorialSpec
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class MlipCaseSummary:
    """Compact diagnostics for one MLIP regime."""

    case: str
    strain: float
    thermal_displacement: float
    force_rmse: float
    force_bias_norm: float
    static_energy_rmse_mev_per_atom: float
    normalized_nve_energy_drift: float
    ensemble_temperature_drift_k: float
    extrapolation_fraction: float
    uncertainty_mean: float
    uncertainty_coverage_2sigma: float
    neighbor_list_risk_fraction: float
    free_energy_barrier_shift: float


@dataclass(frozen=True)
class MlipExperimentSummary:
    """Summary table for one MLIP capstone experiment."""

    post: str
    profile: str
    material: str
    temperature_k: float
    sample_count: int
    time_step_fs: float
    seed: int
    config_sha256: str
    model_name: str
    model_repository: str
    model_revision: str
    model_sha256: str
    cases: list[MlipCaseSummary]


def _case_samples(
    case: MlipCaseSpec,
    *,
    sample_count: int,
    seed: int,
) -> tuple[MlipCaseSummary, dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    displacement = rng.normal(
        loc=case.thermal_displacement + abs(case.strain) * 0.25,
        scale=max(case.thermal_displacement * 0.35, 1.0e-4),
        size=sample_count,
    )
    displacement = np.clip(displacement, 0.0, None)
    true_force = -4.0 * displacement + 0.35 * rng.normal(size=sample_count)
    bias = case.force_bias * (1.0 + 4.0 * abs(case.strain))
    error = rng.normal(bias, case.force_noise, size=sample_count)
    mlip_force = true_force + error
    uncertainty = case.uncertainty_scale * (
        case.force_noise + 0.35 * displacement + abs(case.strain) * 0.25
    )
    extrapolation_score = displacement / 0.085 + abs(case.strain) / 0.08
    extrapolation_fraction = float(np.mean(extrapolation_score > 1.0))
    neighbor_risk = float(np.mean(displacement + abs(case.strain) * 0.5 > 0.12))
    force_rmse = float(np.sqrt(np.mean((mlip_force - true_force) ** 2)))
    force_bias_norm = float(abs(np.mean(mlip_force - true_force)))
    energy_error = 1000.0 * (0.12 * error + 0.18 * case.strain * displacement)
    static_energy_rmse = float(np.sqrt(np.mean(energy_error * energy_error)))
    normalized_drift = float(
        0.002
        + 0.020 * force_rmse
        + 0.050 * force_bias_norm
        + 0.010 * extrapolation_fraction
    )
    temp_drift = float(
        0.5
        + 35.0 * force_bias_norm
        + 12.0 * extrapolation_fraction
        + 6.0 * abs(case.strain)
    )
    coverage = float(np.mean(np.abs(error) <= 2.0 * uncertainty))
    barrier_shift = float(0.08 * np.mean(error) + 0.6 * abs(case.strain) ** 2)
    summary = MlipCaseSummary(
        case=case.name,
        strain=case.strain,
        thermal_displacement=case.thermal_displacement,
        force_rmse=force_rmse,
        force_bias_norm=force_bias_norm,
        static_energy_rmse_mev_per_atom=static_energy_rmse,
        normalized_nve_energy_drift=normalized_drift,
        ensemble_temperature_drift_k=temp_drift,
        extrapolation_fraction=extrapolation_fraction,
        uncertainty_mean=float(np.mean(uncertainty)),
        uncertainty_coverage_2sigma=coverage,
        neighbor_list_risk_fraction=neighbor_risk,
        free_energy_barrier_shift=barrier_shift,
    )
    samples = {
        "displacement": displacement,
        "true_force": true_force,
        "mlip_force": mlip_force,
        "force_error": error,
        "uncertainty": uncertainty,
        "extrapolation_score": extrapolation_score,
    }
    return summary, samples


def run_mlip_experiment(
    spec: MlipTutorialSpec,
    config_sha256: str,
) -> tuple[MlipExperimentSummary, dict[str, dict[str, np.ndarray]]]:
    """Run all configured MLIP reliability diagnostics."""

    summaries = []
    samples = {}
    for idx, case in enumerate(spec.experiment.cases):
        summary, case_samples = _case_samples(
            case,
            sample_count=spec.experiment.sample_count,
            seed=spec.experiment.seed + idx * 1009,
        )
        summaries.append(summary)
        samples[case.name] = case_samples
    artifact = spec.experiment.model_artifact
    return (
        MlipExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            material=spec.experiment.material,
            temperature_k=spec.experiment.temperature_k,
            sample_count=spec.experiment.sample_count,
            time_step_fs=spec.experiment.time_step_fs,
            seed=spec.experiment.seed,
            config_sha256=config_sha256,
            model_name=artifact.name,
            model_repository=artifact.repository,
            model_revision=artifact.revision,
            model_sha256=artifact.sha256,
            cases=summaries,
        ),
        samples,
    )


def _write_mlip_samples(
    path: Path,
    samples: dict[str, dict[str, np.ndarray]],
    max_rows: int = 900,
) -> None:
    first = next(iter(samples.values()))["displacement"]
    stride = max(1, int(np.ceil(len(first) / max_rows)))
    names = list(samples)
    fields = ["displacement", "force_error", "uncertainty", "extrapolation_score"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = []
        for name in names:
            header.extend([f"{name}_{field}" for field in fields])
        writer.writerow(header)
        for idx in range(0, len(first), stride):
            row: list[str] = []
            for name in names:
                case_samples = samples[name]
                row.extend(f"{case_samples[field][idx]:.12g}" for field in fields)
            writer.writerow(row)


def write_mlip_outputs(
    spec: MlipTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-12 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, samples = run_mlip_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "mlip_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "mlip_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_mlip_samples(samples_path, samples)
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


def load_mlip_summary(path: Path) -> MlipExperimentSummary:
    """Read a previously written post-12 MLIP summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    cases = [MlipCaseSummary(**item) for item in data.pop("cases")]
    return MlipExperimentSummary(cases=cases, **data)
