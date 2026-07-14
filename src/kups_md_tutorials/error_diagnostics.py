"""Timestep, precision, and force-error diagnostics for post 03."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import ErrorTutorialSpec
from kups_md_tutorials.integrators import exact_harmonic, harmonic_energy
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class ErrorRunSummary:
    """Compact diagnostics for one timestep/precision/force case."""

    time_step: float
    precision: str
    force_case: str
    force_scale: float
    final_time: float
    initial_energy: float
    final_energy: float
    normalized_energy_drift: float
    max_abs_relative_energy_error: float
    rms_position_error: float
    final_position_error: float
    unstable: bool


@dataclass(frozen=True)
class ErrorExperimentSummary:
    """Summary table for one post/profile simulation-error experiment."""

    post: str
    profile: str
    mass: float
    omega: float
    initial_position: float
    initial_velocity: float
    config_sha256: str
    runs: list[ErrorRunSummary]


def _apply_precision(value: float, precision: str) -> float:
    if precision == "float64":
        return float(value)
    if precision == "float32":
        return float(np.float32(value))
    if precision.startswith("rounded_"):
        quantum = float(precision.removeprefix("rounded_"))
        return float(np.round(value / quantum) * quantum)
    msg = f"unsupported precision model: {precision}"
    raise ValueError(msg)


def integrate_with_error(
    time_step: float,
    num_steps: int,
    mass: float,
    omega: float,
    position0: float,
    velocity0: float,
    precision: str,
    force_scale: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate with velocity Verlet under deterministic force/precision errors."""

    times = np.arange(num_steps + 1, dtype=float) * time_step
    positions = np.empty(num_steps + 1, dtype=float)
    velocities = np.empty(num_steps + 1, dtype=float)
    position = _apply_precision(position0, precision)
    velocity = _apply_precision(velocity0, precision)
    positions[0] = position
    velocities[0] = velocity

    for step in range(num_steps):
        acceleration = -force_scale * omega**2 * position
        position_next = position + velocity * time_step + 0.5 * acceleration * time_step**2
        position_next = _apply_precision(position_next, precision)
        acceleration_next = -force_scale * omega**2 * position_next
        velocity_next = velocity + 0.5 * (acceleration + acceleration_next) * time_step
        velocity_next = _apply_precision(velocity_next, precision)
        position = position_next
        velocity = velocity_next
        positions[step + 1] = position
        velocities[step + 1] = velocity

    return times, positions, velocities


def summarize_error_run(
    time_step: float,
    num_steps: int,
    mass: float,
    omega: float,
    position0: float,
    velocity0: float,
    precision: str,
    force_case: str,
    force_scale: float,
) -> ErrorRunSummary:
    """Compute diagnostics for one error experiment run."""

    times, positions, velocities = integrate_with_error(
        time_step,
        num_steps,
        mass,
        omega,
        position0,
        velocity0,
        precision,
        force_scale,
    )
    exact_positions, _ = exact_harmonic(times, position0, velocity0, omega)
    energy = harmonic_energy(positions, velocities, mass, omega)
    initial_energy = float(energy[0])
    relative_error = (energy - initial_energy) / initial_energy
    normalized_drift = float((energy[-1] - initial_energy) / (initial_energy * times[-1]))
    position_error = positions - exact_positions
    max_error = float(np.max(np.abs(relative_error)))

    return ErrorRunSummary(
        time_step=float(time_step),
        precision=precision,
        force_case=force_case,
        force_scale=float(force_scale),
        final_time=float(times[-1]),
        initial_energy=initial_energy,
        final_energy=float(energy[-1]),
        normalized_energy_drift=normalized_drift,
        max_abs_relative_energy_error=max_error,
        rms_position_error=float(np.sqrt(np.mean(position_error**2))),
        final_position_error=float(position_error[-1]),
        unstable=bool(max_error > 1.0 or not np.isfinite(max_error)),
    )


def run_error_experiment(spec: ErrorTutorialSpec, config_sha256: str) -> ErrorExperimentSummary:
    """Run all configured timestep/precision/force-error combinations."""

    system = spec.system
    runs = [
        summarize_error_run(
            time_step=time_step,
            num_steps=spec.experiment.num_steps,
            mass=system.mass,
            omega=system.omega,
            position0=system.position,
            velocity0=system.velocity,
            precision=precision,
            force_case=force_case.name,
            force_scale=force_case.force_scale,
        )
        for time_step in spec.experiment.time_steps
        for precision in spec.experiment.precisions
        for force_case in spec.experiment.force_cases
    ]
    return ErrorExperimentSummary(
        post=spec.post,
        profile=spec.profile,
        mass=system.mass,
        omega=system.omega,
        initial_position=system.position,
        initial_velocity=system.velocity,
        config_sha256=config_sha256,
        runs=runs,
    )


def _write_samples(path: Path, spec: ErrorTutorialSpec, max_rows: int = 700) -> None:
    time_step = max(spec.experiment.time_steps)
    cases = [
        ("float64", "exact_force", 1.0),
        (spec.experiment.precisions[-1], "exact_force", 1.0),
        ("float64", spec.experiment.force_cases[-1].name, spec.experiment.force_cases[-1].force_scale),
    ]
    trajectories = {}
    for precision, force_case, force_scale in cases:
        trajectories[(precision, force_case)] = integrate_with_error(
            time_step,
            spec.experiment.num_steps,
            spec.system.mass,
            spec.system.omega,
            spec.system.position,
            spec.system.velocity,
            precision,
            force_scale,
        )

    times = next(iter(trajectories.values()))[0]
    exact_positions, _ = exact_harmonic(
        times, spec.system.position, spec.system.velocity, spec.system.omega
    )
    stride = max(1, int(np.ceil(len(times) / max_rows)))

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "time",
                "exact_position",
                "float64_exact_position",
                "low_precision_exact_position",
                "float64_biased_position",
            ]
        )
        low_precision_key = (spec.experiment.precisions[-1], "exact_force")
        biased_key = ("float64", spec.experiment.force_cases[-1].name)
        for idx in range(0, len(times), stride):
            writer.writerow(
                [
                    f"{times[idx]:.12g}",
                    f"{exact_positions[idx]:.12g}",
                    f"{trajectories[('float64', 'exact_force')][1][idx]:.12g}",
                    f"{trajectories[low_precision_key][1][idx]:.12g}",
                    f"{trajectories[biased_key][1][idx]:.12g}",
                ]
            )


def write_error_outputs(
    spec: ErrorTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-03 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary = run_error_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "error_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "error_samples.csv"

    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, spec)
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


def load_error_summary(path: Path) -> ErrorExperimentSummary:
    """Read a previously written post-03 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [ErrorRunSummary(**run) for run in data.pop("runs")]
    return ErrorExperimentSummary(runs=runs, **data)
