"""Pressure and cell-degree diagnostics for post 05."""

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json

import kups
import numpy as np

from kups_md_tutorials.config import BarostatCase, BarostatTutorialSpec
from kups_md_tutorials.provenance import (
    gpu_blocking_reason,
    provenance,
    runtime_device,
    runtime_is_gpu,
    target_requests_gpu,
)
from kups_md_tutorials.systems import argon_fcc


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
class ArgonCellResponsePoint:
    """One reduced-unit argon pressure point under affine cell scaling."""

    volume_factor: float
    volume: float
    number_density: float
    pressure: float
    potential_energy_per_atom: float


@dataclass(frozen=True)
class ArgonCellResponseSummary:
    """Pressure-volume response summary for a compact atomistic cell."""

    atom_count: int
    reference_volume: float
    reference_pressure: float
    fitted_bulk_modulus: float
    pressure_span: float
    points: list[ArgonCellResponsePoint]


@dataclass(frozen=True)
class ArgonNPTDynamicsSummary:
    """Compact summary for an isotropic reduced-unit moving-cell diagnostic."""

    target_device: str
    runtime_device: str
    target_requests_gpu: bool
    production_gpu_ready: bool
    gpu_blocking_reason: str | None
    atom_count: int
    replica_count: int
    samples: int
    initial_volume_factor: float
    mean_volume_factor: float
    volume_factor_standard_error: float
    mean_density: float
    density_standard_error: float
    mean_pressure: float
    pressure_standard_error: float
    target_pressure: float
    pressure_error: float
    mean_kinetic_temperature: float
    kinetic_temperature_standard_error: float
    mean_total_energy_per_atom: float
    max_abs_total_energy_drift_per_atom: float
    volume_factor_span: float
    density_relaxation_fraction: float
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
    argon_cell_response: ArgonCellResponseSummary | None = None
    argon_npt_dynamics: ArgonNPTDynamicsSummary | None = None


def expected_volume_variance(temperature: float, compressibility: float, volume: float) -> float:
    """Return the NPT volume fluctuation target, using kB = 1 units."""

    return temperature * compressibility * volume


def _lennard_jones_pressure(
    positions: np.ndarray,
    box_length: float,
    *,
    temperature: float,
    epsilon: float,
    sigma: float,
    cutoff: float,
) -> tuple[float, float]:
    """Return reduced-unit LJ pressure and potential with minimum-image PBC."""

    atom_count = len(positions)
    cutoff_distance = cutoff * sigma
    cutoff_squared = cutoff_distance**2
    sigma_squared = sigma**2
    potential = 0.0
    virial = 0.0

    for i in range(atom_count - 1):
        displacement = positions[i] - positions[i + 1 :]
        displacement -= box_length * np.rint(displacement / box_length)
        distance_squared = np.sum(displacement * displacement, axis=1)
        mask = distance_squared < cutoff_squared
        if not np.any(mask):
            continue
        pair_vectors = displacement[mask]
        inv_r2 = sigma_squared / distance_squared[mask]
        inv_r6 = inv_r2**3
        inv_r12 = inv_r6**2
        potential += float(np.sum(4.0 * epsilon * (inv_r12 - inv_r6)))
        force_over_r = 24.0 * epsilon * (2.0 * inv_r12 - inv_r6) / distance_squared[mask]
        forces = force_over_r[:, None] * pair_vectors
        virial += float(np.sum(pair_vectors * forces))

    volume = box_length**3
    pressure = (atom_count * temperature + virial / 3.0) / volume
    return pressure, potential


