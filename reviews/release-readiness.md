# Release Readiness Review Notes

## Scope And Provenance

- Scope: final-publication gate for the twelve-post kUPS MD tutorial series.
- Current status: a `verify-release-readiness` CLI command is implemented and
  intentionally fails while final-release blockers remain.
- Current working-tree state: release-readiness artifact-surface gate update
  on top of tutorial commit `a423bff`; no configs, results, notebooks,
  figures, snapshots, website pages, or website assets changed in this pass.
- Hidden website drafts remain the current intended publication state until
  final production diagnostics are complete.

## Commands

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site || true`
- `uv run kups-tutorial verify-release-readiness || true`
- `git diff --check`

## Code And Reproducibility Review

- Added `src/kups_md_tutorials/release_readiness.py`.
- Added CLI command `kups-tutorial verify-release-readiness`.
- The command checks post-level review notes for unresolved final-release
  blockers, checks post 12 config/result metadata for placeholder MACE artifact
  markers, and optionally checks the website repository for hidden or non-final
  page state. The placeholder check remains part of the gate even though the
  current committed Post 12 configs/results now contain pinned MACE artifact
  metadata.
- The command is intentionally separate from routine CI because it should fail
  until the final GPU/model/publication pass is complete.
- Added `tests/test_release_readiness.py` with a clean final-state fixture,
  current-project blocker detection, and hidden-site detection.

## Scientific Review

- The release gate preserves the scientific distinction between hidden draft
  completion and public scientific completion.
- The current failure output correctly identifies production diagnostics that
  are still needed: argon/kUPS physical diagnostics, final estimator and
  enhanced-sampling figures where applicable, real MACE/fcc-Al GPU results,
  and post-snapshot recapture after final changes.
- The post 12 placeholder MACE metadata check remains a hard release blocker
  in the implementation and tests, but the current project state no longer
  triggers that blocker because `mace-mp-0b3-medium.model`, revision
  `e291ace`, and SHA-256
  `2f2be696351ac9e94fbe01cdfb6f017679acdbd2db7645209ef55fec9826b012`
  are recorded in Post 12 configs/results/manifests.

## Figure Feedback Review

- No new figure assets were generated or modified in this pass.
- Existing figure snapshot evidence remains in `reviews/post-01.md` through
  `reviews/post-12.md` and the shared `reviews/page-snapshots.md` ledger.
- Because the implementation only adds a textual release audit command, no
  new figure snapshot capture was required for this milestone.

## Website Page Review

- No website page content or layout was modified in this pass.
- The new release gate checks website page state when `--site-root` is not
  skipped. Against `../sungsoo-ahn.github.io`, it correctly reports that all
  twelve kUPS pages remain hidden with `nav: false`, still declare themselves
  non-final, and still contain hidden-draft notes.
- Existing rendered page snapshots for all twelve hidden drafts are recorded in
  `reviews/page-snapshots.md`.

## Prose And Style Review

- Updated `README.md` to list `uv run kups-tutorial verify-release-readiness`
  and to state that it is expected to fail while hidden drafts,
  final-release blockers, or placeholder model artifacts remain.
- Updated `PLAN.md` verification and progress-log sections to include the new
  final-publication gate.

## Update 2026-07-15: Current Gate State Refresh

Scope:

- Refreshed this review ledger so it no longer describes placeholder Post 12
  MACE metadata as a current blocker.
- No release-readiness code, CLI behavior, tests, configs, results, notebooks,
  figures, website pages, or website assets changed in this pass.

Commands:

- `uv run kups-tutorial verify-reviews`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 140`
- `git diff --check`

Review decision:

- The release-readiness gate still fails intentionally for final publication.
- The expected current blocker set is hidden/public-release status plus
  production diagnostics, including the real MACE/fcc-Al GPU capstone.
- The expected current blocker set does not include placeholder Post 12 MACE
  metadata; `tests/test_release_readiness.py` explicitly checks that the
  current project audit reports the real GPU capstone and does not report a
  placeholder model artifact blocker.
- No figure snapshot feedback was required because no figure asset or figure
  generation code changed.
- No rendered page snapshot feedback was required because no website prose,
  front matter, linked figure, CSS-sensitive markup, or page asset changed.

## Update 2026-07-15: Required Artifact Surface Gate

Scope:

- Expanded `verify-release-readiness` so final release now checks the required
  artifact surface for every post, not only review blockers and Post 12 model
  metadata.
- Added release-gate coverage for both smoke/full configs, smoke/full result
  manifests, compact `*_summary.json` files, exactly one notebook per post,
  publication SVG/PNG figures, full-profile SVG/PNG figures, and both figure
  snapshot PNGs for all twelve posts.
- Added `--notebook-root`, `--figure-root`, and `--snapshot-root` CLI
  arguments so the audit can be tested against isolated final-state fixtures.
- Updated release-readiness tests to create a complete clean final-state
  fixture and to prove missing notebooks or figure snapshots are reported.
- No tutorial configurations, results, notebooks, figures, local snapshots,
  website pages, or website assets changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py src/kups_md_tutorials/cli.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 160`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 80`

Code and reproducibility review:

- The expanded gate validates JSON syntax for configs, manifests, compact
  summaries, and notebooks.
- The current checkout has the required artifact surface, so the
  `--skip-site` audit still reports only the existing final-release blockers:
  hidden/public-indexing state and missing production GPU diagnostics.
- The clean final-state fixture no longer relies on real checkout notebooks or
  figures; it passes explicit artifact roots through the API and CLI.
- The missing-artifact test removes one notebook and one figure snapshot and
  confirms both are reported.
- The placeholder-model test writes `pinned-placeholder` and
  `pending-gpu-artifact-hash` metadata and confirms the hard blocker is still
  reported.

Figure and rendered-page review:

- No figure asset or figure-generation code changed, so no new figure snapshot
  capture was required.
- No website prose, front matter, linked figure, CSS-sensitive markup, or page
  asset changed, so no rendered page snapshot capture was required.
- Existing figure and page snapshot evidence remains in `reviews/post-01.md`
  through `reviews/post-12.md` and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now better represents the PLAN requirement that
  every final post has configs, compact outputs, notebooks, figures, snapshots,
  review evidence, and clean publication state.
- Final release remains blocked on the production GPU/public-indexing items
  reported by `uv run kups-tutorial verify-release-readiness`.

## Update 2026-07-15: Website Blog-Style Gate

Scope:

- Expanded the site-aware `verify-release-readiness` checks so final release
  now audits the kUPS page blog-style contract from `PLAN.md`.
- Added checks for `layout: post`, tutorial `post_type`, author metadata,
  shared series metadata, `series_order`, `order`, title/date/last-updated
  fields, description, categories, tags, `toc.sidebar: left`,
  `related_posts: false`, post-number permalink, muted author-note paragraph,
  `Note:` marker, and source repository link text.
- Updated the clean final-state site fixture in `tests/test_release_readiness.py`
  to represent blog-style kUPS pages instead of minimal stubs.
- Added a regression test that removes `post_type: tutorial`, the TOC sidebar,
  and the author-note marker and confirms the release gate reports each style
  violation.
- No website pages or website assets changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 140`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 100`

Code and reproducibility review:

- The style gate is scoped to site-aware readiness checks; `--skip-site`
  remains focused on repository-side blockers and artifact surface.
- The current hidden website pages satisfy the new blog-style checks. The
  site-aware audit reports hidden/non-final page state and hidden-draft notes,
  but no missing front matter, series metadata, TOC, author-note, or source-link
  violations.
- The checks intentionally keep hidden pages under `_pages` for the current
  direct-link workflow while enforcing the al-folio post layout and metadata
  contract on those hidden pages.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no new figure snapshot
  capture was required.
- No website prose, front matter, linked figure, CSS-sensitive markup, or page
  asset changed, so no rendered page snapshot capture was required.
- Existing deployed rendered-page snapshot evidence remains in
  `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now verifies both sides of the website contract:
  pages must stop being hidden/non-final before public release, and they must
  retain the blog-style metadata/author-note shape required by `PLAN.md`.

## Update 2026-07-15: Website Word-Count Gate

Scope:

- Added a site-aware final-publication check that each kUPS page body has
  3,500-10,000 words, matching the PLAN article-length requirement.
- Updated `tests/test_release_readiness.py` so clean final-state fixtures
  include long enough page bodies, and added a regression test that shortens
  one page and confirms the release gate reports the word-count violation.
- Expanded the hidden Post 09 page at website commit `9b79ab3` with
  claim-narrowing guidance so all twelve current hidden pages satisfy the same
  repository-side word counter.

Commands:

- Website validation before deploy:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check` in
  `../sungsoo-ahn.github.io`.
