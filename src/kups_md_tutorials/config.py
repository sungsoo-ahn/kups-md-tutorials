"""Typed configuration objects for tutorial runs."""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunSpec:
    """Configuration for one reproducible molecular-dynamics run."""

    name: str
    integrator: str
    time_step_fs: float
    temperature_k: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    seed: int

    def validate(self) -> None:
        """Raise ``ValueError`` when the run cannot be sampled reproducibly."""

        if not self.name:
            msg = "name must be non-empty"
            raise ValueError(msg)
        if self.time_step_fs <= 0.0:
            msg = "time_step_fs must be positive"
            raise ValueError(msg)
        if self.temperature_k < 0.0:
            msg = "temperature_k must be non-negative"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0:
            msg = "warmup_steps must be non-negative"
            raise ValueError(msg)
        if self.warmup_steps >= self.num_steps:
            msg = "warmup_steps must be smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "sample_every must be positive"
            raise ValueError(msg)
        if self.num_steps % self.sample_every != 0:
            msg = "sample_every must evenly divide num_steps"
            raise ValueError(msg)

    def output_path(self, run_dir: Path) -> Path:
        """Return the deterministic HDF5 output path for this run."""

        return run_dir / f"{self.name}.h5"

    @property
    def sample_dt_fs(self) -> float:
        """Physical time between recorded samples in femtoseconds."""

        return self.time_step_fs * self.sample_every


@dataclass(frozen=True)
class SystemSpec:
    """Atomic system construction parameters for one tutorial profile."""

    kind: str
    repetitions: int
    number_density: float | None = None
    lattice_constant: float | None = None


@dataclass(frozen=True)
class InitializationSpec:
    """Velocity and state preparation parameters."""

    temperature_k: float
    seed: int
    remove_center_of_mass: bool = True
    force_exact_temperature: bool = False


@dataclass(frozen=True)
class TutorialSpec:
    """Configuration for one tutorial/profile executable workflow."""

    post: str
    profile: str
    title: str
    system: SystemSpec
    initialization: InitializationSpec

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class HarmonicOscillatorSpec:
    """Dimensionless harmonic oscillator parameters for integrator diagnostics."""

    kind: str
    mass: float
    omega: float
    position: float
    velocity: float


@dataclass(frozen=True)
class IntegratorExperimentSpec:
    """Configuration for deterministic integrator error diagnostics."""

    time_steps: tuple[float, ...]
    num_steps: int
    integrators: tuple[str, ...]
    reference_integrator: str

    def validate(self) -> None:
        if not self.time_steps:
            msg = "time_steps must be non-empty"
            raise ValueError(msg)
        if any(time_step <= 0.0 for time_step in self.time_steps):
            msg = "time_steps must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "num_steps must be positive"
            raise ValueError(msg)
        if not self.integrators:
            msg = "integrators must be non-empty"
            raise ValueError(msg)
        if self.reference_integrator not in self.integrators:
            msg = "reference_integrator must be one of integrators"
            raise ValueError(msg)


@dataclass(frozen=True)
class IntegratorTutorialSpec:
    """Configuration for post-02 harmonic oscillator integrator experiments."""

    post: str
    profile: str
    title: str
    system: HarmonicOscillatorSpec
    experiment: IntegratorExperimentSpec

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class ForceErrorCase:
    """One deterministic force model perturbation for post-03 diagnostics."""

    name: str
    force_scale: float


@dataclass(frozen=True)
class ErrorExperimentSpec:
    """Configuration for timestep, precision, and force-error diagnostics."""

    num_steps: int
    time_steps: tuple[float, ...]
    precisions: tuple[str, ...]
    force_cases: tuple[ForceErrorCase, ...]

    def validate(self) -> None:
        if self.num_steps <= 0:
            msg = "num_steps must be positive"
            raise ValueError(msg)
        if not self.time_steps:
            msg = "time_steps must be non-empty"
            raise ValueError(msg)
        if any(time_step <= 0.0 for time_step in self.time_steps):
            msg = "time_steps must be positive"
            raise ValueError(msg)
        if not self.precisions:
            msg = "precisions must be non-empty"
            raise ValueError(msg)
        if not self.force_cases:
            msg = "force_cases must be non-empty"
            raise ValueError(msg)
        if any(not case.name for case in self.force_cases):
            msg = "force case names must be non-empty"
            raise ValueError(msg)
        if any(case.force_scale <= 0.0 for case in self.force_cases):
            msg = "force_scale must be positive"
            raise ValueError(msg)


@dataclass(frozen=True)
class ArgonNveSpec:
    """Configuration for compact argon NVE energy-drift diagnostics."""

    protocol_label: str
    repetitions: int
    number_density: float
    temperature: float
    seed: int
    replica_count: int
    num_steps: int
    sample_every: int
    time_steps: tuple[float, ...]
    epsilon: float
    sigma: float
    cutoff: float
    target_device: str

    def validate(self) -> None:
        if not self.protocol_label:
            msg = "argon_nve protocol_label must be non-empty"
            raise ValueError(msg)
        if self.repetitions <= 0:
            msg = "argon_nve repetitions must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon_nve number_density must be positive"
            raise ValueError(msg)
        if self.temperature <= 0.0:
            msg = "argon_nve temperature must be positive"
            raise ValueError(msg)
        if self.replica_count <= 0:
            msg = "argon_nve replica_count must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "argon_nve num_steps must be positive"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "argon_nve sample_every must be positive"
            raise ValueError(msg)
        if self.num_steps % self.sample_every != 0:
            msg = "argon_nve sample_every must evenly divide num_steps"
            raise ValueError(msg)
        if not self.time_steps:
            msg = "argon_nve time_steps must be non-empty"
            raise ValueError(msg)
        if any(time_step <= 0.0 for time_step in self.time_steps):
            msg = "argon_nve time_steps must be positive"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon_nve epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon_nve sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= self.sigma:
            msg = "argon_nve cutoff must be larger than sigma"
            raise ValueError(msg)
        if not self.target_device:
            msg = "argon_nve target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class ErrorTutorialSpec:
    """Configuration for post-03 simulation-error diagnostics."""

    post: str
    profile: str
    title: str
    system: HarmonicOscillatorSpec
    experiment: ErrorExperimentSpec
    argon_nve: ArgonNveSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class ThermostatCase:
    """One thermostat configuration for post-04 diagnostics."""

    name: str
    method: str
    gamma: float


@dataclass(frozen=True)
class ThermostatExperimentSpec:
    """Configuration for thermostat sampling and dynamics diagnostics."""

    temperature: float
    time_step: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    seed: int
    thermostats: tuple[ThermostatCase, ...]

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "time_step must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.num_steps:
            msg = "warmup_steps must be non-negative and smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "sample_every must be positive"
            raise ValueError(msg)
        if not self.thermostats:
            msg = "thermostats must be non-empty"
            raise ValueError(msg)
        for thermostat in self.thermostats:
            if not thermostat.name:
                msg = "thermostat names must be non-empty"
                raise ValueError(msg)
            if thermostat.method != "baoab_langevin":
                msg = f"unsupported thermostat method: {thermostat.method}"
                raise ValueError(msg)
            if thermostat.gamma <= 0.0:
                msg = "gamma must be positive"
                raise ValueError(msg)


@dataclass(frozen=True)
class ArgonThermostatCase:
    """One compact argon thermostat setting for post-04 diagnostics."""

    name: str
    gamma: float


