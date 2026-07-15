"""Trajectory-length, autocorrelation, and uncertainty diagnostics for post 06."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import TrajectoryLengthTutorialSpec
from kups_md_tutorials.error_diagnostics import (
    _initialized_argon_velocities,
    _lennard_jones_forces,
)
from kups_md_tutorials.provenance import provenance
from kups_md_tutorials.systems import argon_fcc


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
class ArgonObservableCheckpointSummary:
    """Checkpointed uncertainty for one compact argon physical observable."""

    checkpoint_steps: int
    samples_per_replica: int
    total_samples: int
    mean_potential_energy_per_atom: float
    naive_standard_error: float
    integrated_autocorrelation_time: float
    effective_samples: float
    autocorrelation_standard_error: float
    replica_standard_error: float
    conservative_standard_error: float
    conservative_ci95_half_width: float
    mean_coordination_number: float
    coordination_naive_standard_error: float
    coordination_integrated_autocorrelation_time: float
    coordination_effective_samples: float
    coordination_autocorrelation_standard_error: float
    coordination_replica_standard_error: float
    coordination_conservative_standard_error: float
    coordination_conservative_ci95_half_width: float
    coordination_replica_mean_min: float
    coordination_replica_mean_max: float
    replica_mean_min: float
    replica_mean_max: float


@dataclass(frozen=True)
class ArgonObservableSummary:
    """Compact argon trajectory-length diagnostic for a physical observable."""

    atom_count: int
    number_density: float
    temperature: float
    gamma: float
    time_step: float
    warmup_steps: int
    sample_every: int
    replica_count: int
    observable: str
    coordination_cutoff: float
    checkpoints: list[ArgonObservableCheckpointSummary]


@dataclass(frozen=True)
class _ObservableStats:
    mean: float
    naive_standard_error: float
    integrated_autocorrelation_time: float
    effective_samples: float
    autocorrelation_standard_error: float
    replica_standard_error: float
    conservative_standard_error: float
    conservative_ci95_half_width: float
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
    argon_observable: ArgonObservableSummary | None = None


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


def _observable_stats(values_by_replica: list[np.ndarray]) -> _ObservableStats:
    """Return uncertainty diagnostics for checkpointed replica values."""

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
    replica_standard_error = float(np.std(replica_means, ddof=1) / np.sqrt(len(replica_means)))
    conservative_standard_error = max(
        naive_standard_error,
        autocorrelation_standard_error,
        replica_standard_error,
    )
    return _ObservableStats(
        mean=float(np.mean(pooled)),
        naive_standard_error=naive_standard_error,
        integrated_autocorrelation_time=iat,
        effective_samples=effective_samples,
        autocorrelation_standard_error=autocorrelation_standard_error,
        replica_standard_error=replica_standard_error,
        conservative_standard_error=conservative_standard_error,
        conservative_ci95_half_width=1.96 * conservative_standard_error,
        replica_mean_min=float(np.min(replica_means)),
        replica_mean_max=float(np.max(replica_means)),
    )


def _argon_observable_checkpoint_summary(
    *,
    checkpoint: int,
    warmup_steps: int,
    trajectories: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
) -> ArgonObservableCheckpointSummary:
    values_by_replica = [
        values[(times >= warmup_steps) & (times <= checkpoint)]
        for times, values, _ in trajectories
    ]
    coordination_by_replica = [
        coordination[(times >= warmup_steps) & (times <= checkpoint)]
        for times, _, coordination in trajectories
    ]
    energy = _observable_stats(values_by_replica)
    coordination = _observable_stats(coordination_by_replica)
    return ArgonObservableCheckpointSummary(
        checkpoint_steps=checkpoint,
        samples_per_replica=len(values_by_replica[0]),
        total_samples=sum(len(values) for values in values_by_replica),
        mean_potential_energy_per_atom=energy.mean,
        naive_standard_error=energy.naive_standard_error,
        integrated_autocorrelation_time=energy.integrated_autocorrelation_time,
        effective_samples=energy.effective_samples,
        autocorrelation_standard_error=energy.autocorrelation_standard_error,
        replica_standard_error=energy.replica_standard_error,
        conservative_standard_error=energy.conservative_standard_error,
        conservative_ci95_half_width=energy.conservative_ci95_half_width,
        mean_coordination_number=coordination.mean,
        coordination_naive_standard_error=coordination.naive_standard_error,
        coordination_integrated_autocorrelation_time=coordination.integrated_autocorrelation_time,
        coordination_effective_samples=coordination.effective_samples,
        coordination_autocorrelation_standard_error=coordination.autocorrelation_standard_error,
        coordination_replica_standard_error=coordination.replica_standard_error,
        coordination_conservative_standard_error=coordination.conservative_standard_error,
        coordination_conservative_ci95_half_width=coordination.conservative_ci95_half_width,
        coordination_replica_mean_min=coordination.replica_mean_min,
        coordination_replica_mean_max=coordination.replica_mean_max,
        replica_mean_min=energy.replica_mean_min,
        replica_mean_max=energy.replica_mean_max,
    )


def _coordination_number(
    positions: np.ndarray,
    box_length: float,
    cutoff: float,
) -> float:
    """Estimate mean coordination from pair counts inside a cutoff."""

    cutoff_squared = cutoff**2
    pair_count = 0
    for i in range(len(positions) - 1):
        displacement = positions[i] - positions[i + 1 :]
        displacement -= box_length * np.rint(displacement / box_length)
        distance_squared = np.sum(displacement * displacement, axis=1)
        pair_count += int(np.count_nonzero(distance_squared < cutoff_squared))
    return float(2.0 * pair_count / len(positions))


def _simulate_argon_observable_replica(
    spec: TrajectoryLengthTutorialSpec,
    replica_index: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    argon = spec.argon_observable
    if argon is None:
        msg = "argon_observable config is required"
        raise ValueError(msg)

    atoms = argon_fcc(argon.repetitions, argon.number_density)
    positions = atoms.get_positions().astype(float)
    box = float(atoms.cell.lengths()[0])
    velocities = _initialized_argon_velocities(
        atom_count=len(atoms),
        temperature=argon.temperature,
        seed=argon.seed + replica_index * 1009,
    )
    forces, potential = _lennard_jones_forces(
        positions,
        box_length=box,
        epsilon=argon.epsilon,
        sigma=argon.sigma,
        cutoff=argon.cutoff,
    )
    c = float(np.exp(-argon.gamma * argon.time_step))
    sigma_v = float(np.sqrt(argon.temperature * (1.0 - c**2)))
    rng = np.random.default_rng(argon.seed + replica_index * 1009 + 17)
    times: list[float] = []
    potential_energy_per_atom: list[float] = []
    coordination_number: list[float] = []

    for step in range(1, argon.max_steps + 1):
        velocities += 0.5 * argon.time_step * forces
        positions = (positions + 0.5 * argon.time_step * velocities) % box
        velocities = c * velocities + sigma_v * rng.normal(size=velocities.shape)
        velocities -= np.mean(velocities, axis=0)
        positions = (positions + 0.5 * argon.time_step * velocities) % box
        forces, potential = _lennard_jones_forces(
            positions,
            box_length=box,
            epsilon=argon.epsilon,
            sigma=argon.sigma,
            cutoff=argon.cutoff,
        )
        velocities += 0.5 * argon.time_step * forces

        if step >= argon.warmup_steps and (step - argon.warmup_steps) % argon.sample_every == 0:
            times.append(float(step))
            potential_energy_per_atom.append(float(potential / len(atoms)))
            coordination_number.append(
                _coordination_number(positions, box, argon.coordination_cutoff)
            )

    return (
        np.asarray(times, dtype=float),
        np.asarray(potential_energy_per_atom, dtype=float),
        np.asarray(coordination_number, dtype=float),
    )


def run_argon_observable_experiment(
    spec: TrajectoryLengthTutorialSpec,
) -> tuple[ArgonObservableSummary | None, list[tuple[np.ndarray, np.ndarray, np.ndarray]]]:
    """Run optional compact argon physical-observable trajectory-length checks."""

    argon = spec.argon_observable
    if argon is None:
        return None, []

    trajectories = [
        _simulate_argon_observable_replica(spec, replica_index=replica)
        for replica in range(argon.replica_count)
    ]
    atom_count = len(argon_fcc(argon.repetitions, argon.number_density))
    checkpoints = [
        _argon_observable_checkpoint_summary(
            checkpoint=checkpoint,
            warmup_steps=argon.warmup_steps,
            trajectories=trajectories,
        )
        for checkpoint in argon.checkpoints
    ]
    return (
        ArgonObservableSummary(
            atom_count=atom_count,
            number_density=argon.number_density,
            temperature=argon.temperature,
            gamma=argon.gamma,
            time_step=argon.time_step,
            warmup_steps=argon.warmup_steps,
            sample_every=argon.sample_every,
            replica_count=argon.replica_count,
            observable="potential_energy_per_atom",
            coordination_cutoff=argon.coordination_cutoff,
            checkpoints=checkpoints,
        ),
        trajectories,
    )


def run_trajectory_length_experiment(
    spec: TrajectoryLengthTutorialSpec,
    config_sha256: str,
) -> tuple[
    TrajectoryLengthExperimentSummary,
    list[tuple[np.ndarray, np.ndarray]],
    list[tuple[np.ndarray, np.ndarray, np.ndarray]],
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
    argon_summary, argon_trajectories = run_argon_observable_experiment(spec)
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
            argon_observable=argon_summary,
        ),
        trajectories,
        argon_trajectories,
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
        writer = csv.writer(handle, lineterminator="\n")
        header = ["time"]
        header.extend(f"replica_{idx}_observable" for idx in range(len(trajectories)))
        writer.writerow(header)
        sample_indices = np.arange(0, len(trajectories[0][0]), sample_every)
        for sample_idx in sample_indices[::stride]:
            row: list[str] = [f"{trajectories[0][0][sample_idx]:.12g}"]
            for _, values in trajectories:
                row.append(f"{values[sample_idx]:.12g}")
            writer.writerow(row)


def _write_argon_observable_samples(
    path: Path,
    trajectories: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    max_rows: int = 900,
) -> None:
    if not trajectories:
        return
    first_times = trajectories[0][0]
    stride = max(1, int(np.ceil(len(first_times) / max_rows)))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        header = ["step"]
        header.extend(
            f"replica_{idx}_potential_energy_per_atom"
            for idx in range(len(trajectories))
        )
        header.extend(
            f"replica_{idx}_coordination_number"
            for idx in range(len(trajectories))
        )
        writer.writerow(header)
        for row_idx in range(0, len(first_times), stride):
            row: list[str] = [f"{first_times[row_idx]:.12g}"]
            for _, values, _ in trajectories:
                row.append(f"{values[row_idx]:.12g}")
            for _, _, coordination in trajectories:
                row.append(f"{coordination[row_idx]:.12g}")
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
    summary, trajectories, argon_trajectories = run_trajectory_length_experiment(
        spec, prov.config_sha256
    )

    summary_path = output_dir / "trajectory_length_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_length_samples.csv"
    argon_samples_path = output_dir / "argon_observable_samples.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, trajectories, sample_every=spec.experiment.sample_every)
    if summary.argon_observable is not None:
        _write_argon_observable_samples(argon_samples_path, argon_trajectories)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
        "argon_observable_samples_file": (
            argon_samples_path.name if summary.argon_observable is not None else None
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


def load_trajectory_length_summary(path: Path) -> TrajectoryLengthExperimentSummary:
    """Read a previously written post-06 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    checkpoints = [
        TrajectoryCheckpointSummary(**checkpoint)
        for checkpoint in data.pop("checkpoints")
    ]
    argon_observable = data.pop("argon_observable", None)
    if argon_observable is not None:
        argon_observable = ArgonObservableSummary(
            checkpoints=[
                ArgonObservableCheckpointSummary(**checkpoint)
                for checkpoint in argon_observable.pop("checkpoints")
            ],
            **argon_observable,
        )
    return TrajectoryLengthExperimentSummary(
        checkpoints=checkpoints, argon_observable=argon_observable, **data
    )
