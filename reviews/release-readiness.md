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

## Open Items

Blocking items for the current hidden draft/tooling milestone:

- None.

Non-blocking items accepted until the final article pass:

- `verify-release-readiness` is not part of routine CI yet because the current
  repository is not final-publication ready.

Final-release blockers:

- Resolve the blockers reported by `uv run kups-tutorial
  verify-release-readiness`.
- Run the command without `--skip-site` after final website pages are public,
  non-hidden, and no longer marked as drafts.
