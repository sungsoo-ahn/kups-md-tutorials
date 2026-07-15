# Post 10 Review Notes

## Scope And Provenance

- Post: 10
- Profiles reviewed: smoke and full
- Current status: controlled umbrella-sampling workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, expanded
  hidden website draft, rendered page snapshots, and this self-review artifact
  are in place. The page remains hidden from public navigation.
- Working-tree state: website expansion committed as
  `82e9508717fe8a8e826eaae040949e3fa8b18fe7`; this repository has review
  updates and the `/goal` plan clarification staged for the current pass.
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
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_kups_pages.py`
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_blog.py`
- expanded post whitespace check in `../sungsoo-ahn.github.io`:
  `git diff --check`
- inline math delimiter check in `../sungsoo-ahn.github.io`:
  `rg -n '\\\\(|\\\\)' _pages/kups-md-post-10-umbrella-sampling.md || true`
- word-count check for the expanded page: `3602` words
- `gh run watch 29364446798 --exit-status` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=10` in
  `../sungsoo-ahn.github.io`
- `gh run watch 29364628807 --exit-status` in `../sungsoo-ahn.github.io`
- `gh run download 29364628807 --name kups-md-page-snapshots --dir /tmp/kups-post10-expanded-snapshots`
- live hidden-route check with cache buster `?v=82e9508`
- live homepage/blog listing checks with cache buster `?v=82e9508`

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

- None for the controlled code/reproducibility slice in the current hidden
  draft.

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

- The expanded hidden page now emphasizes that umbrella sampling samples biased
  ensembles, not the unbiased PMF directly.
- The expanded hidden page now states that a window can have many samples while
  still failing the global reconstruction if adjacent windows do not overlap.
- Final-release work should still connect the controlled WHAM-style diagnostic
  to a production MD umbrella example with uncertainty intervals and model
  checks.

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

Rendered page figure check:

- The figure was inspected inside the rendered desktop snapshot
  `/tmp/kups-post10-expanded-snapshots/post-10-desktop.png` and mobile
  snapshot `/tmp/kups-post10-expanded-snapshots/post-10-mobile.png`.
- Desktop: the PMF, overlap, and window-sampling panels render below the
  diagnostic section, with axes, legend, and caption readable in the article
  column. No clipping or broken asset was visible.
- Mobile: the figure remains legible at 452 px capture width. The panel labels
  are small but readable enough for the hidden draft, and the caption wraps
  without overlapping neighboring text.

Open items:

- If the final article adds a rendered WHAM iteration, uncertainty, or
  hysteresis figure, repeat the same snapshot review for those publication
  assets.

## Notebook Review

- `notebooks/post-10-umbrella-sampling.ipynb` loads smoke and full
  configurations, prints committed full-summary diagnostics, and regenerates
  the full-profile umbrella figure from committed result files.
- `uv run jupyter execute notebooks/post-10-umbrella-sampling.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`.
- Expanded the hidden page to `3602` words with additional sections on overlap,
  window placement, WHAM-style reconstruction, replicas, initialization,
  hysteresis, uncertainty, overlap failure, methods reporting, and production
  MD extension.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post10_umbrella_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `python3 scripts/validate_kups_pages.py` passes.
- GitHub Pages deployment `29349892098` completed successfully. The live
  hidden URL returns HTTP 200 and contains the expected title, umbrella
  notebook link, full summary link, current-status section, minimum-overlap
  table, and `kups_md_post10_umbrella_diagnostics.svg` figure.
- The public homepage and blog index did not contain
  `post-10-umbrella-sampling` or `kups-md-tutorials` in the deployed HTML
  checked with cache-buster `?v=7c1d612`.
- Expanded-page GitHub Pages deployment `29364446798` completed successfully
  for website commit `82e9508717fe8a8e826eaae040949e3fa8b18fe7`.
- Snapshot workflow `Capture kUPS snapshots` run `29364628807` completed
  successfully for post 10. Artifact `kups-md-page-snapshots` was downloaded
  to `/tmp/kups-post10-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post10-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`;
  both returned HTTP 200 and title
  `What Does Umbrella Sampling Actually Sample? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post10-expanded-snapshots/post-10-desktop.png` at
  `1440 x 10869` and `/tmp/kups-post10-expanded-snapshots/post-10-mobile.png`
  at `452 x 16674`.
- Desktop feedback: the expanded article renders end to end with sidebar table
  of contents, hidden-draft note, source links, dense/sparse diagnostic table,
  figure, methods/protocol sections, practical checklist, reproduction block,
  current-status section, references, and footer present. No blank page,
  missing figure, clipped text, or broken page chrome was found in the
  inspected snapshot.
- Mobile feedback: the title wraps across multiple lines but remains contained.
  The diagnostic tables are tight but readable, the figure and caption are
  contained, the reproduction code block stays inside the page, and the footer
  renders normally.
- Live hidden-route check with `?v=82e9508` confirmed the expanded section
  `How Should Windows Be Initialized?`, the figure asset, the non-final note,
  and the rendered snapshot status phrase.
- Live homepage and blog listing checks with `?v=82e9508` confirmed
  `post-10-umbrella-sampling` and `kups-md-tutorials` are not exposed.

Open items:

- No blocking layout issue was found for the expanded post 10 hidden draft.
- Keep mobile title/table wrapping as a final typography-polish item after the
  rest of the articles are expanded.
- Re-run rendered desktop/mobile snapshots after adding any final production MD
  or uncertainty figures.

## Prose And Style Review

- The expanded website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose is concept-led for MLIP-aware ML researchers: it starts from biased
  ensembles and overlap, then explains reconstruction, window diagnostics,
  initialization, uncertainty, and methods reporting rather than treating WHAM
  as a black-box postprocessor.
- `PLAN.md` was clarified in this pass so future `/goal` continuations must
  name self-review and figure feedback as standalone checklist items and must
  run a snapshot-backed feedback loop when figures or rendered pages change.

## Open Items

Blocking items for the current hidden draft:

- None.

Non-blocking items accepted until the final article pass:

- The expanded draft remains explicitly non-final.
- Mobile title and table wrapping can be polished later if desired, but the
  captured hidden draft is readable and contained.

Final-release blockers:

- Add production MD context with real atomistic umbrella windows, model checks,
  and any production-level uncertainty intervals needed for public claims.
- Re-run rendered desktop/mobile snapshots after any final production MD or
  figure additions.

## Update 2026-07-14: Replica-Disagreement Figure And Blog-Style Index

- Tutorial commit reviewed:
  `f56985cb9915ad0a6f001ed1d56364d915ae8c92`.
- Tutorial verification run:
  `29376292286`.
- Website commit reviewed:
  `41f0674ecf059ba84c58d9e8f71657b67d203c88`.
- Website deployment run:
  `29376297732`.
- Snapshot workflow run:
  `29376446171`.
- Snapshot artifact: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-index-post10-snapshots/`.