- Website deploy run `29412243173`.
- Website snapshot workflow: first attempt `29412398778` failed during
  Playwright WebKit download before capture; rerun `29412462655` passed.
- Tutorial validation:
  `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`,
  `uv run pytest tests/test_release_readiness.py -q`,
  `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 140`,
  and `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 100`.

Code and reproducibility review:

- The word counter strips fenced code blocks, inline code, and HTML tags before
  counting body tokens.
- Current hidden page word counts checked from `../sungsoo-ahn.github.io/_pages`
  are all inside the PLAN range:
  Post 01 `3632`, Post 02 `3538`, Post 03 `3941`, Post 04 `3739`, Post 05
  `4216`, Post 06 `3916`, Post 07 `3910`, Post 08 `3948`, Post 09 `3636`,
  Post 10 `4036`, Post 11 `4040`, and Post 12 `3599`.
- The site-aware readiness audit reports hidden/non-final page state and
  hidden-draft notes, but no word-count violations.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no new figure snapshot
  capture was required.
- Post 09 website prose changed, so deployed desktop/mobile page snapshots were
  required and are recorded in `reviews/post-09.md` and
  `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone and Post 09 hidden-page
  prose refresh.
- The final-publication gate now enforces article length in addition to
  artifact surface, blog-style metadata, hidden/non-final state, and unresolved
  final-release blockers.

## Update 2026-07-15: Website Citation Backlink Gate

Scope:

- Added a site-aware final-publication check for the PLAN citation contract:
  every kUPS page must have a `## References` section, text citation
  `cite-*` anchors, `ref-*` reference anchors, links from citations to matching
  references, and reverse backlinks from references to each citation anchor.
- The gate supports both citation forms already used in the site sources:
  Markdown links after `<span id="cite-*"></span>` and inline
  `<a href="#ref-*" id="cite-*">...</a>` citations.
- Added release-readiness tests for missing reference anchors and missing
  reverse backlinks.
- Repaired Posts 01-04 in website commit `d244d57` so the current hidden pages
  satisfy the same citation/backlink contract as Posts 05-12.

Commands:

- Website validation before deploy:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check` in
  `../sungsoo-ahn.github.io`.
- Website deploy run `29413487745`.
- Website snapshot workflow `29413685814`.
- Tutorial validation:
  `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`,
  `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q`,
  `uv run kups-tutorial verify-reviews`,
  `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 140`,
  and `git diff --check`.

Code and reproducibility review:

- The citation audit is scoped to site-aware readiness checks, so repository
  artifact checks remain available with `--skip-site`.
- Current hidden pages now pass the citation/backlink portion of the
  site-aware audit. The audit still reports intended hidden/non-final states
  and unresolved production diagnostics.
- Existing repeated citations that use suffixes such as `cite-frenkel2001b`
  are accepted when they link to the base `ref-frenkel2001` entry and the
  reference entry links back to each concrete citation anchor.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot
  capture was required.
- Posts 01-04 website prose changed, so deployed desktop/mobile page snapshots
  were required and are recorded in `reviews/post-01.md` through
  `reviews/post-04.md` and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone and Posts 01-04 hidden
  citation refresh.
- The final-publication gate now enforces artifact surface, blog-style
  metadata, article length, citation backlink integrity, hidden/non-final
  state, and unresolved final-release blockers.

## Update 2026-07-15: Website Figure Include Gate

Scope:

- Added a site-aware final-publication check for the PLAN figure-embed
  contract: each kUPS page must include at least one `{% include
  figure.liquid ... %}` figure, the figure path must live under
  `assets/img/blog/`, the referenced asset must exist in the website repo, the
  include must use `class="img-fluid rounded z-depth-1"`, `zoomable=true`, and
  a caption.
- The caption gate rejects dollar-delimited math and requires at least two
  sentences, matching the PLAN expectation that captions state both what the
  figure shows and the interpretation or mechanism it supports.
- Updated the clean final-state site fixture in
  `tests/test_release_readiness.py` to include a real blog figure asset and a
  valid figure include.
- Added a regression test that breaks the figure path, class, zoomable flag,
  and caption requirements and confirms each violation is reported.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 140`
- Pending final validation for this commit: full CLI test subset,
  review-audit, whitespace check, push, and CI.

Code and reproducibility review:

- The figure audit is scoped to site-aware release readiness; repository-only
  checks with `--skip-site` remain focused on configs, results, notebooks,
  figure files, snapshots, and review blockers.
- Current hidden website pages satisfy the figure-include gate. The
  site-aware audit reports intended hidden/non-final page state and production
  blockers, but no missing or malformed figure include violations.
- Asset existence is checked against the website repository root inferred from
  the page path, so stale `assets/img/blog/...` references become final-release
  blockers.

Figure and rendered-page review:

- No figure assets, figure-generation code, figure captions, website pages, or
  website assets changed in this pass.
- Because this milestone only adds a verifier and synthetic test fixtures, no
  new figure snapshot capture or rendered page snapshot capture was required.
- Existing figure and page snapshot evidence remains in the per-post review
  files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now enforces artifact surface, blog-style
  metadata, article length, citation backlink integrity, figure include
  integrity, hidden/non-final state, and unresolved final-release blockers.

## Update 2026-07-15: Website Footnote Hygiene Gate

Scope:

- Added a site-aware final-publication check for the PLAN footnote contract:
  Markdown footnote IDs must be short single words without hyphens, every
  in-text footnote reference must have a matching definition, and every
  definition must be referenced.
- The gate ignores citation-reference backlinks such as
  `class="reversefootnote"` because those are citation backlinks, not Markdown
  footnotes.
- Added a regression test that creates a hyphenated footnote ID, a missing
  footnote definition, and an unused footnote definition and confirms each
  violation is reported.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 160`
- Pending final validation for this commit: full CLI test subset,
  review-audit, website validators, whitespace checks, push, and CI.

Code and reproducibility review:

- Current hidden website pages do not use Markdown footnotes, so the gate is a
  future-proof style guard rather than a page prose change.
- The site-aware readiness audit reports intended hidden/non-final page state
  and production blockers, but no footnote hygiene violations.
- Footnote definition lines are stripped before collecting in-text references,
  so definitions are not incorrectly counted as usages.

Figure and rendered-page review:

- No figure assets, figure-generation code, figure captions, website pages, or
  website assets changed in this pass.
- Because this milestone only adds a verifier and synthetic test fixture, no
  new figure snapshot capture or rendered page snapshot capture was required.
- Existing figure and page snapshot evidence remains in the per-post review
  files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now enforces artifact surface, blog-style
  metadata, article length, citation backlink integrity, figure include
  integrity, footnote hygiene, hidden/non-final state, and unresolved
  final-release blockers.

## Update 2026-07-15: Result Manifest Provenance Gate

Scope:

- Added a repository-side final-publication check for result manifest
  provenance. Every smoke/full `manifest.json` must be a JSON object with a
  matching `config.post`, matching `config.profile`, a `provenance` object, and
  a `versions` object.
- The provenance object must record `config_path`, 64-character
  `config_sha256`, `lock_path`, 64-character `lock_sha256`, non-unknown
  `git_revision`, `python_version`, `platform`, `runtime_device`, and a
  `precision_policy` that includes `jax_enable_x64=`.
- The versions object must record at least `kups` and `numpy`.
- Added a regression test that corrupts `config.post`, `git_revision`,
  `config_sha256`, and the `kups` version and confirms each violation is
  reported.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 160`
- Pending final validation for this commit: full CLI test subset,
  review-audit, website validators, whitespace checks, push, and CI.

Code and reproducibility review:

- Current committed smoke/full manifests satisfy the new provenance schema.
  The `--skip-site` readiness audit reports the expected final-release
  blockers only, with no manifest-provenance violations.
- The gate does not require every deterministic post to invent a seed. Post 02
  is a deterministic harmonic-oscillator integrator diagnostic and its
  manifest has no random seed by design; seeded posts still preserve their
  configured seeds in the committed config object and compact summaries.
- The check complements the existing JSON-syntax and artifact-surface gates by
  verifying that committed manifests are useful for source-control,
  dependency, runtime-device, and precision provenance.

Figure and rendered-page review:

- No figure assets, figure-generation code, website pages, or website assets
  changed in this pass.
- Because this milestone only adds a repository-side verifier and synthetic
  test fixtures, no new figure snapshot capture or rendered page snapshot
  capture was required.
- Existing figure and page snapshot evidence remains in the per-post review
  files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now enforces artifact surface, manifest
  provenance, blog-style metadata, article length, citation backlink integrity,
  figure include integrity, footnote hygiene, hidden/non-final state, and
  unresolved final-release blockers.

