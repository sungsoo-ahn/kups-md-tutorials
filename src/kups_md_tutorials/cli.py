"""Command-line interface for tutorial experiments."""

import argparse
from collections.abc import Sequence
from pathlib import Path

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

    subparsers.add_parser("export-site", help="export compact assets for the site")
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
    except Exception as exc:
        parser.exit(1, f"{exc}\n")

    parser.exit(2, f"{args.command} is not implemented yet.\n")
