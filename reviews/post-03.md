# Post 03 Review Notes

## Scope

- Post: 03
- Profiles reviewed: smoke and full
- Current status: controlled timestep/precision/force-error diagnostic workflow
  plus compact reduced-unit argon NVE diagnostic, committed smoke/full outputs,
  notebook, full-profile diagnostic figure, expanded hidden website draft,
  rendered page snapshots, and self-review artifact are in place.

## Commands

- `uv run kups-tutorial run 03 --profile smoke`
- `uv run kups-tutorial verify 03 --profile smoke`
- `uv run kups-tutorial run 03 --profile full`
- `uv run kups-tutorial verify 03 --profile full`
- `uv run python scripts/generate_post03_figures.py`
- `uv run jupyter execute notebooks/post-03-errors.ipynb --inplace`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/error_diagnostics.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `git diff --check`
- `uv run kups-tutorial export-site --posts 03 --profile full`
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
- The workflow now also includes a deterministic compact argon NVE diagnostic:
  reduced-unit Lennard-Jones argon FCC cells, seeded velocities with
  center-of-mass removal and exact target kinetic temperature, vectorized
  minimum-image forces, velocity Verlet, and downsampled energy traces in
  `argon_nve_samples.csv`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 03.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating the diagnostic implementation.

Open items:

- Replace or augment the compact reduced-unit argon check with a larger GPU
  kUPS production NVE diagnostic before treating this post as final. The
  current argon run is a physical many-body sanity check, not the target
  production MD experiment described in the plan.

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
- The full compact argon NVE diagnostic contains 108 atoms at reduced density
  `0.65` and temperature `0.70`. Across reduced timesteps `0.0015`, `0.003`,
  and `0.006`, the maximum relative energy error stays below `2.7e-4`; the
  largest-timestep normalized drift is about `-8.5e-6`.
- The argon result supports a bounded-energy sanity check for a many-body
  system, but it is not a GPU kUPS production benchmark and should not be
  described as final production evidence.

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
- New compact argon NVE pass: the first four-panel full-profile snapshot at
  `1728 x 1120` had readable axes and legend, but the "108 Ar atoms" annotation
  sat on top of the initial NVE traces.
- Revised the NVE annotation into the legend title and regenerated
  `snapshots/post-03/error_diagnostics_full_snapshot.png`. The revised pass
  leaves the trace data unobscured, preserves readable tick labels at the
  snapshot size, and shows the largest-timestep trace as bounded rather than
  unstable. The caption and panel title now match the compact argon NVE claim.

Open items:

- Consider adding a trajectory-error panel in the final article if phase error
  becomes a major prose claim.
- Repeat figure snapshot review after any larger GPU kUPS NVE production panel
  is added.

## Notebook Review

- `notebooks/post-03-errors.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on error mechanisms rather than
  becoming the implementation source.

Open items:

- Re-execute the notebook if the final article adds a trajectory-error panel or
  a larger GPU kUPS NVE diagnostic figure.

## Website Draft Review

- Added, expanded, and deployed a hidden draft page in
  `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG/PNG figure and compact full-profile
  result files, including `argon_nve_samples.csv`, to
  `../sungsoo-ahn.github.io/assets/` via `uv run kups-tutorial export-site
  --posts 03 --profile full`.
- Expanded the article body from about 756 words to about 3,703 words. The
  expanded draft now separates timestep sensitivity, precision floors, force
  bias, normalized drift, compact argon NVE behavior, phase error,
  NVE error-report interpretation, neighbor-list/cutoff artifacts, MLIP
  workflow controls, and final-release limitations.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes in the website repository with
  pre-existing unused-image warnings.
- `git diff --check` passes in the website repository.
- GitHub Pages deploy `29358250043` built and deployed website commit
  `ebf717a523ff21f9475abc6e04515db8e98e13e4` successfully.
- GitHub Pages deploy `29368638564` built and deployed updated website commit
  `c33b1adc726f91eb4a1f258f6e2a5e2e3651d69d` successfully after adding the
  compact argon NVE figure/prose refresh.
- The deployed page snapshot manifest from workflow `29358450830` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.
- The deployed page snapshot manifest from workflow `29368819123` contains
  desktop and mobile captures for the updated hidden URL, both HTTP 200, with
  title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post03-expanded-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-expanded-snapshots/post-03-mobile.png`
- `/tmp/kups-post03-argon-nve-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-argon-nve-snapshots/post-03-mobile.png`

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
- Updated desktop full-page capture at `1440 x 10796` renders the revised
  four-panel figure, caption, source links, reproduction block, current-status
  list, references, and footer. The new compact argon NVE panel is visible in
  the article body; no missing figure, blank page, obvious clipped text, or
  broken page chrome was found in the inspected snapshot.
- Updated mobile full-page capture at `390 x 16893` renders the long title,
  hidden-draft note, mechanism table, revised figure, caption, timestep-choice
  table, code block, current-status list, and references within the viewport.
  The four-panel figure is small at mobile width but not clipped; table cells
  wrap tightly but remain contained.

Open items:

- The page remains intentionally hidden from public navigation.
- Add a larger GPU kUPS production NVE diagnostic before treating this post as
  final.
