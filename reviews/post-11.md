# Post 11 Review Notes

## Scope And Provenance

- Post: 11
- Profiles reviewed: smoke and full
- Current status: controlled adaptive-bias and nonequilibrium-work workflow,
  compact smoke/full outputs, notebook, full-profile diagnostic figure, figure
  snapshots, expanded hidden website draft, rendered page snapshots, and this
  self-review artifact are in place. The page remains hidden from public
  navigation.
- Working-tree state: website expansion committed as
  `38df18dbbe3a785ed1d380d499735b6473dc09d1`; this repository has review
  updates staged for the current pass.
- Hidden draft URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`

## Commands

- `uv run kups-tutorial run 11 --profile smoke`
- `uv run kups-tutorial verify 11 --profile smoke`
- `uv run kups-tutorial run 11 --profile full`
- `uv run kups-tutorial verify 11 --profile full`
- `uv run python scripts/generate_post11_figures.py`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-11-enhanced-sampling.ipynb --inplace`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `uv run pytest -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify --profile smoke`
- `uv run kups-tutorial verify 11 --profile full`
- `git diff --check` in this repository and `../sungsoo-ahn.github.io`
- `gh run watch 29350802100 --exit-status` in `../sungsoo-ahn.github.io`
- `curl -I -L 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/?v=045f8ba'`
- `curl -L --silent 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/?v=045f8ba' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/?v=045f8ba' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/blog/?v=045f8ba' | rg ...`
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_kups_pages.py`
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_blog.py`
- expanded post whitespace check in `../sungsoo-ahn.github.io`:
  `git diff --check`
- inline math delimiter check in `../sungsoo-ahn.github.io`:
  `rg -n '\\\\(|\\\\)' _pages/kups-md-post-11-enhanced-sampling.md || true`
- word-count check for the expanded page: `3544` words
- `gh run watch 29365244839 --exit-status` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=11` in
  `../sungsoo-ahn.github.io`
- `gh run watch 29365419119 --exit-status` in `../sungsoo-ahn.github.io`
- `gh run download 29365419119 --name kups-md-page-snapshots --dir /tmp/kups-post11-expanded-snapshots`
- live hidden-route check with cache buster `?v=38df18d`
- live homepage/blog listing checks with cache buster `?v=38df18d`

## Code And Reproducibility Review

- Configs are committed-intended under `configs/post-11/`.
- Smoke and full outputs are committed-intended under `results/post-11/`.
- The workflow uses a deterministic double-well coordinate with fixed seeds.
  The adaptive-bias diagnostic samples from the biased distribution and deposits
  well-tempered Gaussian hills. The nonequilibrium diagnostic uses controlled
  Gaussian work ensembles that satisfy the Crooks/Jarzynski relationship by
  construction while retaining finite dissipated work.
- The summary records bias range, reconstructed barrier error, basin/barrier
  visitation fractions, histogram flatness, forward/reverse work means,
  Jarzynski estimates, Crooks crossing, dissipated work, work standard
  deviations, and exponential-weight ESS fractions.
- The manifest records the loaded config, compact output filenames, config
  hash, Git revision, Python/platform metadata, and kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 11.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather
  than reimplementing metadynamics, work estimators, or plotting.

Open items:

- None for the controlled code/reproducibility slice in the current hidden
  draft.

## Scientific Review

- The full metadynamics-style run deposits `3000` hills with hill height
  `0.030`, hill width `0.12`, and bias factor `10.0`.
- The final bias range is `6.534`, reconstructed barrier error is `0.0922`,
  and the final histogram flatness is `0.664`. These values support the claim
  that adaptive bias changes where the trajectory spends time rather than
  directly producing an unbiased trajectory.
- Basin visitation is balanced: left basin fraction `0.360`, right basin
  fraction `0.362`, and barrier-region fraction `0.135`.
- The full nonequilibrium pulling diagnostic has true free-energy difference
  effectively zero. Forward mean work is `0.170`, reverse mean work is `0.173`,
  so both directions show positive dissipated work.
- Jarzynski estimates recover the answer within finite-sample noise: forward
  `0.0011`, reverse `-0.0090`. The Crooks crossing estimate is `-0.0007`.
- Forward and reverse exponential-weight ESS fractions are `0.716` and
  `0.722`, high enough for this controlled diagnostic to be a teaching example
  rather than a rare-event failure case.

Open items:

- The expanded hidden page now states that the pulling work ensemble is
  controlled for identity diagnostics and is not a full steered-MD integrator.
- The expanded hidden page now contrasts adaptive-bias samples, unbiased samples,
  and path-ensemble averages explicitly.
- The expanded hidden page now connects nonequilibrium work identities to the
  path-measure language used in the existing blog.

## Figure Feedback Review

Snapshots reviewed:

- `snapshots/post-11/enhanced_sampling_diagnostics_snapshot.png`
- `snapshots/post-11/enhanced_sampling_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: the adaptive-bias panel is readable and shows the
  true PMF, the PMF reconstructed from final bias, and the scaled final bias
  without legend or line overlap.
