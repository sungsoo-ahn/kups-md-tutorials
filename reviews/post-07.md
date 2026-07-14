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
  block standard error about `0.035`.
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
  values, and regenerates the full-profile diagnostic figure from committed
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

Open items:

- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Add larger GPU kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run the page snapshot workflow again after the final
  production-observable figures and citations are added.
