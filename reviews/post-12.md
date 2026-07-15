# Post 12 Review Notes

## Scope And Provenance

- Post: 12
- Profiles reviewed: smoke and full
- Current status: controlled MLIP reliability workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, expanded
  hidden website draft, rendered page snapshots, pinned MACE artifact metadata,
  and this self-review artifact are in place. The page remains hidden from
  public navigation.
- Working-tree state: pinned-artifact tutorial commit
  `35f16fe7df747b97c77e474312d529e3865f7707` and website commit
  `a755ec8f3a2f2d3cf48081e9bd48f4b9c178c588` were reviewed in the
  pinned-artifact pass; later review-ledger consistency edits are recorded
  below.
- Hidden draft URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`

## Commands

- `uv run kups-tutorial run 12 --profile smoke`
- `uv run kups-tutorial verify 12 --profile smoke`
- `uv run kups-tutorial run 12 --profile full`
- `uv run kups-tutorial verify 12 --profile full`
- `uv run python scripts/generate_post12_figures.py`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run jupyter execute notebooks/post-12-mlip-capstone.ipynb --inplace`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `uv run pytest -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify --profile smoke`
- `uv run kups-tutorial verify 12 --profile full`
- `git diff --check` in this repository and `../sungsoo-ahn.github.io`
- `gh run watch 29351644859 --exit-status` in `../sungsoo-ahn.github.io`
- `curl -I -L 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/?v=3c1b319'`
- `curl -L --silent 'https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/?v=3c1b319' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/?v=3c1b319' | rg ...`
- `curl -L --silent 'https://sungsoo-ahn.github.io/blog/?v=3c1b319' | rg ...`
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_kups_pages.py`
- expanded post validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_blog.py`
- expanded post whitespace check in `../sungsoo-ahn.github.io`:
  `git diff --check`
- inline math delimiter check in `../sungsoo-ahn.github.io`:
  `rg -n '\\\\(|\\\\)' _pages/kups-md-post-12-mlip-capstone.md || true`
- word-count check for the expanded page: `3518` words
- `gh run watch 29366058404 --exit-status` in `../sungsoo-ahn.github.io`
- `gh workflow run "Capture kUPS snapshots" --ref main -f posts=12` in
  `../sungsoo-ahn.github.io`
- `gh run watch 29366249219 --exit-status` in `../sungsoo-ahn.github.io`
- `gh run download 29366249219 --name kups-md-page-snapshots --dir /tmp/kups-post12-expanded-snapshots`
- live hidden-route check with cache buster `?v=c540d52`
- live homepage/blog listing checks with cache buster `?v=c540d52`

## Code And Reproducibility Review

- Configs are committed-intended under `configs/post-12/`.
- Smoke and full outputs are committed-intended under `results/post-12/`.
- The workflow is deterministic and CPU-friendly. It records pinned MACE
  artifact metadata: `mace-mp-0b3-medium.model` from
  `mace-foundations/mace-mp-0` at revision `e291ace` with SHA-256
  `2f2be696351ac9e94fbe01cdfb6f017679acdbd2db7645209ef55fec9826b012`.
  The numerical diagnostic remains a surrogate MLIP reliability diagnostic
  until the final GPU production pass replaces it with real MACE/fcc-Al
  trajectory evidence.
- The summary records static force RMSE, force bias, static energy RMSE, NVE
  drift, ensemble temperature drift, extrapolation fraction, uncertainty mean,
  two-sigma coverage, neighbor-list risk, and free-energy barrier shift.
- The manifest records the loaded config, compact output filenames, config
  hash, Git revision, Python/platform metadata, kUPS/NumPy versions, and model
  artifact metadata.
- `kups-tutorial run`, `verify`, and `run-all` include post 12.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather
  than reimplementing the capstone diagnostic or plotting.

Open items:

- Replace the deterministic CPU surrogate with a real MACE/fcc-Al GPU
  production run during the final article pass.

## Scientific Review

- The full profile compares three fcc-Al regimes: `in_domain_fcc`,
  `strained_cell`, and `extrapolative_hot`.
- Force RMSE increases from `0.0300` to `0.0689` to `0.1530`, showing that
  static force errors worsen as strain and displacement leave the configured
  training-like regime.
- Normalized NVE-like energy drift increases from `0.00261` to `0.01444` to
  `0.01912`, showing why static metrics are not enough for deployment.
- Ensemble temperature drift increases from `0.506 K` to `13.58 K` to
  `16.06 K`, connecting force bias and extrapolation to ensemble control.