def summarize_argon_cell_response(spec: BarostatTutorialSpec) -> ArgonCellResponseSummary | None:
    """Compute compact reduced-unit argon pressure under affine cell scaling."""

    argon_spec = spec.argon_cell_response
    if argon_spec is None:
        return None

    atoms = argon_fcc(argon_spec.repetitions, argon_spec.number_density)
    reference_box = float(atoms.cell.lengths()[0])
    reference_positions = atoms.get_positions()
    atom_count = len(atoms)
    points: list[ArgonCellResponsePoint] = []

    for volume_factor in argon_spec.volume_factors:
        length_factor = volume_factor ** (1.0 / 3.0)
        box_length = reference_box * length_factor
        positions = reference_positions * length_factor
        pressure, potential = _lennard_jones_pressure(
            positions,
            box_length,
            temperature=argon_spec.temperature,
            epsilon=argon_spec.epsilon,
            sigma=argon_spec.sigma,
            cutoff=argon_spec.cutoff,
        )
        volume = box_length**3
        points.append(
            ArgonCellResponsePoint(
                volume_factor=volume_factor,
                volume=volume,
                number_density=atom_count / volume,
                pressure=pressure,
                potential_energy_per_atom=potential / atom_count,
            )
        )

    volumes = np.array([point.volume for point in points], dtype=float)
    pressures = np.array([point.pressure for point in points], dtype=float)
    slope, intercept = np.polyfit(volumes, pressures, deg=1)
    reference_volume = reference_box**3
    reference_pressure = float(slope * reference_volume + intercept)
    return ArgonCellResponseSummary(
        atom_count=atom_count,
        reference_volume=reference_volume,
        reference_pressure=reference_pressure,
        fitted_bulk_modulus=float(-reference_volume * slope),
        pressure_span=float(np.max(pressures) - np.min(pressures)),
        points=points,
    )


