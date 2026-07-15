# Post 01 Review Notes

## Scope

- Post: 01
- Profiles reviewed: smoke and full
- Current status: initialization workflow, committed smoke/full outputs,
  notebook, full-profile diagnostic figure, expanded hidden website draft,
  rendered page snapshots, and self-review artifacts are in place.

## Commands

- `uv run kups-tutorial run 01 --profile smoke`
- `uv run kups-tutorial verify 01 --profile smoke`
- `uv run kups-tutorial run 01 --profile full`
- `uv run kups-tutorial verify 01 --profile full`
- `uv run python scripts/generate_post01_figures.py`
- `uv run jupyter execute notebooks/post-01-initialization.ipynb --inplace`
- `uv run pytest -q`
- `uv run ruff check .`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`
- `curl -I -L https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`
- attempted `npx --yes playwright@latest screenshot ...` for desktop/mobile
  snapshots; blocked because the local Node.js is 12.22.9 and Playwright
  requires Node.js 18 or higher.
- GitHub Pages deploy `29356354203` for website commit
  `6534a212ddd9baa6403c57558b19c9b6daab8d15`.
- GitHub Actions snapshot workflow `29356548516` for post 01.

## Code And Reproducibility Review

- Configs are committed under `configs/post-01/`.
- Smoke outputs are committed under `results/post-01/smoke/`.
- Full initialization outputs are committed under `results/post-01/full/`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- Velocity initialization uses ASE `thermalize_momenta` with a fixed RNG seed.
- Center-of-mass momentum removal is enabled and verified from the compact
  summary.

Open items:

- Keep the compact summary in sync if the initialization workflow changes.

## Scientific Review

- The smoke initial state has 32 argon atoms at the configured number density.
- The full initial state has 500 argon atoms at the same configured number
  density and gives a smoother velocity-component histogram for the website
  diagnostic figure.
- The kinetic temperature is a stochastic Maxwell-Boltzmann draw, not forced to
  the target temperature. The observed difference between target and sample
  temperature is expected for finite systems and should be explained in the
  article.
- The figure should not imply that the histogram is a converged
  distributional test; it is a diagnostic snapshot of deterministic
  initialization.

Open items:

- Recheck the exact-temperature explanation after the integrator and thermostat
  articles are expanded, so the terminology is consistent across posts.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-01/initialization_diagnostics_snapshot.png`
- `snapshots/post-01/initialization_diagnostics_full_snapshot.png`

Feedback loop:

- First pass found that the residual total momentum panel was dominated by
  rounded momenta read back from `initial_state.extxyz`, not the exact
  diagnostics stored in `initialization_summary.json`.
- Revised the third panel into an initialization checklist driven by the JSON
  summary. This avoids presenting file-format rounding as a physical residual
  momentum.
- Second pass: labels are readable at the generated snapshot size, panels do
  not overlap, and the figure communicates cell construction, seeded velocity
  sampling, and provenance checks.
- Full-profile pass: the 500-atom figure has a smoother standardized velocity
  histogram, preserves the same checklist/provenance design, and is the better
  website draft asset. The snapshot labels remain readable.

Open items:

- Recheck figure placement after the final all-post typography pass.

## Notebook Review

- `notebooks/post-01-initialization.ipynb` executes from a clean kernel.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating initialization or plotting implementation details.
- The notebook loads both smoke and full configurations, displays both
  committed summaries, and regenerates the full-profile diagnostic figure from
  the committed initial state.

Open items:

- Re-execute the notebook if the article requests any new numerical table or
  figure beyond the current initialization diagnostics.

## Website Draft Review

- Added, expanded, and deployed a hidden draft page in
  `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post01_initialization_diagnostics.svg`.
- Expanded the article body from about 766 words to about 3,765 words. The
  expanded draft now covers the initialization contract, density/cell
  construction, finite-system velocity sampling, exact-temperature rescaling,
  center-of-mass removal, minimization and warmup boundaries, provenance,
  methods reporting, controlled replicas, and connections to the later
  integrator, thermostat, free-energy, and MLIP posts.