- Extrapolation fraction increases from `0.00006` to `0.99448` to `1.0`, while
  neighbor-list risk increases from `0.0` to `0.1495` to `0.9714`.
- Two-sigma uncertainty coverage is high for all three regimes
  (`0.993`, `1.000`, and `1.000`), so the diagnostic demonstrates calibrated
  warning signals rather than hidden uncertainty failure.
- Free-energy barrier shift grows from effectively zero to `0.00395` and
  `0.01514`, tying MLIP force/ensemble issues back to the free-energy posts.

Open items:

- The expanded hidden page now clearly labels the current workflow as a
  deterministic surrogate diagnostic, not a completed MACE/fcc-Al GPU
  production run.
- The final pass must keep the pinned MACE artifact revision/hash, run the real
  GPU production diagnostic from that artifact, and record the GPU environment.
- The expanded hidden page now connects the MLIP checks to each earlier
  tutorial:
  initialization, integrator drift, thermostat/barostat control, observables,
  free energies, and enhanced sampling.

## Figure Feedback Review

Snapshots reviewed:

- `snapshots/post-12/mlip_diagnostics_snapshot.png`
- `snapshots/post-12/mlip_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: the static-error panel is readable and makes the
  increasing force RMSE and force bias visible.
- The dynamics/extrapolation panel shows that extrapolation and neighbor-list
  risk can be near saturation even when normalized NVE drift remains numerically
  small on the same axis.
- The uncertainty-calibration panel clearly shows the two-sigma marker and the
  case distributions of absolute force error divided by uncertainty.
- The artifact metadata annotation fits and exposes the pinned model file and
  revision. The pinned-artifact update below re-reviewed the generated figure
  and confirmed that no placeholder artifact text remains.
- No label clipping, unreadable ticks, or legend overlap was found in the
  inspected full-profile snapshot.

Rendered page figure check:

- The figure was inspected inside the rendered desktop snapshot
  `/tmp/kups-post12-expanded-snapshots/post-12-desktop.png` and mobile
  snapshot `/tmp/kups-post12-expanded-snapshots/post-12-mobile.png`.
- Desktop: the static-error, dynamics/extrapolation, and
  uncertainty-calibration panels render below the diagnostic section with axes,
  legends, and caption readable in the article column. The later
  pinned-artifact snapshot pass confirmed that the figure annotation and page
  prose contain the verified artifact metadata, not placeholder wording.
- Mobile: the figure remains legible at 555 px capture width. Panel labels are
  small but readable enough for the hidden draft, and the caption wraps without
  overlapping neighboring text.

Open items:

- Regenerate and re-review after the real MACE/fcc-Al GPU production
  diagnostics are added.

## Notebook Review

- `notebooks/post-12-mlip-capstone.ipynb` loads smoke and full configurations,
  prints committed full-summary diagnostics and artifact metadata, and
  regenerates the full-profile MLIP figure from committed result files.
- `uv run jupyter execute notebooks/post-12-mlip-capstone.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`.
- Expanded the hidden page to `3518` words with additional sections on static
  versus deployment validation, extrapolation, drift, ensemble control,
  neighbor-list risk, uncertainty calibration, observable/free-energy impact,
  artifact provenance, production-readiness requirements, and how the MLIP
  capstone closes the series.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post12_mlip_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `python3 scripts/validate_kups_pages.py` passes.
- GitHub Pages deployment `29351644859` completed successfully. The live
  hidden URL returned HTTP 200 and contained the expected title, MLIP capstone
  notebook link, full summary link, current-status section, then-current MACE
  warning, and `kups_md_post12_mlip_diagnostics.svg` figure.
- The public homepage and blog index did not contain
  `post-12-mlip-capstone` or `kups-md-tutorials` in the deployed HTML checked
  with cache-buster `?v=3c1b319`.
- Expanded-page GitHub Pages deployment `29366058404` completed successfully
  for website commit `c540d524e37527a8a586175d53cbefc76474492a`.
- Snapshot workflow `Capture kUPS snapshots` run `29366249219` completed
  successfully for post 12. Artifact `kups-md-page-snapshots` was downloaded
  to `/tmp/kups-post12-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post12-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`;
  both returned HTTP 200 and title
  `What Changes When the Potential Is a Machine-Learned Interatomic Potential? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post12-expanded-snapshots/post-12-desktop.png` at
  `1440 x 10796` and `/tmp/kups-post12-expanded-snapshots/post-12-mobile.png`
  at `555 x 16739`.
- Desktop feedback: the expanded article renders end to end with sidebar table
  of contents, hidden-draft note, source links, capstone regime table,
  provenance table, production-readiness table, MLIP diagnostic figure,
  practical checklist, reproduction block, current-status section, references,
  and footer present. No blank page, missing figure, clipped text, or broken
  page chrome was found in the inspected snapshot.
- Mobile feedback: the title wraps heavily but remains contained. Tables are
  tight but readable, the diagnostic figure and caption stay within the page,
  the reproduction code block is contained, and the footer renders normally.
- Live hidden-route check with `?v=c540d52` confirmed the expanded section
  `How Does This Close The Series?`, the figure asset, the non-final note, and
  the rendered snapshot status phrase. The later pinned-artifact pass replaced
  the earlier artifact caveat with verified model metadata.
- Live homepage and blog listing checks with `?v=c540d52` confirmed
  `post-12-mlip-capstone` and `kups-md-tutorials` are not exposed.

Open items:

- No blocking layout issue was found for the expanded post 12 hidden draft.
- Keep mobile title/table wrapping as a final typography-polish item after the
  rest of the articles are expanded.
- Re-run rendered desktop/mobile snapshots after adding final MACE/fcc-Al GPU
  diagnostics or making any public-indexing change.

## Prose And Style Review

- The expanded website draft follows the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose is concept-led for MLIP-aware ML researchers: static validation is
  not deployment validation; MD exposes extrapolation, drift, ensemble
  instability, neighbor-list risk, uncertainty calibration, and biased
  free-energy claims.

## Open Items

Blocking items for the current hidden draft:

- None.

Non-blocking items accepted until the final article pass:

- The expanded draft remains explicitly non-final.
- The numerical diagnostic remains a deterministic CPU surrogate rather than a
  real MACE/fcc-Al GPU production run.
- Mobile title and table wrapping can be polished later if desired, but the
  captured hidden draft is readable and contained.

Final-release blockers:

- Run and review the real MACE/fcc-Al GPU capstone.
- Add production diagnostics from the real GPU run and regenerate the MLIP
  figure with those production diagnostics.
- Re-run rendered desktop/mobile snapshots after final production diagnostics
  and any public-indexing changes.

## Update 2026-07-15: Pinned MACE Artifact Metadata

Scope:

- Replaced the Post 12 placeholder model metadata with pinned MACE foundation
  model metadata in `configs/post-12/smoke.json` and
  `configs/post-12/full.json`.
- Regenerated committed smoke/full outputs under `results/post-12/`, executed
  `notebooks/post-12-mlip-capstone.ipynb`, regenerated
  `figures/post-12/`, and re-created `snapshots/post-12/`.
- Refreshed the hidden website page and exported assets in
  `../sungsoo-ahn.github.io`.

Artifact provenance:

- Model file: `mace-mp-0b3-medium.model`.
- Repository: `mace-foundations/mace-mp-0`.
- Revision: `e291ace`.
- SHA-256:
  `2f2be696351ac9e94fbe01cdfb6f017679acdbd2db7645209ef55fec9826b012`.
- Source evidence checked:
  `https://huggingface.co/mace-foundations/mace-mp-0/blob/main/mace-mp-0b3-medium.model`,
  `https://github.com/ACEsuit/mace-foundations`, and
  `https://mace-docs.readthedocs.io/en/latest/guide/foundation_models.html`.
