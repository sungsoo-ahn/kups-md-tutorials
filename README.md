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
```

On an NVIDIA CUDA workstation, install the GPU and model-download extras with
`uv sync --extra gpu --extra mlff`. Full profiles write raw HDF5 trajectories
under ignored `runs/` directories and commit only compact summaries,
provenance manifests, and publication figures.

See `PLAN.md` for the twelve-post curriculum, scientific requirements,
progress, and final verification checklist.
