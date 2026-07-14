from pathlib import Path

import pytest

from kups_md_tutorials.config import (
    RunSpec,
    load_barostat_spec,
    load_error_spec,
    load_integrator_spec,
    load_observable_spec,
    load_trajectory_length_spec,
    load_thermostat_spec,
)


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


def test_load_error_spec() -> None:
    spec = load_error_spec("03", "smoke")
    assert spec.system.kind == "harmonic_oscillator"
    assert "float64" in spec.experiment.precisions
    assert spec.experiment.force_cases[0].name == "exact_force"


def test_load_thermostat_spec() -> None:
    spec = load_thermostat_spec("04", "smoke")
    assert spec.system.kind == "harmonic_oscillator"
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.thermostats[0].method == "baoab_langevin"


def test_load_barostat_spec() -> None:
    spec = load_barostat_spec("05", "smoke")
    assert spec.experiment.equilibrium_volume == 1000.0
    assert spec.experiment.compressibility == 0.01
    assert spec.experiment.barostats[0].name == "fast_barostat"


def test_load_trajectory_length_spec() -> None:
    spec = load_trajectory_length_spec("06", "smoke")
    assert spec.experiment.true_mean == 0.5
    assert spec.experiment.replica_count == 4
    assert spec.experiment.checkpoints[-1] == spec.experiment.max_steps


def test_load_observable_spec() -> None:
    spec = load_observable_spec("07", "smoke")
    assert spec.experiment.number_density == 0.021
    assert spec.experiment.systems[0].name == "small_cell"
    assert spec.experiment.coordination_cutoff < spec.experiment.rdf_max_radius
