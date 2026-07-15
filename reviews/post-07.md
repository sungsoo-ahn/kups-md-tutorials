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

Website page review:

- Website commit `604c4833b14622f14e55a3a19c43148affc18d56`
  deployed in GitHub Actions run `29388521392`.
- Snapshot workflow run `29388638389` captured the deployed VACF refresh.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-vacf-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-vacf-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`;
  both returned HTTP 200 with page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post07-vacf-snapshots/post-07-desktop.png` (`1440 x 12256`) and
  `/tmp/kups-post07-vacf-snapshots/post-07-mobile.png` (`541 x 18822`).
- Live cache-busted HTML check returned HTTP 200 and contained
  `VACF integral replica SE` and `replica band`.

Rendered page feedback:

- Desktop capture renders the hidden Post 07 draft end to end with sidebar
  TOC, hidden-draft note, source links, updated compact trajectory table,
  refreshed four-panel figure, revised caption, reproduction block, Practical
  Checklist, Current Status, references, and footer present.
- The refreshed figure is visible in the article body; the VACF panel is not
  clipped and the caption now matches the replica-band content.
- Mobile capture keeps the long title, hidden-draft note, tables, figure,
  caption, reproduction block, Current Status, references, and footer
  contained. Tables and the four-panel figure are dense at mobile width but
  not broken in the inspected snapshot.

Non-blocking items accepted until the final article pass:

- Mobile title/table/figure density remains a typography-polish item.

Final-release blockers:

- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run rendered desktop/mobile snapshots after final production-observable
  figures or any public-indexing change.

## Prose And Style Review

- The hidden website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, the author-note
  paragraph, compact reproduction commands, source links, and references.
- The prose is concept-led for MLIP-aware ML researchers: it treats RDFs,
  coordination integrals, VACFs, and uncertainty as estimators from finite
  trajectories rather than as notebook endpoints, while keeping the compact
  argon evidence separate from final GPU production claims.

## Open Items

Blocking items for the current hidden draft:

- None. The hidden draft states the CPU-fallback/non-production status and has
  rendered desktop/mobile snapshot evidence.

Non-blocking items accepted until the final article pass:

- Mobile table and figure density remain accepted for the hidden draft.
- The compact reduced-unit argon trajectory remains a teaching diagnostic
  rather than a final GPU kUPS production observable study.

Final-release blockers:

- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run rendered desktop/mobile snapshots after final production-observable
  figures or any public-indexing change.

## Update 2026-07-15: Observable Citation Completion

Scope:

- Resolved the Post 07 citation blocker for the hidden draft without changing
  simulations, configs, committed results, notebooks, figure sources, or figure
  snapshots.
- Website page updated:
  `../sungsoo-ahn.github.io/_pages/kups-md-post-07-observables.md`.
- Hidden page URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.

Citation review:

- Added inline citation anchors for RDF normalization, RDF finite-support
  masking, coordination integrals, time-correlation/VACF estimators,
  Green-Kubo tail interpretation, and finite-size transport effects.
- Added reverse backlinks in the `## References` section for Frenkel/Smit,
  Tuckerman, Allen/Tildesley, Hansen/McDonald, Green, Kubo,
  Alder/Wainwright, and Yeh/Hummer.
- The page's Current Status now lists final observable-estimator citations as
  implemented and no longer lists citation work as a missing piece.
- No figure snapshot was required for this citation-only prose pass because
  `figures/post-07/`, `snapshots/post-07/`, notebooks, configs, and results
  were unchanged. The existing reviewed figure snapshots remain
  `snapshots/post-07/observable_diagnostics_snapshot.png` and
  `snapshots/post-07/observable_diagnostics_full_snapshot.png`.

Source checks:

- Yeh/Hummer `System-size dependence of diffusion coefficients and viscosities
  from molecular dynamics simulations with periodic boundary conditions`:
  ACS/JPCB DOI `10.1021/jp0477147`.
- Alder/Wainwright `Decay of the velocity autocorrelation function`: APS/Phys.
  Rev. A DOI `10.1103/PhysRevA.1.18`.
- Kubo `Statistical-mechanical theory of irreversible processes. I`: JPSJ DOI
  `10.1143/JPSJ.12.570`.
