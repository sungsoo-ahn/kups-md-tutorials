# Release Readiness Review Notes

## Scope And Provenance

- Scope: final-publication gate for the twelve-post kUPS MD tutorial series.
- Current status: a `verify-release-readiness` CLI command is implemented and
  intentionally fails while final-release blockers remain.
- Current working-tree state for this ledger refresh: review prose update on
  top of tutorial commit `2ec3ee8`; no release-readiness code, tests, configs,
  results, notebooks, figures, or website pages changed in this pass.
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
