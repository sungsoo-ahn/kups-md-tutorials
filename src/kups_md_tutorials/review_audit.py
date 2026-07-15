"""Audit self-review notes required by the project plan."""

from dataclasses import dataclass
from pathlib import Path
import re

SUPPORTED_POSTS = tuple(f"{post:02d}" for post in range(1, 13))
REQUIRED_SECTION_ALIASES = {
    "scope": ("## Scope", "## Scope And Provenance", "## Scope and Provenance"),
    "commands": ("## Commands",),
    "code": ("## Code And Reproducibility Review",),
    "science": ("## Scientific Review",),
    "figure": ("## Figure Snapshot Review", "## Figure Feedback Review"),
    "notebook": ("## Notebook Review",),
    "website": ("## Website Draft Review", "## Website Page Review"),
    "prose_style": ("## Prose And Style Review", "## Prose and Style Review"),
    "open_items": ("## Open Items",),
}


@dataclass(frozen=True)
class ReviewAuditResult:
    """Result from auditing post-level self-review notes."""

    reviewed_posts: int
    violations: tuple[str, ...]


def audit_reviews(review_dir: Path = Path("reviews")) -> ReviewAuditResult:
    """Check review files for the self-review evidence required by PLAN.md."""

    violations: list[str] = []
    for post in SUPPORTED_POSTS:
        review_path = review_dir / f"post-{post}.md"
        if not review_path.exists():
            violations.append(f"{review_path}: missing review file")
            continue
        text = review_path.read_text(encoding="utf-8")
        _check_sections(review_path, text, violations)
        _check_required_references(post, review_path, text, violations)
        _check_open_item_language(review_path, text, violations)
        _check_hidden_draft_open_item_split(review_path, text, violations)
    return ReviewAuditResult(
        reviewed_posts=len(SUPPORTED_POSTS),
        violations=tuple(violations),
    )


def verify_reviews(review_dir: Path = Path("reviews")) -> ReviewAuditResult:
    """Raise ``ValueError`` if any self-review note is incomplete."""

    result = audit_reviews(review_dir)
    if result.violations:
        msg = "review audit failed:\n" + "\n".join(result.violations)
        raise ValueError(msg)
    return result


def _check_sections(path: Path, text: str, violations: list[str]) -> None:
    for name, aliases in REQUIRED_SECTION_ALIASES.items():
        if not any(alias in text for alias in aliases):
            violations.append(f"{path}: missing {name} review section")


def _check_required_references(
    post: str,
    path: Path,
    text: str,
    violations: list[str],
) -> None:
    required_fragments = (
        f"configs/post-{post}/",
        f"results/post-{post}/",
        f"notebooks/post-{post}",
        f"snapshots/post-{post}/",
        "https://sungsoo-ahn.github.io/kups-md-tutorials/",
        "validate_blog.py",
    )
    for fragment in required_fragments:
        if fragment not in text:
            violations.append(f"{path}: missing reference to {fragment}")

    snapshot_refs = re.findall(r"`(snapshots/post-[^`]+_snapshot\.png)`", text)
    if len(snapshot_refs) < 2:
        violations.append(f"{path}: expected at least two figure snapshot references")
    for snapshot in snapshot_refs:
        if not Path(snapshot).exists():
            violations.append(f"{path}: referenced snapshot does not exist: {snapshot}")


def _check_open_item_language(path: Path, text: str, violations: list[str]) -> None:
    lowered = text.lower()
    if "open items" not in lowered:
        violations.append(f"{path}: missing open items language")
    if "rendered" not in lowered or "snapshot" not in lowered:
        violations.append(f"{path}: missing rendered page snapshot status")


def _check_hidden_draft_open_item_split(
    path: Path,
    text: str,
    violations: list[str],
) -> None:
    lowered = text.lower()
    required_phrases = {
        "blocking items for current hidden draft": (
            "blocking items for current hidden draft",
            "blocking items for the current hidden draft",
        ),
        "non-blocking items accepted until final article pass": (
            "non-blocking items accepted until final article pass",
            "non-blocking items accepted until the final article pass",
        ),
        "final-release blockers": (
            "final-release blockers",
            "final-release blockers after this refresh",
        ),
    }
    for label, aliases in required_phrases.items():
        if not any(alias in lowered for alias in aliases):
            violations.append(f"{path}: missing {label} language")
