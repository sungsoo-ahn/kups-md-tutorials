"""Executable tutorial workflows exposed by the CLI."""

from pathlib import Path

import numpy as np

from kups_md_tutorials.config import (
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
    load_tutorial_spec,
    load_umbrella_spec,
)
from kups_md_tutorials.barostats import (
    load_barostat_summary,
    write_barostat_outputs,
)
from kups_md_tutorials.error_diagnostics import (
    load_error_summary,
    write_error_outputs,
)
from kups_md_tutorials.enhanced_sampling import (
    load_enhanced_sampling_summary,
    write_enhanced_sampling_outputs,
)
from kups_md_tutorials.estimators import (
    load_estimator_summary,
    write_estimator_outputs,
)
from kups_md_tutorials.initialization import (
    load_initialization_summary,
    write_initialization_outputs,
)
from kups_md_tutorials.integrators import (
    load_integrator_summary,
    write_integrator_outputs,
)
from kups_md_tutorials.mlip_capstone import (
    load_mlip_summary,
    write_mlip_outputs,
)
from kups_md_tutorials.free_energies import (
    load_free_energy_summary,
    write_free_energy_outputs,
)
from kups_md_tutorials.observables import (
    load_observable_summary,
    write_observable_outputs,
)
from kups_md_tutorials.thermostats import (
    load_thermostat_summary,
    write_thermostat_outputs,
)
from kups_md_tutorials.trajectory_length import (
    load_trajectory_length_summary,
    write_trajectory_length_outputs,
)
from kups_md_tutorials.umbrella_sampling import (
    load_umbrella_summary,
    write_umbrella_outputs,
)

SUPPORTED_POSTS = (
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
)
SUPPORTED_PROFILES = ("smoke", "full")


def run_post(post: str, profile: str, output_root: Path = Path("results")) -> Path:
    """Run one supported tutorial workflow."""

    if post == "01":
        spec = load_tutorial_spec(post, profile)
        return write_initialization_outputs(spec, output_root=output_root)
    if post == "02":
        spec = load_integrator_spec(post, profile)
        return write_integrator_outputs(spec, output_root=output_root)
    if post == "03":
        spec = load_error_spec(post, profile)
        return write_error_outputs(spec, output_root=output_root)
    if post == "04":
        spec = load_thermostat_spec(post, profile)
        return write_thermostat_outputs(spec, output_root=output_root)
    if post == "05":
        spec = load_barostat_spec(post, profile)
        return write_barostat_outputs(spec, output_root=output_root)
    if post == "06":
        spec = load_trajectory_length_spec(post, profile)
        return write_trajectory_length_outputs(spec, output_root=output_root)
    if post == "07":
        spec = load_observable_spec(post, profile)
        return write_observable_outputs(spec, output_root=output_root)
    if post == "08":
        spec = load_free_energy_spec(post, profile)
        return write_free_energy_outputs(spec, output_root=output_root)
    if post == "09":
        spec = load_estimator_spec(post, profile)
        return write_estimator_outputs(spec, output_root=output_root)
    if post == "10":
        spec = load_umbrella_spec(post, profile)
        return write_umbrella_outputs(spec, output_root=output_root)
    if post == "11":
        spec = load_enhanced_sampling_spec(post, profile)
        return write_enhanced_sampling_outputs(spec, output_root=output_root)
    if post == "12":
        spec = load_mlip_spec(post, profile)
        return write_mlip_outputs(spec, output_root=output_root)
    else:
        msg = f"post {post!r} is not implemented yet"
        raise NotImplementedError(msg)


def run_all(profile: str, output_root: Path = Path("results")) -> list[Path]:
    """Run every currently implemented tutorial workflow."""

    return [run_post(post, profile, output_root=output_root) for post in SUPPORTED_POSTS]


def verify_post(post: str, profile: str, output_root: Path = Path("results")) -> None:
    """Verify compact outputs for one tutorial workflow."""

    if post == "01":
        _verify_post01(post, profile, output_root)
    elif post == "02":
        _verify_post02(post, profile, output_root)
    elif post == "03":
        _verify_post03(post, profile, output_root)
    elif post == "04":
        _verify_post04(post, profile, output_root)
    elif post == "05":
        _verify_post05(post, profile, output_root)
    elif post == "06":
        _verify_post06(post, profile, output_root)
    elif post == "07":
        _verify_post07(post, profile, output_root)
    elif post == "08":
        _verify_post08(post, profile, output_root)
    elif post == "09":
        _verify_post09(post, profile, output_root)
    elif post == "10":
        _verify_post10(post, profile, output_root)
    elif post == "11":
        _verify_post11(post, profile, output_root)
    elif post == "12":
        _verify_post12(post, profile, output_root)
    else:
        msg = f"post {post!r} is not implemented yet"
        raise NotImplementedError(msg)


