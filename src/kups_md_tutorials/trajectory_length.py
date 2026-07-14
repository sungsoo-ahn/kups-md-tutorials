"""Trajectory-length, autocorrelation, and uncertainty diagnostics for post 06."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import TrajectoryLengthTutorialSpec
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class TrajectoryCheckpointSummary:
    """Compact diagnostics for one trajectory-length checkpoint."""

    checkpoint_steps: int
    samples_per_replica: int
    total_samples: int
    mean_estimate: float
    true_mean: float
    absolute_error: float
    naive_standard_error: float
    integrated_autocorrelation_time: float
    effective_samples: float
    autocorrelation_standard_error: float
    block_standard_error: float
    replica_standard_error: float
    conservative_standard_error: float
    conservative_ci95_half_width: float
    z_score: float
    replica_mean_min: float
    replica_mean_max: float


@dataclass(frozen=True)
class TrajectoryLengthExperimentSummary:
    """Summary table for one post/profile trajectory-length experiment."""

    post: str
    profile: str
    true_mean: float
    stationary_variance: float
    correlation_time: float
    equilibration_time: float
    initial_bias: float
    time_step: float
    warmup_steps: int
    sample_every: int
    replica_count: int
    seed: int
    config_sha256: str
    checkpoints: list[TrajectoryCheckpointSummary]


def simulate_correlated_observable(
    *,
    true_mean: float,
    stationary_variance: float,
    correlation_time: float,
    equilibration_time: float,
    initial_bias: float,
    time_step: float,
    max_steps: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate a biased AR(1) observable with a known equilibrium mean."""

    rng = np.random.default_rng(seed)
    phi = float(np.exp(-time_step / correlation_time))
    noise_scale = float(np.sqrt(stationary_variance * (1.0 - phi**2)))
    fluctuation = float(rng.normal(0.0, np.sqrt(stationary_variance)))
    times = np.arange(max_steps, dtype=float) * time_step
    values = np.empty(max_steps, dtype=float)

    for step, time in enumerate(times):
        fluctuation = phi * fluctuation + noise_scale * rng.normal()
        bias = initial_bias * np.exp(-time / equilibration_time)
        values[step] = true_mean + bias + fluctuation

    return times, values


def _integrated_autocorrelation_time(values: np.ndarray, max_lag: int = 1000) -> float:
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
    return max(1.0, tau)


def _block_standard_error(values_by_replica: list[np.ndarray], block_size: int) -> float:
    block_means = []
    for values in values_by_replica:
        block_count = len(values) // block_size
        for idx in range(block_count):
            start = idx * block_size
            block = values[start : start + block_size]
            block_means.append(float(np.mean(block)))
    if len(block_means) < 2:
        return float("nan")
    return float(np.std(block_means, ddof=1) / np.sqrt(len(block_means)))


def _checkpoint_summary(
    *,
    spec: TrajectoryLengthTutorialSpec,
    checkpoint: int,
    trajectories: list[tuple[np.ndarray, np.ndarray]],
) -> TrajectoryCheckpointSummary:
    exp = spec.experiment
    start = exp.warmup_steps
    values_by_replica = [
        values[start:checkpoint: exp.sample_every] for _, values in trajectories
    ]
    pooled = np.concatenate(values_by_replica)
    replica_means = np.array([np.mean(values) for values in values_by_replica], dtype=float)
    iats = np.array(
        [_integrated_autocorrelation_time(values) for values in values_by_replica],
        dtype=float,
    )
    iat = float(np.mean(iats))
    effective_samples = float(len(pooled) / iat)
    naive_standard_error = float(np.std(pooled, ddof=1) / np.sqrt(len(pooled)))
    autocorrelation_standard_error = float(np.std(pooled, ddof=1) / np.sqrt(effective_samples))
    block_size = max(2, int(np.ceil(iat)))
    block_standard_error = _block_standard_error(values_by_replica, block_size)
    replica_standard_error = float(np.std(replica_means, ddof=1) / np.sqrt(len(replica_means)))
    conservative_standard_error = float(
        np.nanmax(
            [
                naive_standard_error,
                autocorrelation_standard_error,
                block_standard_error,
                replica_standard_error,
            ]
        )
    )
    mean_estimate = float(np.mean(pooled))
    absolute_error = float(abs(mean_estimate - exp.true_mean))
    return TrajectoryCheckpointSummary(
        checkpoint_steps=checkpoint,
        samples_per_replica=len(values_by_replica[0]),
        total_samples=len(pooled),
        mean_estimate=mean_estimate,
        true_mean=exp.true_mean,
        absolute_error=absolute_error,
        naive_standard_error=naive_standard_error,
        integrated_autocorrelation_time=iat,
        effective_samples=effective_samples,
        autocorrelation_standard_error=autocorrelation_standard_error,
        block_standard_error=block_standard_error,
        replica_standard_error=replica_standard_error,
        conservative_standard_error=conservative_standard_error,
        conservative_ci95_half_width=1.96 * conservative_standard_error,
        z_score=float(absolute_error / conservative_standard_error),
        replica_mean_min=float(np.min(replica_means)),
        replica_mean_max=float(np.max(replica_means)),
    )


