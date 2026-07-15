# Post 02 Review Notes

## Scope

- Post: 02
- Profiles reviewed: smoke and full
- Current status: harmonic-oscillator integrator diagnostic workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  expanded hidden website draft, rendered page snapshots, and self-review
  artifact are in place.

## Commands

- `uv run kups-tutorial run 02 --profile smoke`
- `uv run kups-tutorial verify 02 --profile smoke`
- `uv run kups-tutorial run 02 --profile full`
- `uv run kups-tutorial verify 02 --profile full`
- `uv run python scripts/generate_post02_figures.py`
- `uv run jupyter execute notebooks/post-02-integrators.ipynb --inplace`
- `uv run pytest -q`
- `uv run ruff check .`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`
- GitHub Pages deploy `29357398623` for website commit
  `53af3daa4dae1c5508ff143ee9fddf490634e86e`.
- GitHub Actions snapshot workflow `29357589065` for post 02.

## Code And Reproducibility Review

- Configs are committed under `configs/post-02/`.
- Smoke and full outputs are committed under `results/post-02/`.
- The workflow uses an exactly solvable harmonic oscillator, which makes
  integrator error, energy behavior, and reversibility checks reproducible
  without relying on noisy trajectory interpretation.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 02.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating integrator or plotting implementation details.

Open items:

- Later kUPS trajectory posts should reuse the same diagnostic language for
  normalized energy drift versus bounded energy oscillation.

## Scientific Review

- Velocity Verlet is compared against the exact harmonic oscillator trajectory,
  not only against another numerical method.
- The full profile sweeps `dt = 0.02, 0.05, 0.1, 0.2` for 2000 steps. The
  largest velocity-Verlet max relative energy error is about `1.0e-2`, while
  explicit Euler becomes unstable on the same grid.
- The forward/backward velocity-Verlet check returns to the initial state at
  roundoff scale (`< 4e-15` in the full profile), supporting the reversibility
  claim for this separable Hamiltonian test.
- The explicit Euler contrast is intentionally included as a negative control;
  it should not be framed as a serious MD production integrator.

Open items:

- Keep the harmonic-oscillator limitations explicit in the final all-post
  consistency pass; the article should not claim that this diagnostic certifies
  a production many-body timestep.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-02/integrator_diagnostics_snapshot.png`
- `snapshots/post-02/integrator_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable at the generated snapshot size,
  the three panels do not overlap, and the phase-space panel clearly shows the
  exact and velocity-Verlet orbits.
- The explicit Euler failure dominates the log-scale energy-error panel by many
  orders of magnitude. That is acceptable for the current diagnostic because
  the intended claim is contrastive, but the final website caption should make
  the negative-control role explicit.
- The forward/backward check text box is readable and stays inside the panel.

Open items:

- Consider a second zoomed velocity-Verlet-only energy panel if the prose needs
  a more detailed shadow-energy discussion.

## Notebook Review

- `notebooks/post-02-integrators.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps explanation at the level of maps and diagnostics rather
  than becoming the implementation source.

Open items:

- Re-execute the notebook if the article requests a second zoomed
  velocity-Verlet-only energy figure.

## Website Draft Review

- Added, expanded, and deployed a hidden draft page in
  `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-02-integrators/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post02_integrator_diagnostics.svg`.
- Expanded the article body from about 812 words to about 3,633 words. The
  expanded draft now covers discrete maps, velocity Verlet splitting,
  symplectic and reversible structure, harmonic-oscillator scope, bounded
  energy error, explicit Euler as a negative control, reversibility testing,
  force-evaluation scheduling, timestep practice, limitations, and the
  connection to timestep, precision, and MLIP force-error diagnostics.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes in the website repository with
  pre-existing unused-image warnings.
- `git diff --check` passes in the website repository.
- GitHub Pages deploy `29357398623` built and deployed website commit
  `53af3daa4dae1c5508ff143ee9fddf490634e86e` successfully.
- The deployed page snapshot manifest from workflow `29357589065` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `What Does an MD Integrator Actually Approximate? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post02-expanded-snapshots/post-02-desktop.png`
- `/tmp/kups-post02-expanded-snapshots/post-02-mobile.png`

Rendered feedback:

- Desktop full-page capture renders the expanded article end to end: sidebar
  table of contents, display equations, harmonic-oscillator configuration table,
  diagnostic figure, methods-practice table, reproduction code block,
  current-status section, references, and footer are present. No missing asset,
  blank page, obvious clipped text, or broken page chrome was found in the
  inspected snapshot.
- Mobile full-page capture renders the title, author note, equations, figure,
  code block, status, references, and footer. The methods-practice table is
  tight but readable and not clipped in the inspected screenshot. Keep table
  wrapping as a final typography-polish item after the remaining articles are
  expanded.

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

- Added text citations for Verlet in the opening integrator-map paragraph and
  for Leimkuhler/Reich plus Hairer/Lubich/Wanner in the shadow-energy
  diagnostic paragraph.
- Added matching `ref-*` anchors and reverse backlinks in `## References`.
- Live HTML contains the new `cite-*`, `ref-*`, and `href="#cite-*"` backlink
  anchors for all three references.
