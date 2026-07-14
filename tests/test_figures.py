from pathlib import Path

from kups_md_tutorials.config import load_integrator_spec, load_tutorial_spec
from kups_md_tutorials.figures import generate_post01_figures, generate_post02_figures
from kups_md_tutorials.initialization import write_initialization_outputs
from kups_md_tutorials.integrators import write_integrator_outputs


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
