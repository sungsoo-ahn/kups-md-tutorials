# Post 04 Review Notes

## Scope

- Post: 04
- Profiles reviewed: smoke and full
- Current status: controlled BAOAB Langevin thermostat diagnostic workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  hidden website draft, and self-review artifact are in place; final prose and
  rendered page snapshots are still pending.

## Commands

- `uv run kups-tutorial run 04 --profile smoke`
- `uv run kups-tutorial verify 04 --profile smoke`
- `uv run kups-tutorial run 04 --profile full`
- `uv run kups-tutorial verify 04 --profile full`
- `uv run python scripts/generate_post04_figures.py`
- `uv run jupyter execute notebooks/post-04-thermostats.ipynb --inplace`
- `uv run pytest -q`
- `uv run ruff check .`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`

## Code And Reproducibility Review

- Configs are committed under `configs/post-04/`.
- Smoke and full outputs are committed under `results/post-04/`.
- The workflow uses a deterministic BAOAB Langevin harmonic oscillator with
  fixed seeds and coupling strengths.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 04.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating thermostat or plotting implementation details.

Open items:

- Add rendered page snapshots after the hidden website draft deploys.
- Add an argon/kUPS thermostat diagnostic before treating this post as final.
  The current oscillator isolates canonical sampling and dynamical memory, but
  does not yet test thermostat behavior on the target argon trajectory family.

## Scientific Review

- The full profile compares BAOAB Langevin coupling strengths `gamma = 0.1`,
  `1.0`, and `5.0` at target temperature `kT = 1`.
- Observed configurational and velocity variances are within roughly 8% of the
  canonical targets in the full run.
- Mean kinetic energy is within roughly 7% of the `0.5 kT` target for all full
  thermostat cases.
- The strong-coupling case has much larger position integrated autocorrelation
  time (`~53`) than the weak/moderate cases (`~10-13`), supporting the claim
  that thermostat coupling changes dynamics even when moments look acceptable.

Open items:

- The website prose should avoid implying that a correct kinetic temperature is
  sufficient evidence of canonical sampling.
- The final article should explain when to switch from thermostatted sampling
  to NVE production for dynamical observables.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-04/thermostat_diagnostics_snapshot.png`
- `snapshots/post-04/thermostat_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable at the generated snapshot size,
  the variance and kinetic panels show the canonical target line clearly, and
  the autocorrelation panel makes the strong-coupling dynamical distortion
  visible.
- The figure is intentionally moment-focused; it does not yet show the full
  kinetic-energy distribution. That is acceptable for this draft but should be
  revisited if the final prose makes a distribution-shape claim.

Open items:

- Recheck mobile rendering after the website draft exists.
- Consider adding a kinetic-energy histogram or empirical CDF in the final
  article if canonical sampling claims become stronger.

## Notebook Review

- `notebooks/post-04-thermostats.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on sampling and dynamics rather
  than becoming the implementation source.

Open items:

- Add the full prose article in the website repository.
- Add citations for Langevin dynamics, BAOAB splitting, canonical sampling, and
  thermostat-induced dynamical distortion when writing the website draft.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post04_thermostat_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Capture and inspect deployed desktop and mobile snapshots for this hidden
  page.
- Expand the draft into the full 3,500-10,000-word article after rendered page
  snapshots and the argon/kUPS thermostat diagnostic are reviewed.
