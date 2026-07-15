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
    argon_samples_path = result_dir / "argon_nve_samples.csv"
    argon_samples = (
        _read_post03_samples(argon_samples_path)
        if argon_samples_path.exists()
        else {}
    )

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-03"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
        _draw_post03_figure(fig, axes, summary, samples, argon_samples)

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
    argon_samples_path = result_dir / "argon_langevin_samples.csv"
    argon_samples = (
        _read_named_series(argon_samples_path, "thermostat", "kinetic_temperature")
        if argon_samples_path.exists()
        else {}
    )

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-04"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
        _draw_post04_figure(fig, axes, summary, samples, argon_samples)

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
    argon_samples_path = result_dir / "argon_cell_response.csv"
    argon_samples = (
        _read_post05_samples(argon_samples_path) if argon_samples_path.exists() else None
    )
    argon_npt_path = result_dir / "argon_npt_dynamics.csv"
    argon_npt = _read_post05_samples(argon_npt_path) if argon_npt_path.exists() else None

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-05"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
        _draw_post05_figure(fig, axes.ravel(), summary, samples, argon_samples, argon_npt)

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
    argon_samples_path = result_dir / "argon_observable_samples.csv"
    argon_samples = (
        _read_post06_samples(argon_samples_path) if argon_samples_path.exists() else None
    )

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-06"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
        _draw_post06_figure(fig, axes.ravel(), summary, samples, argon_samples)

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
    argon_rdf_path = result_dir / "argon_trajectory_rdf_samples.csv"
    argon_vacf_path = result_dir / "argon_trajectory_vacf_samples.csv"
    argon_rdf_samples = (
        _read_post07_samples(argon_rdf_path) if argon_rdf_path.exists() else None
    )
    argon_vacf_samples = (
        _read_post07_samples(argon_vacf_path) if argon_vacf_path.exists() else None
    )

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-07"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
        _draw_post07_figure(
            fig,
            axes.ravel(),
            summary,
            rdf_samples,
            vacf_samples,
            argon_rdf_samples,
            argon_vacf_samples,
        )

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

    has_argon = "argon_rdf_pmf_x" in curves and "argon_rdf_pmf_y" in curves
    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-08"}):
        if has_argon:
            fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), constrained_layout=True)
            draw_axes = axes.ravel()
        else:
            fig, draw_axes = plt.subplots(
                1, 3, figsize=(12.2, 3.6), constrained_layout=True
            )
        _draw_post08_figure(fig, draw_axes, summary, curves)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post09_figures(
    result_dir: Path = Path("results/post-09/smoke"),
    figure_dir: Path = Path("figures/post-09"),
    snapshot_dir: Path = Path("snapshots/post-09"),
    name: str = "estimator_diagnostics",
) -> list[Path]:
    """Generate free-energy estimator diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "estimator_summary.json").read_text())
    samples = _read_post09_samples(result_dir / "work_samples.csv")
    multistate_curves_path = result_dir / "multistate_curves.csv"
    multistate_windows_path = result_dir / "multistate_windows.csv"
    multistate_curves = (
        _read_post09_samples(multistate_curves_path)
        if multistate_curves_path.exists()
        else None
    )
    multistate_windows = (
        _read_post09_samples(multistate_windows_path)
        if multistate_windows_path.exists()
        else None
    )

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-09"}):
        if multistate_curves:
            fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
            axes_for_plot = axes.ravel()
        else:
            fig, axes_for_plot = plt.subplots(
                1, 3, figsize=(12.2, 3.6), constrained_layout=True
            )
        _draw_post09_figure(
            fig,
            axes_for_plot,
            summary,
            samples,
            multistate_curves,
            multistate_windows,
        )

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post10_figures(
    result_dir: Path = Path("results/post-10/smoke"),
    figure_dir: Path = Path("figures/post-10"),
    snapshot_dir: Path = Path("snapshots/post-10"),
    name: str = "umbrella_diagnostics",
) -> list[Path]:
    """Generate umbrella-sampling reconstruction diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "umbrella_summary.json").read_text())
    curves = _read_post10_curves(result_dir / "umbrella_curves.csv")
    windows = _read_post10_windows(result_dir / "umbrella_windows.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-10"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
        _draw_post10_figure(fig, axes.ravel(), summary, curves, windows)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post11_figures(
    result_dir: Path = Path("results/post-11/smoke"),
    figure_dir: Path = Path("figures/post-11"),
    snapshot_dir: Path = Path("snapshots/post-11"),
    name: str = "enhanced_sampling_diagnostics",
) -> list[Path]:
    """Generate adaptive and nonequilibrium enhanced-sampling figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "enhanced_sampling_summary.json").read_text())
    curves = _read_post11_curves(result_dir / "enhanced_sampling_curves.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-11"}):
        fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.0), constrained_layout=True)
        _draw_post11_figure(fig, axes.ravel(), summary, curves)

        svg_path = figure_dir / f"{name}.svg"
        png_path = figure_dir / f"{name}.png"
        snapshot_path = snapshot_dir / f"{name}_snapshot.png"
        fig.savefig(svg_path, metadata={"Date": None})
        _strip_trailing_whitespace(svg_path)
        fig.savefig(png_path, dpi=220)
        fig.savefig(snapshot_path, dpi=160)
        plt.close(fig)
    return [svg_path, png_path, snapshot_path]


def generate_post12_figures(
    result_dir: Path = Path("results/post-12/smoke"),
    figure_dir: Path = Path("figures/post-12"),
    snapshot_dir: Path = Path("snapshots/post-12"),
    name: str = "mlip_diagnostics",
) -> list[Path]:
    """Generate MLIP capstone diagnostic figures."""

    figure_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((result_dir / "mlip_summary.json").read_text())
    samples = _read_post12_samples(result_dir / "mlip_samples.csv")

    with rc_context({"svg.hashsalt": "kups-md-tutorials-post-12"}):
        fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.6), constrained_layout=True)
        _draw_post12_figure(fig, axes, summary, samples)

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


def _read_named_series(
    path: Path,
    name_field: str,
    value_field: str,
) -> dict[str, dict[str, np.ndarray]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    grouped: dict[str, dict[str, list[float]]] = {}
    for row in rows:
        name = row[name_field]
        series = grouped.setdefault(name, {"time": [], value_field: []})
        series["time"].append(float(row["time"]))
        series[value_field].append(float(row[value_field]))
    return {
        name: {
            key: np.asarray(values, dtype=float)
            for key, values in series.items()
        }
        for name, series in grouped.items()
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


def _read_post09_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array(
            [float(row[key]) if row[key] else np.nan for row in rows],
            dtype=float,
        )
        for key in reader.fieldnames or []
    }


def _read_post10_curves(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    curves: dict[str, np.ndarray] = {}
    for key in reader.fieldnames or []:
        values = [float(row[key]) for row in rows if row[key]]
        curves[key] = np.array(values, dtype=float)
    return curves


def _read_post10_windows(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    windows: dict[str, np.ndarray] = {}
    for key in reader.fieldnames or []:
        values = [float(row[key]) for row in rows if row[key]]
        windows[key] = np.array(values, dtype=float)
    return windows


def _read_post11_curves(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    curves: dict[str, np.ndarray] = {}
    for key in reader.fieldnames or []:
        values = [float(row[key]) for row in rows if row[key]]
        curves[key] = np.array(values, dtype=float)
    return curves


def _read_post12_samples(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return {
        key: np.array([float(row[key]) for row in rows], dtype=float)
        for key in reader.fieldnames or []
    }


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
    argon_samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    flat_axes = np.asarray(axes).ravel()

    runs = summary["runs"]
    exact_float64 = sorted(
        [
            run
            for run in runs
            if run["force_case"] == "exact_force" and run["precision"] == "float64"
        ],
        key=lambda run: run["time_step"],
    )
    flat_axes[0].plot(
        [run["time_step"] for run in exact_float64],
        [run["max_abs_relative_energy_error"] for run in exact_float64],
        marker="o",
        color="#2f6f9f",
        linewidth=1.5,
    )
    flat_axes[0].set_title("Timestep controls bounded error")
    flat_axes[0].set_xlabel("oscillator time step")
    flat_axes[0].set_ylabel("max |Delta E| / E0")
    flat_axes[0].set_yscale("log")

    largest_dt = max(run["time_step"] for run in runs)
    exact_largest = [
        run
        for run in runs
        if run["force_case"] == "exact_force" and run["time_step"] == largest_dt
    ]
    exact_largest = sorted(exact_largest, key=lambda run: _precision_sort_key(run["precision"]))
    flat_axes[1].bar(
        np.arange(len(exact_largest)),
        [run["max_abs_relative_energy_error"] for run in exact_largest],
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    flat_axes[1].set_title("Precision can set an error floor")
    flat_axes[1].set_ylabel("max |Delta E| / E0")
    flat_axes[1].set_yscale("log")
    flat_axes[1].set_xticks(np.arange(len(exact_largest)))
    flat_axes[1].set_xticklabels(
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
    flat_axes[2].axhline(0.0, color="#333333", linewidth=0.8)
    flat_axes[2].bar(
        np.arange(len(force_runs)),
        [run["normalized_energy_drift"] for run in force_runs],
        color="#d88c3d",
        edgecolor="#784714",
        linewidth=0.6,
    )
    flat_axes[2].set_title("Force bias appears as drift")
    flat_axes[2].set_ylabel("Delta E / (E0 time)")
    flat_axes[2].set_xticks(np.arange(len(force_runs)))
    flat_axes[2].set_xticklabels(
        [run["force_case"].replace("_", "\n") for run in force_runs],
        fontsize=8,
    )

    argon_runs = sorted(
        summary.get("argon_nve_runs", []),
        key=lambda run: run["time_step"],
    )
    if argon_samples:
        for time_step in sorted(set(argon_samples["time_step"])):
            time_step_mask = argon_samples["time_step"] == time_step
            if "replica_index" in argon_samples:
                times = np.unique(argon_samples["time"][time_step_mask])
                replica_values = []
                for replica_index in sorted(
                    set(argon_samples["replica_index"][time_step_mask])
                ):
                    mask = (
                        time_step_mask
                        & (argon_samples["replica_index"] == replica_index)
                    )
                    order = np.argsort(argon_samples["time"][mask])
                    replica_values.append(
                        argon_samples["relative_energy_error"][mask][order]
                )
                values = np.asarray(replica_values, dtype=float)
                mean = np.mean(values, axis=0)
                std = (
                    np.std(values, axis=0, ddof=1)
                    if len(values) > 1
                    else np.zeros_like(mean)
                )
                flat_axes[3].fill_between(
                    times,
                    mean - std,
                    mean + std,
                    alpha=0.14,
                    linewidth=0,
                )
                flat_axes[3].plot(
                    times,
                    mean,
                    linewidth=1.2,
                    label=f"dt={time_step:g}",
                )
                continue
            mask = time_step_mask
            flat_axes[3].plot(
                argon_samples["time"][mask],
                argon_samples["relative_energy_error"][mask],
                linewidth=1.2,
                label=f"dt={time_step:g}",
            )
    elif argon_runs:
        flat_axes[3].plot(
            [run["time_step"] for run in argon_runs],
            [run["max_abs_relative_energy_error"] for run in argon_runs],
            marker="o",
            color="#7b4f9a",
            linewidth=1.4,
        )
    flat_axes[3].axhline(0.0, color="#333333", linewidth=0.8)
    flat_axes[3].set_title("Argon NVE drift is bounded")
    flat_axes[3].set_xlabel("reduced time")
    flat_axes[3].set_ylabel("Delta E / |E0|")
    if argon_samples:
        title = None
        if argon_runs:
            protocol = summary.get("argon_nve_protocol")
            if protocol is not None:
                title = (
                    f"{protocol['atom_count']} Ar atoms, "
                    f"{protocol['replica_count']} replicas"
                )
            else:
                title = f"{argon_runs[-1]['atom_count']} Ar atoms, LJ units"
        flat_axes[3].legend(
            frameon=True,
            fontsize=8,
            loc="upper right",
            title=title,
            title_fontsize=8,
            framealpha=0.85,
        )

    flat_axes[0].text(
        0.03,
        0.95,
        f"N = {len(runs)} runs\nfull grid: dt, precision, force scale",
        transform=flat_axes[0].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in flat_axes:
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
    argon_samples: dict[str, dict[str, np.ndarray]],
) -> None:
    fig.patch.set_facecolor("white")
    flat_axes = np.asarray(axes).ravel()

    runs = sorted(summary["runs"], key=lambda run: run["gamma"])
    labels = [run["thermostat"].replace("_", "\n") for run in runs]
    x = np.arange(len(runs))

    flat_axes[0].axhline(1.0, color="#333333", linewidth=0.9, label="canonical target")
    flat_axes[0].plot(
        x,
        [run["position_variance"] / run["expected_position_variance"] for run in runs],
        marker="o",
        color="#2f6f9f",
        linewidth=1.5,
        label="position variance",
    )
    flat_axes[0].plot(
        x,
        [run["velocity_variance"] / run["expected_velocity_variance"] for run in runs],
        marker="s",
        color="#d88c3d",
        linewidth=1.5,
        label="velocity variance",
    )
    flat_axes[0].set_title("Canonical variance check")
    flat_axes[0].set_ylabel("observed / expected")
    flat_axes[0].set_xticks(x)
    flat_axes[0].set_xticklabels(labels, fontsize=8)
    flat_axes[0].legend(frameon=False, fontsize=8)

    flat_axes[1].axhline(1.0, color="#333333", linewidth=0.9)
    flat_axes[1].bar(
        x,
        [run["kinetic_mean"] / run["expected_kinetic_mean"] for run in runs],
        color="#6a8f4e",
        edgecolor="#2d4721",
        linewidth=0.6,
    )
    flat_axes[1].set_title("Kinetic temperature check")
    flat_axes[1].set_ylabel("<K> / target")
    flat_axes[1].set_xticks(x)
    flat_axes[1].set_xticklabels(labels, fontsize=8)

    flat_axes[2].bar(
        x,
        [run["position_integrated_autocorrelation_time"] for run in runs],
        color="#8c6bb1",
        edgecolor="#44315d",
        linewidth=0.6,
    )
    flat_axes[2].set_title("Dynamics change with coupling")
    flat_axes[2].set_ylabel("position autocorrelation time")
    flat_axes[2].set_xticks(x)
    flat_axes[2].set_xticklabels(labels, fontsize=8)
    flat_axes[2].text(
        0.03,
        0.95,
        "same canonical target\n"
        "different dynamical memory",
        transform=flat_axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    argon_runs = sorted(summary.get("argon_langevin_runs", []), key=lambda run: run["gamma"])
    handoff_groups: dict[float, list[float]] = {}
    for run in argon_runs:
        handoff_groups.setdefault(run["gamma"], []).append(
            abs(run["nve_normalized_energy_drift"])
        )
    if handoff_groups:
        gammas = np.asarray(sorted(handoff_groups), dtype=float)
        centers = np.arange(len(gammas))
        means = np.asarray([np.mean(handoff_groups[gamma]) for gamma in gammas], dtype=float)
        errors = np.asarray(
            [
                np.std(handoff_groups[gamma], ddof=1) / np.sqrt(len(handoff_groups[gamma]))
                if len(handoff_groups[gamma]) > 1
                else 0.0
                for gamma in gammas
            ],
            dtype=float,
        )
        flat_axes[3].bar(
            centers,
            means,
            yerr=errors,
            color="#4f8c8b",
            edgecolor="#1c4f4e",
            linewidth=0.6,
            capsize=3,
        )
        flat_axes[3].set_xticks(centers)
        flat_axes[3].set_xticklabels([f"gamma={gamma:g}" for gamma in gammas], fontsize=8)
        protocol = summary.get("argon_langevin_protocol") or {}
        if protocol:
            flat_axes[3].text(
                0.03,
                0.95,
                f"{protocol['atom_count']} Ar atoms\n"
                f"{protocol['replica_count']} replicas\n"
                f"NVE steps {protocol['nve_handoff_steps']}",
                transform=flat_axes[3].transAxes,
                va="top",
                ha="left",
                fontsize=8.2,
                bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
            )
    flat_axes[3].set_title("Argon thermostat to NVE handoff")
    flat_axes[3].set_ylabel("|NVE normalized energy drift|")
    if argon_runs:
        flat_axes[3].set_yscale("log")

    for ax in flat_axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post05_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
    argon_samples: dict[str, np.ndarray] | None,
    argon_npt: dict[str, np.ndarray] | None,
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

    axes[3].set_title("Argon moving-cell check")
    if argon_npt is not None:
        unique_times = np.unique(argon_npt["time"])
        volume_mean = []
        volume_std = []
        temperature_mean = []
        for time in unique_times:
            mask = argon_npt["time"] == time
            volume_values = argon_npt["volume_factor"][mask]
            temperature_values = argon_npt["kinetic_temperature"][mask]
            volume_mean.append(float(np.mean(volume_values)))
            volume_std.append(
                float(np.std(volume_values, ddof=1)) if len(volume_values) > 1 else 0.0
            )
            temperature_mean.append(float(np.mean(temperature_values)))
        volume_mean_array = np.asarray(volume_mean, dtype=float)
        volume_std_array = np.asarray(volume_std, dtype=float)
        temperature_mean_array = np.asarray(temperature_mean, dtype=float)
        axes[3].fill_between(
            unique_times,
            volume_mean_array - volume_std_array,
            volume_mean_array + volume_std_array,
            color="#2b8a6e",
            alpha=0.16,
            linewidth=0,
        )
        axes[3].plot(
            unique_times,
            volume_mean_array,
            color="#2b8a6e",
            linewidth=1.4,
            label="mean V / V0",
        )
        axes[3].axhline(1.0, color="#333333", linewidth=0.8, linestyle=":")
        axes[3].set_xlabel("time")
        axes[3].set_ylabel("volume factor")
        temp_axis = axes[3].twinx()
        temp_axis.plot(
            unique_times,
            temperature_mean_array,
            color="#b55339",
            linewidth=1.0,
            alpha=0.82,
            label="mean Tkin",
        )
        temp_axis.axhline(
            summary["argon_npt_dynamics"]["mean_kinetic_temperature"],
            color="#b55339",
            linewidth=0.7,
            linestyle=":",
            alpha=0.75,
        )
        temp_axis.set_ylabel("kinetic temperature", color="#b55339")
        temp_axis.tick_params(axis="y", labelcolor="#b55339", labelsize=8)
        dynamics = summary.get("argon_npt_dynamics") or {}
        axes[3].text(
            0.04,
            0.95,
            f"replicas = {dynamics.get('replica_count', 1)}\n"
            f"Neff = {dynamics.get('volume_effective_samples', float('nan')):.1f}\n"
            f"P = {dynamics.get('mean_pressure', float('nan')):.2f} +/- "
            f"{dynamics.get('pressure_standard_error', float('nan')):.2f}",
            transform=axes[3].transAxes,
            va="top",
            ha="left",
            fontsize=8.0,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
        )
    elif argon_samples is not None:
        axes[3].plot(
            argon_samples["volume_factor"],
            argon_samples["pressure"],
            marker="o",
            color="#2b8a6e",
            linewidth=1.6,
        )
        axes[3].axvline(1.0, color="#333333", linewidth=0.8, linestyle=":")
        axes[3].set_xlabel("V / V0")
        axes[3].set_ylabel("reduced pressure")
        response = summary.get("argon_cell_response") or {}
        axes[3].text(
            0.04,
            0.95,
            f"Kfit = {response.get('fitted_bulk_modulus', float('nan')):.2f}\n"
            f"N = {response.get('atom_count', 0)}",
            transform=axes[3].transAxes,
            va="top",
            ha="left",
            fontsize=8.5,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
        )
    else:
        axes[3].text(
            0.5,
            0.5,
            "argon cell response\nnot configured",
            transform=axes[3].transAxes,
            va="center",
            ha="center",
            fontsize=9,
        )
        axes[3].set_xticks([])
        axes[3].set_yticks([])

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post06_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
    argon_samples: dict[str, np.ndarray] | None,
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

    axes[3].set_title("Argon replica uncertainty")
    argon_summary = summary.get("argon_observable")
    if argon_summary is not None:
        argon_checkpoints = argon_summary["checkpoints"]
        argon_steps = np.array(
            [checkpoint["checkpoint_steps"] for checkpoint in argon_checkpoints],
            dtype=float,
        )
        argon_means = np.array(
            [
                checkpoint["mean_potential_energy_per_atom"]
                for checkpoint in argon_checkpoints
            ],
            dtype=float,
        )
        argon_ci = np.array(
            [checkpoint["conservative_ci95_half_width"] for checkpoint in argon_checkpoints],
            dtype=float,
        )
        coordination_means = np.array(
            [checkpoint["mean_coordination_number"] for checkpoint in argon_checkpoints],
            dtype=float,
        )
        coordination_ci = np.array(
            [
                checkpoint["coordination_conservative_ci95_half_width"]
                for checkpoint in argon_checkpoints
            ],
            dtype=float,
        )
        axes[3].errorbar(
            argon_steps,
            argon_means,
            yerr=argon_ci,
            marker="o",
            color="#2b8a6e",
            ecolor="#6aa891",
            capsize=3,
            linewidth=1.4,
        )
        if argon_samples is not None:
            replica_keys = sorted(
                key
                for key in argon_samples
                if key.startswith("replica_") and key.endswith("_potential_energy_per_atom")
            )
            for key in replica_keys:
                axes[3].plot(
                    argon_samples["step"],
                    argon_samples[key],
                    color="#8bbfad",
                    alpha=0.22,
                    linewidth=0.8,
                )
        axes[3].set_xlabel("trajectory steps")
        axes[3].set_ylabel("PE / atom")
        coordination_axis = axes[3].twinx()
        coordination_axis.errorbar(
            argon_steps,
            coordination_means,
            yerr=coordination_ci,
            marker="s",
            color="#b55339",
            ecolor="#d38a76",
            capsize=3,
            linewidth=1.0,
            label="coordination",
        )
        coordination_axis.set_ylabel("coordination", color="#b55339")
        coordination_axis.tick_params(axis="y", labelcolor="#b55339", labelsize=8)
        axes[3].text(
            0.03,
            0.95,
            f"N = {argon_summary['atom_count']}\n"
            f"replicas = {argon_summary['replica_count']}\n"
            f"rc = {argon_summary['coordination_cutoff']:.2f}",
            transform=axes[3].transAxes,
            va="top",
            ha="left",
            fontsize=8.5,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
        )
    else:
        axes[3].text(
            0.5,
            0.5,
            "argon observable\nnot configured",
            transform=axes[3].transAxes,
            va="center",
            ha="center",
            fontsize=9,
        )
        axes[3].set_xticks([])
        axes[3].set_yticks([])

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
    argon_rdf_samples: dict[str, np.ndarray] | None,
    argon_vacf_samples: dict[str, np.ndarray] | None,
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
        label="controlled VACF",
    )
    if argon_vacf_samples is not None:
        argon_lag = argon_vacf_samples["lag"]
        argon_vacf = argon_vacf_samples["normalized_vacf"]
        argon_vacf_std = argon_vacf_samples.get("vacf_replica_std")
        if argon_vacf_std is not None:
            axes[2].fill_between(
                argon_lag,
                argon_vacf - argon_vacf_std,
                argon_vacf + argon_vacf_std,
                color="#c75c3d",
                alpha=0.16,
                linewidth=0,
                label="argon rep std",
            )
        axes[2].plot(
            argon_lag,
            argon_vacf,
            color="#c75c3d",
            linewidth=1.2,
            label="argon VACF",
        )
    axes[2].set_title("Time correlation is an observable")
    axes[2].set_xlabel("lag")
    axes[2].set_ylabel("normalized VACF")
    axes[2].legend(frameon=False, fontsize=8)
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

    axes[3].set_title("Trajectory RDF is physical")
    argon_summary = summary.get("argon_trajectory")
    if argon_rdf_samples is not None and argon_summary is not None:
        radius_argon = argon_rdf_samples["radius"]
        rdf_argon = argon_rdf_samples["argon_trajectory_rdf"]
        rdf_replica_std = argon_rdf_samples.get("argon_trajectory_rdf_replica_std")
        if rdf_replica_std is not None:
            finite_band = np.isfinite(rdf_argon) & np.isfinite(rdf_replica_std)
            axes[3].fill_between(
                radius_argon[finite_band],
                rdf_argon[finite_band] - rdf_replica_std[finite_band],
                rdf_argon[finite_band] + rdf_replica_std[finite_band],
                color="#2b8a6e",
                alpha=0.18,
                linewidth=0,
                label="replica std",
            )
        axes[3].plot(
            radius_argon,
            rdf_argon,
            color="#2b8a6e",
            linewidth=1.5,
            label="trajectory RDF",
        )
        axes[3].axhline(1.0, color="#333333", linewidth=0.8, linestyle="--")
        axes[3].axvline(
            argon_summary["coordination_cutoff"],
            color="#5b5b5b",
            linewidth=0.8,
            linestyle=":",
        )
        axes[3].set_xlabel("radius")
        axes[3].set_ylabel("g(r)")
        axes[3].legend(frameon=False, fontsize=8)
        axes[3].text(
            0.03,
            0.95,
            f"N = {argon_summary['atom_count']}\n"
            f"coord = {argon_summary['coordination_number']:.2f}\n"
            f"rep SE = {argon_summary['coordination_replica_standard_error']:.3f}",
            transform=axes[3].transAxes,
            va="top",
            ha="left",
            fontsize=8.5,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
        )
    else:
        axes[3].text(
            0.5,
            0.5,
            "argon trajectory\nnot configured",
            transform=axes[3].transAxes,
            va="center",
            ha="center",
            fontsize=9,
        )
        axes[3].set_xticks([])
        axes[3].set_yticks([])

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

    if len(axes) > 3 and summary.get("argon_rdf_pmf") is not None:
        argon = summary["argon_rdf_pmf"]
        pmf_x = curves["argon_rdf_pmf_x"]
        pmf_y = curves["argon_rdf_pmf_y"]
        block_sem = curves.get("argon_rdf_pmf_block_sem_y")
        replica_std = curves.get("argon_rdf_pmf_replica_std_y")
        if block_sem is not None:
            valid_band = np.isfinite(pmf_y) & np.isfinite(block_sem)
            axes[3].fill_between(
                pmf_x[valid_band],
                pmf_y[valid_band] - block_sem[valid_band],
                pmf_y[valid_band] + block_sem[valid_band],
                color="#3f8f8a",
                alpha=0.18,
                linewidth=0,
                label="block SEM",
            )
        axes[3].plot(
            pmf_x,
            pmf_y,
            color="#3f8f8a",
            linewidth=1.5,
            label="support 0.05",
        )
        for threshold, color in (("0.02", "#8bb7b2"), ("0.1", "#1f5f5b")):
            key_x = f"argon_rdf_pmf_support_{threshold}_x"
            key_y = f"argon_rdf_pmf_support_{threshold}_y"
            if key_x in curves and key_y in curves:
                axes[3].plot(
                    curves[key_x],
                    curves[key_y],
                    color=color,
                    linewidth=0.9,
                    linestyle=":",
                    alpha=0.75,
                    label=f"support {threshold}",
                )
        finite_pmf = pmf_y[np.isfinite(pmf_y)]
        pmf_scale = float(np.nanmax(finite_pmf)) if finite_pmf.size else 1.0
        rdf_scale = float(np.nanmax(curves["argon_rdf_y"]))
        if rdf_scale > 0.0 and pmf_scale > 0.0:
            axes[3].plot(
                curves["argon_rdf_x"],
                curves["argon_rdf_y"] / rdf_scale * pmf_scale,
                color="#d88c3d",
                linewidth=1.0,
                alpha=0.8,
                label="scaled g(r)",
            )
        axes[3].axvline(
            argon["pmf_minimum_radius"],
            color="#333333",
            linestyle=":",
            linewidth=0.9,
            label="PMF minimum",
        )
        axes[3].set_title("Trajectory RDF to PMF")
        axes[3].set_xlabel("radius")
        axes[3].set_ylabel("shifted F(r)")
        axes[3].legend(frameon=False, fontsize=8)
        axes[3].text(
            0.03,
            0.95,
            f"N = {argon['atom_count']}\n"
            f"frames = {argon['frame_count']}\n"
            f"rmin = {argon['pmf_minimum_radius']:.3f}\n"
            f"rep std max = {argon['max_replica_pmf_std']:.2f}\n"
            f"support span = {argon['support_threshold_range_span']:.2f}",
            transform=axes[3].transAxes,
            va="top",
            ha="left",
            fontsize=8.5,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
        )
        if replica_std is not None and np.any(np.isfinite(replica_std)):
            twin = axes[3].twinx()
            twin.plot(
                pmf_x,
                replica_std,
                color="#7a4f9f",
                linewidth=1.0,
                linestyle="--",
                label="replica std",
            )
            twin.set_ylabel("replica std", color="#7a4f9f", fontsize=8)
            twin.tick_params(axis="y", colors="#7a4f9f", labelsize=8)
            twin.spines["top"].set_visible(False)
            twin.grid(False)

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post09_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
    multistate_curves: dict[str, np.ndarray] | None = None,
    multistate_windows: dict[str, np.ndarray] | None = None,
) -> None:
    fig.patch.set_facecolor("white")
    cases = summary["cases"]
    labels = [case["case"].replace("_", "\n") for case in cases]
    x = np.arange(len(cases))

    axes[0].axhline(cases[0]["true_delta_f"], color="#333333", linewidth=0.9)
    width = 0.24
    axes[0].bar(
        x - width,
        [case["forward_fep_delta_f"] for case in cases],
        width=width,
        color="#2f6f9f",
        label="forward FEP",
    )
    axes[0].bar(
        x,
        [case["reverse_fep_delta_f"] for case in cases],
        width=width,
        color="#d88c3d",
        label="reverse FEP",
    )
    axes[0].bar(
        x + width,
        [case["bar_delta_f"] for case in cases],
        width=width,
        color="#6a8f4e",
        label="BAR",
    )
    axes[0].set_title("Estimators need overlap")
    axes[0].set_ylabel("Delta F")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=8)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(
        x,
        [case["overlap_coefficient"] for case in cases],
        marker="o",
        color="#8c6bb1",
        linewidth=1.5,
        label="overlap",
    )
    axes[1].plot(
        x,
        [case["forward_weight_ess_fraction"] for case in cases],
        marker="s",
        color="#d88c3d",
        linewidth=1.5,
        label="forward ESS fraction",
    )
    axes[1].set_title("ESS collapses before samples do")
    axes[1].set_ylabel("fraction")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=8)
    axes[1].legend(frameon=False, fontsize=8)

    good = cases[0]["case"]
    poor = cases[-1]["case"]
    bins = np.linspace(
        min(np.min(samples[f"{good}_forward_work"]), np.min(samples[f"{poor}_forward_work"])),
        max(np.max(samples[f"{good}_forward_work"]), np.max(samples[f"{poor}_forward_work"])),
        40,
    )
    axes[2].hist(
        samples[f"{good}_forward_work"],
        bins=bins,
        density=True,
        color="#2f6f9f",
        alpha=0.55,
        label=good.replace("_", " "),
    )
    axes[2].hist(
        samples[f"{poor}_forward_work"],
        bins=bins,
        density=True,
        color="#d88c3d",
        alpha=0.55,
        label=poor.replace("_", " "),
    )
    axes[2].set_title("Work tails drive FEP")
    axes[2].set_xlabel("forward work")
    axes[2].set_ylabel("density")
    axes[2].legend(frameon=False, fontsize=8)

    if multistate_curves is not None and len(axes) > 3:
        ax = axes[3]
        coordinate = multistate_curves["coordinate"]
        ax.plot(
            coordinate,
            multistate_curves["true_pmf"],
            color="#333333",
            linewidth=1.2,
            label="true PMF",
        )
        colors = {
            "dense_bridge_pmf": "#6a8f4e",
            "sparse_bridge_pmf": "#c44e52",
        }
        for key, color in colors.items():
            if key not in multistate_curves:
                continue
            values = multistate_curves[key]
            ax.plot(
                coordinate,
                values,
                linewidth=1.4,
                color=color,
                label=key.replace("_pmf", "").replace("_", " "),
            )
        if multistate_windows is not None:
            text_lines = []
            for key in sorted(multistate_windows):
                if not key.endswith("_adjacent_overlap"):
                    continue
                values = multistate_windows[key]
                values = values[np.isfinite(values)]
                if len(values) == 0:
                    continue
                name = key.removesuffix("_adjacent_overlap").replace("_", " ")
                text_lines.append(f"{name}: min overlap {np.min(values):.3f}")
            if text_lines:
                ax.text(
                    0.03,
                    0.95,
                    "\n".join(text_lines),
                    transform=ax.transAxes,
                    va="top",
                    ha="left",
                    fontsize=8,
                    color="#333333",
                    bbox={
                        "boxstyle": "round,pad=0.25",
                        "facecolor": "white",
                        "alpha": 0.88,
                    },
                )
        ax.set_title("Multi-state bridges need connected overlap")
        ax.set_xlabel("coordinate")
        ax.set_ylabel("shifted PMF")
        ax.legend(frameon=False, fontsize=8, loc="upper center")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post10_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    curves: dict[str, np.ndarray],
    windows: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    protocols = summary["protocols"]
    colors = {"dense_windows": "#2f6f9f", "sparse_windows": "#d88c3d"}

    axes[0].plot(
        curves["true_x"],
        curves["true_pmf"],
        color="#222222",
        linewidth=1.5,
        label="true PMF",
    )
    for protocol in protocols:
        name = protocol["protocol"]
        axes[0].plot(
            curves[f"{name}_x"],
            curves[f"{name}_pmf"],
            color=colors.get(name, "#666666"),
            linewidth=1.35,
            label=name.replace("_", " "),
        )
    axes[0].set_title("Reconstruction needs connected windows")
    axes[0].set_xlabel("collective variable")
    axes[0].set_ylabel("shifted F")
    axes[0].legend(frameon=False, fontsize=8)

    width = 0.34
    for offset, protocol in zip((-0.18, 0.18), protocols, strict=True):
        name = protocol["protocol"]
        overlap = windows[f"{name}_adjacent_overlap"]
        axes[1].bar(
            np.arange(len(overlap)) + offset,
            overlap,
            width=width,
            color=colors.get(name, "#666666"),
            alpha=0.82,
            label=name.replace("_", " "),
        )
    axes[1].set_title("Adjacent overlap is the control")
    axes[1].set_xlabel("window pair")
    axes[1].set_ylabel("histogram overlap")
    axes[1].set_ylim(0.0, 1.0)
    axes[1].legend(frameon=False, fontsize=8)

    for protocol in protocols:
        name = protocol["protocol"]
        centers = windows[f"{name}_window_center"]
        means = windows[f"{name}_sample_mean"]
        stds = windows[f"{name}_sample_std"]
        axes[2].errorbar(
            centers,
            means,
            yerr=stds,
            marker="o",
            linewidth=1.1,
            capsize=2.5,
            color=colors.get(name, "#666666"),
            label=name.replace("_", " "),
        )
    axes[2].plot(
        [summary["domain_min"], summary["domain_max"]],
        [summary["domain_min"], summary["domain_max"]],
        color="#333333",
        linewidth=0.9,
        linestyle="--",
    )
    axes[2].set_title("A biased window samples a distribution")
    axes[2].set_xlabel("umbrella center")
    axes[2].set_ylabel("sample mean +/- std")
    axes[2].legend(frameon=False, fontsize=8)
    dense = next(item for item in protocols if item["protocol"] == "dense_windows")
    sparse = next(item for item in protocols if item["protocol"] == "sparse_windows")
    axes[2].text(
        0.03,
        0.97,
        f"dense RMSE = {dense['pmf_rmse_vs_true']:.3f}\n"
        f"sparse RMSE = {sparse['pmf_rmse_vs_true']:.3f}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for protocol in protocols:
        name = protocol["protocol"]
        axes[3].plot(
            curves[f"{name}_x"],
            curves[f"{name}_replica_abs_difference"],
            color=colors.get(name, "#666666"),
            linewidth=1.25,
            label=name.replace("_", " "),
        )
    axes[3].set_title("Replica disagreement is local")
    axes[3].set_xlabel("collective variable")
    axes[3].set_ylabel("|PMF replica difference|")
    axes[3].legend(frameon=False, fontsize=8)
    axes[3].text(
        0.03,
        0.97,
        f"dense replica RMSE = {dense['forward_reverse_pmf_rmse']:.3f}\n"
        f"sparse replica RMSE = {sparse['forward_reverse_pmf_rmse']:.3f}",
        transform=axes[3].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post11_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    curves: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    meta = summary["metadynamics"]
    pulling = summary["pulling"]
    hysteresis = summary["steered_hysteresis"]

    axes[0].plot(
        curves["grid"],
        curves["true_pmf"],
        color="#222222",
        linewidth=1.4,
        label="true PMF",
    )
    axes[0].plot(
        curves["grid"],
        curves["reconstructed_pmf"],
        color="#2f6f9f",
        linewidth=1.35,
        label="from final bias",
    )
    scaled_bias = curves["bias"] / max(np.nanmax(curves["bias"]), 1.0e-12)
    scaled_bias *= np.nanmax(curves["true_pmf"]) * 0.55
    axes[0].plot(
        curves["grid"],
        scaled_bias,
        color="#d88c3d",
        linewidth=1.0,
        alpha=0.85,
        label="scaled bias",
    )
    axes[0].set_title("Adaptive bias fills basins")
    axes[0].set_xlabel("collective variable")
    axes[0].set_ylabel("shifted F")
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(
        curves["record_step"],
        curves["record_bias_range"],
        color="#8c6bb1",
        linewidth=1.5,
    )
    axes[1].set_title("Bias growth is history-dependent")
    axes[1].set_xlabel("hill deposition")
    axes[1].set_ylabel("bias range")
    axes[1].text(
        0.03,
        0.95,
        f"left visits = {meta['basin_visit_fraction_left']:.2f}\n"
        f"right visits = {meta['basin_visit_fraction_right']:.2f}\n"
        f"barrier visits = {meta['barrier_visit_fraction']:.2f}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    forward = curves["forward_work"]
    reverse = curves["reverse_work"]
    bins = np.linspace(
        min(float(np.min(forward)), float(np.min(-reverse))),
        max(float(np.max(forward)), float(np.max(-reverse))),
        48,
    )
    axes[2].hist(
        forward,
        bins=bins,
        density=True,
        color="#2f6f9f",
        alpha=0.58,
        label="forward work",
    )
    axes[2].hist(
        -reverse,
        bins=bins,
        density=True,
        color="#d88c3d",
        alpha=0.58,
        label="- reverse work",
    )
    axes[2].axvline(
        pulling["true_delta_f"],
        color="#222222",
        linewidth=1.1,
        label="true Delta F",
    )
    axes[2].axvline(
        pulling["forward_jarzynski_delta_f"],
        color="#2f6f9f",
        linewidth=1.0,
        linestyle="--",
        label="forward Jarzynski",
    )
    axes[2].axvline(
        pulling["crooks_crossing_delta_f"],
        color="#6a8f4e",
        linewidth=1.0,
        linestyle=":",
        label="Crooks crossing",
    )
    axes[2].set_title("Nonequilibrium work is a path ensemble")
    axes[2].set_xlabel("work")
    axes[2].set_ylabel("density")
    axes[2].legend(frameon=False, fontsize=7.4)

    x = np.arange(2)
    gaps = [
        hysteresis["fast_hysteresis_gap"],
        hysteresis["slow_hysteresis_gap"],
    ]
    errors = [
        hysteresis["fast_hysteresis_gap_sem"],
        hysteresis["slow_hysteresis_gap_sem"],
    ]
    colors = ["#b95f30", "#3a7ca5"]
    axes[3].bar(x, gaps, yerr=errors, color=colors, alpha=0.76, capsize=3)
    axes[3].set_xticks(x)
    axes[3].set_xticklabels(
        [
            f"fast\n{hysteresis['fast_path_steps']} steps",
            f"slow\n{hysteresis['slow_path_steps']} steps",
        ]
    )
    axes[3].set_title("Steered trajectories show hysteresis")
    axes[3].set_ylabel("mean W_F - mean (-W_R)")
    axes[3].text(
        0.03,
        0.95,
        f"path replicas = {hysteresis['trajectory_path_count']}\n"
        f"fast/slow gap = {hysteresis['hysteresis_gap_ratio']:.2f}",
        transform=axes[3].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)


def _draw_post12_figure(
    fig: plt.Figure,
    axes: np.ndarray,
    summary: dict,
    samples: dict[str, np.ndarray],
) -> None:
    fig.patch.set_facecolor("white")
    cases = summary["cases"]
    labels = [case["case"].replace("_", "\n") for case in cases]
    x = np.arange(len(cases))

    width = 0.34
    axes[0].bar(
        x - width / 2,
        [case["force_rmse"] for case in cases],
        width=width,
        color="#2f6f9f",
        label="force RMSE",
    )
    axes[0].bar(
        x + width / 2,
        [case["force_bias_norm"] for case in cases],
        width=width,
        color="#d88c3d",
        label="force bias norm",
    )
    axes[0].set_title("Static errors miss deployment risk")
    axes[0].set_ylabel("force error")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=8)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(
        x,
        [case["normalized_nve_energy_drift"] for case in cases],
        marker="o",
        color="#8c6bb1",
        linewidth=1.5,
        label="NVE drift",
    )
    axes[1].plot(
        x,
        [case["extrapolation_fraction"] for case in cases],
        marker="s",
        color="#6a8f4e",
        linewidth=1.5,
        label="extrapolation fraction",
    )
    axes[1].plot(
        x,
        [case["neighbor_list_risk_fraction"] for case in cases],
        marker="^",
        color="#d88c3d",
        linewidth=1.5,
        label="neighbor-list risk",
    )
    axes[1].set_title("Dynamics expose extrapolation")
    axes[1].set_ylabel("fraction or normalized drift")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=8)
    axes[1].legend(frameon=False, fontsize=7.8)

    colors = ["#2f6f9f", "#d88c3d", "#8c6bb1"]
    for case, color in zip(cases, colors, strict=True):
        name = case["case"]
        error = np.abs(samples[f"{name}_force_error"])
        uncertainty = samples[f"{name}_uncertainty"]
        ratio = error / np.maximum(uncertainty, 1.0e-12)
        axes[2].hist(
            ratio,
            bins=np.linspace(0.0, 4.0, 36),
            density=True,
            histtype="step",
            linewidth=1.4,
            color=color,
            label=name.replace("_", " "),
        )
    axes[2].axvline(2.0, color="#333333", linewidth=0.9, linestyle="--")
    axes[2].set_title("Uncertainty must calibrate errors")
    axes[2].set_xlabel("|force error| / uncertainty")
    axes[2].set_ylabel("density")
    axes[2].legend(frameon=False, fontsize=7.6)
    axes[2].text(
        0.03,
        0.96,
        f"artifact: {summary['model_name']}\n"
        f"revision: {summary['model_revision']}",
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.0,
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "alpha": 0.9},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.18, linewidth=0.6)