Commands added in this pass:

- `uv run kups-tutorial run 10 --profile smoke`
- `uv run kups-tutorial verify 10 --profile smoke`
- `uv run kups-tutorial run 10 --profile full`
- `uv run kups-tutorial verify 10 --profile full`
- `uv run python scripts/generate_post10_figures.py`
- `uv run ruff check src/kups_md_tutorials/umbrella_sampling.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `python3 scripts/validate_kups_pages.py` in
  `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=index,10`
- `gh run download 29376446171 --name kups-md-page-snapshots --dir /tmp/kups-index-post10-snapshots`

Code and artifact review:

- `UmbrellaProtocolSummary` now records replica barrier height, barrier
  replica difference, and maximum local replica PMF difference.
- `umbrella_curves.csv` now exports each protocol's local
  `replica_abs_difference` curve.
- Post 10 verification now checks that dense windows improve forward/reverse
  PMF consistency relative to the sparse protocol.
- CSV writers use explicit LF line endings, and `git diff --check` passes.

Scientific review:

- Dense windows have forward/reverse replica PMF RMSE `0.1148` and maximum
  local replica PMF difference `0.6938`.
- Sparse windows have forward/reverse replica PMF RMSE `0.2352` and maximum
  local replica PMF difference `0.9656`.
- The dense barrier replica difference is `0.0206`; the sparse barrier replica
  difference is `0.0151`. This scalar is not the central comparison. The local
  replica-disagreement curve and replica PMF RMSE are more informative because
  they expose the missing-bridge region directly.

Figure feedback:

- The first revised four-panel figure used a barrier-difference annotation in
  the replica-disagreement panel. That was rejected as potentially misleading
  because the sparse scalar barrier difference was not larger in this seed.
- The accepted figure annotates dense/sparse replica PMF RMSE instead.
- The inspected full-profile figure snapshot
  `snapshots/post-10/umbrella_diagnostics_full_snapshot.png` shows a sparse
  local-disagreement spike near the missing bridge, while dense disagreement is
  mostly lower. Labels, legends, and panel titles fit.

Notebook review:

- The notebook now prints replica PMF RMSE, maximum local replica difference,
  and barrier replica difference for each protocol.
- `uv run jupyter execute notebooks/post-10-umbrella-sampling.ipynb --inplace`
  completed successfully during artifact regeneration.

Website and rendered-page review:

- The hidden index at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/` now mirrors the main
  `/blog/` listing structure more closely while keeping `nav: false`.
