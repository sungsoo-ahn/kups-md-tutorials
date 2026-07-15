# Post 05 Review Notes

## Scope

- Post: 05
- Profiles reviewed: smoke and full
- Current status: controlled scalar-volume pressure/cell diagnostic workflow,
  compact reduced-unit argon cell-response workflow, committed smoke/full
  outputs, notebook, full-profile diagnostic figure, expanded hidden website
  draft, rendered page snapshots, and self-review artifact are in place; the
  final dynamic argon/kUPS NPT diagnostic is still pending.

## Commands

- `uv run kups-tutorial run 05 --profile smoke`
- `uv run kups-tutorial verify 05 --profile smoke`
- `uv run kups-tutorial run 05 --profile full`
- `uv run kups-tutorial verify 05 --profile full`
- `uv run python scripts/generate_post05_figures.py`
- `uv run jupyter execute notebooks/post-05-barostats.ipynb --inplace`
- `uv run ruff check .`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run kups-tutorial verify-artifacts`
- `git diff --check`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29360083501` for website commit
  `13ea87083b474465450efdcc503a0fdee06c6e6e`
- GitHub Actions snapshot run `29360274825`
- GitHub Actions tutorial verification run `29370738271` for tutorial commit
  `1e4d7724b5dabdeffab5406156e34bb744f67bff`
- GitHub Actions deploy run `29370738331` for website commit
  `943dde4d9094385516588f7c831dbf8512c3919f`
- GitHub Actions snapshot run `29370897946`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-05/`.
- Smoke and full outputs are committed under `results/post-05/`.
- The workflow uses a deterministic scalar-volume Ornstein-Uhlenbeck model with
  known NPT-like volume and pressure fluctuation targets.
- The workflow now also writes `argon_cell_response.csv`, a deterministic
  reduced-unit FCC argon pressure-volume sweep using affine box scaling,
  minimum-image periodic boundaries, and the Lennard-Jones virial pressure.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 05.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating barostat or plotting implementation details.

Open items:

- Add a dynamic argon/kUPS NPT diagnostic before treating this post as final.
  The current scalar model isolates fluctuation and memory concepts, and the
  compact argon sweep checks real coordinates/cell scaling, but it does not yet
  exercise moving-cell MD sampling.

## Scientific Review

- The full profile compares scalar barostat relaxation times `0.5`, `2.0`, and
  `8.0` at target pressure `1.0`, volume `1000`, compressibility `0.01`, and
  `kT = 1`.
- Full-profile volume and pressure variance estimates are within about 15% of
  the analytical targets.
- Volume autocorrelation time increases from about `2.0` for the fast barostat
  to about `22.5` for the slow barostat, supporting the claim that barostat
  time constants change memory and effective sampling.
- The compact full-profile argon response uses 108 atoms, reference reduced
  density `1.0`, volume factors `0.90` through `1.10`, fitted reduced-unit bulk
  response about `42.1`, and pressure span about `8.7`. The pressure decreases
  with expansion, so the virial sign and affine scaling are qualitatively
  consistent for this wiring check.
- The smoke profile uses fewer samples; verification tolerances are deliberately
  wider for fluctuation variance than for the full scientific review.

Open items:

- The website prose should not imply that pressure itself is tightly controlled
  instant by instant. Pressure fluctuations are the signal in small-system NPT.
- The final article should discuss isotropic versus flexible-cell coupling and
  finite-size effects using a dynamic argon/kUPS NPT workflow.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-05/barostat_diagnostics_snapshot.png`
- `snapshots/post-05/barostat_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable, target lines are visible in the
  volume and pressure panels, and the autocorrelation panel clearly increases
  with relaxation time.
- Compact argon cell-response refresh: the fourth panel is visible in the
  full-profile snapshot, the `V / V0` axis and reduced pressure labels fit, the
  pressure-volume trend is clear, and the `Kfit = 42.13`, `N = 108` annotation
  does not obscure the interpretation.
- The figure does not yet show dynamic NPT density relaxation or
  anisotropic/flexible-cell behavior. That is acceptable for this draft, but
  the final post should add a production cell-dynamics diagnostic if
  flexible-cell claims are made.

Open items:

- Add a production-cell dynamics figure after argon/kUPS NPT diagnostics are
  implemented.

## Notebook Review

- `notebooks/post-05-barostats.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, reports the compact argon response summary, and regenerates the
  full-profile diagnostic figure from committed result files.
