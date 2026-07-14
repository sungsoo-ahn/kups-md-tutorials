"""Generate post 09 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post09_figures


def main() -> None:
    """Generate figures for available post 09 result profiles."""

    generate_post09_figures(
        result_dir=Path("results/post-09/smoke"),
        figure_dir=Path("figures/post-09"),
        snapshot_dir=Path("snapshots/post-09"),
        name="estimator_diagnostics",
    )
    full_result_dir = Path("results/post-09/full")
    if full_result_dir.exists():
        generate_post09_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-09"),
            snapshot_dir=Path("snapshots/post-09"),
            name="estimator_diagnostics_full",
        )


if __name__ == "__main__":
    main()