def verify_all(profile: str, output_root: Path = Path("results")) -> None:
    """Verify every currently implemented tutorial workflow."""

    for post in SUPPORTED_POSTS:
        verify_post(post, profile, output_root=output_root)


def _verify_post01(post: str, profile: str, output_root: Path) -> None:
    spec = load_tutorial_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "initialization_summary.json"
    manifest_path = output_dir / "manifest.json"
    structure_path = output_dir / "initial_state.extxyz"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, structure_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_initialization_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if summary.atom_count <= 0:
        msg = "summary contains no atoms"
        raise ValueError(msg)
    if summary.number_density <= 0:
        msg = "summary number density must be positive"
        raise ValueError(msg)
    if summary.center_of_mass_speed > 1.0e-12:
        msg = "center-of-mass speed is not sufficiently removed"
        raise ValueError(msg)


def _verify_post02(post: str, profile: str, output_root: Path) -> None:
    spec = load_integrator_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "integrator_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_integrator_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)

    expected_runs = len(spec.experiment.time_steps) * len(spec.experiment.integrators)
    if len(summary.runs) != expected_runs:
        msg = "summary does not contain the expected integrator/timestep grid"
        raise ValueError(msg)

    verlet_runs = [
        run for run in summary.runs if run.integrator == spec.experiment.reference_integrator
    ]
    if not verlet_runs:
        msg = "summary is missing the reference integrator"
        raise ValueError(msg)
    if max(run.reversibility_error for run in verlet_runs) > 1.0e-10:
        msg = "reference integrator reversibility error is unexpectedly large"
        raise ValueError(msg)
    if max(run.max_abs_relative_energy_error for run in verlet_runs) > 0.02:
        msg = "reference integrator energy error exceeds review threshold"
        raise ValueError(msg)


def _verify_post03(post: str, profile: str, output_root: Path) -> None:
    spec = load_error_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "error_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "error_samples.csv"
    argon_samples_path = output_dir / "argon_nve_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path, argon_samples_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_error_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)

    expected_runs = (
        len(spec.experiment.time_steps)
        * len(spec.experiment.precisions)
        * len(spec.experiment.force_cases)
    )
    if len(summary.runs) != expected_runs:
        msg = "summary does not contain the expected error grid"
        raise ValueError(msg)

    exact_float64 = [
        run
        for run in summary.runs
        if run.force_case == "exact_force" and run.precision == "float64"
    ]
    if not exact_float64:
        msg = "summary is missing exact-force float64 reference runs"
        raise ValueError(msg)
    if max(run.max_abs_relative_energy_error for run in exact_float64) > 0.01:
        msg = "exact-force float64 energy error exceeds review threshold"
        raise ValueError(msg)

    biased_runs = [run for run in summary.runs if run.force_case != "exact_force"]
    if not biased_runs:
        msg = "summary is missing force-error comparison runs"
        raise ValueError(msg)
    if max(abs(run.normalized_energy_drift) for run in biased_runs) <= 1.0e-6:
        msg = "force-error runs do not show measurable normalized drift"
        raise ValueError(msg)
    if spec.argon_nve is not None:
        expected_argon_runs = len(spec.argon_nve.time_steps) * spec.argon_nve.replica_count
        if len(summary.argon_nve_runs) != expected_argon_runs:
            msg = "summary does not contain the expected argon NVE timestep/replica grid"
            raise ValueError(msg)
        if summary.argon_nve_protocol is None:
            msg = "summary is missing argon NVE aggregate protocol diagnostics"
            raise ValueError(msg)
        if summary.argon_nve_protocol.replica_count != spec.argon_nve.replica_count:
            msg = "argon NVE aggregate replica count does not match config"
            raise ValueError(msg)
        if any(run.unstable for run in summary.argon_nve_runs):
            msg = "argon NVE diagnostic contains an unstable run"
            raise ValueError(msg)
        if max(run.max_abs_relative_energy_error for run in summary.argon_nve_runs) > 0.02:
            msg = "argon NVE energy error exceeds review threshold"
            raise ValueError(msg)
        if summary.argon_nve_protocol.unstable_run_count != 0:
            msg = "argon NVE aggregate reports unstable runs"
            raise ValueError(msg)
        if summary.argon_nve_protocol.max_abs_normalized_energy_drift > 1.0e-3:
            msg = "argon NVE aggregate normalized drift exceeds review threshold"
            raise ValueError(msg)
        if not summary.argon_nve_protocol.runtime_device:
            msg = "argon NVE aggregate is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_nve_protocol.target_requests_gpu
            and not summary.argon_nve_protocol.production_gpu_ready
            and not summary.argon_nve_protocol.gpu_blocking_reason
        ):
            msg = "argon NVE GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)