- The notebook keeps the explanation focused on pressure fluctuations and cell
  memory rather than becoming the implementation source.

Open items:

- Add citations for NPT ensemble fluctuations, compressibility relations,
  barostat coupling, and finite-size pressure fluctuations before final
  publication.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post05_barostat_diagnostics.svg`.
- Expanded the hidden page from the short draft to about 3,606 words. The
  expanded prose explains pressure fluctuations, scalar-volume NPT-like
  diagnostics, barostat relaxation time, effective samples, initialization
  before NPT, cell-degree choices, thermostat/barostat interaction, and the
  compact atomistic argon cell-response check.
- The expanded prose keeps the scope clear: the committed result is a
  controlled scalar diagnostic plus a static argon pressure-volume sweep, not a
  final production NPT workflow with moving cell degrees of freedom.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29360083501` succeeded for commit
  `13ea87083b474465450efdcc503a0fdee06c6e6e`.
- Snapshot workflow run `29360274825` captured the expanded hidden page.
- Snapshot workflow run `29370897946` captured the compact argon cell-response
  refresh for website commit `943dde4d9094385516588f7c831dbf8512c3919f`.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post05-expanded-snapshots/`.
- Refreshed snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post05-argon-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-expanded-snapshots/manifest.json`.
- Refreshed manifest reviewed:
  `/tmp/kups-post05-argon-cell-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`; both
  returned HTTP 200 with page title
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post05-expanded-snapshots/post-05-desktop.png` and
  `/tmp/kups-post05-expanded-snapshots/post-05-mobile.png`.
- Refreshed rendered snapshots visually inspected:
  `/tmp/kups-post05-argon-cell-snapshots/post-05-desktop.png` and
  `/tmp/kups-post05-argon-cell-snapshots/post-05-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, several tables, full-profile
  barostat figure, reproduction code block, current-status section, references,
  and footer present. No blank page, missing figure, obvious clipping, or broken
  page chrome was found in the inspected snapshot.
- Mobile capture renders the same content through the mobile layout with the
  title, navigation, author note, tables, figure, code block, current-status
  section, and references present. Tables are tight but readable and are not
  clipped in the inspected snapshot.
- Refreshed desktop capture renders the compact argon cell-response article
  end to end with the updated four-panel figure, the argon configuration table,
  the reproduction command, current-status section, and references visible. No
  blank page, missing figure, obvious clipping, or broken page chrome was found
  in the inspected snapshot.
- Refreshed mobile capture renders the updated page with the four-panel figure
  present and legible. The narrow left navigation and tables are tight, as in
  earlier captures, but no blocking clipping or missing asset was found in the
  inspected snapshot.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Add final kUPS production NPT dynamics with full thermostat/barostat,
  energy/temperature, and pressure/cell diagnostics before public indexing.
- Re-run the page snapshot workflow again after final production-cell figures
  and citations are added.

## Update 2026-07-15: Reduced-Unit Argon Moving-Cell Diagnostic

Scope:

- Added an optional `argon_npt_dynamics` configuration block for Post 05 smoke
  and full profiles.
- Implemented a compact reduced-unit isotropic moving-cell argon diagnostic in
  `src/kups_md_tutorials/barostats.py`.
- Regenerated `results/post-05/`, `notebooks/post-05-barostats.ipynb`,
  `figures/post-05/`, and `snapshots/post-05/`.
- Refreshed the hidden website page and exported assets in
  `../sungsoo-ahn.github.io`.

Commands:

- `uv run kups-tutorial run 05 --profile smoke`
- `uv run kups-tutorial verify 05 --profile smoke`
- `uv run kups-tutorial run 05 --profile full`
- `uv run kups-tutorial verify 05 --profile full`
- `uv run python scripts/generate_post05_figures.py`
- `uv run jupyter execute notebooks/post-05-barostats.ipynb --inplace`
- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/barostats.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `git diff --check`
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full --posts 5`
- Website validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check`.