- Green `Markoff random processes and the statistical mechanics of
  time-dependent phenomena. II`: JCP DOI `10.1063/1.1740082`.
- RDF normalization and coordination-integral context checked against
  Allen/Tildesley, Frenkel/Smit, Tuckerman, and Hansen/McDonald references.

Validation and page review:

- Website validation passed before deployment:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check`.
- Website commit reviewed and deployed: `da462ee`.
- Website deploy workflow run: `29406139927`, passed.
- Snapshot workflow run: `29406322485`, passed.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-citation-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-citation-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`,
  both with HTTP 200 and page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Full-page snapshots visually inspected:
  `/tmp/kups-post07-citation-snapshots/post-07-desktop.png`
  (`1440 x 13150`) and
  `/tmp/kups-post07-citation-snapshots/post-07-mobile.png`
  (`541 x 20364`).
- Focused crops visually inspected:
  `/tmp/kups-post07-citation-snapshots/desktop-top-citations.png`,
  `/tmp/kups-post07-citation-snapshots/desktop-mid-citations.png`,
  `/tmp/kups-post07-citation-snapshots/desktop-status-refs.png`,
  `/tmp/kups-post07-citation-snapshots/mobile-top-citations.png`,
  `/tmp/kups-post07-citation-snapshots/mobile-mid-citations.png`, and
  `/tmp/kups-post07-citation-snapshots/mobile-lower-status-refs-a.png`.
- Desktop feedback: the intro and estimator-definition citation cluster,
  RDF-normalization citations, finite-support/finite-size citations,
  coordination-integral citations, time-correlation citations, Current Status,
  and expanded References section all render inside the article column. The
  figure section and tables remain contained and unchanged.
- Mobile feedback: the long title, hidden-draft note, source links, citations,
  tables, equations, figure, Current Status, references, backlinks, and footer
  fit at `541 px` width. The article remains dense, but no citation overflow,
  table clipping, missing reference, or broken page chrome was found in the
  inspected crops.
- Live check with cache-buster `?v=da462ee` confirmed the deployed Post 07 page
  contains the new citation/status text and Hansen, Green, Kubo, Alder, and Yeh
  reference entries.
- Live homepage and `/blog/` checks found no `kups-md-tutorials` or
  `post-07-observables` links, so the page remains direct-link only.

Blocking items for the current hidden draft:

- None from this citation refresh.

Non-blocking items accepted until the final article pass:

- Mobile table and figure density remain accepted for the hidden draft.
- The compact reduced-unit argon trajectory remains a teaching diagnostic
  rather than a final GPU kUPS production observable study.

Final-release blockers after this refresh:

- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run rendered desktop/mobile snapshots after final production-observable
  figures or any public-indexing change.

## Update 2026-07-15: Runtime Provenance Gate

Scope:

- Added target-device, runtime-device, GPU-readiness, and blocking-reason
  provenance to the Post 07 compact argon trajectory observable diagnostic.
- Implementation commit reviewed:
  `c1e3058be3b2ce658de5cf995ad56f010cca31a3`.
- Website commit reviewed:
  `7dbb74d`.

Commands run:

- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/observables.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py`
- `uv run pytest tests/test_config.py::test_load_observable_spec tests/test_config.py::test_load_free_energy_spec -q`
- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in both repositories

Code and reproducibility review:

- `ArgonObservableTrajectorySpec` now has an explicit `target_device`. Post 07
  smoke records `cpu`, and Post 07 full records `cuda_or_cpu_fallback`.
- The shared config loader now reads `uncertainty_block_count`,
  `uncertainty_replica_count`, and `target_device` from `argon_trajectory`
  instead of relying on defaults for Post 07.
- `ArgonTrajectoryObservableSummary` now records `target_device`,
  `runtime_device`, `target_requests_gpu`, `production_gpu_ready`, and
  `gpu_blocking_reason`.
- Post 07 verification now requires runtime-device provenance and requires a
  blocking reason whenever a GPU-targeted compact argon trajectory diagnostic
  falls back from GPU execution.
- The full profile records `target_device = cuda_or_cpu_fallback`,
  `runtime_device = jax:cpu;devices:cpu`, `production_gpu_ready = false`, and
  the blocking reason `target device requests CUDA/GPU, but generated artifact
  runtime was jax:cpu;devices:cpu`.
- The notebook now prints target device, runtime device, production GPU
  readiness, and blocking reason next to the full-profile compact argon
  trajectory summary.
- Local execution again reported that an NVIDIA GPU may be present, but a
  CUDA-enabled `jaxlib` is not installed, so JAX/kUPS fell back to CPU.

Scientific review:

- The numerical observable metrics are unchanged by the provenance schema
  change. The full compact argon trajectory still reports 108 atoms, 551
  sampled frames, coordination `11.655481602089955`, coordination replica SE
  `0.02829313477003499`, VACF normalized integral `0.018046003263717525`, and
  VACF integral replica SE `0.01205097253796811`.
- The new fields prevent the compact reduced-unit observable diagnostic from
  being mistaken for a completed GPU kUPS production trajectory-observable
  study. The current artifact is a CPU-fallback reduced-unit diagnostic with
  explicit evidence for why the final GPU blocker remains.

Figure feedback:

- Full-profile figure snapshot inspected:
  `snapshots/post-07/observable_diagnostics_full_snapshot.png`
  (`1728 x 1152`).
- Smoke-profile figure snapshot inspected:
  `snapshots/post-07/observable_diagnostics_snapshot.png` (`1728 x 1152`).
- Intended visual claim: the fourth panel should show compact argon RDF,
  coordination-replica uncertainty, and the first-shell cutoff while making
  clear that the artifact is CPU fallback, not a completed GPU production
  observable run.
- Full-profile feedback: the trajectory RDF annotation now includes `runtime:
  CPU fallback`. It stays inside the white annotation box and does not cover
  the RDF curve, replica standard-deviation band, legend, or cutoff marker.
- Smoke-profile feedback: the runtime label is visible for the 32-atom compact
  smoke trajectory. The label remains contained and the RDF peak, cutoff line,
  and replica band remain readable.
- Revision decision: accepted for the hidden draft. No additional figure edit
  was needed after adding the runtime label and inspecting both snapshots.

Website page review:

- Hidden page URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- Website deploy run `29395058835` succeeded for commit `7dbb74d`.
- Snapshot workflow run `29395226951` captured the deployed runtime-provenance
  refresh.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post07-runtime-provenance-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-runtime-provenance-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`;
  both returned HTTP 200 with page title
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post07-runtime-provenance-snapshots/post-07-desktop.png`
  (`1440 x 12646`) and
  `/tmp/kups-post07-runtime-provenance-snapshots/post-07-mobile.png`
  (`541 x 19404`).
- Focused crops inspected:
  `desktop-runtime-table.png`, `desktop-figure.png`, `desktop-status.png`,
  `mobile-runtime-table.png`, `mobile-figure-2.png`, and
  `mobile-status.png`.
- Desktop feedback: the runtime limitation table is contained; the blocking
  reason wraps; the figure caption names the compact CPU-fallback argon
  trajectory panel; the runtime label is visible in the rendered figure; and
  Current Status lists the machine-readable provenance item.
- Mobile feedback: the runtime table wraps without horizontal clipping, the
  figure is dense but readable enough for the hidden draft, and Current Status
  remains contained with the larger GPU kUPS production observable diagnostic
  still in the missing list.
- Live hidden-page check with cache-buster `?v=7dbb74d` confirmed the deployed
  HTML contains `production GPU ready`, `runtime device`,
  `jax:cpu;devices:cpu`, `cuda_or_cpu_fallback`, `CPU-fallback`, and
  `machine-readable`.
- Public home and `/blog/` checks returned no `kups-md-tutorials` or
  `post-07-observables` hits, preserving the direct-link-only status.

Blocking items for the current hidden draft:

- None. The hidden draft states the CPU-fallback/non-production status and has
  rendered desktop/mobile snapshot evidence.

Non-blocking items accepted until the final article pass:

- Mobile table and figure density remain accepted for the hidden draft.
- The compact reduced-unit argon trajectory remains a teaching diagnostic
  rather than a final GPU kUPS production observable study.

Final-release blockers:

- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run rendered desktop/mobile snapshots after final production-observable
  figures or any public-indexing change.
