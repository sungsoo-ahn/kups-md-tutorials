# Post 11 Review Notes

## Scope And Provenance

- Post: 11
- Profiles reviewed: smoke and full
- Current status: controlled adaptive-bias and nonequilibrium-work workflow,
  compact smoke/full outputs, notebook, full-profile diagnostic figure, figure
  snapshots, and this self-review artifact are in place; the hidden website
  draft is in place.
- Working-tree state: post 11 implementation is uncommitted during this review
  pass.
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

- Capture rendered desktop and mobile page snapshots after the hidden draft
  deploys.

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

- The final article should state that the pulling work ensemble is controlled
  for identity diagnostics and is not a full steered-MD integrator.
- The final article should contrast adaptive-bias samples, unbiased samples,
  and path-ensemble averages explicitly.
- The final article should connect nonequilibrium work identities to the path
  measure language used in the existing blog.

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

Open items:

- Recheck figure readability inside the rendered hidden webpage at desktop and
  mobile widths.
- If the final article adds real steered-MD trajectory panels, repeat the same
  snapshot review for those publication assets.

## Notebook Review

- `notebooks/post-11-enhanced-sampling.ipynb` loads smoke and full
  configurations, prints committed full-summary diagnostics, and regenerates
  the full-profile enhanced-sampling figure from committed result files.
- `uv run jupyter execute notebooks/post-11-enhanced-sampling.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post11_enhanced_sampling_diagnostics.svg`.
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
  modified sampling measures and path ensembles, then explain metadynamics,
  well-tempered bias, steered work, Jarzynski, and Crooks as corrections to
  those measures.

## Open Items

Blocking items for the current hidden draft:

- Verify the deployed hidden URL after the website commit is pushed.
- Confirm that public navigation does not link to the hidden page.

Non-blocking items accepted until the final article pass:

- Rendered page snapshots are still pending.
- The draft will remain short and explicitly non-final.

Final-release blockers:

- Expand the prose to a full article with citations for metadynamics,
  well-tempered metadynamics, Jarzynski equality, Crooks fluctuation theorem,
  and steered MD.
- Add production MD context and any final diagnostics needed for the public
  article.
- Resolve rendered desktop/mobile page snapshot feedback.