Code and reproducibility review:

- The new full-profile output `results/post-05/full/argon_npt_dynamics.csv`
  records time, volume factor, number density, and reduced pressure for the
  compact moving-cell diagnostic.
- `results/post-05/full/barostat_summary.json` now records
  `argon_npt_dynamics` with `1000` samples, `N = 108`, initial `V/V0 = 0.90`,
  mean `V/V0 = 0.9297`, mean density `1.0758`, mean pressure `1.0621` against
  target pressure `1.0`, volume-factor span `0.0532`, and volume effective
  samples `92.2`.
- The manifest records `argon_npt_dynamics_file:
  "argon_npt_dynamics.csv"` and the exact moving-cell configuration.
- The local run reported CPU fallback because CUDA-enabled `jaxlib` is not
  installed. That is acceptable for this deterministic reduced-unit hidden
  draft diagnostic and remains insufficient for a final kUPS production NPT
  article.
- Tutorial commit reviewed:
  `15d4536179235efbef89db82b03b02cbe26d2873`.
- Tutorial verify run: `29379747365`.

Scientific review:

- The compact moving-cell diagnostic starts from a compressed reduced-unit FCC
  argon cell and evolves an isotropic volume factor with pressure feedback and
  controlled noise.
- The full-profile mean pressure is close to the target, while the volume
  factor remains below one because the reduced-unit LJ virial pressure at this
  density balances near the compressed state. This is a useful sign and
  relaxation check, not an equation-of-state claim.
- The effective-sample count is much smaller than the stored sample count,
  which reinforces the article's point that slow cell variables reduce
  independent density/volume information.
- The diagnostic now exercises actual coordinates, periodic boundaries,
  pressure evaluation, and a moving isotropic cell; it still does not exercise
  a full kUPS production NPT trajectory with energy/temperature diagnostics.

Figure feedback:

- Inspected figure asset:
  `figures/post-05/barostat_diagnostics_full.svg`.
- Inspected snapshot:
  `snapshots/post-05/barostat_diagnostics_full_snapshot.png`.
- Intended visual claim: scalar fluctuation targets and barostat memory should
  be reviewed together with an atomistic moving-cell pressure/density check.
- The revised fourth panel is titled `Argon moving-cell check`, shows the
  volume factor trajectory, includes the `V/V0 = 1` reference line, and annotates
  `Neff = 92.2` and `Pmean = 1.06`.
- Labels, tick marks, and annotations fit inside the panel. The volume factor
  sits below one rather than relaxing exactly to one; this is accepted because
  it reflects the reduced-unit pressure balance and is described as a compact
  moving-cell check rather than a production NPT result.

Website review:

- Website commit reviewed:
  `1d822d55239551f8a1c07299f2386c5fe1fd4d31`.
- Website deploy run: `29379768876`.
- Live hidden-route check with `?v=1d822d5` confirmed the page contains the
  new `moving-cell` prose and no longer contains the stale phrase
  `does not yet run dynamic`.
- Snapshot workflow run: `29379867440`.
- Snapshot artifact downloaded to `/tmp/kups-post05-moving-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-moving-cell-snapshots/manifest.json`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post05-moving-cell-snapshots/post-05-desktop.png` and
  `/tmp/kups-post05-moving-cell-snapshots/post-05-mobile.png`.
- Desktop feedback: the page renders end to end with the updated author note,
  tables, moving-cell figure panel, reproduction block, Practical Checklist,
  Current Status, references, and footer present. The figure caption and prose
  now match the fourth panel.
- Mobile feedback: the title, sidebar links, tables, updated figure, code
  block, Current Status, references, and footer stay contained. Tables and the
  compact navigation remain dense, but no overlap, missing figure, or broken
  page chrome was found.

Release-readiness decision:

- The hidden draft now includes a compact reduced-unit moving-cell diagnostic
  and rendered page snapshots for that page state.
- Final public release still requires a real kUPS production NPT diagnostic
  with full thermostat/barostat settings, energy/temperature checks, final
  citations, and another desktop/mobile snapshot pass.

## Update 2026-07-15: Replica Moving-Cell Temperature/Energy Refresh

Scope:

- Strengthened the optional `argon_npt_dynamics` configuration block for Post
  05 smoke and full profiles with explicit `replica_count`.
- Regenerated `results/post-05/`, `figures/post-05/`,
  `snapshots/post-05/`, and `notebooks/post-05-barostats.ipynb`.
- Refreshed the hidden website page prose and exported Post 05 website assets
  in `../sungsoo-ahn.github.io`.

Commands:

- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/barostats.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py` passed.
- `uv run pytest tests/test_config.py::test_load_barostat_spec -q` passed.
- `uv run kups-tutorial run 05 --profile smoke` passed with CPU fallback.
- `uv run kups-tutorial verify 05 --profile smoke` passed.
- `uv run kups-tutorial run 05 --profile full` was interrupted after the
  first four-replica attempt proved too slow for the pure-NumPy pair-pressure
  loop.