@dataclass(frozen=True)
class ArgonThermostatSpec:
    """Configuration for compact argon Langevin thermostat diagnostics."""

    protocol_label: str
    repetitions: int
    number_density: float
    temperature: float
    seed: int
    replica_count: int
    time_step: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    nve_handoff_steps: int
    nve_handoff_sample_every: int
    epsilon: float
    sigma: float
    cutoff: float
    target_device: str
    cases: tuple[ArgonThermostatCase, ...]

    def validate(self) -> None:
        if not self.protocol_label:
            msg = "argon_langevin protocol_label must be non-empty"
            raise ValueError(msg)
        if self.repetitions <= 0:
            msg = "argon_langevin repetitions must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon_langevin number_density must be positive"
            raise ValueError(msg)
        if self.temperature <= 0.0:
            msg = "argon_langevin temperature must be positive"
            raise ValueError(msg)
        if self.replica_count <= 0:
            msg = "argon_langevin replica_count must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "argon_langevin time_step must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "argon_langevin num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.num_steps:
            msg = "argon_langevin warmup_steps must be non-negative and smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "argon_langevin sample_every must be positive"
            raise ValueError(msg)
        if self.nve_handoff_steps <= 0:
            msg = "argon_langevin nve_handoff_steps must be positive"
            raise ValueError(msg)
        if self.nve_handoff_sample_every <= 0:
            msg = "argon_langevin nve_handoff_sample_every must be positive"
            raise ValueError(msg)
        if self.nve_handoff_steps % self.nve_handoff_sample_every != 0:
            msg = "argon_langevin nve_handoff_sample_every must evenly divide nve_handoff_steps"
            raise ValueError(msg)
        if not self.cases:
            msg = "argon_langevin cases must be non-empty"
            raise ValueError(msg)
        if any(not case.name for case in self.cases):
            msg = "argon_langevin case names must be non-empty"
            raise ValueError(msg)
        if any(case.gamma <= 0.0 for case in self.cases):
            msg = "argon_langevin gamma must be positive"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon_langevin epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon_langevin sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= self.sigma:
            msg = "argon_langevin cutoff must be larger than sigma"
            raise ValueError(msg)
        if not self.target_device:
            msg = "argon_langevin target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class ThermostatTutorialSpec:
    """Configuration for post-04 thermostat experiments."""

    post: str
    profile: str
    title: str
    system: HarmonicOscillatorSpec
    experiment: ThermostatExperimentSpec
    argon_langevin: ArgonThermostatSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class BarostatCase:
    """One barostat relaxation-time setting for post-05 diagnostics."""

    name: str
    relaxation_time: float


@dataclass(frozen=True)
class BarostatExperimentSpec:
    """Configuration for scalar NPT pressure/cell diagnostics."""

    temperature: float
    target_pressure: float
    equilibrium_volume: float
    compressibility: float
    time_step: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    seed: int
    barostats: tuple[BarostatCase, ...]

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.equilibrium_volume <= 0.0:
            msg = "equilibrium_volume must be positive"
            raise ValueError(msg)
        if self.compressibility <= 0.0:
            msg = "compressibility must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "time_step must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.num_steps:
            msg = "warmup_steps must be non-negative and smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "sample_every must be positive"
            raise ValueError(msg)
        if not self.barostats:
            msg = "barostats must be non-empty"
            raise ValueError(msg)
        for barostat in self.barostats:
            if not barostat.name:
                msg = "barostat names must be non-empty"
                raise ValueError(msg)
            if barostat.relaxation_time <= 0.0:
                msg = "relaxation_time must be positive"
                raise ValueError(msg)


@dataclass(frozen=True)
class ArgonCellResponseSpec:
    """Configuration for compact reduced-unit argon pressure-volume checks."""

    repetitions: int
    number_density: float
    temperature: float
    volume_factors: tuple[float, ...]
    epsilon: float = 1.0
    sigma: float = 1.0
    cutoff: float = 2.5

    def validate(self) -> None:
        if self.repetitions <= 0:
            msg = "argon repetitions must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon number_density must be positive"
            raise ValueError(msg)
        if self.temperature < 0.0:
            msg = "argon temperature must be non-negative"
            raise ValueError(msg)
        if not self.volume_factors:
            msg = "argon volume_factors must be non-empty"
            raise ValueError(msg)
        if any(factor <= 0.0 for factor in self.volume_factors):
            msg = "argon volume_factors must be positive"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= 0.0:
            msg = "argon cutoff must be positive"
            raise ValueError(msg)


@dataclass(frozen=True)
class ArgonNPTDynamicsSpec:
    """Configuration for compact reduced-unit argon moving-cell checks."""

    repetitions: int
    replica_count: int
    number_density: float
    target_pressure: float
    temperature: float
    compressibility: float
    relaxation_time: float
    time_step: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    initial_volume_factor: float
    seed: int
    target_device: str
    epsilon: float = 1.0
    sigma: float = 1.0
    cutoff: float = 2.5

    def validate(self) -> None:
        if self.repetitions <= 0:
            msg = "argon NPT repetitions must be positive"
            raise ValueError(msg)
        if self.replica_count <= 0:
            msg = "argon NPT replica_count must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon NPT number_density must be positive"
            raise ValueError(msg)
        if self.temperature <= 0.0:
            msg = "argon NPT temperature must be positive"
            raise ValueError(msg)
        if self.compressibility <= 0.0:
            msg = "argon NPT compressibility must be positive"
            raise ValueError(msg)
        if self.relaxation_time <= 0.0:
            msg = "argon NPT relaxation_time must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "argon NPT time_step must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "argon NPT num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.num_steps:
            msg = "argon NPT warmup_steps must be non-negative and smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "argon NPT sample_every must be positive"
            raise ValueError(msg)
        if self.initial_volume_factor <= 0.0:
            msg = "argon NPT initial_volume_factor must be positive"
            raise ValueError(msg)
        if not self.target_device:
            msg = "argon NPT target_device must be non-empty"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon NPT epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon NPT sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= 0.0:
            msg = "argon NPT cutoff must be positive"
            raise ValueError(msg)


@dataclass(frozen=True)
class BarostatTutorialSpec:
    """Configuration for post-05 barostat experiments."""

    post: str
    profile: str
    title: str
    experiment: BarostatExperimentSpec
    argon_cell_response: ArgonCellResponseSpec | None = None
    argon_npt_dynamics: ArgonNPTDynamicsSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class TrajectoryLengthExperimentSpec:
    """Configuration for trajectory-length and uncertainty diagnostics."""

    true_mean: float
    stationary_variance: float
    correlation_time: float
    equilibration_time: float
    initial_bias: float
    time_step: float
    max_steps: int
    warmup_steps: int
    sample_every: int
    replica_count: int
    seed: int
    checkpoints: tuple[int, ...]

    def validate(self) -> None:
        if self.stationary_variance <= 0.0:
            msg = "stationary_variance must be positive"
            raise ValueError(msg)
        if self.correlation_time <= 0.0:
            msg = "correlation_time must be positive"
            raise ValueError(msg)
        if self.equilibration_time <= 0.0:
            msg = "equilibration_time must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "time_step must be positive"
            raise ValueError(msg)
        if self.max_steps <= 0:
            msg = "max_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.max_steps:
            msg = "warmup_steps must be non-negative and smaller than max_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "sample_every must be positive"
            raise ValueError(msg)
        if self.replica_count < 2:
            msg = "replica_count must be at least two"
            raise ValueError(msg)
        if not self.checkpoints:
            msg = "checkpoints must be non-empty"
            raise ValueError(msg)
        if any(checkpoint <= self.warmup_steps for checkpoint in self.checkpoints):
            msg = "checkpoints must exceed warmup_steps"
            raise ValueError(msg)
        if max(self.checkpoints) > self.max_steps:
            msg = "checkpoints cannot exceed max_steps"
            raise ValueError(msg)
        if tuple(sorted(self.checkpoints)) != self.checkpoints:
            msg = "checkpoints must be sorted"
            raise ValueError(msg)


@dataclass(frozen=True)
class ArgonTrajectoryLengthSpec:
    """Configuration for compact argon physical-observable length diagnostics."""

    repetitions: int
    number_density: float
    temperature: float
    gamma: float
    time_step: float
    max_steps: int
    warmup_steps: int
    sample_every: int
    replica_count: int
    seed: int
    checkpoints: tuple[int, ...]
    coordination_cutoff: float = 1.5
    epsilon: float = 1.0
    sigma: float = 1.0
    cutoff: float = 2.5
    target_device: str = "cpu"

    def validate(self) -> None:
        if self.repetitions <= 0:
            msg = "argon trajectory repetitions must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon trajectory number_density must be positive"
            raise ValueError(msg)
        if self.temperature <= 0.0:
            msg = "argon trajectory temperature must be positive"
            raise ValueError(msg)
        if self.gamma <= 0.0:
            msg = "argon trajectory gamma must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "argon trajectory time_step must be positive"
            raise ValueError(msg)
        if self.max_steps <= 0:
            msg = "argon trajectory max_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.max_steps:
            msg = "argon trajectory warmup_steps must be non-negative and smaller than max_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "argon trajectory sample_every must be positive"
            raise ValueError(msg)
        if self.replica_count < 2:
            msg = "argon trajectory replica_count must be at least two"
            raise ValueError(msg)
        if not self.checkpoints:
            msg = "argon trajectory checkpoints must be non-empty"
            raise ValueError(msg)
        if any(checkpoint <= self.warmup_steps for checkpoint in self.checkpoints):
            msg = "argon trajectory checkpoints must exceed warmup_steps"
            raise ValueError(msg)
        if max(self.checkpoints) > self.max_steps:
            msg = "argon trajectory checkpoints cannot exceed max_steps"
            raise ValueError(msg)
        if tuple(sorted(self.checkpoints)) != self.checkpoints:
            msg = "argon trajectory checkpoints must be sorted"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon trajectory epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon trajectory sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= self.sigma:
            msg = "argon trajectory cutoff must be larger than sigma"
            raise ValueError(msg)
        if self.coordination_cutoff <= 0.0:
            msg = "argon trajectory coordination_cutoff must be positive"
            raise ValueError(msg)
        if self.coordination_cutoff >= self.cutoff:
            msg = "argon trajectory coordination_cutoff must be smaller than cutoff"
            raise ValueError(msg)
        if not self.target_device:
            msg = "argon trajectory target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class TrajectoryLengthTutorialSpec:
    """Configuration for post-06 trajectory-length experiments."""

    post: str
    profile: str
    title: str
    experiment: TrajectoryLengthExperimentSpec
    argon_observable: ArgonTrajectoryLengthSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class ObservableSystemSpec:
    """One finite-size argon system for observable diagnostics."""

    name: str
    repetitions: int


