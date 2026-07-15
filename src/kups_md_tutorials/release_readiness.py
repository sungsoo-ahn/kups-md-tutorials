"""Final-release readiness audit for the tutorial series."""

from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
import tomllib

from kups_md_tutorials.provenance import file_sha256

SUPPORTED_POSTS = tuple(f"{post:02d}" for post in range(1, 13))
MIN_POST_WORDS = 3500
MAX_POST_WORDS = 10000
ALLOWED_MANIFEST_OUTPUT_SUFFIXES = (".csv", ".extxyz", ".json")
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


CURRENT_FINAL_BLOCKER_MARKERS = (
    "unresolved final-release blockers",
    "missing final _posts blog post",
    "series index still queries hidden pages instead of final posts",
    "page remains hidden with nav: false",
    "page still declares itself non-final",
    "page still has hidden-draft note",
)

CONFIG_LOADERS = {
    "01": "load_tutorial_spec",
    "02": "load_integrator_spec",
    "03": "load_error_spec",
    "04": "load_thermostat_spec",
    "05": "load_barostat_spec",
    "06": "load_trajectory_length_spec",
    "07": "load_observable_spec",
    "08": "load_free_energy_spec",
    "09": "load_estimator_spec",
    "10": "load_umbrella_spec",
    "11": "load_enhanced_sampling_spec",
    "12": "load_mlip_spec",
}


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
    _check_figure_source_provenance(
        review_dir / "figure-sources.json",
        figure_root=figure_root,
        results_root=results_root,
        violations=violations,
    )
    _check_notebook_execution_ledger(
        review_dir / "notebook-execution.json",
        notebook_root=notebook_root,
        violations=violations,
    )
    _check_page_snapshot_ledger(
        review_dir / "page-snapshots.md",
        violations,
        site_root=site_root,
    )
    _check_website_build_ledger(
        review_dir / "website-build.json",
        site_root=site_root,
        violations=violations,
    )
    _check_ci_workflow(
        review_dir.parent / ".github" / "workflows" / "verify.yml",
        violations,
    )
    _check_gitignore_policy(review_dir.parent / ".gitignore", violations)
    _check_pyproject_contract(review_dir.parent / "pyproject.toml", violations)
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
        _check_site_snapshot_capture(site_root, violations)
        _check_site_publication_state(
            site_root,
            source_root=review_dir.parent,
            violations=violations,
        )
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


def verify_release_surface(
    *,
    review_dir: Path = Path("reviews"),
    config_root: Path = Path("configs"),
    results_root: Path = Path("results"),
    notebook_root: Path = Path("notebooks"),
    figure_root: Path = Path("figures"),
    snapshot_root: Path = Path("snapshots"),
    site_root: Path | None = None,
) -> ReleaseReadinessResult:
    """Raise if release readiness has unexpected structural violations.

    This keeps CI strict about artifact, provenance, notebook, and website
    contract regressions while allowing the known hidden-draft and production
    GPU blockers to remain until final publication.
    """

    result = audit_release_readiness(
        review_dir=review_dir,
        config_root=config_root,
        results_root=results_root,
        notebook_root=notebook_root,
        figure_root=figure_root,
        snapshot_root=snapshot_root,
        site_root=site_root,
    )
    unexpected = tuple(
        violation
        for violation in result.violations
        if not is_current_final_blocker(violation)
    )
    if unexpected:
        msg = "release surface audit failed:\n" + "\n".join(unexpected)
        raise ValueError(msg)
    return result


