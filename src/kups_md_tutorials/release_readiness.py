"""Final-release readiness audit for the tutorial series."""

from dataclasses import dataclass
from pathlib import Path
import json
import re

SUPPORTED_POSTS = tuple(f"{post:02d}" for post in range(1, 13))
MIN_POST_WORDS = 3500
MAX_POST_WORDS = 10000
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
        _check_site_blog_style(page_path, post, text, violations)
        if re.search(r"(?m)^nav:\s*false\s*$", text):
            violations.append(f"{page_path}: page remains hidden with nav: false")
        if "This page is not the final article" in text:
            violations.append(f"{page_path}: page still declares itself non-final")
        if "intentionally hidden from site navigation" in text:
            violations.append(f"{page_path}: page still has hidden-draft note")


def _check_site_blog_style(
    page_path: Path,
    post: str,
    text: str,
    violations: list[str],
) -> None:
    front_matter = _front_matter(text)
    if front_matter is None:
        violations.append(f"{page_path}: missing YAML front matter")
        return

    required_pairs = {
        "layout": "post",
        "post_type": "tutorial",
        "authors": '["Sungsoo Ahn"]',
        "series": "kups-md-tutorials",
        "series_title": '"kUPS Molecular Dynamics Tutorials"',
        "series_description": (
            '"Executable molecular-dynamics practice for MLIP-aware '
            'machine-learning researchers."'
        ),
        "series_order": str(int(post)),
        "related_posts": "false",
    }
    for key, expected in required_pairs.items():
        actual = _front_matter_value(front_matter, key)
        if actual != expected:
            violations.append(
                f"{page_path}: expected front matter {key}: {expected}, "
                f"found {actual or 'missing'}"
            )

    for key in ("title", "date", "last_updated", "description", "categories", "tags"):
        if _front_matter_value(front_matter, key) is None:
            violations.append(f"{page_path}: missing front matter {key}")

    if _front_matter_value(front_matter, "order") != str(int(post)):
        violations.append(
            f"{page_path}: expected front matter order: {int(post)}, "
            f"found {_front_matter_value(front_matter, 'order') or 'missing'}"
        )
    if f"post-{post}" not in (_front_matter_value(front_matter, "permalink") or ""):
        violations.append(f"{page_path}: permalink does not include post-{post}")
    if not re.search(r"(?m)^toc:\s*\n\s+sidebar:\s*left\s*$", front_matter):
        violations.append(f"{page_path}: missing toc sidebar: left front matter")

    body = text.split("---", 2)[2] if text.startswith("---") else text
    if '<p style="color: #666; font-size: 0.9em; margin-bottom: 1.5em;">' not in body:
        violations.append(f"{page_path}: missing muted author-note paragraph")
    if "<em>Note:" not in body:
        violations.append(f"{page_path}: missing author-note Note text")
    if "sungsoo-ahn/kups-md-tutorials" not in body:
        violations.append(f"{page_path}: missing source repository link text")
    _check_site_references(page_path, body, violations)
    _check_site_figures(page_path, body, violations)
    word_count = _body_word_count(body)
    if not MIN_POST_WORDS <= word_count <= MAX_POST_WORDS:
        violations.append(
            f"{page_path}: expected {MIN_POST_WORDS}-{MAX_POST_WORDS} body words, "
            f"found {word_count}"
        )


