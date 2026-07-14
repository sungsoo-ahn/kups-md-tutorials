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
