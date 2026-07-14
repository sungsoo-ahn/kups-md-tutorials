from pathlib import Path

from kups_md_tutorials.config import (
    load_barostat_spec,
    load_error_spec,
    load_estimator_spec,
    load_free_energy_spec,
    load_integrator_spec,
    load_observable_spec,
    load_trajectory_length_spec,
    load_thermostat_spec,
    load_tutorial_spec,
    load_umbrella_spec,
)
from kups_md_tutorials.barostats import write_barostat_outputs
from kups_md_tutorials.error_diagnostics import write_error_outputs
from kups_md_tutorials.figures import (
    generate_post01_figures,
    generate_post02_figures,
    generate_post03_figures,
    generate_post04_figures,
    generate_post05_figures,
    generate_post06_figures,
    generate_post07_figures,
    generate_post08_figures,
    generate_post09_figures,
    generate_post10_figures,
)
from kups_md_tutorials.estimators import write_estimator_outputs
from kups_md_tutorials.free_energies import write_free_energy_outputs
from kups_md_tutorials.initialization import write_initialization_outputs
from kups_md_tutorials.integrators import write_integrator_outputs
from kups_md_tutorials.observables import write_observable_outputs
from kups_md_tutorials.thermostats import write_thermostat_outputs
from kups_md_tutorials.trajectory_length import write_trajectory_length_outputs
from kups_md_tutorials.umbrella_sampling import write_umbrella_outputs


def test_post01_figure_generation(tmp_path: Path) -> None:
    spec = load_tutorial_spec("01", "smoke")
    result_dir = write_initialization_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post01_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post02_figure_generation(tmp_path: Path) -> None:
    spec = load_integrator_spec("02", "smoke")
    result_dir = write_integrator_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post02_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post03_figure_generation(tmp_path: Path) -> None:
    spec = load_error_spec("03", "smoke")
    result_dir = write_error_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post03_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post04_figure_generation(tmp_path: Path) -> None:
    spec = load_thermostat_spec("04", "smoke")
    result_dir = write_thermostat_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post04_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post05_figure_generation(tmp_path: Path) -> None:
    spec = load_barostat_spec("05", "smoke")
    result_dir = write_barostat_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post05_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post06_figure_generation(tmp_path: Path) -> None:
    spec = load_trajectory_length_spec("06", "smoke")
    result_dir = write_trajectory_length_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post06_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post07_figure_generation(tmp_path: Path) -> None:
    spec = load_observable_spec("07", "smoke")
    result_dir = write_observable_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post07_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post08_figure_generation(tmp_path: Path) -> None:
    spec = load_free_energy_spec("08", "smoke")
    result_dir = write_free_energy_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post08_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post09_figure_generation(tmp_path: Path) -> None:
    spec = load_estimator_spec("09", "smoke")
    result_dir = write_estimator_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post09_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_post10_figure_generation(tmp_path: Path) -> None:
    spec = load_umbrella_spec("10", "smoke")
    result_dir = write_umbrella_outputs(spec, output_root=tmp_path / "results")
    outputs = generate_post10_figures(
        result_dir=result_dir,
        figure_dir=tmp_path / "figures",
        snapshot_dir=tmp_path / "snapshots",
    )
    assert len(outputs) == 3
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0
