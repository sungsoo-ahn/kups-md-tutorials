"""Generate post 04 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post04_figures


def main() -> None:
    """Generate figures for available post 04 result profiles."""

    generate_post04_figures(
        result_dir=Path("results/post-04/smoke"),
        figure_dir=Path("figures/post-04"),
        snapshot_dir=Path("snapshots/post-04"),
        name="thermostat_diagnostics",
    )
    full_result_dir = Path("results/post-04/full")
    if full_result_dir.exists():
        generate_post04_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-04"),
            snapshot_dir=Path("snapshots/post-04"),
            name="thermostat_diagnostics_full",
        )


if __name__ == "__main__":
    main()
