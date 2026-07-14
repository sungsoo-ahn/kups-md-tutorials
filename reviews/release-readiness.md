# Release Readiness Review Notes

## Scope And Provenance

- Scope: final-publication gate for the twelve-post kUPS MD tutorial series.
- Current status: a `verify-release-readiness` CLI command is implemented and
  intentionally fails while final-release blockers remain.
- Working-tree state: release-readiness audit implementation, tests, README,
  PLAN, and this review note are staged for the current pass.
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
  page state.
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
  pinned model artifact hash, and post-snapshot recapture after final changes.
- The post 12 placeholder MACE metadata is treated as a hard release blocker,
  not a warning.

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
