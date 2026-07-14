"""Thermostat sampling and dynamics diagnostics for post 04."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import ase
import kups
import numpy as np

from kups_md_tutorials.config import ThermostatCase, ThermostatTutorialSpec
from kups_md_tutorials.error_diagnostics import _lennard_jones_forces
from kups_md_tutorials.provenance import provenance
from kups_md_tutorials.systems import argon_fcc


@dataclass(frozen=True)
class ThermostatRunSummary:
    """Compact diagnostics for one thermostat run."""

    thermostat: str
    method: str
    gamma: float
    samples: int
    position_mean: float
    position_variance: float
    velocity_mean: float
    velocity_variance: float
    kinetic_mean: float
    kinetic_variance: float
    expected_position_variance: float
    expected_velocity_variance: float
    expected_kinetic_mean: float
    position_variance_relative_error: float
    velocity_variance_relative_error: float
    kinetic_mean_relative_error: float
    position_lag1_autocorrelation: float
    velocity_lag1_autocorrelation: float
    position_integrated_autocorrelation_time: float
    position_effective_samples: float


@dataclass(frozen=True)
class ArgonThermostatRunSummary:
    """Compact diagnostics for one argon Langevin thermostat run."""

    thermostat: str
    gamma: float
    atom_count: int
    samples: int
    target_temperature: float
    kinetic_temperature_mean: float
    kinetic_temperature_std: float
    kinetic_temperature_relative_error: float
    velocity_lag1_autocorrelation: float
    velocity_integrated_autocorrelation_time: float
    final_total_energy: float


@dataclass(frozen=True)
class ThermostatExperimentSummary:
    """Summary table for one post/profile thermostat experiment."""

    post: str
    profile: str
    mass: float
    omega: float
    temperature: float
    time_step: float
    sample_every: int
    seed: int
    config_sha256: str
    runs: list[ThermostatRunSummary]
    argon_langevin_runs: list[ArgonThermostatRunSummary]


def simulate_baoab_langevin(
    *,
    mass: float,
    omega: float,
    temperature: float,
    time_step: float,
    num_steps: int,
    warmup_steps: int,
    sample_every: int,
    gamma: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run a 1D harmonic oscillator with BAOAB Langevin dynamics."""

    rng = np.random.default_rng(seed)
    position = float(rng.normal(0.0, np.sqrt(temperature / (mass * omega**2))))
    velocity = float(rng.normal(0.0, np.sqrt(temperature / mass)))
    c = float(np.exp(-gamma * time_step))
    sigma = float(np.sqrt((temperature / mass) * (1.0 - c**2)))
    samples: list[tuple[float, float, float]] = []

    for step in range(num_steps):
        acceleration = -(omega**2) * position
        velocity += 0.5 * time_step * acceleration
        position += 0.5 * time_step * velocity
        velocity = c * velocity + sigma * rng.normal()
        position += 0.5 * time_step * velocity
        acceleration = -(omega**2) * position
        velocity += 0.5 * time_step * acceleration

        if step >= warmup_steps and (step - warmup_steps) % sample_every == 0:
            samples.append((step * time_step, position, velocity))

    data = np.array(samples, dtype=float)
    return data[:, 0], data[:, 1], data[:, 2]


def _lag_autocorrelation(values: np.ndarray, lag: int = 1) -> float:
    centered = values - np.mean(values)
    denominator = float(np.dot(centered, centered))
    if denominator == 0.0 or len(centered) <= lag:
        return 0.0
    return float(np.dot(centered[:-lag], centered[lag:]) / denominator)


def _integrated_autocorrelation_time(values: np.ndarray, max_lag: int = 400) -> float:
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


