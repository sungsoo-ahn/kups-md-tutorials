"""Deterministic integrator diagnostics for post 02."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import IntegratorTutorialSpec
from kups_md_tutorials.provenance import provenance


@dataclass(frozen=True)
class IntegratorRunSummary:
    """Compact diagnostics for one integrator and timestep."""

    integrator: str
    time_step: float
    num_steps: int
    final_time: float
    initial_energy: float
    final_energy: float
    signed_energy_drift: float
    max_abs_relative_energy_error: float
    rms_position_error: float
    final_position_error: float
    reversibility_error: float


@dataclass(frozen=True)
class IntegratorExperimentSummary:
    """Summary table for one post/profile integrator experiment."""

    post: str
    profile: str
    seed: int
    mass: float
    omega: float
    initial_position: float
    initial_velocity: float
    config_sha256: str
    runs: list[IntegratorRunSummary]


def harmonic_energy(position: np.ndarray, velocity: np.ndarray, mass: float, omega: float):
    """Return total energy for a dimensionless harmonic oscillator."""

    return 0.5 * mass * velocity**2 + 0.5 * mass * omega**2 * position**2


def exact_harmonic(
    times: np.ndarray,
    position0: float,
    velocity0: float,
    omega: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact harmonic oscillator trajectory."""

    cos = np.cos(omega * times)
    sin = np.sin(omega * times)
    position = position0 * cos + velocity0 / omega * sin
    velocity = velocity0 * cos - position0 * omega * sin
    return position, velocity


def integrate_harmonic(
    integrator: str,
    time_step: float,
    num_steps: int,
    mass: float,
    omega: float,
    position0: float,
    velocity0: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate a harmonic oscillator with a named one-step scheme."""

    times = np.arange(num_steps + 1, dtype=float) * time_step
    positions = np.empty(num_steps + 1, dtype=float)
    velocities = np.empty(num_steps + 1, dtype=float)
    positions[0] = position0
    velocities[0] = velocity0

    position = float(position0)
    velocity = float(velocity0)
    for step in range(num_steps):
        if integrator == "velocity_verlet":
            acceleration = -(omega**2) * position
            position_next = position + velocity * time_step + 0.5 * acceleration * time_step**2
            acceleration_next = -(omega**2) * position_next
            velocity_next = velocity + 0.5 * (acceleration + acceleration_next) * time_step
        elif integrator == "explicit_euler":
            acceleration = -(omega**2) * position
            position_next = position + velocity * time_step
            velocity_next = velocity + acceleration * time_step
        else:
            msg = f"unsupported integrator: {integrator}"
            raise ValueError(msg)

        position = position_next
        velocity = velocity_next
        positions[step + 1] = position
        velocities[step + 1] = velocity

    return times, positions, velocities


def reversibility_error(
    integrator: str,
    time_step: float,
    num_steps: int,
    mass: float,
    omega: float,
    position0: float,
    velocity0: float,
) -> float:
    """Integrate forward, reverse velocity, integrate again, and compare state."""

    _, positions, velocities = integrate_harmonic(
        integrator, time_step, num_steps, mass, omega, position0, velocity0
    )
    _, back_positions, back_velocities = integrate_harmonic(
        integrator,
        time_step,
        num_steps,
        mass,
        omega,
        float(positions[-1]),
        float(-velocities[-1]),
    )
    return float(np.hypot(back_positions[-1] - position0, back_velocities[-1] + velocity0))


def summarize_integrator_run(
    integrator: str,
    time_step: float,
    num_steps: int,
    mass: float,
    omega: float,
    position0: float,
    velocity0: float,
) -> IntegratorRunSummary:
    """Compute compact error diagnostics for one integrator run."""

    times, positions, velocities = integrate_harmonic(
        integrator, time_step, num_steps, mass, omega, position0, velocity0
    )
    exact_positions, _ = exact_harmonic(times, position0, velocity0, omega)
    energy = harmonic_energy(positions, velocities, mass, omega)
    initial_energy = float(energy[0])
    relative_error = (energy - initial_energy) / initial_energy
    position_error = positions - exact_positions

    return IntegratorRunSummary(
        integrator=integrator,
        time_step=float(time_step),
        num_steps=int(num_steps),
        final_time=float(times[-1]),
        initial_energy=initial_energy,
        final_energy=float(energy[-1]),
        signed_energy_drift=float(energy[-1] - initial_energy),
        max_abs_relative_energy_error=float(np.max(np.abs(relative_error))),
        rms_position_error=float(np.sqrt(np.mean(position_error**2))),
        final_position_error=float(position_error[-1]),
        reversibility_error=reversibility_error(
            integrator, time_step, num_steps, mass, omega, position0, velocity0
        ),
    )


def run_integrator_experiment(spec: IntegratorTutorialSpec, config_sha256: str) -> IntegratorExperimentSummary:
    """Run every configured integrator/timestep diagnostic."""

    system = spec.system
    runs = [
        summarize_integrator_run(
            integrator=integrator,
            time_step=time_step,
            num_steps=spec.experiment.num_steps,
            mass=system.mass,
            omega=system.omega,
            position0=system.position,
            velocity0=system.velocity,
        )
        for time_step in spec.experiment.time_steps
        for integrator in spec.experiment.integrators
    ]
    return IntegratorExperimentSummary(
        post=spec.post,
        profile=spec.profile,
        seed=spec.experiment.seed,
        mass=system.mass,
        omega=system.omega,
        initial_position=system.position,
        initial_velocity=system.velocity,
        config_sha256=config_sha256,
        runs=runs,
    )


def _write_samples(
    path: Path,
    spec: IntegratorTutorialSpec,
    integrator: str,
    time_step: float,
    max_rows: int = 600,
) -> None:
    times, positions, velocities = integrate_harmonic(
        integrator,
        time_step,
        spec.experiment.num_steps,
        spec.system.mass,
        spec.system.omega,
        spec.system.position,
        spec.system.velocity,
    )
    exact_positions, exact_velocities = exact_harmonic(
        times, spec.system.position, spec.system.velocity, spec.system.omega
    )
    stride = max(1, int(np.ceil(len(times) / max_rows)))
    energy = harmonic_energy(positions, velocities, spec.system.mass, spec.system.omega)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "time",
                "position",
                "velocity",
                "exact_position",
                "exact_velocity",
                "energy",
            ]
        )
        for idx in range(0, len(times), stride):
            writer.writerow(
                [
                    f"{times[idx]:.12g}",
                    f"{positions[idx]:.12g}",
                    f"{velocities[idx]:.12g}",
                    f"{exact_positions[idx]:.12g}",
                    f"{exact_velocities[idx]:.12g}",
                    f"{energy[idx]:.12g}",
                ]
            )


def write_integrator_outputs(
    spec: IntegratorTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-02 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary = run_integrator_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "integrator_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_samples.csv"

    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(
        samples_path,
        spec,
        spec.experiment.reference_integrator,
        max(spec.experiment.time_steps),
    )
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


def load_integrator_summary(path: Path) -> IntegratorExperimentSummary:
    """Read a previously written integrator experiment summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [IntegratorRunSummary(**run) for run in data.pop("runs")]
    return IntegratorExperimentSummary(runs=runs, **data)
