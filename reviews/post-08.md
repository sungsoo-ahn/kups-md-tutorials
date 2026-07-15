# Post 08 Review Notes

## Scope

- Post: 08
- Profiles reviewed: smoke and full
- Current status: controlled one-dimensional free-energy workflow, compact
  reduced-unit argon trajectory RDF-derived PMF workflow with block/replica
  uncertainty, committed smoke/full outputs, notebook, full-profile diagnostic
  figure, hidden website draft, rendered page snapshots, and self-review
  artifact are in place; larger GPU kUPS RDF-derived PMF diagnostics and final
  citations remain pending.

## Commands

- `uv run kups-tutorial run 08 --profile smoke`
- `uv run kups-tutorial verify 08 --profile smoke`
- `uv run kups-tutorial run 08 --profile full`
- `uv run kups-tutorial verify 08 --profile full`
- `uv run python scripts/generate_post08_figures.py`
- `uv run ruff check .`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace`
- `uv run kups-tutorial verify-artifacts`
- `git diff --check`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29362569505` for website commit
  `80f1adec082720e3db395ff0c078c166fe3113f7`
- GitHub Actions snapshot run `29362752198`
- GitHub Actions tutorial verify run `29374144064` for tutorial commit
  `535c48586c6fe30ad14887b2343887d74ae53be8`
- GitHub Actions deploy run `29374143464` for website commit
  `c049640dc27e3ce763b6b744358fe34dde491cf1`
- GitHub Actions snapshot run `29374285478`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-08/`.
- Smoke and full outputs are committed under `results/post-08/`.
- The workflow uses deterministic samples from a tabulated double-well
  equilibrium distribution, histogram PMF estimates, bootstrap barrier
  uncertainty, simple biased-sample reweighting, and an RDF-derived PMF.
- The workflow now also writes compact argon trajectory RDF and RDF-PMF curves
  into `free_energy_curves.csv`, generated from actual sampled reduced-unit
  positions rather than a synthetic RDF profile.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 08.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating PMF, reweighting, bootstrap, or plotting implementation details.

Open items:

- Add larger GPU kUPS RDF-derived PMF diagnostics before treating this post as
  final.

## Scientific Review

- The full profile samples `80000` points from a known double-well potential
  with true barrier height `1.0` in `kT = 1` units.
- Histogram bin widths `0.06`, `0.18`, and `0.35` estimate barriers `0.985`,
  `0.976`, and `0.915`, showing that coarse binning can bias the barrier
  downward even when the data are equilibrium samples.
- Bootstrap standard errors are positive for each bin width and are recorded in
  the summary rather than inferred from visual smoothness.
- Simple reweighting from a biased sample gives barrier height `1.123`, close
  enough for a basic diagnostic but visibly not identical to the direct
  histogram PMF.
- The RDF-derived PMF has a minimum at radius `1.20`, matching the configured
  synthetic RDF first-neighbor peak.
- The compact full-profile argon trajectory uses 108 atoms and 551 sampled
  frames at number density `0.85` and temperature `0.70`.
- Its trajectory RDF has a first peak near radius `1.125`, peak value about
  `3.01`, and the shifted `-kT log g(r)` PMF minimum at the same radius.
- The argon RDF-PMF transform masks 32 finite low-RDF bins and retains 52
  finite PMF bins; the retained shifted PMF range is about `1.64` in reduced
  energy units. This is a support-aware PMF transform diagnostic, not a
  production free-energy barrier.
- The refreshed argon RDF-PMF uncertainty diagnostic uses 4 contiguous blocks
  and 3 independent seed-shifted compact replicas.
- The full profile reports mean block PMF SEM `0.0084`, maximum block PMF SEM
  `0.0290`, mean local replica PMF standard deviation `0.0109`, and maximum
  local replica PMF standard deviation `0.0616`.

Open items:

- The website prose should emphasize that a PMF is defined only after choosing
  a collective variable, normalization, binning/smoothing rule, and uncertainty
  estimate.
- The final article should keep connecting `-kT log g(r)` to the RDF estimator
  from post 07 and explain where finite-size and low-count bins make PMFs
  fragile.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-08/free_energy_diagnostics_snapshot.png`