@dataclass(frozen=True)
class ObservableExperimentSpec:
    """Configuration for RDF, coordination, and time-correlation diagnostics."""

    number_density: float
    displacement_sigma: float
    frame_count: int
    sample_every: int
    seed: int
    rdf_max_radius: float
    rdf_bin_width: float
    coordination_cutoff: float
    velocity_correlation_time: float
    max_vacf_lag: int
    systems: tuple[ObservableSystemSpec, ...]

    def validate(self) -> None:
        if self.number_density <= 0.0:
            msg = "number_density must be positive"
            raise ValueError(msg)
        if self.displacement_sigma < 0.0:
            msg = "displacement_sigma must be non-negative"
            raise ValueError(msg)
        if self.frame_count <= 1:
            msg = "frame_count must exceed one"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "sample_every must be positive"
            raise ValueError(msg)
        if self.rdf_max_radius <= 0.0:
            msg = "rdf_max_radius must be positive"
            raise ValueError(msg)
        if self.rdf_bin_width <= 0.0:
            msg = "rdf_bin_width must be positive"
            raise ValueError(msg)
        if self.coordination_cutoff <= 0.0:
            msg = "coordination_cutoff must be positive"
            raise ValueError(msg)
        if self.coordination_cutoff > self.rdf_max_radius:
            msg = "coordination_cutoff cannot exceed rdf_max_radius"
            raise ValueError(msg)
        if self.velocity_correlation_time <= 0.0:
            msg = "velocity_correlation_time must be positive"
            raise ValueError(msg)
        if self.max_vacf_lag <= 0 or self.max_vacf_lag >= self.frame_count:
            msg = "max_vacf_lag must be positive and smaller than frame_count"
            raise ValueError(msg)
        if not self.systems:
            msg = "systems must be non-empty"
            raise ValueError(msg)
        for system in self.systems:
            if not system.name:
                msg = "system names must be non-empty"
                raise ValueError(msg)
            if system.repetitions <= 0:
                msg = "system repetitions must be positive"
                raise ValueError(msg)


@dataclass(frozen=True)
class ArgonObservableTrajectorySpec:
    """Configuration for compact argon trajectory observable diagnostics."""

    repetitions: int
    number_density: float
    temperature: float
    gamma: float
    time_step: float
    num_steps: int
    warmup_steps: int
    sample_every: int
    seed: int
    rdf_max_radius: float
    rdf_bin_width: float
    coordination_cutoff: float
    max_vacf_lag: int
    epsilon: float = 1.0
    sigma: float = 1.0
    cutoff: float = 2.5
    uncertainty_block_count: int = 4
    uncertainty_replica_count: int = 3
    target_device: str = "cpu"

    def validate(self) -> None:
        if self.repetitions <= 0:
            msg = "argon trajectory repetitions must be positive"
            raise ValueError(msg)
        if self.number_density <= 0.0:
            msg = "argon trajectory number_density must be positive"
            raise ValueError(msg)
        if self.temperature <= 0.0:
            msg = "argon trajectory temperature must be positive"
            raise ValueError(msg)
        if self.gamma <= 0.0:
            msg = "argon trajectory gamma must be positive"
            raise ValueError(msg)
        if self.time_step <= 0.0:
            msg = "argon trajectory time_step must be positive"
            raise ValueError(msg)
        if self.num_steps <= 0:
            msg = "argon trajectory num_steps must be positive"
            raise ValueError(msg)
        if self.warmup_steps < 0 or self.warmup_steps >= self.num_steps:
            msg = "argon trajectory warmup_steps must be non-negative and smaller than num_steps"
            raise ValueError(msg)
        if self.sample_every <= 0:
            msg = "argon trajectory sample_every must be positive"
            raise ValueError(msg)
        sample_count = 1 + (self.num_steps - self.warmup_steps - 1) // self.sample_every
        if self.max_vacf_lag <= 0 or self.max_vacf_lag >= sample_count:
            msg = "argon trajectory max_vacf_lag must be positive and smaller than sample count"
            raise ValueError(msg)
        if self.rdf_max_radius <= 0.0:
            msg = "argon trajectory rdf_max_radius must be positive"
            raise ValueError(msg)
        if self.rdf_bin_width <= 0.0:
            msg = "argon trajectory rdf_bin_width must be positive"
            raise ValueError(msg)
        if self.coordination_cutoff <= 0.0:
            msg = "argon trajectory coordination_cutoff must be positive"
            raise ValueError(msg)
        if self.coordination_cutoff > self.rdf_max_radius:
            msg = "argon trajectory coordination_cutoff cannot exceed rdf_max_radius"
            raise ValueError(msg)
        if self.epsilon <= 0.0:
            msg = "argon trajectory epsilon must be positive"
            raise ValueError(msg)
        if self.sigma <= 0.0:
            msg = "argon trajectory sigma must be positive"
            raise ValueError(msg)
        if self.cutoff <= self.sigma:
            msg = "argon trajectory cutoff must be larger than sigma"
            raise ValueError(msg)
        if self.uncertainty_block_count < 2:
            msg = "argon trajectory uncertainty_block_count must be at least two"
            raise ValueError(msg)
        if self.uncertainty_replica_count < 2:
            msg = "argon trajectory uncertainty_replica_count must be at least two"
            raise ValueError(msg)
        if not self.target_device:
            msg = "argon trajectory target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class ObservableTutorialSpec:
    """Configuration for post-07 observable-estimator experiments."""

    post: str
    profile: str
    title: str
    experiment: ObservableExperimentSpec
    argon_trajectory: ArgonObservableTrajectorySpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class FreeEnergyExperimentSpec:
    """Configuration for equilibrium-sample free-energy diagnostics."""

    temperature: float
    sample_count: int
    seed: int
    domain_min: float
    domain_max: float
    grid_points: int
    bin_widths: tuple[float, ...]
    bootstrap_replicates: int
    bias_center: float
    bias_strength: float
    rdf_peak_radius: float
    rdf_peak_width: float

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.sample_count <= 0:
            msg = "sample_count must be positive"
            raise ValueError(msg)
        if self.domain_min >= self.domain_max:
            msg = "domain_min must be smaller than domain_max"
            raise ValueError(msg)
        if self.grid_points < 16:
            msg = "grid_points must be at least 16"
            raise ValueError(msg)
        if not self.bin_widths:
            msg = "bin_widths must be non-empty"
            raise ValueError(msg)
        if any(width <= 0.0 for width in self.bin_widths):
            msg = "bin_widths must be positive"
            raise ValueError(msg)
        if self.bootstrap_replicates <= 1:
            msg = "bootstrap_replicates must exceed one"
            raise ValueError(msg)
        if self.bias_strength <= 0.0:
            msg = "bias_strength must be positive"
            raise ValueError(msg)
        if self.rdf_peak_radius <= 0.0:
            msg = "rdf_peak_radius must be positive"
            raise ValueError(msg)
        if self.rdf_peak_width <= 0.0:
            msg = "rdf_peak_width must be positive"
            raise ValueError(msg)


