"""Generate post 02 figures and review snapshots."""

from pathlib import Path

from kups_md_tutorials.figures import generate_post02_figures


def main() -> None:
    """Generate figures for available post 02 result profiles."""

    generate_post02_figures(
        result_dir=Path("results/post-02/smoke"),
        figure_dir=Path("figures/post-02"),
        snapshot_dir=Path("snapshots/post-02"),
        name="integrator_diagnostics",
    )
    full_result_dir = Path("results/post-02/full")
    if full_result_dir.exists():
        generate_post02_figures(
            result_dir=full_result_dir,
            figure_dir=Path("figures/post-02"),
            snapshot_dir=Path("snapshots/post-02"),
            name="integrator_diagnostics_full",
        )


if __name__ == "__main__":
    main()