- `uv run kups-tutorial run 05 --profile full` passed after scaling the full
  moving-cell diagnostic to three replicas and 10,000 steps.
- `uv run kups-tutorial verify 05 --profile full` passed.
- `uv run python scripts/generate_post05_figures.py` passed.
- `uv run jupyter execute notebooks/post-05-barostats.ipynb --inplace` passed.
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q` passed with 49 tests and 62 warnings.
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full --posts 5` passed.
- In `../sungsoo-ahn.github.io`, `python3 scripts/validate_kups_pages.py`
  passed.
- In `../sungsoo-ahn.github.io`, `python3 scripts/validate_blog.py` passed
  with pre-existing unused-image warnings.
- In both repositories, `git diff --check` passed after fixing Post 05 CSV
  line endings.
- `uv run kups-tutorial verify-artifacts` passed.
- `uv run kups-tutorial verify-reviews` passed.

Code and reproducibility review:

- `configs/post-05/smoke.json` now sets `argon_npt_dynamics.replica_count` to
  `2`.
- `configs/post-05/full.json` now sets `argon_npt_dynamics.replica_count` to
  `3`, `num_steps` to `10000`, and `warmup_steps` to `2000`. This preserves a
  replica uncertainty check while keeping the O(N^2) reduced-unit pressure loop
  practical for CI.
- `results/post-05/full/argon_npt_dynamics.csv` now records `time`,
  `replica_index`, `volume_factor`, `number_density`, `pressure`,
  `kinetic_temperature`, `potential_energy_per_atom`, and
  `total_energy_per_atom`.
- `results/post-05/full/barostat_summary.json` records `argon_npt_dynamics`
  with `1200` samples, `N = 108`, `3` replicas, initial `V/V0 = 0.90`, mean
  `V/V0 = 0.9315 +/- 0.00008`, mean density `1.0736 +/- 0.00009`, mean
  pressure `0.9255 +/- 0.0052` against target `1.0`, mean kinetic temperature
  `0.6988 +/- 0.0009` against target `0.70`, volume-factor effective samples
  `96.0`, and maximum absolute sampled total-energy change `0.1205` per atom.
- The local run reported CPU fallback because CUDA-enabled `jaxlib` is not
  installed. This remains acceptable for the hidden reduced-unit diagnostic and
  insufficient for final public NPT claims.

Scientific review:

- The refreshed moving-cell diagnostic now distinguishes within-run samples
  from independent replicas. Pressure and density claims use replica-level
  standard errors rather than a single trajectory mean.
- The kinetic-temperature trace tests the thermostat side of the NPT review
  habit: the full-profile mean is close to the configured target, but the
  trace remains noisy, as expected for a small reduced-unit system.
- The total-energy-per-atom trace is not an NVE conservation claim because the
  moving-cell update is stochastic and pressure-coupled. It is retained as a
  sanity signal for hidden integration or pressure-feedback pathologies.
- The pressure mean remains below the target by about `0.075` reduced pressure
  units. This is accepted for the hidden draft because the diagnostic is a
  compact pressure-feedback wiring check, not a calibrated equation-of-state
  result. The prose now states this limitation explicitly.
