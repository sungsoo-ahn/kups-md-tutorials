from pathlib import Path

import pytest

from kups_md_tutorials.config import RunSpec, load_integrator_spec


def test_run_spec_validates_sampling_interval() -> None:
    spec = RunSpec(
        name="bad",
        integrator="verlet",
        time_step_fs=1.0,
        temperature_k=100.0,
        num_steps=10,
        warmup_steps=0,
        sample_every=3,
        seed=1,
    )
    with pytest.raises(ValueError, match="sample_every"):
        spec.validate()


def test_output_path_is_stable() -> None:
    spec = RunSpec(
        name="example",
        integrator="verlet",
        time_step_fs=1.0,
        temperature_k=100.0,
        num_steps=10,
        warmup_steps=0,
        sample_every=1,
        seed=1,
    )
    assert spec.output_path(Path("runs")) == Path("runs/example.h5")


def test_load_integrator_spec() -> None:
    spec = load_integrator_spec("02", "smoke")
    assert spec.system.kind == "harmonic_oscillator"
    assert spec.experiment.reference_integrator == "velocity_verlet"
    assert "explicit_euler" in spec.experiment.integrators
