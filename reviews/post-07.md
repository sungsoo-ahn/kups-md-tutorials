# Post 07 Review Notes

## Scope

- Post: 07
- Profiles reviewed: smoke and full
- Current status: controlled argon-FCC observable-estimator workflow, committed
  smoke/full outputs, notebook, full-profile diagnostic figure, hidden website
  draft, and self-review artifact are in place; final prose and
  rendered page snapshots are still pending.

## Commands

- `uv run kups-tutorial run 07 --profile smoke`
- `uv run kups-tutorial verify 07 --profile smoke`
- `uv run kups-tutorial run 07 --profile full`
- `uv run kups-tutorial verify 07 --profile full`
- `uv run python scripts/generate_post07_figures.py`
- `uv run jupyter execute notebooks/post-07-observables.ipynb --inplace`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`

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

- Add rendered page snapshots after the hidden website draft deploys.
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

- Recheck mobile rendering after the hidden website draft exists.
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

- Add the full prose article in the website repository.
- Add citations for RDF normalization, coordination integrals, finite-size
  effects, and time-correlation functions when writing the full article.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post07_observable_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Capture and inspect deployed desktop and mobile snapshots for this hidden
  page.
- Expand the draft into the full 3,500-10,000-word article after rendered page
  snapshots and the argon/kUPS observable diagnostic are reviewed.
