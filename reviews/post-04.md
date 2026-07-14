# Post 04 Review Notes

## Scope

- Post: 04
- Profiles reviewed: smoke and full
- Current status: controlled BAOAB Langevin thermostat diagnostic workflow plus
  compact reduced-unit argon Langevin temperature-response diagnostic,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  expanded hidden website draft, rendered page snapshots, and self-review
  artifact are in place.

## Commands

- `uv run kups-tutorial run 04 --profile smoke`
- `uv run kups-tutorial verify 04 --profile smoke`
- `uv run kups-tutorial run 04 --profile full`
- `uv run kups-tutorial verify 04 --profile full`
- `uv run python scripts/generate_post04_figures.py`
- `uv run jupyter execute notebooks/post-04-thermostats.ipynb --inplace`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run ruff check .`
- `uv run kups-tutorial verify-artifacts`
- `uv run kups-tutorial verify-reviews`
- `uv run kups-tutorial export-site --posts 04 --profile full`
- `git diff --check`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`
- GitHub Pages deploy `29359119367` for website commit
  `7aa89addc2ee2fa2e334bdc2f2b9a38fecb22a07`.
- GitHub Actions snapshot workflow `29359320951` for post 04.

## Code And Reproducibility Review

- Configs are committed under `configs/post-04/`.
- Smoke and full outputs are committed under `results/post-04/`.
- The workflow uses a deterministic BAOAB Langevin harmonic oscillator with
  fixed seeds and coupling strengths.
- The workflow now also includes a deterministic compact argon Langevin
  diagnostic: reduced-unit Lennard-Jones argon FCC cells, seeded velocities,
  vectorized minimum-image forces, BAOAB Langevin updates, and downsampled
  kinetic-temperature traces in `argon_langevin_samples.csv`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 04.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating thermostat or plotting implementation details.

Open items:

- Replace or augment the compact reduced-unit argon check with a larger GPU
  kUPS production thermostat and NVE-handoff diagnostic before treating this
  post as final. The current argon run is a many-body sanity check, not the
  target production MD experiment described in the plan.

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
- The full compact argon Langevin diagnostic contains 108 atoms at reduced
  density `0.65` and target temperature `0.70`. Kinetic-temperature means are
  about `0.614`, `0.698`, and `0.703` for `gamma = 0.2`, `1.0`, and `4.0`;
  all stay within the configured review threshold, and the weak-coupling
  under-target result is visible in the figure rather than hidden.
- The argon result supports a many-body kinetic-temperature response sanity
  check, but it is not a GPU kUPS production thermostat benchmark and should
  not be described as final production evidence.

Open items:

- Keep the distinction between moment checks and dynamical distortion in the
  final all-post consistency pass.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-04/thermostat_diagnostics_snapshot.png`
- `snapshots/post-04/thermostat_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable at the generated snapshot size,
  the variance and kinetic panels show the canonical target line clearly, and
  the autocorrelation panel makes the strong-coupling dynamical distortion
  visible.
- New compact argon pass: the first four-panel full-profile snapshot at
  `1728 x 1120` showed the argon kinetic-temperature traces clearly, but the
  title "Argon temperature remains controlled" overstated the weak-coupling
  trace, which sits below target in the compact run.
- Revised the argon panel title to "Argon thermostat temperature response",
  added a white legend frame, regenerated
  `snapshots/post-04/thermostat_diagnostics_full_snapshot.png`, and inspected
  the second pass. The revised figure no longer overclaims the compact argon
  result, the legend remains readable, and no panel labels or tick labels are
  clipped.
- The figure is intentionally moment-focused; it does not yet show the full
  kinetic-energy distribution. That is acceptable for this draft but should be
  revisited if the final prose makes a distribution-shape claim.

Open items:

- Consider adding a kinetic-energy histogram or empirical CDF in the final
  article if canonical sampling claims become stronger.
- Repeat figure snapshot review after any larger GPU kUPS production
  thermostat or NVE-handoff panel is added.

## Notebook Review

- `notebooks/post-04-thermostats.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on sampling and dynamics rather
  than becoming the implementation source.

Open items:

- Re-execute the notebook if the final article adds a kinetic-energy histogram,
  empirical CDF, or larger GPU kUPS thermostat figure.

## Website Draft Review

- Added, expanded, and deployed a hidden draft page in
  `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG/PNG figure and compact full-profile
  result files, including `argon_langevin_samples.csv`, to
  `../sungsoo-ahn.github.io/assets/` via `uv run kups-tutorial export-site
  --posts 04 --profile full`.
- Expanded the article body from about 738 words to about 3,630 words. The
  expanded draft now covers thermostat maps, BAOAB Langevin splitting,
  coupling strength, canonical moment targets, temperature as insufficient
  evidence, compact argon temperature response, autocorrelation and effective
  sample size, NVE handoff, enhanced sampling implications, thermostat
  families, stronger distribution checks, common failure modes, replica design,
  and final-release limitations.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes in the website repository with
  pre-existing unused-image warnings.
- `git diff --check` passes in the website repository.
- GitHub Pages deploy `29359119367` built and deployed website commit
  `7aa89addc2ee2fa2e334bdc2f2b9a38fecb22a07` successfully.
- The deployed page snapshot manifest from workflow `29359320951` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post04-expanded-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-expanded-snapshots/post-04-mobile.png`

Rendered feedback:

- Desktop full-page capture renders the expanded article end to end: sidebar
  table of contents, equations, multiple tables, thermostat diagnostic figure,
  reproduction code block, current-status section, references, and footer are
  present. No missing asset, blank page, obvious clipped text, or broken page
  chrome was found in the inspected snapshot.
- Mobile full-page capture renders the title, author note, equations, tables,
  figure, code block, status, references, and footer. The tables are narrow but
  readable and not clipped in the inspected screenshot. Keep table wrapping as
  a final typography-polish item after the remaining articles are expanded.

Open items:

- The page remains intentionally hidden from public navigation.
- Re-run deployed desktop/mobile page snapshots after the updated figure and
  prose are committed and deployed.
- Add a larger GPU kUPS production thermostat and NVE-handoff diagnostic before
  treating this post as final.