def _verify_post04(post: str, profile: str, output_root: Path) -> None:
    spec = load_thermostat_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "thermostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "thermostat_samples.csv"
    argon_samples_path = output_dir / "argon_langevin_samples.csv"
    argon_handoff_samples_path = output_dir / "argon_handoff_samples.csv"
    missing = [
        str(path)
        for path in (
            summary_path,
            manifest_path,
            samples_path,
            argon_samples_path,
            argon_handoff_samples_path,
        )
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_thermostat_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.runs) != len(spec.experiment.thermostats):
        msg = "summary does not contain the expected thermostat cases"
        raise ValueError(msg)
    if min(run.samples for run in summary.runs) <= 0:
        msg = "thermostat summary contains no samples"
        raise ValueError(msg)
    if max(abs(run.kinetic_mean_relative_error) for run in summary.runs) > 0.25:
        msg = "thermostat kinetic mean is outside the review threshold"
        raise ValueError(msg)
    if min(run.position_effective_samples for run in summary.runs) <= 5.0:
        msg = "thermostat effective sample count is too small"
        raise ValueError(msg)
    if spec.argon_langevin is not None:
        expected_argon_runs = (
            len(spec.argon_langevin.cases) * spec.argon_langevin.replica_count
        )
        if len(summary.argon_langevin_runs) != expected_argon_runs:
            msg = "summary does not contain the expected argon thermostat cases"
            raise ValueError(msg)
        if summary.argon_langevin_protocol is None:
            msg = "summary is missing the argon thermostat protocol aggregate"
            raise ValueError(msg)
        if summary.argon_langevin_protocol.replica_count != spec.argon_langevin.replica_count:
            msg = "argon thermostat protocol replica count does not match config"
            raise ValueError(msg)
        if not summary.argon_langevin_protocol.runtime_device:
            msg = "argon thermostat protocol is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_langevin_protocol.target_requests_gpu
            and not summary.argon_langevin_protocol.production_gpu_ready
            and not summary.argon_langevin_protocol.gpu_blocking_reason
        ):
            msg = "argon thermostat GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)
        if min(run.samples for run in summary.argon_langevin_runs) <= 0:
            msg = "argon thermostat summary contains no samples"
            raise ValueError(msg)
        if max(abs(run.kinetic_temperature_relative_error) for run in summary.argon_langevin_runs) > 0.35:
            msg = "argon thermostat kinetic temperature is outside the review threshold"
            raise ValueError(msg)
        ordered = sorted(summary.argon_langevin_runs, key=lambda run: run.gamma)
        if ordered[-1].velocity_integrated_autocorrelation_time >= (
            1.5 * ordered[0].velocity_integrated_autocorrelation_time
        ):
            msg = "strong argon thermostat did not reduce velocity-temperature memory"
            raise ValueError(msg)
        if summary.argon_langevin_protocol.unstable_handoff_count != 0:
            msg = "argon NVE handoff contains an unstable run"
            raise ValueError(msg)
        if summary.argon_langevin_protocol.max_abs_nve_handoff_drift > 1.0e-3:
            msg = "argon NVE handoff drift is outside the review threshold"
            raise ValueError(msg)


