"""Small provenance helpers for reproducible tutorial outputs."""

from dataclasses import dataclass
from pathlib import Path
import hashlib
import platform
import subprocess


@dataclass(frozen=True)
class Provenance:
    """Version and source-control metadata for one generated artifact."""

    config_path: str
    config_sha256: str
    git_revision: str
    python_version: str
    platform: str


def file_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_revision(cwd: Path = Path(".")) -> str:
    """Return the current git revision, or ``unknown`` outside git."""

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def provenance(config_path: Path) -> Provenance:
    """Collect provenance metadata for an output generated from a config file."""

    return Provenance(
        config_path=str(config_path),
        config_sha256=file_sha256(config_path),
        git_revision=git_revision(config_path.parents[2]),
        python_version=platform.python_version(),
        platform=platform.platform(),
    )
