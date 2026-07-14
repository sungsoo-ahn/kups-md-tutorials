"""Executable tutorial workflows exposed by the CLI."""

from pathlib import Path

from kups_md_tutorials.config import (
    load_error_spec,
    load_integrator_spec,
    load_tutorial_spec,
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

SUPPORTED_POSTS = ("01", "02", "03")
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