- `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: PMF, binning, and RDF-derived PMF panels are
  readable; bin labels fit; uncertainty bars are visible; and the figure
  supports the claim that PMFs are estimators, not direct trajectory output.
- The true double-well curve has high walls near the domain edge, which is
  acceptable because the histogram PMF only has support where samples exist.
  The final article should explain missing/empty bins explicitly.
- Compact argon RDF-PMF refresh: the fourth panel is visible in
  `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`; axis labels,
  legend, PMF minimum marker, and `N = 108`, `frames = 551`,
  `rmin = 1.125` annotation fit without covering the first minimum.
- The trajectory PMF line is intentionally discontinuous where low RDF bins are
  masked before the logarithm; this makes unsupported pair-distance regions
  visible rather than presenting a falsely smooth PMF.

Open items:

- Add larger production RDF-PMF figures after GPU kUPS diagnostics are
  implemented.

## Notebook Review

- `notebooks/post-08-free-energies.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
  values, reports the compact argon RDF-PMF minimum/range/finite-bin count, and
  regenerates the full-profile diagnostic figure from committed result files.
- The notebook keeps the explanation focused on collective variables,
  histogram PMFs, binning bias, bootstrap uncertainty, reweighting, and
  RDF-derived PMFs rather than becoming the implementation source.

Open items:

- Citation coverage for PMFs, histogram estimators, reweighting, and
  RDF-derived potentials of mean force is now implemented in the hidden
  website page. Keep the citations synchronized with any final production
  RDF-PMF rewrite.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post08_free_energy_diagnostics.svg`.
- Expanded the hidden page from the short draft to about 3,501 words. The
  expanded prose explains collective-variable choice, histogram PMFs, binning
  bias, empty and low-count bins, reweighting, RDF-derived PMFs, uncertainty,
  common PMF mistakes, methods reporting, and the planned argon/kUPS extension.
- Refreshed the hidden page to describe the compact reduced-unit argon
  trajectory RDF-PMF panel and to keep larger GPU kUPS PMF diagnostics as the
  remaining production blocker.
- The expanded prose keeps the scope clear: the committed result is a
  controlled one-dimensional PMF, synthetic RDF-derived PMF, and compact
  reduced-unit argon trajectory RDF-PMF diagnostic, not a final production
  GPU kUPS free-energy calculation.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29362569505` succeeded for commit
  `80f1adec082720e3db395ff0c078c166fe3113f7`.
- Snapshot workflow run `29362752198` captured the expanded hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post08-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`;
  both returned HTTP 200 with page title
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post08-expanded-snapshots/post-08-desktop.png` and
  `/tmp/kups-post08-expanded-snapshots/post-08-mobile.png`.
- Refreshed hidden page and hidden index deployed in website commit
  `c049640dc27e3ce763b6b744358fe34dde491cf1`; deploy run
  `29374143464` succeeded.
- Tutorial commit `535c48586c6fe30ad14887b2343887d74ae53be8` passed verify
  run `29374144064`.
- Snapshot workflow run `29374285478` captured the hidden index and refreshed
  post 08 page after deployment.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post08-index-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-index-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/` and
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`;
  all four requests returned HTTP 200.
- Rendered snapshots visually inspected:
  `/tmp/kups-post08-index-snapshots/post-index-desktop.png`,
  `/tmp/kups-post08-index-snapshots/post-index-mobile.png`,
  `/tmp/kups-post08-index-snapshots/post-08-desktop.png`, and
  `/tmp/kups-post08-index-snapshots/post-08-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, PMF diagnostic tables, display
  equations, full-profile free-energy figure, reproduction code block,
  current-status section, references, and footer present. No blank page,
  missing figure, obvious clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the same content through the mobile layout with title,
  navigation, author note, tables, display equations, figure, code block,
  current-status section, and references present. The title wraps but remains
  readable; tables are tight but contained.
- Refreshed desktop post 08 capture renders the updated four-panel diagnostic
  figure and article flow without missing assets, blank regions, or broken
  page chrome.
- Refreshed mobile post 08 capture scales the diagnostic figure into the column
  without overlapping neighboring text.
- Hidden index desktop capture matches the existing blog-list style and keeps
  kUPS content out of public navigation; only the existing public blog and
  publications links appear in the header.
- Hidden index mobile capture is readable and direct-link reachable. The
  repository command block wraps tightly around the clone URL, but it remains
  contained and acceptable for the hidden draft state.

Open items:

- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Add larger GPU kUPS RDF-derived PMF diagnostics before treating this post as
  final.
- Re-run the page snapshot workflow again after the final production
  RDF-derived PMF figure is added.

## Update 2026-07-15: RDF-PMF Block And Replica Uncertainty

- Tutorial working-tree state reviewed before commit: Post 08 schema,
  workflow, figure, configs, committed smoke/full outputs, notebook, snapshots,
  and website export assets changed together.
- Website commit reviewed:
  `8bff587c0ff672594e6a462b40d6722f60b2b5ef`.
- Website deployment run:
  `29381569320`.
- Snapshot workflow run:
  `29381687757`.
- Snapshot artifact: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/`.

