"""Small provenance helpers for reproducible tutorial outputs."""

from dataclasses import dataclass
from pathlib import Path
import hashlib
import os
import platform
import subprocess


@dataclass(frozen=True)
class Provenance:
    """Version and source-control metadata for one generated artifact."""

    config_path: str
    config_sha256: str
    lock_path: str | None
    lock_sha256: str | None
    git_revision: str
    python_version: str
    platform: str
    runtime_device: str
    precision_policy: str


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


def runtime_device() -> str:
    """Return a compact description of the numerical runtime device."""

    try:
        import jax
    except Exception:
        return "unknown"
    try:
        backend = jax.default_backend()
        devices = ",".join(device.platform for device in jax.devices())
    except Exception:
        return "unknown"
    return f"jax:{backend};devices:{devices}"


def target_requests_gpu(target_device: str) -> bool:
    """Return whether a configured target device requests GPU execution."""

    target = target_device.lower()
    return "cuda" in target or "gpu" in target


def runtime_is_gpu(runtime: str) -> bool:
    """Return whether a compact runtime-device string indicates GPU execution."""

    lowered = runtime.lower()
    return "jax:gpu" in lowered or "devices:gpu" in lowered or "cuda" in lowered


def gpu_blocking_reason(target_device: str, runtime: str) -> str | None:
    """Return a blocking reason when a GPU-targeted artifact ran on non-GPU."""

    if target_requests_gpu(target_device) and not runtime_is_gpu(runtime):
        return (
            "target device requests CUDA/GPU, but generated artifact runtime "
            f"was {runtime}"
        )
    return None


def precision_policy() -> str:
    """Return the active global precision policy relevant to JAX/kUPS runs."""

    try:
        import jax
    except Exception:
        jax_enable_x64 = "unknown"
    else:
        try:
            jax_enable_x64 = str(bool(jax.config.jax_enable_x64)).lower()
        except Exception:
            jax_enable_x64 = "unknown"
    env_value = os.environ.get("JAX_ENABLE_X64")
    if env_value is None:
        return f"jax_enable_x64={jax_enable_x64};env_JAX_ENABLE_X64=unset"
    return f"jax_enable_x64={jax_enable_x64};env_JAX_ENABLE_X64={env_value}"


def provenance(config_path: Path) -> Provenance:
    """Collect provenance metadata for an output generated from a config file."""

    repo_root = config_path.parents[2]
    lock_path = repo_root / "uv.lock"
    lock_sha256 = file_sha256(lock_path) if lock_path.exists() else None
    return Provenance(
        config_path=str(config_path),
        config_sha256=file_sha256(config_path),
        lock_path=str(lock_path.relative_to(repo_root)) if lock_path.exists() else None,
        lock_sha256=lock_sha256,
        git_revision=git_revision(repo_root),
        python_version=platform.python_version(),
        platform=platform.platform(),
        runtime_device=runtime_device(),
        precision_policy=precision_policy(),
    )
