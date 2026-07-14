"""Generate post 12 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post12_figures


def main() -> None:
    """Generate figures for available post 12 result profiles."""

    generate_post12_figures(
        result_dir=Path("results/post-12/smoke"),
        figure_dir=Path("figures/post-12"),
        snapshot_dir=Path("snapshots/post-12"),
        name="mlip_diagnostics",
    )
    full_result_dir = Path("results/post-12/full")
    if full_result_dir.exists():
        generate_post12_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-12"),
            snapshot_dir=Path("snapshots/post-12"),
            name="mlip_diagnostics_full",
        )


if __name__ == "__main__":
    main()