## Update 2026-07-15: Smoke-Before-Full Run Guard

Scope:

- Added the PLAN execution rule that full-profile runs require existing
  verified smoke outputs first.
- `run_post(..., profile="full")` now calls `verify_post(post, "smoke", ...)`
  before generating full outputs. Because `run-all --profile full` delegates to
  `run_post`, the guard covers both single-post and all-post full workflows.
- Added tests for the failure path when smoke outputs are absent and for a
  successful Post 02 full run after smoke generation and verification.

Commands:

- `uv run ruff check src/kups_md_tutorials/workflows.py tests/test_cli.py`
- `uv run pytest tests/test_cli.py -q`
- `uv run kups-tutorial run 02 --profile full --output-dir /tmp/kups-full-guard-no-smoke`
  failed intentionally with missing smoke summary, manifest, and samples.
- Pending final validation for this commit: full local validation set, push,
  and CI.

Code and reproducibility review:

- The guard is placed at the workflow boundary rather than individual post
  writers, so all current and future full-profile post runners inherit the
  same smoke-first behavior.
- The guard uses the existing per-post smoke verification checks, not just file
  existence, so malformed smoke summaries still block a full run.
- The positive test uses Post 02 because it is deterministic and cheap while
  still exercising the full run path.

Figure and rendered-page review:

- No figure assets, figure-generation code, website pages, or website assets
  changed in this pass.
- Because this milestone only changes workflow control flow and tests, no new
  figure snapshot capture or rendered page snapshot capture was required.

Review decision:

- Accepted for the workflow tooling milestone.
- Full-profile execution now enforces the smoke-before-full checkpoint from
  PLAN.md.

## Update 2026-07-15: Figure Source Provenance Gate

Scope:

- Added a repository-side final-publication check for the PLAN requirement to
  record figure source URL, license or ownership status, and modifications
  outside the rendered post body.
- Added `reviews/figure-sources.json` as the current provenance ledger for all
  committed SVG/PNG tutorial figures. The current figures are custom-generated
  from committed compact outputs and generation scripts, not copied from
  external figure sources.
- The release gate now requires every committed figure under
  `figures/post-*/*.svg` and `figures/post-*/*.png` to be covered by a ledger
  entry with `source_url`, `source_type`, `license`, `modifications`,
  `generator`, and existing `source_data` paths.
- Added a regression test that removes one Post 08 figure from the ledger and
  clears its license field, then confirms both violations are reported.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 180`
- Pending final validation for this commit: full local validation set, push,
  and CI.

Code and reproducibility review:

- The ledger check runs before the generic artifact-surface check so missing
  or incomplete source records are reported even when the figure files exist.
- Current committed figures satisfy the new provenance gate; the
  `--skip-site` readiness audit reports only the known hidden/public-release
  and production-diagnostic blockers, with no figure-source violations.
- The check resolves ledger paths relative to the repository root implied by
  the review directory, which keeps isolated tests and the real checkout
  consistent.

Figure and rendered-page review:

- No figure assets, figure-generation code, website pages, or website assets
  changed in this pass.
- Because this milestone only adds a provenance ledger, verifier, and
  synthetic test fixture, no new figure snapshot capture or rendered page
  snapshot capture was required.
- Existing figure and page snapshot evidence remains in the per-post review
  files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- The final-publication gate now enforces artifact surface, figure source
  provenance, manifest provenance, blog-style metadata, article length,
  citation backlink integrity, figure include integrity, footnote hygiene,
  hidden/non-final state, and unresolved final-release blockers.

## Update 2026-07-15: Website Export Manifest Gate

Scope:

- Added a site-aware final-publication check that the website repo contains a
  full-profile `assets/json/kups-md-tutorials/manifest.json` export manifest.
- The gate now verifies that every exported manifest file entry is a JSON
  object with a supported post, supported kind, source, destination,
  64-character SHA-256 digest, an existing destination under the website repo,
  and a digest that matches the current website file contents.
- The gate requires both figure and compact-result entries for all twelve
  posts so a stale single-post export cannot pass final readiness.
- Updated `export-site` to write portable paths relative to the tutorial
  artifact root and website root instead of embedding local absolute paths.
- Added tests for portable export paths and stale website manifests with a
  hash mismatch and missing Post 08 figure coverage.

Commands:

- `uv run ruff check src/kups_md_tutorials/site_export.py src/kups_md_tutorials/release_readiness.py tests/test_site_export.py tests/test_release_readiness.py`
- `uv run pytest tests/test_site_export.py tests/test_release_readiness.py -q`
- `uv run pytest tests/test_site_export.py tests/test_release_readiness.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 160`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 220`
- `uv run kups-tutorial export-site --profile full`
- Website validation after export:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check` in
  `../sungsoo-ahn.github.io`.
- Pending final validation for this commit: push and CI for both repositories.

Code and reproducibility review:

- The current pre-export website manifest was stale and covered only Post 09.
  The new gate caught that state, reporting missing exported figure and
  compact-result entries for Posts 01-08 and 10-12.
- After `uv run kups-tutorial export-site --profile full`, the website
  manifest records source revision `8e902dd`, profile `full`, 71 exported
  files, all twelve posts, and no absolute source or destination paths.
- Site-aware release readiness after export no longer reports export-manifest
  coverage or SHA-256 problems; it reports only the intended hidden/non-final
  page state and production GPU/publication blockers.
- Destination paths are resolved against the website root and rejected if they
  escape it, which prevents a manifest from passing with unrelated local files.
- Source paths are required as manifest metadata but are not resolved by the
  site-aware gate because the published website only needs to prove that its
  committed/exported destination files match their recorded hashes.

Figure and rendered-page review:

- No figure-generation code or website page markup changed in this tutorial
  commit.
- The follow-up website export changed only
  `assets/json/kups-md-tutorials/manifest.json`; all copied figure and compact
  result payloads were already byte-identical in the website repo.
- No rendered page snapshot capture was required because no website page
  markup, rendered figure bytes, CSS-sensitive content, or linked figure asset
  changed. The hidden pages do not render the JSON export manifest.

Review decision:

- Accepted for the release-readiness tooling milestone after focused tests.
- The final-publication gate now enforces artifact surface, figure source
  provenance, website export-manifest synchronization, manifest provenance,
  blog-style metadata, article length, citation backlink integrity, figure
  include integrity, footnote hygiene, hidden/non-final state, and unresolved
  final-release blockers.

## Update 2026-07-15: Notebook Execution Ledger Gate

Scope:

- Added a repository-side final-publication check for clean-kernel notebook
  execution evidence.
- Added `reviews/notebook-execution.json`, a machine-checkable ledger for all
  twelve notebooks with source paths, source SHA-256 digests, code-cell counts,
  executed-cell counts, output counts, kernel, timeout, and source revision.
- The release gate now fails if a notebook is missing from the ledger, if a
  ledger source path is stale, if a notebook source hash no longer matches, if
  the recorded code-cell count disagrees with the current notebook JSON, if
  not all code cells executed, or if a notebook recorded no outputs.
- Added a regression test that removes the Post 08 ledger entry, corrupts one
  source hash, and marks another notebook partially executed.

Commands:

- `uv run kups-tutorial verify-notebooks --output-dir /tmp/kups-notebook-runs`
- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py tests/test_notebook_execution.py -q`
- `uv run pytest tests/test_release_readiness.py tests/test_notebook_execution.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 180`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 220`
- `git diff --check`
- Pending validation for this commit: push and CI.

Code and reproducibility review:

- The clean notebook execution command passed and wrote
  `/tmp/kups-notebook-runs/manifest.json`.
- The committed `reviews/notebook-execution.json` was derived from that
  manifest and records current notebook source hashes for Posts 01-12.
- The gate checks the current notebook files directly, so editing a notebook
  without rerunning `verify-notebooks` and updating the ledger becomes a
  final-release blocker.

Figure and rendered-page review:

- No notebook source, figure asset, figure-generation code, website page, CSS
  sensitive markup, website manifest, or linked figure changed in this pass.
- Because this milestone only adds notebook execution evidence and verifier
  coverage, no new figure snapshot capture or rendered page snapshot capture
  was required.

Review decision:

- Accepted for the release-readiness tooling milestone after the clean
  notebook run.
- The final-publication gate now enforces artifact surface, notebook execution
  ledger freshness, figure source provenance, website export-manifest
  synchronization, manifest provenance, blog-style metadata, article length,
  citation backlink integrity, figure include integrity, footnote hygiene,
  hidden/non-final state, and unresolved final-release blockers.

## Update 2026-07-15: Oversized Tracked Artifact Gate

Scope:

- Added a tracked-file size guard to `verify-artifacts`, matching the PLAN
  requirement to confirm that no trajectories, model archives, caches, or
  oversized generated files are tracked.
- The audit now rejects any tracked file larger than 5 MiB while keeping the
  current compact committed summaries, notebooks, figures, and snapshots
  valid. The largest current tracked file is
  `results/post-11/full/enhanced_sampling_curves.csv` at about 1.8 MiB.
- Added tests for an oversized compact-result-like file and a small compact
  file below the limit.

Commands:

- `uv run ruff check src/kups_md_tutorials/artifact_audit.py tests/test_artifact_audit.py`
- `uv run pytest tests/test_artifact_audit.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run pytest tests/test_artifact_audit.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 160`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 220`
- `git diff --check`
- Pending validation for this commit: push and CI.

