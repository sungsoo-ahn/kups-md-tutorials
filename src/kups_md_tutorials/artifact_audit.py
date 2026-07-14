"""Repository hygiene checks for tracked tutorial artifacts."""

from dataclasses import dataclass
from pathlib import Path
import subprocess

FORBIDDEN_PATH_PARTS = {
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "models",
    "notebook-runs",
    "runs",
}
FORBIDDEN_SUFFIXES = {
    ".ckpt",
    ".h5",
    ".model",
    ".npy",
    ".npz",
    ".pkl",
    ".pickle",
    ".pt",
    ".pth",
    ".traj",
}
FORBIDDEN_FILENAMES = {"hello.py"}


@dataclass(frozen=True)
class ArtifactAuditResult:
    """Result from auditing files tracked by git."""

    tracked_file_count: int
    violations: tuple[str, ...]


def tracked_files(repo_root: Path = Path(".")) -> tuple[Path, ...]:
    """Return files tracked by git relative to ``repo_root``."""

    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(Path(line) for line in result.stdout.splitlines() if line)


def audit_tracked_artifacts(
    repo_root: Path = Path("."),
    paths: tuple[Path, ...] | None = None,
) -> ArtifactAuditResult:
    """Check tracked files against the repository artifact policy."""

    files = tracked_files(repo_root) if paths is None else paths
    violations = tuple(
        str(path)
        for path in files
        if _is_forbidden(path)
    )
    return ArtifactAuditResult(
        tracked_file_count=len(files),
        violations=violations,
    )


def verify_tracked_artifacts(
    repo_root: Path = Path("."),
    paths: tuple[Path, ...] | None = None,
) -> ArtifactAuditResult:
    """Raise ``ValueError`` if forbidden artifacts are tracked."""

    result = audit_tracked_artifacts(repo_root=repo_root, paths=paths)
    if result.violations:
        msg = "forbidden tracked artifacts: " + ", ".join(result.violations)
        raise ValueError(msg)
    return result


def _is_forbidden(path: Path) -> bool:
    parts = set(path.parts)
    if parts & FORBIDDEN_PATH_PARTS:
        return True
    if path.suffix in FORBIDDEN_SUFFIXES:
        return True
    return path.name in FORBIDDEN_FILENAMES