def _verify_post05(post: str, profile: str, output_root: Path) -> None:
    spec = load_barostat_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "barostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "barostat_samples.csv"
    argon_samples_path = output_dir / "argon_cell_response.csv"
    argon_npt_path = output_dir / "argon_npt_dynamics.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
    if spec.argon_cell_response is not None and not argon_samples_path.exists():
        missing.append(str(argon_samples_path))
    if spec.argon_npt_dynamics is not None and not argon_npt_path.exists():
        missing.append(str(argon_npt_path))
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_barostat_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.runs) != len(spec.experiment.barostats):
        msg = "summary does not contain the expected barostat cases"
        raise ValueError(msg)
    if min(run.samples for run in summary.runs) <= 0:
        msg = "barostat summary contains no samples"
        raise ValueError(msg)
    if max(abs(run.volume_variance_relative_error) for run in summary.runs) > 0.60:
        msg = "volume variance is outside the review threshold"
        raise ValueError(msg)
    if max(abs(run.pressure_variance_relative_error) for run in summary.runs) > 0.60:
        msg = "pressure variance is outside the review threshold"
        raise ValueError(msg)
    if min(run.volume_effective_samples for run in summary.runs) <= 5.0:
        msg = "barostat effective sample count is too small"
        raise ValueError(msg)
    if spec.argon_cell_response is not None:
        if summary.argon_cell_response is None:
            msg = "argon cell-response summary is missing"
            raise ValueError(msg)
        if len(summary.argon_cell_response.points) != len(
            spec.argon_cell_response.volume_factors
        ):
            msg = "argon cell-response summary has the wrong number of points"
            raise ValueError(msg)
        if summary.argon_cell_response.fitted_bulk_modulus <= 0.0:
            msg = "argon cell-response fitted bulk modulus must be positive"
            raise ValueError(msg)
        if summary.argon_cell_response.pressure_span <= 0.5:
            msg = "argon cell-response pressure span is too small"
            raise ValueError(msg)
    if spec.argon_npt_dynamics is not None:
        if summary.argon_npt_dynamics is None:
            msg = "argon NPT dynamics summary is missing"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.samples <= 0:
            msg = "argon NPT dynamics summary contains no samples"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.replica_count != spec.argon_npt_dynamics.replica_count:
            msg = "argon NPT dynamics replica count does not match config"
            raise ValueError(msg)
        if not summary.argon_npt_dynamics.runtime_device:
            msg = "argon NPT dynamics summary is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_npt_dynamics.target_requests_gpu
            and not summary.argon_npt_dynamics.production_gpu_ready
            and not summary.argon_npt_dynamics.gpu_blocking_reason
        ):
            msg = "argon NPT GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.volume_factor_span <= 0.005:
            msg = "argon NPT moving-cell span is too small"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.density_relaxation_fraction <= 0.01:
            msg = "argon NPT density relaxation is too small"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.volume_effective_samples <= 5.0:
            msg = "argon NPT effective sample count is too small"
            raise ValueError(msg)
        if abs(
            summary.argon_npt_dynamics.mean_kinetic_temperature
            - spec.argon_npt_dynamics.temperature
        ) > 0.15:
            msg = "argon NPT kinetic temperature is outside the review threshold"
            raise ValueError(msg)
        if summary.argon_npt_dynamics.max_abs_total_energy_drift_per_atom > 1.0:
            msg = "argon NPT total-energy drift is outside the review threshold"
            raise ValueError(msg)


