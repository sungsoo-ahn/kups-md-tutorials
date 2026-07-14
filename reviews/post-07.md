# Post 07 Review Notes

## Scope

- Post: 07
- Profiles reviewed: smoke and full
- Current status: controlled argon-FCC observable-estimator workflow, committed
  smoke/full outputs, notebook, full-profile diagnostic figure, hidden website
  draft, rendered page snapshots, and self-review artifact are in place; the
  final argon/kUPS production trajectory observable diagnostic is still
  pending.

## Commands

- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29361737064` for website commit
  `2ae2434e4933fde7fe3f2241e18be00af913d159`
- GitHub Actions snapshot run `29361900585`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-07/`.
- Smoke and full outputs are committed under `results/post-07/`.
- The workflow uses deterministic periodic argon FCC cells with seeded thermal
  displacements, PBC minimum-image pair distances, RDF normalization,
  coordination integration, block standard errors, and a seeded velocity
  autocorrelation estimator.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 07.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating RDF, coordination, or VACF implementation details.

Open items:

- Replace or augment the displaced-FCC estimator with an actual argon/kUPS
  trajectory before treating this post as final.

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

Open items:

- The website prose should emphasize that RDF is a normalized estimator, not
  just a plotted histogram.
- The final article should connect coordination and time-correlation estimates
  to uncertainty and finite-size diagnostics from actual kUPS trajectories.

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
- The current figure is intentionally estimator-focused. A final post should
  add a production trajectory observable figure if dynamical or liquid-like
  argon claims are made.

Open items:

- Add a production-observable figure after argon/kUPS diagnostics are
  implemented.

## Notebook Review

- `notebooks/post-07-observables.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
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
- The expanded prose keeps the scope clear: the committed result is a
  controlled displaced-FCC observable-estimator diagnostic, not a final
  production argon/kUPS trajectory-observable study.
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

Open items:

- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Add argon/kUPS trajectory diagnostics for physical observables before
  treating this post as final.
- Re-run the page snapshot workflow after the final production-observable
  figure and citations are added.
