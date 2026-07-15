"""Final-release readiness audit for the tutorial series."""

from dataclasses import dataclass
from pathlib import Path
import json
import re

SUPPORTED_POSTS = tuple(f"{post:02d}" for post in range(1, 13))
PLACEHOLDER_MARKERS = (
    "pending-gpu-artifact-hash",
    "pinned-placeholder",
    "placeholder",
)


@dataclass(frozen=True)
class ReleaseReadinessResult:
    """Result from auditing final-release blockers."""

    checked_posts: int
    violations: tuple[str, ...]


def audit_release_readiness(
    *,
    review_dir: Path = Path("reviews"),
    config_root: Path = Path("configs"),
    results_root: Path = Path("results"),
    notebook_root: Path = Path("notebooks"),
    figure_root: Path = Path("figures"),
    snapshot_root: Path = Path("snapshots"),
    site_root: Path | None = None,
) -> ReleaseReadinessResult:
    """Check whether the series is ready for public final release."""

    violations: list[str] = []
    _check_review_blockers(review_dir, violations)
    _check_required_artifact_surface(
        config_root=config_root,
        results_root=results_root,
        notebook_root=notebook_root,
        figure_root=figure_root,
        snapshot_root=snapshot_root,
        violations=violations,
    )
    _check_post12_model_artifact(config_root, results_root, violations)
    if site_root is not None:
        _check_site_publication_state(site_root, violations)
    return ReleaseReadinessResult(
        checked_posts=len(SUPPORTED_POSTS),
        violations=tuple(violations),
    )


def verify_release_readiness(
    *,
    review_dir: Path = Path("reviews"),
    config_root: Path = Path("configs"),
    results_root: Path = Path("results"),
    notebook_root: Path = Path("notebooks"),
    figure_root: Path = Path("figures"),
    snapshot_root: Path = Path("snapshots"),
    site_root: Path | None = None,
) -> ReleaseReadinessResult:
    """Raise ``ValueError`` if final-release blockers remain."""

    result = audit_release_readiness(
        review_dir=review_dir,
        config_root=config_root,
        results_root=results_root,
        notebook_root=notebook_root,
        figure_root=figure_root,
        snapshot_root=snapshot_root,
        site_root=site_root,
    )
    if result.violations:
        msg = "release readiness audit failed:\n" + "\n".join(result.violations)
        raise ValueError(msg)
    return result


def _check_review_blockers(review_dir: Path, violations: list[str]) -> None:
    for post in SUPPORTED_POSTS:
        review_path = review_dir / f"post-{post}.md"
        if not review_path.exists():
            violations.append(f"{review_path}: missing review file")
            continue
        text = review_path.read_text(encoding="utf-8")
        section = _final_release_blocker_section(text)
        if section is None:
            section = _last_open_items_section(text)
            if section is None:
                violations.append(
                    f"{review_path}: missing Final-release blockers section"
                )
                continue
        blockers = _bullet_items(section)
        if blockers and not _blockers_are_none(blockers):
            violations.append(
                f"{review_path}: unresolved final-release blockers: "
                + "; ".join(blockers)
            )


def _check_required_artifact_surface(
    *,
    config_root: Path,
    results_root: Path,
    notebook_root: Path,
    figure_root: Path,
    snapshot_root: Path,
    violations: list[str],
) -> None:
    for post in SUPPORTED_POSTS:
        for profile in ("smoke", "full"):
            _check_json_file(
                config_root / f"post-{post}" / f"{profile}.json",
                violations,
                missing_reason=f"missing {profile} configuration",
            )
            result_dir = results_root / f"post-{post}" / profile
            _check_json_file(
                result_dir / "manifest.json",
                violations,
                missing_reason=f"missing {profile} result manifest",
            )
            summary_paths = sorted(result_dir.glob("*_summary.json"))
            if not summary_paths:
                violations.append(f"{result_dir}: missing {profile} compact summary")
            for summary_path in summary_paths:
                _check_json_file(
                    summary_path,
                    violations,
                    missing_reason=f"missing {profile} compact summary",
                )

        notebook_matches = sorted(notebook_root.glob(f"post-{post}-*.ipynb"))
        if len(notebook_matches) != 1:
            violations.append(
                f"{notebook_root}: expected one notebook for post {post}, "
                f"found {len(notebook_matches)}"
            )
        else:
            _check_json_file(
                notebook_matches[0],
                violations,
                missing_reason=f"missing notebook for post {post}",
            )

        figure_dir = figure_root / f"post-{post}"
        for pattern, description in (
            ("*_diagnostics.svg", "publication SVG figure"),
            ("*_diagnostics.png", "publication PNG figure"),
            ("*_diagnostics_full.svg", "full-profile SVG figure"),
            ("*_diagnostics_full.png", "full-profile PNG figure"),
        ):
            _check_glob_matches(
                figure_dir,
                pattern,
                violations,
                missing_reason=f"missing {description}",
            )

        snapshot_dir = snapshot_root / f"post-{post}"
        for pattern, description in (
            ("*_diagnostics_snapshot.png", "figure snapshot"),
            ("*_diagnostics_full_snapshot.png", "full-profile figure snapshot"),
        ):
            _check_glob_matches(
                snapshot_dir,
                pattern,
                violations,
                missing_reason=f"missing {description}",
            )