- The final public article still requires a real kUPS production NPT run with
  full atomistic thermostat/barostat settings, GPU provenance, and production
  stress/cell diagnostics.

Figure feedback:

- Source data inspected:
  `results/post-05/full/barostat_summary.json` and
  `results/post-05/full/argon_npt_dynamics.csv`.
- Figure assets inspected:
  `figures/post-05/barostat_diagnostics_full.svg` and
  `figures/post-05/barostat_diagnostics.svg`.
- Snapshot paths inspected:
  `snapshots/post-05/barostat_diagnostics_full_snapshot.png` (`1728 x 1152`)
  and `snapshots/post-05/barostat_diagnostics_snapshot.png` (`1728 x 1152`).
- Intended visual claim: the figure should show scalar fluctuation targets and
  barostat memory together with a compact atomistic moving-cell check that
  includes replica volume uncertainty and kinetic-temperature behavior.
- Full snapshot feedback: labels and tick marks fit in all four panels. The
  fourth panel now shows mean `V/V0` with a pale replica-spread band, a
  right-axis kinetic-temperature trace, a `V/V0 = 1` reference line, and an
  annotation with `replicas = 3`, `Neff = 96.0`, and `P = 0.93 +/- 0.01`. The
  annotation does not obscure the main trajectory, and the right-axis label is
  readable.
- Smoke snapshot feedback: the same visual structure remains readable with the
  smaller 32-atom, two-replica run. The kinetic-temperature trace is noisier
  and the pressure mean is farther from the target, which is acceptable for a
  smoke profile and not used for final prose claims.
- Revision decision: accepted for hidden draft. No blocking figure layout issue
  was found. The figure still does not show a real kUPS production NPT
  trajectory or flexible-cell behavior, so that remains a final-release
  blocker.

Website review:

- Hidden website page updated at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- The prose now states the three-replica full-profile metrics, pressure SEM,
  kinetic-temperature mean, and total-energy sanity signal.
- Website commit reviewed:
  `06cbf7c59f4f40eb79675d60be1d9dc58f588456`.
- Website deploy run: `29386632830`.
- Snapshot workflow run: `29386749372`.
- Snapshot artifact: `kups-md-page-snapshots`.
- Snapshot artifact downloaded to
  `/tmp/kups-post05-replica-moving-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-replica-moving-cell-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`; both
  returned HTTP 200 with page title
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post05-replica-moving-cell-snapshots/post-05-desktop.png`
  (`1440 x 12267`) and
  `/tmp/kups-post05-replica-moving-cell-snapshots/post-05-mobile.png`
  (`616 x 19414`).
- Desktop feedback: the page renders end to end with sidebar table of contents,
  updated three-replica prose, source links, tables, refreshed four-panel
  figure, caption, reproduction block, Practical Checklist, Current Status,
  references, and footer present. The updated figure panel is visible and not
  clipped.
- Mobile feedback: the long title, navigation, author note, tables, refreshed
  figure, caption, code block, Current Status, references, and footer remain
  contained. The figure is small at mobile width but readable enough for the
  hidden draft, and no missing asset, broken page chrome, or overlap was found.
- Live hidden-route check with `?v=06cbf7c` confirmed the page contains
  `three moving-cell replicas`, `0.925 +/- 0.005`, `kinetic temperature is
  0.699`, and the refreshed figure asset path. The public home and blog pages
  do not expose `kups-md-tutorials` or `post-05-barostats`.

Release-readiness decision:

- Blocking items for the current hidden draft: none found after local figure
  inspection, website validation, and rendered page snapshot review.
- Non-blocking items accepted until the final article pass: mobile tables and
  compact figure density remain acceptable for the hidden page state.
- Final-release blockers:
  - Run and review a real kUPS production NPT diagnostic with full atomistic
    thermostat/barostat settings, GPU provenance, and production stress/cell
    checks.
  - Add final citations for NPT ensemble fluctuations, compressibility,
    barostat coupling, and finite-size pressure fluctuations.
  - Re-run rendered desktop/mobile page snapshots after final production NPT
    diagnostics or public-indexing changes.
