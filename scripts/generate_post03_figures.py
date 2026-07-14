"""Generate post 03 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post03_figures


def main() -> None:
    """Generate figures for available post 03 result profiles."""

    generate_post03_figures(
        result_dir=Path("results/post-03/smoke"),
        figure_dir=Path("figures/post-03"),
        snapshot_dir=Path("snapshots/post-03"),
        name="error_diagnostics",
    )
    full_result_dir = Path("results/post-03/full")
    if full_result_dir.exists():
        generate_post03_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-03"),
            snapshot_dir=Path("snapshots/post-03"),
            name="error_diagnostics_full",
        )


if __name__ == "__main__":
    main()
