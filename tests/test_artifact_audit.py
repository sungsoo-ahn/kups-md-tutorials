from pathlib import Path
import subprocess

import pytest

from kups_md_tutorials.artifact_audit import (
    MAX_TRACKED_FILE_BYTES,
    audit_tracked_artifacts,
    verify_tracked_artifacts,
)
from kups_md_tutorials.cli import main


def test_artifact_audit_allows_compact_results_and_figures() -> None:
    result = verify_tracked_artifacts(
        paths=(
            Path("results/post-01/full/manifest.json"),
            Path("results/post-02/full/trajectory_samples.csv"),
            Path("figures/post-01/initialization_diagnostics.svg"),
            Path("snapshots/post-01/initialization_diagnostics_snapshot.png"),
            Path("notebooks/post-01-initialization.ipynb"),
        )
    )

    assert result.tracked_file_count == 5
    assert result.violations == ()


def test_artifact_audit_rejects_raw_or_cached_artifacts() -> None:
    paths = (
        Path("runs/post-01/raw.h5"),
        Path("models/mace.pt"),
        Path(".venv/lib/example.py"),
        Path("src/pkg/__pycache__/module.pyc"),
        Path("hello.py"),
    )
    result = audit_tracked_artifacts(paths=paths)

    assert result.violations == (
        "runs/post-01/raw.h5",
        "models/mace.pt",
        ".venv/lib/example.py",
        "src/pkg/__pycache__/module.pyc",
        "hello.py",
    )
    with pytest.raises(ValueError, match="forbidden tracked artifacts"):
        verify_tracked_artifacts(paths=paths)


def test_artifact_audit_rejects_oversized_tracked_file(tmp_path: Path) -> None:
    path = tmp_path / "results" / "post-01" / "full" / "large_summary.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"x" * (MAX_TRACKED_FILE_BYTES + 1))

    result = audit_tracked_artifacts(repo_root=tmp_path, paths=(path.relative_to(tmp_path),))

    assert len(result.violations) == 1
    assert "large_summary.json" in result.violations[0]
    assert "exceeds" in result.violations[0]


def test_artifact_audit_allows_compact_file_under_size_limit(tmp_path: Path) -> None:
    path = tmp_path / "results" / "post-01" / "full" / "small_summary.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"x" * 1024)

    result = verify_tracked_artifacts(
        repo_root=tmp_path,
        paths=(path.relative_to(tmp_path),),
    )

    assert result.violations == ()


def test_verify_artifacts_cli_passes_clean_git_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / "README.md").write_text("ok\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    monkeypatch.chdir(tmp_path)

    assert main(["verify-artifacts"]) == 0