Commands added in this pass:

- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/free_energies.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py`
- `uv run pytest tests/test_config.py tests/test_figures.py -q`
- `uv run kups-tutorial run 08 --profile smoke`
- `uv run kups-tutorial verify 08 --profile smoke`
- `uv run kups-tutorial run 08 --profile full`
- `uv run kups-tutorial verify 08 --profile full`
- `uv run python scripts/generate_post08_figures.py`
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full`
- `python3 scripts/validate_kups_pages.py` in
  `../sungsoo-ahn.github.io`

## Update 2026-07-15: Runtime Provenance Gate

### Scope and provenance

- Post: 08
- Profiles reviewed: smoke and full
- Implementation commit: `82fe878dbecd0a51ca7c2f84b2e0e128b8f8dbd2`
- Restamp/review commit in progress after this note; pushed tutorial state
  before this note: `46683e910458f874f6930dbc32fb76611afce717`
- Website commit reviewed:
  `8e103a968f313b9562d79071614df23376001f80`
- Website deploy run: `29396296025`
- Website snapshot workflow: `Capture kUPS snapshots`, run `29396474029`,
  artifact `kups-md-page-snapshots`
- Downloaded snapshot review copy:
  `/tmp/kups-post08-runtime-provenance-snapshots/`
- Hidden draft URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`

Generated files inspected:

- `results/post-08/smoke/free_energy_summary.json`
- `results/post-08/full/free_energy_summary.json`
- `results/post-08/smoke/manifest.json`
- `results/post-08/full/manifest.json`
- `figures/post-08/free_energy_diagnostics.png`
- `figures/post-08/free_energy_diagnostics_full.png`
- `snapshots/post-08/free_energy_diagnostics_snapshot.png`
- `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`
- `notebooks/post-08-free-energies.ipynb`
- `../sungsoo-ahn.github.io/_pages/kups-md-post-08-free-energies.md`
- `../sungsoo-ahn.github.io/assets/img/blog/kups_md_post08_free_energy_diagnostics.svg`

Commands run:

- `uv run ruff check src/kups_md_tutorials/free_energies.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py` passed.
- `uv run pytest tests/test_config.py::test_load_free_energy_spec tests/test_figures.py::test_post08_figure_generation -q` passed.
- `uv run kups-tutorial run 08 --profile smoke` passed.
- `uv run kups-tutorial verify 08 --profile smoke` passed.
- `uv run kups-tutorial run 08 --profile full` passed with expected CPU
  fallback warning.
- `uv run kups-tutorial verify 08 --profile full` passed.
- `uv run python scripts/generate_post08_figures.py` passed.
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace` passed.
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q` passed with `49 passed, 62 warnings`.
- `uv run kups-tutorial verify-artifacts` passed.
- `git diff --check` passed.
- `python3 scripts/validate_kups_pages.py` passed in
  `../sungsoo-ahn.github.io`.
- `python3 scripts/validate_blog.py` passed in `../sungsoo-ahn.github.io`
  with pre-existing unused-image warnings.
- `gh run watch 29396287224 --repo sungsoo-ahn/kups-md-tutorials --exit-status` passed.
- `gh run watch 29396296025 --repo sungsoo-ahn/sungsoo-ahn.github.io --exit-status` passed.
- `gh run watch 29396474029 --repo sungsoo-ahn/sungsoo-ahn.github.io --exit-status` passed.

### Code and reproducibility review

- `configs/post-08/smoke.json` now declares `argon_rdf_pmf.target_device:
  "cpu"`; `configs/post-08/full.json` declares
  `argon_rdf_pmf.target_device: "cuda_or_cpu_fallback"`.
- `ArgonRdfPmfSummary` now records target device, runtime device,
  target-GPU request status, production GPU readiness, and a GPU blocking
  reason.
- `_verify_post08` now fails if runtime-device provenance is missing, and it
  requires a blocking reason when a GPU-targeted run falls back to CPU.
- The full-profile compact argon RDF-PMF summary records target
  `cuda_or_cpu_fallback`, runtime `jax:cpu;devices:cpu`, production GPU ready
  `false`, and blocking reason `target device requests CUDA/GPU, but generated
  artifact runtime was jax:cpu;devices:cpu`.
- The full manifest records config hash
  `7d98bc849d66ecd7769dca29ede00e593774fd47e4b1c2854ef4e7b428ed6703` and
  source revision `82fe878dbecd0a51ca7c2f84b2e0e128b8f8dbd2`.
- The notebook prints the same target/runtime/GPU-readiness fields beside the
  RDF-PMF uncertainty and support-threshold diagnostics.

### Scientific review

- The provenance change does not alter the PMF estimator or numerical PMF
  values; it changes the interpretation of the compact trajectory diagnostic.
- Full-profile numerical values remain the compact reduced-unit argon
  diagnostic: 108 atoms, 551 frames, RDF first peak at radius `1.125`, finite
  PMF range about `1.6429`, max block PMF SEM about `0.0290`, and max local
  replica PMF standard deviation about `0.0616`.
- The new machine-readable fields make the limitation explicit: the diagnostic
  requests CUDA/GPU for a production-ready target, but the committed artifact
  was generated on CPU because this environment has CPU-only JAX.
- Revision decision: accept the CPU-fallback artifact for the hidden draft
  because the page labels it as non-final and records the blocking reason.
  Final publication still requires a larger GPU kUPS RDF-derived PMF run.

### Figure feedback review

- Source data inspected:
  `results/post-08/full/free_energy_summary.json` and
  `results/post-08/full/free_energy_curves.csv`.
- Figure assets inspected:
  `figures/post-08/free_energy_diagnostics_full.png` and
  `figures/post-08/free_energy_diagnostics.png`.
- Snapshot inspected:
  `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`, raster
  `1728 x 1152`.
- Snapshot inspected:
  `snapshots/post-08/free_energy_diagnostics_snapshot.png`, raster
  `1728 x 1152`.
- Intended visual claim: the fourth panel should show that compact trajectory
  RDF-derived PMFs depend on support thresholds and uncertainty estimates, and
  should now also disclose whether the trajectory artifact came from a
  production GPU run or CPU fallback.
- Full-profile feedback: the new `runtime: CPU fallback` label fits inside the
  existing annotation box. It does not cover the PMF minimum marker, support
  threshold curves, scaled RDF curve, legend, or replica-standard-deviation
  axis. Axis labels and the right-hand replica-std axis remain readable.
- Smoke-profile feedback: the annotation is taller but still fits in the
  upper-left panel region. It does not obscure the first PMF basin or the
  visible support-threshold curves.
- Revision decision: no figure revision needed after the runtime label pass;
  accept for hidden draft. Re-run figure snapshots after any production GPU
  PMF diagnostic is added.

### Website page review

- Deployed URL inspected:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`
- Snapshot manifest:
  `/tmp/kups-post08-runtime-provenance-snapshots/manifest.json`