@dataclass(frozen=True)
class FreeEnergyTutorialSpec:
    """Configuration for post-08 free-energy experiments."""

    post: str
    profile: str
    title: str
    experiment: FreeEnergyExperimentSpec
    argon_rdf_pmf: ArgonObservableTrajectorySpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class EstimatorCase:
    """One two-state overlap case for free-energy estimator diagnostics."""

    name: str
    mean_shift: float
    true_delta_f: float


@dataclass(frozen=True)
class EstimatorExperimentSpec:
    """Configuration for FEP/BAR overlap diagnostics."""

    temperature: float
    sample_count: int
    seed: int
    cases: tuple[EstimatorCase, ...]

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.sample_count <= 0:
            msg = "sample_count must be positive"
            raise ValueError(msg)
        if not self.cases:
            msg = "cases must be non-empty"
            raise ValueError(msg)
        for case in self.cases:
            if not case.name:
                msg = "case names must be non-empty"
                raise ValueError(msg)
            if case.mean_shift < 0.0:
                msg = "mean_shift must be non-negative"
                raise ValueError(msg)


@dataclass(frozen=True)
class MultiStateProtocolSpec:
    """One multi-state bridge layout for WHAM/MBAR-style diagnostics."""

    name: str
    window_centers: tuple[float, ...]


@dataclass(frozen=True)
class MultiStateOverlapSpec:
    """Configuration for multi-state overlap/reconstruction diagnostics."""

    sample_count_per_window: int
    seed: int
    force_constant: float
    domain_min: float
    domain_max: float
    bin_width: float
    protocols: tuple[MultiStateProtocolSpec, ...]

    def validate(self) -> None:
        if self.sample_count_per_window <= 0:
            msg = "sample_count_per_window must be positive"
            raise ValueError(msg)
        if self.force_constant <= 0.0:
            msg = "force_constant must be positive"
            raise ValueError(msg)
        if self.domain_min >= self.domain_max:
            msg = "domain_min must be smaller than domain_max"
            raise ValueError(msg)
        if self.bin_width <= 0.0:
            msg = "bin_width must be positive"
            raise ValueError(msg)
        if not self.protocols:
            msg = "protocols must be non-empty"
            raise ValueError(msg)
        for protocol in self.protocols:
            if not protocol.name:
                msg = "protocol names must be non-empty"
                raise ValueError(msg)
            if len(protocol.window_centers) < 2:
                msg = "multi-state protocols require at least two windows"
                raise ValueError(msg)
            if any(
                right <= left
                for left, right in zip(
                    protocol.window_centers[:-1],
                    protocol.window_centers[1:],
                    strict=False,
                )
            ):
                msg = "window_centers must be strictly increasing"
                raise ValueError(msg)


@dataclass(frozen=True)
class EstimatorTutorialSpec:
    """Configuration for post-09 free-energy estimator experiments."""

    post: str
    profile: str
    title: str
    experiment: EstimatorExperimentSpec
    multistate_overlap: MultiStateOverlapSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class UmbrellaProtocolSpec:
    """One umbrella-sampling window layout."""

    name: str
    force_constant: float
    window_centers: tuple[float, ...]


@dataclass(frozen=True)
class UmbrellaExperimentSpec:
    """Configuration for umbrella-sampling reconstruction diagnostics."""

    temperature: float
    domain_min: float
    domain_max: float
    grid_points: int
    bin_width: float
    sample_count_per_window: int
    seed: int
    protocols: tuple[UmbrellaProtocolSpec, ...]

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.domain_min >= self.domain_max:
            msg = "domain_min must be smaller than domain_max"
            raise ValueError(msg)
        if self.grid_points < 16:
            msg = "grid_points must be at least 16"
            raise ValueError(msg)
        if self.bin_width <= 0.0:
            msg = "bin_width must be positive"
            raise ValueError(msg)
        if self.sample_count_per_window <= 0:
            msg = "sample_count_per_window must be positive"
            raise ValueError(msg)
        if not self.protocols:
            msg = "protocols must be non-empty"
            raise ValueError(msg)
        for protocol in self.protocols:
            if not protocol.name:
                msg = "protocol names must be non-empty"
                raise ValueError(msg)
            if protocol.force_constant <= 0.0:
                msg = "force_constant must be positive"
                raise ValueError(msg)
            if len(protocol.window_centers) < 2:
                msg = "each protocol must contain at least two windows"
                raise ValueError(msg)
            if tuple(sorted(protocol.window_centers)) != protocol.window_centers:
                msg = "window_centers must be sorted"
                raise ValueError(msg)
            if any(
                center < self.domain_min or center > self.domain_max
                for center in protocol.window_centers
            ):
                msg = "window centers must lie inside the domain"
                raise ValueError(msg)


@dataclass(frozen=True)
class PairDistanceUmbrellaSpec:
    """Compact pair-distance umbrella diagnostic for post 10."""

    temperature: float
    domain_min: float
    domain_max: float
    grid_points: int
    bin_width: float
    sample_count_per_window: int
    seed: int
    force_constant: float
    window_centers: tuple[float, ...]
    epsilon: float = 1.0
    sigma: float = 1.0
    target_device: str = "cpu"

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "pair-distance temperature must be positive"
            raise ValueError(msg)
        if self.domain_min <= 0.0 or self.domain_min >= self.domain_max:
            msg = "pair-distance domain must be positive and ordered"
            raise ValueError(msg)
        if self.grid_points < 16:
            msg = "pair-distance grid_points must be at least 16"
            raise ValueError(msg)
        if self.bin_width <= 0.0:
            msg = "pair-distance bin_width must be positive"
            raise ValueError(msg)
        if self.sample_count_per_window <= 0:
            msg = "pair-distance sample_count_per_window must be positive"
            raise ValueError(msg)
        if self.force_constant <= 0.0:
            msg = "pair-distance force_constant must be positive"
            raise ValueError(msg)
        if len(self.window_centers) < 2:
            msg = "pair-distance umbrella requires at least two windows"
            raise ValueError(msg)
        if tuple(sorted(self.window_centers)) != self.window_centers:
            msg = "pair-distance window_centers must be sorted"
            raise ValueError(msg)
        if any(
            center < self.domain_min or center > self.domain_max
            for center in self.window_centers
        ):
            msg = "pair-distance window centers must lie inside the domain"
            raise ValueError(msg)
        if self.epsilon <= 0.0 or self.sigma <= 0.0:
            msg = "pair-distance epsilon and sigma must be positive"
            raise ValueError(msg)
        if not self.target_device:
            msg = "pair-distance target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class UmbrellaTutorialSpec:
    """Configuration for post-10 umbrella-sampling experiments."""

    post: str
    profile: str
    title: str
    experiment: UmbrellaExperimentSpec
    pair_distance_umbrella: PairDistanceUmbrellaSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class MetadynamicsSpec:
    """Configuration for the post-11 adaptive-bias diagnostic."""

    deposit_count: int
    hill_height: float
    hill_width: float
    bias_factor: float
    record_every: int


@dataclass(frozen=True)
class PullingSpec:
    """Configuration for the post-11 nonequilibrium-pulling diagnostic."""

    path_count: int
    path_steps: int
    trap_force_constant: float
    start_center: float
    end_center: float
    noise_scale: float


@dataclass(frozen=True)
class PairDistanceSteeredSpec:
    """Compact pair-distance steered-pulling diagnostic for post 11."""

    temperature: float
    domain_min: float
    domain_max: float
    grid_points: int
    path_count: int
    fast_path_steps: int
    slow_path_steps: int
    seed: int
    trap_force_constant: float
    start_radius: float
    end_radius: float
    noise_scale: float
    epsilon: float = 1.0
    sigma: float = 1.0
    target_device: str = "cpu"

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "pair-distance steered temperature must be positive"
            raise ValueError(msg)
        if self.domain_min <= 0.0 or self.domain_min >= self.domain_max:
            msg = "pair-distance steered domain must be positive and ordered"
            raise ValueError(msg)
        if self.grid_points < 16:
            msg = "pair-distance steered grid_points must be at least 16"
            raise ValueError(msg)
        if self.path_count <= 0:
            msg = "pair-distance steered path_count must be positive"
            raise ValueError(msg)
        if self.fast_path_steps <= 1 or self.slow_path_steps <= 1:
            msg = "pair-distance steered path counts must exceed one"
            raise ValueError(msg)
        if self.slow_path_steps <= self.fast_path_steps:
            msg = "pair-distance slow path must have more steps than fast path"
            raise ValueError(msg)
        if self.trap_force_constant <= 0.0:
            msg = "pair-distance steered trap_force_constant must be positive"
            raise ValueError(msg)
        if self.noise_scale < 0.0:
            msg = "pair-distance steered noise_scale must be non-negative"
            raise ValueError(msg)
        for radius in (self.start_radius, self.end_radius):
            if radius < self.domain_min or radius > self.domain_max:
                msg = "pair-distance steered radii must lie inside the domain"
                raise ValueError(msg)
        if self.epsilon <= 0.0 or self.sigma <= 0.0:
            msg = "pair-distance steered epsilon and sigma must be positive"
            raise ValueError(msg)
        if not self.target_device:
            msg = "pair-distance steered target_device must be non-empty"
            raise ValueError(msg)