Code and reproducibility review:

- The guard is implemented inside `audit_tracked_artifacts`, so it applies to
  both direct Python calls and the `kups-tutorial verify-artifacts` CLI used by
  CI.
- The size check only inspects files that exist in the audited repository,
  which preserves existing unit tests that use synthetic forbidden path names
  without creating files.

Figure and rendered-page review:

- No configs, results, notebooks, figures, snapshots, website pages, or
  website assets changed in this pass.
- Because this milestone only changes repository hygiene tooling and tests, no
  figure snapshot capture or rendered-page snapshot capture was required.

Review decision:

- Accepted for the artifact-hygiene tooling milestone after focused validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by `verify-release-readiness`.

## Update 2026-07-15: CI Release-Surface Gate

Scope:

- Added `verify_release_surface`, a release-readiness mode that allows the
  current hidden-draft and production-GPU final blockers but still fails on
  structural release-surface regressions.
- Added the CLI flag
  `kups-tutorial verify-release-readiness --allow-current-blockers`.
- Added a CI workflow step:
  `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`.
- Added tests proving the current project blockers are allowed by the surface
  audit and that structural violations, such as a missing figure-source ledger,
  still fail.

Commands:

- `uv run ruff check src/kups_md_tutorials/cli.py src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q`
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py tests/test_artifact_audit.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial verify-release-readiness --skip-site 2>&1 | tail -n 160`
- `uv run kups-tutorial verify-release-readiness 2>&1 | tail -n 220`
- `git diff --check`
- Pending validation for this commit: push and CI.

Code and reproducibility review:

- The original `verify-release-readiness` behavior is unchanged: it remains the
  strict final-publication gate and still fails while final blockers remain.
- The new `--allow-current-blockers` mode exists so CI can enforce artifact,
  manifest, notebook, figure-source, and review-surface regressions before the
  final GPU/public-indexing pass.
- The CI step uses `--skip-site` because the website repository is not checked
  out in the tutorial workflow. Site-aware readiness remains validated locally
  and by website-side validation when website files change.

Figure and rendered-page review:

- No configs, results, notebooks, figures, snapshots, website pages, or
  website assets changed in this pass.
- Because this milestone only changes release-readiness tooling, tests, and CI
  configuration, no figure snapshot capture or rendered-page snapshot capture
  was required.

Review decision:

- Accepted for the CI/release-surface tooling milestone after focused
  validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Typed Config Loader Gate

Scope:

- Added typed loader validation to the release-readiness artifact surface for
  every committed `configs/post-XX/{smoke,full}.json` file.
- The audit now calls the post-specific loader for all 12 posts, so syntax-only
  JSON files or schema-invalid edits fail before final release or CI surface
  checks can pass.
- Updated release-readiness test fixtures to copy the real committed tutorial
  configs into temporary release fixtures instead of using placeholder
  `{post, profile}` JSON.
- Added a regression test that corrupts post 02's full-profile
  `integrator_experiment.num_steps` and verifies the release audit reports a
  typed config validation failure.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py tests/test_config.py -q`
  passed: 33 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_config.py tests/test_cli.py -q`
  passed: 47 tests, with the existing ASE/NumPy deprecation warnings from CLI
  tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-artifacts` passed for 279 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --skip-site` failed only on
  the existing final-release blockers for hidden pages and production GPU /
  public-indexing work.
- `git diff --check` passed.

Code and reproducibility review:

- The loader mapping covers posts 01-12 and uses the same public loader
  functions already used by runners and config tests.
- The check runs after the required config file existence/JSON check and skips
  only missing config files so the original missing-file violation remains the
  primary failure.
- The synthetic clean-release fixture now uses real config schemas, preserving
  coverage for post-specific required fields such as post 12's model artifact
  metadata.
- The placeholder model-artifact test now mutates copied post 12 configs in
  place, so it continues to exercise the final-release placeholder marker gate
  without bypassing typed MLIP config validation.

Figure and rendered-page review:

- No tutorial config values, results, notebooks, figures, snapshots, website
  pages, website assets, or prose claims changed in this milestone.
- Because this was a release-tooling and test-fixture change only, no figure
  snapshot capture or rendered desktop/mobile page snapshot capture was
  required.

Review decision:

- Accepted for the typed-config release-surface milestone after focused and
  release-surface validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: kUPS Series Index Gate

Scope:

- Added a site-aware release-readiness check for the direct-link series index
  page at `../sungsoo-ahn.github.io/_pages/kups-md-tutorials.md`.
- The gate now requires the index to use the blog-native page layout,
  `/kups-md-tutorials/` permalink, description metadata, disabled pagination,
  `publications blog-index` wrapper, series-ordered `site.pages` Liquid query,
  bibliography list, post title/description blocks, post-type badge, read-time
  metadata, and `part {{ post.series_order }} of {{ tutorial_count }}` series
  metadata.
- The current `nav: false` state for the index is treated as a final-publication
  blocker, like the hidden tutorial posts, so hidden direct-link pages remain
  allowed only in the release-surface audit mode.
- Updated the synthetic website fixture to include a blog-style kUPS index and
  added a regression test for index layout/query/metadata violations.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 21 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  35 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-artifacts` passed for 279 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers plus the intended hidden
  `kups-md-tutorials.md` index blocker.

Code and reproducibility review:

- The new index check is site-aware only and does not affect skip-site CI
  contexts where the website checkout is unavailable.
- The check validates the source Liquid structure that renders the direct-link
  index page, so future edits cannot silently replace the blog-style listing
  with a standalone tutorial-roadmap page.
- The violation string for `nav: false` intentionally reuses the current
  hidden-page blocker marker, which keeps `--allow-current-blockers` focused on
  structural regressions while the series remains intentionally unpublished.

Figure and rendered-page review:

- No website page source, front matter, prose, linked figures, CSS-sensitive
  markup, assets, figures, configs, results, notebooks, or snapshots changed in
  this milestone.
- The actual deployed direct-link index page was already inspected in the
  previous continuation and remains unchanged; this pass only adds verifier
  coverage and test fixtures, so no new rendered desktop/mobile snapshot
  capture was required.

Review decision:

- Accepted for the kUPS series-index release-surface milestone after focused,
  site-aware, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Rendered Page Snapshot Ledger Gate

Scope:

- Added a repository-side release-readiness check for
  `reviews/page-snapshots.md`.
- The gate now requires rendered page snapshot evidence to include the website
  workflow, `kups-md-page-snapshots` artifact name, reviewed manifest,
  manifest coverage, inspected snapshot list, feedback, and revision decisions.
- The gate requires desktop and mobile rendered snapshot references for the
  direct-link series index (`post-index`) and for all twelve hidden tutorial
  posts (`post-01` through `post-12`).
- Updated the synthetic release-readiness fixture to include a page snapshot
  ledger and added a regression test for missing artifact, index-mobile, and
  post-12 desktop evidence.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 22 tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run pytest tests/test_release_readiness.py tests/test_review_audit.py tests/test_cli.py -q`
  passed: 39 tests, with the existing ASE/NumPy deprecation warnings from CLI
  tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-artifacts` passed for 279 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The new check is independent of browser availability and validates committed
  review evidence from the CI/browser snapshot workflow.
- The check covers the user-facing direct-link index as well as all twelve post
  pages, so a missing or stale desktop/mobile snapshot reference becomes a
  release-readiness violation before public publication.
- The current ledger already records the required index and post snapshot
  evidence, so `--allow-current-blockers` remains green while strict readiness
  continues to fail on the intended hidden/final-production blockers.

Figure and rendered-page review:

- No website page source, front matter, prose, linked figures, CSS-sensitive
  markup, assets, figures, configs, results, notebooks, or snapshot images
  changed in this milestone.
- Because this pass only adds verifier coverage for existing rendered-page
  snapshot evidence, no new desktop/mobile page capture was required.

Review decision:

