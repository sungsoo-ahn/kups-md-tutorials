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
class ErrorTutorialSpec:
    """Configuration for post-03 simulation-error diagnostics."""

    post: str
    profile: str
    title: str
    system: HarmonicOscillatorSpec
    experiment: ErrorExperimentSpec

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
class ThermostatTutorialSpec:
    """Configuration for post-04 thermostat experiments."""

    post: str
    profile: str
    title: str
    system: HarmonicOscillatorSpec
    experiment: ThermostatExperimentSpec

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
class BarostatTutorialSpec:
    """Configuration for post-05 barostat experiments."""

    post: str
    profile: str
    title: str
    experiment: BarostatExperimentSpec

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
class TrajectoryLengthTutorialSpec:
    """Configuration for post-06 trajectory-length experiments."""

    post: str
    profile: str
    title: str
    experiment: TrajectoryLengthExperimentSpec

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
class ObservableTutorialSpec:
    """Configuration for post-07 observable-estimator experiments."""

    post: str
    profile: str
    title: str
    experiment: ObservableExperimentSpec

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
class EstimatorTutorialSpec:
    """Configuration for post-09 free-energy estimator experiments."""

    post: str
    profile: str
    title: str
    experiment: EstimatorExperimentSpec

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


def load_observable_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> ObservableTutorialSpec:
    """Load a committed JSON configuration for observable diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "observable config")
    experiment = _expect_mapping(root.get("observable_experiment"), "observable_experiment")
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


def load_free_energy_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> FreeEnergyTutorialSpec:
    """Load a committed JSON configuration for free-energy diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "free-energy config")
    experiment = _expect_mapping(root.get("free_energy_experiment"), "free_energy_experiment")
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


def load_estimator_spec(
    post: str, profile: str, config_root: Path = Path("configs")
) -> EstimatorTutorialSpec:
    """Load a committed JSON configuration for estimator diagnostics."""

    path = config_root / f"post-{post}" / f"{profile}.json"
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    root = _expect_mapping(data, "estimator config")
    experiment = _expect_mapping(root.get("estimator_experiment"), "estimator_experiment")
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