def _verify_post06(post: str, profile: str, output_root: Path) -> None:
    spec = load_trajectory_length_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "trajectory_length_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_length_samples.csv"
    argon_samples_path = output_dir / "argon_observable_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
    if spec.argon_observable is not None and not argon_samples_path.exists():
        missing.append(str(argon_samples_path))
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_trajectory_length_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.checkpoints) != len(spec.experiment.checkpoints):
        msg = "summary does not contain the expected checkpoints"
        raise ValueError(msg)
    if min(checkpoint.total_samples for checkpoint in summary.checkpoints) <= 0:
        msg = "trajectory-length summary contains no samples"
        raise ValueError(msg)
    if any(
        checkpoint.conservative_standard_error <= checkpoint.naive_standard_error
        for checkpoint in summary.checkpoints
    ):
        msg = "conservative uncertainty should exceed naive uncertainty"
        raise ValueError(msg)
    if summary.checkpoints[-1].effective_samples <= summary.checkpoints[0].effective_samples:
        msg = "effective samples should increase with trajectory length"
        raise ValueError(msg)
    if summary.checkpoints[-1].conservative_ci95_half_width >= (
        0.75 * summary.checkpoints[0].conservative_ci95_half_width
    ):
        msg = "uncertainty did not shrink enough over the configured trajectory"
        raise ValueError(msg)
    if spec.argon_observable is not None:
        if summary.argon_observable is None:
            msg = "argon observable summary is missing"
            raise ValueError(msg)
        if len(summary.argon_observable.checkpoints) != len(
            spec.argon_observable.checkpoints
        ):
            msg = "argon observable summary has the wrong number of checkpoints"
            raise ValueError(msg)
        first = summary.argon_observable.checkpoints[0]
        last = summary.argon_observable.checkpoints[-1]
        if last.effective_samples <= first.effective_samples:
            msg = "argon observable effective samples should increase"
            raise ValueError(msg)
        if (
            profile == "full"
            and last.autocorrelation_standard_error >= first.autocorrelation_standard_error
        ):
            msg = "argon observable autocorrelation-adjusted uncertainty should shrink"
            raise ValueError(msg)
        if not np.isfinite(last.conservative_ci95_half_width):
            msg = "argon observable conservative uncertainty is not finite"
            raise ValueError(msg)
        if not np.isfinite(last.mean_potential_energy_per_atom):
            msg = "argon observable mean is not finite"
            raise ValueError(msg)
        if last.mean_coordination_number <= 0.0:
            msg = "argon coordination mean must be positive"
            raise ValueError(msg)
        if (
            profile == "full"
            and last.coordination_effective_samples <= first.coordination_effective_samples
        ):
            msg = "argon coordination effective samples should increase"
            raise ValueError(msg)
        if not np.isfinite(last.coordination_conservative_ci95_half_width):
            msg = "argon coordination conservative uncertainty is not finite"
            raise ValueError(msg)
        if not summary.argon_observable.runtime_device:
            msg = "argon observable summary is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_observable.target_requests_gpu
            and not summary.argon_observable.production_gpu_ready
            and not summary.argon_observable.gpu_blocking_reason
        ):
            msg = "argon observable GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)


def _verify_post07(post: str, profile: str, output_root: Path) -> None:
    spec = load_observable_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "observable_summary.json"
    manifest_path = output_dir / "manifest.json"
    rdf_path = output_dir / "rdf_samples.csv"
    vacf_path = output_dir / "vacf_samples.csv"
    argon_rdf_path = output_dir / "argon_trajectory_rdf_samples.csv"
    argon_vacf_path = output_dir / "argon_trajectory_vacf_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, rdf_path, vacf_path)
        if not path.exists()
    ]
    if spec.argon_trajectory is not None:
        missing.extend(
            str(path)
            for path in (argon_rdf_path, argon_vacf_path)
            if not path.exists()
        )
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_observable_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.systems) != len(spec.experiment.systems):
        msg = "summary does not contain the expected observable systems"
        raise ValueError(msg)
    if min(system.atom_count for system in summary.systems) <= 0:
        msg = "observable summary contains no atoms"
        raise ValueError(msg)
    if min(system.coordination_number for system in summary.systems) <= 0.0:
        msg = "coordination estimates must be positive"
        raise ValueError(msg)
    if min(system.rdf_first_peak_value for system in summary.systems) <= 1.0:
        msg = "RDF first peak should exceed the ideal-gas baseline"
        raise ValueError(msg)
    if len(summary.systems) >= 2:
        ordered = sorted(summary.systems, key=lambda system: system.atom_count)
        if ordered[-1].finite_size_shell_fraction >= ordered[0].finite_size_shell_fraction:
            msg = "larger system should reduce the RDF finite-size shell fraction"
            raise ValueError(msg)
    if summary.vacf.lag1_autocorrelation <= 0.0:
        msg = "VACF lag-1 autocorrelation should be positive"
        raise ValueError(msg)
    if summary.vacf.normalized_integral <= 0.0:
        msg = "VACF integral should be positive"
        raise ValueError(msg)
    if spec.argon_trajectory is not None:
        if summary.argon_trajectory is None:
            msg = "argon trajectory observable summary is missing"
            raise ValueError(msg)
        if summary.argon_trajectory.atom_count <= 0:
            msg = "argon trajectory observable summary contains no atoms"
            raise ValueError(msg)
        if summary.argon_trajectory.frame_count <= spec.argon_trajectory.max_vacf_lag:
            msg = "argon trajectory observable summary contains too few frames"
            raise ValueError(msg)
        if summary.argon_trajectory.rdf_first_peak_value <= 1.0:
            msg = "argon trajectory RDF first peak should exceed the ideal-gas baseline"
            raise ValueError(msg)
        if summary.argon_trajectory.coordination_number <= 0.0:
            msg = "argon trajectory coordination estimate must be positive"
            raise ValueError(msg)
        if summary.argon_trajectory.uncertainty_replica_count < 2:
            msg = "argon trajectory observable summary should record replicas"
            raise ValueError(msg)
        if summary.argon_trajectory.coordination_replica_standard_error <= 0.0:
            msg = "argon trajectory coordination replica uncertainty should be positive"
            raise ValueError(msg)
        if summary.argon_trajectory.max_rdf_replica_std <= 0.0:
            msg = "argon trajectory RDF replica uncertainty should be positive"
            raise ValueError(msg)
        if summary.argon_trajectory.vacf_integral_replica_standard_error <= 0.0:
            msg = "argon trajectory VACF integral replica uncertainty should be positive"
            raise ValueError(msg)
        if summary.argon_trajectory.max_vacf_replica_std <= 0.0:
            msg = "argon trajectory VACF replica uncertainty should be positive"
            raise ValueError(msg)
        if summary.argon_trajectory.vacf_lag1_autocorrelation <= 0.0:
            msg = "argon trajectory VACF lag-1 autocorrelation should be positive"
            raise ValueError(msg)
        if not summary.argon_trajectory.runtime_device:
            msg = "argon trajectory summary is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_trajectory.target_requests_gpu
            and not summary.argon_trajectory.production_gpu_ready
            and not summary.argon_trajectory.gpu_blocking_reason
        ):
            msg = "argon trajectory GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)