- Download verification command:
  `curl -L --fail --retry 3 -o /tmp/kups-mace-artifact/mace-mp-0b3-medium.model https://huggingface.co/mace-foundations/mace-mp-0/resolve/main/mace-mp-0b3-medium.model`
  followed by `sha256sum /tmp/kups-mace-artifact/mace-mp-0b3-medium.model`.
- The downloaded artifact hash matched the configured SHA-256 exactly. The
  model file was kept in `/tmp/kups-mace-artifact/` and was not committed.

Commands:

- `uv run kups-tutorial run 12 --profile smoke`
- `uv run kups-tutorial verify 12 --profile smoke`
- `uv run kups-tutorial run 12 --profile full`
- `uv run kups-tutorial verify 12 --profile full`
- `uv run python scripts/generate_post12_figures.py`
- `uv run jupyter execute notebooks/post-12-mlip-capstone.ipynb --inplace`
- `uv run ruff check src/kups_md_tutorials/mlip_capstone.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `git diff --check`
- `uv run kups-tutorial verify-release-readiness --skip-site`
- `uv run kups-tutorial export-site --site-root ../sungsoo-ahn.github.io --profile full --posts 12`
- Website validation in `../sungsoo-ahn.github.io`:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check`.

Code and reproducibility review:

- The regenerated `results/post-12/smoke/mlip_summary.json`,
  `results/post-12/full/mlip_summary.json`, and
  `results/post-12/full/manifest.json` record the pinned model name,
  repository, revision, and SHA-256.
