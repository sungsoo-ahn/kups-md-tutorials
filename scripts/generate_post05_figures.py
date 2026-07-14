"""Generate post 05 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post05_figures


def main() -> None:
    """Generate figures for available post 05 result profiles."""

    generate_post05_figures(
        result_dir=Path("results/post-05/smoke"),
        figure_dir=Path("figures/post-05"),
        snapshot_dir=Path("snapshots/post-05"),
        name="barostat_diagnostics",
    )
    full_result_dir = Path("results/post-05/full")
    if full_result_dir.exists():
        generate_post05_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-05"),
            snapshot_dir=Path("snapshots/post-05"),
            name="barostat_diagnostics_full",
        )


if __name__ == "__main__":
    main()
