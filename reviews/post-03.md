# Post 03 Review Notes

## Scope

- Post: 03
- Profiles reviewed: smoke and full
- Current status: controlled timestep/precision/force-error diagnostic workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  expanded hidden website draft, rendered page snapshots, and self-review
  artifact are in place.

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
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`
- GitHub Pages deploy `29358250043` for website commit
  `ebf717a523ff21f9475abc6e04515db8e98e13e4`.
- GitHub Actions snapshot workflow `29358450830` for post 03.

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
- Keep the distinction among bounded energy oscillation, normalized drift,
  instability, and position/phase error in the final all-post consistency pass.

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

- Re-execute the notebook if the final article adds a trajectory-error panel or
  an argon/kUPS NVE diagnostic figure.

## Website Draft Review

- Added, expanded, and deployed a hidden draft page in
  `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post03_error_diagnostics.svg`.
- Expanded the article body from about 756 words to about 3,703 words. The
  expanded draft now separates timestep sensitivity, precision floors, force
  bias, normalized drift, phase error, NVE error-report interpretation,
  neighbor-list/cutoff artifacts, MLIP workflow controls, and final-release
  limitations.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes in the website repository with
  pre-existing unused-image warnings.
- `git diff --check` passes in the website repository.
- GitHub Pages deploy `29358250043` built and deployed website commit
  `ebf717a523ff21f9475abc6e04515db8e98e13e4` successfully.
- The deployed page snapshot manifest from workflow `29358450830` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post03-expanded-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-expanded-snapshots/post-03-mobile.png`

Rendered feedback:

- Desktop full-page capture renders the expanded article end to end: sidebar
  table of contents, mechanism table, diagnostic figure, timestep-choice table,
  reproduction code block, current-status section, references, and footer are
  present. No missing asset, blank page, obvious clipped text, or broken page
  chrome was found in the inspected snapshot. The final-release argon/kUPS NVE
  limitation is visible in Current Status.
- Mobile full-page capture renders the title, author note, tables, figure, code
  block, status, references, and footer. The two tables are tight but readable
  and not clipped in the inspected screenshot. Keep table wrapping as a final
  typography-polish item after the remaining articles are expanded.

Open items:

- The page remains intentionally hidden from public navigation.
- Add an argon/kUPS NVE diagnostic before treating this post as final.
- Perform a final all-post consistency pass after the other articles are
  expanded.
- Re-capture rendered desktop and mobile snapshots after that final consistency
  pass.