def is_current_final_blocker(violation: str) -> bool:
    """Return whether a violation is an accepted hidden/final-release blocker."""

    return any(marker in violation for marker in CURRENT_FINAL_BLOCKER_MARKERS)


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
            _check_config_seed_coverage(
                config_root / f"post-{post}" / f"{profile}.json",
                violations,
            )
            _check_typed_config_file(
                config_root=config_root,
                post=post,
                profile=profile,
                violations=violations,
            )
            result_dir = results_root / f"post-{post}" / profile
            _check_result_manifest_file(
                result_dir / "manifest.json",
                violations,
                config_root=config_root,
                post=post,
                profile=profile,
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


def _check_typed_config_file(
    *,
    config_root: Path,
    post: str,
    profile: str,
    violations: list[str],
) -> None:
    config_path = config_root / f"post-{post}" / f"{profile}.json"
    if not config_path.exists():
        return

    loader_name = CONFIG_LOADERS[post]
    try:
        from kups_md_tutorials import config as config_module

        loader = getattr(config_module, loader_name)
        spec = loader(post, profile, config_root=config_root)
    except Exception as exc:
        violations.append(f"{config_path}: typed config validation failed: {exc}")
        return

    if getattr(spec, "post", None) != post:
        violations.append(
            f"{config_path}: typed config loader returned post "
            f"{getattr(spec, 'post', None)!r}"
        )
    if getattr(spec, "profile", None) != profile:
        violations.append(
            f"{config_path}: typed config loader returned profile "
            f"{getattr(spec, 'profile', None)!r}"
        )


def _check_config_seed_coverage(path: Path, violations: list[str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    try:
        config = json.loads(text)
    except json.JSONDecodeError:
        return
    if not _json_contains_key(config, "seed"):
        violations.append(f"{path}: missing explicit fixed seed")


def _json_contains_key(value: object, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(
            _json_contains_key(child, key) for child in value.values()
        )
    if isinstance(value, list):
        return any(_json_contains_key(child, key) for child in value)
    return False


def _check_figure_source_provenance(
    path: Path,
    *,
    figure_root: Path,
    results_root: Path,
    violations: list[str],
) -> None:
    if not path.exists():
        violations.append(f"{path}: missing figure source provenance ledger")
        return
    text = path.read_text(encoding="utf-8")
    try:
        ledger = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(ledger, dict):
        violations.append(f"{path}: figure source provenance ledger must be a JSON object")
        return

    repo_root = path.parent.parent
    covered_files: set[str] = set()
    for post in SUPPORTED_POSTS:
        entries = ledger.get(f"post-{post}")
        if not isinstance(entries, list) or not entries:
            violations.append(f"{path}: missing figure source entries for post {post}")
            continue
        post_covered_files: set[str] = set()
        for index, entry in enumerate(entries, start=1):
            label = f"{path}: post-{post} entry {index}"
            if not isinstance(entry, dict):
                violations.append(f"{label} must be a JSON object")
                continue
            figure_files = entry.get("figure_files")
            if not isinstance(figure_files, list) or not figure_files:
                violations.append(f"{label} missing figure_files")
            else:
                for figure_file in figure_files:
                    if not isinstance(figure_file, str) or not figure_file:
                        violations.append(f"{label} contains invalid figure file path")
                        continue
                    covered_files.add(figure_file)
                    post_covered_files.add(figure_file)
                    if not figure_file.startswith(f"figures/post-{post}/"):
                        violations.append(
                            f"{label} figure file is not under figures/post-{post}/: "
                            f"{figure_file}"
                        )
                    if not _ledger_path_exists(repo_root, figure_file):
                        violations.append(f"{label} figure file does not exist: {figure_file}")

            for field in (
                "source_url",
                "source_type",
                "license",
                "modifications",
                "generator",
            ):
                value = entry.get(field)
                if not isinstance(value, str) or not value.strip():
                    violations.append(f"{label} missing {field}")

            generator = entry.get("generator")
            if isinstance(generator, str) and generator.strip():
                _check_ledger_relative_file(
                    label,
                    repo_root=repo_root,
                    field="generator",
                    path_text=generator,
                    violations=violations,
                )
                source_url = entry.get("source_url")
                expected_source_url = f"internal:{generator}"
                if source_url != expected_source_url:
                    violations.append(
                        f"{label} expected source_url {expected_source_url}, "
                        f"found {source_url!r}"
                    )

            source_data = entry.get("source_data")
            if not isinstance(source_data, list) or not source_data:
                violations.append(f"{label} missing source_data")
            else:
                source_data_paths: set[str] = set()
                for source_path in source_data:
                    if not isinstance(source_path, str) or not source_path:
                        violations.append(f"{label} contains invalid source data path")
                        continue
                    source_data_paths.add(source_path)
                    if not _ledger_path_exists(repo_root, source_path):
                        violations.append(f"{label} source data does not exist: {source_path}")
                _check_figure_source_data_coverage(
                    label,
                    post=post,
                    source_data_paths=source_data_paths,
                    violations=violations,
                )
        _check_post_figure_source_coverage(
            path,
            post=post,
            figure_root=figure_root,
            repo_root=repo_root,
            covered_files=post_covered_files,
            violations=violations,
        )

    for figure_path in sorted(figure_root.glob("post-*/*.svg")) + sorted(
        figure_root.glob("post-*/*.png")
    ):
        rel_path = _relative_to_root_or_posix(figure_path, repo_root)
        if rel_path not in covered_files:
            violations.append(f"{path}: missing source provenance for {rel_path}")


def _check_post_figure_source_coverage(
    path: Path,
    *,
    post: str,
    figure_root: Path,
    repo_root: Path,
    covered_files: set[str],
    violations: list[str],
) -> None:
    figure_dir = figure_root / f"post-{post}"
    for pattern, description in (
        ("*_diagnostics.svg", "publication SVG figure"),
        ("*_diagnostics.png", "publication PNG figure"),
        ("*_diagnostics_full.svg", "full-profile SVG figure"),
        ("*_diagnostics_full.png", "full-profile PNG figure"),
    ):
        matches = sorted(figure_dir.glob(pattern))
        if not matches:
            continue
        for figure_path in matches:
            rel_path = _relative_to_root_or_posix(figure_path, repo_root)
            if rel_path not in covered_files:
                violations.append(
                    f"{path}: missing {description} source provenance "
                    f"for post {post}: {rel_path}"
                )


def _check_figure_source_data_coverage(
    label: str,
    *,
    post: str,
    source_data_paths: set[str],
    violations: list[str],
) -> None:
    for profile in ("smoke", "full"):
        config_path = f"configs/post-{post}/{profile}.json"
        if config_path not in source_data_paths:
            violations.append(f"{label} missing source data {config_path}")
        result_prefix = f"results/post-{post}/{profile}/"
        if not any(
            source_path.startswith(result_prefix)
            and source_path.endswith("_summary.json")
            for source_path in source_data_paths
        ):
            violations.append(
                f"{label} missing {profile} compact summary source data"
            )


def _check_ledger_relative_file(
    label: str,
    *,
    repo_root: Path,
    field: str,
    path_text: str,
    violations: list[str],
) -> None:
    ledger_path = Path(path_text)
    if ledger_path.is_absolute():
        violations.append(f"{label} {field} should be repository-relative: {path_text}")
        return
    resolved_path = repo_root / ledger_path
    if not _path_is_within(resolved_path, repo_root):
        violations.append(f"{label} {field} escapes repository root: {path_text}")
        return
    if not resolved_path.exists():
        violations.append(f"{label} {field} does not exist: {path_text}")


def _check_notebook_execution_ledger(
    path: Path,
    *,
    notebook_root: Path,
    violations: list[str],
) -> None:
    if not path.exists():
        violations.append(f"{path}: missing notebook execution ledger")
        return
    text = path.read_text(encoding="utf-8")
    try:
        ledger = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(ledger, dict):
        violations.append(f"{path}: notebook execution ledger must be a JSON object")
        return

    source_revision = ledger.get("source_git_revision")
    if not isinstance(source_revision, str) or len(source_revision) < 7:
        violations.append(f"{path}: missing source_git_revision")
    elif source_revision == "unknown":
        violations.append(f"{path}: source_git_revision is unknown")
    else:
        repo_root = path.parent.parent
        actual_revision = _git_head_sha(repo_root)
        if (
            actual_revision is not None
            and not _git_revision_is_ancestor(repo_root, source_revision, actual_revision)
        ):
            violations.append(
                f"{path}: source_git_revision {source_revision} "
                f"is not an ancestor of repository HEAD {actual_revision}"
            )

    if ledger.get("execution_mode") != "fresh_kernel_per_notebook":
        violations.append(
            f"{path}: expected execution_mode fresh_kernel_per_notebook, "
            f"found {ledger.get('execution_mode')!r}"
        )
    if ledger.get("kernel_name") != "python3":
        violations.append(
            f"{path}: expected kernel_name python3, found {ledger.get('kernel_name')!r}"
        )
    timeout = ledger.get("timeout_seconds")
    if not isinstance(timeout, int) or timeout <= 0:
        violations.append(f"{path}: missing positive timeout_seconds")

    entries = ledger.get("notebooks")
    if not isinstance(entries, list) or not entries:
        violations.append(f"{path}: missing notebook execution entries")
        return

    seen_posts: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        label = f"{path}: notebook entry {index}"
        if not isinstance(entry, dict):
            violations.append(f"{label} must be a JSON object")
            continue
        post = entry.get("post")
        if post not in SUPPORTED_POSTS:
            violations.append(f"{label} has unsupported post {post!r}")
            continue
        seen_posts.add(post)
        source = entry.get("source")
        if not isinstance(source, str) or not source:
            violations.append(f"{label} missing source")
            continue
        executed_copy = entry.get("executed_copy")
        if not isinstance(executed_copy, str) or not executed_copy:
            violations.append(f"{label} missing executed_copy")
        expected_source = _single_notebook_for_post(notebook_root, post)
        if expected_source is None:
            violations.append(f"{label} cannot find current notebook for post {post}")
            continue
        source_path = Path(source)
        if source_path.is_absolute():
            violations.append(f"{label} source should be repository-relative: {source}")
        elif source_path != expected_source:
            violations.append(
                f"{label} expected source {expected_source.as_posix()}, found {source}"
            )
        source_file = notebook_root.parent / source_path
        if not source_file.exists():
            violations.append(f"{label} source does not exist: {source}")
            continue
        expected_sha = entry.get("source_sha256")
        actual_sha = file_sha256(source_file)
        if expected_sha != actual_sha:
            violations.append(
                f"{label} source_sha256 mismatch for {source}: "
                f"expected {expected_sha!r}, found {actual_sha}"
            )
        after_sha = entry.get("source_sha256_after")
        if after_sha != actual_sha:
            violations.append(
                f"{label} source_sha256_after mismatch for {source}: "
                f"expected {after_sha!r}, found {actual_sha}"
            )
        if entry.get("source_unchanged") is not True:
            violations.append(f"{label} source_unchanged must be true")

        code_cells = entry.get("code_cells")
        executed_code_cells = entry.get("executed_code_cells")
        output_count = entry.get("output_count")
        elapsed_seconds = entry.get("elapsed_seconds")
        actual_code_cells = _notebook_code_cell_count(source_file, violations)
        if not isinstance(code_cells, int) or code_cells <= 0:
            violations.append(f"{label} missing positive code_cells")
        elif actual_code_cells is not None and code_cells != actual_code_cells:
            violations.append(
                f"{label} expected code_cells {actual_code_cells}, found {code_cells}"
            )
        if executed_code_cells != code_cells:
            violations.append(
                f"{label} executed_code_cells {executed_code_cells!r} "
                f"does not match code_cells {code_cells!r}"
            )
        if not isinstance(output_count, int) or output_count <= 0:
            violations.append(f"{label} missing positive output_count")
        if not isinstance(elapsed_seconds, int | float) or elapsed_seconds <= 0:
            violations.append(f"{label} missing positive elapsed_seconds")

    missing_posts = sorted(set(SUPPORTED_POSTS) - seen_posts)
    if missing_posts:
        violations.append(
            f"{path}: missing notebook execution entries for posts "
            + ", ".join(missing_posts)
        )


def _check_page_snapshot_ledger(
    path: Path,
    violations: list[str],
    *,
    site_root: Path | None = None,
) -> None:
    if not path.exists():
        violations.append(f"{path}: missing rendered page snapshot ledger")
        return

    text = path.read_text(encoding="utf-8")
    required_fragments = (
        "Website workflow",
        "kups-md-page-snapshots",
        "Manifest reviewed",
        "Manifest coverage",
        "Snapshots visually inspected",
        "Feedback",
        "Revision decisions",
    )
    for fragment in required_fragments:
        if fragment not in text:
            violations.append(f"{path}: missing rendered page snapshot {fragment}")

    required_pages = ("index", *SUPPORTED_POSTS)
    for page in required_pages:
        label = "post-index" if page == "index" else f"post-{page}"
        for viewport in ("desktop", "mobile"):
            snapshot_name = f"{label}-{viewport}.png"
            if snapshot_name not in text:
                violations.append(
                    f"{path}: missing rendered page snapshot reference "
                    f"for {label} {viewport}"
                )

    if site_root is not None:
        _check_page_snapshot_site_freshness(
            path,
            text,
            site_root=site_root,
            violations=violations,
        )


def _check_page_snapshot_site_freshness(
    path: Path,
    text: str,
    *,
    site_root: Path,
    violations: list[str],
) -> None:
    actual_head = _git_head_sha(site_root)
    if actual_head is None:
        return

    snapshot_commits = _snapshot_website_commits(text)
    if not snapshot_commits:
        violations.append(f"{path}: missing rendered page snapshot website commit")
        return

    latest_snapshot_commit = None
    for commit in snapshot_commits:
        if _git_revision_is_ancestor(site_root, commit, actual_head):
            latest_snapshot_commit = commit
    if latest_snapshot_commit is None:
        violations.append(
            f"{path}: no rendered page snapshot website commit is an ancestor "
            f"of site root HEAD {actual_head}"
        )
        return

    changed_paths = _git_changed_files(site_root, latest_snapshot_commit, actual_head)
    if changed_paths is None:
        return
    stale_paths = sorted(path for path in changed_paths if _kups_snapshot_sensitive_path(path))
    if stale_paths:
        shown_paths = ", ".join(stale_paths[:8])
        if len(stale_paths) > 8:
            shown_paths += f", ... ({len(stale_paths)} total)"
        violations.append(
            f"{path}: rendered page snapshots predate kUPS-sensitive website "
            f"changes since {latest_snapshot_commit}: {shown_paths}"
        )


def _snapshot_website_commits(text: str) -> list[str]:
    commits: list[str] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "Website commit" not in line:
            continue
        nearby_text = "\n".join(lines[index : index + 6])
        commits.extend(re.findall(r"`([0-9a-f]{7,40})`", nearby_text))
    return commits


def _kups_snapshot_sensitive_path(path_text: str) -> bool:
    path = Path(path_text)
    parts = path.parts
    if len(parts) >= 2 and parts[0] == "_pages":
        return parts[1] == "kups-md-tutorials.md" or parts[1].startswith(
            "kups-md-post-"
        )
    if len(parts) >= 2 and parts[0] == "_posts" and "kups-md-post-" in parts[1]:
        return True
    if len(parts) >= 4 and parts[:3] == ("assets", "img", "blog"):
        return parts[3].startswith("kups_md_post")
    if len(parts) >= 4 and parts[:3] == ("assets", "json", "kups-md-tutorials"):
        return False
    sensitive_files = {
        "_layouts/default.liquid",
        "_layouts/page.liquid",
        "_layouts/post.liquid",
        "_includes/figure.liquid",
        "_includes/head.liquid",
        "_includes/header.liquid",
        "_includes/scripts.liquid",
        "_sass/_base.scss",
        "assets/css/main.scss",
        "scripts/capture_kups_snapshots.js",
    }
    return path_text in sensitive_files


def _check_website_build_ledger(
    path: Path,
    *,
    site_root: Path | None,
    violations: list[str],
) -> None:
    if not path.exists():
        violations.append(f"{path}: missing website build/deploy ledger")
        return

    text = path.read_text(encoding="utf-8")
    try:
        ledger = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(ledger, dict):
        violations.append(f"{path}: website build/deploy ledger must be a JSON object")
        return

    expected_pairs = {
        "repository": "sungsoo-ahn/sungsoo-ahn.github.io",
        "workflow": "Deploy site",
        "status": "completed",
        "conclusion": "success",
    }
    for field, expected in expected_pairs.items():
        actual = ledger.get(field)
        if actual != expected:
            violations.append(
                f"{path}: expected {field} {expected!r}, found {actual!r}"
            )

    run_id = ledger.get("run_id")
    if not isinstance(run_id, int) or run_id <= 0:
        violations.append(f"{path}: missing positive run_id")
    run_url = ledger.get("run_url")
    if not isinstance(run_url, str) or "/actions/runs/" not in run_url:
        violations.append(f"{path}: missing GitHub Actions run_url")
    head_sha = ledger.get("head_sha")
    if not isinstance(head_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", head_sha):
        violations.append(f"{path}: missing 40-character head_sha")
        head_sha = None

    required_steps = (
        "Validate blog posts",
        "Validate hidden kUPS pages",
        "Build site",
        "Deploy to GitHub Pages",
    )
    steps = ledger.get("validated_steps")
    if not isinstance(steps, list):
        violations.append(f"{path}: missing validated_steps")
    else:
        for step in required_steps:
            if step not in steps:
                violations.append(f"{path}: missing validated step {step}")

    required_commands = (
        "python3 scripts/validate_blog.py",
        "python3 scripts/validate_kups_pages.py",
        "bundle exec jekyll build",
    )
    commands = ledger.get("validated_commands")
    if not isinstance(commands, list):
        violations.append(f"{path}: missing validated_commands")
    else:
        for command in required_commands:
            if command not in commands:
                violations.append(f"{path}: missing validated command {command}")

    if site_root is None:
        return

    actual_head = _git_head_sha(site_root)
    if head_sha is not None and actual_head is not None and actual_head != head_sha:
        violations.append(
            f"{path}: head_sha {head_sha} does not match site root HEAD {actual_head}"
        )

    workflow_path = site_root / ".github" / "workflows" / "deploy.yml"
    if not workflow_path.exists():
        violations.append(f"{workflow_path}: missing website deploy workflow")
        return
    workflow_text = workflow_path.read_text(encoding="utf-8")
    for command in required_commands:
        if command not in workflow_text:
            violations.append(
                f"{workflow_path}: missing release validation command {command}"
            )


def _check_site_snapshot_capture(site_root: Path, violations: list[str]) -> None:
    workflow_path = site_root / ".github" / "workflows" / "kups-snapshots.yml"
    script_path = site_root / "scripts" / "capture_kups_snapshots.js"
    if not workflow_path.exists():
        violations.append(f"{workflow_path}: missing kUPS page snapshot workflow")
    else:
        workflow_text = workflow_path.read_text(encoding="utf-8")
        required_workflow_fragments = {
            "workflow_dispatch:": "manual dispatch trigger",
            "base_url": "base URL input",
            "posts": "post selection input",
            "npx playwright install chromium": "Chromium installation",
            "node scripts/capture_kups_snapshots.js": "snapshot capture command",
            "--output-dir snapshots/kups-md-pages": "snapshot output directory",
            "name: kups-md-page-snapshots": "snapshot artifact name",
            "path: snapshots/kups-md-pages": "snapshot artifact path",
        }
        for fragment, description in required_workflow_fragments.items():
            if fragment not in workflow_text:
                violations.append(
                    f"{workflow_path}: missing kUPS snapshot {description}: {fragment}"
                )

    if not script_path.exists():
        violations.append(f"{script_path}: missing kUPS page snapshot script")
        return

    script_text = script_path.read_text(encoding="utf-8")
    required_script_fragments = {
        '["desktop", { width: 1440, height: 1200 }]': "desktop viewport",
        '["mobile", { width: 390, height: 1200, isMobile: true }]': (
            "mobile viewport"
        ),
        "page.goto(url": "page navigation",
        "waitUntil: \"networkidle\"": "network-idle wait",
        "response.status() >= 400": "HTTP failure check",
        "page.screenshot": "page screenshot capture",
        "fullPage: true": "full-page capture",
        "manifest.json": "snapshot manifest output",
        "/kups-md-tutorials/": "series index URL",
    }
    for post in SUPPORTED_POSTS:
        required_script_fragments[f"post-{post}-"] = f"post {post} URL slug"
    for fragment, description in required_script_fragments.items():
        if fragment not in script_text:
            violations.append(
                f"{script_path}: missing kUPS snapshot {description}: {fragment}"
            )


def _check_ci_workflow(path: Path, violations: list[str]) -> None:
    if not path.exists():
        violations.append(f"{path}: missing tutorial verification workflow")
        return

    text = path.read_text(encoding="utf-8")
    required_fragments = {
        "uv sync --locked": "locked dependency installation",
        "uv run ruff check .": "ruff check",
        "uv run pytest -q": "pytest",
        "uv run kups-tutorial run-all --profile smoke": "smoke reproduction",
        "uv run kups-tutorial verify --profile smoke": "smoke verification",
        "uv run kups-tutorial verify --profile full": "committed full verification",
        "uv run kups-tutorial verify-artifacts": "tracked artifact audit",
        "uv run kups-tutorial verify-reviews": "review audit",
        (
            "uv run kups-tutorial verify-release-readiness --skip-site "
            "--allow-current-blockers"
        ): "release-surface audit",
        "uv run kups-tutorial verify-notebooks": "clean notebook execution",
        "git diff --check": "whitespace audit",
    }
    for fragment, description in required_fragments.items():
        if fragment not in text:
            violations.append(f"{path}: missing CI {description}: {fragment}")

    required_order = (
        (
            "uv run kups-tutorial run-all --profile smoke",
            "uv run kups-tutorial verify --profile smoke",
            "smoke reproduction",
            "smoke verification",
        ),
        (
            "uv run kups-tutorial verify --profile smoke",
            "uv run kups-tutorial verify --profile full",
            "smoke verification",
            "committed full verification",
        ),
        (
            "uv run kups-tutorial verify-reviews",
            "uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers",
            "review audit",
            "release-surface audit",
        ),
        (
            "uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers",
            "uv run kups-tutorial verify-notebooks",
            "release-surface audit",
            "clean notebook execution",
        ),
    )
    for before, after, before_label, after_label in required_order:
        before_index = text.find(before)
        after_index = text.find(after)
        if before_index != -1 and after_index != -1 and before_index > after_index:
            violations.append(
                f"{path}: CI {before_label} must run before {after_label}"
            )

    required_order = (
        ("uv sync --locked", "locked dependency installation"),
        ("uv run ruff check .", "ruff check"),
        ("uv run pytest -q", "pytest"),
        ("uv run kups-tutorial run-all --profile smoke", "smoke reproduction"),
        ("uv run kups-tutorial verify --profile smoke", "smoke verification"),
        ("uv run kups-tutorial verify --profile full", "committed full verification"),
        ("uv run kups-tutorial verify-artifacts", "tracked artifact audit"),
        ("uv run kups-tutorial verify-reviews", "review audit"),
        (
            "uv run kups-tutorial verify-release-readiness --skip-site "
            "--allow-current-blockers",
            "release-surface audit",
        ),
        ("uv run kups-tutorial verify-notebooks", "clean notebook execution"),
        ("git diff --check", "whitespace audit"),
    )
    previous_index = -1
    previous_description = ""
    for fragment, description in required_order:
        index = text.find(fragment)
        if index == -1:
            continue
        if index < previous_index:
            violations.append(
                f"{path}: CI {description} runs before {previous_description}"
            )
        else:
            previous_index = index
            previous_description = description


def _check_gitignore_policy(path: Path, violations: list[str]) -> None:
    if not path.exists():
        violations.append(f"{path}: missing repository artifact ignore policy")
        return

    patterns = {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    required_patterns = {
        "__pycache__/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".venv",
        "runs/",
        "notebook-runs/",
        ".ipynb_checkpoints/",
        "models/",
        "*.ckpt",
        "*.h5",
        "*.hdf5",
        "*.model",
        "*.npy",
        "*.npz",
        "*.pkl",
        "*.pickle",
        "*.pt",
        "*.pth",
        "*.traj",
    }
    for pattern in sorted(required_patterns - patterns):
        violations.append(f"{path}: missing artifact ignore pattern {pattern}")


def _check_pyproject_contract(path: Path, violations: list[str]) -> None:
    if not path.exists():
        violations.append(f"{path}: missing Python packaging contract")
        return

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        violations.append(f"{path}: invalid TOML: {exc}")
        return

    project = data.get("project")
    if not isinstance(project, dict):
        violations.append(f"{path}: missing [project] table")
        return

    if project.get("requires-python") != ">=3.13,<3.14":
        violations.append(
            f"{path}: expected requires-python >=3.13,<3.14, "
            f"found {project.get('requires-python')!r}"
        )

    dependencies = _string_set(project.get("dependencies"))
    if "kups==1.0.3" not in dependencies:
        violations.append(f"{path}: missing pinned dependency kups==1.0.3")

    optional = project.get("optional-dependencies")
    if not isinstance(optional, dict):
        violations.append(f"{path}: missing [project.optional-dependencies]")
    else:
        if "kups[cuda]==1.0.3" not in _string_set(optional.get("gpu")):
            violations.append(f"{path}: missing gpu extra kups[cuda]==1.0.3")
        if "kups[hf]==1.0.3" not in _string_set(optional.get("mlff")):
            violations.append(f"{path}: missing mlff extra kups[hf]==1.0.3")

    scripts = project.get("scripts")
    if not isinstance(scripts, dict):
        violations.append(f"{path}: missing [project.scripts]")
    elif scripts.get("kups-tutorial") != "kups_md_tutorials.cli:main":
        violations.append(
            f"{path}: expected kups-tutorial script to point to "
            "kups_md_tutorials.cli:main"
        )

    tool = data.get("tool")
    ruff = tool.get("ruff") if isinstance(tool, dict) else None
    if not isinstance(ruff, dict) or ruff.get("target-version") != "py313":
        violations.append(f"{path}: expected Ruff target-version py313")


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


def _check_site_publication_state(
    site_root: Path,
    *,
    source_root: Path,
    violations: list[str],
) -> None:
    _check_site_export_manifest(
        site_root,
        source_root=source_root,
        violations=violations,
    )
    posts_dir = site_root / "_posts"
    pages_dir = site_root / "_pages"
    final_post_paths: dict[str, Path] = {}
    hidden_page_paths: dict[str, Path] = {}
    for post in SUPPORTED_POSTS:
        post_matches = sorted(posts_dir.glob(f"*-kups-md-post-{post}-*.md"))
        if post_matches:
            final_post_paths[post] = post_matches[0]
        if len(post_matches) > 1:
            violations.append(
                f"{posts_dir}: expected one final _posts blog post for post {post}, "
                f"found {len(post_matches)}"
            )
        page_matches = sorted(pages_dir.glob(f"kups-md-post-{post}-*.md"))
        if page_matches:
            hidden_page_paths[post] = page_matches[0]
        if len(page_matches) > 1:
            violations.append(
                f"{pages_dir}: expected one hidden _pages draft for post {post}, "
                f"found {len(page_matches)}"
            )

    _check_site_series_index(
        site_root,
        violations,
        final_posts_available=len(final_post_paths) == len(SUPPORTED_POSTS),
    )
    if len(final_post_paths) == len(SUPPORTED_POSTS):
        _check_site_publication_dates(final_post_paths, violations)
    pages_dir = site_root / "_pages"
    for post in SUPPORTED_POSTS:
        page_path = final_post_paths.get(post)
        if page_path is None:
            violations.append(
                f"{posts_dir}: missing final _posts blog post for post {post}"
            )
            page_path = hidden_page_paths.get(post)
        if page_path is None:
            violations.append(f"{pages_dir}: missing website page for post {post}")
            continue
        text = page_path.read_text(encoding="utf-8")
        _check_site_blog_style(
            page_path,
            post,
            text,
            violations,
            final_post=post in final_post_paths,
        )
        if re.search(r"(?m)^nav:\s*false\s*$", text):
            violations.append(f"{page_path}: page remains hidden with nav: false")
        if "This page is not the final article" in text:
            violations.append(f"{page_path}: page still declares itself non-final")
        if "intentionally hidden from site navigation" in text:
            violations.append(f"{page_path}: page still has hidden-draft note")


def _check_site_publication_dates(
    post_paths: dict[str, Path],
    violations: list[str],
) -> None:
    publication_dates: dict[str, str] = {}
    for post, page_path in sorted(post_paths.items()):
        text = page_path.read_text(encoding="utf-8")
        front_matter = _front_matter(text)
        if front_matter is None:
            continue
        date = _front_matter_value(front_matter, "date")
        last_updated = _front_matter_value(front_matter, "last_updated")
        if not _is_iso_date(date):
            violations.append(f"{page_path}: front matter date is not YYYY-MM-DD")
            continue
        publication_dates[post] = date
        if not page_path.name.startswith(f"{date}-"):
            violations.append(
                f"{page_path}: _posts filename date does not match front matter date {date}"
            )
        if not _is_iso_date(last_updated):
            violations.append(
                f"{page_path}: front matter last_updated is not YYYY-MM-DD"
            )
        elif last_updated < date:
            violations.append(
                f"{page_path}: last_updated {last_updated} predates publication date {date}"
            )

    unique_dates = sorted(set(publication_dates.values()))
    if len(unique_dates) > 1:
        details = ", ".join(
            f"post {post}: {date}" for post, date in sorted(publication_dates.items())
        )
        violations.append(
            "kUPS final blog posts must share one publication date; found "
            + details
        )


def _is_iso_date(value: str | None) -> bool:
    return isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None


def _check_site_series_index(
    site_root: Path,
    violations: list[str],
    *,
    final_posts_available: bool,
) -> None:
    index_path = site_root / "_pages" / "kups-md-tutorials.md"
    if not index_path.exists():
        violations.append(f"{index_path}: missing kUPS series index page")
        return
    text = index_path.read_text(encoding="utf-8")
    front_matter = _front_matter(text)
    if front_matter is None:
        violations.append(f"{index_path}: missing YAML front matter")
        return

    required_pairs = {
        "layout": "page",
        "permalink": "/kups-md-tutorials/",
        "title": "kUPS MD Tutorials",
    }
    for key, expected in required_pairs.items():
        actual = _front_matter_value(front_matter, key)
        if actual != expected:
            violations.append(
                f"{index_path}: expected front matter {key}: {expected}, "
                f"found {actual or 'missing'}"
            )
    if _front_matter_value(front_matter, "description") is None:
        violations.append(f"{index_path}: missing front matter description")
    if not re.search(r"(?m)^pagination:\s*\n\s+enabled:\s*false\s*$", front_matter):
        violations.append(f"{index_path}: missing pagination enabled: false")
    if re.search(r"(?m)^nav:\s*false\s*$", text):
        violations.append(f"{index_path}: page remains hidden with nav: false")

    body = text.split("---", 2)[2] if text.startswith("---") else text
    expected_query = (
        '{% assign postlist = site.posts | where: "series", "kups-md-tutorials" | sort: "series_order" %}'
        if final_posts_available
        else '{% assign postlist = site.pages | where: "series", "kups-md-tutorials" | sort: "series_order" %}'
    )
    if (
        not final_posts_available
        and '{% assign postlist = site.pages | where: "series", "kups-md-tutorials" | sort: "series_order" %}'
        in body
    ):
        violations.append(
            f"{index_path}: series index still queries hidden pages instead of final posts"
        )

    required_fragments = {
        '<div class="publications blog-index">': "blog-index wrapper",
        expected_query: (
            "series-ordered post query"
            if final_posts_available
            else "series-ordered page query"
        ),
        "{% assign tutorial_count = postlist | size %}": "tutorial count assignment",
        "<h1>kUPS MD Tutorials</h1>": "series h1",
        '<p class="blog-index-note">': "blog-index note",
        '<div class="blog-type-summary"': "blog type summary",
        '<ol class="bibliography">': "bibliography list",
        "{% for post in postlist %}": "postlist loop",
        '<div class="title">': "blog-list title block",
        '{{ post.url | relative_url }}': "relative post URL link",
        "blog-list-description": "post description block",
        "blog-post-type blog-post-type-{{ post_type }}": "post type badge",
        "{{ read_time }} min read": "read-time metadata",
        "part {{ post.series_order }} of {{ tutorial_count }}": "series position metadata",
    }
    for fragment, description in required_fragments.items():
        if fragment not in body:
            violations.append(f"{index_path}: missing {description}")


def _check_site_export_manifest(
    site_root: Path,
    *,
    source_root: Path,
    violations: list[str],
) -> None:
    manifest_path = site_root / "assets" / "json" / "kups-md-tutorials" / "manifest.json"
    if not manifest_path.exists():
        violations.append(f"{manifest_path}: missing website export manifest")
        return
    text = manifest_path.read_text(encoding="utf-8")
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{manifest_path}: invalid JSON: {exc}")
        return
    if not isinstance(manifest, dict):
        violations.append(f"{manifest_path}: website export manifest must be a JSON object")
        return

    if manifest.get("profile") != "full":
        violations.append(
            f"{manifest_path}: expected profile full, found {manifest.get('profile')!r}"
        )
    source_revision = manifest.get("source_git_revision")
    if not isinstance(source_revision, str) or len(source_revision) < 7:
        violations.append(f"{manifest_path}: missing source_git_revision")
    elif source_revision == "unknown":
        violations.append(f"{manifest_path}: source_git_revision is unknown")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        violations.append(f"{manifest_path}: missing exported files")
        return

    posts_with_figures: set[str] = set()
    posts_with_results: set[str] = set()
    for index, item in enumerate(files, start=1):
        label = f"{manifest_path}: file {index}"
        if not isinstance(item, dict):
            violations.append(f"{label} must be a JSON object")
            continue
        post = item.get("post")
        kind = item.get("kind")
        destination_text = item.get("destination")
        sha256 = item.get("sha256")
        source = item.get("source")
        if post not in SUPPORTED_POSTS:
            violations.append(f"{label} has unsupported post {post!r}")
        if kind not in {"figure", "compact-result"}:
            violations.append(f"{label} has unsupported kind {kind!r}")
        if not isinstance(source, str) or not source:
            violations.append(f"{label} missing source")
        if not isinstance(destination_text, str) or not destination_text:
            violations.append(f"{label} missing destination")
            continue
        if not isinstance(sha256, str) or re.fullmatch(r"[0-9a-f]{64}", sha256) is None:
            violations.append(f"{label} missing sha256")
            continue

        if isinstance(source, str) and source:
            source_path = source_root / source
            if not _path_is_within(source_path.resolve(), source_root.resolve()):
                violations.append(f"{label} source escapes source root: {source}")
            elif not source_path.exists():
                violations.append(f"{label} source does not exist: {source}")
            else:
                source_sha256 = file_sha256(source_path)
                if source_sha256 != sha256:
                    violations.append(
                        f"{label} source sha256 mismatch for {source}: "
                        f"expected {sha256}, found {source_sha256}"
                    )

        destination = _site_manifest_destination(site_root, destination_text)
        if not _path_is_within(destination, site_root):
            violations.append(f"{label} destination escapes site root: {destination_text}")
            continue
        if not destination.exists():
            violations.append(f"{label} destination does not exist: {destination_text}")
            continue
        actual_sha256 = file_sha256(destination)
        if actual_sha256 != sha256:
            violations.append(
                f"{label} sha256 mismatch for {destination_text}: "
                f"expected {sha256}, found {actual_sha256}"
            )
        if post in SUPPORTED_POSTS:
            if kind == "figure":
                posts_with_figures.add(post)
            elif kind == "compact-result":
                posts_with_results.add(post)

    missing_figure_posts = sorted(set(SUPPORTED_POSTS) - posts_with_figures)
    if missing_figure_posts:
        violations.append(
            f"{manifest_path}: missing exported figure entries for posts "
            + ", ".join(missing_figure_posts)
        )
    missing_result_posts = sorted(set(SUPPORTED_POSTS) - posts_with_results)
    if missing_result_posts:
        violations.append(
            f"{manifest_path}: missing exported compact-result entries for posts "
            + ", ".join(missing_result_posts)
        )


def _check_site_blog_style(
    page_path: Path,
    post: str,
    text: str,
    violations: list[str],
    *,
    final_post: bool,
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
    if final_post:
        if f"kups-md-post-{post}" not in page_path.name:
            violations.append(f"{page_path}: _posts filename does not include kups-md-post-{post}")
        for page_only_key in ("permalink", "nav", "nav_order", "pagination"):
            if _front_matter_value(front_matter, page_only_key) is not None:
                violations.append(
                    f"{page_path}: final _posts article should not set "
                    f"page-only front matter {page_only_key}"
                )
    elif f"post-{post}" not in (_front_matter_value(front_matter, "permalink") or ""):
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
    _check_site_source_links(page_path, post, body, violations)
    _check_site_references(page_path, body, violations)
    _check_site_figures(page_path, post, body, violations)
    _check_site_footnotes(page_path, body, violations)
    _check_site_notebook_transcript_markers(page_path, body, violations)
    word_count = _body_word_count(body)
    if not MIN_POST_WORDS <= word_count <= MAX_POST_WORDS:
        violations.append(
            f"{page_path}: expected {MIN_POST_WORDS}-{MAX_POST_WORDS} body words, "
            f"found {word_count}"
        )


def _check_site_source_links(
    page_path: Path,
    post: str,
    body: str,
    violations: list[str],
) -> None:
    required_fragments = {
        f"configs/post-{post}/smoke.json": "smoke configuration link",
        f"configs/post-{post}/full.json": "full configuration link",
        f"notebooks/post-{post}": "notebook link",
        f"results/post-{post}/full/manifest.json": "full provenance manifest link",
        f"scripts/generate_post{post}_figures.py": "figure-generation source link",
        f"reviews/post-{post}.md": "self-review note link",
    }
    for fragment, description in required_fragments.items():
        if fragment not in body:
            violations.append(f"{page_path}: missing {description}: {fragment}")

    summary_link_patterns = {
        "smoke compact summary link": rf"results/post-{post}/smoke/[^)\s]+_summary\.json",
        "full compact summary link": rf"results/post-{post}/full/[^)\s]+_summary\.json",
    }
    for description, pattern in summary_link_patterns.items():
        if re.search(pattern, body) is None:
            violations.append(f"{page_path}: missing {description}")


def _check_site_notebook_transcript_markers(
    page_path: Path,
    body: str,
    violations: list[str],
) -> None:
    transcript_patterns = {
        r"(?m)^\s*In\s*\[\d*\]:": "Jupyter input prompt",
        r"(?m)^\s*Out\s*\[\d+\]:": "Jupyter output prompt",
        r"(?m)^\s*execution_count\s*:": "notebook execution_count field",
        r"(?m)^\s*cell_type\s*:": "notebook cell_type field",
    }
    for pattern, description in transcript_patterns.items():
        if re.search(pattern, body):
            violations.append(
                f"{page_path}: contains notebook transcript marker: {description}"
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
    post: str,
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
        elif not figure_path.endswith((".svg", ".png")):
            violations.append(f"{label} path should reference a static SVG/PNG asset")
        elif f"post{post}" not in figure_path and f"post-{post}" not in figure_path:
            violations.append(f"{label} path does not identify post {post}")
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


def _check_site_footnotes(
    page_path: Path,
    body: str,
    violations: list[str],
) -> None:
    body_without_definitions = re.sub(r"(?m)^\[\^[^\]]+\]:.*$", "", body)
    used_ids = set(re.findall(r"\[\^([^\]]+)\]", body_without_definitions))
    definition_ids = set(re.findall(r"(?m)^\[\^([^\]]+)\]:", body))
    footnote_ids = used_ids | definition_ids

    for footnote_id in sorted(footnote_ids):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,19}", footnote_id):
            violations.append(
                f"{page_path}: footnote id {footnote_id!r} must be a short "
                "single word without hyphens"
            )

    missing_definitions = sorted(used_ids - definition_ids)
    if missing_definitions:
        violations.append(
            f"{page_path}: missing footnote definition(s) for "
            + ", ".join(missing_definitions)
        )

    unused_definitions = sorted(definition_ids - used_ids)
    if unused_definitions:
        violations.append(
            f"{page_path}: unused footnote definition(s): "
            + ", ".join(unused_definitions)
        )


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


def _check_result_manifest_file(
    path: Path,
    violations: list[str],
    *,
    config_root: Path,
    post: str,
    profile: str,
) -> None:
    if not path.exists():
        violations.append(f"{path}: missing {profile} result manifest")
        return
    text = path.read_text(encoding="utf-8")
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(manifest, dict):
        violations.append(f"{path}: result manifest must be a JSON object")
        return
    _check_manifest_provenance(
        path,
        manifest,
        config_root=config_root,
        post=post,
        profile=profile,
        violations=violations,
    )
    _check_manifest_execution(path, manifest, profile=profile, violations=violations)
    _check_manifest_output_files(path, manifest, violations)


def _check_manifest_provenance(
    path: Path,
    manifest: dict[str, object],
    *,
    config_root: Path,
    post: str,
    profile: str,
    violations: list[str],
) -> None:
    repo_root = config_root.parent
    config = manifest.get("config")
    if not isinstance(config, dict):
        violations.append(f"{path}: missing config object")
    else:
        if str(config.get("post")) != post:
            violations.append(
                f"{path}: expected config.post {post}, found {config.get('post')!r}"
            )
        if config.get("profile") != profile:
            violations.append(
                f"{path}: expected config.profile {profile}, "
                f"found {config.get('profile')!r}"
            )

    provenance = manifest.get("provenance")
    if not isinstance(provenance, dict):
        violations.append(f"{path}: missing provenance object")
    else:
        _check_required_string(path, provenance, "config_path", violations)
        _check_hex_digest(path, provenance, "config_sha256", violations)
        _check_required_string(path, provenance, "lock_path", violations)
        _check_hex_digest(path, provenance, "lock_sha256", violations)
        _check_manifest_file_hash(
            path,
            provenance,
            repo_root=repo_root,
            path_key="config_path",
            sha_key="config_sha256",
            expected_path=config_root / f"post-{post}" / f"{profile}.json",
            violations=violations,
        )
        _check_manifest_file_hash(
            path,
            provenance,
            repo_root=repo_root,
            path_key="lock_path",
            sha_key="lock_sha256",
            expected_path=repo_root / "uv.lock",
            violations=violations,
        )
        git_revision = provenance.get("git_revision")
        if not isinstance(git_revision, str) or len(git_revision) < 7:
            violations.append(f"{path}: missing provenance git_revision")
        elif git_revision == "unknown":
            violations.append(f"{path}: provenance git_revision is unknown")
        _check_required_string(path, provenance, "python_version", violations)
        _check_required_string(path, provenance, "platform", violations)
        _check_required_string(path, provenance, "runtime_device", violations)
        precision = provenance.get("precision_policy")
        if not isinstance(precision, str) or "jax_enable_x64=" not in precision:
            violations.append(f"{path}: missing provenance precision_policy")

    versions = manifest.get("versions")
    if not isinstance(versions, dict):
        violations.append(f"{path}: missing versions object")
    else:
        for package in ("kups", "numpy"):
            _check_required_string(path, versions, package, violations)


def _check_manifest_output_files(
    path: Path,
    manifest: dict[str, object],
    violations: list[str],
) -> None:
    output_fields = {
        key: value
        for key, value in manifest.items()
        if key.endswith("_file") and key != "config_file"
    }
    if not output_fields:
        violations.append(f"{path}: missing result output file references")
        return

    result_dir = path.parent
    for field, value in sorted(output_fields.items()):
        if not isinstance(value, str) or not value:
            violations.append(f"{path}: missing manifest {field}")
            continue
        output_path = Path(value)
        if output_path.is_absolute():
            violations.append(f"{path}: manifest {field} should be result-relative")
            continue
        if output_path.suffix not in ALLOWED_MANIFEST_OUTPUT_SUFFIXES:
            allowed = ", ".join(ALLOWED_MANIFEST_OUTPUT_SUFFIXES)
            violations.append(
                f"{path}: manifest {field} should reference compact output "
                f"({allowed}), found {value}"
            )
            continue
        resolved_path = result_dir / output_path
        if not _path_is_within(resolved_path, result_dir):
            violations.append(f"{path}: manifest {field} escapes result directory")
            continue
        if not resolved_path.exists():
            violations.append(
                f"{path}: manifest {field} does not exist: {value}"
            )


def _check_manifest_execution(
    path: Path,
    manifest: dict[str, object],
    *,
    profile: str,
    violations: list[str],
) -> None:
    execution = manifest.get("execution")
    if not isinstance(execution, dict):
        violations.append(f"{path}: missing execution timing metadata")
        return

    elapsed = execution.get("elapsed_seconds")
    if not isinstance(elapsed, int | float) or elapsed <= 0:
        violations.append(f"{path}: missing positive execution elapsed_seconds")
    measured_by = execution.get("measured_by")
    if measured_by != "kups_md_tutorials.workflows.run_post":
        violations.append(f"{path}: missing workflow execution measurement source")

    max_seconds = execution.get("max_full_profile_seconds")
    if profile == "full":
        if not isinstance(max_seconds, int | float) or max_seconds <= 0:
            violations.append(f"{path}: missing positive max_full_profile_seconds")
        elif isinstance(elapsed, int | float) and elapsed > max_seconds:
            violations.append(
                f"{path}: full-profile execution elapsed_seconds {elapsed} "
                f"exceeds max_full_profile_seconds {max_seconds}"
            )


def _check_manifest_file_hash(
    path: Path,
    provenance: dict[str, object],
    *,
    repo_root: Path,
    path_key: str,
    sha_key: str,
    expected_path: Path,
    violations: list[str],
) -> None:
    path_text = provenance.get(path_key)
    expected_sha = provenance.get(sha_key)
    if not isinstance(path_text, str) or not isinstance(expected_sha, str):
        return

    provenance_path = Path(path_text)
    if provenance_path.is_absolute():
        violations.append(f"{path}: provenance {path_key} should be repository-relative")
        return
    resolved_path = repo_root / provenance_path
    if not _path_is_within(resolved_path, repo_root):
        violations.append(f"{path}: provenance {path_key} escapes repository root")
        return
    if resolved_path != expected_path:
        violations.append(
            f"{path}: expected provenance {path_key} "
            f"{expected_path.relative_to(repo_root).as_posix()}, found {path_text}"
        )
        return
    if not resolved_path.exists():
        violations.append(f"{path}: provenance {path_key} does not exist: {path_text}")
        return
    actual_sha = file_sha256(resolved_path)
    if expected_sha != actual_sha:
        violations.append(
            f"{path}: provenance {sha_key} mismatch for {path_text}: "
            f"expected {expected_sha!r}, found {actual_sha}"
        )


def _check_required_string(
    path: Path,
    section: dict[str, object],
    key: str,
    violations: list[str],
) -> None:
    value = section.get(key)
    if not isinstance(value, str) or not value:
        violations.append(f"{path}: missing {key}")


def _check_hex_digest(
    path: Path,
    section: dict[str, object],
    key: str,
    violations: list[str],
) -> None:
    value = section.get(key)
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        violations.append(f"{path}: missing {key}")


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


def _relative_or_posix(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def _relative_to_root_or_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return _relative_or_posix(path)


def _ledger_path_exists(repo_root: Path, path_text: str) -> bool:
    path = Path(path_text)
    if path.is_absolute():
        return path.exists()
    return path.exists() or (repo_root / path).exists()


def _single_notebook_for_post(notebook_root: Path, post: str) -> Path | None:
    matches = sorted(notebook_root.glob(f"post-{post}-*.ipynb"))
    if len(matches) != 1:
        return None
    return matches[0].relative_to(notebook_root.parent)


def _notebook_code_cell_count(path: Path, violations: list[str]) -> int | None:
    text = path.read_text(encoding="utf-8")
    try:
        notebook = json.loads(text)
    except json.JSONDecodeError as exc:
        violations.append(f"{path}: invalid notebook JSON: {exc}")
        return None
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        violations.append(f"{path}: notebook missing cells list")
        return None
    return sum(
        1
        for cell in cells
        if isinstance(cell, dict) and cell.get("cell_type") == "code"
    )


def _site_manifest_destination(site_root: Path, destination_text: str) -> Path:
    destination = Path(destination_text)
    if destination.is_absolute():
        return destination
    return site_root / destination


def _git_head_sha(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    try:
        completed = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            cwd=path,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def _git_revision_is_ancestor(repo_root: Path, ancestor: str, descendant: str) -> bool:
    try:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", ancestor, descendant),
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def _git_changed_files(repo_root: Path, ancestor: str, descendant: str) -> tuple[str, ...] | None:
    try:
        completed = subprocess.run(
            ("git", "diff", "--name-only", f"{ancestor}..{descendant}"),
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return tuple(
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip()
    )


def _string_set(value: object) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


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