- Manifest coverage: desktop and mobile captures for post 08, both HTTP 200,
  title `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.
- Full-page snapshots inspected:
  `/tmp/kups-post08-runtime-provenance-snapshots/post-08-desktop.png`
  (`1440 x 12349`) and
  `/tmp/kups-post08-runtime-provenance-snapshots/post-08-mobile.png`
  (`550 x 18769`).
- Focused crops inspected:
  `/tmp/kups-post08-runtime-provenance-snapshots/desktop-figure.png`,
  `/tmp/kups-post08-runtime-provenance-snapshots/desktop-runtime-table.png`,
  `/tmp/kups-post08-runtime-provenance-snapshots/mobile-figure-corrected.png`,
  `/tmp/kups-post08-runtime-provenance-snapshots/mobile-runtime-table-3.png`,
  and `/tmp/kups-post08-runtime-provenance-snapshots/mobile-status-2.png`.
- Desktop feedback: the runtime table renders below reproduction provenance;
  `cuda_or_cpu_fallback`, `jax:cpu;devices:cpu`, `false`, and the blocking
  reason all remain inside the table. The Current Status item for
  machine-readable provenance wraps without overflow.
- Desktop figure feedback: the updated figure caption is present, the
  CPU-fallback label is visible in the fourth panel, and the page text around
  the figure has no obvious overlap or missing asset.
- Mobile figure feedback: the four-panel figure is dense but not clipped; the
  CPU-fallback line is still visible in the fourth panel, and the caption wraps
  cleanly below the image.
- Mobile runtime-table feedback: the long config hash wraps in the prose, and
  the runtime table keeps all rows contained; the blocking reason wraps inside
  the value column without horizontal clipping.
- Live HTML checks with cache-busting query `?v=8e103a9` confirmed the page
  contains `cuda_or_cpu_fallback`, `jax:cpu;devices:cpu`, production GPU
  readiness `false`, CPU-fallback runtime provenance, and source revision
  `82fe878dbecd0a51ca7c2f84b2e0e128b8f8dbd2`.
- Public navigation check: live `/blog/` and `/` still contain no
  `kups-md-tutorials` or `post-08-free-energies` links. The draft remains
  direct-link only.
- Revision decision: accept the rendered page for hidden draft. Re-run
  deployed snapshots after final production RDF-PMF figures or any
  public-indexing change.

### Prose and style review

- The page remains an al-folio `post` layout hidden from navigation with the
  shared `kups-md-tutorials` series metadata.
- The added prose is limited to provenance: a compact target/runtime row in
  the diagnostic table, a runtime limitation table in reproduction, an updated
  figure caption, and a Current Status bullet.
- The page still states that the current result is a compact CPU-fallback
  diagnostic, not a production GPU kUPS free-energy result.

### Open items

Blocking for final publication:

- Add larger GPU kUPS RDF-derived PMF diagnostics before public indexing.
- Re-run figure and rendered desktop/mobile snapshots after final production
  RDF-PMF figures or any public-indexing change.

Accepted hidden-draft limitations:

- The current full-profile compact argon RDF-derived PMF artifact was
  generated on CPU fallback while targeting `cuda_or_cpu_fallback`.
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=8`
- `gh run download 29381687757 --name kups-md-page-snapshots --dir /tmp/kups-post08-rdf-pmf-uncertainty-snapshots`

