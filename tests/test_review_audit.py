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
    with pytest.raises(ValueError, match="review audit failed"):
        verify_reviews(review_dir)


def test_verify_reviews_cli() -> None:
    assert main(["verify-reviews"]) == 0
