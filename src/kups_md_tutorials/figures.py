"""Figure generation for tutorial posts."""

from pathlib import Path
import json

from ase.io import read
import matplotlib.pyplot as plt
from matplotlib import rc_context
import numpy as np


def _standardize(values: np.ndarray) -> np.ndarray:
    centered = values - np.mean(values)
    scale = np.std(centered, ddof=1)
    if scale == 0.0:
        msg = "cannot standardize values with zero variance"
        raise ValueError(msg)
    return centered / scale


def _strip_trailing_whitespace(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def generate_post01_figures(
    result_dir: Path = Path("results/post-01/smoke"),
    figure_dir: Path = Path("figures/post-01"),
    snapshot_dir: Path = Path("snapshots/post-01"),
    name: str = "initialization_diagnostics",
) -> list[Path]:
    """Generate initialization diagnostic figures and review snapshots."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    atoms = read(result_dir / "initial_state.extxyz")
    summary = json.loads((result_dir / "initialization_summary.json").read_text())
    positions = atoms.get_positions()
    velocities = atoms.get_velocities()
    standardized_velocities = _standardize(velocities.reshape(-1))

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-01"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post01_figure(fig, axes, atoms, summary, positions, standardized_velocities)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def _draw_post01_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    atoms,
    summary: dict,
    positions: np.ndarray,
    standardized_velocities: np.ndarray,
) -> None:
    fig.patch.set_facecolor("white")

    axes[0].scatter(
        positions[:, 0],
        positions[:, 1],
        s=32,
        color="#2f6f9f",
        edgecolor="#18384f",
        linewidth=0.45,
    )
    cell = atoms.cell.lengths()
    axes[0].set_xlim(-0.04 * cell[0], 1.04 * cell[0])
    axes[0].set_ylim(-0.04 * cell[1], 1.04 * cell[1])
    axes[0].set_aspect("equal")
    axes[0].set_title("FCC argon cell projection")
    axes[0].set_xlabel("x (angstrom)")
    axes[0].set_ylabel("y (angstrom)")
    axes[0].text(
        0.02,
        0.98,
        f"N = {len(atoms)}\n"
        f"rho = {summary['number_density']:.4f} atoms/angstrom^3",
        transform=axes[0].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    bins = np.linspace(-3.5, 3.5, 18)
    axes[1].hist(
        standardized_velocities,
        bins=bins,
        density=True,
        color="#d88c3d",
        edgecolor="#784714",
        linewidth=0.45,
        alpha=0.82,
    )
    x = np.linspace(-3.5, 3.5, 300)
    axes[1].plot(
        x,
        np.exp(-0.5 * x**2) / np.sqrt(2.0 * np.pi),
        color="#222222",
        linewidth=1.5,
        label="standard normal",
    )
    axes[1].set_title("Seeded velocity draw")
    axes[1].set_xlabel("standardized velocity component")
    axes[1].set_ylabel("density")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].text(
        0.02,
        0.98,
        f"target T = {summary['target_temperature_k']:.1f} K\n"
        f"sample T = {summary['instantaneous_temperature_k']:.1f} K",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    axes[2].set_title("Initialization checks")
    axes[2].axis("off")
    checks = [
        ("density from cell", f"{summary['number_density']:.4f} atoms/angstrom^3"),
        ("seed", str(summary["seed"])),
        ("COM speed", f"{summary['center_of_mass_speed']:.2e}"),
        ("config hash", summary["config_sha256"][:12]),
    ]
    for idx, (label, value) in enumerate(checks):
        y = 0.84 - idx * 0.2
        axes[2].scatter(
            0.05,
            y,
            s=150,
            marker="o",
            color="#6a8f4e",
            edgecolor="#2d4721",
            transform=axes[2].transAxes,
        )
        axes[2].text(
            0.05,
            y,
            "ok",
            transform=axes[2].transAxes,
            va="center",
            ha="center",
            fontsize=7,
            color="white",
            fontweight="bold",
        )
        axes[2].text(
            0.13,
            y + 0.045,
            label,
            transform=axes[2].transAxes,
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )
        axes[2].text(
            0.13,
            y - 0.035,
            value,
            transform=axes[2].transAxes,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
            color="#111111",
        )

    for ax in axes[:2]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)
