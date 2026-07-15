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

## Update 2026-07-15: Fresh-Kernel Mode And Source-Immutability Evidence

Scope:

- Hardened the notebook execution manifest and release-readiness checker so
  the clean-kernel evidence explicitly records `execution_mode:
  fresh_kernel_per_notebook`, each executed notebook copy path, each source
  notebook SHA-256 before and after execution, `source_unchanged: true`, and
  positive elapsed time for every notebook.
- Re-executed all twelve committed notebooks from clean kernels and replaced
  the committed compact ledger at `reviews/notebook-execution.json`.

Command:

```bash
uv run kups-tutorial verify-notebooks --output-dir /tmp/kups-notebook-mode-ledger
```

Result:

- Passed.
- Temporary manifest path: `/tmp/kups-notebook-mode-ledger/manifest.json`.
- Committed ledger path: `reviews/notebook-execution.json`.
- Source revision recorded by the temporary manifest:
  `24d7bdffa19a74dc34ab2fb1739441882f4f6aed`.
- Execution mode: `fresh_kernel_per_notebook`.
- Kernel: `python3`.
- Timeout: 120 seconds per cell.
- Jupyter emitted the same local TCP transport warnings as earlier clean-kernel
  runs. No notebook failed; the warnings do not indicate execution errors.

Execution summary:

| Post | Notebook | Code cells | Executed cells | Outputs | Source unchanged |
|---|---|---:|---:|---:|---|
| 01 | `post-01-initialization.ipynb` | 6 | 6 | 7 | yes |
| 02 | `post-02-integrators.ipynb` | 6 | 6 | 6 | yes |
| 03 | `post-03-errors.ipynb` | 7 | 7 | 7 | yes |
| 04 | `post-04-thermostats.ipynb` | 6 | 6 | 6 | yes |
| 05 | `post-05-barostats.ipynb` | 6 | 6 | 7 | yes |
| 06 | `post-06-trajectory-length.ipynb` | 5 | 5 | 4 | yes |
| 07 | `post-07-observables.ipynb` | 5 | 5 | 4 | yes |
| 08 | `post-08-free-energies.ipynb` | 5 | 5 | 4 | yes |
| 09 | `post-09-estimators.ipynb` | 5 | 5 | 4 | yes |
| 10 | `post-10-umbrella-sampling.ipynb` | 5 | 5 | 4 | yes |
| 11 | `post-11-enhanced-sampling.ipynb` | 5 | 5 | 4 | yes |
| 12 | `post-12-mlip-capstone.ipynb` | 5 | 5 | 4 | yes |

Review decision:

- Accepted for the notebook-execution evidence milestone. The release-surface
  audit now fails if the notebook ledger omits fresh-kernel execution mode,
  source-immutability hashes, source-unchanged flags, executed-copy paths, or
  elapsed-time evidence.
- No figure snapshot or rendered-page snapshot capture was required because
  this pass changed only verifier code, tests, and notebook execution ledgers;
  notebook sources, result summaries, figures, website pages, CSS-sensitive
  markup, and linked publication assets were unchanged.
- Final public release still requires rerunning the same strengthened
  clean-kernel ledger after final GPU summaries, final figures, and public
  article edits are frozen.