Code and reproducibility review:

- `ArgonObservableTrajectorySpec` now records explicit
  `uncertainty_block_count` and `uncertainty_replica_count` values, both
  committed in the smoke and full Post 08 configs.
- `ArgonRdfPmfSummary` now records block and replica PMF uncertainty metrics:
  block count, replica count, mean and maximum block PMF SEM, and mean and
  maximum local replica PMF standard deviation.
- `free_energy_curves.csv` now exports `argon_rdf_pmf_block_sem` and
  `argon_rdf_pmf_replica_std` columns aligned to the trajectory RDF-PMF
  radius grid.
- Post 08 verification now requires positive block and replica PMF uncertainty
  when the argon RDF-PMF diagnostic is configured.
- The implementation remains deterministic: uncertainty replicas are
  seed-shifted compact trajectories, and block uncertainty is computed from
  contiguous blocks of the committed compact trajectory protocol.

Scientific review:

- Full-profile compact argon RDF-PMF still uses 108 atoms and 551 sampled
  frames at number density `0.85` and temperature `0.70`.
- RDF first peak remains near radius `1.125` with `g(r)` about `3.01`.
- Shifted PMF minimum remains radius `1.125`; finite-bin PMF range remains
  about `1.6429` reduced energy units.
- The refreshed uncertainty diagnostic uses 4 trajectory blocks and 3 compact
  seed-shifted replicas.
- Mean block PMF SEM is `0.0084`; maximum block PMF SEM is `0.0290`.
- Mean local replica PMF standard deviation is `0.0109`; maximum local
  replica PMF standard deviation is `0.0616`.