@dataclass(frozen=True)
class EnhancedSamplingExperimentSpec:
    """Configuration for adaptive and nonequilibrium sampling diagnostics."""

    temperature: float
    domain_min: float
    domain_max: float
    grid_points: int
    seed: int
    metadynamics: MetadynamicsSpec
    pulling: PullingSpec

    def validate(self) -> None:
        if self.temperature <= 0.0:
            msg = "temperature must be positive"
            raise ValueError(msg)
        if self.domain_min >= self.domain_max:
            msg = "domain_min must be smaller than domain_max"
            raise ValueError(msg)
        if self.grid_points < 16:
            msg = "grid_points must be at least 16"
            raise ValueError(msg)
        if self.metadynamics.deposit_count <= 0:
            msg = "deposit_count must be positive"
            raise ValueError(msg)
        if self.metadynamics.hill_height <= 0.0:
            msg = "hill_height must be positive"
            raise ValueError(msg)
        if self.metadynamics.hill_width <= 0.0:
            msg = "hill_width must be positive"
            raise ValueError(msg)
        if self.metadynamics.bias_factor <= 1.0:
            msg = "bias_factor must exceed one"
            raise ValueError(msg)
        if self.metadynamics.record_every <= 0:
            msg = "record_every must be positive"
            raise ValueError(msg)
        if self.pulling.path_count <= 0:
            msg = "path_count must be positive"
            raise ValueError(msg)
        if self.pulling.path_steps <= 1:
            msg = "path_steps must exceed one"
            raise ValueError(msg)
        if self.pulling.trap_force_constant <= 0.0:
            msg = "trap_force_constant must be positive"
            raise ValueError(msg)
        if self.pulling.noise_scale < 0.0:
            msg = "noise_scale must be non-negative"
            raise ValueError(msg)
        for center in (self.pulling.start_center, self.pulling.end_center):
            if center < self.domain_min or center > self.domain_max:
                msg = "pulling centers must lie inside the domain"
                raise ValueError(msg)


@dataclass(frozen=True)
class EnhancedSamplingTutorialSpec:
    """Configuration for post-11 enhanced-sampling experiments."""

    post: str
    profile: str
    title: str
    experiment: EnhancedSamplingExperimentSpec
    pair_distance_steered: PairDistanceSteeredSpec | None = None

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


@dataclass(frozen=True)
class ModelArtifactSpec:
    """Pinned MLIP artifact metadata for post-12."""

    name: str
    repository: str
    revision: str
    sha256: str


@dataclass(frozen=True)
class MlipCaseSpec:
    """One MLIP reliability diagnostic regime."""

    name: str
    strain: float
    thermal_displacement: float
    force_noise: float
    force_bias: float
    uncertainty_scale: float


@dataclass(frozen=True)
class MlipExperimentSpec:
    """Configuration for MLIP capstone diagnostics."""

    material: str
    temperature_k: float
    seed: int
    sample_count: int
    time_step_fs: float
    model_artifact: ModelArtifactSpec
    cases: tuple[MlipCaseSpec, ...]

    def validate(self) -> None:
        if not self.material:
            msg = "material must be non-empty"
            raise ValueError(msg)
        if self.temperature_k <= 0.0:
            msg = "temperature_k must be positive"
            raise ValueError(msg)
        if self.sample_count <= 0:
            msg = "sample_count must be positive"
            raise ValueError(msg)
        if self.time_step_fs <= 0.0:
            msg = "time_step_fs must be positive"
            raise ValueError(msg)
        if not self.model_artifact.name:
            msg = "model artifact name must be non-empty"
            raise ValueError(msg)
        if not self.model_artifact.repository:
            msg = "model artifact repository must be non-empty"
            raise ValueError(msg)
        if not self.model_artifact.revision:
            msg = "model artifact revision must be non-empty"
            raise ValueError(msg)
        if not self.model_artifact.sha256:
            msg = "model artifact sha256 must be non-empty"
            raise ValueError(msg)
        if not self.cases:
            msg = "MLIP cases must be non-empty"
            raise ValueError(msg)
        for case in self.cases:
            if not case.name:
                msg = "MLIP case names must be non-empty"
                raise ValueError(msg)
            if case.thermal_displacement < 0.0:
                msg = "thermal_displacement must be non-negative"
                raise ValueError(msg)
            if case.force_noise < 0.0:
                msg = "force_noise must be non-negative"
                raise ValueError(msg)
            if case.uncertainty_scale <= 0.0:
                msg = "uncertainty_scale must be positive"
                raise ValueError(msg)


@dataclass(frozen=True)
class MlipTutorialSpec:
    """Configuration for post-12 MLIP capstone experiments."""

    post: str
    profile: str
    title: str
    experiment: MlipExperimentSpec

    @property
    def result_dir_name(self) -> Path:
        return Path(f"post-{self.post}") / self.profile


def _expect_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        msg = f"{name} must be an object"
        raise ValueError(msg)
    return value


def load_tutorial_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> TutorialSpec:
    """Load a committed JSON tutorial configuration."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "tutorial config")
    system = _expect_mapping(root.get("system"), "system")
    initialization = _expect_mapping(root.get("initialization"), "initialization")

    spec = TutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        system=SystemSpec(
            kind=str(system["kind"]),
            repetitions=int(system["repetitions"]),
            number_density=(
                None
                if system.get("number_density") is None
                else float(system["number_density"])
            ),
            lattice_constant=(
                None
                if system.get("lattice_constant") is None
                else float(system["lattice_constant"])
            ),
        ),
        initialization=InitializationSpec(
            temperature_k=float(initialization["temperature_k"]),
            seed=int(initialization["seed"]),
            remove_center_of_mass=bool(
                initialization.get("remove_center_of_mass", True)
            ),
            force_exact_temperature=bool(
                initialization.get("force_exact_temperature", False)
            ),
        ),
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    return spec


def load_integrator_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> IntegratorTutorialSpec:
    """Load a committed JSON configuration for integrator diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "integrator config")
    system = _expect_mapping(root.get("system"), "system")
    experiment = _expect_mapping(
        root.get("integrator_experiment"), "integrator_experiment"
    )

    spec = IntegratorTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        system=HarmonicOscillatorSpec(
            kind=str(system["kind"]),
            mass=float(system["mass"]),
            omega=float(system["omega"]),
            position=float(system["position"]),
            velocity=float(system["velocity"]),
        ),
        experiment=IntegratorExperimentSpec(
            time_steps=tuple(float(value) for value in experiment["time_steps"]),
            num_steps=int(experiment["num_steps"]),
            integrators=tuple(str(value) for value in experiment["integrators"]),
            reference_integrator=str(experiment["reference_integrator"]),
        ),
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    if spec.system.kind != "harmonic_oscillator":
        msg = f"unsupported integrator system kind: {spec.system.kind}"
        raise ValueError(msg)
    if spec.system.mass <= 0.0:
        msg = "harmonic oscillator mass must be positive"
        raise ValueError(msg)
    if spec.system.omega <= 0.0:
        msg = "harmonic oscillator omega must be positive"
        raise ValueError(msg)
    spec.experiment.validate()
    return spec