- `rg` over `configs/post-12`, `results/post-12`,
  `notebooks/post-12-mlip-capstone.ipynb`, `figures/post-12`, and
  `snapshots/post-12` found the pinned artifact metadata and no old
  placeholder hash tokens in generated artifacts.
- The local run reported that an NVIDIA GPU may be present but CUDA-enabled
  `jaxlib` is not installed, so the workflow fell back to CPU. This is
  acceptable for the deterministic hidden-draft surrogate and remains
  insufficient for the final GPU capstone.
- Tutorial commit `35f16fe7df747b97c77e474312d529e3865f7707` contains the
  pinned metadata configs, regenerated results, notebook output, figures, and
  figure snapshots.
- The first CI run for `35f16fe` was `29378375343`; it failed only because
  `tests/test_release_readiness.py` still expected a placeholder-artifact
  violation after that violation was intentionally removed. The test has been
  updated to expect the remaining real GPU capstone blocker instead.

Figure feedback:

- Inspected `snapshots/post-12/mlip_diagnostics_full_snapshot.png`.
- The annotation now shows `artifact: mace-mp-0b3-medium.model` and
  `revision: e291ace`; no placeholder artifact text remains in the figure.
- Static-error, dynamics/extrapolation, and uncertainty panels remain readable.
  The annotation fits inside the uncertainty panel without clipping or legend
  collision.

Website review:

- Website commit reviewed:
  `a755ec8f3a2f2d3cf48081e9bd48f4b9c178c588`.
- Website deploy run: `29378460379`.
- Live hidden-route check with `?v=a755ec8` confirmed the page contains
  `mace-mp-0b3-medium.model`, the full SHA-256 hash, and no `placeholder`
  text.
- Snapshot workflow run: `29378598376`.
- Snapshot artifact downloaded to
  `/tmp/kups-post12-pinned-artifact-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post12-pinned-artifact-snapshots/manifest.json`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post12-pinned-artifact-snapshots/post-12-desktop.png` and
  `/tmp/kups-post12-pinned-artifact-snapshots/post-12-mobile.png`.
- Desktop feedback: the page renders end to end with the pinned-artifact note,
  source links, diagnostic tables, updated figure, production-readiness table,
  reproduction block, current-status section, references, and footer present.
- Mobile feedback: the long title, tables, updated figure, reproduction block,
  current-status section, references, and footer stay contained. Tables remain
  dense but readable enough for the hidden draft.

Release-readiness decision:

- The artifact-provenance blocker is resolved for the hidden draft: the MACE
  file, repository revision, and downloaded SHA-256 are pinned and recorded in
  configs, results, manifest, notebook output, figure annotation, and website
  prose.
- The final public article remains blocked on a real MACE/fcc-Al GPU
  production run and production diagnostic figures/snapshots from that run.

## Update 2026-07-15: Review Ledger Consistency Cleanup

Scope:

- Cleaned the older top-level Post 12 review sections so they no longer
  contradict the later pinned-artifact update.
- No configs, results, notebooks, figures, website page, or website assets
  changed in this pass.

Commands:

- `rg -n "placeholder|MACE|artifact|model_revision|model_sha256|sha256|GPU|production" reviews/post-12.md reviews/page-snapshots.md configs/post-12 results/post-12 figures/post-12 notebooks/post-12-mlip-capstone.ipynb`
- `rg -n "placeholder|MACE|artifact|model_revision|model_sha256|sha256|GPU|production|non-final|Current Status" _pages/kups-md-post-12-mlip-capstone.md assets/img/blog/kups_md_post12_mlip_diagnostics.svg` in `../sungsoo-ahn.github.io`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial verify-release-readiness --skip-site`
- `git diff --check`

Review decision:

- The current committed Post 12 configs, results, notebook output, figure
  annotation, and website page already record pinned MACE metadata:
  `mace-mp-0b3-medium.model`, revision `e291ace`, SHA-256
  `2f2be696351ac9e94fbe01cdfb6f017679acdbd2db7645209ef55fec9826b012`.
- The remaining `placeholder` mentions in this file are historical notes in
  the pinned-artifact update, describing the earlier issue that was fixed.
- No new figure snapshot was required because this pass changed only review
  prose. The relevant existing inspected figure snapshot remains
  `snapshots/post-12/mlip_diagnostics_full_snapshot.png`.
