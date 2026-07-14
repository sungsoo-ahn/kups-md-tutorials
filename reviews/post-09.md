# Post 09 Review Notes

## Scope And Provenance

- Post: 09
- Profiles reviewed: smoke and full
- Current status: controlled free-energy estimator workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, expanded
  hidden website draft, rendered page snapshots, and this self-review artifact
  are in place.
- Working-tree state: website expansion committed as
  `4c32e635190a3aa15f270c6c04cfb3c8dc06bdb0`; review update committed after
  this pass.
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
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `uv run pytest -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify --profile smoke`
- `uv run kups-tutorial verify 09 --profile full`
- `git diff --check` in this repository and `../sungsoo-ahn.github.io`
- `gh run watch 29348734443 --exit-status` in `../sungsoo-ahn.github.io`
- `gh run watch 29348976216 --exit-status` in `../sungsoo-ahn.github.io`
- `curl -I -L 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/?v=449ed1b'`
- `curl -L --silent 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/?v=449ed1b' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/?v=449ed1b' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/blog/?v=449ed1b' | rg ...`
- GitHub Actions deploy run `29363423337` for website commit
  `4c32e635190a3aa15f270c6c04cfb3c8dc06bdb0`
- GitHub Actions snapshot run `29363609573`
- `uv run kups-tutorial verify-reviews`

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

- The final article should explain that a small FEP error in one finite run
  does not prove reliability when ESS and overlap are poor.
- Any final WHAM/MBAR production figure should be added only with its own
  snapshot review.

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
- Expanded the hidden page from the short draft to about 3,503 words. The
  expanded prose explains FEP assumptions, reverse FEP, BAR, ESS, WHAM/MBAR
  overlap networks, estimator failure symptoms, intermediate-state design,
  MLIP-specific risks, reporting mistakes, methods reporting, and practical
  estimator diagnostics.
- The expanded prose keeps the scope clear: the committed result is an exactly
  solvable Gaussian estimator diagnostic, not a production alchemical workflow.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- GitHub Pages deployments `29348734443` and correction run `29348976216`
  completed successfully. The live hidden URL returns HTTP 200 and contains the
  expected title, estimator notebook link, full summary link, current-status
  section, and `kups_md_post09_estimator_diagnostics.svg` figure.
- The public homepage and blog index did not contain `post-09-estimators` or
  `kups-md-tutorials` in the deployed HTML checked with cache-buster
  `?v=449ed1b`.
- Website deploy run `29363423337` succeeded for the expanded page commit
  `4c32e635190a3aa15f270c6c04cfb3c8dc06bdb0`.
- Snapshot workflow run `29363609573` captured the expanded hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post09-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`; both
  returned HTTP 200 with page title
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post09-expanded-snapshots/post-09-desktop.png` and
  `/tmp/kups-post09-expanded-snapshots/post-09-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, estimator/ESS tables, full-profile
  estimator figure, reproduction code block, current-status section,
  references, and footer present. No blank page, missing figure, obvious
  clipping, or broken page chrome was found in the inspected snapshot.
- Mobile capture renders the same content through the mobile layout with title,
  navigation, author note, tables, figure, code block, current-status section,
  and references present. Tables are tight but contained, and the figure remains
  readable.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Add any final MBAR/WHAM production figures and snapshot-review them before
  treating this post as final.

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

- None.

Non-blocking items accepted until the final article pass:

- The page remains hidden and explicitly non-final.

Final-release blockers:

- Add any final MBAR/WHAM production figures and snapshot-review them.
- Re-run rendered desktop/mobile snapshots after any final estimator figures,
  citation changes, or publication indexing changes.
