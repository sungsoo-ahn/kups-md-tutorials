"""Executable tutorial workflows exposed by the CLI."""

from pathlib import Path

from kups_md_tutorials.config import (
    load_barostat_spec,
    load_error_spec,
    load_integrator_spec,
    load_observable_spec,
    load_trajectory_length_spec,
    load_thermostat_spec,
    load_tutorial_spec,
)
from kups_md_tutorials.barostats import (
    load_barostat_summary,
    write_barostat_outputs,
)
from kups_md_tutorials.error_diagnostics import (
    load_error_summary,
    write_error_outputs,
)
from kups_md_tutorials.initialization import (
    load_initialization_summary,
    write_initialization_outputs,
)
from kups_md_tutorials.integrators import (
    load_integrator_summary,
    write_integrator_outputs,
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

SUPPORTED_POSTS = ("01", "02", "03", "04", "05", "06", "07")
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
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
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


def _verify_post04(post: str, profile: str, output_root: Path) -> None:
    spec = load_thermostat_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "thermostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "thermostat_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
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


def _verify_post05(post: str, profile: str, output_root: Path) -> None:
    spec = load_barostat_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "barostat_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "barostat_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
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


def _verify_post06(post: str, profile: str, output_root: Path) -> None:
    spec = load_trajectory_length_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "trajectory_length_summary.json"
    manifest_path = output_dir / "manifest.json"
    samples_path = output_dir / "trajectory_length_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, samples_path)
        if not path.exists()
    ]
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


def _verify_post07(post: str, profile: str, output_root: Path) -> None:
    spec = load_observable_spec(post, profile)
    output_dir = output_root / spec.result_dir_name
    summary_path = output_dir / "observable_summary.json"
    manifest_path = output_dir / "manifest.json"
    rdf_path = output_dir / "rdf_samples.csv"
    vacf_path = output_dir / "vacf_samples.csv"
    missing = [
        str(path)
        for path in (summary_path, manifest_path, rdf_path, vacf_path)
        if not path.exists()
    ]
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