- Accepted for the rendered-page snapshot-ledger milestone after focused,
  site-aware, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Website Source-Link Gate

Scope:

- Added a site-aware release-readiness check that every hidden kUPS post links
  back to the executable source artifacts required by PLAN.md.
- For each post, the gate now requires links or URL fragments for the smoke
  config, full config, notebook, smoke results, full results, full provenance
  manifest, and self-review note.
- Updated the synthetic website fixture with the same source-link block and
  added a regression test that removes Post 02 source links and verifies the
  release audit reports the missing coverage.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 23 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  37 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-artifacts` passed for 279 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The new check mirrors the existing website-side `validate_kups_pages.py`
  source-link requirement, bringing the same invariant into the repository-side
  final-publication gate.
- The gate is site-aware only, so CI contexts without the website checkout can
  continue using `--skip-site` while local final-readiness checks verify the
  full cross-repository link surface.
- The current hidden website pages already satisfy the new source-link gate.

Figure and rendered-page review:

- No website page source, front matter, prose, linked figures, CSS-sensitive
  markup, assets, figures, configs, results, notebooks, or snapshot images
  changed in this milestone.
- Because this pass only adds verifier coverage and synthetic fixture links,
  no new figure snapshot or rendered desktop/mobile page capture was required.

Review decision:

- Accepted for the website source-link release-surface milestone after focused,
  site-aware, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Website Build Evidence Gate

Scope:

- Added a repository-side release-readiness check for
  `reviews/website-build.json`.
- The gate records the latest successful `Deploy site` workflow run for
  `sungsoo-ahn/sungsoo-ahn.github.io` and requires a completed successful run,
  a GitHub Actions run URL, a 40-character website `head_sha`, validator/build
  step names, and the exact website validation commands from the deploy
  workflow.
- When `--site-root` is provided, the gate checks the ledger `head_sha` against
  the website checkout HEAD and confirms the deploy workflow contains
  `python3 scripts/validate_blog.py`,
  `python3 scripts/validate_kups_pages.py`, and
  `bundle exec jekyll build`.
- Added a regression test that fails the ledger conclusion, removes the Jekyll
  build command from the ledger, and removes the hidden-kUPS validator from the
  workflow fixture.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 24 tests.
- `python3 scripts/validate_blog.py` passed in the website checkout with only
  pre-existing unused-image warnings.
- `python3 scripts/validate_kups_pages.py` passed in the website checkout.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  38 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 279 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The current website ledger points to successful workflow run `29416965348`
  for website commit `a98e133c2576ef0e953fa04f202b8daf196de457`.
- The GitHub Actions run completed both `build` and `deploy` jobs successfully;
  the `build` job included `Validate blog posts`, `Validate hidden kUPS pages`,
  `Build site`, and artifact upload before the Pages deploy job.
- This check complements rendered snapshot evidence by proving that the current
  exported hidden pages passed the website validators and production Jekyll
  build before deploy.

Figure and rendered-page review:

- No website page source, front matter, prose, linked figures, CSS-sensitive
  markup, assets, figures, configs, results, notebooks, or snapshot images
  changed in this milestone.
- Because this pass only adds build/deploy evidence validation and a review
  ledger, no new figure snapshot or rendered desktop/mobile page capture was
  required.

Review decision:

- Accepted for the website build-evidence release-surface milestone after
  focused, site-aware, website-validator, artifact, review, and strict-readiness
  validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: CI Workflow Contract Gate

Scope:

- Added a repository-side release-readiness check for
  `.github/workflows/verify.yml`.
- The gate now requires the CI workflow to keep the PLAN verification surface:
  locked dependency installation, Ruff, Pytest, smoke reproduction, smoke
  verification, committed full-output verification, tracked-artifact audit,
  review audit, release-surface audit with current blockers allowed, notebook
  execution from clean kernels, and `git diff --check`.
- Updated the synthetic release-readiness fixture with a minimal CI workflow
  and added a regression test that removes smoke reproduction, the
  current-blocker release-surface audit, and notebook execution.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 25 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  39 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The new check derives the workflow path from the review-root fixture, so
  isolated release-readiness tests audit their own synthetic `.github`
  workflow instead of accidentally reading the current checkout.
- The current workflow already contains the required commands; this milestone
  makes that contract explicit in the final-publication gate.
- The gate protects the smoke-before-full and notebook-execution requirements
  from future CI drift without making hidden drafts public.

Figure and rendered-page review:

- No code that generates tutorial figures, no figure assets, no website page
  source, no CSS-sensitive markup, and no website assets changed in this
  milestone.
- Because this pass only adds CI workflow contract validation and a synthetic
  test fixture, no new figure snapshot or rendered desktop/mobile page capture
  was required.

Review decision:

- Accepted for the CI workflow-contract release-surface milestone after
  focused, site-aware, artifact, review, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Gitignore Artifact Policy Gate

Scope:

- Expanded `.gitignore` so the repository ignores the raw trajectories, model
  archives, cache directories, and bulky generated arrays that the artifact
  audit forbids from being tracked.
- Added a repository-side release-readiness check for `.gitignore` so final
  publication now requires ignore coverage for Python caches, virtual
  environments, raw simulation directories, notebook execution outputs,
  downloaded model caches, HDF5 trajectories, trajectory files, NumPy arrays,
  pickle files, checkpoint files, model files, and PyTorch model archives.
- Updated the synthetic release-readiness fixture with the ignore policy and
  added a regression test that removes representative cache, HDF5, and model
  archive patterns.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 26 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_artifact_audit.py tests/test_cli.py -q`
  passed: 45 tests, with the existing ASE/NumPy deprecation warnings from CLI
  tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The existing `verify-artifacts` command still audits tracked files directly;
  this milestone adds the complementary preventative policy so raw outputs and
  model archives are ignored before they are accidentally added.
- The release-readiness check derives `.gitignore` from the review-root fixture,
  so isolated tests audit their own synthetic repository hygiene policy.
- The actual checkout now ignores the suffixes and directories already treated
  as forbidden by the tracked-artifact audit.

Figure and rendered-page review:

- No simulation code, configs, numerical outputs, notebooks, figures, website
  pages, website assets, or CSS-sensitive markup changed in this milestone.
- Because this pass only changes repository hygiene policy and verifier tests,
  no new figure snapshot or rendered desktop/mobile page capture was required.

Review decision:

- Accepted for the gitignore artifact-policy release-surface milestone after
  focused, site-aware, artifact, review, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Pyproject Dependency Contract Gate

Scope:

- Added a repository-side release-readiness check for `pyproject.toml`.
- The gate now enforces the PLAN packaging contract: Python is pinned to
  `>=3.13,<3.14`, the core kUPS dependency is pinned to `kups==1.0.3`, CUDA
  development is exposed through `gpu = ["kups[cuda]==1.0.3"]`, Hugging Face
  model-download support is exposed through `mlff = ["kups[hf]==1.0.3"]`, the
  `kups-tutorial` console script points to `kups_md_tutorials.cli:main`, and
  Ruff targets `py313`.
- Updated the synthetic release-readiness fixture with a minimal pyproject
  contract and added a regression test that weakens the Python pin, kUPS pin,
  CUDA extra, and Ruff target.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 27 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  41 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The new check uses Python's standard TOML parser and validates packaging
  metadata directly instead of relying on comments or README instructions.
- The current checkout already satisfies the dependency contract; this
  milestone makes the contract part of the final-publication release gate.
- The check protects reproducibility assumptions that all posts share: the same
  Python minor version, the same kUPS release, and explicit optional extras for
  GPU execution and model-artifact download.

Figure and rendered-page review:

- No simulation code, configs, numerical outputs, notebooks, figures, website
  pages, website assets, or CSS-sensitive markup changed in this milestone.
- Because this pass only changes dependency-contract validation and synthetic
  test metadata, no new figure snapshot or rendered desktop/mobile page capture
  was required.

Review decision:

- Accepted for the pyproject dependency-contract release-surface milestone
  after focused, site-aware, artifact, review, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Manifest File-Hash Integrity Gate

Scope:

- Expanded the result-manifest release-readiness check so recorded
  `config_path`, `config_sha256`, `lock_path`, and `lock_sha256` must match the
  current committed config file and `uv.lock`, not only be present and
  hex-shaped.
- The gate now rejects absolute or escaping provenance paths, stale config
  hashes, stale lock hashes, and manifests that point to the wrong config or
  lock file.
- Updated the synthetic release-readiness fixture so every result manifest uses
  real fixture config and lock hashes, including the Post 12 smoke/full
  manifests rewritten after model-artifact metadata mutation.
