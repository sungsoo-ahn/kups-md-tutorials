import json
from pathlib import Path
import shutil

import pytest

from kups_md_tutorials.cli import main
from kups_md_tutorials.release_readiness import (
    audit_release_readiness,
    verify_release_surface,
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
            shutil.copyfile(
                Path("configs") / f"post-{post_id}" / f"{profile}.json",
                config_dir / f"{profile}.json",
            )
            result_dir = root / "results" / f"post-{post_id}" / profile
            result_dir.mkdir(parents=True)
            (result_dir / "manifest.json").write_text(
                json.dumps(_manifest_fixture(post_id, profile)) + "\n",
                encoding="utf-8",
            )
            (result_dir / "example_summary.json").write_text(
                json.dumps({"post": post_id, "profile": profile}) + "\n",
                encoding="utf-8",
            )

        (notebook_dir / f"post-{post_id}-example.ipynb").write_text(
            json.dumps(
                {
                    "cells": [
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": "print('ok')",
                        }
                    ],
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
    _write_figure_source_ledger(root)
    _write_notebook_execution_ledger(root)


def _write_figure_source_ledger(root: Path) -> None:
    review_dir = root / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    ledger = {}
    for post in range(1, 13):
        post_id = f"{post:02d}"
        ledger[f"post-{post_id}"] = [
            {
                "figure_files": [
                    f"figures/post-{post_id}/example_diagnostics.svg",
                    f"figures/post-{post_id}/example_diagnostics.png",
                    f"figures/post-{post_id}/example_diagnostics_full.svg",
                    f"figures/post-{post_id}/example_diagnostics_full.png",
                ],
                "source_url": f"internal:scripts/generate_post{post_id}_figures.py",
                "source_type": "custom-generated",
                "license": "repository-owned draft figure",
                "modifications": (
                    "Generated from committed compact tutorial outputs; no external "
                    "figure source was reused."
                ),
                "generator": f"scripts/generate_post{post_id}_figures.py",
                "source_data": [
                    f"configs/post-{post_id}/full.json",
                    f"results/post-{post_id}/full/example_summary.json",
                ],
            }
        ]
    (review_dir / "figure-sources.json").write_text(
        json.dumps(ledger, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_notebook_execution_ledger(root: Path) -> None:
    review_dir = root / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for post in range(1, 13):
        post_id = f"{post:02d}"
        notebook_path = root / "notebooks" / f"post-{post_id}-example.ipynb"
        entries.append(
            {
                "post": post_id,
                "source": f"notebooks/post-{post_id}-example.ipynb",
                "source_sha256": _sha256(notebook_path),
                "code_cells": 1,
                "executed_code_cells": 1,
                "output_count": 1,
            }
        )
    (review_dir / "notebook-execution.json").write_text(
        json.dumps(
            {
                "kernel_name": "python3",
                "timeout_seconds": 120,
                "notebooks": entries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _manifest_fixture(post_id: str, profile: str) -> dict[str, object]:
    return {
        "config": {
            "post": post_id,
            "profile": profile,
            "experiment": {"seed": 2026071400 + int(post_id)},
        },
        "provenance": {
            "config_path": f"configs/post-{post_id}/{profile}.json",
            "config_sha256": "a" * 64,
            "lock_path": "uv.lock",
            "lock_sha256": "b" * 64,
            "git_revision": "c" * 40,
            "python_version": "3.13.0",
            "platform": "test",
            "runtime_device": "jax:cpu;devices:cpu",
            "precision_policy": "jax_enable_x64=false;env_JAX_ENABLE_X64=unset",
        },
        "summary_file": "example_summary.json",
        "versions": {"kups": "1.0.3", "numpy": "2.0.0"},
    }


def _write_post12_model_metadata(root: Path, *, placeholder: bool) -> None:
    config_dir = root / "configs" / "post-12"
    results_dir = root / "results" / "post-12" / "full"
    revision = "pinned-placeholder" if placeholder else "mace-v0.3.10"
    sha = "pending-gpu-artifact-hash" if placeholder else "a" * 64
    summary = (
        "{"
        f'"model_revision": "{revision}", "model_sha256": "{sha}"'
        "}\n"
    )
    for profile in ("smoke", "full"):
        config_path = config_dir / f"{profile}.json"
        config_data = json.loads(config_path.read_text(encoding="utf-8"))
        artifact = config_data["mlip_experiment"]["model_artifact"]
        artifact["revision"] = revision
        artifact["sha256"] = sha
        config_path.write_text(json.dumps(config_data) + "\n", encoding="utf-8")

    manifest_data = _manifest_fixture("12", "full")
    manifest_data["config"]["experiment"]["model_artifact"] = {
        "revision": revision,
        "sha256": sha,
    }
    (results_dir / "mlip_summary.json").write_text(summary, encoding="utf-8")
    (results_dir / "manifest.json").write_text(
        json.dumps(manifest_data) + "\n",
        encoding="utf-8",
    )


def _write_site_pages(site_root: Path, *, hidden: bool) -> None:
    pages = site_root / "_pages"
    figure_dir = site_root / "assets" / "img" / "blog"
    export_dir = site_root / "assets" / "json" / "kups-md-tutorials"
    pages.mkdir(parents=True)
    figure_dir.mkdir(parents=True)
    body_words = " ".join(f"sample{idx}" for idx in range(3600))
    exported_files = []
    for post in range(1, 13):
        post_id = f"{post:02d}"
        figure_path = f"assets/img/blog/kups_md_post{post_id}_diagnostics.svg"
        figure_file = site_root / figure_path
        figure_file.write_text("<svg></svg>\n", encoding="utf-8")
        exported_files.append(
            {
                "post": post_id,
                "kind": "figure",
                "source": f"figures/post-{post_id}/example_diagnostics_full.svg",
                "destination": figure_path,
                "sha256": _sha256(figure_file),
            }
        )
        result_path = f"assets/json/kups-md-tutorials/post-{post_id}/full/manifest.json"
        result_file = site_root / result_path
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_file.write_text(json.dumps(_manifest_fixture(post_id, "full")) + "\n")
        exported_files.append(
            {
                "post": post_id,
                "kind": "compact-result",
                "source": f"results/post-{post_id}/full/manifest.json",
                "destination": result_path,
                "sha256": _sha256(result_file),
            }
        )
        nav = "false" if hidden else "true"
        note_context = (
            "This page is not the final article. "
            "It is intentionally hidden from site navigation. "
            if hidden
            else "Final article. "
        )
        (pages / f"kups-md-post-{post:02d}-example.md").write_text(
            "---\n"
            "layout: post\n"
            f"permalink: /kups-md-tutorials/post-{post_id}-example/\n"
            f'title: "Post {post_id}"\n'
            "date: 2026-07-14\n"
            "last_updated: 2026-07-15\n"
            f'description: "Post {post_id} description."\n'
            "post_type: tutorial\n"
            'authors: ["Sungsoo Ahn"]\n'
            f"order: {post}\n"
            "series: kups-md-tutorials\n"
            'series_title: "kUPS Molecular Dynamics Tutorials"\n'
            'series_description: "Executable molecular-dynamics practice for MLIP-aware machine-learning researchers."\n'
            f"series_order: {post}\n"
            "categories: [science]\n"
            "tags: [molecular-dynamics, kups]\n"
            "toc:\n"
            "  sidebar: left\n"
            "related_posts: false\n"
            f"nav: {nav}\n"
            "---\n\n"
            '<p style="color: #666; font-size: 0.9em; margin-bottom: 1.5em;">\n'
            f"<em>Note: {note_context}Corrections and replication issues should be tracked in "
            '<a href="https://github.com/sungsoo-ahn/kups-md-tutorials">sungsoo-ahn/kups-md-tutorials</a>.</em>\n'
            "</p>\n"
            f"\n<span id=\"cite-example{post_id}\"></span>[Example {post_id}](#ref-example{post_id})\n\n"
            f'{{% include figure.liquid path="{figure_path}" class="img-fluid rounded z-depth-1" zoomable=true caption="Figure {post_id} diagnostics for the committed full profile. The caption explains the mechanism supported by the figure." %}}\n\n'
            f"{body_words}\n\n"
            "## References\n\n"
            f"- <span id=\"ref-example{post_id}\"></span>Example {post_id}. "
            f'<a href="#cite-example{post_id}" class="reversefootnote" role="doc-backlink">↩</a>\n',
            encoding="utf-8",
        )
    export_dir.mkdir(parents=True, exist_ok=True)
    (export_dir / "manifest.json").write_text(
        json.dumps(
            {
                "profile": "full",
                "source_git_revision": "c" * 40,
                "files": exported_files,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


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


def test_release_surface_allows_current_project_blockers() -> None:
    result = verify_release_surface(
        review_dir=Path("reviews"),
        config_root=Path("configs"),
        results_root=Path("results"),
        notebook_root=Path("notebooks"),
        figure_root=Path("figures"),
        snapshot_root=Path("snapshots"),
        site_root=None,
    )

    assert result.checked_posts == 12
    assert result.violations
    assert all(
        "unresolved final-release blockers" in violation
        for violation in result.violations
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


def test_release_readiness_reports_stale_site_export_manifest(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    manifest_path = (
        tmp_path / "site" / "assets" / "json" / "kups-md-tutorials" / "manifest.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"] = [
        item
        for item in manifest["files"]
        if not (item["post"] == "08" and item["kind"] == "figure")
    ]
    manifest["files"][0]["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("sha256 mismatch" in violation for violation in result.violations)
    assert any(
        "missing exported figure entries for posts 08" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_blog_style_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-03-example.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace("post_type: tutorial\n", "")
    text = text.replace("  sidebar: left\n", "")
    text = text.replace("<em>Note:", "<em>")
    page.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("post_type: tutorial" in violation for violation in result.violations)
    assert any("toc sidebar: left" in violation for violation in result.violations)
    assert any("author-note Note text" in violation for violation in result.violations)


def test_release_readiness_reports_short_site_page(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-04-example.md"
    text = page.read_text(encoding="utf-8")
    front_matter, body = text.split("---\n\n", 1)
    note = body.split("</p>", 1)[0] + "</p>\n"
    page.write_text(
        front_matter + "---\n\n" + note + "\nshort body\n",
        encoding="utf-8",
    )

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
        "expected 3500-10000 body words" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_site_reference_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-04-example.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace('id="ref-example04"', 'id="ref-broken04"')
    text = text.replace('href="#cite-example04"', 'href="#cite-missing04"')
    page.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("cite-example04 has no matching ref-* anchor" in violation for violation in result.violations)
    assert any("ref-broken04 has no matching cite-* anchor" in violation for violation in result.violations)


def test_release_readiness_reports_missing_reference_backlink(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-05-example.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace('href="#cite-example05"', 'href="#cite-other05"')
    page.write_text(text, encoding="utf-8")

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
        "ref-example05 missing reverse backlink(s) to cite-example05" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_site_figure_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-06-example.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        'path="assets/img/blog/kups_md_post06_diagnostics.svg"',
        'path="assets/img/other.svg"',
    )
    text = text.replace('class="img-fluid rounded z-depth-1"', 'class="bad"')
    text = text.replace("zoomable=true", "zoomable=false")
    text = text.replace(
        "Figure 06 diagnostics for the committed full profile. "
        "The caption explains the mechanism supported by the figure.",
        "Short caption with $x$.",
    )
    page.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("path is not under assets/img/blog/" in violation for violation in result.violations)
    assert any('expected class="img-fluid rounded z-depth-1"' in violation for violation in result.violations)
    assert any("expected zoomable=true" in violation for violation in result.violations)
    assert any("caption uses dollar math delimiters" in violation for violation in result.violations)
    assert any("caption should have at least two sentences" in violation for violation in result.violations)


def test_release_readiness_reports_site_footnote_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-post-07-example.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        "sample0",
        "sample0 with malformed footnote[^bad-id] and missing footnote[^missing]",
        1,
    )
    text += "\n[^bad-id]: A distracting caveat.\n[^unused]: Not referenced.\n"
    page.write_text(text, encoding="utf-8")

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
        "footnote id 'bad-id' must be a short single word without hyphens" in violation
        for violation in result.violations
    )
    assert any("missing footnote definition(s) for missing" in violation for violation in result.violations)
    assert any("unused footnote definition(s): unused" in violation for violation in result.violations)


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


def test_release_surface_rejects_structural_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    (tmp_path / "reviews" / "figure-sources.json").unlink()

    with pytest.raises(ValueError, match="release surface audit failed"):
        verify_release_surface(
            review_dir=tmp_path / "reviews",
            config_root=tmp_path / "configs",
            results_root=tmp_path / "results",
            notebook_root=tmp_path / "notebooks",
            figure_root=tmp_path / "figures",
            snapshot_root=tmp_path / "snapshots",
            site_root=tmp_path / "site",
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


def test_release_readiness_reports_typed_config_validation_errors(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    config_path = tmp_path / "configs" / "post-02" / "full.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["integrator_experiment"]["num_steps"] = 0
    config_path.write_text(json.dumps(config) + "\n", encoding="utf-8")

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
        "configs/post-02/full.json" in violation
        and "typed config validation failed" in violation
        and "num_steps must be positive" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_missing_figure_source_provenance(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    ledger_path = tmp_path / "reviews" / "figure-sources.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["post-08"][0]["figure_files"].remove(
        "figures/post-08/example_diagnostics_full.png"
    )
    ledger["post-08"][0]["license"] = ""
    ledger_path.write_text(json.dumps(ledger) + "\n", encoding="utf-8")

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
        "missing source provenance for figures/post-08/example_diagnostics_full.png"
        in violation
        for violation in result.violations
    )
    assert any("post-08 entry 1 missing license" in violation for violation in result.violations)


def test_release_readiness_reports_stale_notebook_execution_ledger(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    ledger_path = tmp_path / "reviews" / "notebook-execution.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["notebooks"] = [
        entry for entry in ledger["notebooks"] if entry["post"] != "08"
    ]
    ledger["notebooks"][0]["source_sha256"] = "0" * 64
    ledger["notebooks"][1]["executed_code_cells"] = 0
    ledger_path.write_text(json.dumps(ledger) + "\n", encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("source_sha256 mismatch" in violation for violation in result.violations)
    assert any("does not match code_cells" in violation for violation in result.violations)
    assert any(
        "missing notebook execution entries for posts 08" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_manifest_provenance_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    manifest_path = tmp_path / "results" / "post-07" / "full" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["config"]["post"] = "99"
    manifest["provenance"]["git_revision"] = "unknown"
    manifest["provenance"]["config_sha256"] = "not-a-sha"
    manifest["versions"].pop("kups")
    manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("expected config.post 07" in violation for violation in result.violations)
    assert any("provenance git_revision is unknown" in violation for violation in result.violations)
    assert any("missing config_sha256" in violation for violation in result.violations)
    assert any("missing kups" in violation for violation in result.violations)


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


def test_verify_release_surface_cli_allows_current_blockers() -> None:
    assert (
        main(
            [
                "verify-release-readiness",
                "--skip-site",
                "--allow-current-blockers",
            ]
        )
        == 0
    )