- Live `/` and `/blog/` checks found no `kups-md-tutorials` or
  `post-02-integrators` links, so the page remains direct-link only.

Rendered snapshots reviewed:

- `/tmp/kups-citation-backlinks-snapshots/post-02-desktop.png`
  (`1440 x 10461`).
- `/tmp/kups-citation-backlinks-snapshots/post-02-mobile.png`
  (`416 x 16214`).

Rendered feedback:

- Desktop capture shows the added citations inline, with equations, diagnostic
  figure, tables, code block, references, and footer still rendered cleanly.
- Mobile capture keeps the edited paragraphs and dense methods table contained
  within the article width; the reference backlinks are visible and legible.
- No figure asset changed, so no new figure snapshot was required.

Revision decision:

- Accepted for the hidden draft citation-backlink pass.

## Prose And Style Review

- The hidden website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, the author-note
  paragraph, compact reproduction commands, source links, and references.
- The prose is concept-led for MLIP-aware ML researchers: it starts from the
  discrete map being applied after initialization, then explains splitting,
  velocity Verlet, reversibility, shadow energy, timestep sensitivity, and why
  implementation conventions matter for production MD.

## Open Items

Blocking items for the current hidden draft:

- None. The hidden draft has source links, rendered desktop/mobile snapshot
  evidence, and an explicit direct-link-only status.

Non-blocking items accepted until the final article pass:

- The page remains intentionally hidden from public navigation while the full
  series is still under review.
- The methods-practice table is dense on mobile but readable in the inspected
  snapshot.

Final-release blockers:

- Make the page public only after the series-level final production and
  public-indexing pass.
- Re-run rendered desktop/mobile snapshots after any public-indexing change.

## Update 2026-07-15: Explicit Integrator Seed

Scope and provenance:

- Added explicit fixed seed `2026071402` to both Post 02 profiles in
  `configs/post-02/smoke.json` and `configs/post-02/full.json`.
- Extended the typed integrator config schema and compact
  `integrator_summary.json` so the deterministic integrator diagnostic records
  the same fixed-seed convention as the stochastic posts.
- Regenerated `results/post-02/smoke/` and `results/post-02/full/`, executed
  `notebooks/post-02-integrators.ipynb`, regenerated the Post 02 figure
  snapshots, and exported the refreshed full-profile compact JSON assets to
  `../sungsoo-ahn.github.io`.

Commands:

- `uv run kups-tutorial run 02 --profile smoke` passed.
- `uv run kups-tutorial verify 02 --profile smoke` passed.
- `uv run kups-tutorial run 02 --profile full` passed.
- `uv run kups-tutorial verify 02 --profile full` passed.
- `uv run python scripts/generate_post02_figures.py` passed.
- `uv run jupyter execute notebooks/post-02-integrators.ipynb --inplace`
  passed.
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io`
  passed and restored all twelve posts in the export manifest.

Code and reproducibility review:

- The integrator workflow remains deterministic, but the config now carries a
  machine-readable seed so every tutorial profile has an explicit fixed-seed
  field.
- The full manifest records `config.experiment.seed = 2026071402` and
  `provenance.config_sha256 =
  f50d0058bc90342e80be4a9ea6e7b25bbd7defbfe39a5bec72e27056ea46e388`.
- The full compact summary records `seed = 2026071402`, the same config hash,
  and eight run summaries.
- Added a release-readiness regression that removes the Post 02 seed and
  expects `missing explicit fixed seed`.

Figure feedback review:

- Smoke figure snapshot inspected:
  `snapshots/post-02/integrator_diagnostics_snapshot.png` (`1952 x 576`).
- Full figure snapshot inspected:
  `snapshots/post-02/integrator_diagnostics_full_snapshot.png`
  (`1952 x 576`).
- Intended visual claim: the figure should show that velocity Verlet preserves
  the oscillator phase-space structure and keeps bounded energy/reversibility
  error while explicit Euler has scheme-dependent runaway energy error.
- Smoke feedback: axis labels, legend, timestep labels, and the
  forward/backward annotation are readable; the annotation does not cover the
  bars; no clipping or caption mismatch was found.
- Full feedback: the log-scale energy-error panel clearly separates velocity
  Verlet from explicit Euler over all timesteps; the phase-space orbit and
  reversibility panel remain readable at the inspected raster size.
- Revision decision: accepted without a figure edit. The figure assets were
  regenerated from the updated summaries but the visual content remains
  consistent with the prior hidden draft.

Website page review:

- No website prose, front matter, figure include, caption, or CSS-sensitive
  markup changed.
- The website export manifest now contains 71 files across posts 01-12, and
  the Post 02 exported full summary/manifest include seed `2026071402`.
- No rendered desktop/mobile page snapshot was required for this data-only
  export refresh because the rendered hidden page does not consume the compact
  JSON assets directly.

Open items:

Blocking items for the current hidden draft:

- None. The hidden draft remains direct-link only and the integrator package
  now has explicit seed provenance.

Non-blocking items accepted until the final article pass:

- The page remains intentionally hidden from public navigation while the full
  series is still under review.

Final-release blockers:

- Make the page public only after the series-level final production and
  public-indexing pass.
- Re-run rendered desktop/mobile snapshots after any public-indexing change.