def _check_site_references(
    page_path: Path,
    body: str,
    violations: list[str],
) -> None:
    if not re.search(r"(?m)^## References\s*$", body):
        violations.append(f"{page_path}: missing References section")
        return

    cite_ids = set(re.findall(r'id=["\'](cite-[A-Za-z0-9_-]+)["\']', body))
    ref_ids = set(re.findall(r'id=["\'](ref-[A-Za-z0-9_-]+)["\']', body))
    if not cite_ids:
        violations.append(f"{page_path}: missing cite-* text citation anchors")
    if not ref_ids:
        violations.append(f"{page_path}: missing ref-* reference anchors")

    ref_keys = {ref_id.removeprefix("ref-") for ref_id in ref_ids}
    ref_targets = set(re.findall(r'(?:href=["\']#ref-|]\(#ref-)([A-Za-z0-9_-]+)', body))
    cite_backlinks = set(re.findall(r'href=["\']#(cite-[A-Za-z0-9_-]+)', body))

    cite_to_ref: dict[str, str | None] = {}
    for cite_id in sorted(cite_ids):
        cite_key = cite_id.removeprefix("cite-")
        ref_key = _matching_ref_key(cite_key, ref_keys)
        cite_to_ref[cite_id] = ref_key
        if ref_key is None:
            violations.append(f"{page_path}: {cite_id} has no matching ref-* anchor")
            continue
        if ref_key not in ref_targets:
            violations.append(f"{page_path}: {cite_id} does not link to #ref-{ref_key}")

    for ref_id in sorted(ref_ids):
        ref_key = ref_id.removeprefix("ref-")
        matching_cites = {
            cite_id
            for cite_id, matched_ref in cite_to_ref.items()
            if matched_ref == ref_key
        }
        if not matching_cites:
            violations.append(f"{page_path}: {ref_id} has no matching cite-* anchor")
            continue
        missing_backlinks = sorted(matching_cites - cite_backlinks)
        if missing_backlinks:
            violations.append(
                f"{page_path}: {ref_id} missing reverse backlink(s) to "
                + ", ".join(missing_backlinks)
            )


def _matching_ref_key(cite_key: str, ref_keys: set[str]) -> str | None:
    if cite_key in ref_keys:
        return cite_key
    if len(cite_key) > 1 and cite_key[-1].isalpha() and cite_key[:-1] in ref_keys:
        return cite_key[:-1]
    return None


def _check_site_figures(
    page_path: Path,
    body: str,
    violations: list[str],
) -> None:
    includes = re.findall(r"{%\s*include\s+figure\.liquid\s+(.+?)\s*%}", body)
    if not includes:
        violations.append(f"{page_path}: missing figure.liquid include")
        return

    site_root = page_path.parent.parent
    for index, include in enumerate(includes, start=1):
        attrs = _liquid_include_attrs(include)
        label = f"{page_path}: figure include {index}"
        figure_path = attrs.get("path")
        if figure_path is None:
            violations.append(f"{label} missing path")
        elif not figure_path.startswith("assets/img/blog/"):
            violations.append(f"{label} path is not under assets/img/blog/")
        elif not (site_root / figure_path).exists():
            violations.append(f"{label} path does not exist: {figure_path}")

        expected_class = "img-fluid rounded z-depth-1"
        if attrs.get("class") != expected_class:
            violations.append(
                f'{label} expected class="{expected_class}", '
                f"found {attrs.get('class') or 'missing'}"
            )
        if attrs.get("zoomable") != "true":
            violations.append(f"{label} expected zoomable=true")

        caption = attrs.get("caption")
        if caption is None:
            violations.append(f"{label} missing caption")
        else:
            if "$" in caption:
                violations.append(f"{label} caption uses dollar math delimiters")
            if _sentence_count(caption) < 2:
                violations.append(f"{label} caption should have at least two sentences")


def _liquid_include_attrs(include: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    pattern = re.compile(r'([A-Za-z_][A-Za-z0-9_-]*)=("([^"]*)"|(\S+))')
    for match in pattern.finditer(include):
        attrs[match.group(1)] = match.group(3) if match.group(3) is not None else match.group(4)
    return attrs


def _sentence_count(text: str) -> int:
    return len(re.findall(r"[.!?](?:\s|$)", text))


def _front_matter(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def _front_matter_value(front_matter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", front_matter)
    if match is None:
        return None
    return match.group(1).strip()


def _body_word_count(body: str) -> int:
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'/-]*", body))


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