def load_error_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> ErrorTutorialSpec:
    """Load a committed JSON configuration for simulation-error diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "error config")
    system = _expect_mapping(root.get("system"), "system")
    experiment = _expect_mapping(root.get("error_experiment"), "error_experiment")
    argon_nve_data = root.get("argon_nve")
    argon_nve = None
    if argon_nve_data is not None:
        argon_nve_root = _expect_mapping(argon_nve_data, "argon_nve")
        argon_nve = ArgonNveSpec(
            protocol_label=str(argon_nve_root.get("protocol_label", "compact_lj_nve")),
            repetitions=int(argon_nve_root["repetitions"]),
            number_density=float(argon_nve_root["number_density"]),
            temperature=float(argon_nve_root["temperature"]),
            seed=int(argon_nve_root["seed"]),
            replica_count=int(argon_nve_root.get("replica_count", 1)),
            num_steps=int(argon_nve_root["num_steps"]),
            sample_every=int(argon_nve_root["sample_every"]),
            time_steps=tuple(float(value) for value in argon_nve_root["time_steps"]),
            epsilon=float(argon_nve_root["epsilon"]),
            sigma=float(argon_nve_root["sigma"]),
            cutoff=float(argon_nve_root["cutoff"]),
            target_device=str(argon_nve_root.get("target_device", "cpu")),
        )

    spec = ErrorTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        system=HarmonicOscillatorSpec(
            kind=str(system["kind"]),
            mass=float(system["mass"]),
            omega=float(system["omega"]),
            position=float(system["position"]),
            velocity=float(system["velocity"]),
        ),
        experiment=ErrorExperimentSpec(
            num_steps=int(experiment["num_steps"]),
            time_steps=tuple(float(value) for value in experiment["time_steps"]),
            precisions=tuple(str(value) for value in experiment["precisions"]),
            force_cases=tuple(
                ForceErrorCase(
                    name=str(_expect_mapping(value, "force case")["name"]),
                    force_scale=float(
                        _expect_mapping(value, "force case")["force_scale"]
                    ),
                )
                for value in experiment["force_cases"]
            ),
        ),
        argon_nve=argon_nve,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    if spec.system.kind != "harmonic_oscillator":
        msg = f"unsupported error system kind: {spec.system.kind}"
        raise ValueError(msg)
    if spec.system.mass <= 0.0:
        msg = "harmonic oscillator mass must be positive"
        raise ValueError(msg)
    if spec.system.omega <= 0.0:
        msg = "harmonic oscillator omega must be positive"
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_nve is not None:
        spec.argon_nve.validate()
    return spec


def load_thermostat_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> ThermostatTutorialSpec:
    """Load a committed JSON configuration for thermostat diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "thermostat config")
    system = _expect_mapping(root.get("system"), "system")
    experiment = _expect_mapping(
        root.get("thermostat_experiment"), "thermostat_experiment"
    )
    argon_data = root.get("argon_langevin")
    argon_langevin = None
    if argon_data is not None:
        argon_root = _expect_mapping(argon_data, "argon_langevin")
        argon_langevin = ArgonThermostatSpec(
            protocol_label=str(
                argon_root.get("protocol_label", "compact_argon_langevin")
            ),
            repetitions=int(argon_root["repetitions"]),
            number_density=float(argon_root["number_density"]),
            temperature=float(argon_root["temperature"]),
            seed=int(argon_root["seed"]),
            replica_count=int(argon_root.get("replica_count", 1)),
            time_step=float(argon_root["time_step"]),
            num_steps=int(argon_root["num_steps"]),
            warmup_steps=int(argon_root["warmup_steps"]),
            sample_every=int(argon_root["sample_every"]),
            nve_handoff_steps=int(argon_root.get("nve_handoff_steps", 1)),
            nve_handoff_sample_every=int(
                argon_root.get("nve_handoff_sample_every", 1)
            ),
            epsilon=float(argon_root["epsilon"]),
            sigma=float(argon_root["sigma"]),
            cutoff=float(argon_root["cutoff"]),
            target_device=str(argon_root.get("target_device", "cpu")),
            cases=tuple(
                ArgonThermostatCase(
                    name=str(_expect_mapping(value, "argon thermostat")["name"]),
                    gamma=float(_expect_mapping(value, "argon thermostat")["gamma"]),
                )
                for value in argon_root["cases"]
            ),
        )

    spec = ThermostatTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        system=HarmonicOscillatorSpec(
            kind=str(system["kind"]),
            mass=float(system["mass"]),
            omega=float(system["omega"]),
            position=0.0,
            velocity=0.0,
        ),
        experiment=ThermostatExperimentSpec(
            temperature=float(experiment["temperature"]),
            time_step=float(experiment["time_step"]),
            num_steps=int(experiment["num_steps"]),
            warmup_steps=int(experiment["warmup_steps"]),
            sample_every=int(experiment["sample_every"]),
            seed=int(experiment["seed"]),
            thermostats=tuple(
                ThermostatCase(
                    name=str(_expect_mapping(value, "thermostat")["name"]),
                    method=str(_expect_mapping(value, "thermostat")["method"]),
                    gamma=float(_expect_mapping(value, "thermostat")["gamma"]),
                )
                for value in experiment["thermostats"]
            ),
        ),
        argon_langevin=argon_langevin,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    if spec.system.kind != "harmonic_oscillator":
        msg = f"unsupported thermostat system kind: {spec.system.kind}"
        raise ValueError(msg)
    if spec.system.mass <= 0.0:
        msg = "harmonic oscillator mass must be positive"
        raise ValueError(msg)
    if spec.system.omega <= 0.0:
        msg = "harmonic oscillator omega must be positive"
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_langevin is not None:
        spec.argon_langevin.validate()
    return spec


def load_barostat_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> BarostatTutorialSpec:
    """Load a committed JSON configuration for pressure/cell diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "barostat config")
    experiment = _expect_mapping(
        root.get("barostat_experiment"), "barostat_experiment"
    )
    cell_response = root.get("argon_cell_response")
    npt_dynamics = root.get("argon_npt_dynamics")
    spec = BarostatTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=BarostatExperimentSpec(
            temperature=float(experiment["temperature"]),
            target_pressure=float(experiment["target_pressure"]),
            equilibrium_volume=float(experiment["equilibrium_volume"]),
            compressibility=float(experiment["compressibility"]),
            time_step=float(experiment["time_step"]),
            num_steps=int(experiment["num_steps"]),
            warmup_steps=int(experiment["warmup_steps"]),
            sample_every=int(experiment["sample_every"]),
            seed=int(experiment["seed"]),
            barostats=tuple(
                BarostatCase(
                    name=str(_expect_mapping(value, "barostat")["name"]),
                    relaxation_time=float(
                        _expect_mapping(value, "barostat")["relaxation_time"]
                    ),
                )
                for value in experiment["barostats"]
            ),
        ),
        argon_cell_response=(
            None
            if cell_response is None
            else ArgonCellResponseSpec(
                repetitions=int(_expect_mapping(cell_response, "argon_cell_response")["repetitions"]),
                number_density=float(_expect_mapping(cell_response, "argon_cell_response")["number_density"]),
                temperature=float(_expect_mapping(cell_response, "argon_cell_response")["temperature"]),
                volume_factors=tuple(
                    float(value)
                    for value in _expect_mapping(cell_response, "argon_cell_response")[
                        "volume_factors"
                    ]
                ),
                epsilon=float(_expect_mapping(cell_response, "argon_cell_response").get("epsilon", 1.0)),
                sigma=float(_expect_mapping(cell_response, "argon_cell_response").get("sigma", 1.0)),
                cutoff=float(_expect_mapping(cell_response, "argon_cell_response").get("cutoff", 2.5)),
            )
        ),
        argon_npt_dynamics=(
            None
            if npt_dynamics is None
            else ArgonNPTDynamicsSpec(
                repetitions=int(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["repetitions"]),
                replica_count=int(
                    _expect_mapping(npt_dynamics, "argon_npt_dynamics").get("replica_count", 1)
                ),
                number_density=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["number_density"]),
                target_pressure=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["target_pressure"]),
                temperature=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["temperature"]),
                compressibility=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["compressibility"]),
                relaxation_time=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["relaxation_time"]),
                time_step=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["time_step"]),
                num_steps=int(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["num_steps"]),
                warmup_steps=int(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["warmup_steps"]),
                sample_every=int(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["sample_every"]),
                initial_volume_factor=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["initial_volume_factor"]),
                seed=int(_expect_mapping(npt_dynamics, "argon_npt_dynamics")["seed"]),
                target_device=str(_expect_mapping(npt_dynamics, "argon_npt_dynamics").get("target_device", "cpu")),
                epsilon=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics").get("epsilon", 1.0)),
                sigma=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics").get("sigma", 1.0)),
                cutoff=float(_expect_mapping(npt_dynamics, "argon_npt_dynamics").get("cutoff", 2.5)),
            )
        ),
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_cell_response is not None:
        spec.argon_cell_response.validate()
    if spec.argon_npt_dynamics is not None:
        spec.argon_npt_dynamics.validate()
    return spec


def load_trajectory_length_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> TrajectoryLengthTutorialSpec:
    """Load a committed JSON configuration for trajectory-length diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "trajectory-length config")
    experiment = _expect_mapping(
        root.get("trajectory_length_experiment"),
        "trajectory_length_experiment",
    )

    spec = TrajectoryLengthTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=TrajectoryLengthExperimentSpec(
            true_mean=float(experiment["true_mean"]),
            stationary_variance=float(experiment["stationary_variance"]),
            correlation_time=float(experiment["correlation_time"]),
            equilibration_time=float(experiment["equilibration_time"]),
            initial_bias=float(experiment["initial_bias"]),
            time_step=float(experiment["time_step"]),
            max_steps=int(experiment["max_steps"]),
            warmup_steps=int(experiment["warmup_steps"]),
            sample_every=int(experiment["sample_every"]),
            replica_count=int(experiment["replica_count"]),
            seed=int(experiment["seed"]),
            checkpoints=tuple(int(value) for value in experiment["checkpoints"]),
        ),
        argon_observable=(
            None
            if root.get("argon_observable") is None
            else ArgonTrajectoryLengthSpec(
                repetitions=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "repetitions"
                    ]
                ),
                number_density=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "number_density"
                    ]
                ),
                temperature=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "temperature"
                    ]
                ),
                gamma=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "gamma"
                    ]
                ),
                time_step=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "time_step"
                    ]
                ),
                max_steps=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "max_steps"
                    ]
                ),
                warmup_steps=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "warmup_steps"
                    ]
                ),
                sample_every=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "sample_every"
                    ]
                ),
                replica_count=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "replica_count"
                    ]
                ),
                seed=int(
                    _expect_mapping(root.get("argon_observable"), "argon_observable")[
                        "seed"
                    ]
                ),
                checkpoints=tuple(
                    int(value)
                    for value in _expect_mapping(
                        root.get("argon_observable"), "argon_observable"
                    )["checkpoints"]
                ),
                coordination_cutoff=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable").get(
                        "coordination_cutoff", 1.5
                    )
                ),
                epsilon=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable").get(
                        "epsilon", 1.0
                    )
                ),
                sigma=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable").get(
                        "sigma", 1.0
                    )
                ),
                cutoff=float(
                    _expect_mapping(root.get("argon_observable"), "argon_observable").get(
                        "cutoff", 2.5
                    )
                ),
                target_device=str(
                    _expect_mapping(root.get("argon_observable"), "argon_observable").get(
                        "target_device", "cpu"
                    )
                ),
            )
        ),
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_observable is not None:
        spec.argon_observable.validate()
    return spec


