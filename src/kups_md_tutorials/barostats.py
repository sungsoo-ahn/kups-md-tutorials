"""Pressure and cell-degree diagnostics for post 05."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import BarostatCase, BarostatTutorialSpec
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class BarostatRunSummary:
    """Compact diagnostics for one scalar barostat run."""

    barostat: str
    relaxation_time: float
    samples: int
    volume_mean: float
    volume_variance: float
    expected_volume_mean: float
    expected_volume_variance: float
    volume_variance_relative_error: float
    pressure_mean: float
    pressure_variance: float
    expected_pressure_mean: float
    expected_pressure_variance: float
    pressure_variance_relative_error: float
    volume_lag1_autocorrelation: float
    volume_integrated_autocorrelation_time: float
    volume_effective_samples: float


@dataclass(frozen=True)
class BarostatExperimentSummary:
    """Summary table for one post/profile pressure experiment."""

    post: str
    profile: str
    temperature: float
    target_pressure: float
    equilibrium_volume: float
    compressibility: float
    time_step: float
    sample_every: int
    seed: int
    config_sha256: str
    runs: list[BarostatRunSummary]


def expected_volume_variance(temperature: float, compressibility: float, volume: float) -> float:
    """Return the NPT volume fluctuation target, using kB = 1 units."""

    return temperature * compressibility * volume


def simulate_scalar_barostat(
    *,
    temperature: float,
    target_pressure: float,
    equilibrium_volume: float,
    compressibility: float,
    time_step: float,
    num_steps: int,
    warmup_steps: int,
    sample_every: int,
    relaxation_time: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sample a scalar-volume Ornstein-Uhlenbeck pressure model."""

    rng = np.random.default_rng(seed)
    variance = expected_volume_variance(temperature, compressibility, equilibrium_volume)
    volume = float(equilibrium_volume)
    decay = float(np.exp(-time_step / relaxation_time))
    noise_scale = float(np.sqrt(variance * (1.0 - decay**2)))
    samples: list[tuple[float, float, float]] = []

    for step in range(num_steps):
        volume = equilibrium_volume + decay * (volume - equilibrium_volume)
        volume += noise_scale * rng.normal()
        pressure = target_pressure - (volume - equilibrium_volume) / (
            compressibility * equilibrium_volume
        )
        if step >= warmup_steps and (step - warmup_steps) % sample_every == 0:
            samples.append((step * time_step, volume, pressure))

    data = np.array(samples, dtype=float)
    return data[:, 0], data[:, 1], data[:, 2]


def _lag_autocorrelation(values: np.ndarray, lag: int = 1) -> float:
    centered = values - np.mean(values)
    denominator = float(np.dot(centered, centered))
    if denominator == 0.0 or len(centered) <= lag:
        return 0.0
    return float(np.dot(centered[:-lag], centered[lag:]) / denominator)


def _integrated_autocorrelation_time(values: np.ndarray, max_lag: int = 500) -> float:
    centered = values - np.mean(values)
    denominator = float(np.dot(centered, centered))
    if denominator == 0.0:
        return 1.0
    tau = 1.0
    lag_limit = min(max_lag, len(centered) - 1)
    for lag in range(1, lag_limit + 1):
        corr = float(np.dot(centered[:-lag], centered[lag:]) / denominator)
        if corr <= 0.0:
            break
        tau += 2.0 * corr
    return tau


def summarize_barostat_run(
    *,
    spec: BarostatTutorialSpec,
    barostat: BarostatCase,
    seed_offset: int,
) -> tuple[BarostatRunSummary, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Run and summarize one scalar barostat configuration."""

    exp = spec.experiment
    times, volumes, pressures = simulate_scalar_barostat(
        temperature=exp.temperature,
        target_pressure=exp.target_pressure,
        equilibrium_volume=exp.equilibrium_volume,
        compressibility=exp.compressibility,
        time_step=exp.time_step,
        num_steps=exp.num_steps,
        warmup_steps=exp.warmup_steps,
        sample_every=exp.sample_every,
        relaxation_time=barostat.relaxation_time,
        seed=exp.seed + seed_offset,
    )
    volume_variance_target = expected_volume_variance(
        exp.temperature, exp.compressibility, exp.equilibrium_volume
    )
    pressure_variance_target = exp.temperature / (
        exp.compressibility * exp.equilibrium_volume
    )
    volume_iat = _integrated_autocorrelation_time(volumes)
    summary = BarostatRunSummary(
        barostat=barostat.name,
        relaxation_time=barostat.relaxation_time,
        samples=len(volumes),
        volume_mean=float(np.mean(volumes)),
        volume_variance=float(np.var(volumes, ddof=1)),
        expected_volume_mean=exp.equilibrium_volume,
        expected_volume_variance=volume_variance_target,
        volume_variance_relative_error=float(np.var(volumes, ddof=1) / volume_variance_target - 1.0),
        pressure_mean=float(np.mean(pressures)),
        pressure_variance=float(np.var(pressures, ddof=1)),
        expected_pressure_mean=exp.target_pressure,
        expected_pressure_variance=pressure_variance_target,
        pressure_variance_relative_error=float(
            np.var(pressures, ddof=1) / pressure_variance_target - 1.0
        ),
        volume_lag1_autocorrelation=_lag_autocorrelation(volumes),
        volume_integrated_autocorrelation_time=volume_iat,
        volume_effective_samples=float(len(volumes) / volume_iat),
    )
    return summary, (times, volumes, pressures)


def run_barostat_experiment(
    spec: BarostatTutorialSpec, config_sha256: str
) -> tuple[BarostatExperimentSummary, dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]]:
    """Run all configured pressure/cell diagnostics."""

    summaries = []
    trajectories = {}
    for idx, barostat in enumerate(spec.experiment.barostats):
        summary, trajectory = summarize_barostat_run(
            spec=spec,
            barostat=barostat,
            seed_offset=idx * 1009,
        )
        summaries.append(summary)
        trajectories[barostat.name] = trajectory
    exp = spec.experiment
    return (
        BarostatExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            temperature=exp.temperature,
            target_pressure=exp.target_pressure,
            equilibrium_volume=exp.equilibrium_volume,
            compressibility=exp.compressibility,
            time_step=exp.time_step,
            sample_every=exp.sample_every,
            seed=exp.seed,
            config_sha256=config_sha256,
            runs=summaries,
        ),
        trajectories,
    )


def _write_samples(
    path: Path,
    trajectories: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
    max_rows: int = 800,
) -> None:
    first_times = next(iter(trajectories.values()))[0]
    stride = max(1, int(np.ceil(len(first_times) / max_rows)))
    names = list(trajectories)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = ["time"]
        for name in names:
            header.extend([f"{name}_volume", f"{name}_pressure"])
        writer.writerow(header)
        for idx in range(0, len(first_times), stride):
            row: list[str] = [f"{first_times[idx]:.12g}"]
            for name in names:
                _, volumes, pressures = trajectories[name]
                row.extend([f"{volumes[idx]:.12g}", f"{pressures[idx]:.12g}"])
            writer.writerow(row)


def write_barostat_outputs(
    spec: BarostatTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-05 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, trajectories = run_barostat_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "barostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "barostat_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, trajectories)
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


def load_barostat_summary(path: Path) -> BarostatExperimentSummary:
    """Read a previously written post-05 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [BarostatRunSummary(**run) for run in data.pop("runs")]
    return BarostatExperimentSummary(runs=runs, **data)
