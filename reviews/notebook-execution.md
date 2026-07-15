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

## Update 2026-07-15: Machine-Checkable Execution Ledger

Scope:

- Re-executed all twelve committed notebooks from clean kernels after the
  website export-manifest gate work.
- Added `reviews/notebook-execution.json` as a compact committed ledger of the
  notebook source paths, source SHA-256 digests, code-cell counts, executed
  code-cell counts, output counts, kernel, timeout, and source revision used
  for the clean execution check.

Command:

```bash
uv run kups-tutorial verify-notebooks --output-dir /tmp/kups-notebook-runs
```

Result:

- Passed.
- Temporary manifest path: `/tmp/kups-notebook-runs/manifest.json`.
- Committed ledger path: `reviews/notebook-execution.json`.
- Source revision recorded by the temporary manifest:
  `8469eb3487f555284a0ba6c6d519fda08487de26`.
- Kernel: `python3`.
- Timeout: 120 seconds per cell.
- Jupyter again emitted local TCP transport warnings. No notebook failed; the
  warnings do not indicate execution errors.

Execution summary:

| Post | Notebook | Code cells | Executed cells | Outputs |
|---|---|---:|---:|---:|
| 01 | `post-01-initialization.ipynb` | 6 | 6 | 7 |
| 02 | `post-02-integrators.ipynb` | 6 | 6 | 6 |
| 03 | `post-03-errors.ipynb` | 7 | 7 | 7 |
| 04 | `post-04-thermostats.ipynb` | 6 | 6 | 6 |
| 05 | `post-05-barostats.ipynb` | 6 | 6 | 7 |
| 06 | `post-06-trajectory-length.ipynb` | 5 | 5 | 4 |
| 07 | `post-07-observables.ipynb` | 5 | 5 | 4 |
| 08 | `post-08-free-energies.ipynb` | 5 | 5 | 4 |
| 09 | `post-09-estimators.ipynb` | 5 | 5 | 4 |
| 10 | `post-10-umbrella-sampling.ipynb` | 5 | 5 | 4 |
| 11 | `post-11-enhanced-sampling.ipynb` | 5 | 5 | 4 |
| 12 | `post-12-mlip-capstone.ipynb` | 5 | 5 | 4 |

Review decision:

- Accepted for the notebook-execution tooling milestone.
- No figure snapshot or rendered-page snapshot capture was required because no
  notebook source, figure asset, website page, CSS-sensitive markup, or linked
  figure changed in this pass.
- Final public release still requires rerunning the same clean-kernel ledger
  after final GPU summaries, final figures, and public article edits are
  frozen.
