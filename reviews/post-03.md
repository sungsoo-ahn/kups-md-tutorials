# Post 03 Review Notes

## Scope

- Post: 03
- Profiles reviewed: smoke and full
- Current status: controlled timestep/precision/force-error diagnostic workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  hidden website draft, and self-review artifact are in place; final prose and
  rendered page snapshots are still pending.

## Commands

- `uv run kups-tutorial run 03 --profile smoke`
- `uv run kups-tutorial verify 03 --profile smoke`
- `uv run kups-tutorial run 03 --profile full`
- `uv run kups-tutorial verify 03 --profile full`
- `uv run python scripts/generate_post03_figures.py`
- `uv run jupyter execute notebooks/post-03-errors.ipynb --inplace`
- `uv run pytest -q`
- `uv run ruff check .`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`

## Code And Reproducibility Review

- Configs are committed under `configs/post-03/`.
- Smoke and full outputs are committed under `results/post-03/`.
- The workflow uses a deterministic velocity-Verlet oscillator with exact
  reference positions, configurable precision models, and deterministic
  force-scale perturbations.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 03.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating the diagnostic implementation.

Open items:

- Add rendered page snapshots after the hidden website draft deploys.
- Add an argon/kUPS NVE diagnostic before treating this post as final. The
  current oscillator is a controlled microscope for error mechanisms, not yet
  the target production MD experiment described in the plan.

## Scientific Review

- The full profile contains 48 runs: 4 timesteps, 4 precision models, and 3
  force-scale cases.
- Exact-force float64 max relative energy error increases from about `1.0e-4`
  at `dt = 0.02` to about `8.1e-3` at `dt = 0.18`, consistent with bounded
  timestep error.
- At `dt = 0.18`, rounded precision raises the exact-force max relative energy
  error from about `8.1e-3` (`float64`) to about `2.0e-2`
  (`rounded_1e-3`), showing a precision/rounding floor.
- At `dt = 0.18`, deterministic force scaling changes normalized energy drift.
  The low-force case shows a larger negative drift than the exact-force case,
  while the high-force case changes the sign.

Open items:

- The prose must not imply that all MLIP force errors are simple scale errors.
  This diagnostic isolates a readable failure mode; post 12 needs MLIP-specific
  extrapolation and instability checks.
- The final article should separate bounded energy oscillation, normalized
  drift, instability, and position/phase error rather than reporting a single
  scalar.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-03/error_diagnostics_snapshot.png`
- `snapshots/post-03/error_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels were readable, but the precision panel sorted
  labels alphabetically, which put `rounded_1e-3` before `rounded_1e-4` and made
  the mechanism harder to scan.
- Revised precision ordering to `float64`, `float32`, `rounded_1e-4`,
  `rounded_1e-3` and regenerated the figure and snapshot.
- Second pass: the three panels fit without overlap, the precision story reads
  left to right, and the force-bias panel clearly separates negative,
  near-zero, and positive normalized drift.

Open items:

- Recheck mobile rendering after the website draft exists.
- Consider adding a trajectory-error panel in the final article if phase error
  becomes a major prose claim.

## Notebook Review

- `notebooks/post-03-errors.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on error mechanisms rather than
  becoming the implementation source.

Open items:

- Add the full prose article in the website repository.
- Add citations for timestep stability, backward error analysis, mixed
  precision, and MLIP force-error diagnostics when writing the website draft.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post03_error_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Capture and inspect deployed desktop and mobile snapshots for this hidden
  page.
- Expand the draft into the full 3,500-10,000-word article after rendered page
  snapshots and the argon/kUPS NVE diagnostic are reviewed.
