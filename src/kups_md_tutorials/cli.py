"""Command-line interface for tutorial experiments."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from kups_md_tutorials.artifact_audit import verify_tracked_artifacts
from kups_md_tutorials.release_readiness import verify_release_readiness
from kups_md_tutorials.review_audit import verify_reviews
from kups_md_tutorials.site_export import export_site_assets
from kups_md_tutorials.workflows import run_all, run_post, verify_all, verify_post


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kups-tutorial")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run one tutorial experiment")
    run.add_argument("post", help="tutorial identifier, such as 01")
    run.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    run.add_argument("--output-dir", type=Path, default=Path("results"))

    run_all = subparsers.add_parser("run-all", help="run all tutorial experiments")
    run_all.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    run_all.add_argument("--output-dir", type=Path, default=Path("results"))

    verify = subparsers.add_parser("verify", help="verify generated summaries")
    verify.add_argument("post", nargs="?", help="tutorial identifier, such as 01")
    verify.add_argument("--profile", choices=("smoke", "full"), default="smoke")
    verify.add_argument("--output-dir", type=Path, default=Path("results"))

    subparsers.add_parser(
        "verify-artifacts",
        help="verify tracked files do not include raw trajectories, caches, or models",
    )
    review_parser = subparsers.add_parser(
        "verify-reviews",
        help="verify post self-review notes contain required evidence",
    )
    review_parser.add_argument("--review-dir", type=Path, default=Path("reviews"))

    release_parser = subparsers.add_parser(
        "verify-release-readiness",
        help="verify no final-release blockers remain before public publication",
    )
    release_parser.add_argument("--review-dir", type=Path, default=Path("reviews"))
    release_parser.add_argument("--config-root", type=Path, default=Path("configs"))
    release_parser.add_argument("--results-root", type=Path, default=Path("results"))
    release_parser.add_argument("--notebook-root", type=Path, default=Path("notebooks"))
    release_parser.add_argument("--figure-root", type=Path, default=Path("figures"))
    release_parser.add_argument("--snapshot-root", type=Path, default=Path("snapshots"))
    release_parser.add_argument(
        "--site-root",
        type=Path,
        default=Path("../sungsoo-ahn.github.io"),
        help="website repository root; use --skip-site to omit page publication checks",
    )
    release_parser.add_argument(
        "--skip-site",
        action="store_true",
        help="skip website hidden/non-final page checks",
    )

    export_site = subparsers.add_parser(
        "export-site", help="export compact assets for the site"
    )
    export_site.add_argument(
        "--site-root",
        type=Path,
        default=Path("../sungsoo-ahn.github.io"),
    )
    export_site.add_argument("--profile", choices=("smoke", "full"), default="full")
    export_site.add_argument("--results-dir", type=Path, default=Path("results"))
    export_site.add_argument("--figures-dir", type=Path, default=Path("figures"))
    export_site.add_argument(
        "--posts",
        help="comma-separated post identifiers to export, such as 01,02",
    )

    verify_notebooks = subparsers.add_parser(
        "verify-notebooks", help="execute tutorial notebooks from clean kernels"
    )
    verify_notebooks.add_argument("--notebooks-dir", type=Path, default=Path("notebooks"))
    verify_notebooks.add_argument("--output-dir", type=Path, default=Path("notebook-runs"))
    verify_notebooks.add_argument("--kernel-name", default="python3")
    verify_notebooks.add_argument("--timeout", type=int, default=120)
    verify_notebooks.add_argument(
        "--posts",
        help="comma-separated post identifiers to execute, such as 01,02",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            output_dir = run_post(args.post, args.profile, output_root=args.output_dir)
            print(f"Wrote {output_dir}")
            return 0
        if args.command == "run-all":
            output_dirs = run_all(args.profile, output_root=args.output_dir)
            for output_dir in output_dirs:
                print(f"Wrote {output_dir}")
            return 0
        if args.command == "verify":
            if args.post is None:
                verify_all(args.profile, output_root=args.output_dir)
            else:
                verify_post(args.post, args.profile, output_root=args.output_dir)
            print("Verification passed")
            return 0
        if args.command == "verify-artifacts":
            result = verify_tracked_artifacts(repo_root=Path.cwd())
            print(f"Artifact audit passed for {result.tracked_file_count} tracked files")
            return 0
        if args.command == "verify-reviews":
            result = verify_reviews(review_dir=args.review_dir)
            print(f"Review audit passed for {result.reviewed_posts} posts")
            return 0
        if args.command == "verify-release-readiness":
            site_root = None if args.skip_site else args.site_root
            result = verify_release_readiness(
                review_dir=args.review_dir,
                config_root=args.config_root,
                results_root=args.results_root,
                notebook_root=args.notebook_root,
                figure_root=args.figure_root,
                snapshot_root=args.snapshot_root,
                site_root=site_root,
            )
            print(f"Release readiness audit passed for {result.checked_posts} posts")
            return 0
        if args.command == "export-site":
            posts = None
            if args.posts:
                posts = tuple(post.strip().zfill(2) for post in args.posts.split(","))
            manifest_path = export_site_assets(
                site_root=args.site_root,
                profile=args.profile,
                results_root=args.results_dir,
                figures_root=args.figures_dir,
                posts=posts,
            )
            print(f"Wrote {manifest_path}")
            return 0
        if args.command == "verify-notebooks":
            from kups_md_tutorials.notebook_execution import execute_notebooks

            posts = None
            if args.posts:
                posts = tuple(post.strip().zfill(2) for post in args.posts.split(","))
            manifest_path = execute_notebooks(
                notebooks_dir=args.notebooks_dir,
                output_dir=args.output_dir,
                posts=posts,
                kernel_name=args.kernel_name,
                timeout_seconds=args.timeout,
                cwd=Path.cwd(),
            )
            print(f"Notebook verification passed; wrote {manifest_path}")
            return 0
    except Exception as exc:
        parser.exit(1, f"{exc}\n")

    parser.exit(2, f"{args.command} is not implemented yet.\n")