- The bias-growth panel makes history dependence visible and the basin/barrier
  visitation annotation fits without obscuring the curve.
- The work-distribution panel shows the forward and reverse path ensembles,
  positive mean-work separation, and the true/Jarzynski/Crooks markers near the
  free-energy difference.
- No label clipping, unreadable ticks, or misleading scale was found in the
  inspected full-profile snapshot.

Rendered page figure check:

- The figure was inspected inside the rendered desktop snapshot
  `/tmp/kups-post11-expanded-snapshots/post-11-desktop.png` and mobile
  snapshot `/tmp/kups-post11-expanded-snapshots/post-11-mobile.png`.
- Desktop: the adaptive PMF/bias, bias-growth, and work-distribution panels
  render below the diagnostic section, with axes, markers, and caption readable
  in the article column. No clipping or broken asset was visible.
- Mobile: the figure remains legible at 390 px capture width. The panel text is
  small but readable enough for the hidden draft, and the caption wraps without
  overlapping neighboring text.

Open items:

- If the final article adds real steered-MD trajectory, uncertainty, or
  hysteresis panels, repeat the same snapshot review for those publication
  assets.

## Notebook Review

- `notebooks/post-11-enhanced-sampling.ipynb` loads smoke and full
  configurations, prints committed full-summary diagnostics, and regenerates
  the full-profile enhanced-sampling figure from committed result files.
- `uv run jupyter execute notebooks/post-11-enhanced-sampling.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`.
- Expanded the hidden page to `3544` words with additional sections on
  adaptive measure changes, well-tempered bias parameters, adaptive estimator
  metadata, nonequilibrium path ensembles, exponential averaging fragility,
  Crooks diagnostics, pulling protocol design, hysteresis, reporting limits,
  methods reporting, and production MD extension.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post11_enhanced_sampling_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `python3 scripts/validate_kups_pages.py` passes.
- GitHub Pages deployment `29350802100` completed successfully. The live
  hidden URL returns HTTP 200 and contains the expected title,
  enhanced-sampling notebook link, full summary link, current-status section,
  Jarzynski/Crooks text, and
  `kups_md_post11_enhanced_sampling_diagnostics.svg` figure.
- The public homepage and blog index did not contain
  `post-11-enhanced-sampling` or `kups-md-tutorials` in the deployed HTML
  checked with cache-buster `?v=045f8ba`.
- Expanded-page GitHub Pages deployment `29365244839` completed successfully
  for website commit `38df18dbbe3a785ed1d380d499735b6473dc09d1`.
- Snapshot workflow `Capture kUPS snapshots` run `29365419119` completed
  successfully for post 11. Artifact `kups-md-page-snapshots` was downloaded
  to `/tmp/kups-post11-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post11-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`;
  both returned HTTP 200 and title
  `How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post11-expanded-snapshots/post-11-desktop.png` at
  `1440 x 10685` and `/tmp/kups-post11-expanded-snapshots/post-11-mobile.png`
  at `390 x 16732`.
