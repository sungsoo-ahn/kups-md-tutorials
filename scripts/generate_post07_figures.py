"""Generate post 07 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post07_figures


def main() -> None:
    """Generate figures for available post 07 result profiles."""

    generate_post07_figures(
        result_dir=Path("results/post-07/smoke"),
        figure_dir=Path("figures/post-07"),
        snapshot_dir=Path("snapshots/post-07"),
        name="observable_diagnostics",
    )
    full_result_dir = Path("results/post-07/full")
    if full_result_dir.exists():
        generate_post07_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-07"),
            snapshot_dir=Path("snapshots/post-07"),
            name="observable_diagnostics_full",
        )


if __name__ == "__main__":
    main()
