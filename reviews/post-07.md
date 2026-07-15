# Post 07 Review Notes

## Scope

- Post: 07
- Profiles reviewed: smoke and full
- Current status: controlled argon-FCC observable-estimator workflow, compact
  reduced-unit argon trajectory observable workflow, committed smoke/full
  outputs, notebook, full-profile diagnostic figure, hidden website draft,
  rendered page snapshots, and self-review artifact are in place; larger GPU
  kUPS production trajectory observable diagnostics remain pending.

## Commands

- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- `uv run ruff check .`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run kups-tutorial verify-artifacts`
- `git diff --check`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29361737064` for website commit
  `2ae2434e4933fde7fe3f2241e18be00af913d159`
- GitHub Actions snapshot run `29361900585`
- GitHub Actions tutorial verify run `29372999316` for tutorial commit
  `e7961d3650c5c41fafca370782b61d80c305e21d`
- GitHub Actions deploy run `29372999672` for website commit
  `184a54fd81c3b4a38fe659839ee9427666d46324`
- GitHub Actions snapshot run `29373158618`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-07/`.
- Smoke and full outputs are committed under `results/post-07/`.
- The workflow uses deterministic periodic argon FCC cells with seeded thermal
  displacements, PBC minimum-image pair distances, RDF normalization,
  coordination integration, block standard errors, and a seeded velocity
  autocorrelation estimator.
- The workflow now also writes `argon_trajectory_rdf_samples.csv` and
  `argon_trajectory_vacf_samples.csv`, generated from a compact reduced-unit
  argon Langevin trajectory with actual sampled positions and velocities.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 07.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating RDF, coordination, or VACF implementation details.

Open items:

- Add larger GPU kUPS trajectory-observable diagnostics before treating this
  post as final. The compact reduced-unit trajectory exercises real
  time-correlated frames, but it is not yet a production kUPS observable study.

## Scientific Review

- The full profile compares a 32-atom cell and a 256-atom cell at number
  density `0.021` with the same seeded displacement scale.
- Both full-profile systems recover the first-neighbor coordination number near
  `12.0` using cutoff `4.6`.
- The larger system lowers the finite-size shell fraction from about `1.39` to
  about `0.70`, so the RDF can be interpreted over a larger radial interval.
- The RDF estimator masks radii beyond half the periodic box length for each
  system; the first implementation drew invalid small-cell shells, which was
  corrected before committing the review snapshot.
- The full-profile VACF has lag-1 autocorrelation about `0.921` and normalized
  integral about `12.0`, matching the configured correlated-velocity timescale.
- The compact full-profile argon trajectory uses 108 atoms and 551 sampled
  frames. Its trajectory RDF has a first peak near radius `1.095`, first peak
  value about `3.02`, and first-shell coordination number about `11.66` with
  four-block standard error about `0.030`.
- The compact trajectory now runs three seed-shifted replicas for an
  initialization-sensitivity check: coordination replica SE is about `0.028`,
  coordination ranges from about `11.60` to `11.70`, first-peak-radius replica
  standard deviation is about `0.017`, first-peak-value replica standard
  deviation is about `0.019`, mean RDF-bin replica standard deviation is about
  `0.011`, and max RDF-bin replica standard deviation is about `0.051`.
- The compact trajectory VACF has lag-1 autocorrelation about `0.800` and a
  first zero crossing at lag `4`; this supports only a wiring check for
  time-correlated velocity samples, not a transport claim.

Open items:

- The website prose should emphasize that RDF is a normalized estimator, not
  just a plotted histogram.
- The final article should connect coordination and time-correlation estimates
  to uncertainty and finite-size diagnostics from larger GPU kUPS trajectories.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-07/observable_diagnostics_snapshot.png`
- `snapshots/post-07/observable_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: panel labels and legends are readable, RDF peaks are
  visible, coordination error bars are present, and the VACF decay is clear.
- Figure correction: small-cell RDF bins beyond half the box length were masked
  and the figure was regenerated, so the plot does not present invalid radial
  shells as physical estimator support.
- Compact argon trajectory refresh: the fourth panel is visible in
  `snapshots/post-07/observable_diagnostics_full_snapshot.png`; `g(r)` and
  radius labels fit, the first peak and coordination cutoff marker are visible,
  and the `N = 108`, `coord = 11.66` annotation does not cover the peak.
- Compact replica refresh: the fourth panel now shows a seed-shifted replica
  RDF standard-deviation band and reports `rep SE = 0.028`. The band is visible
  without obscuring the first peak, the legend fits in the panel, and the
  annotation box remains away from the main RDF peak.
- The current figure includes a physical reduced-unit trajectory RDF, but it
  does not yet show larger GPU kUPS production observables, finite-size
  production comparisons, or transport-quality VACF uncertainty.

Open items:

- Add larger production-observable figures after GPU kUPS diagnostics are
  implemented.

## Notebook Review

- `notebooks/post-07-observables.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
  values, reports compact argon trajectory RDF/coordination/VACF summary
  values including block SE, replica SE, and max RDF replica standard
  deviation, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on RDF normalization,
  coordination integration, finite-size support, error bars, and time
  correlations rather than becoming the implementation source.

