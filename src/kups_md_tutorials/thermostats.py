"""Thermostat sampling and dynamics diagnostics for post 04."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import ThermostatCase, ThermostatTutorialSpec
from kups_md_tutorials.provenance import provenance


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
            header.extend([f"{name}_position", f"{name}_velocity"])
        writer.writerow(header)
        for idx in range(0, len(first_times), stride):
            row: list[str] = [f"{first_times[idx]:.12g}"]
            for name in names:
                _, positions, velocities = trajectories[name]
                row.extend([f"{positions[idx]:.12g}", f"{velocities[idx]:.12g}"])
            writer.writerow(row)


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


def load_thermostat_summary(path: Path) -> ThermostatExperimentSummary:
    """Read a previously written post-04 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [ThermostatRunSummary(**run) for run in data.pop("runs")]
    return ThermostatExperimentSummary(runs=runs, **data)