def load_observable_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> ObservableTutorialSpec:
    """Load a committed JSON configuration for observable diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "observable config")
    experiment = _expect_mapping(root.get("observable_experiment"), "observable_experiment")
    argon_data = root.get("argon_trajectory")
    argon_trajectory = None
    if argon_data is not None:
        argon_root = _expect_mapping(argon_data, "argon_trajectory")
        argon_trajectory = ArgonObservableTrajectorySpec(
            repetitions=int(argon_root["repetitions"]),
            number_density=float(argon_root["number_density"]),
            temperature=float(argon_root["temperature"]),
            gamma=float(argon_root["gamma"]),
            time_step=float(argon_root["time_step"]),
            num_steps=int(argon_root["num_steps"]),
            warmup_steps=int(argon_root["warmup_steps"]),
            sample_every=int(argon_root["sample_every"]),
            seed=int(argon_root["seed"]),
            rdf_max_radius=float(argon_root["rdf_max_radius"]),
            rdf_bin_width=float(argon_root["rdf_bin_width"]),
            coordination_cutoff=float(argon_root["coordination_cutoff"]),
            max_vacf_lag=int(argon_root["max_vacf_lag"]),
            epsilon=float(argon_root.get("epsilon", 1.0)),
            sigma=float(argon_root.get("sigma", 1.0)),
            cutoff=float(argon_root.get("cutoff", 2.5)),
            uncertainty_block_count=int(argon_root.get("uncertainty_block_count", 4)),
            uncertainty_replica_count=int(argon_root.get("uncertainty_replica_count", 3)),
            target_device=str(argon_root.get("target_device", "cpu")),
        )
    spec = ObservableTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=ObservableExperimentSpec(
            number_density=float(experiment["number_density"]),
            displacement_sigma=float(experiment["displacement_sigma"]),
            frame_count=int(experiment["frame_count"]),
            sample_every=int(experiment["sample_every"]),
            seed=int(experiment["seed"]),
            rdf_max_radius=float(experiment["rdf_max_radius"]),
            rdf_bin_width=float(experiment["rdf_bin_width"]),
            coordination_cutoff=float(experiment["coordination_cutoff"]),
            velocity_correlation_time=float(experiment["velocity_correlation_time"]),
            max_vacf_lag=int(experiment["max_vacf_lag"]),
            systems=tuple(
                ObservableSystemSpec(
                    name=str(_expect_mapping(value, "observable system")["name"]),
                    repetitions=int(
                        _expect_mapping(value, "observable system")["repetitions"]
                    ),
                )
                for value in experiment["systems"]
            ),
        ),
        argon_trajectory=argon_trajectory,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_trajectory is not None:
        spec.argon_trajectory.validate()
    return spec


def load_free_energy_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> FreeEnergyTutorialSpec:
    """Load a committed JSON configuration for free-energy diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "free-energy config")
    experiment = _expect_mapping(root.get("free_energy_experiment"), "free_energy_experiment")
    argon_rdf_pmf = root.get("argon_rdf_pmf")
    parsed_argon_rdf_pmf = None
    if argon_rdf_pmf is not None:
        argon = _expect_mapping(argon_rdf_pmf, "argon_rdf_pmf")
        parsed_argon_rdf_pmf = ArgonObservableTrajectorySpec(
            repetitions=int(argon["repetitions"]),
            number_density=float(argon["number_density"]),
            temperature=float(argon["temperature"]),
            gamma=float(argon["gamma"]),
            time_step=float(argon["time_step"]),
            num_steps=int(argon["num_steps"]),
            warmup_steps=int(argon["warmup_steps"]),
            sample_every=int(argon["sample_every"]),
            seed=int(argon["seed"]),
            rdf_max_radius=float(argon["rdf_max_radius"]),
            rdf_bin_width=float(argon["rdf_bin_width"]),
            coordination_cutoff=float(argon["coordination_cutoff"]),
            max_vacf_lag=int(argon["max_vacf_lag"]),
            epsilon=float(argon.get("epsilon", 1.0)),
            sigma=float(argon.get("sigma", 1.0)),
            cutoff=float(argon.get("cutoff", 2.5)),
            uncertainty_block_count=int(argon.get("uncertainty_block_count", 4)),
            uncertainty_replica_count=int(argon.get("uncertainty_replica_count", 3)),
            target_device=str(argon.get("target_device", "cpu")),
        )
    spec = FreeEnergyTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=FreeEnergyExperimentSpec(
            temperature=float(experiment["temperature"]),
            sample_count=int(experiment["sample_count"]),
            seed=int(experiment["seed"]),
            domain_min=float(experiment["domain_min"]),
            domain_max=float(experiment["domain_max"]),
            grid_points=int(experiment["grid_points"]),
            bin_widths=tuple(float(value) for value in experiment["bin_widths"]),
            bootstrap_replicates=int(experiment["bootstrap_replicates"]),
            bias_center=float(experiment["bias_center"]),
            bias_strength=float(experiment["bias_strength"]),
            rdf_peak_radius=float(experiment["rdf_peak_radius"]),
            rdf_peak_width=float(experiment["rdf_peak_width"]),
        ),
        argon_rdf_pmf=parsed_argon_rdf_pmf,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.argon_rdf_pmf is not None:
        spec.argon_rdf_pmf.validate()
    return spec


