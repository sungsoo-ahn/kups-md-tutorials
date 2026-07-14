"""Generate post 11 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post11_figures


def main() -> None:
    """Generate figures for available post 11 result profiles."""

    generate_post11_figures(
        result_dir=Path("results/post-11/smoke"),
        figure_dir=Path("figures/post-11"),
        snapshot_dir=Path("snapshots/post-11"),
        name="enhanced_sampling_diagnostics",
    )
    full_result_dir = Path("results/post-11/full")
    if full_result_dir.exists():
        generate_post11_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-11"),
            snapshot_dir=Path("snapshots/post-11"),
            name="enhanced_sampling_diagnostics_full",
        )


if __name__ == "__main__":
    main()