- Replaced inline `\(...\)` notation in the expanded prose with plain notation
  where this Jekyll stack rendered inline math delimiters as ordinary
  parentheses. Display equations remain in display-math form.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes in the website repository with
  pre-existing unused-image warnings.
- `git diff --check` passes in the website repository.
- GitHub Pages deploy `29356354203` built and deployed website commit
  `6534a212ddd9baa6403c57558b19c9b6daab8d15` successfully.
- The deployed page snapshot manifest from workflow `29356548516` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do You Initialize an MD Simulation Without Biasing the Result? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post01-final-snapshots/post-01-desktop.png`
- `/tmp/kups-post01-final-snapshots/post-01-mobile.png`

Rendered feedback:

- Desktop full-page capture renders the expanded article end to end: sidebar
  table of contents, equations, initialization table, density equation, figure,
  minimization/warmup table, reproduction commands, current-status section,
  references, and footer are present. No missing figure, blank page, obvious
  clipped text, or broken page chrome was found in the inspected snapshot.
- Mobile full-page capture renders the title, author note, article sections,
  equations, figure, code blocks, status, references, and footer. The two
  tables are narrow but remain readable and are not clipped in the inspected
  screenshot. Keep table wrapping as a final typography-polish item when the
  rest of the series reaches full article length.

Open items:

- The page remains intentionally hidden from public navigation.

## Citation Backlink Refresh 2026-07-15

Scope and provenance:

- Website commit reviewed: `d244d57`.
- Website deploy run: `29413487745`.
- Snapshot workflow: `29413685814`.
- Snapshot artifact downloaded to `/tmp/kups-citation-backlinks-snapshots/`.
- Live cache-busted HTML checked with `?v=d244d57`.

Website and prose review:

- Added the first text citations for Frenkel & Smit and Tuckerman in the
  initialization-statistical-measure paragraph.
- Added matching `ref-*` anchors and reverse backlinks in `## References`.
- Live HTML contains `cite-frenkel2001`, `cite-tuckerman2010`,
  `ref-frenkel2001`, `ref-tuckerman2010`, and matching `href="#cite-*"`
  backlinks.
- Live `/` and `/blog/` checks found no `kups-md-tutorials` or
  `post-01-initialization` links, so the page remains direct-link only.

Rendered snapshots reviewed:

- `/tmp/kups-citation-backlinks-snapshots/post-01-desktop.png`
  (`1440 x 10870`).
- `/tmp/kups-citation-backlinks-snapshots/post-01-mobile.png`
  (`428 x 16938`).

Rendered feedback:

- Desktop capture shows the added citation paragraph in the introduction
  without line-wrap or spacing issues; figure, tables, code blocks, references,
  and footer remain contained.
- Mobile capture keeps the edited paragraph, tables, code block, and
  References section within the article width. The new backlink markers remain
  readable at the bottom.
- No figure asset changed, so no new figure snapshot was required.

Revision decision:

- Accepted for the hidden draft citation-backlink pass.

## Prose And Style Review

- The hidden website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, the author-note
  paragraph, compact reproduction commands, source links, and references.
- The prose is concept-led for MLIP-aware ML researchers: it starts from
  simulation initialization as a reproducibility contract, then explains cell
  construction, seeded velocities, center-of-mass removal, warmup boundaries,
  provenance, and why initialization choices affect later integrator,
  thermostat, and free-energy claims.

## Open Items

Blocking items for the current hidden draft:

- None. The hidden draft has source links, rendered desktop/mobile snapshot
  evidence, and an explicit direct-link-only status.

Non-blocking items accepted until the final article pass:

- The page remains intentionally hidden from public navigation while the full
  series is still under review.
- Table wrapping and final typography can be revisited after the public-index
  pass, but the captured hidden draft is readable and contained.

Final-release blockers:

- Make the page public only after the series-level final production and
  public-indexing pass.
- Re-run rendered desktop/mobile snapshots after any public-indexing change.
