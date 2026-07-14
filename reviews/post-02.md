# Post 02 Review Notes

## Scope

- Post: 02
- Profiles reviewed: smoke and full
- Current status: harmonic-oscillator integrator diagnostic workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  hidden website draft, and self-review artifact are in place; final prose and
  rendered page snapshots are still pending.

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

- Add rendered page snapshots after the hidden website draft deploys.
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

- The website prose should explain that symplectic structure and time
  reversibility are properties of the discrete map, not generic consequences of
  writing down Newton's equation.
- The article should avoid overgeneralizing from the harmonic oscillator to
  chaotic many-body trajectories; it is a microscope for integrator structure.

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

- Recheck mobile rendering after the website draft exists.
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

- Add citations for Verlet, symplectic integration, and shadow Hamiltonian
  discussion when writing the website draft.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-02-integrators/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post02_integrator_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Capture and inspect deployed desktop and mobile snapshots for this hidden
  page.
- Expand the draft into the full 3,500-10,000-word article after rendered page
  snapshots are reviewed.