Open items:

- Add citations for RDF normalization, coordination integrals, finite-size
  effects, and time-correlation functions before final publication.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post07_observable_diagnostics.svg`.
- Expanded the hidden page from the short draft to about 3,528 words. The
  expanded prose explains observable definitions, RDF normalization,
  coordination integrals, VACF interpretation, uncertainty, finite-size
  support, common estimator mistakes, methods reporting, and the planned
  argon/kUPS trajectory extension.
- Refreshed the hidden page to describe the compact reduced-unit argon
  trajectory RDF panel and to keep larger GPU kUPS observables as the remaining
  production blocker.
- The expanded prose keeps the scope clear: the committed result is a
  controlled displaced-FCC observable-estimator diagnostic plus a compact
  reduced-unit trajectory observable check, not a final production GPU kUPS
  trajectory-observable study.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29361737064` succeeded for commit
  `2ae2434e4933fde7fe3f2241e18be00af913d159`.
- Snapshot workflow run `29361900585` captured the expanded hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`; both
  returned HTTP 200 with page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post07-expanded-snapshots/post-07-desktop.png` and
  `/tmp/kups-post07-expanded-snapshots/post-07-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, estimator tables, display equation,
  full-profile observable figure, reproduction code block, current-status
  section, references, and footer present. No blank page, missing figure,
  obvious clipping, or broken page chrome was found in the inspected snapshot.
- Mobile capture renders the same content through the mobile layout with title,
  navigation, author note, tables, equation, figure, code block,
  current-status section, and references present. The title wraps heavily but
  remains readable; tables and code block stay within the page.
- Website deploy run `29372999672` succeeded for compact argon trajectory
  refresh commit `184a54fd81c3b4a38fe659839ee9427666d46324`.
- Snapshot workflow run `29373158618` captured the refreshed hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-argon-trajectory-snapshots/`.
- Refreshed manifest reviewed:
  `/tmp/kups-post07-argon-trajectory-snapshots/manifest.json`.
- Refreshed manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`; both
  returned HTTP 200 with page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Refreshed rendered snapshots visually inspected:
  `/tmp/kups-post07-argon-trajectory-snapshots/post-07-desktop.png` and
  `/tmp/kups-post07-argon-trajectory-snapshots/post-07-mobile.png`.
- Refreshed desktop capture renders the compact trajectory table, updated
  source links, full article body, and four-panel observable diagnostic figure
  with the trajectory RDF panel visible. No blank page, missing figure, clipped
  table, or broken page chrome was found in the inspected snapshot.
- Refreshed mobile capture renders the updated article through the mobile
  layout with the compact trajectory table, four-panel figure, reproduction
  code block, current-status section, and references present. The embedded
  plot text is small, as expected for a full-width diagnostic on mobile, but
  the figure, caption, and surrounding prose remain coherent and unclipped.
- Website deploy run `29382464261` succeeded for compact replica observable
  refresh commit `1c9520bcbabef814ca91e2e58fbe8bb622ba6e53`.
- Snapshot workflow run `29382588504` captured the refreshed hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-replica-observable-snapshots/`.
- Replica-refresh manifest reviewed:
  `/tmp/kups-post07-replica-observable-snapshots/manifest.json`.
- Replica-refresh manifest coverage: desktop and mobile snapshots were captured
  for `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`;
  both returned HTTP 200 with page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Replica-refresh rendered snapshots visually inspected:
  `/tmp/kups-post07-replica-observable-snapshots/post-07-desktop.png` and
  `/tmp/kups-post07-replica-observable-snapshots/post-07-mobile.png`.
- Replica-refresh desktop capture renders the new trajectory-replica rows,
  updated uncertainty prose, revised figure/caption, reproduction block,
  current-status section, references, and footer. No missing figure, clipped
  table, overlap, or broken page chrome was found.
- Replica-refresh mobile capture renders the same new rows/prose/figure through
  the mobile layout. The article remains dense and the full diagnostic figure is
  small on mobile, but the new table and caption are contained and readable.
- Live checks confirmed the direct hidden URL contains the updated
  `coordination replica standard error` text, while `/` and `/blog/` do not
  expose `post-07-observables` or `kups-md-tutorials`.

## Update 2026-07-15: Compact Replica Observable Diagnostic

Commands run for this update:

