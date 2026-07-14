"""Command-line interface for tutorial experiments."""

import argparse
from collections.abc import Sequence


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kups-tutorial")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run one tutorial experiment")
    run.add_argument("post", help="tutorial identifier, such as 01")
    run.add_argument("--profile", choices=("smoke", "full"), default="smoke")

    run_all = subparsers.add_parser("run-all", help="run all tutorial experiments")
    run_all.add_argument("--profile", choices=("smoke", "full"), default="smoke")

    verify = subparsers.add_parser("verify", help="verify generated summaries")
    verify.add_argument("--profile", choices=("smoke", "full"), default="smoke")

    subparsers.add_parser("export-site", help="export compact assets for the site")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    parser.exit(2, f"{args.command} is not implemented yet.\n")
