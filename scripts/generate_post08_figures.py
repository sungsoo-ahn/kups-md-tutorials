"""Generate post 08 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post08_figures


def main() -> None:
    """Generate figures for available post 08 result profiles."""

    generate_post08_figures(
        result_dir=Path("results/post-08/smoke"),
        figure_dir=Path("figures/post-08"),
        snapshot_dir=Path("snapshots/post-08"),
        name="free_energy_diagnostics",
    )
    full_result_dir = Path("results/post-08/full")
    if full_result_dir.exists():
        generate_post08_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-08"),
            snapshot_dir=Path("snapshots/post-08"),
            name="free_energy_diagnostics_full",
        )


if __name__ == "__main__":
    main()
