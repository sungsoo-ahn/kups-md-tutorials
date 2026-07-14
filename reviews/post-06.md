# Post 06 Review Notes

## Scope

- Post: 06
- Profiles reviewed: smoke and full
- Current status: controlled correlated-observable trajectory-length workflow,
  committed smoke/full outputs, notebook, full-profile diagnostic figure,
  expanded hidden website draft, rendered page snapshots, and self-review
  artifact are in place; the final argon/kUPS physical-observable diagnostic is
  still pending.

## Commands

- `uv run kups-tutorial run 06 --profile smoke`
- `uv run kups-tutorial verify 06 --profile smoke`
- `uv run kups-tutorial run 06 --profile full`
- `uv run kups-tutorial verify 06 --profile full`
- `uv run python scripts/generate_post06_figures.py`
- `uv run jupyter execute notebooks/post-06-trajectory-length.ipynb --inplace`
- `uv run ruff check src tests scripts`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29360919260` for website commit
  `aac0e52f2cbfc388afc884073e36172cd26e4c9e`
- GitHub Actions snapshot run `29361099780`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-06/`.
- Smoke and full outputs are committed under `results/post-06/`.
- The workflow uses a deterministic correlated observable with a known
  equilibrium mean, stationary variance, equilibration decay, and correlation
  time.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 06.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating uncertainty or plotting implementation details.

Open items:

- Replace or augment the controlled observable with argon/kUPS observable
  diagnostics before treating the post as final.

## Scientific Review

- The full profile uses six independent replicas of a correlated observable
  with true mean `0.5`, stationary variance `1.0`, correlation time `30`, and
  an initial bias that decays with time constant `120`.
- The full-profile conservative standard error falls from about `0.162` at
  `2000` steps to about `0.0208` at `24000` steps.
- Effective sample size increases from about `149` to about `2296`, while raw
  retained samples increase from `1500` to `34500`.
- The final full-profile estimate is `0.4936`, within the conservative 95%
  half-width of `0.0408` around the known mean.
- Naive standard errors are smaller than autocorrelation-, block-, or
  replica-aware uncertainty estimates, supporting the claim that frame count is
  not the same thing as independent information.

Open items:

- The website prose should not imply that the known mean exists in real MD. In
  production, replica agreement and uncertainty diagnostics replace access to
  the answer key.
- The final article should connect this controlled diagnostic to actual
  observables such as energy, density, RDF coordination, or time-correlation
  estimates from argon/kUPS runs.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-06/trajectory_length_diagnostics_snapshot.png`
- `snapshots/post-06/trajectory_length_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable, running means visibly retain
  early-history memory, uncertainty bars clearly separate naive and
  block/replica-aware estimates, and the ESS panel increases with trajectory
  length.
- The current figure is intentionally about estimator behavior, not a physical
  argon observable. A final post should add a production observable figure if
  physical equilibration claims are made.

Open items:

- Add a production-observable trajectory-length figure after argon/kUPS
  diagnostics are implemented.

## Notebook Review

- `notebooks/post-06-trajectory-length.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
  values, and regenerates the full-profile diagnostic figure from committed
  result files.
- The notebook keeps the explanation focused on warmup removal,
  autocorrelation, ESS, block uncertainty, and replica agreement rather than
  becoming the implementation source.

Open items:

- Add citations for autocorrelation, effective sample size, blocking analysis,
  and equilibration diagnostics before final publication.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post06_trajectory_length_diagnostics.svg`.
- Expanded the hidden page from the short draft to about 3,534 words. The
  expanded prose explains warmup removal, autocorrelation, effective sample
  size, block uncertainty, replica agreement, checkpoints, physical-observable
  extensions, and methods reporting.
- The expanded prose keeps the scope clear: the committed result is a
  controlled correlated-observable diagnostic, not a final argon/kUPS physical
  observable trajectory-length study.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29360919260` succeeded for commit
  `aac0e52f2cbfc388afc884073e36172cd26e4c9e`.
- Snapshot workflow run `29361099780` captured the expanded hidden page.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post06-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-expanded-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`;
  both returned HTTP 200 with page title
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post06-expanded-snapshots/post-06-desktop.png` and
  `/tmp/kups-post06-expanded-snapshots/post-06-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, diagnostic tables, display equation,
  full-profile trajectory-length figure, reproduction code block,
  current-status section, references, and footer present. No blank page, missing
  figure, obvious clipping, or broken page chrome was found in the inspected
  snapshot.
- Mobile capture renders the same content through the mobile layout with title,
  navigation, author note, tables, equation, figure, code block,
  current-status section, and references present. Tables are narrow but readable
  and are not clipped in the inspected snapshot.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Add argon/kUPS trajectory-length diagnostics for physical observables before
  treating this post as final.
- Re-run the page snapshot workflow after the final physical-observable figure
  and citations are added.
