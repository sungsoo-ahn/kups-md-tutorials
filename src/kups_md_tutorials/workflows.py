"""Executable tutorial workflows exposed by the CLI."""

from pathlib import Path

from kups_md_tutorials.config import load_tutorial_spec
from kups_md_tutorials.initialization import (
    load_initialization_summary,
    write_initialization_outputs,
)

SUPPORTED_POSTS = ("01",)
SUPPORTED_PROFILES = ("smoke", "full")


def run_post(post: str, profile: str, output_root: Path = Path("results")) -> Path:
    """Run one supported tutorial workflow."""

    if post != "01":
        msg = f"post {post!r} is not implemented yet"
        raise NotImplementedError(msg)
    spec = load_tutorial_spec(post, profile)
    return write_initialization_outputs(spec, output_root=output_root)


def run_all(profile: str, output_root: Path = Path("results")) -> list[Path]:
    """Run every currently implemented tutorial workflow."""

    return [run_post(post, profile, output_root=output_root) for post in SUPPORTED_POSTS]


def verify_post(post: str, profile: str, output_root: Path = Path("results")) -> None:
    """Verify compact outputs for one tutorial workflow."""

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


def verify_all(profile: str, output_root: Path = Path("results")) -> None:
    """Verify every currently implemented tutorial workflow."""

    for post in SUPPORTED_POSTS:
        verify_post(post, profile, output_root=output_root)
