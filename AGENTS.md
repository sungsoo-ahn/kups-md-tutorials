# Repository Guidelines

## Project Structure & Module Organization

This repository is an early Python scaffold for executable kUPS molecular-dynamics tutorials. `PROJECT.md` defines the scientific scope and publication requirements; read it before changing experiment behavior. `hello.py` is the current entry point, while `pyproject.toml` and `uv.lock` define the Python 3.13 environment.

As the first tutorial is implemented, keep reusable simulation and analysis code under `src/`, tests under `tests/`, executable narratives under `notebooks/`, and lightweight experiment settings under `configs/`. Store publication-ready figures in a clearly named asset directory such as `figures/`. Do not commit trajectories, caches, or other large generated outputs.

## Build, Test, and Development Commands

- `uv sync`: create or update `.venv` from `pyproject.toml` and `uv.lock`.
- `uv run python hello.py`: run the current smoke entry point.
- `uv run python -m pytest`: run the test suite once pytest and `tests/` are added.

When dependencies change, update both `pyproject.toml` and `uv.lock`. Prefer commands executed through `uv run` so results use the locked environment.

## Coding Style & Naming Conventions

Use four-space indentation, type hints for public functions, and short docstrings for scientific assumptions or units. Follow Python conventions: `snake_case` for modules, functions, variables, and configuration files; `PascalCase` for classes; `UPPER_SNAKE_CASE` for constants. Keep notebooks as presentation layers and move reusable logic into `src/`. No formatter or linter is configured yet; keep changes PEP 8-compatible and avoid introducing tooling without declaring it in `pyproject.toml`.

## Testing & Reproducibility

No test framework or coverage threshold is currently configured. New simulation logic should include focused unit tests named `tests/test_<module>.py`; add integration tests for the CPU smoke workflow. Fix random seeds, reuse identical initial states across timestep comparisons, record software versions and configuration, and test numerical invariants with explicit tolerances. Never rely only on visual trajectory inspection.

## Commit & Pull Request Guidelines

The existing history uses Conventional Commit style (`chore: initialize kUPS tutorial project`). Continue with concise prefixes such as `feat:`, `fix:`, `test:`, `docs:`, and `chore:`. Pull requests should explain the scientific or user-visible change, list reproduction commands, identify configuration and seed values, and link relevant issues. Include updated plots or notebook screenshots when outputs change, and note any expected numerical differences.
