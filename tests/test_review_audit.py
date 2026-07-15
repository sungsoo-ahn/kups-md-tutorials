from pathlib import Path

import pytest

from kups_md_tutorials.cli import main
from kups_md_tutorials.review_audit import audit_reviews, verify_reviews


def test_review_audit_passes_current_reviews() -> None:
    result = verify_reviews()

    assert result.reviewed_posts == 12
    assert result.violations == ()


def test_review_audit_reports_missing_evidence(tmp_path: Path) -> None:
    review_dir = tmp_path / "reviews"
    review_dir.mkdir()
    for post in range(1, 13):
        (review_dir / f"post-{post:02d}.md").write_text(
            "# Review\n\n## Scope\n\nincomplete\n",
            encoding="utf-8",
        )

    result = audit_reviews(review_dir)

    assert result.violations
    assert any("missing commands" in violation for violation in result.violations)
    assert any("missing prose_style" in violation for violation in result.violations)
    assert any("missing open_items" in violation for violation in result.violations)
    with pytest.raises(ValueError, match="review audit failed"):
        verify_reviews(review_dir)


def test_review_audit_requires_hidden_draft_open_item_split(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    review_dir = tmp_path / "reviews"
    review_dir.mkdir()
    for post in range(1, 13):
        (review_dir / f"post-{post:02d}.md").write_text(
            "\n".join(
                [
                    "# Review",
                    "",
                    "## Scope",
                    "",
                    f"- configs/post-{post:02d}/",
                    f"- results/post-{post:02d}/",
                    f"- notebooks/post-{post:02d}",
                    f"- snapshots/post-{post:02d}/figure_snapshot.png",
                    "- https://sungsoo-ahn.github.io/kups-md-tutorials/",
                    "- validate_blog.py",
                    "",
                    "## Commands",
                    "",
                    "- rendered page snapshot command passed.",
                    "",
                    "## Code And Reproducibility Review",
                    "",
                    "- checked.",
                    "",
                    "## Scientific Review",
                    "",
                    "- checked.",
                    "",
                    "## Figure Snapshot Review",
                    "",
                    f"- `snapshots/post-{post:02d}/figure_snapshot.png`",
                    f"- `snapshots/post-{post:02d}/figure_full_snapshot.png`",
                    "",
                    "## Notebook Review",
                    "",
                    "- checked.",
                    "",
                    "## Website Draft Review",
                    "",
                    "- rendered desktop/mobile snapshots checked.",
                    "",
                    "## Prose And Style Review",
                    "",
                    "- checked.",
                    "",
                    "## Open Items",
                    "",
                    "- Generic open items only.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        snapshot_dir = Path(f"snapshots/post-{post:02d}")
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        (snapshot_dir / "figure_snapshot.png").touch()
        (snapshot_dir / "figure_full_snapshot.png").touch()

    result = audit_reviews(review_dir)

    assert any(
        "missing blocking items for current hidden draft language" in violation
        for violation in result.violations
    )
    assert any(
        "missing non-blocking items accepted until final article pass language"
        in violation
        for violation in result.violations
    )
    assert any(
        "missing final-release blockers language" in violation
        for violation in result.violations
    )


def test_review_audit_requires_rendered_page_snapshot_references(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    review_dir = tmp_path / "reviews"
    review_dir.mkdir()
    for post in range(1, 13):
        desktop_ref = (
            f"- `/tmp/kups-snapshots/post-{post:02d}-desktop.png`"
            if post != 4
            else ""
        )
        mobile_ref = (
            f"- `/tmp/kups-snapshots/post-{post:02d}-mobile.png`"
            if post != 5
            else ""
        )
        (review_dir / f"post-{post:02d}.md").write_text(
            "\n".join(
                [
                    "# Review",
                    "",
                    "## Scope",
                    "",
                    f"- configs/post-{post:02d}/",
                    f"- results/post-{post:02d}/",
                    f"- notebooks/post-{post:02d}",
                    f"- snapshots/post-{post:02d}/figure_snapshot.png",
                    "- https://sungsoo-ahn.github.io/kups-md-tutorials/",
                    "- validate_blog.py",
                    "",
                    "## Commands",
                    "",
                    "- rendered page snapshot command passed.",
                    "",
                    "## Code And Reproducibility Review",
                    "",
                    "- checked.",
                    "",
                    "## Scientific Review",
                    "",
                    "- checked.",
                    "",
                    "## Figure Snapshot Review",
                    "",
                    f"- `snapshots/post-{post:02d}/figure_snapshot.png`",
                    f"- `snapshots/post-{post:02d}/figure_full_snapshot.png`",
                    "",
                    "## Notebook Review",
                    "",
                    "- checked.",
                    "",
                    "## Website Draft Review",
                    "",
                    "- rendered desktop/mobile snapshots checked.",
                    desktop_ref,
                    mobile_ref,
                    "",
                    "## Prose And Style Review",
                    "",
                    "- checked.",
                    "",
                    "## Open Items",
                    "",
                    "- Blocking items for the current hidden draft: none.",
                    "- Non-blocking items accepted until the final article pass: hidden.",
                    "- Final-release blockers: public indexing.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        snapshot_dir = Path(f"snapshots/post-{post:02d}")
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        (snapshot_dir / "figure_snapshot.png").touch()
        (snapshot_dir / "figure_full_snapshot.png").touch()

    result = audit_reviews(review_dir)

    assert any(
        "post-04.md: missing desktop rendered page snapshot" in violation
        for violation in result.violations
    )
    assert any(
        "post-05.md: missing mobile rendered page snapshot" in violation
        for violation in result.violations
    )


def test_verify_reviews_cli() -> None:
    assert main(["verify-reviews"]) == 0
