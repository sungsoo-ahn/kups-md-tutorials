"""Figure generation for tutorial posts."""

from pathlib import Path
import json
import csv

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


def generate_post02_figures(
    result_dir: Path = Path("results/post-02/smoke"),
    figure_dir: Path = Path("figures/post-02"),
    snapshot_dir: Path = Path("snapshots/post-02"),
    name: str = "integrator_diagnostics",
) -> list[Path]:
    """Generate harmonic-oscillator integrator diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "integrator_summary.json").read_text())
    samples = _read_post02_samples(result_dir / "trajectory_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-02"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post02_figure(fig, axes, summary, samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post03_figures(
    result_dir: Path = Path("results/post-03/smoke"),
    figure_dir: Path = Path("figures/post-03"),
    snapshot_dir: Path = Path("snapshots/post-03"),
    name: str = "error_diagnostics",
) -> list[Path]:
    """Generate timestep, precision, and force-error diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "error_summary.json").read_text())
    samples = _read_post03_samples(result_dir / "error_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-03"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post03_figure(fig, axes, summary, samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post04_figures(
    result_dir: Path = Path("results/post-04/smoke"),
    figure_dir: Path = Path("figures/post-04"),
    snapshot_dir: Path = Path("snapshots/post-04"),
    name: str = "thermostat_diagnostics",
) -> list[Path]:
    """Generate thermostat sampling and dynamics diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "thermostat_summary.json").read_text())
    samples = _read_post04_samples(result_dir / "thermostat_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-04"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post04_figure(fig, axes, summary, samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post05_figures(
    result_dir: Path = Path("results/post-05/smoke"),
    figure_dir: Path = Path("figures/post-05"),
    snapshot_dir: Path = Path("snapshots/post-05"),
    name: str = "barostat_diagnostics",
) -> list[Path]:
    """Generate pressure and scalar-cell diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "barostat_summary.json").read_text())
    samples = _read_post05_samples(result_dir / "barostat_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-05"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post05_figure(fig, axes, summary, samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post06_figures(
    result_dir: Path = Path("results/post-06/smoke"),
    figure_dir: Path = Path("figures/post-06"),
    snapshot_dir: Path = Path("snapshots/post-06"),
    name: str = "trajectory_length_diagnostics",
) -> list[Path]:
    """Generate trajectory length and uncertainty diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "trajectory_length_summary.json").read_text())
    samples = _read_post06_samples(result_dir / "trajectory_length_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-06"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post06_figure(fig, axes, summary, samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post07_figures(
    result_dir: Path = Path("results/post-07/smoke"),
    figure_dir: Path = Path("figures/post-07"),
    snapshot_dir: Path = Path("snapshots/post-07"),
    name: str = "observable_diagnostics",
) -> list[Path]:
    """Generate RDF, coordination, and VACF diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "observable_summary.json").read_text())
    rdf_samples = _read_post07_samples(result_dir / "rdf_samples.csv")
    vacf_samples = _read_post07_samples(result_dir / "vacf_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-07"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post07_figure(fig, axes, summary, rdf_samples, vacf_samples)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post08_figures(
    result_dir: Path = Path("results/post-08/smoke"),
    figure_dir: Path = Path("figures/post-08"),
    snapshot_dir: Path = Path("snapshots/post-08"),
    name: str = "free_energy_diagnostics",
) -> list[Path]:
    """Generate PMF, binning, reweighting, and RDF-PMF figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "free_energy_summary.json").read_text())
    curves = _read_post08_curves(result_dir / "free_energy_curves.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-08"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post08_figure(fig, axes, summary, curves)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def _read_post02_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post03_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post04_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post05_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post06_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post07_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


def _read_post08_curves(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    curves: dict[str, np.ndarray] = {}
    for key in reader.fieldnames or []:
        values = [float(row[key]) for row in rows if row[key]]
        curves[key] = np.array(values, dtype=float)
    return curves


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


def _draw_post02_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")

    axes[0].plot(
        samples["exact_position"],
        samples["exact_velocity"],
        color="#222222",
        linewidth=1.5,
        label="exact",
    )
    axes[0].plot(
        samples["position"],
        samples["velocity"],
        color="#2f6f9f",
        linewidth=1.2,
        linestyle="--",
        label="velocity Verlet",
    )
    axes[0].set_title("Phase-space orbit")
    axes[0].set_xlabel("position")
    axes[0].set_ylabel("velocity")
    axes[0].set_aspect("equal", adjustable="box")
    axes[0].legend(frameon=False, fontsize=8)

    runs = summary["runs"]
    grouped: dict[str, list[dict]] = {}
    for run in runs:
        grouped.setdefault(run["integrator"], []).append(run)

    colors = {"velocity_verlet": "#2f6f9f", "explicit_euler": "#d88c3d"}
    for integrator, run_group in grouped.items():
        sorted_runs = sorted(run_group, key=lambda run: run["time_step"])
        axes[1].plot(
            [run["time_step"] for run in sorted_runs],
            [run["max_abs_relative_energy_error"] for run in sorted_runs],
            marker="o",
            linewidth=1.4,
            color=colors.get(integrator, "#555555"),
            label=integrator.replace("_", " "),
        )
    axes[1].set_title("Energy error is scheme-dependent")
    axes[1].set_xlabel("time step")
    axes[1].set_ylabel("max |Delta E| / E0")
    axes[1].set_yscale("log")
    axes[1].legend(frameon=False, fontsize=8)

    reference = grouped["velocity_verlet"]
    labels = [f"dt={run['time_step']:.2g}" for run in reference]
    axes[2].bar(
        np.arange(len(reference)),
        [run["reversibility_error"] for run in reference],
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    axes[2].set_title("Forward/backward check")
    axes[2].set_ylabel("state error")
    axes[2].set_xticks(np.arange(len(reference)))
    axes[2].set_xticklabels(labels, rotation=25, ha="right")
    axes[2].set_yscale("log")
    axes[2].text(
        0.03,
        0.95,
        "velocity Verlet returns to the initial state\n"
        "up to floating-point roundoff after velocity reversal",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post03_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")

    runs = summary["runs"]
    exact_float64 = sorted(
        [
            run
            for run in runs
            if run["force_case"] == "exact_force" and run["precision"] == "float64"
        ],
        key=lambda run: run["time_step"],
    )
    axes[0].plot(
        [run["time_step"] for run in exact_float64],
        [run["max_abs_relative_energy_error"] for run in exact_float64],
        marker="o",
        color="#2f6f9f",
        linewidth=1.5,
    )
    axes[0].set_title("Timestep controls bounded error")
    axes[0].set_xlabel("time step")
    axes[0].set_ylabel("max |Delta E| / E0")
    axes[0].set_yscale("log")

    largest_dt = max(run["time_step"] for run in runs)
    exact_largest = [
        run
        for run in runs
        if run["force_case"] == "exact_force" and run["time_step"] == largest_dt
    ]
    exact_largest = sorted(exact_largest, key=lambda run: _precision_sort_key(run["precision"]))
    axes[1].bar(
        np.arange(len(exact_largest)),
        [run["max_abs_relative_energy_error"] for run in exact_largest],
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    axes[1].set_title("Precision can set an error floor")
    axes[1].set_ylabel("max |Delta E| / E0")
    axes[1].set_yscale("log")
    axes[1].set_xticks(np.arange(len(exact_largest)))
    axes[1].set_xticklabels(
        [run["precision"].replace("_", "\n") for run in exact_largest],
        fontsize=8,
    )

    force_runs = sorted(
        [
            run
            for run in runs
            if run["precision"] == "float64" and run["time_step"] == largest_dt
        ],
        key=lambda run: run["force_scale"],
    )
    axes[2].axhline(0.0, color="#333333", linewidth=0.8)
    axes[2].bar(
        np.arange(len(force_runs)),
        [run["normalized_energy_drift"] for run in force_runs],
        color="#d88c3d",
        edgecolor="#784714",
        linewidth=0.6,
    )
    axes[2].set_title("Force bias appears as drift")
    axes[2].set_ylabel("Delta E / (E0 time)")
    axes[2].set_xticks(np.arange(len(force_runs)))
    axes[2].set_xticklabels(
        [run["force_case"].replace("_", "\n") for run in force_runs],
        fontsize=8,
    )

    axes[0].text(
        0.03,
        0.95,
        f"N = {len(runs)} runs\nfull grid: dt, precision, force scale",
        transform=axes[0].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _precision_sort_key(precision: str) -> tuple[int, float]:
    if precision == "float64":
        return (0, 0.0)
    if precision == "float32":
        return (1, 0.0)
    if precision.startswith("rounded_"):
        return (2, float(precision.removeprefix("rounded_")))
    return (3, 0.0)


def _draw_post04_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")

    runs = sorted(summary["runs"], key=lambda run: run["gamma"])
    labels = [run["thermostat"].replace("_", "\n") for run in runs]
    x = np.arange(len(runs))

    axes[0].axhline(1.0, color="#333333", linewidth=0.9, label="canonical target")
    axes[0].plot(
        x,
        [run["position_variance"] / run["expected_position_variance"] for run in runs],
        marker="o",
        color="#2f6f9f",
        linewidth=1.5,
        label="position variance",
    )
    axes[0].plot(
        x,
        [run["velocity_variance"] / run["expected_velocity_variance"] for run in runs],
        marker="s",
        color="#d88c3d",
        linewidth=1.5,
        label="velocity variance",
    )
    axes[0].set_title("Canonical variance check")
    axes[0].set_ylabel("observed / expected")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=8)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].axhline(1.0, color="#333333", linewidth=0.9)
    axes[1].bar(
        x,
        [run["kinetic_mean"] / run["expected_kinetic_mean"] for run in runs],
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    axes[1].set_title("Kinetic temperature check")
    axes[1].set_ylabel("<K> / target")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=8)

    axes[2].bar(
        x,
        [run["position_integrated_autocorrelation_time"] for run in runs],
        color="#8c6bb1",
        edgecolor="#44315d",
        linewidth=0.6,
    )
    axes[2].set_title("Dynamics change with coupling")
    axes[2].set_ylabel("position autocorrelation time")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels, fontsize=8)
    axes[2].text(
        0.03,
        0.95,
        "same canonical target\n"
        "different dynamical memory",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post05_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    runs = sorted(summary["runs"], key=lambda run: run["relaxation_time"])
    labels = [run["barostat"].replace("_", "\n") for run in runs]
    x = np.arange(len(runs))

    axes[0].axhline(1.0, color="#333333", linewidth=0.9)
    axes[0].bar(
        x,
        [run["volume_variance"] / run["expected_volume_variance"] for run in runs],
        color="#2f6f9f",
        edgecolor="#18384f",
        linewidth=0.6,
    )
    axes[0].set_title("Volume fluctuation check")
    axes[0].set_ylabel("observed / expected")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=8)

    axes[1].axhline(1.0, color="#333333", linewidth=0.9)
    axes[1].bar(
        x,
        [run["pressure_variance"] / run["expected_pressure_variance"] for run in runs],
        color="#d88c3d",
        edgecolor="#784714",
        linewidth=0.6,
    )
    axes[1].set_title("Pressure fluctuations are large")
    axes[1].set_ylabel("observed / expected")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=8)

    axes[2].bar(
        x,
        [run["volume_integrated_autocorrelation_time"] for run in runs],
        color="#8c6bb1",
        edgecolor="#44315d",
        linewidth=0.6,
    )
    axes[2].set_title("Barostat time controls memory")
    axes[2].set_ylabel("volume autocorrelation time")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels, fontsize=8)
    axes[2].text(
        0.03,
        0.95,
        f"kappa = {summary['compressibility']:.3g}\n"
        f"V0 = {summary['equilibrium_volume']:.0f}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post06_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    checkpoints = summary["checkpoints"]
    checkpoint_steps = np.array(
        [checkpoint["checkpoint_steps"] for checkpoint in checkpoints],
        dtype=float,
    )
    x = np.arange(len(checkpoints))

    axes[0].axhline(summary["true_mean"], color="#333333", linewidth=0.9, label="true mean")
    time = samples["time"]
    replica_keys = sorted(key for key in samples if key.startswith("replica_"))
    for key in replica_keys:
        running = np.cumsum(samples[key]) / np.arange(1, len(samples[key]) + 1)
        axes[0].plot(time, running, linewidth=1.0, alpha=0.72, label=key.replace("_", " "))
    axes[0].set_title("Running means are sticky")
    axes[0].set_xlabel("time")
    axes[0].set_ylabel("running mean")
    axes[0].legend(frameon=False, fontsize=7, ncol=2)

    axes[1].bar(
        x - 0.18,
        [checkpoint["naive_standard_error"] for checkpoint in checkpoints],
        width=0.36,
        color="#2f6f9f",
        edgecolor="#18384f",
        linewidth=0.6,
        label="naive",
    )
    axes[1].bar(
        x + 0.18,
        [checkpoint["conservative_standard_error"] for checkpoint in checkpoints],
        width=0.36,
        color="#d88c3d",
        edgecolor="#784714",
        linewidth=0.6,
        label="block/replica-aware",
    )
    axes[1].set_title("Correlation inflates uncertainty")
    axes[1].set_ylabel("standard error")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([f"{int(step)}" for step in checkpoint_steps], fontsize=8)
    axes[1].legend(frameon=False, fontsize=8)

    axes[2].plot(
        checkpoint_steps,
        [checkpoint["effective_samples"] for checkpoint in checkpoints],
        marker="o",
        color="#6a8f4e",
        linewidth=1.5,
    )
    axes[2].set_title("ESS, not frames, controls trust")
    axes[2].set_xlabel("trajectory steps")
    axes[2].set_ylabel("effective samples")
    axes[2].text(
        0.03,
        0.95,
        f"tau target = {summary['correlation_time']:.0f}\n"
        f"replicas = {summary['replica_count']}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post07_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    rdf_samples: dict[str, np.ndarray],
    vacf_samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    systems = sorted(summary["systems"], key=lambda system: system["atom_count"])
    radius = rdf_samples["radius"]
    colors = ["#2f6f9f", "#d88c3d", "#6a8f4e"]

    for idx, system in enumerate(systems):
        key = f"{system['system']}_rdf"
        axes[0].plot(
            radius,
            rdf_samples[key],
            color=colors[idx % len(colors)],
            linewidth=1.4,
            label=f"{system['system']} (N={system['atom_count']})",
        )
    axes[0].axhline(1.0, color="#333333", linewidth=0.8, linestyle="--")
    axes[0].set_title("RDF is an estimator")
    axes[0].set_xlabel("radius")
    axes[0].set_ylabel("g(r)")
    axes[0].legend(frameon=False, fontsize=8)

    x = np.arange(len(systems))
    axes[1].bar(
        x,
        [system["coordination_number"] for system in systems],
        yerr=[system["coordination_block_standard_error"] for system in systems],
        capsize=4,
        color=["#6a8f4e", "#8c6bb1", "#d88c3d"][: len(systems)],
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    axes[1].set_title("Coordination needs an error bar")
    axes[1].set_ylabel("coordination number")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(
        [f"{system['system']}\nN={system['atom_count']}" for system in systems],
        fontsize=8,
    )

    axes[2].axhline(0.0, color="#333333", linewidth=0.8)
    axes[2].plot(
        vacf_samples["lag"],
        vacf_samples["normalized_vacf"],
        color="#2f6f9f",
        linewidth=1.5,
    )
    axes[2].set_title("Time correlation is an observable")
    axes[2].set_xlabel("lag")
    axes[2].set_ylabel("normalized VACF")
    axes[2].text(
        0.03,
        0.95,
        f"rho = {summary['number_density']:.3g}\n"
        f"bin = {summary['rdf_bin_width']:.2g}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post08_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    curves: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")

    axes[0].plot(
        curves["true_pmf_x"],
        curves["true_pmf_y"],
        color="#222222",
        linewidth=1.2,
        label="true F(s)",
    )
    axes[0].plot(
        curves["histogram_pmf_x"],
        curves["histogram_pmf_y"],
        color="#2f6f9f",
        linewidth=1.4,
        label="histogram PMF",
    )
    axes[0].plot(
        curves["reweighted_pmf_x"],
        curves["reweighted_pmf_y"],
        color="#d88c3d",
        linewidth=1.2,
        linestyle="--",
        label="reweighted",
    )
    axes[0].set_title("PMF from equilibrium samples")
    axes[0].set_xlabel("collective variable s")
    axes[0].set_ylabel("F(s)")
    axes[0].legend(frameon=False, fontsize=8)

    bins = summary["bins"]
    x = np.arange(len(bins))
    axes[1].axhline(summary["true_barrier_height"], color="#333333", linewidth=0.9)
    axes[1].bar(
        x,
        [item["barrier_height"] for item in bins],
        yerr=[item["bootstrap_barrier_standard_error"] for item in bins],
        capsize=4,
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    axes[1].set_title("Binning changes barriers")
    axes[1].set_ylabel("barrier height")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels([f"bin {item['bin_width']:.2g}" for item in bins], fontsize=8)

    axes[2].plot(
        curves["rdf_pmf_x"],
        curves["rdf_pmf_y"],
        color="#8c6bb1",
        linewidth=1.5,
        label="-log g(r)",
    )
    axes[2].plot(
        curves["rdf_x"],
        curves["rdf_y"] / np.nanmax(curves["rdf_y"]) * np.nanmax(curves["rdf_pmf_y"]),
        color="#d88c3d",
        linewidth=1.0,
        alpha=0.8,
        label="scaled g(r)",
    )
    axes[2].set_title("RDF can become a PMF")
    axes[2].set_xlabel("radius")
    axes[2].set_ylabel("shifted F(r)")
    axes[2].legend(frameon=False, fontsize=8)
    axes[2].text(
        0.03,
        0.95,
        f"kT = {summary['temperature']:.1f}\n"
        f"N = {summary['sample_count']}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)
