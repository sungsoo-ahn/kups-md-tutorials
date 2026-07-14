"""Generate post 06 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post06_figures


def main() -> None:
    """Generate figures for available post 06 result profiles."""

    generate_post06_figures(
        result_dir=Path("results/post-06/smoke"),
        figure_dir=Path("figures/post-06"),
        snapshot_dir=Path("snapshots/post-06"),
        name="trajectory_length_diagnostics",
    )
    full_result_dir = Path("results/post-06/full")
    if full_result_dir.exists():
        generate_post06_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-06"),
            snapshot_dir=Path("snapshots/post-06"),
            name="trajectory_length_diagnostics_full",
        )


if __name__ == "__main__":
    main()
