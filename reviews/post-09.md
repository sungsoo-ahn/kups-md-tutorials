# Post 09 Review Notes

## Scope And Provenance

- Post: 09
- Profiles reviewed: smoke and full
- Current status: controlled free-energy estimator workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, and this
  self-review artifact are in place; the hidden website draft is in place.
- Working-tree state: post 09 implementation is uncommitted during this review
  pass.
- Hidden draft URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`

## Commands

- `uv run kups-tutorial run 09 --profile smoke`
- `uv run kups-tutorial verify 09 --profile smoke`
- `uv run kups-tutorial run 09 --profile full`
- `uv run kups-tutorial verify 09 --profile full`
- `uv run python scripts/generate_post09_figures.py`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-09-estimators.ipynb --inplace`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `uv run pytest -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify --profile smoke`
- `uv run kups-tutorial verify 09 --profile full`
- `git diff --check` in this repository and `../sungsoo-ahn.github.io`

## Code And Reproducibility Review

- Configs are committed-intended under `configs/post-09/`.
- Smoke and full outputs are committed-intended under `results/post-09/`.
- The workflow uses deterministic Gaussian state pairs with fixed seeds,
  known true free-energy offsets, and increasing state displacement to isolate
  estimator behavior from unknown physics.
- The summary records forward FEP, reverse FEP, BAR, estimator errors, overlap
  coefficient, forward/reverse effective-sample-size fractions, and work
  distribution moments for each overlap regime.
- The manifest records the loaded config, compact output filenames, config
  hash, Git revision, Python/platform metadata, and kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 09.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather
  than reimplementing the estimator or plotting code.

Open items:

- Capture rendered desktop and mobile page snapshots after the hidden draft
  deploys.

## Scientific Review

- The full profile samples `50000` points from each of two unit-variance
  Gaussian states for every case. The true dimensionless free-energy
  difference is `0.8`.
- `good_overlap` has overlap coefficient `0.803`, forward ESS fraction
  `0.779`, and BAR error `0.00036`. Forward and reverse FEP errors are both
  below `0.003`, so the direct exponential averages are well behaved.
- `marginal_overlap` has overlap coefficient `0.453`, forward ESS fraction
  `0.0966`, and BAR error `0.0081`. FEP remains close in this seeded run, but
  the ESS diagnostic already warns that only a small weighted subset controls
  the estimate.
- `poor_overlap` has overlap coefficient `0.134`, forward ESS fraction
  `0.00274`, reverse ESS fraction `0.00182`, and BAR error `0.0326`. Forward
  FEP error rises to `0.0472`, showing the expected overlap failure before BAR
  becomes catastrophically wrong.
- The verification rule checks that overlap regimes are distinct, BAR remains
  close to the answer key, forward ESS collapses from good to poor overlap, and
  poor-overlap forward FEP is worse than good-overlap forward FEP.

Open items:

- The final article should state that this is an exactly solvable estimator
  diagnostic, not a production alchemical workflow.
- The final article should explain that a small FEP error in one finite run
  does not prove reliability when ESS and overlap are poor.
- WHAM/MBAR should be introduced conceptually in prose after the two-state
  BAR/FEP diagnostic, with references and a clear statement of what additional
  overlap structure they assume.

## Figure Feedback Review

Snapshots reviewed:

- `snapshots/post-09/estimator_diagnostics_snapshot.png`
- `snapshots/post-09/estimator_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: the estimator comparison panel keeps the true
  \(\Delta F\) line visible, all three estimator labels are readable, and the
  poor-overlap forward FEP bias is visible without exaggerating the y-axis.
- The overlap/ESS panel clearly shows overlap decreasing from about `0.80` to
  `0.45` to `0.13`, while forward ESS collapses from about `0.78` to `0.10` to
  near zero. This supports the intended mechanism better than estimator error
  alone.
- The work-distribution panel shows why the exponential average becomes fragile:
  good-overlap work values sit near the free-energy line, while poor-overlap
  work values rely on rare low-work tail samples.
- No label clipping, legend overlap, unreadable ticks, or misleading scale was
  found in the inspected full-profile snapshot.

Open items:

- Recheck figure readability inside the rendered hidden webpage at desktop and
  mobile widths.
- If the final article adds MBAR/WHAM figures, repeat the same snapshot review
  for those publication assets.

## Notebook Review

- `notebooks/post-09-estimators.ipynb` loads smoke and full configurations,
  prints committed full-summary diagnostics, and regenerates the full-profile
  estimator figure from committed result files.
- `uv run jupyter execute notebooks/post-09-estimators.ipynb --inplace` passes
  and saves executed outputs. Jupyter emitted a non-blocking
  `MissingIDFieldWarning` while normalizing cell IDs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post09_estimator_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Verify the deployed hidden page after the website commit is pushed.
- Confirm that the page is directly reachable but not linked from public
  navigation.
- Capture and inspect rendered desktop and mobile snapshots for this hidden
  page.

## Prose And Style Review

- The planned website draft should follow the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose should be concept-led for MLIP-aware ML researchers: start from
  exponential averages and overlap, then explain BAR and the bridge to
  WHAM/MBAR rather than presenting estimator formulas as isolated recipes.

## Open Items

Blocking items for the current hidden draft:

- Verify the deployed hidden URL after the website commit is pushed.
- Confirm that public navigation does not link to the hidden page.

Non-blocking items accepted until the final article pass:

- Rendered page snapshots are still pending.
- The draft will remain short and explicitly non-final.

Final-release blockers:

- Expand the prose to a full article with citations for FEP, BAR, WHAM, MBAR,
  overlap, and effective sample size.
- Add any final MBAR/WHAM production figures and snapshot-review them.
- Resolve rendered desktop/mobile page snapshot feedback.
