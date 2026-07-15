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


def _write_model_metadata(root: Path, *, placeholder: bool) -> None:
    config_dir = root / "configs" / "post-12"
    results_dir = root / "results" / "post-12" / "full"
    config_dir.mkdir(parents=True)
    results_dir.mkdir(parents=True)
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
    _write_model_metadata(tmp_path, placeholder=False)
    _write_site_pages(tmp_path / "site", hidden=False)

    result = verify_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        site_root=tmp_path / "site",
    )

    assert result.checked_posts == 12
    assert result.violations == ()


def test_release_readiness_reports_current_project_blockers() -> None:
    result = audit_release_readiness(
        review_dir=Path("reviews"),
        config_root=Path("configs"),
        results_root=Path("results"),
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
    _write_model_metadata(tmp_path, placeholder=False)
    _write_site_pages(tmp_path / "site", hidden=True)

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        site_root=tmp_path / "site",
    )

    assert any("nav: false" in violation for violation in result.violations)
    assert any("non-final" in violation for violation in result.violations)
    with pytest.raises(ValueError, match="release readiness audit failed"):
        verify_release_readiness(
            review_dir=tmp_path / "reviews",
            config_root=tmp_path / "configs",
            results_root=tmp_path / "results",
            site_root=tmp_path / "site",
        )


def test_verify_release_readiness_cli_passes_clean_final_state(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_model_metadata(tmp_path, placeholder=False)
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
                "--site-root",
                str(tmp_path / "site"),
            ]
        )
        == 0
    )
