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
