# Post 09 Review Notes

## Scope And Provenance

- Post: 09
- Profiles reviewed: smoke and full
- Current status: controlled free-energy estimator workflow, multi-state
  bridge diagnostic, compact smoke/full outputs, notebook, full-profile
  four-panel diagnostic figure, figure snapshots, refreshed hidden website
  draft, rendered page snapshots, and this self-review artifact are in place.
- Working-tree state: multi-state bridge diagnostic committed as
  `dabe886cc2021f96badc89c6d8d98605f4b0ac90`; hidden website refresh
  committed as `d0144d9f96023e9c5fa57a44dcd9d3a729f0603b`.
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
- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/estimators.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- GitHub Actions tutorial verify run `29375269908` for tutorial commit
  `dabe886cc2021f96badc89c6d8d98605f4b0ac90`
- GitHub Actions deploy run `29375280052` for website commit
  `d0144d9f96023e9c5fa57a44dcd9d3a729f0603b`
- GitHub Actions snapshot run `29375440197`
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
- The workflow now also records a multi-state bridge diagnostic under
  `multistate_protocols`, plus `multistate_curves.csv` and
  `multistate_windows.csv`. The diagnostic compares a connected dense bridge
  against an endpoint-only sparse bridge for a known Gaussian target with
  harmonic biased windows.
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
- The full-profile dense multi-state bridge uses 7 harmonic windows, minimum
  adjacent overlap about `0.184`, and no disconnected adjacent edges.
- The sparse bridge uses only endpoint windows, has minimum adjacent overlap
  `0.0`, and has one disconnected edge. Its support-aware PMF RMSE is higher
  than the dense bridge because unsupported bins are penalized as protocol
  failures rather than silently removed from the error calculation.
- The verification rule checks that overlap regimes are distinct, BAR remains
  close to the answer key, forward ESS collapses from good to poor overlap, and
  poor-overlap forward FEP is worse than good-overlap forward FEP.
- The verification rule also checks that the dense bridge has better adjacent
  overlap than the sparse bridge, that the dense bridge has no disconnected
  edges, that the sparse bridge exposes a broken overlap-network edge, and
  that the dense bridge has lower support-aware PMF RMSE.

Open items:

- The final article should explain that a small FEP error in one finite run
  does not prove reliability when ESS and overlap are poor.
- If a later public article adds a chemistry-specific WHAM/MBAR or alchemical
  production example, add that figure only with its own snapshot review.

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
- First multi-state bridge pass: the dense bridge line tracks the true PMF
  through the central high-probability region, while the sparse endpoint-only
  bridge has a visible missing middle. This supports the intended WHAM/MBAR
  lesson that a broken overlap network is a protocol failure.
- The snapshot review caught an earlier reconstruction bug: the PMF panel was
  flattened because the biased-window normalization constants were omitted.
  The reconstruction now applies the analytic harmonic-window bridge constant,
  and support-aware RMSE penalizes unsupported bins.
- The final full-profile snapshot has readable labels, ticks, legends, and the
  dense/sparse bridge annotation. The dense curve has edge-tail noise near the
  low-support ends, which is accepted for the hidden draft because it visibly
  illustrates tail sensitivity and does not obscure the central bridge claim.

Open items:

- Repeat figure snapshot review if a later public article adds a
  chemistry-specific production WHAM/MBAR or alchemical figure.

## Notebook Review

- `notebooks/post-09-estimators.ipynb` loads smoke and full configurations,
  prints committed full-summary diagnostics including the dense/sparse
  multi-state bridge metrics, and regenerates the full-profile estimator
  figure from committed result files.
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
- Refreshed hidden page and exported assets deployed in website commit
  `d0144d9f96023e9c5fa57a44dcd9d3a729f0603b`; deploy run
  `29375280052` succeeded.
- Tutorial commit `dabe886cc2021f96badc89c6d8d98605f4b0ac90` passed verify
  run `29375269908`.
