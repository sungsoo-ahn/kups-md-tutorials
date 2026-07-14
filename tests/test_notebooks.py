from pathlib import Path
import shutil

import nbformat
from nbclient import NotebookClient


def test_post01_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-01-initialization.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post02_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-02-integrators.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post03_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-03-errors.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post04_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-04-thermostats.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post05_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-05-barostats.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post06_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-06-trajectory-length.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post07_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-07-observables.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post08_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-08-free-energies.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post09_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-09-estimators.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post10_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-10-umbrella-sampling.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())


def test_post11_notebook_executes(tmp_path: Path) -> None:
    source = Path("notebooks/post-11-enhanced-sampling.ipynb")
    notebook_path = tmp_path / source.name
    shutil.copy(source, notebook_path)
    notebook = nbformat.read(notebook_path, as_version=4)
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    client.execute(cwd=Path.cwd())