- Added a regression test where valid-looking config and lock SHA strings are
  stale and must be reported as mismatches.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 28 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  42 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- A preflight script checked all 24 committed result manifests before this
  change; all current `config_sha256` and `lock_sha256` values matched the
  corresponding committed config files and `uv.lock`.
- The new check directly supports the PLAN requirement to record configuration
  and lock hashes for reproducibility.
- This milestone found and fixed a synthetic-fixture issue where the Post 12
  smoke config was mutated after its manifest was written.

Figure and rendered-page review:

- No simulation code, configs, numerical outputs, notebooks, figures, website
  pages, website assets, or CSS-sensitive markup changed in this milestone.
- Because this pass only changes manifest validation and synthetic test
  metadata, no new figure snapshot or rendered desktop/mobile page capture was
  required.

Review decision:

- Accepted for the manifest file-hash integrity release-surface milestone after
  focused, site-aware, artifact, review, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Figure Generator Provenance Gate

Scope:

- Expanded the figure-source release-readiness check so each
  `reviews/figure-sources.json` entry must point to an existing
  repository-relative generator script.
- The gate now rejects absolute or escaping generator paths, missing generator
  files, and `source_url` values that do not match the expected
  `internal:<generator>` form for repository-owned generated figures.
- Updated the synthetic release-readiness fixture to create per-post synthetic
  figure generator scripts and extended the stale figure-source regression to
  break Post 08's generator path and internal source URL.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 28 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  42 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --skip-site --allow-current-blockers`
  passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the existing final-release blockers for hidden pages,
  hidden-draft notes, production GPU diagnostics, and public indexing.

Code and reproducibility review:

- The previous figure-source gate proved that image files and source data
  existed, but it did not prove that the named script capable of regenerating
  the figure was committed.
- The current checkout already has `scripts/generate_post01_figures.py` through
  `scripts/generate_post12_figures.py`, and the ledger points to those files.
- This check directly supports the PLAN requirement to commit figure sources
  and keep final figures reproducible from committed compact outputs.

Figure and rendered-page review:

- No figure-generation code, figure assets, numerical outputs, notebooks,
  website pages, website assets, or CSS-sensitive markup changed in this
  milestone.
- Because this pass only changes provenance validation and synthetic test
  fixtures, no new figure snapshot or rendered desktop/mobile page capture was
  required.

Review decision:

- Accepted for the figure-generator provenance release-surface milestone after
  focused, site-aware, artifact, review, and strict-readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Figure Source Data Coverage Gate

Scope:

- Expanded the figure-source release-readiness check so each
  `reviews/figure-sources.json` entry must cite both
  `configs/post-XX/smoke.json` and `configs/post-XX/full.json`.
- The same gate now requires at least one committed compact
  `results/post-XX/{smoke,full}/*_summary.json` source for each profile, so a
  figure cannot pass provenance review by citing only a full-profile result or
  an unrelated existing file.
- Updated the synthetic release-readiness fixture and stale Post 08 regression
  so missing full config and smoke-summary coverage are reported explicitly.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 28 tests.
- `uv run pytest tests/test_release_readiness.py tests/test_cli.py -q` passed:
  42 tests, with the existing ASE/NumPy deprecation warnings from CLI tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.
- `git diff --check` passed.
- `uv run kups-tutorial verify-artifacts` passed for 280 tracked files.
- `uv run kups-tutorial verify-reviews` passed for 12 posts after this ledger
  entry and the hidden-index snapshot note were added.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts after updating `reviews/website-build.json` to website
  deploy run `29424070898` and site commit `4d7bfe9`.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on existing final-release blockers: hidden pages and hidden-draft
  notes, production GPU diagnostics, and public-indexing/snapshot refresh work.
- `bundle exec jekyll build` was skipped because `bundle` is not installed on
  this host.
- `docker compose -f docker-compose-slim.yml up` was skipped because the
  current user cannot access `/var/run/docker.sock`.

Code and reproducibility review:

- The real `reviews/figure-sources.json` ledger already cites smoke and full
  configs plus smoke and full compact summaries for all twelve posts.
- The new gate makes that expectation executable and protects the PLAN rule
  that final figures must be traceable to committed compact outputs, not only
  to rendered image files.
- The check is intentionally profile-aware but summary-name agnostic, because
  different posts use different compact summary filenames.

Figure and rendered-page review:

- No figure-generation code, figure assets, numerical outputs, notebooks, or
  website post bodies changed in this milestone.
- No figure snapshot was required for this validation-only gate.
- The hidden series index was separately aligned with the public blog-list
  style in the website repository and is tracked in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the figure-source data coverage release-surface milestone after
  focused tests, site-aware readiness validation, artifact audit, and review
  audit.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: CI Release Audit Ordering Gate

Scope:

- Tightened the tutorial CI release-readiness contract so
  `.github/workflows/verify.yml` must run checks in the expected review order,
  not merely contain the right commands somewhere in the file.
- The enforced order is locked dependency installation, lint, tests, smoke
  reproduction, smoke verification, committed full-output verification,
  artifact audit, review audit, allowed-blocker release-surface audit, clean
  notebook execution, and whitespace audit.
- Added a regression test that swaps the review audit and release-surface audit
  and verifies the release-readiness checker reports the misordered workflow.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 29 tests.

Code and reproducibility review:

- The previous workflow gate caught missing CI commands but could not detect a
  workflow that performed the release-surface audit before review evidence was
  checked.
- The current gate preserves the intended progression from generated outputs
  and review ledgers into release-surface validation, then notebook execution
  and whitespace checks.
- This directly supports the PLAN requirement that validation and review gates
  stay explicit rather than being hidden under generic CI success.

Figure and rendered-page review:

- No figure-generation code, figure assets, numerical outputs, notebooks,
  website pages, website assets, or CSS-sensitive markup changed in this
  milestone.
- No figure or rendered-page snapshot was required for this validation-only CI
  contract change.

Review decision:

- Accepted for the CI release-audit ordering milestone after focused lint and
  release-readiness regression tests.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Website Figure-Source Link Gate

Scope:

- Expanded the site-aware blog-style release gate so every hidden kUPS post
  must link to its committed figure-generation script:
  `scripts/generate_postXX_figures.py`.
- Added the missing figure-source links to website Posts 02, 03, 04, 08, 09,
  10, 11, and 12.
- Updated the synthetic site fixture and stale source-link regression so a
  missing figure-generation source link is reported explicitly.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 29 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts after the website source-link refresh.
- Website deploy run `29426768593` passed `Validate blog posts`, `Validate
  hidden kUPS pages`, `Build site`, and `Deploy to GitHub Pages`.
- Snapshot workflow run `29427006700` passed for the eight changed hidden
  pages.
- Live cache-busted checks with `?v=eda02e4` confirmed all eight changed pages
  include their `scripts/generate_postXX_figures.py` link.
- Live public `/blog/` check found no `kups-md-tutorials` or
  `post-02-integrators` links.

Code and reproducibility review:

- The previous site-source-link gate enforced configs, notebook, compact
  summaries, full manifest, and self-review links, but did not enforce the
  PLAN requirement to link the figure-generation source from the rendered post.
- The current gate closes that gap and keeps the rendered prose connected to
  the committed scripts already tracked by `reviews/figure-sources.json`.
- `reviews/website-build.json` now records website deploy run `29426768593`
  and site commit `eda02e408bf4d268bbb2f8514b31803db7b21f93`.

Figure and rendered-page review:

- No figure-generation code, figure assets, numerical outputs, notebooks, or
  figure captions changed.
- Because website source-link lists changed, rendered desktop/mobile snapshots
  were captured through CI and reviewed for Posts 02, 03, 04, 08, 09, 10, 11,
  and 12.
- Snapshot evidence and feedback are recorded in `reviews/page-snapshots.md`
  under "Posts 02-04 And 08-12 Figure-Source Link Refresh".

Review decision:

- Accepted for the website figure-source link milestone after focused tests,
  site-aware readiness validation, website deploy, live hidden/public exposure
  checks, and desktop/mobile page snapshot review.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Website Export Source Hash Gate

Scope:

- Expanded the website export-manifest audit so every exported file must match
  both the website destination hash and the current repository source hash.
- The gate now rejects source paths that escape the repository root, missing
  source files, and source/destination hash drift after export.
- Updated the synthetic website fixture to copy from generated source artifacts
  instead of creating unrelated dummy website files.
- Added a regression test that mutates a source figure after export and
  verifies the release-readiness checker reports a source SHA-256 mismatch.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed: 30 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.

Code and reproducibility review:

- The previous export-manifest gate proved that website destinations existed
  and matched the recorded hash, but it did not prove that the source artifact
  in this repository still matched the exported copy.