- The hidden Post 10 page caption and diagnostic prose now describe the
  four-panel figure and local replica-disagreement panel.
- Snapshot manifest reviewed:
  `/tmp/kups-index-post10-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for the hidden
  index and Post 10 page; all returned HTTP 200.
- Index snapshots inspected:
  `/tmp/kups-index-post10-snapshots/post-index-desktop.png` and
  `/tmp/kups-index-post10-snapshots/post-index-mobile.png`.
- Post 10 snapshots inspected:
  `/tmp/kups-index-post10-snapshots/post-10-desktop.png` and
  `/tmp/kups-index-post10-snapshots/post-10-mobile.png`.
- Desktop index feedback: the page renders in the same blog-list style as the
  main blog, lists all 12 tutorials, and does not add kUPS to the public nav.
- Mobile index feedback: the heading, status row, all tutorial entries, and
  repository block remain readable and contained.
- Desktop Post 10 feedback: the four-panel diagnostic renders in the article
  body without overflow; caption and surrounding prose are readable.
- Mobile Post 10 feedback: the figure scales inside the article column, the
  caption wraps, and no text overlap was found in the inspected snapshot.

## Update 2026-07-15: Uncertainty Status And Snapshot Refresh

- Website commit reviewed:
  `6901b0ec2115f565db9f6f1fcbaf44411373ea63`.
- Website deployment run:
  `29380373319`.
- Snapshot workflow run:
  `29380491599`.
- Snapshot artifact: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post10-uncertainty-status-snapshots/`.

Scope:

- No tutorial code or generated-data change was made in this pass.
- The hidden page status text was corrected to reflect the already implemented
  local replica-disagreement diagnostic.
- The final-release blocker was narrowed so it no longer treats all uncertainty
  diagnostics as missing. The remaining blocker is production MD context with
  real atomistic umbrella windows, model checks, and any production-level
  uncertainty intervals required by future public claims.

Validation:

- `python3 scripts/validate_kups_pages.py` passed in
  `../sungsoo-ahn.github.io`.
- `python3 scripts/validate_blog.py` passed in `../sungsoo-ahn.github.io` with
  pre-existing unused-image warnings.
- `git diff --check` passed in `../sungsoo-ahn.github.io`.
- Live check with `?v=6901b0e` confirmed the Post 10 page contains the updated
  replica-diagnostic status text.
- Live homepage and blog listing checks with `?v=6901b0e` confirmed
  `post-10-umbrella-sampling` and `kups-md-tutorials` are not exposed.

Scientific status:

- Dense windows retain forward/reverse replica PMF RMSE `0.1148`, maximum
  local replica PMF difference `0.6938`, and barrier replica difference
  `0.0206`.
- Sparse windows retain forward/reverse replica PMF RMSE `0.2352`, maximum
  local replica PMF difference `0.9656`, and barrier replica difference
  `0.0151`.
- The accepted uncertainty diagnostic for the controlled hidden draft is the
  local replica-disagreement curve plus forward/reverse replica PMF RMSE. It is
  not a substitute for production atomistic uncertainty intervals if later
  public claims depend on them.

Rendered-page review:

- Snapshot manifest reviewed:
  `/tmp/kups-post10-uncertainty-status-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`;
  both returned HTTP 200 and title
  `What Does Umbrella Sampling Actually Sample? | Sungsoo Ahn`.
- Desktop snapshot inspected:
  `/tmp/kups-post10-uncertainty-status-snapshots/post-10-desktop.png` at
  `1440 x 11224`.
- Mobile snapshot inspected:
  `/tmp/kups-post10-uncertainty-status-snapshots/post-10-mobile.png` at
  `452 x 17062`.
- Desktop feedback: the page renders end to end with source links, diagnostic
  tables, four-panel figure, practical checklist, reproduction block, updated
  Current Status section, references, and footer present. No blank page,
  missing figure, clipped text, or broken page chrome was found.
- Mobile feedback: the title, tables, figure, caption, code block, updated
  Current Status section, references, and footer remain contained. Tables are
  dense but readable, and no text overlap was found in the inspected snapshot.