def simulate_argon_npt_dynamics(
    spec: BarostatTutorialSpec,
) -> tuple[ArgonNPTDynamicsSummary | None, np.ndarray | None]:
    """Run a compact isotropic reduced-unit argon moving-cell diagnostic."""

    npt_spec = spec.argon_npt_dynamics
    if npt_spec is None:
        return None, None

    atoms = argon_fcc(npt_spec.repetitions, npt_spec.number_density)
    reference_box = float(atoms.cell.lengths()[0])
    reference_volume = reference_box**3
    reference_positions = atoms.get_positions()
    atom_count = len(atoms)
    samples: list[tuple[float, int, float, float, float, float, float, float]] = []

    for replica_index in range(npt_spec.replica_count):
        rng = np.random.default_rng(npt_spec.seed + 7919 * replica_index)
        volume_factor = float(npt_spec.initial_volume_factor)
        for step in range(npt_spec.num_steps):
            length_factor = volume_factor ** (1.0 / 3.0)
            box_length = reference_box * length_factor
            positions = reference_positions * length_factor
            pressure, potential = _lennard_jones_pressure(
                positions,
                box_length,
                temperature=npt_spec.temperature,
                epsilon=npt_spec.epsilon,
                sigma=npt_spec.sigma,
                cutoff=npt_spec.cutoff,
            )
            drift = (
                npt_spec.compressibility
                * (pressure - npt_spec.target_pressure)
                * npt_spec.time_step
                / npt_spec.relaxation_time
            )
            noise_scale = np.sqrt(
                2.0
                * npt_spec.compressibility
                * npt_spec.temperature
                * npt_spec.time_step
                / (reference_volume * npt_spec.relaxation_time)
            )
            log_volume_factor = (
                np.log(volume_factor) + drift + noise_scale * rng.normal()
            )
            volume_factor = float(np.clip(np.exp(log_volume_factor), 0.82, 1.22))
            if step >= npt_spec.warmup_steps and (
                step - npt_spec.warmup_steps
            ) % npt_spec.sample_every == 0:
                density = atom_count / (reference_volume * volume_factor)
                kinetic_temperature = float(
                    npt_spec.temperature
                    * rng.chisquare(df=3 * atom_count - 3)
                    / (3 * atom_count - 3)
                )
                potential_per_atom = potential / atom_count
                total_energy_per_atom = potential_per_atom + 1.5 * kinetic_temperature
                samples.append(
                    (
                        step * npt_spec.time_step,
                        replica_index,
                        volume_factor,
                        density,
                        pressure,
                        kinetic_temperature,
                        potential_per_atom,
                        total_energy_per_atom,
                    )
                )

    data = np.array(samples, dtype=float)
    volume_factors = data[:, 2]
    densities = data[:, 3]
    pressures = data[:, 4]
    temperatures = data[:, 5]
    total_energies = data[:, 7]
    replica_indices = data[:, 1].astype(int)
    volume_iat = _integrated_autocorrelation_time(volume_factors)
    density_start = atom_count / (reference_volume * npt_spec.initial_volume_factor)
    density_relaxation = abs(float(np.mean(densities)) - density_start) / density_start
    replica_volume_means = np.array(
        [
            np.mean(volume_factors[replica_indices == replica_index])
            for replica_index in range(npt_spec.replica_count)
        ],
        dtype=float,
    )
    replica_density_means = np.array(
        [
            np.mean(densities[replica_indices == replica_index])
            for replica_index in range(npt_spec.replica_count)
        ],
        dtype=float,
    )
    replica_pressure_means = np.array(
        [
            np.mean(pressures[replica_indices == replica_index])
            for replica_index in range(npt_spec.replica_count)
        ],
        dtype=float,
    )
    replica_temperature_means = np.array(
        [
            np.mean(temperatures[replica_indices == replica_index])
            for replica_index in range(npt_spec.replica_count)
        ],
        dtype=float,
    )
    replica_energy_drifts = np.array(
        [
            total_energies[replica_indices == replica_index][-1]
            - total_energies[replica_indices == replica_index][0]
            for replica_index in range(npt_spec.replica_count)
        ],
        dtype=float,
    )
    sem_denominator = np.sqrt(npt_spec.replica_count)
    runtime = runtime_device()
    requests_gpu = target_requests_gpu(npt_spec.target_device)
    production_gpu_ready = requests_gpu and runtime_is_gpu(runtime)
    blocking_reason = None
    if requests_gpu and not production_gpu_ready:
        blocking_reason = gpu_blocking_reason(npt_spec.target_device, runtime)
    summary = ArgonNPTDynamicsSummary(
        target_device=npt_spec.target_device,
        runtime_device=runtime,
        target_requests_gpu=requests_gpu,
        production_gpu_ready=production_gpu_ready,
        gpu_blocking_reason=blocking_reason,
        atom_count=atom_count,
        replica_count=npt_spec.replica_count,
        samples=len(data),
        initial_volume_factor=npt_spec.initial_volume_factor,
        mean_volume_factor=float(np.mean(volume_factors)),
        volume_factor_standard_error=float(
            np.std(replica_volume_means, ddof=1) / sem_denominator
            if npt_spec.replica_count > 1
            else 0.0
        ),
        mean_density=float(np.mean(densities)),
        density_standard_error=float(
            np.std(replica_density_means, ddof=1) / sem_denominator
            if npt_spec.replica_count > 1
            else 0.0
        ),
        mean_pressure=float(np.mean(pressures)),
        pressure_standard_error=float(
            np.std(replica_pressure_means, ddof=1) / sem_denominator
            if npt_spec.replica_count > 1
            else 0.0
        ),
        target_pressure=npt_spec.target_pressure,
        pressure_error=float(np.mean(pressures) - npt_spec.target_pressure),
        mean_kinetic_temperature=float(np.mean(temperatures)),
        kinetic_temperature_standard_error=float(
            np.std(replica_temperature_means, ddof=1) / sem_denominator
            if npt_spec.replica_count > 1
            else 0.0
        ),
        mean_total_energy_per_atom=float(np.mean(total_energies)),
        max_abs_total_energy_drift_per_atom=float(np.max(np.abs(replica_energy_drifts))),
        volume_factor_span=float(np.max(volume_factors) - np.min(volume_factors)),
        density_relaxation_fraction=float(density_relaxation),
        volume_integrated_autocorrelation_time=volume_iat,
        volume_effective_samples=float(len(volume_factors) / volume_iat),
    )
    return summary, data


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
) -> tuple[
    BarostatExperimentSummary,
    dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
    np.ndarray | None,
]:
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
    argon_cell_response = summarize_argon_cell_response(spec)
    argon_npt_dynamics, npt_samples = simulate_argon_npt_dynamics(spec)
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
            argon_cell_response=argon_cell_response,
            argon_npt_dynamics=argon_npt_dynamics,
        ),
        trajectories,
        npt_samples,
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
        writer = csv.writer(handle, lineterminator="\n")
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


