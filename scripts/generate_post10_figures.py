"""Generate post 10 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post10_figures


def main() -> None:
    """Generate figures for available post 10 result profiles."""

    generate_post10_figures(
        result_dir=Path("results/post-10/smoke"),
        figure_dir=Path("figures/post-10"),
        snapshot_dir=Path("snapshots/post-10"),
        name="umbrella_diagnostics",
    )
    full_result_dir = Path("results/post-10/full")
    if full_result_dir.exists():
        generate_post10_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-10"),
            snapshot_dir=Path("snapshots/post-10"),
            name="umbrella_diagnostics_full",
        )


if __name__ == "__main__":
    main()