def _verify_post08(post: str, profile: str, output_root: Path) -> None:
    spec = load_free_energy_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "free_energy_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "free_energy_curves.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, curves_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_free_energy_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.bins) != len(spec.experiment.bin_widths):
        msg = "summary does not contain the expected histogram bin widths"
        raise ValueError(msg)
    if min(item.occupied_bins for item in summary.bins) <= 0:
        msg = "histogram PMF contains no occupied bins"
        raise ValueError(msg)
    if min(item.bootstrap_barrier_standard_error for item in summary.bins) <= 0.0:
        msg = "bootstrap uncertainty should be positive"
        raise ValueError(msg)
    if min(abs(item.barrier_error) for item in summary.bins) > 0.35:
        msg = "no histogram bin width recovers the known barrier within tolerance"
        raise ValueError(msg)
    if abs(summary.reweighted_barrier_error) > 0.45:
        msg = "reweighted PMF barrier is outside the review threshold"
        raise ValueError(msg)
    if summary.rdf_pmf_barrier_height <= 0.0:
        msg = "RDF-derived PMF should have a nonzero barrier height"
        raise ValueError(msg)
    if spec.argon_rdf_pmf is not None:
        if summary.argon_rdf_pmf is None:
            msg = "argon RDF-derived PMF summary is missing"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.atom_count <= 0:
            msg = "argon RDF-derived PMF should record atoms"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.frame_count <= spec.argon_rdf_pmf.max_vacf_lag:
            msg = "argon RDF-derived PMF should have enough sampled frames"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.rdf_first_peak_value <= 1.0:
            msg = "argon RDF first peak should exceed ideal-gas baseline"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.pmf_barrier_height <= 0.0:
            msg = "argon RDF-derived PMF should have a nonzero range"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.finite_pmf_bins <= 2:
            msg = "argon RDF-derived PMF should retain finite bins"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.uncertainty_block_count < 2:
            msg = "argon RDF-derived PMF should record block uncertainty"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.uncertainty_replica_count < 2:
            msg = "argon RDF-derived PMF should record replica uncertainty"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.max_block_pmf_sem <= 0.0:
            msg = "argon RDF-derived PMF block uncertainty should be positive"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.max_replica_pmf_std <= 0.0:
            msg = "argon RDF-derived PMF replica uncertainty should be positive"
            raise ValueError(msg)
        if len(summary.argon_rdf_pmf.support_thresholds) < 2:
            msg = "argon RDF-derived PMF should record support thresholds"
            raise ValueError(msg)
        if len(summary.argon_rdf_pmf.support_thresholds) != len(
            summary.argon_rdf_pmf.support_threshold_pmf_ranges
        ):
            msg = "argon RDF-derived PMF support threshold arrays are inconsistent"
            raise ValueError(msg)
        if summary.argon_rdf_pmf.support_threshold_range_span <= 0.0:
            msg = "argon RDF-derived PMF support sensitivity should be positive"
            raise ValueError(msg)
        if not summary.argon_rdf_pmf.runtime_device:
            msg = "argon RDF-derived PMF summary is missing runtime-device provenance"
            raise ValueError(msg)
        if (
            summary.argon_rdf_pmf.target_requests_gpu
            and not summary.argon_rdf_pmf.production_gpu_ready
            and not summary.argon_rdf_pmf.gpu_blocking_reason
        ):
            msg = "argon RDF-derived PMF GPU-targeted fallback must record a blocking reason"
            raise ValueError(msg)


