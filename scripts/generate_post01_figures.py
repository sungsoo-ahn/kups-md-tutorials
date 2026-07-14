"""Generate publication figures for post 01."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post01_figures


def main() -> None:
    generate_post01_figures(
        result_dir=Path("results/post-01/smoke"),
        figure_dir=Path("figures/post-01"),
        snapshot_dir=Path("snapshots/post-01"),
    )


if __name__ == "__main__":
    main()
