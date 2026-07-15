import json
from pathlib import Path
import shutil
import subprocess

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
    (root / "uv.lock").write_text("locked test dependencies\n", encoding="utf-8")
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
            config_sha256 = _sha256(config_dir / f"{profile}.json")
            lock_sha256 = _sha256(root / "uv.lock")
            result_dir = root / "results" / f"post-{post_id}" / profile
            result_dir.mkdir(parents=True)
            (result_dir / "manifest.json").write_text(
                json.dumps(
                    _manifest_fixture(
                        post_id,
                        profile,
                        config_sha256=config_sha256,
                        lock_sha256=lock_sha256,
                    )
                )
                + "\n",
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
    _write_figure_generators(root)
    _write_figure_source_ledger(root)
    _write_notebook_execution_ledger(root)
    _write_page_snapshot_ledger(root)
    _write_website_build_ledger(root)
    _write_ci_workflow(root)
    _write_gitignore_policy(root)
    _write_pyproject_contract(root)


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
                    f"configs/post-{post_id}/smoke.json",
                    f"configs/post-{post_id}/full.json",
                    f"results/post-{post_id}/smoke/example_summary.json",
                    f"results/post-{post_id}/full/example_summary.json",
                ],
            }
        ]
    (review_dir / "figure-sources.json").write_text(
        json.dumps(ledger, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_figure_generators(root: Path) -> None:
    scripts_dir = root / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for post in range(1, 13):
        post_id = f"{post:02d}"
        (scripts_dir / f"generate_post{post_id}_figures.py").write_text(
            f"# synthetic post {post_id} figure generator\n",
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
                "executed_copy": f"/tmp/kups-notebook-runs/post-{post_id}-example.ipynb",
                "source_sha256": _sha256(notebook_path),
                "source_sha256_after": _sha256(notebook_path),
                "source_unchanged": True,
                "code_cells": 1,
                "executed_code_cells": 1,
                "output_count": 1,
                "elapsed_seconds": 1.0,
            }
        )
    (review_dir / "notebook-execution.json").write_text(
        json.dumps(
            {
                "source_git_revision": "c" * 40,
                "execution_mode": "fresh_kernel_per_notebook",
                "kernel_name": "python3",
                "timeout_seconds": 120,
                "notebooks": entries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_page_snapshot_ledger(root: Path) -> None:
    review_dir = root / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    snapshot_lines = [
        "# Rendered Page Snapshot Review",
        "",
        "## Synthetic Release Snapshot Pass",
        "",
        "- Website workflow: `Capture kUPS snapshots`.",
        "- Snapshot run: `123456789`.",
        "- Artifact name: `kups-md-page-snapshots`.",
        "- Manifest reviewed: `/tmp/kups-snapshots/manifest.json`.",
        "",
        "Manifest coverage:",
        "",
        "- Desktop and mobile snapshots were captured for the hidden index and Posts 01-12.",
        "- All captured URLs returned HTTP 200.",
        "",
        "Snapshots visually inspected:",
        "",
        "- `/tmp/kups-snapshots/post-index-desktop.png`",
        "- `/tmp/kups-snapshots/post-index-mobile.png`",
    ]
    for post in range(1, 13):
        post_id = f"{post:02d}"
        snapshot_lines.extend(
            [
                f"- `/tmp/kups-snapshots/post-{post_id}-desktop.png`",
                f"- `/tmp/kups-snapshots/post-{post_id}-mobile.png`",
            ]
        )
    snapshot_lines.extend(
        [
            "",
            "Feedback:",
            "",
            "- Desktop and mobile captures were inspected for page chrome, figures, tables, code blocks, references, and footer spacing.",
            "",
            "Revision decisions:",
            "",
            "- Accepted for the synthetic clean final-state fixture.",
        ]
    )
    (review_dir / "page-snapshots.md").write_text(
        "\n".join(snapshot_lines) + "\n",
        encoding="utf-8",
    )


def _write_website_build_ledger(root: Path) -> None:
    review_dir = root / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "website-build.json").write_text(
        json.dumps(
            {
                "repository": "sungsoo-ahn/sungsoo-ahn.github.io",
                "workflow": "Deploy site",
                "run_id": 123456789,
                "run_url": (
                    "https://github.com/sungsoo-ahn/sungsoo-ahn.github.io/"
                    "actions/runs/123456789"
                ),
                "head_sha": "c" * 40,
                "status": "completed",
                "conclusion": "success",
                "validated_steps": [
                    "Validate blog posts",
                    "Validate hidden kUPS pages",
                    "Build site",
                    "Deploy to GitHub Pages",
                ],
                "validated_commands": [
                    "python3 scripts/validate_blog.py",
                    "python3 scripts/validate_kups_pages.py",
                    "bundle exec jekyll build",
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_ci_workflow(root: Path) -> None:
    workflow_dir = root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "verify.yml").write_text(
        "name: Verify tutorials\n"
        "jobs:\n"
        "  verify:\n"
        "    steps:\n"
        "      - name: Install dependencies\n"
        "        run: uv sync --locked\n"
        "      - name: Ruff\n"
        "        run: uv run ruff check .\n"
        "      - name: Pytest\n"
        "        run: uv run pytest -q\n"
        "      - name: Reproduce smoke outputs\n"
        "        run: uv run kups-tutorial run-all --profile smoke --output-dir /tmp/kups-md-smoke\n"
        "      - name: Verify smoke outputs\n"
        "        run: uv run kups-tutorial verify --profile smoke --output-dir /tmp/kups-md-smoke\n"
        "      - name: Verify committed full outputs\n"
        "        run: uv run kups-tutorial verify --profile full\n"
        "      - name: Audit tracked artifacts\n"
        "        run: uv run kups-tutorial verify-artifacts\n"
        "      - name: Audit review notes\n"
        "        run: uv run kups-tutorial verify-reviews\n"
        "      - name: Audit release surface\n"
        "        run: uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers\n"
        "      - name: Execute notebooks\n"
        "        run: uv run kups-tutorial verify-notebooks --output-dir /tmp/kups-md-notebooks\n"
        "      - name: Whitespace check\n"
        "        run: git diff --check\n",
        encoding="utf-8",
    )


def _write_gitignore_policy(root: Path) -> None:
    (root / ".gitignore").write_text(
        "# Python-generated files\n"
        "__pycache__/\n"
        ".pytest_cache/\n"
        ".ruff_cache/\n"
        "\n"
        "# Virtual environments\n"
        ".venv\n"
        "\n"
        "# Generated simulation and notebook artifacts\n"
        "runs/\n"
        "notebook-runs/\n"
        ".ipynb_checkpoints/\n"
        "*.h5\n"
        "*.hdf5\n"
        "*.traj\n"
        "*.npy\n"
        "*.npz\n"
        "*.pkl\n"
        "*.pickle\n"
        "\n"
        "# Downloaded model caches\n"
        "models/\n"
        "*.ckpt\n"
        "*.model\n"
        "*.pt\n"
        "*.pth\n",
        encoding="utf-8",
    )


def _write_pyproject_contract(root: Path) -> None:
    (root / "pyproject.toml").write_text(
        '[project]\n'
        'name = "kups-tutorial"\n'
        'version = "0.1.0"\n'
        'requires-python = ">=3.13,<3.14"\n'
        'dependencies = ["kups==1.0.3"]\n'
        '\n'
        '[project.optional-dependencies]\n'
        'gpu = ["kups[cuda]==1.0.3"]\n'
        'mlff = ["kups[hf]==1.0.3"]\n'
        '\n'
        '[project.scripts]\n'
        'kups-tutorial = "kups_md_tutorials.cli:main"\n'
        '\n'
        '[tool.ruff]\n'
        'target-version = "py313"\n',
        encoding="utf-8",
    )


def _manifest_fixture(
    post_id: str,
    profile: str,
    *,
    config_sha256: str = "a" * 64,
    lock_sha256: str = "b" * 64,
) -> dict[str, object]:
    return {
        "config": {
            "post": post_id,
            "profile": profile,
            "experiment": {"seed": 2026071400 + int(post_id)},
        },
        "provenance": {
            "config_path": f"configs/post-{post_id}/{profile}.json",
            "config_sha256": config_sha256,
            "lock_path": "uv.lock",
            "lock_sha256": lock_sha256,
            "git_revision": "c" * 40,
            "python_version": "3.13.0",
            "platform": "test",
            "runtime_device": "jax:cpu;devices:cpu",
            "precision_policy": "jax_enable_x64=false;env_JAX_ENABLE_X64=unset",
        },
        "execution": {
            "elapsed_seconds": 1.0,
            "max_full_profile_seconds": 3600,
            "measured_by": "kups_md_tutorials.workflows.run_post",
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

    (results_dir / "mlip_summary.json").write_text(summary, encoding="utf-8")
    for profile in ("smoke", "full"):
        manifest_data = _manifest_fixture(
            "12",
            profile,
            config_sha256=_sha256(config_dir / f"{profile}.json"),
            lock_sha256=_sha256(root / "uv.lock"),
        )
        manifest_data["config"]["experiment"]["model_artifact"] = {
            "revision": revision,
            "sha256": sha,
        }
        manifest_path = root / "results" / "post-12" / profile / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest_data) + "\n",
            encoding="utf-8",
        )


def _write_site_pages(site_root: Path, *, hidden: bool) -> None:
    pages = site_root / "_pages"
    posts = site_root / "_posts"
    scripts = site_root / "scripts"
    figure_dir = site_root / "assets" / "img" / "blog"
    export_dir = site_root / "assets" / "json" / "kups-md-tutorials"
    workflow_dir = site_root / ".github" / "workflows"
    pages.mkdir(parents=True)
    posts.mkdir(parents=True)
    scripts.mkdir(parents=True)
    figure_dir.mkdir(parents=True)
    workflow_dir.mkdir(parents=True)
    (workflow_dir / "deploy.yml").write_text(
        "name: Deploy site\n"
        "jobs:\n"
        "  build:\n"
        "    steps:\n"
        "      - name: Validate blog posts\n"
        "        run: python3 scripts/validate_blog.py\n"
        "      - name: Validate hidden kUPS pages\n"
        "        run: python3 scripts/validate_kups_pages.py\n"
        "      - name: Build site\n"
        "        run: bundle exec jekyll build\n",
        encoding="utf-8",
    )
    (workflow_dir / "kups-snapshots.yml").write_text(
        "name: Capture kUPS snapshots\n"
        "on:\n"
        "  workflow_dispatch:\n"
        "    inputs:\n"
        "      base_url:\n"
        "        default: https://sungsoo-ahn.github.io\n"
        "      posts:\n"
        "        default: 01,02,03,04,05,06,07,08,09,10,11,12\n"
        "jobs:\n"
        "  capture:\n"
        "    steps:\n"
        "      - name: Install Chromium\n"
        "        run: npx playwright install chromium\n"
        "      - name: Capture hidden page snapshots\n"
        "        run: |\n"
        "          node scripts/capture_kups_snapshots.js --base-url \"${{ inputs.base_url }}\" --posts \"${{ inputs.posts }}\" --output-dir snapshots/kups-md-pages\n"
        "      - name: Upload snapshots\n"
        "        uses: actions/upload-artifact@v4\n"
        "        with:\n"
        "          name: kups-md-page-snapshots\n"
        "          path: snapshots/kups-md-pages\n",
        encoding="utf-8",
    )
    (scripts / "capture_kups_snapshots.js").write_text(
        "const viewports = [\n"
        '  ["desktop", { width: 1440, height: 1200 }],\n'
        '  ["mobile", { width: 390, height: 1200, isMobile: true }],\n'
        "];\n"
        "const slugs = [\n"
        '  "/kups-md-tutorials/",\n'
        + "".join(
            f'  "/kups-md-tutorials/post-{post:02d}-example/",\n'
            for post in range(1, 13)
        )
        + "];\n"
        "async function capture(page, url) {\n"
        '  const response = await page.goto(url, { waitUntil: "networkidle" });\n'
        "  if (!response || response.status() >= 400) throw new Error(url);\n"
        "  await page.screenshot({ path: 'snapshot.png', fullPage: true });\n"
        "}\n"
        "fs.writeFileSync('manifest.json', JSON.stringify(slugs));\n",
        encoding="utf-8",
    )
    body_words = " ".join(f"sample{idx}" for idx in range(3600))
    exported_files = []
    nav = "false" if hidden else "true"
    post_collection = "site.pages" if hidden else "site.posts"
    (pages / "kups-md-tutorials.md").write_text(
        "---\n"
        "layout: page\n"
        "permalink: /kups-md-tutorials/\n"
        "title: kUPS MD Tutorials\n"
        "description: Executable molecular-dynamics tutorials for MLIP-aware machine-learning researchers.\n"
        f"nav: {nav}\n"
        "nav_order: 4\n"
        "pagination:\n"
        "  enabled: false\n"
        "---\n\n"
        '<div class="publications blog-index">\n'
        f'  {{% assign postlist = {post_collection} | where: "series", "kups-md-tutorials" | sort: "series_order" %}}\n'
        "  {% assign tutorial_count = postlist | size %}\n\n"
        "  <h1>kUPS MD Tutorials</h1>\n"
        '  <p class="blog-index-note">\n'
        "    Executable molecular-dynamics notes for ML researchers who already know MLIPs and the equations of motion.\n"
        "  </p>\n"
        '  <div class="blog-type-summary" aria-label="kUPS tutorial types">\n'
        "    <span>Post types</span>\n"
        "    <span>Tutorials {{ tutorial_count }}</span>\n"
        "    <span>Executable notes</span>\n"
        "  </div>\n\n"
        '  <ol class="bibliography">\n'
        "  {% for post in postlist %}\n"
        '    {% assign post_type = "tutorial" %}\n'
        '    {% assign post_type_label = "Tutorial" %}\n'
        "    {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}\n"
        "    <li>\n"
        '      <div class="row">\n'
        '        <div class="col-sm-10">\n'
        '          <div class="title">\n'
        '            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>\n'
        "          </div>\n"
        "          {% if post.description %}\n"
        '            <div class="blog-list-description">{{ post.description }}</div>\n'
        "          {% endif %}\n"
        '          <div class="author">\n'
        '            <span class="blog-post-type blog-post-type-{{ post_type }}">{{ post_type_label }}</span>; {{ read_time }} min read; part {{ post.series_order }} of {{ tutorial_count }}\n'
        "          </div>\n"
        "        </div>\n"
        "      </div>\n"
        "    </li>\n"
        "  {% endfor %}\n"
        "  </ol>\n"
        "</div>\n",
        encoding="utf-8",
    )
    for post in range(1, 13):
        post_id = f"{post:02d}"
        figure_path = f"assets/img/blog/kups_md_post{post_id}_diagnostics.svg"
        figure_file = site_root / figure_path
        figure_source = f"figures/post-{post_id}/example_diagnostics_full.svg"
        shutil.copyfile(site_root.parent / figure_source, figure_file)
        exported_files.append(
            {
                "post": post_id,
                "kind": "figure",
                "source": figure_source,
                "destination": figure_path,
                "sha256": _sha256(figure_file),
            }
        )
        result_path = f"assets/json/kups-md-tutorials/post-{post_id}/full/manifest.json"
        result_file = site_root / result_path
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_source = f"results/post-{post_id}/full/manifest.json"
        shutil.copyfile(site_root.parent / result_source, result_file)
        exported_files.append(
            {
                "post": post_id,
                "kind": "compact-result",
                "source": result_source,
                "destination": result_path,
                "sha256": _sha256(result_file),
            }
        )
        note_context = (
            "This page is not the final article. "
            "It is intentionally hidden from site navigation. "
            if hidden
            else "Final article. "
        )
        page_dir = pages if hidden else posts
        page_name = (
            f"kups-md-post-{post:02d}-example.md"
            if hidden
            else f"2026-07-14-kups-md-post-{post:02d}-example.md"
        )
        permalink_front_matter = (
            f"permalink: /kups-md-tutorials/post-{post_id}-example/\n"
            if hidden
            else ""
        )
        nav_front_matter = f"nav: {nav}\n" if hidden else ""
        page_front_matter = (
            "---\n"
            "layout: post\n"
            f"{permalink_front_matter}"
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
            f"{nav_front_matter}"
            "---\n\n"
        )
        (page_dir / page_name).write_text(
            page_front_matter +
            '<p style="color: #666; font-size: 0.9em; margin-bottom: 1.5em;">\n'
            f"<em>Note: {note_context}Corrections and replication issues should be tracked in "
            '<a href="https://github.com/sungsoo-ahn/kups-md-tutorials">sungsoo-ahn/kups-md-tutorials</a>.</em>\n'
            "</p>\n"
            "\n## Source Links\n\n"
            f"- [smoke configuration](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/configs/post-{post_id}/smoke.json)\n"
            f"- [full configuration](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/configs/post-{post_id}/full.json)\n"
            f"- [notebook](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/notebooks/post-{post_id}-example.ipynb)\n"
            f"- [smoke summary](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/results/post-{post_id}/smoke/example_summary.json)\n"
            f"- [full summary](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/results/post-{post_id}/full/example_summary.json)\n"
            f"- [full provenance manifest](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/results/post-{post_id}/full/manifest.json)\n"
            f"- [figure-generation source](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/scripts/generate_post{post_id}_figures.py)\n"
            f"- [self-review note](https://github.com/sungsoo-ahn/kups-md-tutorials/blob/main/reviews/post-{post_id}.md)\n"
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


def _site_post_page_path(site_root: Path, post: str) -> Path:
    matches = sorted((site_root / "_posts").glob(f"*-kups-md-post-{post}-*.md"))
    if matches:
        return matches[0]
    return site_root / "_pages" / f"kups-md-post-{post}-example.md"


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
    assert any("missing final _posts blog post" in violation for violation in result.violations)
    assert any("series index still queries hidden pages" in violation for violation in result.violations)
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


def test_release_readiness_reports_duplicate_site_pages(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    first_final_post = _site_post_page_path(tmp_path / "site", "03")
    duplicate_final_post = (
        tmp_path / "site" / "_posts" / "2026-07-14-kups-md-post-03-copy.md"
    )
    duplicate_final_post.write_text(
        first_final_post.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    _write_site_pages(tmp_path / "hidden-site", hidden=True)
    first_hidden_page = _site_post_page_path(tmp_path / "hidden-site", "04")
    duplicate_hidden_page = (
        tmp_path / "hidden-site" / "_pages" / "kups-md-post-04-copy.md"
    )
    duplicate_hidden_page.write_text(
        first_hidden_page.read_text(encoding="utf-8"),
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
    hidden_result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "hidden-site",
    )

    assert any(
        "expected one final _posts blog post for post 03, found 2" in violation
        for violation in result.violations
    )
    assert any(
        "expected one hidden _pages draft for post 04, found 2" in violation
        for violation in hidden_result.violations
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


def test_release_readiness_reports_stale_site_export_source(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    source_path = tmp_path / "figures" / "post-01" / "example_diagnostics_full.svg"
    source_path.write_text("<svg>changed source</svg>\n", encoding="utf-8")

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
        "source sha256 mismatch for figures/post-01/example_diagnostics_full.svg"
        in violation
        for violation in result.violations
    )


def test_release_readiness_reports_blog_style_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "03")
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


def test_release_readiness_reports_final_post_page_front_matter(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "03")
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        "related_posts: false\n",
        "related_posts: false\n"
        "permalink: /kups-md-tutorials/post-03-example/\n"
        "nav: false\n"
        "nav_order: 4\n"
        "pagination:\n"
        "  enabled: false\n",
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

    assert any("page-only front matter permalink" in violation for violation in result.violations)
    assert any("page-only front matter nav" in violation for violation in result.violations)
    assert any("page-only front matter nav_order" in violation for violation in result.violations)
    assert any("page-only front matter pagination" in violation for violation in result.violations)


def test_release_readiness_reports_publication_date_violations(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "03")
    text = page.read_text(encoding="utf-8")
    text = text.replace("date: 2026-07-14\n", "date: 2026-07-20\n")
    text = text.replace("last_updated: 2026-07-15\n", "last_updated: 2026-07-19\n")
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
        "_posts filename date does not match front matter date 2026-07-20"
        in violation
        for violation in result.violations
    )
    assert any(
        "last_updated 2026-07-19 predates publication date 2026-07-20"
        in violation
        for violation in result.violations
    )
    assert any(
        "must share one publication date" in violation
        and "post 03: 2026-07-20" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_missing_site_source_links(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "02")
    text = page.read_text(encoding="utf-8")
    text = text.replace("configs/post-02/smoke.json", "configs/post-99/smoke.json")
    text = text.replace("notebooks/post-02-example.ipynb", "notebooks/example.ipynb")
    text = text.replace(
        "results/post-02/smoke/example_summary.json",
        "results/post-02/smoke/example.csv",
    )
    text = text.replace(
        "results/post-02/full/example_summary.json",
        "results/post-02/full/example.csv",
    )
    text = text.replace("results/post-02/full/manifest.json", "results/post-99/full/manifest.json")
    text = text.replace("scripts/generate_post02_figures.py", "scripts/generate_post99_figures.py")
    text = text.replace("reviews/post-02.md", "reviews/post-99.md")
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

    assert any("missing smoke configuration link" in violation for violation in result.violations)
    assert any("missing notebook link" in violation for violation in result.violations)
    assert any("missing smoke compact summary link" in violation for violation in result.violations)
    assert any("missing full compact summary link" in violation for violation in result.violations)
    assert any("missing full provenance manifest link" in violation for violation in result.violations)
    assert any("missing figure-generation source link" in violation for violation in result.violations)
    assert any("missing self-review note link" in violation for violation in result.violations)


def test_release_readiness_reports_notebook_transcript_markers(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "03")
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        "sample0",
        "sample0\n\nIn [12]:\nprint('not blog prose')\n\nOut [12]:\nok\n\nexecution_count: 12\ncell_type: code",
        1,
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

    assert any("Jupyter input prompt" in violation for violation in result.violations)
    assert any("Jupyter output prompt" in violation for violation in result.violations)
    assert any("execution_count field" in violation for violation in result.violations)
    assert any("cell_type field" in violation for violation in result.violations)


def test_release_readiness_reports_series_index_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = tmp_path / "site" / "_pages" / "kups-md-tutorials.md"
    text = page.read_text(encoding="utf-8")
    text = text.replace("layout: page\n", "layout: archive\n")
    text = text.replace('<div class="publications blog-index">\n', "")
    text = text.replace(
        '{% assign postlist = site.posts | where: "series", "kups-md-tutorials" | sort: "series_order" %}\n',
        "",
    )
    text = text.replace("part {{ post.series_order }} of {{ tutorial_count }}", "")
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

    assert any("expected front matter layout: page" in violation for violation in result.violations)
    assert any("missing blog-index wrapper" in violation for violation in result.violations)
    assert any("missing series-ordered post query" in violation for violation in result.violations)
    assert any("missing series position metadata" in violation for violation in result.violations)


def test_release_readiness_reports_short_site_page(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "04")
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
    page = _site_post_page_path(tmp_path / "site", "04")
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
    page = _site_post_page_path(tmp_path / "site", "05")
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


def test_release_readiness_reports_ref_link_without_cite_anchor(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "05")
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        "sample0",
        "sample0 and a repeated [Example 05](#ref-example05) citation without a cite anchor",
        1,
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

    assert any(
        "text citation link to #ref-example05 is missing a nearby cite-* anchor"
        in violation
        for violation in result.violations
    )


def test_release_readiness_reports_site_figure_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "06")
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


def test_release_readiness_reports_site_figure_path_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "06")
    text = page.read_text(encoding="utf-8")
    text = text.replace(
        'path="assets/img/blog/kups_md_post06_diagnostics.svg"',
        'path="assets/img/blog/kups_md_post06_diagnostics.gif"',
    )
    page.write_text(text, encoding="utf-8")

    wrong_extension_result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    text = text.replace(
        'path="assets/img/blog/kups_md_post06_diagnostics.gif"',
        'path="assets/img/blog/kups_md_post07_diagnostics.svg"',
    )
    page.write_text(text, encoding="utf-8")

    wrong_post_result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any(
        "path should reference a static SVG/PNG asset" in violation
        for violation in wrong_extension_result.violations
    )
    assert any(
        "path does not identify post 06" in violation
        for violation in wrong_post_result.violations
    )


def test_release_readiness_reports_site_footnote_violations(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    page = _site_post_page_path(tmp_path / "site", "07")
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


def test_release_readiness_reports_missing_config_seed(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    config_path = tmp_path / "configs" / "post-02" / "full.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["integrator_experiment"].pop("seed")
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
        and "missing explicit fixed seed" in violation
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
    ledger["post-08"][0]["figure_files"][0] = (
        "figures/post-07/example_diagnostics.svg"
    )
    ledger["post-08"][0]["source_data"].remove("configs/post-08/full.json")
    ledger["post-08"][0]["source_data"].remove(
        "results/post-08/smoke/example_summary.json"
    )
    ledger["post-08"][0]["license"] = ""
    ledger["post-08"][0]["generator"] = "scripts/missing_post08_figures.py"
    ledger["post-08"][0]["source_url"] = "internal:scripts/other.py"
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
    assert any(
        "missing publication SVG figure source provenance for post 08" in violation
        for violation in result.violations
    )
    assert any(
        "figure file is not under figures/post-08/: figures/post-07/example_diagnostics.svg"
        in violation
        for violation in result.violations
    )
    assert any("post-08 entry 1 missing license" in violation for violation in result.violations)
    assert any("post-08 entry 1 generator does not exist" in violation for violation in result.violations)
    assert any("expected source_url internal:scripts/missing_post08_figures.py" in violation for violation in result.violations)
    assert any("missing source data configs/post-08/full.json" in violation for violation in result.violations)
    assert any("missing smoke compact summary source data" in violation for violation in result.violations)


def test_release_readiness_reports_stale_notebook_execution_ledger(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "README.md").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "fixture"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    ledger_path = tmp_path / "reviews" / "notebook-execution.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["notebooks"] = [
        entry for entry in ledger["notebooks"] if entry["post"] != "08"
    ]
    ledger.pop("execution_mode")
    ledger["notebooks"][0]["source_sha256"] = "0" * 64
    ledger["notebooks"][0]["source_sha256_after"] = "1" * 64
    ledger["notebooks"][0]["source_unchanged"] = False
    ledger["notebooks"][1]["executed_code_cells"] = 0
    ledger["notebooks"][1].pop("elapsed_seconds")
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

    assert any("source_git_revision" in violation for violation in result.violations)
    assert any("source_sha256 mismatch" in violation for violation in result.violations)
    assert any("source_sha256_after mismatch" in violation for violation in result.violations)
    assert any("source_unchanged must be true" in violation for violation in result.violations)
    assert any("expected execution_mode fresh_kernel_per_notebook" in violation for violation in result.violations)
    assert any("does not match code_cells" in violation for violation in result.violations)
    assert any("missing positive elapsed_seconds" in violation for violation in result.violations)
    assert any(
        "missing notebook execution entries for posts 08" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_stale_page_snapshot_ledger(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    ledger_path = tmp_path / "reviews" / "page-snapshots.md"
    text = ledger_path.read_text(encoding="utf-8")
    text = text.replace("- Artifact name: `kups-md-page-snapshots`.\n", "")
    text = text.replace("- `/tmp/kups-snapshots/post-index-mobile.png`\n", "")
    text = text.replace("- `/tmp/kups-snapshots/post-12-desktop.png`\n", "")
    ledger_path.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("missing rendered page snapshot kups-md-page-snapshots" in violation for violation in result.violations)
    assert any("post-index mobile" in violation for violation in result.violations)
    assert any("post-12 desktop" in violation for violation in result.violations)


def test_release_readiness_reports_snapshots_before_site_page_changes(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    site_root = tmp_path / "site"
    _write_site_pages(site_root, hidden=False)
    subprocess.run(["git", "init"], cwd=site_root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "tester@example.com"],
        cwd=site_root,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Tester"],
        cwd=site_root,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=site_root, check=True)
    subprocess.run(
        ["git", "commit", "-m", "snapshot state"],
        cwd=site_root,
        check=True,
        capture_output=True,
    )
    snapshot_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=site_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    ledger_path = tmp_path / "reviews" / "page-snapshots.md"
    ledger_path.write_text(
        ledger_path.read_text(encoding="utf-8")
        + f"\n- Website commit reviewed: `{snapshot_commit}`.\n",
        encoding="utf-8",
    )
    page_path = site_root / "_posts" / "2026-07-14-kups-md-post-01-example.md"
    page_path.write_text(
        page_path.read_text(encoding="utf-8") + "\n\nSnapshot-sensitive edit.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", str(page_path)], cwd=site_root, check=True)
    subprocess.run(
        ["git", "commit", "-m", "edit kups page"],
        cwd=site_root,
        check=True,
        capture_output=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=site_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    website_build_path = tmp_path / "reviews" / "website-build.json"
    website_build = json.loads(website_build_path.read_text(encoding="utf-8"))
    website_build["head_sha"] = head
    website_build_path.write_text(json.dumps(website_build) + "\n", encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=site_root,
    )

    assert any(
        "rendered page snapshots predate kUPS-sensitive website changes"
        in violation
        and "_posts/2026-07-14-kups-md-post-01-example.md" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_stale_website_build_ledger(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    ledger_path = tmp_path / "reviews" / "website-build.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["conclusion"] = "failure"
    ledger["validated_commands"].remove("bundle exec jekyll build")
    ledger_path.write_text(json.dumps(ledger) + "\n", encoding="utf-8")
    workflow_path = tmp_path / "site" / ".github" / "workflows" / "deploy.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow_text.replace("python3 scripts/validate_kups_pages.py", ""),
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

    assert any("expected conclusion 'success'" in violation for violation in result.violations)
    assert any("missing validated command bundle exec jekyll build" in violation for violation in result.violations)
    assert any(
        "missing release validation command python3 scripts/validate_kups_pages.py"
        in violation
        for violation in result.violations
    )


def test_release_readiness_reports_stale_site_snapshot_capture(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    workflow_path = tmp_path / "site" / ".github" / "workflows" / "kups-snapshots.yml"
    workflow_text = workflow_path.read_text(encoding="utf-8")
    workflow_path.write_text(
        workflow_text.replace("name: kups-md-page-snapshots", "name: snapshots"),
        encoding="utf-8",
    )
    script_path = tmp_path / "site" / "scripts" / "capture_kups_snapshots.js"
    script_text = script_path.read_text(encoding="utf-8")
    script_text = script_text.replace(
        '  ["mobile", { width: 390, height: 1200, isMobile: true }],\n',
        "",
    )
    script_text = script_text.replace("fullPage: true", "fullPage: false")
    script_path.write_text(script_text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("missing kUPS snapshot snapshot artifact name" in violation for violation in result.violations)
    assert any("missing kUPS snapshot mobile viewport" in violation for violation in result.violations)
    assert any("missing kUPS snapshot full-page capture" in violation for violation in result.violations)


def test_release_readiness_reports_stale_ci_workflow(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    workflow_path = tmp_path / ".github" / "workflows" / "verify.yml"
    text = workflow_path.read_text(encoding="utf-8")
    text = text.replace(
        "uv run kups-tutorial run-all --profile smoke",
        "uv run kups-tutorial run-all --profile full",
    )
    text = text.replace(
        "uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers",
        "uv run kups-tutorial verify-release-readiness --skip-site",
    )
    text = text.replace("uv run kups-tutorial verify-notebooks", "uv run pytest")
    workflow_path.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("missing CI smoke reproduction" in violation for violation in result.violations)
    assert any("missing CI release-surface audit" in violation for violation in result.violations)
    assert any("missing CI clean notebook execution" in violation for violation in result.violations)


def test_release_readiness_reports_misordered_ci_workflow(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    workflow_path = tmp_path / ".github" / "workflows" / "verify.yml"
    text = workflow_path.read_text(encoding="utf-8")
    review_step = (
        "      - name: Audit review notes\n"
        "        run: uv run kups-tutorial verify-reviews\n"
    )
    release_step = (
        "      - name: Audit release surface\n"
        "        run: uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers\n"
    )
    text = text.replace(review_step + release_step, release_step + review_step)
    workflow_path.write_text(text, encoding="utf-8")

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
        "CI review audit must run before release-surface audit" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_full_verification_before_smoke(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    workflow_path = tmp_path / ".github" / "workflows" / "verify.yml"
    text = workflow_path.read_text(encoding="utf-8")
    smoke_step = (
        "      - name: Verify smoke outputs\n"
        "        run: uv run kups-tutorial verify --profile smoke --output-dir /tmp/kups-md-smoke\n"
    )
    full_step = (
        "      - name: Verify committed full outputs\n"
        "        run: uv run kups-tutorial verify --profile full\n"
    )
    text = text.replace(smoke_step + full_step, full_step + smoke_step)
    workflow_path.write_text(text, encoding="utf-8")

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
        "CI smoke verification must run before committed full verification"
        in violation
        for violation in result.violations
    )


def test_release_readiness_reports_stale_gitignore_policy(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    gitignore_path = tmp_path / ".gitignore"
    text = gitignore_path.read_text(encoding="utf-8")
    text = text.replace("*.h5\n", "")
    text = text.replace("*.model\n", "")
    text = text.replace(".ruff_cache/\n", "")
    gitignore_path.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("missing artifact ignore pattern *.h5" in violation for violation in result.violations)
    assert any("missing artifact ignore pattern *.model" in violation for violation in result.violations)
    assert any("missing artifact ignore pattern .ruff_cache/" in violation for violation in result.violations)


def test_release_readiness_reports_stale_pyproject_contract(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    pyproject_path = tmp_path / "pyproject.toml"
    text = pyproject_path.read_text(encoding="utf-8")
    text = text.replace('requires-python = ">=3.13,<3.14"', 'requires-python = ">=3.12"')
    text = text.replace('"kups==1.0.3"', '"kups>=1.0"')
    text = text.replace('"kups[cuda]==1.0.3"', '"kups[cuda]>=1.0"')
    text = text.replace('"kups[hf]==1.0.3"', '"kups[hf]>=1.0"')
    text = text.replace(
        'kups-tutorial = "kups_md_tutorials.cli:main"',
        'kups-tutorial = "kups_md_tutorials.cli:broken"',
    )
    text = text.replace('target-version = "py313"', 'target-version = "py312"')
    pyproject_path.write_text(text, encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("expected requires-python >=3.13,<3.14" in violation for violation in result.violations)
    assert any("missing pinned dependency kups==1.0.3" in violation for violation in result.violations)
    assert any("missing gpu extra kups[cuda]==1.0.3" in violation for violation in result.violations)
    assert any("missing mlff extra kups[hf]==1.0.3" in violation for violation in result.violations)
    assert any("expected kups-tutorial script" in violation for violation in result.violations)
    assert any("expected Ruff target-version py313" in violation for violation in result.violations)


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


def test_release_readiness_reports_stale_manifest_file_hashes(tmp_path: Path) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    manifest_path = tmp_path / "results" / "post-04" / "full" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["provenance"]["config_sha256"] = "0" * 64
    manifest["provenance"]["lock_sha256"] = "1" * 64
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

    assert any(
        "provenance config_sha256 mismatch" in violation
        for violation in result.violations
    )
    assert any(
        "provenance lock_sha256 mismatch" in violation
        for violation in result.violations
    )


def test_release_readiness_reports_stale_manifest_execution_timing(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    smoke_manifest_path = tmp_path / "results" / "post-03" / "smoke" / "manifest.json"
    smoke_manifest = json.loads(smoke_manifest_path.read_text(encoding="utf-8"))
    smoke_manifest.pop("execution")
    smoke_manifest_path.write_text(json.dumps(smoke_manifest) + "\n", encoding="utf-8")

    full_manifest_path = tmp_path / "results" / "post-03" / "full" / "manifest.json"
    full_manifest = json.loads(full_manifest_path.read_text(encoding="utf-8"))
    full_manifest["execution"]["elapsed_seconds"] = 3600.1
    full_manifest_path.write_text(json.dumps(full_manifest) + "\n", encoding="utf-8")

    result = audit_release_readiness(
        review_dir=tmp_path / "reviews",
        config_root=tmp_path / "configs",
        results_root=tmp_path / "results",
        notebook_root=tmp_path / "notebooks",
        figure_root=tmp_path / "figures",
        snapshot_root=tmp_path / "snapshots",
        site_root=tmp_path / "site",
    )

    assert any("missing execution timing metadata" in violation for violation in result.violations)
    assert any(
        "full-profile execution elapsed_seconds 3600.1 exceeds max_full_profile_seconds 3600"
        in violation
        for violation in result.violations
    )


def test_release_readiness_reports_manifest_output_file_violations(
    tmp_path: Path,
) -> None:
    _write_clean_reviews(tmp_path / "reviews")
    _write_required_artifacts(tmp_path)
    _write_site_pages(tmp_path / "site", hidden=False)
    manifest_path = tmp_path / "results" / "post-04" / "full" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["summary_file"] = "missing_summary.json"
    manifest["samples_file"] = "../escaped.csv"
    manifest["raw_trajectory_file"] = "trajectory.traj"
    manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
    (manifest_path.parent / "trajectory.traj").write_text("raw\n", encoding="utf-8")

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
        "manifest summary_file does not exist: missing_summary.json" in violation
        for violation in result.violations
    )
    assert any(
        "manifest samples_file escapes result directory" in violation
        for violation in result.violations
    )
    assert any(
        "manifest raw_trajectory_file should reference compact output" in violation
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