def _check_post12_model_artifact(
    config_root: Path,
    results_root: Path,
    violations: list[str],
) -> None:
    paths = (
        config_root / "post-12" / "full.json",
        config_root / "post-12" / "smoke.json",
        results_root / "post-12" / "full" / "mlip_summary.json",
        results_root / "post-12" / "full" / "manifest.json",
    )
    for path in paths:
        if not path.exists():
            violations.append(f"{path}: missing post-12 model artifact metadata")
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for marker in PLACEHOLDER_MARKERS:
            if marker in lowered:
                violations.append(f"{path}: contains placeholder model artifact marker")
                break
        if path.suffix == ".json":
            _check_json_text(path, text, violations)


def _check_site_publication_state(site_root: Path, violations: list[str]) -> None:
    pages_dir = site_root / "_pages"
    for post in SUPPORTED_POSTS:
        matches = sorted(pages_dir.glob(f"kups-md-post-{post}-*.md"))
        if not matches:
            violations.append(f"{pages_dir}: missing website page for post {post}")
            continue
        page_path = matches[0]
        text = page_path.read_text(encoding="utf-8")
        if re.search(r"(?m)^nav:\s*false\s*$", text):
            violations.append(f"{page_path}: page remains hidden with nav: false")
        if "This page is not the final article" in text:
            violations.append(f"{page_path}: page still declares itself non-final")
        if "intentionally hidden from site navigation" in text:
            violations.append(f"{page_path}: page still has hidden-draft note")


def _check_json_file(
    path: Path,
    violations: list[str],
    *,
    missing_reason: str,
) -> None:
    if not path.exists():
        violations.append(f"{path}: {missing_reason}")
        return
    text = path.read_text(encoding="utf-8")
    _check_json_text(path, text, violations)


def _check_json_text(path: Path, text: str, violations: list[str]) -> None:
    try:
        json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON: {exc}")


def _check_glob_matches(
    directory: Path,
    pattern: str,
    violations: list[str],
    *,
    missing_reason: str,
) -> None:
    if not directory.exists():
        violations.append(f"{directory}: {missing_reason}")
        return
    matches = sorted(directory.glob(pattern))
    if not matches:
        violations.append(f"{directory}: {missing_reason}")


def _section_after_heading(text: str, heading: str) -> str | None:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$", flags=re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return None
    next_heading = re.search(r"^##\s+", text[match.end() :], flags=re.MULTILINE)
    if next_heading is None:
        return text[match.end() :]
    return text[match.end() : match.end() + next_heading.start()]


def _final_release_blocker_section(text: str) -> str | None:
    section = _section_after_heading(text, "Final-release blockers")
    if section is not None:
        return section
    label = re.search(r"^Final-release blockers:\s*$", text, flags=re.MULTILINE)
    if label is None:
        return None
    rest = text[label.end() :]
    next_boundary = re.search(
        r"^(?:##\s+|Blocking items|Non-blocking items|Final-release blockers:)",
        rest,
        flags=re.MULTILINE,
    )
    if next_boundary is None:
        return rest
    return rest[: next_boundary.start()]


def _last_open_items_section(text: str) -> str | None:
    labels = tuple(re.finditer(r"^Open items:\s*$", text, flags=re.MULTILINE))
    if not labels:
        return None
    label = labels[-1]
    rest = text[label.end() :]
    next_heading = re.search(r"^##\s+", rest, flags=re.MULTILINE)
    if next_heading is None:
        return rest
    return rest[: next_heading.start()]


def _bullet_items(section: str) -> tuple[str, ...]:
    items: list[str] = []
    current: list[str] = []
    for line in section.splitlines():
        if line.startswith("- "):
            if current:
                items.append(" ".join(current).strip())
            current = [line[2:].strip()]
        elif current and line.startswith("  "):
            current.append(line.strip())
        elif current and line.strip():
            current.append(line.strip())
    if current:
        items.append(" ".join(current).strip())
    return tuple(items)


def _blockers_are_none(blockers: tuple[str, ...]) -> bool:
    return all(
        item.strip().lower().rstrip(".") in {"none", "none remaining"}
        for item in blockers
    )