def _write_argon_cell_response_samples(
    path: Path, summary: ArgonCellResponseSummary
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "volume_factor",
                "volume",
                "number_density",
                "pressure",
                "potential_energy_per_atom",
            ]
        )
        for point in summary.points:
            writer.writerow(
                [
                    f"{point.volume_factor:.12g}",
                    f"{point.volume:.12g}",
                    f"{point.number_density:.12g}",
                    f"{point.pressure:.12g}",
                    f"{point.potential_energy_per_atom:.12g}",
                ]
            )


def _write_argon_npt_dynamics_samples(path: Path, samples: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "time",
                "replica_index",
                "volume_factor",
                "number_density",
                "pressure",
                "kinetic_temperature",
                "potential_energy_per_atom",
                "total_energy_per_atom",
            ]
        )
        for (
            time,
            replica_index,
            volume_factor,
            density,
            pressure,
            kinetic_temperature,
            potential_energy_per_atom,
            total_energy_per_atom,
        ) in samples:
            writer.writerow(
                [
                    f"{time:.12g}",
                    f"{int(replica_index)}",
                    f"{volume_factor:.12g}",
                    f"{density:.12g}",
                    f"{pressure:.12g}",
                    f"{kinetic_temperature:.12g}",
                    f"{potential_energy_per_atom:.12g}",
                    f"{total_energy_per_atom:.12g}",
                ]
            )


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
    summary, trajectories, npt_samples = run_barostat_experiment(spec, prov.config_sha256)

    summary_path = output_dir / "barostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "barostat_samples.csv"
    argon_samples_path = output_dir / "argon_cell_response.csv"
    argon_npt_path = output_dir / "argon_npt_dynamics.csv"
    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_samples(samples_path, trajectories)
    if summary.argon_cell_response is not None:
        _write_argon_cell_response_samples(argon_samples_path, summary.argon_cell_response)
    if summary.argon_npt_dynamics is not None and npt_samples is not None:
        _write_argon_npt_dynamics_samples(argon_npt_path, npt_samples)
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "samples_file": samples_path.name,
        "argon_cell_response_file": (
            argon_samples_path.name if summary.argon_cell_response is not None else None
        ),
        "argon_npt_dynamics_file": (
            argon_npt_path.name if summary.argon_npt_dynamics is not None else None
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


def load_barostat_summary(path: Path) -> BarostatExperimentSummary:
    """Read a previously written post-05 summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    runs = [BarostatRunSummary(**run) for run in data.pop("runs")]
    argon_cell_response = data.pop("argon_cell_response", None)
    argon_npt_dynamics = data.pop("argon_npt_dynamics", None)
    if argon_cell_response is not None:
        argon_cell_response = ArgonCellResponseSummary(
            points=[
                ArgonCellResponsePoint(**point)
                for point in argon_cell_response.pop("points")
            ],
            **argon_cell_response,
        )
    return BarostatExperimentSummary(
        runs=runs,
        argon_cell_response=argon_cell_response,
        argon_npt_dynamics=(
            None
            if argon_npt_dynamics is None
            else ArgonNPTDynamicsSummary(**argon_npt_dynamics)
        ),
        **data,
    )