- Interpretation: the hidden draft now has a concrete block/replica
  uncertainty diagnostic for the compact RDF-PMF transform. This remains a
  compact reduced-unit teaching diagnostic, not a larger GPU kUPS production
  free-energy calculation.

Figure feedback:

- Source data inspected:
  `results/post-08/full/free_energy_summary.json` and
  `results/post-08/full/free_energy_curves.csv`.
- Figure asset inspected:
  `figures/post-08/free_energy_diagnostics_full.svg`.
- Snapshot inspected:
  `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`.
- Intended visual claim: PMFs are estimator products; RDF-derived PMFs require
  finite support; and compact trajectory RDF-PMF uncertainty should be visible
  through block and replica diagnostics rather than hidden in prose.
- Feedback: the fourth panel now shows the trajectory RDF-PMF, scaled RDF,
  PMF minimum marker, block SEM band, and dashed replica-standard-deviation
  curve. Axis labels and legends fit. The block SEM band is subtle because the
  maximum SEM is only `0.0290`, so the annotation and notebook printout carry
  the quantitative value. The dashed replica curve is legible on the secondary
  axis and does not obscure the PMF line.
- Revision decision: no additional figure edit was needed after inspecting the
  refreshed full-profile snapshot.

Notebook review:

- The notebook now prints compact argon RDF-PMF block count, replica count,
  maximum block SEM, and maximum replica standard deviation.
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace`
  completed successfully after the notebook source was updated.

Website and rendered-page review:

- The hidden page now describes the block/replica RDF-PMF uncertainty
  diagnostic and keeps the larger GPU kUPS RDF-PMF diagnostic as the remaining
  production blocker.
- Website validators passed; `validate_blog.py` still reports only
  pre-existing unused-image warnings.
- Live hidden-route check with `?v=8bff587` confirmed the Post 08 page
  contains `block SEM` and `replica disagreement`.
- Live homepage and blog listing checks with `?v=8bff587` confirmed
  `post-08-free-energies` and `kups-md-tutorials` are not exposed.
- Snapshot manifest reviewed:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`;
  both returned HTTP 200 and title
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.
- Desktop snapshot inspected:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/post-08-desktop.png` at
  `1440 x 11537`.
- Mobile snapshot inspected:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/post-08-mobile.png` at
  `550 x 17669`.
- Desktop feedback: the refreshed hidden article renders end to end with
  source links, PMF tables, equations, updated four-panel figure, reproduction
  block, Current Status section, references, and footer present. The updated
  fourth figure panel is visible and contained; no missing asset, blank page,
  clipped text, or broken page chrome was found.
- Mobile feedback: the title, tables, equations, updated figure, caption,
  code block, Current Status section, references, and footer remain contained.
  Tables are dense but readable; the four-panel figure scales into the column
  without overlapping neighboring text.

Revision decisions:

- No blocking layout issue was found for the Post 08 refreshed hidden draft.
- The compact block/replica RDF-PMF uncertainty diagnostic is accepted for the
  hidden draft state.
- Keep mobile title/table density as a final typography-polish item.
- Add larger GPU kUPS RDF-derived PMF diagnostics before public indexing.
- Re-run rendered snapshots after final production RDF-PMF figures or any
  public-indexing change.

## Update 2026-07-15: RDF-PMF Support-Threshold Sensitivity

Commands added in this pass:

- `uv run ruff check src/kups_md_tutorials/free_energies.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run python -m py_compile src/kups_md_tutorials/free_energies.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run kups-tutorial run 08 --profile smoke`
- `uv run kups-tutorial verify 08 --profile smoke`
- `uv run kups-tutorial run 08 --profile full`
- `uv run kups-tutorial verify 08 --profile full`
- `uv run python scripts/generate_post08_figures.py`
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace`

Code and reproducibility review:

- `ArgonRdfPmfSummary` now records RDF support-threshold sensitivity fields:
  thresholds, finite PMF-bin counts, PMF ranges, minimum radii, and the span of
  PMF ranges across thresholds.
- The RDF-PMF workflow exports support-threshold PMF curves for thresholds
  `0.02`, `0.05`, and `0.10` in `free_energy_curves.csv`.
- Post 08 verification now requires multiple support thresholds, matching
  threshold/range lengths, and a positive support-threshold range span.
- The figure generator overlays dotted support-threshold PMF curves in the
  trajectory RDF-PMF panel and annotates the support sensitivity span.
- The notebook now prints support thresholds, finite-bin counts, PMF ranges,
  and range span from the committed full-profile summary.

Scientific review:

- Smoke-profile compact argon RDF-PMF support thresholds `0.02`, `0.05`, and
  `0.10` retain `19`, `18`, and `18` finite PMF bins, respectively.
- Smoke-profile PMF ranges across those thresholds are `3.1088`, `1.4170`,
  and `1.4170`, giving a support-threshold range span of `1.6918` reduced
  energy units.
- Full-profile compact argon RDF-PMF support thresholds `0.02`, `0.05`, and
  `0.10` retain `53`, `52`, and `52` finite PMF bins, respectively.
- Full-profile PMF ranges across those thresholds are `2.9979`, `1.6429`,
  and `1.6429`, giving a support-threshold range span of `1.3550` reduced
  energy units.
- Interpretation: the first RDF-PMF minimum is stable at radius `1.125` across
  thresholds in the full profile, but the reported shifted PMF range is
  sensitive to whether very low RDF-support bins are admitted. The figure and
  page should therefore frame this as a support-sensitive transform, not a
  production barrier estimate.

Figure feedback:

- Full-profile figure snapshot inspected:
  `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`
  (`1728 x 1152`).
- Smoke-profile figure snapshot inspected:
  `snapshots/post-08/free_energy_diagnostics_snapshot.png`
  (`1728 x 1152`).
- Full-profile feedback: the fourth panel shows the main support `0.05` PMF,
  dotted support `0.02` and `0.10` curves, scaled RDF, PMF-minimum marker,
  block SEM band, replica-standard-deviation axis, and annotation with
  `support span = 1.35`. The dense legend is contained and does not block the
  first-minimum interpretation.
- Smoke-profile feedback: the same visual elements are present, with a larger
  support span of `1.69` and visibly stronger low-support sensitivity. The
  panel remains readable and no blocking clipping or overlap was found.
- Revision decision: no additional local figure edit was needed after
  inspecting the support-threshold snapshots.

Website review status:

- Website commit reviewed:
  `6c08328`.
- Website deploy run:
  `29390018103`.
- Snapshot workflow run:
  `29390138917`.
- Snapshot artifact: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`;
  both returned HTTP 200 with page title
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.
- Desktop snapshot inspected:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-desktop.png`
  (`1440 x 11817`).
- Mobile snapshot inspected:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-mobile.png`
  (`550 x 18162`).
- Desktop figure crop inspected:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-figure-wide.png`.
- Mobile figure crop inspected:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-mobile-figure-wide.png`.
- Desktop feedback: the hidden page renders end to end with sidebar TOC,
  updated support-threshold prose, refreshed four-panel figure, caption,
  reproduction block, Current Status section, references, and footer. The
  fourth panel shows the support-threshold curves and `support span = 1.35`
  annotation without clipping.
- Mobile feedback: the support-threshold prose, figure, and caption remain
  contained in the mobile column. The figure is dense but readable; no text or
  image overlap was found in the inspected crop.
- Live hidden-route check with `?v=6c08328` confirmed the deployed HTML
  contains `support-threshold sensitivity`, `2.998`, `1.355`, and the updated
  figure caption.
- Live homepage and public blog checks confirmed `kups-md-tutorials` and
  `post-08-free-energies` are not exposed in public navigation or the public
  blog listing.

Final-release blockers:

- Add larger GPU kUPS RDF-derived PMF diagnostics before public indexing.
- Re-run rendered snapshots after final production RDF-PMF figures or any
  public-indexing change.

## Update 2026-07-15: Free-Energy Citation Completion

Scope:

- Resolved the Post 08 citation blocker for the hidden draft without changing
  simulations, configs, committed results, notebooks, figure sources, or figure
  snapshots.
- Website page updated:
  `../sungsoo-ahn.github.io/_pages/kups-md-post-08-free-energies.md`.
- Hidden page URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.

Citation review:

- Added inline citation anchors for the PMF probability relation, potential of
  mean force interpretation, histogram estimators, bin-width sensitivity,
  reweighting/WHAM-style weighting, MBAR overlap assumptions, RDF-derived PMFs,
  and bootstrap/histogram uncertainty context.
