# Post 08 Review Notes

## Scope

- Post: 08
- Profiles reviewed: smoke and full
- Current status: controlled one-dimensional free-energy workflow, committed
  smoke/full outputs, notebook, full-profile diagnostic figure, hidden website
  draft, rendered page snapshots, and self-review artifact are in place; the
  final argon/kUPS RDF-derived PMF diagnostic is still pending.

## Commands

- `uv run kups-tutorial run 08 --profile smoke`
- `uv run kups-tutorial verify 08 --profile smoke`
- `uv run kups-tutorial run 08 --profile full`
- `uv run kups-tutorial verify 08 --profile full`
- `uv run python scripts/generate_post08_figures.py`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-08-free-energies.ipynb --inplace`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29362569505` for website commit
  `80f1adec082720e3db395ff0c078c166fe3113f7`
- GitHub Actions snapshot run `29362752198`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-08/`.
- Smoke and full outputs are committed under `results/post-08/`.
- The workflow uses deterministic samples from a tabulated double-well
  equilibrium distribution, histogram PMF estimates, bootstrap barrier
  uncertainty, simple biased-sample reweighting, and an RDF-derived PMF.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 08.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating PMF, reweighting, bootstrap, or plotting implementation details.

Open items:

- Connect the PMF diagnostic to an actual argon/RDF-derived observable before
  treating this post as final.

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

Open items:

- The website prose should emphasize that a PMF is defined only after choosing
  a collective variable, normalization, binning/smoothing rule, and uncertainty
  estimate.
- The final article should connect `-kT log g(r)` to the RDF estimator from
  post 07 and explain where finite-size and low-count bins make PMFs fragile.

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

Open items:

- Add an RDF/PMF figure derived from the production observable workflow before
  treating this post as final.

## Notebook Review

- `notebooks/post-08-free-energies.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
  values, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on collective variables,
  histogram PMFs, binning bias, bootstrap uncertainty, reweighting, and
  RDF-derived PMFs rather than becoming the implementation source.

Open items:

- Add citations for PMFs, histogram estimators, reweighting, and RDF-derived
  potentials of mean force before final publication.

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
- The expanded prose keeps the scope clear: the committed result is a
  controlled one-dimensional PMF and synthetic RDF-derived PMF diagnostic, not
  a final production argon/kUPS free-energy calculation.
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

Open items:

- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Add the argon/kUPS RDF-derived PMF diagnostic linked back to post 07
  observables before treating this post as final.
- Re-run the page snapshot workflow after the final production RDF-derived PMF
  figure and citations are added.
