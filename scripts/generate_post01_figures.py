"""Generate publication figures for post 01."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post01_figures


def main() -> None:
    generate_post01_figures(
        result_dir=Path("results/post-01/smoke"),
        figure_dir=Path("figures/post-01"),
        snapshot_dir=Path("snapshots/post-01"),
        name="initialization_diagnostics",
    )
    full_result_dir = Path("results/post-01/full")
    if full_result_dir.exists():
        generate_post01_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-01"),
            snapshot_dir=Path("snapshots/post-01"),
            name="initialization_diagnostics_full",
        )


if __name__ == "__main__":
    main()
