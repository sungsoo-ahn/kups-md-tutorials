"""Typed configuration objects for tutorial runs."""

from dataclasses import dataclass
from pathlib import Path


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