- No new rendered page snapshot was required because this pass did not change
  the website page, assets, front matter, CSS-sensitive markup, or linked
  figures. The relevant existing rendered snapshots remain
  `/tmp/kups-post12-pinned-artifact-snapshots/post-12-desktop.png` and
  `/tmp/kups-post12-pinned-artifact-snapshots/post-12-mobile.png` from
  snapshot workflow run `29378598376`.
- `uv run kups-tutorial verify-reviews` passed for all 12 posts.
- `uv run kups-tutorial verify-release-readiness --skip-site` still fails, as
  expected, on hidden/public-release blockers and the real MACE/fcc-Al GPU
  production blocker. It no longer reports placeholder artifact metadata as a
  blocker.

## Update 2026-07-15: MLIP Validation Citation Pass

Scope:

- Updated the hidden website page at website commit `e03d963` to cite MLIP
  validation guidance and the MACE-MP-0 foundation-model context.
- Added prose that separates a qualitative foundation-model pilot from a
  quantitative fcc-Al dynamics or free-energy claim.
- Added the planned final GPU pass protocol: exact MACE artifact/revision,
  fcc-Al cell and initialization path, timestep and precision policy,
  neighbor/cutoff settings, thermostat or NVE handoff, trajectory length and
  replica plan, model-support diagnostics, observable/free-energy targets, and
  rejection or claim-narrowing rules.
- Updated the hidden page's Current Status so the current citation pass is no
  longer listed as missing. Additional citations are only required if the final
  production article adds new scientific claims beyond the current controlled
  MLIP-reliability and protocol discussion.
- No tutorial code, configs, notebooks, result files, figures, or local figure
  snapshots changed in this pass.

Source checks:

- Existing page context retained the earlier MLIP references: Behler &
  Parrinello, Bartok et al., Batzner et al., and Batatia et al. 2022.
- Added Morrow, Gardner & Deringer, "How to validate machine-learned
  interatomic potentials", *The Journal of Chemical Physics* 158, 121501
  (2023), DOI `10.1063/5.0139611`, for the task-specific validation claim.
- Added Batatia et al., "A foundation model for atomistic materials chemistry",
  *The Journal of Chemical Physics* 163, 184110 (2025), checked at
  `https://pubs.aip.org/aip/jcp/article/163/18/184110/3372267/A-foundation-model-for-atomistic-materials`,
  for the MACE-MP-0 foundation-model and task-specific-validation context.

Website validation:

- Website validators at commit `e03d963` passed:
  `python3 scripts/validate_kups_pages.py`,
  `python3 scripts/validate_blog.py`, and `git diff --check`.
- Website deploy run `29410048273` completed successfully.
- Live hidden-route check with cache-buster `?v=e03d963` confirmed the page
  contains the new Morrow citation, Batatia foundation-model citation,
  foundation-model-family text, final-GPU-protocol paragraph, and updated
  Current Status language.
- Live homepage and `/blog/` checks with cache-buster `?v=e03d963` found no
  `kups-md-tutorials` or `post-12-mlip-capstone` links, so the page remains
  direct-link only.

Rendered-page review:

- Snapshot workflow run: `29410306409`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post12-mlip-validation-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post12-mlip-validation-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile captures of
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`
  both returned HTTP 200 with title
  `What Changes When the Potential Is a Machine-Learned Interatomic Potential? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post12-mlip-validation-snapshots/post-12-desktop.png`
  (`1440 x 11364`) and
  `/tmp/kups-post12-mlip-validation-snapshots/post-12-mobile.png`
  (`555 x 17739`).
- Desktop feedback: the title, hidden-draft notice, source links, Morrow and
  Batatia citation text, diagnostic tables, diagnostic figure, reproduction
  block, final-GPU-protocol paragraph, updated Current Status, references, and
  footer render without visible clipping or missing assets.
- Mobile feedback: the long title, citation paragraphs, stacked tables,
  diagnostic figure, production-readiness table, reproduction block, Current
  Status section, references, and footer remain contained within the article
  width. The figure and tables are dense but acceptable for the hidden draft.

Prose and style review:

- The new citations are attached to claims that need them: task-specific MLIP
  validation and foundation-model deployment limits.
- The page still distinguishes the deterministic CPU surrogate from the final
  real MACE/fcc-Al GPU production evidence.
- The production protocol paragraph improves the article as a planning
  document without making unsupported production claims.

Open items:

- No additional hidden-draft blockers were found in this pass.
- Final release remains blocked on the real MACE/fcc-Al GPU production run,
  production diagnostics, regenerated production figure if the numerical
  evidence changes, and refreshed rendered snapshots after final production
  diagnostics or any public-indexing change.
