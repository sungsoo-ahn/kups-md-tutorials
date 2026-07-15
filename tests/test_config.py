from pathlib import Path

import pytest

from kups_md_tutorials.config import (
    RunSpec,
    load_barostat_spec,
    load_enhanced_sampling_spec,
    load_error_spec,
    load_estimator_spec,
    load_free_energy_spec,
    load_integrator_spec,
    load_mlip_spec,
    load_observable_spec,
    load_trajectory_length_spec,
    load_thermostat_spec,
    load_umbrella_spec,
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
    assert spec.argon_nve is not None
    assert spec.argon_nve.repetitions == 2
    assert spec.argon_nve.time_steps[-1] == 0.005


def test_load_thermostat_spec() -> None:
    spec = load_thermostat_spec("04", "smoke")
    assert spec.system.kind == "harmonic_oscillator"
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.thermostats[0].method == "baoab_langevin"
    assert spec.argon_langevin is not None
    assert spec.argon_langevin.repetitions == 2
    assert spec.argon_langevin.cases[-1].gamma == 4.0


def test_load_barostat_spec() -> None:
    spec = load_barostat_spec("05", "smoke")
    assert spec.experiment.equilibrium_volume == 1000.0
    assert spec.experiment.compressibility == 0.01
    assert spec.experiment.barostats[0].name == "fast_barostat"
    assert spec.argon_cell_response is not None
    assert spec.argon_cell_response.number_density == 1.0
    assert spec.argon_npt_dynamics is not None
    assert spec.argon_npt_dynamics.initial_volume_factor < 1.0


def test_load_trajectory_length_spec() -> None:
    spec = load_trajectory_length_spec("06", "smoke")
    assert spec.experiment.true_mean == 0.5
    assert spec.argon_observable is not None
    assert spec.argon_observable.repetitions == 2
    assert spec.experiment.replica_count == 4
    assert spec.experiment.checkpoints[-1] == spec.experiment.max_steps


def test_load_observable_spec() -> None:
    spec = load_observable_spec("07", "smoke")
    assert spec.experiment.number_density == 0.021
    assert spec.experiment.systems[0].name == "small_cell"
    assert spec.experiment.coordination_cutoff < spec.experiment.rdf_max_radius
    assert spec.argon_trajectory is not None
    assert spec.argon_trajectory.repetitions == 2
    assert spec.argon_trajectory.uncertainty_replica_count == 3


def test_load_free_energy_spec() -> None:
    spec = load_free_energy_spec("08", "smoke")
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.bin_widths[0] == 0.10
    assert spec.experiment.domain_min < spec.experiment.domain_max
    assert spec.argon_rdf_pmf is not None
    assert spec.argon_rdf_pmf.repetitions == 2
    assert spec.argon_rdf_pmf.uncertainty_block_count == 4
    assert spec.argon_rdf_pmf.uncertainty_replica_count == 3


def test_load_estimator_spec() -> None:
    spec = load_estimator_spec("09", "smoke")
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.cases[0].name == "good_overlap"
    assert spec.experiment.cases[-1].mean_shift > spec.experiment.cases[0].mean_shift
    assert spec.multistate_overlap is not None
    assert spec.multistate_overlap.protocols[0].name == "dense_bridge"
    assert len(spec.multistate_overlap.protocols[0].window_centers) > len(
        spec.multistate_overlap.protocols[1].window_centers
    )


def test_load_umbrella_spec() -> None:
    spec = load_umbrella_spec("10", "smoke")
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.protocols[0].name == "dense_windows"
    assert len(spec.experiment.protocols[0].window_centers) > len(
        spec.experiment.protocols[1].window_centers
    )


def test_load_enhanced_sampling_spec() -> None:
    spec = load_enhanced_sampling_spec("11", "smoke")
    assert spec.experiment.temperature == 1.0
    assert spec.experiment.metadynamics.bias_factor > 1.0
    assert spec.experiment.pulling.path_count > 0


def test_load_mlip_spec() -> None:
    spec = load_mlip_spec("12", "smoke")
    assert spec.experiment.material == "fcc_aluminum"
    assert spec.experiment.model_artifact.name.startswith("mace")
    assert spec.experiment.cases[-1].strain > spec.experiment.cases[0].strain