- `uv run ruff check src/kups_md_tutorials/observables.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py src/kups_md_tutorials/free_energies.py tests/test_config.py`
- `uv run pytest tests/test_config.py tests/test_figures.py -q`
- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`

Code and reproducibility changes:

- Added `uncertainty_block_count` to the compact trajectory summary and wired it
  into the trajectory coordination block-SE estimator.
- Added three seed-shifted compact trajectory replicas and exported
  `argon_trajectory_rdf_replica_std` in
  `results/post-07/full/argon_trajectory_rdf_samples.csv`.
- Updated the Post 07 verifier to reject missing or zero-valued compact
  trajectory replica diagnostics.
- Preserved Post 08 compatibility by allowing the shared argon trajectory
  summarizer to operate on its lightweight container.

Full-profile compact trajectory metrics:

- `uncertainty_block_count = 4`
- `coordination_number = 11.655481602089955`
- `coordination_block_standard_error = 0.030055183447317606`
- `uncertainty_replica_count = 3`
- `coordination_replica_standard_error = 0.02829313477003499`
- `coordination_replica_min = 11.600600018185911`
- `coordination_replica_max = 11.698365216194265`
- `rdf_first_peak_radius_replica_std = 0.017320508075688787`
- `rdf_first_peak_value_replica_std = 0.018813132994856912`
- `mean_rdf_replica_std = 0.01050357350467306`
- `max_rdf_replica_std = 0.05092733709807738`

Review decisions:

- The compact replica observable diagnostic is accepted for the hidden draft
  state.
- It narrows the previous uncertainty gap for the compact trajectory panel, but
  it does not replace the larger GPU kUPS trajectory-observable diagnostic
  required before public finalization.
- Keep mobile title/table/figure density as a final typography-polish item.

Open items:

- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run the page snapshot workflow again after the final
  production-observable figures and citations are added.

## Update 2026-07-15: Compact VACF Replica Diagnostic

Commands run for this update:

- `uv run ruff check src/kups_md_tutorials/observables.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run python -m py_compile src/kups_md_tutorials/observables.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- First `uv run pytest tests/test_config.py tests/test_figures.py -q` failed
  because Post 08 still unpacked the shared Post 07 argon trajectory
  summarizer as a four-return-value helper.
- After updating the Post 08 caller, `uv run ruff check src/kups_md_tutorials/observables.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py src/kups_md_tutorials/free_energies.py tests/test_config.py` passed.
- After updating the Post 08 caller, `uv run pytest tests/test_config.py tests/test_figures.py -q` passed.
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `git diff --check`

Code and reproducibility changes:

- Added compact argon VACF replica statistics to
  `ArgonTrajectoryObservableSummary`.
- Added `vacf_replica_std` to
  `argon_trajectory_vacf_samples.csv`, preserving the existing `lag` and
  `normalized_vacf` columns.
- Updated the Post 07 verifier to reject missing or zero-valued compact
  trajectory VACF replica diagnostics.
- Preserved Post 08 compatibility by updating its shared argon trajectory
  summarizer call to ignore the new VACF-replica curve.
- Updated the Post 07 figure so the time-correlation panel overlays the
  controlled VACF, compact argon VACF, and the compact argon replica standard
  deviation band.
- Refreshed the hidden website draft to state the VACF replica uncertainty
  evidence and to keep production GPU observable diagnostics as the remaining
  final-release blocker.

Full-profile compact trajectory metrics:

- `vacf_normalized_integral = 0.018046003263717525`
- `vacf_integral_replica_standard_error = 0.01205097253796811`
- `vacf_integral_replica_min = -0.016547857491124418`
- `vacf_integral_replica_max = 0.020984735725791293`
- `mean_vacf_replica_std = 0.00501188264309433`
- `max_vacf_replica_std = 0.019083293100295495`
- `vacf_first_zero_lag = 4`
- `vacf_lag1_autocorrelation = 0.7997626737115738`

Figure feedback:

- Reviewed
  `snapshots/post-07/observable_diagnostics_full_snapshot.png`
  (`1728 x 1152`).
- Reviewed
  `snapshots/post-07/observable_diagnostics_snapshot.png`
  (`1728 x 1152`).
- Visual claim checked: the time-correlation panel should show that VACF is a
  lagged observable and that the compact trajectory tail has replica
  uncertainty rather than a precise transport interpretation.
- Full-profile snapshot: the new compact argon VACF line and pale replica
  standard-deviation band are visible, the controlled VACF remains legible, the
  legend fits in the panel, and the existing RDF/coordination panels are not
  clipped.
- Smoke-profile snapshot: the shorter compact trajectory has a wider VACF
  replica band, but the zero line, lag axis, legend, and RDF panel remain
  readable. No revision was needed after inspection.

Review decisions:

- The compact VACF replica diagnostic is accepted for the hidden draft state.
- The diagnostic strengthens the physical-observable wiring check, but it does
  not replace a larger GPU kUPS production trajectory with physical units,
  finite-size checks, tail treatment, and production uncertainty intervals.

Blocking items for the current hidden draft:

- None from this update.

Non-blocking items accepted until the final article pass:

- Mobile title/table/figure density remains a typography-polish item.

Final-release blockers:

- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Add final citations for RDF normalization, coordination integrals,
  finite-size effects, and time-correlation functions.
- Re-run rendered desktop/mobile snapshots after final production-observable
  figures, final citations, or any public-indexing change.