- Snapshot workflow run `29375440197` captured the refreshed hidden post 09
  page after deployment.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post09-bridge-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-bridge-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`; both
  returned HTTP 200 with page title
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post09-bridge-snapshots/post-09-desktop.png` and
  `/tmp/kups-post09-bridge-snapshots/post-09-mobile.png`.

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
- Refreshed desktop capture renders the new four-panel diagnostic figure, the
  updated WHAM/MBAR bridge prose, current-status section, references, and
  footer. No blank page, missing figure, obvious clipping, or broken page
  chrome was found.
- Refreshed mobile capture keeps the four-panel figure inside the article
  column. Long title and tables remain tight but contained, and the bridge
  panel remains legible enough for the hidden draft state.
- Index-refresh desktop capture from `2026-07-15` renders the current deployed
  hidden draft end to end after the blog-style hidden index and later post
  updates. The sidebar table of contents, author note, executable-artifact
  links, estimator tables, four-panel diagnostic figure, reproduction block,
  current-status section, references, and footer are present. No blank page,
  missing figure, clipped table, or broken page chrome was found.
- Index-refresh mobile capture keeps the title, author note, estimator tables,
  four-panel figure, reproduction block, current-status section, references,
  and footer inside the page column. Tables remain dense at mobile width, but
  text does not overlap and the figure remains legible enough for the hidden
  draft.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Repeat rendered snapshots if a later public article adds a
  chemistry-specific estimator figure or if the page is made public.