- The current gate uses `review_dir.parent` as the audited source root, so
  isolated test fixtures and the real checkout use the same repository-relative
  source-path semantics.
- This protects the PLAN ownership boundary: simulations, compact summaries,
  and figures remain owned by this repository, while the website repository
  carries synchronized copies.

Figure and rendered-page review:

- No figure-generation code, figure assets, numerical outputs, notebooks,
  website pages, website assets, or CSS-sensitive markup changed in this
  milestone.
- No figure or rendered-page snapshot was required because this pass only
  changes release-readiness validation and synthetic test fixtures.

Review decision:

- Accepted for the website export source-hash milestone after focused tests and
  site-aware readiness validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Review Protocol Split Gate

Scope:

- Tightened `verify-reviews` so every post-level self-review must include the
  PLAN-level `## Prose And Style Review` and `## Open Items` sections.
- Added a review-audit gate for the hidden-draft open-item split: blocking
  items for the current hidden draft, non-blocking items accepted until the
  final article pass, and final-release blockers.
- Normalized `reviews/post-01.md` through `reviews/post-08.md` with explicit
  prose/style and open-item sections. Posts 09-12 already used the newer
  section structure.
- Added regression coverage proving that a generic open-items note without the
  hidden-draft split is rejected.

Commands:

- `uv run kups-tutorial verify-reviews` passed for 12 posts.
- `uv run pytest tests/test_review_audit.py -q` passed: 4 tests.
- `uv run ruff check src/kups_md_tutorials/review_audit.py tests/test_review_audit.py`
  passed.

Code and reproducibility review:

- The previous review audit accepted old section aliases and general open-item
  language, which was weaker than the `/goal` protocol in `PLAN.md`.
- The new gate makes the split review status machine-checkable before any post
  can be treated as reviewed, while still preserving historical review entries.
- The synthetic regression runs in a temporary checkout so snapshot references
  are resolved without touching real committed snapshot assets.

Figure and rendered-page review:

- No tutorial configs, results, notebooks, figure-generation code, figure
  assets, website pages, website assets, or CSS-sensitive markup changed.
- No new figure snapshot or rendered desktop/mobile page snapshot was required
  for this validation-only milestone.
- Existing figure and rendered-page snapshot evidence remains in the per-post
  review files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the review-protocol split gate after focused review-audit tests
  and lint.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Fixed-Seed Config Gate

Scope:

- Added an explicit fixed seed to Post 02 smoke/full integrator configs so the
  deterministic integrator diagnostic follows the same seed-provenance
  convention as the rest of the series.
- Extended the typed integrator config and compact summary schema to carry the
  seed.
- Added a release-readiness gate that rejects any smoke/full config without an
  explicit `seed` field anywhere in the JSON tree.
- Regenerated Post 02 smoke/full outputs, the executed notebook, figure
  snapshots, and the website export JSON assets.

Commands:

- `uv run kups-tutorial run 02 --profile smoke` passed.
- `uv run kups-tutorial verify 02 --profile smoke` passed.
- `uv run kups-tutorial run 02 --profile full` passed.
- `uv run kups-tutorial verify 02 --profile full` passed.
- `uv run python scripts/generate_post02_figures.py` passed.
- `uv run jupyter execute notebooks/post-02-integrators.ipynb --inplace`
  passed.
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io`
  passed.
- Website validation and deploy run `29430420195` passed for website commit
  `ed0ba9e608968a349b42e13e57fa36feba724313`.
- Live deployed JSON checks with `?v=ed0ba9e` confirmed the Post 02 full
  manifest and compact summary both record seed `2026071402` and config hash
  `f50d0058bc90342e80be4a9ea6e7b25bbd7defbfe39a5bec72e27056ea46e388`.
- `uv run pytest tests/test_config.py tests/test_release_readiness.py::test_release_readiness_reports_missing_config_seed -q`
  passed: 14 tests.
- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/integrators.py src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.

Code and reproducibility review:

- Before this pass, every post except Post 02 already had at least one
  explicit seed in each smoke/full profile. Post 02 was deterministic but did
  not state that reproducibility convention in machine-readable config.
- The new gate recursively checks each committed profile JSON for `seed`, so a
  future deterministic diagnostic cannot omit fixed-seed provenance silently.
- Post 02 full manifest and exported website manifest now record
  `config.experiment.seed = 2026071402` and the refreshed config hash.
- `reviews/website-build.json` now records the successful website deploy run
  and commit used for the refreshed exported JSON assets.

Figure and rendered-page review:

- Post 02 smoke and full figure snapshots were regenerated and visually
  inspected:
  `snapshots/post-02/integrator_diagnostics_snapshot.png` (`1952 x 576`) and
  `snapshots/post-02/integrator_diagnostics_full_snapshot.png`
  (`1952 x 576`).
- The phase-space, log-energy-error, and forward/backward panels remain
  readable; labels and annotations are not clipped; the figure still supports
  the velocity-Verlet versus explicit-Euler mechanism described in the hidden
  draft.
- No rendered desktop/mobile page snapshot was required because no website
  prose, front matter, figure include, caption, or CSS-sensitive markup
  changed; only exported compact JSON assets changed.

Review decision:

- Accepted for the fixed-seed config gate after focused config, run, figure,
  notebook, export, lint, and regression validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Result Manifest Output File Gate

Scope:

- Tightened `verify-release-readiness` so every result manifest must contain
  at least one `*_file` output reference.
- Added checks that each manifest output path is result-directory relative,
  stays inside the result directory, and points to an existing committed
  compact output.
- Added regression coverage that breaks a summary path and makes a samples
  path escape the result directory.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py::test_release_readiness_reports_manifest_output_file_violations tests/test_release_readiness.py::test_verify_release_readiness_cli_passes_clean_final_state -q`
  passed: 2 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed for 12 posts.

Code and reproducibility review:

- The existing manifest provenance gate verified config hashes, lock hashes,
  runtime, precision, versions, and post/profile identity, but did not prove
  that manifest output-file fields still resolved to current compact outputs.
- The new gate protects the compact-output contract without changing the
  generated manifest schema: existing `summary_file`, `samples_file`,
  `curves_file`, `windows_file`, and post-specific sample fields are audited
  directly.
- Current smoke/full manifests for all twelve posts pass the new output-file
  reference audit.

Figure and rendered-page review:

- No tutorial configs, results, notebooks, figure-generation code, figure
  assets, website pages, website assets, or CSS-sensitive markup changed.
- No new figure snapshot or rendered desktop/mobile page snapshot was required
  for this validation-only milestone.
- Existing figure and rendered-page snapshot evidence remains in the per-post
  review files and `reviews/page-snapshots.md`.

Review decision:

- Accepted for the result-manifest output-file gate after focused lint,
  regression tests, and site-aware release-surface validation.
- Final release still requires the existing production GPU diagnostics and
  public-indexing work reported by strict `verify-release-readiness`.

## Update 2026-07-15: Final Blog Post Location Gate

Scope:

- Tightened the site-aware final-publication gate so the clean final state must
  publish the twelve kUPS articles as `_posts/YYYY-MM-DD-slug.md` blog posts,
  matching `PLAN.md`.
- Hidden direct-link drafts under `_pages` remain accepted current blockers
  until public indexing. The gate now reports the missing final `_posts`
  articles and the hidden index query against `site.pages` as final-release
  blockers instead of treating `_pages` as a clean final publication shape.
- Updated the release-readiness test fixture so hidden drafts use `_pages`,
  final fixtures use `_posts`, and the kUPS index queries `site.posts` in the
  clean final-state case.
- No configs, results, notebooks, figures, snapshots, website pages, website
  assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 32 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed intentionally and now reports that final `_posts` blog posts are
  missing while the hidden `_pages` drafts and direct-link index remain in use.

Code and reproducibility review:

- The release gate now checks `_posts/*-kups-md-post-XX-*.md` first for each
  final article. If a final blog post is missing, it records a final-release
  blocker and falls back to the hidden `_pages/kups-md-post-XX-*.md` draft for
  the existing style, link, reference, figure, and word-count checks.
- The current real website state remains intentional: `_pages` direct links are
  live and hidden from navigation, and `_posts` entries do not exist yet.
- The clean final-state fixture proves that a final publication can pass with
  `_posts` articles and a `site.posts` series query.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone.
- Final release remains blocked on the already recorded production GPU
  diagnostics, public indexing, recaptured rendered snapshots after final
  publication changes, and now the explicit migration from hidden `_pages`
  drafts to final `_posts` blog articles.

## Update 2026-07-15: Final Publication Date Gate

Scope:

- Tightened the site-aware final-publication gate so the twelve final `_posts`
  articles must share one publication date, matching the `PLAN.md` requirement
  for one publication date across the series.