def _verify_post09(post: str, profile: str, output_root: Path) -> None:
    spec = load_estimator_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "estimator_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "work_samples.csv"
    curves_path = output_dir / "multistate_curves.csv"
    windows_path = output_dir / "multistate_windows.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_estimator_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.cases) != len(spec.experiment.cases):
        msg = "summary does not contain the expected estimator cases"
        raise ValueError(msg)
    if min(case.overlap_coefficient for case in summary.cases) >= max(
        case.overlap_coefficient for case in summary.cases
    ):
        msg = "estimator cases should span distinct overlap regimes"
        raise ValueError(msg)
    if max(abs(case.bar_error) for case in summary.cases) > 0.35:
        msg = "BAR estimate is outside the review threshold"
        raise ValueError(msg)
    poor = min(summary.cases, key=lambda case: case.overlap_coefficient)
    good = max(summary.cases, key=lambda case: case.overlap_coefficient)
    if poor.forward_weight_ess_fraction >= good.forward_weight_ess_fraction:
        msg = "poor-overlap case should have lower forward ESS than good overlap"
        raise ValueError(msg)
    if abs(poor.forward_fep_error) <= abs(good.forward_fep_error):
        msg = "poor-overlap FEP should be less reliable than good-overlap FEP"
        raise ValueError(msg)
    if spec.multistate_overlap is not None:
        missing_multistate = [
            str(path) for path in (curves_path, windows_path) if not path.exists()
        ]
        if missing_multistate:
            msg = "missing expected multi-state estimator files: " + ", ".join(
                missing_multistate
            )
            raise FileNotFoundError(msg)
        if not summary.multistate_protocols:
            msg = "configured multi-state overlap summary is missing"
            raise ValueError(msg)
        dense = next(
            protocol
            for protocol in summary.multistate_protocols
            if protocol.protocol == "dense_bridge"
        )
        sparse = next(
            protocol
            for protocol in summary.multistate_protocols
            if protocol.protocol == "sparse_bridge"
        )
        if dense.min_adjacent_overlap <= sparse.min_adjacent_overlap:
            msg = "dense bridge should improve minimum adjacent overlap"
            raise ValueError(msg)
        if dense.disconnected_edges != 0:
            msg = "dense bridge should not have disconnected adjacent windows"
            raise ValueError(msg)
        if sparse.disconnected_edges == 0:
            msg = "sparse bridge should expose an overlap-network failure"
            raise ValueError(msg)
        if dense.pmf_rmse_vs_true >= sparse.pmf_rmse_vs_true:
            msg = "dense bridge should reconstruct the PMF more accurately"
            raise ValueError(msg)


def _verify_post10(post: str, profile: str, output_root: Path) -> None:
    spec = load_umbrella_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "umbrella_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "umbrella_curves.csv"
    windows_path = output_dir / "umbrella_windows.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, curves_path, windows_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_umbrella_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.protocols) != len(spec.experiment.protocols):
        msg = "summary does not contain the expected umbrella protocols"
        raise ValueError(msg)
    if min(protocol.window_count for protocol in summary.protocols) <= 1:
        msg = "umbrella protocols require multiple windows"
        raise ValueError(msg)
    if min(protocol.min_effective_bins for protocol in summary.protocols) <= 2:
        msg = "at least one umbrella window has too little sampled support"
        raise ValueError(msg)

    dense = next(
        protocol for protocol in summary.protocols if protocol.protocol == "dense_windows"
    )
    sparse = next(
        protocol for protocol in summary.protocols if protocol.protocol == "sparse_windows"
    )
    if dense.min_adjacent_overlap <= sparse.min_adjacent_overlap:
        msg = "dense windows should improve the minimum adjacent overlap"
        raise ValueError(msg)
    if dense.pmf_rmse_vs_true >= sparse.pmf_rmse_vs_true:
        msg = "dense windows should reconstruct the PMF more accurately"
        raise ValueError(msg)
    if abs(dense.barrier_error) > 0.20:
        msg = "dense-window barrier estimate is outside the review threshold"
        raise ValueError(msg)
    if dense.forward_reverse_pmf_rmse > 0.35:
        msg = "dense-window replica consistency is outside the review threshold"
        raise ValueError(msg)
    if dense.forward_reverse_pmf_rmse >= sparse.forward_reverse_pmf_rmse:
        msg = "dense windows should improve replica PMF consistency"
        raise ValueError(msg)