def run_trajectory_length_experiment(
    spec: TrajectoryLengthTutorialSpec,
    config_sha256: str,
) -> tuple[
    TrajectoryLengthExperimentSummary,
    list[tuple[np.ndarray, np.ndarray]],
]:
    """Run all configured trajectory-length diagnostics."""

    exp = spec.experiment
    trajectories = [
        simulate_correlated_observable(
            true_mean=exp.true_mean,
            stationary_variance=exp.stationary_variance,
            correlation_time=exp.correlation_time,
            equilibration_time=exp.equilibration_time,
            initial_bias=exp.initial_bias,
            time_step=exp.time_step,
            max_steps=exp.max_steps,
            seed=exp.seed + replica * 1009,
        )
        for replica in range(exp.replica_count)
    ]
    checkpoints = [
        _checkpoint_summary(spec=spec, checkpoint=checkpoint, trajectories=trajectories)
        for checkpoint in exp.checkpoints
    ]
    return (
        TrajectoryLengthExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            true_mean=exp.true_mean,
            stationary_variance=exp.stationary_variance,
            correlation_time=exp.correlation_time,
            equilibration_time=exp.equilibration_time,
            initial_bias=exp.initial_bias,
            time_step=exp.time_step,
            warmup_steps=exp.warmup_steps,
            sample_every=exp.sample_every,
            replica_count=exp.replica_count,
            seed=exp.seed,
            config_sha256=config_sha256,
            checkpoints=checkpoints,
        ),
        trajectories,
    )


def _write_samples(
    path: Path,
    trajectories: list[tuple[np.ndarray, np.ndarray]],
    *,
    sample_every: int,
    max_rows: int = 900,
) -> None:
    first_times = trajectories[0][0][::sample_every]
    stride = max(1, int(np.ceil(len(first_times) / max_rows)))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        header = ["time"]
        header.extend(f"replica_{idx}_observable" for idx in range(len(trajectories)))
        writer.writerow(header)
        sample_indices = np.arange(0, len(trajectories[0][0]), sample_every)
        for sample_idx in sample_indices[::stride]:
            row: list[str] = [f"{trajectories[0][0][sample_idx]:.12g}"]
            for _, values in trajectories:
                row.append(f"{values[sample_idx]:.12g}")
            writer.writerow(row)


def write_trajectory_length_outputs(
    spec: TrajectoryLengthTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-06 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, trajectories = run_trajectory_length_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "trajectory_length_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_length_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, trajectories, sample_every=spec.experiment.sample_every)
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


def load_trajectory_length_summary(path: Path) -> TrajectoryLengthExperimentSummary:
    """Read a previously written post-06 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    checkpoints = [
        TrajectoryCheckpointSummary(**checkpoint)
        for checkpoint in data.pop("checkpoints")
    ]
    return TrajectoryLengthExperimentSummary(checkpoints=checkpoints, **data)