def summarize_thermostat_run(
    *,
    spec: ThermostatTutorialSpec,
    thermostat: ThermostatCase,
    seed_offset: int,
) -> tuple[ThermostatRunSummary, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Run and summarize one thermostat configuration."""

    exp = spec.experiment
    system = spec.system
    times, positions, velocities = simulate_baoab_langevin(
        mass=system.mass,
        omega=system.omega,
        temperature=exp.temperature,
        time_step=exp.time_step,
        num_steps=exp.num_steps,
        warmup_steps=exp.warmup_steps,
        sample_every=exp.sample_every,
        gamma=thermostat.gamma,
        seed=exp.seed + seed_offset,
    )
    kinetic = 0.5 * system.mass * velocities**2
    expected_position_variance = exp.temperature / (system.mass * system.omega**2)
    expected_velocity_variance = exp.temperature / system.mass
    expected_kinetic_mean = 0.5 * exp.temperature
    position_iat = _integrated_autocorrelation_time(positions)

    summary = ThermostatRunSummary(
        thermostat=thermostat.name,
        method=thermostat.method,
        gamma=thermostat.gamma,
        samples=len(positions),
        position_mean=float(np.mean(positions)),
        position_variance=float(np.var(positions, ddof=1)),
        velocity_mean=float(np.mean(velocities)),
        velocity_variance=float(np.var(velocities, ddof=1)),
        kinetic_mean=float(np.mean(kinetic)),
        kinetic_variance=float(np.var(kinetic, ddof=1)),
        expected_position_variance=expected_position_variance,
        expected_velocity_variance=expected_velocity_variance,
        expected_kinetic_mean=expected_kinetic_mean,
        position_variance_relative_error=float(
            np.var(positions, ddof=1) / expected_position_variance - 1.0
        ),
        velocity_variance_relative_error=float(
            np.var(velocities, ddof=1) / expected_velocity_variance - 1.0
        ),
        kinetic_mean_relative_error=float(
            np.mean(kinetic) / expected_kinetic_mean - 1.0
        ),
        position_lag1_autocorrelation=_lag_autocorrelation(positions, lag=1),
        velocity_lag1_autocorrelation=_lag_autocorrelation(velocities, lag=1),
        position_integrated_autocorrelation_time=position_iat,
        position_effective_samples=float(len(positions) / position_iat),
    )
    return summary, (times, positions, velocities)


def run_thermostat_experiment(
    spec: ThermostatTutorialSpec, config_sha256: str
) -> tuple[ThermostatExperimentSummary, dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]]:
    """Run all configured thermostat diagnostics."""

    summaries = []
    trajectories = {}
    for idx, thermostat in enumerate(spec.experiment.thermostats):
        summary, trajectory = summarize_thermostat_run(
            spec=spec,
            thermostat=thermostat,
            seed_offset=idx * 1009,
        )
        summaries.append(summary)
        trajectories[thermostat.name] = trajectory
    return (
        ThermostatExperimentSummary(
            post=spec.post,
            profile=spec.profile,
            mass=spec.system.mass,
            omega=spec.system.omega,
            temperature=spec.experiment.temperature,
            time_step=spec.experiment.time_step,
            sample_every=spec.experiment.sample_every,
            seed=spec.experiment.seed,
            config_sha256=config_sha256,
            runs=summaries,
            argon_langevin_runs=run_argon_langevin_experiment(spec),
        ),
        trajectories,
    )


def run_argon_langevin_experiment(
    spec: ThermostatTutorialSpec,
) -> list[ArgonThermostatRunSummary]:
    """Run optional compact argon Langevin thermostat diagnostics."""

    if spec.argon_langevin is None:
        return []
    return [
        summarize_argon_langevin_run(spec, case_index=idx)[0]
        for idx, _ in enumerate(spec.argon_langevin.cases)
    ]


def summarize_argon_langevin_run(
    spec: ThermostatTutorialSpec,
    case_index: int,
) -> tuple[ArgonThermostatRunSummary, tuple[np.ndarray, np.ndarray]]:
    """Simulate reduced-unit argon with BAOAB Langevin dynamics."""

    if spec.argon_langevin is None:
        msg = "argon_langevin config is required"
        raise ValueError(msg)
    argon = spec.argon_langevin
    case = argon.cases[case_index]
    atoms = argon_fcc(argon.repetitions, argon.number_density)
    positions = atoms.get_positions().astype(float)
    box = float(atoms.cell.lengths()[0])
    velocities = _initialized_argon_velocities(
        atom_count=len(atoms),
        temperature=argon.temperature,
        seed=argon.seed + case_index * 1009,
    )
    forces, potential = _lennard_jones_forces(
        positions,
        box_length=box,
        epsilon=argon.epsilon,
        sigma=argon.sigma,
        cutoff=argon.cutoff,
    )
    c = float(np.exp(-case.gamma * argon.time_step))
    sigma_v = float(np.sqrt(argon.temperature * (1.0 - c**2)))
    rng = np.random.default_rng(argon.seed + case_index * 1009 + 17)
    times: list[float] = []
    kinetic_temperatures: list[float] = []
    velocity_memory: list[float] = []

    for step in range(argon.num_steps):
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
            kinetic = 0.5 * float(np.sum(velocities**2))
            kinetic_temperature = 2.0 * kinetic / (3 * len(atoms) - 3)
            times.append(step * argon.time_step)
            kinetic_temperatures.append(kinetic_temperature)
            velocity_memory.append(float(np.mean(np.sum(velocities * velocities, axis=1))))

    time_array = np.asarray(times, dtype=float)
    temperature_array = np.asarray(kinetic_temperatures, dtype=float)
    memory_array = np.asarray(velocity_memory, dtype=float)
    velocity_iat = _integrated_autocorrelation_time(memory_array)
    final_energy = float(0.5 * np.sum(velocities**2) + potential)
    summary = ArgonThermostatRunSummary(
        thermostat=case.name,
        gamma=case.gamma,
        atom_count=len(atoms),
        samples=len(temperature_array),
        target_temperature=argon.temperature,
        kinetic_temperature_mean=float(np.mean(temperature_array)),
        kinetic_temperature_std=float(np.std(temperature_array, ddof=1)),
        kinetic_temperature_relative_error=float(
            np.mean(temperature_array) / argon.temperature - 1.0
        ),
        velocity_lag1_autocorrelation=_lag_autocorrelation(memory_array, lag=1),
        velocity_integrated_autocorrelation_time=velocity_iat,
        final_total_energy=final_energy,
    )
    return summary, (time_array, temperature_array)


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
            header.extend([f"{name}_position", f"{name}_velocity"])
        writer.writerow(header)
        for idx in range(0, len(first_times), stride):
            row: list[str] = [f"{first_times[idx]:.12g}"]
            for name in names:
                _, positions, velocities = trajectories[name]
                row.extend([f"{positions[idx]:.12g}", f"{velocities[idx]:.12g}"])
            writer.writerow(row)


def _write_argon_langevin_samples(
    path: Path,
    spec: ThermostatTutorialSpec,
    max_rows: int = 800,
) -> None:
    if spec.argon_langevin is None:
        return

    trajectories = {
        spec.argon_langevin.cases[idx].name: summarize_argon_langevin_run(spec, idx)[1]
        for idx in range(len(spec.argon_langevin.cases))
    }
    longest = max(len(times) for times, _ in trajectories.values())
    stride = max(1, int(np.ceil(longest / max_rows)))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["thermostat", "time", "kinetic_temperature"])
        for name, (times, temperatures) in trajectories.items():
            for idx in range(0, len(times), stride):
                writer.writerow(
                    [
                        name,
                        f"{times[idx]:.12g}",
                        f"{temperatures[idx]:.12g}",
                    ]
                )


def write_thermostat_outputs(
    spec: ThermostatTutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Run post-04 diagnostics and write compact outputs."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    prov = provenance(config_path)
    summary, trajectories = run_thermostat_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "thermostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "thermostat_samples.csv"
    argon_samples_path = output_dir / "argon_langevin_samples.csv"

    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, trajectories)
    _write_argon_langevin_samples(argon_samples_path, spec)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
        "argon_langevin_samples_file": (
            argon_samples_path.name if spec.argon_langevin is not None else None
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


def load_thermostat_summary(path: Path) -> ThermostatExperimentSummary:
    """Read a previously written post-04 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [ThermostatRunSummary(**run) for run in data.pop("runs")]
    argon_langevin_runs = [
        ArgonThermostatRunSummary(**run)
        for run in data.pop("argon_langevin_runs", [])
    ]
    return ThermostatExperimentSummary(
        runs=runs,
        argon_langevin_runs=argon_langevin_runs,
        **data,
    )