- Added checks that each `_posts` filename date matches its front matter
  `date`, and that `last_updated` is a valid `YYYY-MM-DD` date that does not
  predate publication.
- Scoped the new date invariant to the final `_posts` state. Current hidden
  drafts under `_pages` remain governed by the existing hidden/publication
  blockers.
- No configs, results, notebooks, figures, snapshots, website pages, website
  assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 33 tests.

Code and reproducibility review:

- The previous site style gate only required `date` and `last_updated` fields
  to exist. The new gate validates their format and relationship when all
  final `_posts` articles are present.
- Regression coverage now mutates Post 03 in the clean final-state fixture to
  use a different front matter date, a stale filename date, and a
  `last_updated` value before the publication date. The audit reports all
  three problems.
- The current real website still lacks final `_posts` entries by design, so
  this gate does not add noise to the hidden draft state beyond the already
  accepted final-publication blockers.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint and
  release-readiness regression tests.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to final `_posts`, recapturing rendered snapshots
  after that migration, and passing strict `verify-release-readiness`.

## Update 2026-07-15: Final Blog-Native Front Matter Gate

Scope:

- Tightened the site-aware final-publication gate so final `_posts` articles
  cannot carry page-only front matter from hidden drafts.
- Final `_posts` now reject `permalink`, `nav`, `nav_order`, and `pagination`
  fields, matching the existing blog-post front matter shape in
  `../sungsoo-ahn.github.io/_posts`.
- Hidden `_pages` drafts still require their direct-link `permalink` and may
  keep `nav: false` while the series is intentionally unpublished.
- Updated the clean final-state fixture to omit page-navigation fields from
  synthetic `_posts`, and added regression coverage that reintroduces those
  fields on Post 03.
- No configs, results, notebooks, figures, snapshots, website pages, website
  assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 34 tests.

Code and reproducibility review:

- The checker now passes `final_post=True` only for posts found under `_posts`;
  hidden `_pages` drafts continue to use the existing permalink check.
- The new regression test proves that `permalink`, `nav`, `nav_order`, and
  `pagination` in a final `_posts` article are reported as page-only front
  matter violations.
- This gate keeps the final migration from becoming a renamed page dump; the
  final articles must be true blog-collection posts.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint and
  release-readiness regression tests.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to final blog-native `_posts`, recapturing rendered
  snapshots after that migration, and passing strict `verify-release-readiness`.

## Update 2026-07-15: Exact Site Page Coverage Gate

Scope:

- Tightened the site-aware publication-state audit so each kUPS post number may
  have at most one matching final `_posts` article and at most one matching
  hidden `_pages` draft.
- Added regression coverage for duplicate final `_posts` entries and duplicate
  hidden `_pages` drafts.
- No configs, results, notebooks, figures, snapshots, website pages, website
  assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 35 tests.

Code and reproducibility review:

- The previous audit selected the first matching file for a post number. That
  was too weak for final publication because duplicate pages could leave two
  URLs with conflicting prose, dates, figures, or metadata.
- The new audit reports duplicate final article matches under `_posts` and
  duplicate hidden draft matches under `_pages` before continuing to run the
  normal blog-style checks on the selected primary file.
- The current real website state has one hidden draft per post and no final
  `_posts` kUPS articles yet, so the accepted blocker set remains unchanged.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint and
  release-readiness regression tests.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to exactly one blog-native `_posts` article per post,
  recapturing rendered snapshots after that migration, and passing strict
  `verify-release-readiness`.

## Update 2026-07-15: Blog Prose and Summary Link Gate

Scope:

- Tightened the site-aware blog-style audit so each kUPS page must link
  directly to both smoke and full compact `*_summary.json` outputs.
- Added a prose-shape guard that rejects common copied-notebook transcript
  markers: `In [n]:`, `Out [n]:`, `execution_count:`, and `cell_type:`.
- Added regression coverage for missing compact summary links and notebook
  transcript markers.
- No configs, results, notebooks, figures, snapshots, website pages, website
  assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 36 tests.

Code and reproducibility review:

- The previous source-link gate checked config, notebook, manifest,
  figure-source, and review links, but accepted generic result-directory
  fragments. The new check requires direct smoke and full compact-summary
  links, matching the PLAN requirement to link compact summaries rather than
  notebook-only output.
- The transcript-marker guard protects the blog-native prose contract without
  banning ordinary fenced code snippets.
- The current hidden website pages already satisfy these checks.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint and
  release-readiness regression tests.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to final `_posts`, recapturing rendered snapshots
  after that migration, and passing strict `verify-release-readiness`.

## Update 2026-07-15: Static Post-Specific Figure Include Gate

Scope:

- Tightened the site-aware figure include audit so every included publication
  figure must reference a static `.svg` or `.png` asset.
- Added a post-specific figure-path check so a Post XX page cannot accidentally
  include a diagnostic asset named for another post.
- Added regression coverage for a `.gif` include and a Post 06 page that
  points at a Post 07 figure asset.
- No configs, results, notebooks, figure assets, snapshots, website pages,
  website assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 37 tests.

Code and reproducibility review:

- The previous figure gate checked `assets/img/blog/`, class, zoomable state,
  caption dollar delimiters, and caption sentence count, but it did not
  constrain file type or post identity.
- The new check keeps the final website contract aligned with static
  publication SVG/PNG figures and prevents copy-paste mistakes across posts.
- The current hidden website pages already satisfy these checks.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, or CSS-sensitive
  markup changed, so no rendered desktop/mobile page snapshots were required.
  Existing rendered-page evidence remains in `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint and
  release-readiness regression tests.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to final `_posts`, recapturing rendered snapshots
  after that migration, and passing strict `verify-release-readiness`.

## Update 2026-07-15: Website Snapshot Capture Infrastructure Gate

Scope:

- Added a site-aware release-readiness check for the website snapshot capture
  infrastructure used by the rendered-page review ledger.
- The gate now verifies `../sungsoo-ahn.github.io/.github/workflows/kups-snapshots.yml`
  keeps manual dispatch inputs, Chromium installation, the
  `scripts/capture_kups_snapshots.js` command, the `snapshots/kups-md-pages`
  output directory, and the `kups-md-page-snapshots` artifact.
- The gate also verifies the capture script keeps desktop and mobile
  viewports, direct-link kUPS URLs for the index and posts 01-12, HTTP failure
  checks, network-idle navigation, full-page screenshots, and a manifest.
- Added regression coverage for a stale artifact name, a removed mobile
  viewport, and disabled full-page capture.
- No configs, results, notebooks, figure assets, snapshots, website pages,
  website assets, or CSS-sensitive markup changed in this pass.

Commands:

- `uv run ruff check src/kups_md_tutorials/release_readiness.py tests/test_release_readiness.py`
  passed.
- `uv run pytest tests/test_release_readiness.py -q` passed with 38 tests.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io --allow-current-blockers`
  passed.
- `uv run kups-tutorial verify-release-readiness --site-root ../sungsoo-ahn.github.io`
  failed only on the expected final-release blockers: production GPU
  diagnostics, hidden/non-final pages, missing final `_posts`, and snapshot
  recapture after public indexing.

Code and reproducibility review:

- The previous release gate read `reviews/page-snapshots.md` and the website
  build ledger, but it did not prove the website repository still had the
  capture workflow and script required to reproduce those snapshot artifacts.
- The new check ties the ledger to the workflow and script that can regenerate
  desktop/mobile direct-link page snapshots.
- The current website checkout satisfies the new infrastructure check.

Figure and rendered-page review:

- No figure assets or figure-generation code changed, so no figure snapshot was
  required.
- No website prose, front matter, linked figures, page assets, capture output,
  or CSS-sensitive markup changed, so no new rendered desktop/mobile page
  snapshots were required. Existing rendered-page evidence remains in
  `reviews/page-snapshots.md`.

Review decision:

- Accepted for the release-readiness tooling milestone after focused lint,
  release-readiness regression tests, and a site-aware audit against the real
  website checkout.
- Final release remains blocked on production GPU diagnostics, public indexing,
  migrating hidden drafts to final `_posts`, recapturing rendered snapshots
  after that migration, and passing strict `verify-release-readiness`.

## Open Items

Blocking items for the current hidden draft/tooling milestone:

- None.

Non-blocking items accepted until the final article pass:

- The routine CI release-surface audit intentionally runs with `--skip-site
  --allow-current-blockers` while the website pages remain hidden drafts.

Final-release blockers:

- Resolve the blockers reported by `uv run kups-tutorial
  verify-release-readiness`.
- Run the command without `--skip-site` after final website pages are public,
  non-hidden, and no longer marked as drafts.
