# Post 03 Review Notes

## Scope

- Post: 03
- Profiles reviewed: smoke and full
- Current status: controlled timestep/precision/force-error diagnostic workflow
  plus a 256-atom, three-replica reduced-unit argon NVE diagnostic, committed
  smoke/full outputs, notebook, full-profile diagnostic figure, expanded hidden
  website draft, rendered page snapshots, and self-review artifact are in place.

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
- `uv run kups-tutorial export-site --profile full`
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
- The workflow now also includes a deterministic 256-atom argon NVE diagnostic:
  reduced-unit Lennard-Jones argon FCC cells, seeded velocities with
  center-of-mass removal and exact target kinetic temperature, three
  independent velocity-seed replicas per timestep, vectorized minimum-image
  forces, velocity Verlet, and downsampled energy traces in
  `argon_nve_samples.csv`.
- The argon NVE protocol summary records the protocol label
  `gpu_ready_lj_nve_replicas`, target device `cuda_or_cpu_fallback`, replica
  count, drift/error extrema, and replica drift standard error.
- CSV writers now use Unix line endings so regenerated and exported result
  files pass `git diff --check`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 03.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating the diagnostic implementation.

Open items:

- Replace or augment the CPU-fallback reduced-unit argon check with a real
  CUDA/GPU kUPS production NVE diagnostic before treating this post as final.
  The current argon run is a stronger physical many-body sanity check, not the
  target production MD experiment described in the plan.

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
- The full argon NVE protocol contains 256 atoms at reduced density `0.65` and
  temperature `0.70`, with 3 velocity-seed replicas for each reduced timestep
  `0.0015`, `0.003`, and `0.006`.
- Across the 9 argon NVE runs, the maximum relative energy error is
  `2.65e-4`, the maximum absolute normalized drift is `3.12e-5`, the mean
  absolute normalized drift is `1.47e-5`, the largest replica drift standard
  error is `2.79e-6`, and no run is marked unstable.
- The argon result supports a bounded-energy sanity check for a many-body
  system with initialization sensitivity represented by replicas, but it is not
  a CUDA/GPU kUPS production benchmark and should not be described as final
  production evidence.

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
- New replica argon NVE pass: the first four-panel full-profile snapshot at
  `1728 x 1120` had readable axes and uncertainty bands, but the lower-right
  NVE legend overlapped the longest-time green trace.
- Revised the NVE legend to the upper-right and regenerated the figure. The
  second snapshot moved the legend off the trace but left the legend title
  sitting directly on the zero-reference line.
- Added a framed legend with `framealpha=0.85` and regenerated
  `snapshots/post-03/error_diagnostics_full_snapshot.png`. The final inspected
  pass keeps the timestep, precision, force-bias, and NVE panels readable; the
  256-atom/3-replica legend no longer obscures the energy-drift interpretation,
  and the replica standard-deviation bands remain visible.

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
- The notebook now includes an argon NVE protocol check reporting
  `gpu_ready_lj_nve_replicas`, `cuda_or_cpu_fallback`, 256 atoms, 3 replicas,
  and maximum drift standard error `2.794e-06`.
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
- GitHub Pages deploy `29383806796` built and deployed website commit
  `e31de95f84635b1ba81a9644b195dcc4f7d6f54d2` successfully after adding the
  256-atom, three-replica NVE protocol refresh.
- The deployed page snapshot manifest from workflow `29358450830` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.
- The deployed page snapshot manifest from workflow `29368819123` contains
  desktop and mobile captures for the updated hidden URL, both HTTP 200, with
  title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.
- The deployed page snapshot manifest from workflow `29383922778` contains
  desktop and mobile captures for the replica NVE hidden URL, both HTTP 200,
  with title
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post03-expanded-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-expanded-snapshots/post-03-mobile.png`
- `/tmp/kups-post03-argon-nve-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-argon-nve-snapshots/post-03-mobile.png`
- `/tmp/kups-post03-replica-nve-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-replica-nve-snapshots/post-03-mobile.png`

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
- Replica NVE desktop capture at `1440 x 11452` renders the hidden draft end to
  end with sidebar TOC, updated full-profile NVE protocol table, refreshed
  four-panel figure, reproduction block, Current Status section, references, and
  footer present. No missing figure, clipped table, blank region, or broken page
  chrome was found in the inspected snapshot.
- Replica NVE mobile capture at `453 x 18146` renders the long title, draft
  note, tables, refreshed figure, caption, code block, Current Status section,
  references, and footer. Tables are dense but contained, and the figure is
  small at mobile width but not clipped.
- Live checks with cache-buster `?v=e31de95` confirmed the direct hidden post
  contains `gpu_ready_lj_nve_replicas` and `256-atom`; the hidden kUPS index
  links to Post 03; `/` and `/blog/` do not expose `kups-md-tutorials` or
  `post-03-errors`.

Open items:

- The page remains intentionally hidden from public navigation.
- Add a larger GPU kUPS production NVE diagnostic before treating this post as
  final.