def load_estimator_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> EstimatorTutorialSpec:
    """Load a committed JSON configuration for estimator diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "estimator config")
    experiment = _expect_mapping(root.get("estimator_experiment"), "estimator_experiment")
    multistate_data = root.get("multistate_overlap")
    multistate = None
    if multistate_data is not None:
        multistate_root = _expect_mapping(multistate_data, "multistate_overlap")
        multistate = MultiStateOverlapSpec(
            sample_count_per_window=int(multistate_root["sample_count_per_window"]),
            seed=int(multistate_root["seed"]),
            force_constant=float(multistate_root["force_constant"]),
            domain_min=float(multistate_root["domain_min"]),
            domain_max=float(multistate_root["domain_max"]),
            bin_width=float(multistate_root["bin_width"]),
            protocols=tuple(
                MultiStateProtocolSpec(
                    name=str(_expect_mapping(value, "multi-state protocol")["name"]),
                    window_centers=tuple(
                        float(center)
                        for center in _expect_mapping(
                            value, "multi-state protocol"
                        )["window_centers"]
                    ),
                )
                for value in multistate_root["protocols"]
            ),
        )
    spec = EstimatorTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=EstimatorExperimentSpec(
            temperature=float(experiment["temperature"]),
            sample_count=int(experiment["sample_count"]),
            seed=int(experiment["seed"]),
            cases=tuple(
                EstimatorCase(
                    name=str(_expect_mapping(value, "estimator case")["name"]),
                    mean_shift=float(
                        _expect_mapping(value, "estimator case")["mean_shift"]
                    ),
                    true_delta_f=float(
                        _expect_mapping(value, "estimator case")["true_delta_f"]
                    ),
                )
                for value in experiment["cases"]
            ),
        ),
        multistate_overlap=multistate,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.multistate_overlap is not None:
        spec.multistate_overlap.validate()
    return spec


def load_umbrella_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> UmbrellaTutorialSpec:
    """Load a committed JSON configuration for umbrella diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "umbrella config")
    experiment = _expect_mapping(root.get("umbrella_experiment"), "umbrella_experiment")
    pair_distance_data = root.get("pair_distance_umbrella")
    pair_distance_umbrella = None
    if pair_distance_data is not None:
        pair_distance = _expect_mapping(
            pair_distance_data,
            "pair_distance_umbrella",
        )
        pair_distance_umbrella = PairDistanceUmbrellaSpec(
            temperature=float(pair_distance["temperature"]),
            domain_min=float(pair_distance["domain_min"]),
            domain_max=float(pair_distance["domain_max"]),
            grid_points=int(pair_distance["grid_points"]),
            bin_width=float(pair_distance["bin_width"]),
            sample_count_per_window=int(pair_distance["sample_count_per_window"]),
            seed=int(pair_distance["seed"]),
            force_constant=float(pair_distance["force_constant"]),
            window_centers=tuple(
                float(center) for center in pair_distance["window_centers"]
            ),
            epsilon=float(pair_distance.get("epsilon", 1.0)),
            sigma=float(pair_distance.get("sigma", 1.0)),
            target_device=str(pair_distance.get("target_device", "cpu")),
        )
    spec = UmbrellaTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=UmbrellaExperimentSpec(
            temperature=float(experiment["temperature"]),
            domain_min=float(experiment["domain_min"]),
            domain_max=float(experiment["domain_max"]),
            grid_points=int(experiment["grid_points"]),
            bin_width=float(experiment["bin_width"]),
            sample_count_per_window=int(experiment["sample_count_per_window"]),
            seed=int(experiment["seed"]),
            protocols=tuple(
                UmbrellaProtocolSpec(
                    name=str(_expect_mapping(value, "umbrella protocol")["name"]),
                    force_constant=float(
                        _expect_mapping(value, "umbrella protocol")[
                            "force_constant"
                        ]
                    ),
                    window_centers=tuple(
                        float(center)
                        for center in _expect_mapping(
                            value,
                            "umbrella protocol",
                        )["window_centers"]
                    ),
                )
                for value in experiment["protocols"]
            ),
        ),
        pair_distance_umbrella=pair_distance_umbrella,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.pair_distance_umbrella is not None:
        spec.pair_distance_umbrella.validate()
    return spec


def load_enhanced_sampling_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> EnhancedSamplingTutorialSpec:
    """Load a committed JSON configuration for enhanced-sampling diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "enhanced-sampling config")
    experiment = _expect_mapping(
        root.get("enhanced_sampling_experiment"),
        "enhanced_sampling_experiment",
    )
    metadynamics = _expect_mapping(experiment.get("metadynamics"), "metadynamics")
    pulling = _expect_mapping(experiment.get("pulling"), "pulling")
    pair_distance_data = root.get("pair_distance_steered")
    pair_distance_steered = None
    if pair_distance_data is not None:
        pair_distance = _expect_mapping(
            pair_distance_data,
            "pair_distance_steered",
        )
        pair_distance_steered = PairDistanceSteeredSpec(
            temperature=float(pair_distance["temperature"]),
            domain_min=float(pair_distance["domain_min"]),
            domain_max=float(pair_distance["domain_max"]),
            grid_points=int(pair_distance["grid_points"]),
            path_count=int(pair_distance["path_count"]),
            fast_path_steps=int(pair_distance["fast_path_steps"]),
            slow_path_steps=int(pair_distance["slow_path_steps"]),
            seed=int(pair_distance["seed"]),
            trap_force_constant=float(pair_distance["trap_force_constant"]),
            start_radius=float(pair_distance["start_radius"]),
            end_radius=float(pair_distance["end_radius"]),
            noise_scale=float(pair_distance["noise_scale"]),
            epsilon=float(pair_distance.get("epsilon", 1.0)),
            sigma=float(pair_distance.get("sigma", 1.0)),
            target_device=str(pair_distance.get("target_device", "cpu")),
        )
    spec = EnhancedSamplingTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=EnhancedSamplingExperimentSpec(
            temperature=float(experiment["temperature"]),
            domain_min=float(experiment["domain_min"]),
            domain_max=float(experiment["domain_max"]),
            grid_points=int(experiment["grid_points"]),
            seed=int(experiment["seed"]),
            metadynamics=MetadynamicsSpec(
                deposit_count=int(metadynamics["deposit_count"]),
                hill_height=float(metadynamics["hill_height"]),
                hill_width=float(metadynamics["hill_width"]),
                bias_factor=float(metadynamics["bias_factor"]),
                record_every=int(metadynamics["record_every"]),
            ),
            pulling=PullingSpec(
                path_count=int(pulling["path_count"]),
                path_steps=int(pulling["path_steps"]),
                trap_force_constant=float(pulling["trap_force_constant"]),
                start_center=float(pulling["start_center"]),
                end_center=float(pulling["end_center"]),
                noise_scale=float(pulling["noise_scale"]),
            ),
        ),
        pair_distance_steered=pair_distance_steered,
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    if spec.pair_distance_steered is not None:
        spec.pair_distance_steered.validate()
    return spec


def load_mlip_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> MlipTutorialSpec:
    """Load a committed JSON configuration for MLIP diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "MLIP config")
    experiment = _expect_mapping(root.get("mlip_experiment"), "mlip_experiment")
    artifact = _expect_mapping(experiment.get("model_artifact"), "model_artifact")
    spec = MlipTutorialSpec(
        post=str(root["post"]),
        profile=str(root["profile"]),
        title=str(root["title"]),
        experiment=MlipExperimentSpec(
            material=str(experiment["material"]),
            temperature_k=float(experiment["temperature_k"]),
            seed=int(experiment["seed"]),
            sample_count=int(experiment["sample_count"]),
            time_step_fs=float(experiment["time_step_fs"]),
            model_artifact=ModelArtifactSpec(
                name=str(artifact["name"]),
                repository=str(artifact["repository"]),
                revision=str(artifact["revision"]),
                sha256=str(artifact["sha256"]),
            ),
            cases=tuple(
                MlipCaseSpec(
                    name=str(_expect_mapping(value, "MLIP case")["name"]),
                    strain=float(_expect_mapping(value, "MLIP case")["strain"]),
                    thermal_displacement=float(
                        _expect_mapping(value, "MLIP case")[
                            "thermal_displacement"
                        ]
                    ),
                    force_noise=float(
                        _expect_mapping(value, "MLIP case")["force_noise"]
                    ),
                    force_bias=float(_expect_mapping(value, "MLIP case")["force_bias"]),
                    uncertainty_scale=float(
                        _expect_mapping(value, "MLIP case")["uncertainty_scale"]
                    ),
                )
                for value in experiment["cases"]
            ),
        ),
    )
    if spec.post != post:
        msg = f"config post {spec.post!r} does not match requested {post!r}"
        raise ValueError(msg)
    if spec.profile != profile:
        msg = (
            f"config profile {spec.profile!r} does not match requested {profile!r}"
        )
        raise ValueError(msg)
    spec.experiment.validate()
    return spec