def _verify_post11(post: str, profile: str, output_root: Path) -> None:
    spec = load_enhanced_sampling_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "enhanced_sampling_summary.json"
    manifest_path = output_dir / "manifest.json"
    curves_path = output_dir / "enhanced_sampling_curves.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, curves_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_enhanced_sampling_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if summary.metadynamics.final_bias_range <= 0.5:
        msg = "metadynamics bias did not fill a meaningful free-energy range"
        raise ValueError(msg)
    if summary.metadynamics.barrier_visit_fraction <= 0.05:
        msg = "metadynamics run did not visit the barrier region often enough"
        raise ValueError(msg)
    if min(
        summary.metadynamics.basin_visit_fraction_left,
        summary.metadynamics.basin_visit_fraction_right,
    ) <= 0.15:
        msg = "metadynamics run did not sample both basins"
        raise ValueError(msg)
    if summary.pulling.forward_dissipated_work <= 0.0:
        msg = "forward pulling should show positive dissipated work"
        raise ValueError(msg)
    if summary.pulling.reverse_dissipated_work <= 0.0:
        msg = "reverse pulling should show positive dissipated work"
        raise ValueError(msg)
    if abs(summary.pulling.forward_jarzynski_delta_f - summary.pulling.true_delta_f) > 0.45:
        msg = "forward Jarzynski estimate is outside the review threshold"
        raise ValueError(msg)
    if abs(summary.pulling.reverse_jarzynski_delta_f - summary.pulling.true_delta_f) > 0.45:
        msg = "reverse Jarzynski estimate is outside the review threshold"
        raise ValueError(msg)
    if abs(summary.pulling.crooks_crossing_delta_f - summary.pulling.true_delta_f) > 0.50:
        msg = "Crooks crossing estimate is outside the review threshold"
        raise ValueError(msg)
    if (
        summary.steered_hysteresis.fast_hysteresis_gap
        <= summary.steered_hysteresis.slow_hysteresis_gap
    ):
        msg = "fast steered pulling should show a larger hysteresis gap"
        raise ValueError(msg)
    if summary.steered_hysteresis.hysteresis_gap_ratio <= 1.25:
        msg = "steered-pulling hysteresis ratio is too weak for review"
        raise ValueError(msg)


def _verify_post12(post: str, profile: str, output_root: Path) -> None:
    spec = load_mlip_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "mlip_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "mlip_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
    if missing:
        msg = "missing expected output files: " + ", ".join(missing)
        raise FileNotFoundError(msg)

    summary = load_mlip_summary(summary_path)
    if summary.post != post or summary.profile != profile:
        msg = "summary post/profile does not match requested verification target"
        raise ValueError(msg)
    if len(summary.cases) != len(spec.experiment.cases):
        msg = "summary does not contain the expected MLIP cases"
        raise ValueError(msg)
    if not summary.model_revision or not summary.model_sha256:
        msg = "MLIP artifact metadata is incomplete"
        raise ValueError(msg)

    in_domain = next(case for case in summary.cases if case.case == "in_domain_fcc")
    hot = next(case for case in summary.cases if case.case == "extrapolative_hot")
    if hot.force_rmse <= in_domain.force_rmse:
        msg = "extrapolative case should have larger force RMSE"
        raise ValueError(msg)
    if hot.extrapolation_fraction <= in_domain.extrapolation_fraction:
        msg = "extrapolative case should have larger extrapolation fraction"
        raise ValueError(msg)
    if hot.normalized_nve_energy_drift <= in_domain.normalized_nve_energy_drift:
        msg = "extrapolative case should have larger NVE drift"
        raise ValueError(msg)
    if hot.ensemble_temperature_drift_k <= in_domain.ensemble_temperature_drift_k:
        msg = "extrapolative case should have larger ensemble drift"
        raise ValueError(msg)
    if min(case.uncertainty_coverage_2sigma for case in summary.cases) < 0.85:
        msg = "uncertainty coverage is too low for the diagnostic"
        raise ValueError(msg)
    if max(case.static_energy_rmse_mev_per_atom for case in summary.cases) <= 0.0:
        msg = "static energy errors should be nonzero"
        raise ValueError(msg)