Index-refresh snapshot evidence:

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29379023705`.
- Website commit reviewed:
  `a755ec8f3a2f2d3cf48081e9bd48f4b9c178c588`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post09-index-refresh-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-index-refresh-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`; both
  returned HTTP 200 with page title
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post09-index-refresh-snapshots/post-09-desktop.png` and
  `/tmp/kups-post09-index-refresh-snapshots/post-09-mobile.png`.

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
- If the page is made public or a later chemistry-specific estimator figure is
  added, rerun desktop/mobile snapshots and update this review before final
  indexing.

Final-release blockers:

- None.

## Update 2026-07-15: Provenance Restamp And Page Snapshot Refresh

- Tutorial restamp commit reviewed:
  `1022fbe4c9f5bd4bfdf615b5b657e21f22d1239e`.
- Website commits reviewed:
  `e22f2924b97f996f43f70b235b471dd050b5df67`,
  `d7fff97a9770bdb822bcd88a15d61cce68b0da32`, and
  `dee7bead9504f33250259ec3cc47cb502d76ad64`.
- Website deployment runs:
  `29400709025`, `29401143938`, and final deploy `29401528292`.
- Snapshot workflow runs:
  first pass `29400881017`, second pass `29401323263`, and final pass
  `29401699781`.
- Final snapshot artifact: `kups-md-page-snapshots`.
- Downloaded final review copy:
  `/tmp/kups-post09-provenance-final-snapshots/`.

Scope:

- No estimator algorithm or numerical-summary logic changed in this pass.
- Smoke and full Post 09 manifests were restamped under the current repository
  state, and the notebook was re-executed.
- The hidden website page `last_updated` was moved to `2026-07-15`.
- The Reproduction section now exposes the full-profile configuration hash,
  source revision, runtime device, and precision policy in a provenance table.
- The Current Status section now lists rendered desktop/mobile snapshots as
  implemented instead of missing.

Validation:

- `uv run kups-tutorial run 09 --profile smoke` and
  `uv run kups-tutorial verify 09 --profile smoke` passed.
- `uv run kups-tutorial run 09 --profile full` and
  `uv run kups-tutorial verify 09 --profile full` passed.
- `uv run python scripts/generate_post09_figures.py` passed; figure files were
  unchanged.
- `uv run jupyter execute notebooks/post-09-estimators.ipynb --inplace` passed.
- `uv run pytest tests/test_config.py::test_load_estimator_spec
  tests/test_cli.py::test_cli_run_and_verify_post09_smoke
  tests/test_figures.py::test_post09_figure_generation
  tests/test_notebooks.py::test_post09_notebook_executes -q` passed.
- `uv run kups-tutorial verify-artifacts` passed.
- `python3 scripts/validate_kups_pages.py` passed in
  `../sungsoo-ahn.github.io`.
- `python3 scripts/validate_blog.py` passed in `../sungsoo-ahn.github.io` with
  pre-existing unused-image warnings.
- `git diff --check` passed in both repositories.

Code and reproducibility review:

- Full manifest now records source revision
  `98dc7cb2b3a6828141117f80de81bb9a242e57aa`, configuration hash
  `54f9c7456965f1eb75ff0f47960d59c3eccd1c5dfa192c5298919e3fc04ed125`,
  runtime device `jax:cpu;devices:cpu`, and precision policy
  `jax_enable_x64=false;env_JAX_ENABLE_X64=unset`.
- Numerical estimator summaries are unchanged relative to the prior reviewed
  hidden draft. The provenance restamp is accepted because it brings the page
  metadata in line with the current executable repository state.

Figure feedback:

- Figure asset inspected:
  `figures/post-09/estimator_diagnostics_full.svg`.
- Snapshot inspected:
  `snapshots/post-09/estimator_diagnostics_full_snapshot.png`.
- Intended visual claim: estimator reliability is controlled by overlap and
  effective sample size, and a multi-state bridge needs connected adjacent
  overlap.
- Feedback: the existing four-panel snapshot remains readable. The estimator
  bars keep the true \(\Delta F\) line visible, the overlap/ESS panel shows
  ESS collapse before raw samples disappear, the work histogram still exposes
  rare-tail dependence, and the bridge panel shows the sparse protocol's
  missing middle without label clipping. No figure edit was needed.
- Revision decision: accepted unchanged; no revised figure snapshot was needed
  because the figure assets did not change.

Website and rendered-page review:

- Final snapshot manifest reviewed:
  `/tmp/kups-post09-provenance-final-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`; both
  returned HTTP 200 and title
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.
- Desktop snapshot inspected:
  `/tmp/kups-post09-provenance-final-snapshots/post-09-desktop.png` at
  `1440 x 11282`.
- Mobile snapshot inspected:
  `/tmp/kups-post09-provenance-final-snapshots/post-09-mobile.png` at
  `573 x 16950`.
- Focused crops inspected:
  `/tmp/kups-post09-provenance-final-snapshots/desktop-provenance-status.png`
  and
  `/tmp/kups-post09-provenance-final-snapshots/mobile-provenance-status.png`.
- First mobile snapshot pass found that the provenance table values clipped
  horizontally because markdown code spans did not wrap inside the value cell.
- First fix using `overflow-wrap: anywhere` around markdown code was
  insufficient; the second fix used explicit HTML `code` elements with
  `white-space: normal`, `overflow-wrap: anywhere`, and `word-break: break-all`.
- Final desktop feedback: the provenance table, Current Status section,
  References, and footer are present and contained. Long hashes wrap in the
  table without disturbing the article column.
- Final mobile feedback: the provenance values now wrap inside the table; the
  Current Status section no longer lists snapshots as missing; references and
  footer remain contained. The reproduction code block remains horizontally
  dense but is unchanged from prior hidden-draft behavior.
- Live check with cache buster `?v=dee7bea` confirmed the deployed page
  contains the current configuration hash, source revision, runtime device, and
  `Provenance field` table.
- Live homepage and `/blog/` checks with cache buster `?v=dee7bea` confirmed
  `post-09-estimators` and `kups-md-tutorials` are not exposed.

Open items:

- Blocking items for the current hidden draft: none.
- Non-blocking items accepted until the final article pass: the page remains
  explicitly non-final and direct-link only.
- Final-release blockers: none specific to this controlled estimator post,
  unless a later public article adds a chemistry-specific production WHAM/MBAR
  or alchemical example; if so, add that figure and rerun snapshot review.