- Added reverse backlinks in the `## References` section for Frenkel/Smit,
  Tuckerman, Chandler, Kirkwood, Ferrenberg/Swendsen, Kumar/Rosenberg/Bouzida/
  Swendsen/Kollman, Souaille/Roux, and Shirts/Chodera.
- The page's Current Status now lists final free-energy citations as
  implemented and no longer lists citation work as a missing piece.
- No figure snapshot was required for this citation-only prose pass because
  `figures/post-08/`, `snapshots/post-08/`, notebooks, configs, and results
  were unchanged. The existing reviewed figure snapshots remain
  `snapshots/post-08/free_energy_diagnostics_snapshot.png` and
  `snapshots/post-08/free_energy_diagnostics_full_snapshot.png`.

Source checks:

- Kirkwood `Statistical mechanics of fluid mixtures`: AIP/JCP DOI
  `10.1063/1.1749657`.
- Ferrenberg/Swendsen `Optimized Monte Carlo data analysis`: APS/PRL DOI
  `10.1103/PhysRevLett.63.1195`.
- Kumar/Rosenberg/Bouzida/Swendsen/Kollman `The weighted histogram analysis
  method for free-energy calculations on biomolecules`: Wiley/JCC DOI
  `10.1002/jcc.540130812`.
- Souaille/Roux `Extension to the weighted histogram analysis method`:
  Computer Physics Communications DOI `10.1016/S0010-4655(00)00215-0`.
- Shirts/Chodera `Statistically optimal analysis of samples from multiple
  equilibrium states`: JCP DOI `10.1063/1.2978177`.
- PMF/statistical-mechanics context checked against Frenkel/Smit, Tuckerman,
  and Chandler references.

Validation and page review:

- Website validation passed before deployment:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check`.
- Website commit reviewed and deployed: `f88202f`.
- Website deploy workflow run: `29407274298`, passed.
- Snapshot workflow run: `29407440841`, passed.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post08-citation-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-citation-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`,
  both with HTTP 200 and page title
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.
- Full-page snapshots visually inspected:
  `/tmp/kups-post08-citation-snapshots/post-08-desktop.png`
  (`1440 x 12805`) and
  `/tmp/kups-post08-citation-snapshots/post-08-mobile.png`
  (`550 x 19585`).
- Focused crops visually inspected:
  `/tmp/kups-post08-citation-snapshots/desktop-top-citations.png`,
  `/tmp/kups-post08-citation-snapshots/desktop-mid-citations.png`,
  `/tmp/kups-post08-citation-snapshots/desktop-status-refs.png`,
  `/tmp/kups-post08-citation-snapshots/mobile-top-citations.png`,
  `/tmp/kups-post08-citation-snapshots/mobile-mid-citations.png`, and
  `/tmp/kups-post08-citation-snapshots/mobile-lower-status-refs.png`.
- Desktop feedback: the PMF-definition citations, Kirkwood/Chandler mean-force
  citations, histogram/reweighting/MBAR citations, RDF-derived PMF citations,
  Current Status, and expanded References section render inside the article
  column. The figure section, runtime table, and practical checklist remain
  contained and unchanged.
- Mobile feedback: the long title, hidden-draft note, source links, equations,
  citation clusters, dense tables, figure, Current Status, references,
  backlinks, and footer fit at `550 px` width. No citation overflow, table
  clipping, missing reference, or broken page chrome was found in the inspected
  crops.
- Live check with cache-buster `?v=f88202f` confirmed the deployed Post 08 page
  contains the new citation/status text and Kirkwood, Ferrenberg, Kumar,
  Souaille, and Shirts reference entries.
- Live homepage and `/blog/` checks found no `kups-md-tutorials` or
  `post-08-free-energies` links, so the page remains direct-link only.

Blocking items for the current hidden draft:

- None from this citation refresh.

Non-blocking items accepted until the final article pass:

- Mobile title, table, and figure density remain accepted for the hidden draft.
- The compact reduced-unit argon RDF-PMF remains a teaching diagnostic rather
  than a final GPU kUPS production free-energy study.

Final-release blockers after this refresh:

- Add larger GPU kUPS RDF-derived PMF diagnostics before public indexing.
- Re-run rendered snapshots after final production RDF-PMF figures or any
  public-indexing change.
