"""Export compact tutorial artifacts to the website repository."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import os
import shutil

from kups_md_tutorials.provenance import file_sha256, git_revision

SUPPORTED_POSTS = tuple(f"{post:02d}" for post in range(1, 13))
COMPACT_RESULT_SUFFIXES = (".csv", ".json")


@dataclass(frozen=True)
class ExportedFile:
    """One file copied into the website repository."""

    post: str
    kind: str
    source: str
    destination: str
    sha256: str


@dataclass(frozen=True)
class SiteExportManifest:
    """Manifest for one website export operation."""

    profile: str
    source_git_revision: str
    files: tuple[ExportedFile, ...]


def export_site_assets(
    site_root: Path = Path("../sungsoo-ahn.github.io"),
    profile: str = "full",
    results_root: Path = Path("results"),
    figures_root: Path = Path("figures"),
    posts: tuple[str, ...] | None = None,
) -> Path:
    """Copy publication figures and compact result files to the website repo."""

    site_root = site_root.resolve()
    figures_root = figures_root.resolve()
    results_root = results_root.resolve()
    source_root = Path(os.path.commonpath((figures_root, results_root)))
    exported: list[ExportedFile] = []
    selected_posts = SUPPORTED_POSTS if posts is None else posts
    for post in selected_posts:
        normalized_post = post.zfill(2)
        _validate_post(normalized_post)
        exported.extend(
            _export_post_figures(
                normalized_post,
                site_root,
                figures_root,
                source_root,
            )
        )
        exported.extend(
            _export_post_compact_results(
                normalized_post,
                profile,
                site_root,
                results_root,
                source_root,
            )
        )

    manifest = SiteExportManifest(
        profile=profile,
        source_git_revision=git_revision(Path(".")),
        files=tuple(exported),
    )
    manifest_path = site_root / "assets" / "json" / "kups-md-tutorials" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def _validate_post(post: str) -> None:
    if post not in SUPPORTED_POSTS:
        msg = f"post {post!r} is not supported"
        raise ValueError(msg)


def _export_post_figures(
    post: str,
    site_root: Path,
    figures_root: Path,
    source_root: Path,
) -> list[ExportedFile]:
    figure_dir = figures_root / f"post-{post}"
    source_svgs = sorted(figure_dir.glob("*_full.svg"))
    if not source_svgs:
        msg = f"missing full-profile SVG figure for post {post}: {figure_dir}"
        raise FileNotFoundError(msg)

    exported: list[ExportedFile] = []
    for source_svg in source_svgs:
        stem = source_svg.stem.removesuffix("_full")
        for source in (source_svg, source_svg.with_suffix(".png")):
            if not source.exists():
                msg = f"missing paired website figure asset: {source}"
                raise FileNotFoundError(msg)
            destination = (
                site_root
                / "assets"
                / "img"
                / "blog"
                / f"kups_md_post{post}_{stem}{source.suffix}"
            )
            exported.append(
                _copy_file(post, "figure", source, destination, source_root, site_root)
            )
    return exported


def _export_post_compact_results(
    post: str,
    profile: str,
    site_root: Path,
    results_root: Path,
    source_root: Path,
) -> list[ExportedFile]:
    result_dir = results_root / f"post-{post}" / profile
    if not result_dir.exists():
        msg = f"missing result directory for post {post} {profile}: {result_dir}"
        raise FileNotFoundError(msg)

    exported: list[ExportedFile] = []
    for source in sorted(result_dir.iterdir()):
        if not source.is_file() or source.suffix not in COMPACT_RESULT_SUFFIXES:
            continue
        destination = (
            site_root
            / "assets"
            / "json"
            / "kups-md-tutorials"
            / f"post-{post}"
            / profile
            / source.name
        )
        exported.append(
            _copy_file(post, "compact-result", source, destination, source_root, site_root)
        )
    if not exported:
        msg = f"no compact result files found for post {post} {profile}: {result_dir}"
        raise FileNotFoundError(msg)
    return exported


def _copy_file(
    post: str,
    kind: str,
    source: Path,
    destination: Path,
    source_root: Path,
    site_root: Path,
) -> ExportedFile:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return ExportedFile(
        post=post,
        kind=kind,
        source=_relative_or_posix(source, source_root),
        destination=_relative_or_posix(destination, site_root),
        sha256=file_sha256(destination),
    )


def _relative_or_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
