# Clean Notebook Execution Review

## Scope and Provenance

- Date: 2026-07-14.
- Scope: all twelve committed tutorial notebooks.
- Source commit: `2e58c16a16d56c2feb21d82a44901ce3824076e4`.
- Command:

```bash
uv run kups-tutorial verify-notebooks --output-dir notebook-runs
```

- Result: passed.
- Manifest path: `notebook-runs/manifest.json`.
- Manifest status: generated and intentionally untracked because it points to
  executed notebook copies under ignored `notebook-runs/`.
- Kernel: `python3`.
- Timeout: 120 seconds per cell.

During execution, IPython emitted local TCP transport warnings for each kernel.
No notebook failed; the warnings do not indicate notebook execution errors.

## Executed Notebooks

| Post | Notebook | Code cells | Executed cells | Outputs |
|---|---|---:|---:|---:|
| 01 | `post-01-initialization.ipynb` | 6 | 6 | 6 |
| 02 | `post-02-integrators.ipynb` | 6 | 6 | 6 |
| 03 | `post-03-errors.ipynb` | 6 | 6 | 6 |
| 04 | `post-04-thermostats.ipynb` | 6 | 6 | 6 |
| 05 | `post-05-barostats.ipynb` | 6 | 6 | 7 |
| 06 | `post-06-trajectory-length.ipynb` | 5 | 5 | 4 |
| 07 | `post-07-observables.ipynb` | 5 | 5 | 4 |
| 08 | `post-08-free-energies.ipynb` | 5 | 5 | 4 |
| 09 | `post-09-estimators.ipynb` | 5 | 5 | 4 |
| 10 | `post-10-umbrella-sampling.ipynb` | 5 | 5 | 4 |
| 11 | `post-11-enhanced-sampling.ipynb` | 5 | 5 | 4 |
| 12 | `post-12-mlip-capstone.ipynb` | 5 | 5 | 4 |

## Review Status

- Blocking items for current hidden drafts: none from notebook execution.
- Non-blocking items accepted until the final article pass: notebooks remain
  presentation layers and rely on committed compact outputs rather than raw
  production trajectories.
- Final-release blockers: rerun `verify-notebooks` after final GPU summaries,
  final figures, and public article edits are frozen.
