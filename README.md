# kUPS Molecular Dynamics Tutorials

Executable, reproducible molecular dynamics tutorials for MLIP-aware
machine-learning researchers. The simulations use the Python API of
[kUPS](https://github.com/cusp-ai-oss/kUPS); polished articles are published in
the adjacent `sungsoo-ahn.github.io` repository.

## Setup

```bash
uv sync
uv run kups-tutorial run 01 --profile smoke
uv run kups-tutorial verify --profile smoke
uv run kups-tutorial verify-artifacts
uv run kups-tutorial verify-reviews
uv run kups-tutorial verify-notebooks
uv run kups-tutorial gpu-status
uv run kups-tutorial verify-release-readiness
uv run jupyter execute notebooks/post-01-initialization.ipynb --inplace
uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full
```

On an NVIDIA CUDA workstation, install the GPU and model-download extras with
`uv sync --extra gpu --extra mlff`. Full profiles write raw HDF5 trajectories
under ignored `runs/` directories and commit only compact summaries,
provenance manifests, and publication figures.

Use `uv run kups-tutorial gpu-status` to list full-profile artifacts that still
target CUDA/GPU but currently record CPU fallback, including the exact
`run`/`verify` commands to rerun before public release.

See `PLAN.md` for the twelve-post curriculum, scientific requirements,
progress, and final verification checklist.

`verify-release-readiness` is expected to fail while hidden drafts,
final-release blockers, or placeholder model artifacts remain. It is the
publication gate, not a routine development check.
