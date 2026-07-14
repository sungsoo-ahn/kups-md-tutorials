# Post 10 Review Notes

## Scope And Provenance

- Post: 10
- Profiles reviewed: smoke and full
- Current status: controlled umbrella-sampling workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, and this
  self-review artifact are in place; the hidden website draft is in place.
- Working-tree state: post 10 implementation is uncommitted during this review
  pass.
- Hidden draft URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`

## Commands

- `uv run kups-tutorial run 10 --profile smoke`
- `uv run kups-tutorial verify 10 --profile smoke`
- `uv run kups-tutorial run 10 --profile full`
- `uv run kups-tutorial verify 10 --profile full`
- `uv run python scripts/generate_post10_figures.py`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-10-umbrella-sampling.ipynb --inplace`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `uv run pytest -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify --profile smoke`
- `uv run kups-tutorial verify 10 --profile full`
- `git diff --check` in this repository and `../sungsoo-ahn.github.io`
- `gh run watch 29349892098 --exit-status` in `../sungsoo-ahn.github.io`
- `curl -I -L 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/?v=7c1d612'`
- `curl -L --silent 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/?v=7c1d612' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/?v=7c1d612' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/blog/?v=7c1d612' | rg ...`

## Code And Reproducibility Review

- Configs are committed-intended under `configs/post-10/`.
- Smoke and full outputs are committed-intended under `results/post-10/`.
- The workflow uses deterministic samples from biased double-well
  distributions with fixed seeds, known unbiased PMF, and two predefined
  umbrella protocols: dense connected windows and sparse windows that leave a
  bridge gap.
- The summary records reconstructed barrier height, barrier error, PMF RMSE
  versus the known answer, minimum and mean adjacent overlap, forward/reverse
  replica PMF consistency, replica mean spread, and per-window support.
- The manifest records the loaded config, compact output filenames, config
  hash, Git revision, Python/platform metadata, and kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 10.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather
  than reimplementing biased sampling, WHAM reconstruction, or plotting.

Open items:

- Capture rendered desktop and mobile page snapshots after the hidden draft
  deploys.

## Scientific Review

- The full profile samples `20000` points per window from a dimensionless
  double-well potential with true barrier height `1.0`.
- `dense_windows` uses nine windows from `-1.6` to `1.6`. Its minimum adjacent
  overlap is `0.3552`, reconstructed barrier error is `0.0106`, PMF RMSE is
  `0.1730`, and forward/reverse replica PMF RMSE is `0.1148`.
- `sparse_windows` skips the barrier bridge with four windows at `-1.6`,
  `-0.8`, `0.8`, and `1.6`. Its minimum adjacent overlap is `0.0003`,
  reconstructed barrier error is `-0.2554`, PMF RMSE is `0.2229`, and
  forward/reverse replica PMF RMSE is `0.2352`.
- The verification rule checks that dense windows improve minimum adjacent
  overlap, improve PMF RMSE versus the sparse protocol, recover the barrier
  within `0.20`, and have acceptable replica consistency.

Open items:

- The final article should emphasize that umbrella sampling samples biased
  ensembles, not the unbiased PMF directly.
- The final article should state that a window can have many samples while
  still failing the global reconstruction if adjacent windows do not overlap.
- The final article should connect this controlled WHAM-style diagnostic to
  practical window placement, hysteresis checks, and replica agreement in MD.

## Figure Feedback Review

Snapshots reviewed:

- `snapshots/post-10/umbrella_diagnostics_snapshot.png`
- `snapshots/post-10/umbrella_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: the PMF panel is readable and shows dense/sparse
  reconstructions against the known PMF without hiding the high-energy walls.
- The overlap panel makes the key failure mode visible: dense adjacent overlap
  stays around `0.36` or higher, while the sparse bridge overlap is nearly
  zero.
- The window sampling panel shows that an umbrella center is not a sampled
  point. Each window has a mean and width, and the biased distribution shifts
  away from the nominal center where the double-well force competes with the
  bias.
- No label clipping, legend overlap, unreadable ticks, or misleading scale was
  found in the inspected full-profile snapshot.

Open items:

- Recheck figure readability inside the rendered hidden webpage at desktop and
  mobile widths.
- If the final article adds a rendered WHAM iteration or hysteresis figure,
  repeat the same snapshot review for those publication assets.

## Notebook Review

- `notebooks/post-10-umbrella-sampling.ipynb` loads smoke and full
  configurations, prints committed full-summary diagnostics, and regenerates
  the full-profile umbrella figure from committed result files.
- `uv run jupyter execute notebooks/post-10-umbrella-sampling.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post10_umbrella_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- GitHub Pages deployment `29349892098` completed successfully. The live
  hidden URL returns HTTP 200 and contains the expected title, umbrella
  notebook link, full summary link, current-status section, minimum-overlap
  table, and `kups_md_post10_umbrella_diagnostics.svg` figure.
- The public homepage and blog index did not contain
  `post-10-umbrella-sampling` or `kups-md-tutorials` in the deployed HTML
  checked with cache-buster `?v=7c1d612`.

Open items:

- Capture and inspect rendered desktop and mobile snapshots for this hidden
  page.

## Prose And Style Review

- The planned website draft should follow the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose should be concept-led for MLIP-aware ML researchers: start from
  biased ensembles and overlap, then explain reconstruction and window
  diagnostics rather than treating WHAM as a black-box postprocessor.

## Open Items

Blocking items for the current hidden draft:

- None.

Non-blocking items accepted until the final article pass:

- Rendered page snapshots are still pending.
- The draft will remain short and explicitly non-final.

Final-release blockers:

- Expand the prose to a full article with citations for umbrella sampling,
  WHAM/MBAR, hysteresis diagnostics, and finite-window uncertainty.
- Add production MD context and any final diagnostics needed for the public
  article.
- Resolve rendered desktop/mobile page snapshot feedback.
