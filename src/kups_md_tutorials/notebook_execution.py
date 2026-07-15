"""Clean-kernel execution helpers for tutorial notebooks."""

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import shutil
import time

import nbformat
from nbclient import NotebookClient

from kups_md_tutorials.provenance import file_sha256, git_revision

NOTEBOOKS = (
    ("01", "post-01-initialization.ipynb"),
    ("02", "post-02-integrators.ipynb"),
    ("03", "post-03-errors.ipynb"),
    ("04", "post-04-thermostats.ipynb"),
    ("05", "post-05-barostats.ipynb"),
    ("06", "post-06-trajectory-length.ipynb"),
    ("07", "post-07-observables.ipynb"),
    ("08", "post-08-free-energies.ipynb"),
    ("09", "post-09-estimators.ipynb"),
    ("10", "post-10-umbrella-sampling.ipynb"),
    ("11", "post-11-enhanced-sampling.ipynb"),
    ("12", "post-12-mlip-capstone.ipynb"),
)


@dataclass(frozen=True)
class NotebookExecution:
    """Execution record for one notebook."""

    post: str
    source: str
    executed_copy: str
    source_sha256: str
    source_sha256_after: str
    source_unchanged: bool
    code_cells: int
    executed_code_cells: int
    output_count: int
    elapsed_seconds: float


@dataclass(frozen=True)
class NotebookExecutionManifest:
    """Manifest for one clean-kernel notebook verification run."""

    source_git_revision: str
    execution_mode: str
    kernel_name: str
    timeout_seconds: int
    notebooks: tuple[NotebookExecution, ...]


def execute_notebooks(
    notebooks_dir: Path = Path("notebooks"),
    output_dir: Path = Path("notebook-runs"),
    posts: tuple[str, ...] | None = None,
    kernel_name: str = "python3",
    timeout_seconds: int = 120,
    cwd: Path = Path("."),
) -> Path:
    """Execute selected tutorial notebooks from clean kernels."""

    selected_posts = {post.zfill(2) for post in posts} if posts is not None else None
    records: list[NotebookExecution] = []
    output_dir.mkdir(parents=True, exist_ok=True)
    for post, filename in NOTEBOOKS:
        if selected_posts is not None and post not in selected_posts:
            continue
        source = notebooks_dir / filename
        if not source.exists():
            msg = f"missing notebook for post {post}: {source}"
            raise FileNotFoundError(msg)

        source_sha256_before = file_sha256(source)
        executed_copy = output_dir / filename
        shutil.copyfile(source, executed_copy)
        notebook = nbformat.read(executed_copy, as_version=4)
        start = time.monotonic()
        client = NotebookClient(
            notebook,
            timeout=timeout_seconds,
            kernel_name=kernel_name,
        )
        client.execute(cwd=cwd)
        elapsed = time.monotonic() - start
        nbformat.write(notebook, executed_copy)
        source_sha256_after = file_sha256(source)
        code_cells = [
            cell for cell in notebook.cells if cell.get("cell_type") == "code"
        ]
        records.append(
            NotebookExecution(
                post=post,
                source=str(source),
                executed_copy=str(executed_copy),
                source_sha256=source_sha256_before,
                source_sha256_after=source_sha256_after,
                source_unchanged=source_sha256_before == source_sha256_after,
                code_cells=len(code_cells),
                executed_code_cells=sum(
                    1 for cell in code_cells if cell.get("execution_count") is not None
                ),
                output_count=sum(len(cell.get("outputs", [])) for cell in code_cells),
                elapsed_seconds=round(elapsed, 3),
            )
        )

    if not records:
        msg = "no notebooks selected for execution"
        raise ValueError(msg)

    manifest = NotebookExecutionManifest(
        source_git_revision=git_revision(cwd),
        execution_mode="fresh_kernel_per_notebook",
        kernel_name=kernel_name,
        timeout_seconds=timeout_seconds,
        notebooks=tuple(records),
    )
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path
