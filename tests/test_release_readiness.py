import json
from pathlib import Path

import pytest

from kups_md_tutorials.cli import main
from kups_md_tutorials.release_readiness import (
    audit_release_readiness,
    verify_release_readiness,
)


def _write_clean_reviews(review_dir: Path) -> None:
    review_dir.mkdir(parents=True)
    for post in range(1, 13):
        (review_dir / f"post-{post:02d}.md").write_text(
            "# Review\n\n## Open Items\n\n"
            "Blocking items for the current hidden draft:\n\n"
            "- None.\n\n"
            "## Final-release blockers\n\n"
            "- None.\n",
            encoding="utf-8",
        )


def _write_required_artifacts(root: Path, *, placeholder: bool = False) -> None:
    for post in range(1, 13):
        post_id = f"{post:02d}"
        config_dir = root / "configs" / f"post-{post_id}"
        notebook_dir = root / "notebooks"
        figure_dir = root / "figures" / f"post-{post_id}"
        snapshot_dir = root / "snapshots" / f"post-{post_id}"
        config_dir.mkdir(parents=True)
        notebook_dir.mkdir(parents=True, exist_ok=True)
        figure_dir.mkdir(parents=True)
        snapshot_dir.mkdir(parents=True)

        for profile in ("smoke", "full"):
            (config_dir / f"{profile}.json").write_text(
                json.dumps({"post": post_id, "profile": profile}) + "\n",
                encoding="utf-8",
            )
            result_dir = root / "results" / f"post-{post_id}" / profile
            result_dir.mkdir(parents=True)
            (result_dir / "manifest.json").write_text(
                json.dumps({"post": post_id, "profile": profile}) + "\n",
                encoding="utf-8",
            )
            (result_dir / "example_summary.json").write_text(
                json.dumps({"post": post_id, "profile": profile}) + "\n",
                encoding="utf-8",
            )

        (notebook_dir / f"post-{post_id}-example.ipynb").write_text(
            json.dumps(
                {
                    "cells": [],
                    "metadata": {},
                    "nbformat": 4,
                    "nbformat_minor": 5,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        for suffix in (
            "diagnostics.svg",
            "diagnostics.png",
            "diagnostics_full.svg",
            "diagnostics_full.png",
        ):
            (figure_dir / f"example_{suffix}").write_text("asset\n", encoding="utf-8")
        for suffix in (
            "diagnostics_snapshot.png",
            "diagnostics_full_snapshot.png",
        ):
            (snapshot_dir / f"example_{suffix}").write_text(
                "snapshot\n", encoding="utf-8"
            )

    _write_post12_model_metadata(root, placeholder=placeholder)


def _write_post12_model_metadata(root: Path, *, placeholder: bool) -> None:
    config_dir = root / "configs" / "post-12"
    results_dir = root / "results" / "post-12" / "full"
    revision = "pinned-placeholder" if placeholder else "mace-v0.3.10"
    sha = "pending-gpu-artifact-hash" if placeholder else "a" * 64
    config = (
        '{"mlip_experiment": {"model_artifact": {'
        f'"revision": "{revision}", "sha256": "{sha}"'
        "}}}\n"
    )
    summary = (
        "{"
        f'"model_revision": "{revision}", "model_sha256": "{sha}"'
        "}\n"
    )
    manifest = (
        '{"config": {"experiment": {"model_artifact": {'
        f'"revision": "{revision}", "sha256": "{sha}"'
        "}}}}\n"
    )
    (config_dir / "full.json").write_text(config, encoding="utf-8")
    (config_dir / "smoke.json").write_text(config, encoding="utf-8")
    (results_dir / "mlip_summary.json").write_text(summary, encoding="utf-8")
    (results_dir / "manifest.json").write_text(manifest, encoding="utf-8")


def _write_site_pages(site_root: Path, *, hidden: bool) -> None:
    pages = site_root / "_pages"
    pages.mkdir(parents=True)
    for post in range(1, 13):
        frontmatter = "nav: false\n" if hidden else "nav: true\n"
        note = (
            "This page is not the final article. "
            "It is intentionally hidden from site navigation.\n"
            if hidden
            else "Final article.\n"
        )
        (pages / f"kups-md-post-{post:02d}-example.md").write_text(
            f"---\n{frontmatter}---\n\n{note}",
            encoding="utf-8",
        )


def test_release_readiness_passes_clean_final_state(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)

    result = verify_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert result.checked_posts == 12
    assert result.violations == ()


def test_release_readiness_reports_current_project_blockers() -> None:
    result = audit_release_readiness(
        review_dir=Path("reviews"),
        config_root=Path("configs"),
        results_root=Path("results"),
        notebook_root=Path("notebooks"),
        figure_root=Path("figures"),
        snapshot_root=Path("snapshots"),
        site_root=None,
    )

    assert result.violations
    assert any("post-12" in violation for violation in result.violations)
    assert any("real MACE/fcc-Al GPU capstone" in violation for violation in result.violations)
    assert not any(
        "placeholder model artifact" in violation for violation in result.violations
    )


def test_release_readiness_reports_hidden_site_pages(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=True)

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("nav: false" in violation for violation in result.violations)
    assert any("non-final" in violation for violation in result.violations)
    with pytest.raises(ValueError, match="release readiness audit failed"):
        verify_release_readiness(
            review_dir=tmp_path / "reviews",
            config_root=tmp_path / "configs",
            results_root=tmp_path / "results",
            notebook_root=tmp_path / "notebooks",
            figure_root=tmp_path / "figures",
            snapshot_root=tmp_path / "snapshots",
            site_root=tmp_path / "site",
        )


def test_release_readiness_reports_placeholder_model_metadata(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path, placeholder=True)
    _write_site_pages(tmp_path / "site", hidden=False)

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any(
        "placeholder model artifact" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_missing_required_artifacts(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    (tmp_path / "notebooks" / "post-06-example.ipynb").unlink()
    (tmp_path / "snapshots" / "post-08" / "example_diagnostics_snapshot.png").unlink()

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any(
        "expected one notebook for post 06" in violation
        for violation in result.violations
    )
    assert any(
        "post-08" in violation and "figure snapshot" in violation
        for violation in result.violations
    )


def test_verify_release_readiness_cli_passes_clean_final_state(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)

    assert (
        main(
            [
                "verify-release-readiness",
                "--review-dir",
                str(tmp_path / "reviews"),
                "--config-root",
                str(tmp_path / "configs"),
                "--results-root",
                str(tmp_path / "results"),
                "--notebook-root",
                str(tmp_path / "notebooks"),
                "--figure-root",
                str(tmp_path / "figures"),
                "--snapshot-root",
                str(tmp_path / "snapshots"),
                "--site-root",
                str(tmp_path / "site"),
            ]
        )
        == 0
    )
