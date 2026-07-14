"""Executable tutorial workflows exposed by the CLI."""

from pathlib import Path

from kups_md_tutorials.config import load_integrator_spec, load_tutorial_spec
from kups_md_tutorials.initialization import (
    load_initialization_summary,
    write_initialization_outputs,
)
from kups_md_tutorials.integrators import (
    load_integrator_summary,
    write_integrator_outputs,
)

SUPPORTED_POSTS = ("01", "02")
SUPPORTED_PROFILES = ("smoke", "full")


def run_post(post: str, profile: str, output_root: Path = Path("results")) -> Path:
    """Run one supported tutorial workflow."""

    if post == "01":
        spec = load_tutorial_spec(post, profile)
        return write_initialization_outputs(spec, output_root=output_root)
    if post == "02":
        spec = load_integrator_spec(post, profile)
        return write_integrator_outputs(spec, output_root=output_root)
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