- Desktop feedback: the expanded article renders end to end with sidebar table
  of contents, hidden-draft note, source links, adaptive-bias and
  nonequilibrium-work tables, figure, protocol/methods sections, practical
  checklist, reproduction block, current-status section, references, and
  footer present. No blank page, missing figure, clipped text, or broken page
  chrome was found in the inspected snapshot.
- Mobile feedback: the title wraps heavily but remains contained. Tables are
  tight but readable, the diagnostic figure and caption stay within the page,
  the reproduction code block is contained, and the footer renders normally.
- Live hidden-route check with `?v=38df18d` confirmed the expanded section
  `What Should Not Be Claimed?`, the figure asset, the non-final note, and the
  rendered snapshot status phrase.
- Live homepage and blog listing checks with `?v=38df18d` confirmed
  `post-11-enhanced-sampling` and `kups-md-tutorials` are not exposed.

Open items:

- No blocking layout issue was found for the expanded post 11 hidden draft.
- Keep mobile title/table wrapping as a final typography-polish item after the
  rest of the articles are expanded.
- Re-run rendered desktop/mobile snapshots after adding any final production MD
  or uncertainty figures.

## Prose And Style Review

- The expanded website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose is concept-led for MLIP-aware ML researchers: it starts from
  modified sampling measures and path ensembles, then explains metadynamics,
  well-tempered bias, steered work, Jarzynski, Crooks, ESS, and hysteresis as
  estimator and protocol diagnostics.

## Open Items

Blocking items for the current hidden draft:

- None.

Non-blocking items accepted until the final article pass:

- The expanded draft remains explicitly non-final.
- Mobile title and table wrapping can be polished later if desired, but the
  captured hidden draft is readable and contained.

Final-release blockers:

- Add production MD context with real atomistic steered trajectories and any
  final diagnostics needed for the public article, including final uncertainty
  diagnostics.
- Re-run rendered desktop/mobile snapshots after any final production MD or
  figure additions.

## Update 2026-07-14: Steered-Trajectory Hysteresis Diagnostic

- Tutorial commit reviewed:
  `cc48b6e98842111e8bba2882545d19a21e4d0bcd`.
- Tutorial verification run:
  `29377110812`.
- Website commits reviewed:
  `8e7dfec3f3a3f56fb346d85fb99a6b7a11cce2de` and
  `ba3944c7bd14b1b8966d6676b88a8af9fc662d40`.
- Website deployment runs:
  `29377110434` and final deploy `29377412704`.
- Snapshot workflow runs:
  first pass `29377264543` and final pass `29377552573`.
- Final snapshot artifact: `kups-md-page-snapshots`.
- Downloaded final review copy:
  `/tmp/kups-post11-final-hysteresis-snapshots/`.

Commands added in this pass:

- `uv run kups-tutorial run 11 --profile smoke`
- `uv run kups-tutorial verify 11 --profile smoke`
- `uv run kups-tutorial run 11 --profile full`
- `uv run kups-tutorial verify 11 --profile full`
- `uv run python scripts/generate_post11_figures.py`
- `uv run jupyter execute notebooks/post-11-enhanced-sampling.ipynb --inplace`
- `uv run ruff check src/kups_md_tutorials/enhanced_sampling.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `python3 scripts/validate_kups_pages.py` in
  `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=11`
- `gh run download 29377552573 --name kups-md-page-snapshots --dir /tmp/kups-post11-final-hysteresis-snapshots`

Code and reproducibility review:

- `EnhancedSamplingExperimentSummary` now includes a
  `steered_hysteresis` block derived from the path-level pulling simulator,
  separate from the controlled Gaussian Jarzynski/Crooks work ensemble.
- The full profile compares a fast 65-step steered protocol to a slow 520-step
  protocol with 6000 path replicas.
- `enhanced_sampling_curves.csv` now exports fast/slow forward/reverse
  steered-work arrays in addition to the adaptive-bias and Gaussian work
  curves.
- Post 11 verification now requires the fast steered protocol to have a larger
  hysteresis gap than the slow protocol and requires the fast/slow gap ratio to
  exceed `1.25`.
- CSV writing for Post 11 curves now uses explicit LF line endings; whitespace
  checks passed.

Scientific review:

- The controlled Gaussian work ensemble remains the identity check for
  Jarzynski/Crooks: forward Jarzynski `0.0011`, reverse Jarzynski `-0.0090`,
  Crooks crossing `-0.0007`, and true \(\Delta F\) approximately zero.
- The new path-level steered diagnostic is a protocol hysteresis check, not a
  free-energy estimator. It intentionally remains separate from the
  Jarzynski/Crooks identity panel.
- Full-profile fast steered hysteresis gap is `33.7415 +/- 0.2534`.
- Full-profile slow steered hysteresis gap is `5.5457 +/- 0.1116`.
- The fast/slow hysteresis-gap ratio is `6.08`, supporting the prose claim
  that faster pulling increases forward/reverse hysteresis in this controlled
  path model.
- The page now states that a final public article should replace this
  controlled path model with real atomistic steered trajectories rather than
  overclaiming the hidden draft as production MD.

Figure feedback:

- Figure source data inspected:
  `results/post-11/full/enhanced_sampling_summary.json` and
  `results/post-11/full/enhanced_sampling_curves.csv`.
- Figure asset inspected:
  `figures/post-11/enhanced_sampling_diagnostics_full.svg`.
- Snapshot inspected:
  `snapshots/post-11/enhanced_sampling_diagnostics_full_snapshot.png`.
- Intended visual claim: adaptive bias modifies the sampled measure,
  nonequilibrium work is a path ensemble rather than mean work, and faster
  steered pulling produces a larger forward/reverse hysteresis loop than slower
  pulling.
- Feedback: the new fourth panel makes the fast/slow hysteresis ordering
  obvious; the fast bar dominates, the slow bar and uncertainty marker remain
  visible, and the annotation reports `path replicas = 6000` and `fast/slow
  gap = 6.08`. The y-axis label, x-tick labels, panel title, and neighboring
  panels fit without clipping. The fast uncertainty bar is visually small
  because the path-replica standard error is small relative to the gap; this is
  accepted for the hidden draft because the exact value is printed in the
  summary and notebook.
- Revision decision: no additional figure edit was needed after inspecting the
  four-panel snapshot.

Notebook review:

- The notebook now prints fast/slow protocol step counts, hysteresis gaps with
  standard errors, and the fast/slow gap ratio.
- Executed notebook output records fast gap `33.7415 +/- 0.2534`, slow gap
  `5.5457 +/- 0.1116`, and ratio `6.08`.
- `uv run jupyter execute notebooks/post-11-enhanced-sampling.ipynb --inplace`
  completed successfully.

Website and rendered-page review:

- The hidden page now describes the fourth steered-trajectory hysteresis panel
  and distinguishes it from the Gaussian Jarzynski/Crooks identity check.
- The Current Status section now lists rendered desktop/mobile snapshots for
  the latest four-panel figure as implemented while keeping production
  atomistic steered trajectories as a missing final-release item.
- Final snapshot manifest reviewed:
  `/tmp/kups-post11-final-hysteresis-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`;
  both returned HTTP 200 and title
  `How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work? | Sungsoo Ahn`.
- Final snapshots visually inspected:
  `/tmp/kups-post11-final-hysteresis-snapshots/post-11-desktop.png` and
  `/tmp/kups-post11-final-hysteresis-snapshots/post-11-mobile.png`.
- Desktop feedback: the long hidden article renders end to end with sidebar,
  source links, diagnostic tables, updated four-panel figure, caption,
  reproduction block, Current Status section, references, and footer present.
  No broken figure, blank page, clipped text, or page chrome issue was found.
- Mobile feedback: the title wraps heavily but remains contained; tables and
  code blocks are tight but readable; the four-panel figure scales inside the
  article column; the hysteresis panel is small but still legible enough for
  the hidden draft; the status section now reflects that snapshots were
  captured.
