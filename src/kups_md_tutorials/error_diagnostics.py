"""Timestep, precision, and force-error diagnostics for post 03."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import ase
import kups
import numpy as np

from kups_md_tutorials.config import ErrorTutorialSpec
from kups_md_tutorials.integrators import exact_harmonic, harmonic_energy
from kups_md_tutorials.provenance import provenance
from kups_md_tutorials.systems import argon_fcc


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
class ArgonNveRunSummary:
    """Compact diagnostics for one reduced-unit argon NVE run."""

    protocol_label: str
    time_step: float
    replica_index: int
    seed: int
    num_steps: int
    sample_every: int
    atom_count: int
    number_density: float
    temperature: float
    final_time: float
    initial_energy: float
    final_energy: float
    max_abs_relative_energy_error: float
    normalized_energy_drift: float
    energy_span: float
    unstable: bool


@dataclass(frozen=True)
class ArgonNveProtocolSummary:
    """Aggregate diagnostics for the configured argon NVE protocol."""

    protocol_label: str
    target_device: str
    replica_count: int
    time_step_count: int
    atom_count: int
    num_steps: int
    final_time_max: float
    max_abs_relative_energy_error: float
    max_abs_normalized_energy_drift: float
    mean_abs_normalized_energy_drift: float
    replica_drift_standard_error_max: float
    unstable_run_count: int


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
    argon_nve_runs: list[ArgonNveRunSummary]
    argon_nve_protocol: ArgonNveProtocolSummary | None = None


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
    argon_nve_runs = run_argon_nve_experiment(spec)
    return ErrorExperimentSummary(
        post=spec.post,
        profile=spec.profile,
        mass=system.mass,
        omega=system.omega,
        initial_position=system.position,
        initial_velocity=system.velocity,
        config_sha256=config_sha256,
        runs=runs,
        argon_nve_runs=argon_nve_runs,
        argon_nve_protocol=summarize_argon_nve_protocol(spec, argon_nve_runs),
    )


def run_argon_nve_experiment(spec: ErrorTutorialSpec) -> list[ArgonNveRunSummary]:
    """Run optional compact argon NVE energy-drift checks."""

    if spec.argon_nve is None:
        return []
    return [
        summarize_argon_nve_run(
            spec,
            time_step=time_step,
            replica_index=replica_index,
        )[0]
        for time_step in spec.argon_nve.time_steps
        for replica_index in range(spec.argon_nve.replica_count)
    ]


def summarize_argon_nve_protocol(
    spec: ErrorTutorialSpec,
    runs: list[ArgonNveRunSummary],
) -> ArgonNveProtocolSummary | None:
    """Aggregate configured argon NVE diagnostics across timesteps and replicas."""

    if spec.argon_nve is None or not runs:
        return None
    drift_se_by_timestep = []
    for time_step in spec.argon_nve.time_steps:
        drifts = np.asarray(
            [
                run.normalized_energy_drift
                for run in runs
                if np.isclose(run.time_step, time_step)
            ],
            dtype=float,
        )
        if len(drifts) < 2:
            drift_se_by_timestep.append(0.0)
        else:
            drift_se_by_timestep.append(float(np.std(drifts, ddof=1) / np.sqrt(len(drifts))))
    return ArgonNveProtocolSummary(
        protocol_label=spec.argon_nve.protocol_label,
        target_device=spec.argon_nve.target_device,
        replica_count=spec.argon_nve.replica_count,
        time_step_count=len(spec.argon_nve.time_steps),
        atom_count=runs[0].atom_count,
        num_steps=spec.argon_nve.num_steps,
        final_time_max=float(max(run.final_time for run in runs)),
        max_abs_relative_energy_error=float(
            max(run.max_abs_relative_energy_error for run in runs)
        ),
        max_abs_normalized_energy_drift=float(
            max(abs(run.normalized_energy_drift) for run in runs)
        ),
        mean_abs_normalized_energy_drift=float(
            np.mean([abs(run.normalized_energy_drift) for run in runs])
        ),
        replica_drift_standard_error_max=float(max(drift_se_by_timestep)),
        unstable_run_count=sum(1 for run in runs if run.unstable),
    )


def summarize_argon_nve_run(
    spec: ErrorTutorialSpec,
    time_step: float,
    replica_index: int = 0,
) -> tuple[ArgonNveRunSummary, tuple[np.ndarray, np.ndarray]]:
    """Integrate a deterministic reduced-unit argon LJ system in NVE."""

    if spec.argon_nve is None:
        msg = "argon_nve config is required"
        raise ValueError(msg)

    nve = spec.argon_nve
    atoms = argon_fcc(nve.repetitions, nve.number_density)
    positions = atoms.get_positions().astype(float)
    box = float(atoms.cell.lengths()[0])
    replica_seed = nve.seed + 1009 * replica_index
    velocities = _initialized_argon_velocities(
        atom_count=len(atoms),
        temperature=nve.temperature,
        seed=replica_seed,
    )
    forces, potential = _lennard_jones_forces(
        positions,
        box_length=box,
        epsilon=nve.epsilon,
        sigma=nve.sigma,
        cutoff=nve.cutoff,
    )
    times: list[float] = []
    energies: list[float] = []

    def sample(step: int, potential_energy: float) -> None:
        kinetic = 0.5 * float(np.sum(velocities**2))
        times.append(step * time_step)
        energies.append(kinetic + potential_energy)

    sample(0, potential)
    for step in range(1, nve.num_steps + 1):
        velocities += 0.5 * time_step * forces
        positions = (positions + time_step * velocities) % box
        forces, potential = _lennard_jones_forces(
            positions,
            box_length=box,
            epsilon=nve.epsilon,
            sigma=nve.sigma,
            cutoff=nve.cutoff,
        )
        velocities += 0.5 * time_step * forces
        if step % nve.sample_every == 0 or step == nve.num_steps:
            sample(step, potential)

    time_array = np.asarray(times, dtype=float)
    energy_array = np.asarray(energies, dtype=float)
    initial_energy = float(energy_array[0])
    relative_error = (energy_array - initial_energy) / abs(initial_energy)
    final_time = float(time_array[-1])
    normalized_drift = float((energy_array[-1] - initial_energy) / (abs(initial_energy) * final_time))
    max_error = float(np.max(np.abs(relative_error)))
    summary = ArgonNveRunSummary(
        protocol_label=nve.protocol_label,
        time_step=float(time_step),
        replica_index=replica_index,
        seed=replica_seed,
        num_steps=nve.num_steps,
        sample_every=nve.sample_every,
        atom_count=len(atoms),
        number_density=nve.number_density,
        temperature=nve.temperature,
        final_time=final_time,
        initial_energy=initial_energy,
        final_energy=float(energy_array[-1]),
        max_abs_relative_energy_error=max_error,
        normalized_energy_drift=normalized_drift,
        energy_span=float(np.max(energy_array) - np.min(energy_array)),
        unstable=bool(max_error > 0.05 or not np.isfinite(max_error)),
    )
    return summary, (time_array, energy_array)


def _initialized_argon_velocities(
    atom_count: int,
    temperature: float,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    velocities = rng.normal(0.0, np.sqrt(temperature), size=(atom_count, 3))
    velocities -= np.mean(velocities, axis=0)
    target_kinetic = 0.5 * (3 * atom_count - 3) * temperature
    current_kinetic = 0.5 * float(np.sum(velocities**2))
    return velocities * np.sqrt(target_kinetic / current_kinetic)


def _lennard_jones_forces(
    positions: np.ndarray,
    box_length: float,
    epsilon: float,
    sigma: float,
    cutoff: float,
) -> tuple[np.ndarray, float]:
    forces = np.zeros_like(positions)
    pair_i, pair_j = np.triu_indices(len(positions), k=1)
    rij = positions[pair_i] - positions[pair_j]
    rij -= box_length * np.rint(rij / box_length)
    r2 = np.sum(rij**2, axis=1)
    mask = r2 < cutoff**2
    if not np.any(mask):
        return forces, 0.0

    rij = rij[mask]
    r2 = r2[mask]
    pair_i = pair_i[mask]
    pair_j = pair_j[mask]
    shift = 4.0 * epsilon * ((sigma / cutoff) ** 12 - (sigma / cutoff) ** 6)
    inv_r2 = sigma**2 / r2
    inv_r6 = inv_r2**3
    inv_r12 = inv_r6**2
    potential = float(np.sum(4.0 * epsilon * (inv_r12 - inv_r6) - shift))
    coefficients = 24.0 * epsilon * (2.0 * inv_r12 - inv_r6) / r2
    pair_forces = coefficients[:, None] * rij
    np.add.at(forces, pair_i, pair_forces)
    np.add.at(forces, pair_j, -pair_forces)
    return forces, potential


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
        writer = csv.writer(handle, lineterminator="\n")
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


def _write_argon_nve_samples(
    path: Path,
    spec: ErrorTutorialSpec,
    max_rows: int = 700,
) -> None:
    if spec.argon_nve is None:
        return

    trajectories = {
        (time_step, replica_index): summarize_argon_nve_run(
            spec,
            time_step=time_step,
            replica_index=replica_index,
        )[1]
        for time_step in spec.argon_nve.time_steps
        for replica_index in range(spec.argon_nve.replica_count)
    }
    longest = max(len(times) for times, _ in trajectories.values())
    stride = max(1, int(np.ceil(longest / max_rows)))

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["time_step", "replica_index", "time", "relative_energy_error"])
        for (time_step, replica_index), (times, energies) in trajectories.items():
            initial_energy = float(energies[0])
            relative = (energies - initial_energy) / abs(initial_energy)
            for idx in range(0, len(times), stride):
                writer.writerow(
                    [
                        f"{time_step:.12g}",
                        replica_index,
                        f"{times[idx]:.12g}",
                        f"{relative[idx]:.12g}",
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
    argon_samples_path = output_dir / "argon_nve_samples.csv"

    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, spec)
    _write_argon_nve_samples(argon_samples_path, spec)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
        "argon_nve_samples_file": (
            argon_samples_path.name if spec.argon_nve is not None else None
        ),
        "provenance": asdict(prov),
        "versions": {
            "ase": ase.__version__,
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
    argon_nve_runs = [
        ArgonNveRunSummary(**run) for run in data.pop("argon_nve_runs", [])
    ]
    argon_nve_protocol_data = data.pop("argon_nve_protocol", None)
    argon_nve_protocol = (
        None
        if argon_nve_protocol_data is None
        else ArgonNveProtocolSummary(**argon_nve_protocol_data)
    )
    return ErrorExperimentSummary(
        runs=runs,
        argon_nve_runs=argon_nve_runs,
        argon_nve_protocol=argon_nve_protocol,
        **data,
    )
