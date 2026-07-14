from pathlib import Path
import json

import nbformat
from nbformat.v4 import new_code_cell, new_notebook

from kups_md_tutorials.cli import main
from kups_md_tutorials.notebook_execution import execute_notebooks


def _write_notebook(path: Path) -> None:
    notebook = new_notebook(cells=[new_code_cell("x = 2\nprint(x + 3)")])
    nbformat.write(notebook, path)


def test_execute_notebooks_writes_manifest(tmp_path: Path) -> None:
    notebooks_dir = tmp_path / "notebooks"
    notebooks_dir.mkdir()
    _write_notebook(notebooks_dir / "post-01-initialization.ipynb")

    manifest_path = execute_notebooks(
        notebooks_dir=notebooks_dir,
        output_dir=tmp_path / "runs",
        posts=("01",),
        cwd=Path.cwd(),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["notebooks"][0]["post"] == "01"
    assert manifest["notebooks"][0]["code_cells"] == 1
    assert manifest["notebooks"][0]["executed_code_cells"] == 1
    assert manifest["notebooks"][0]["output_count"] == 1
    assert (tmp_path / "runs/post-01-initialization.ipynb").exists()


def test_cli_verify_notebooks(tmp_path: Path) -> None:
    notebooks_dir = tmp_path / "notebooks"
    notebooks_dir.mkdir()
    _write_notebook(notebooks_dir / "post-01-initialization.ipynb")

    assert (
        main(
            [
                "verify-notebooks",
                "--notebooks-dir",
                str(notebooks_dir),
                "--output-dir",
                str(tmp_path / "runs"),
                "--posts",
                "1",
            ]
        )
        == 0
    )
    assert (tmp_path / "runs/manifest.json").exists()
