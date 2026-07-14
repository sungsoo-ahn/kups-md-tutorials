from pathlib import Path

from kups_md_tutorials.config import (
    load_error_spec,
    load_integrator_spec,
    load_thermostat_spec,
    load_tutorial_spec,
)
from kups_md_tutorials.error_diagnostics import write_error_outputs
from kups_md_tutorials.figures import (
    generate_post01_figures,
    generate_post02_figures,
    generate_post03_figures,
    generate_post04_figures,
)
from kups_md_tutorials.initialization import write_initialization_outputs
from kups_md_tutorials.integrators import write_integrator_outputs
from kups_md_tutorials.thermostats import write_thermostat_outputs


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
