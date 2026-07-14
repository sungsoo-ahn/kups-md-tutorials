# Post 01 Review Notes

## Scope

- Post: 01
- Profile reviewed: smoke
- Current status: initialization workflow and first diagnostic figure are in
  place; notebook, website post, full-run review, and rendered page snapshots
  are still pending.

## Commands

- `uv run kups-tutorial run 01 --profile smoke`
- `uv run kups-tutorial verify 01 --profile smoke`
- `uv run python scripts/generate_post01_figures.py`
- `uv run jupyter execute notebooks/post-01-initialization.ipynb --inplace`
- `uv run pytest -q`
- `uv run ruff check .`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `curl -I -L https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`
- attempted `npx --yes playwright@latest screenshot ...` for desktop/mobile
  snapshots; blocked because the local Node.js is 12.22.9 and Playwright
  requires Node.js 18 or higher.

## Code And Reproducibility Review

- Configs are committed under `configs/post-01/`.
- Smoke outputs are committed under `results/post-01/smoke/`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- Velocity initialization uses ASE `thermalize_momenta` with a fixed RNG seed.
- Center-of-mass momentum removal is enabled and verified from the compact
  summary.

Open items:

- Add rendered page snapshots after the hidden website draft deploys.
- Decide whether to commit full-profile initialization outputs after reviewing
  their size and scientific value.

## Scientific Review

- The smoke initial state has 32 argon atoms at the configured number density.
- The kinetic temperature is a stochastic Maxwell-Boltzmann draw, not forced to
  the target temperature. The observed difference between target and sample
  temperature is expected for this small smoke system and should be explained in
  the article.
- The figure should not imply that the smoke histogram is a converged
  distributional test; it is a diagnostic snapshot of deterministic
  initialization.

Open items:

- Add a larger full-profile figure or table if a smoother velocity distribution
  is needed for publication.
- Add explicit text explaining when exact temperature rescaling is useful and
  why it changes the sampled distribution.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-01/initialization_diagnostics_snapshot.png`

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

Open items:

- Recheck mobile rendering once the website post exists.
- Confirm caption wording in the website draft uses `\(...\)` for any math.

## Notebook Review

- `notebooks/post-01-initialization.ipynb` executes from a clean kernel.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating initialization or plotting implementation details.
- The notebook displays the committed smoke summary and regenerates the
  diagnostic figure from the committed initial state.

Open items:

- Add the full prose article in the website repository.
- Re-run the notebook after full-profile outputs are added.

## Website Draft Review

- Added and deployed a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke summary, manifest, and review note.
- Copied the reviewed SVG figure to
  `assets/img/blog/kups_md_post01_initialization_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- The deployed page returns HTTP 200.

Open items:

- Capture and inspect deployed desktop and mobile snapshots for this hidden
  page. The current local environment lacks a browser-capable screenshot path:
  `bundle` is unavailable, no Chromium/Firefox binary is installed, and
  Playwright CLI is blocked by Node.js 12.22.9.
- Expand the draft into the full 3,500-10,000-word article after full-profile
  outputs and final figures are reviewed.
