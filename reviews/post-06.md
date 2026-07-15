# Post 06 Review Notes

## Scope

- Post: 06
- Profiles reviewed: smoke and full
- Current status: controlled correlated-observable trajectory-length workflow,
  compact reduced-unit argon potential-energy-per-atom trajectory-length
  workflow, committed smoke/full outputs, notebook, full-profile diagnostic
  figure, expanded hidden website draft, rendered page snapshots, and
  self-review artifact are in place; larger GPU kUPS physical-observable
  diagnostics remain pending before public release.

## Commands

- `uv run kups-tutorial run 06 --profile smoke`
- `uv run kups-tutorial verify 06 --profile smoke`
- `uv run kups-tutorial run 06 --profile full`
- `uv run kups-tutorial verify 06 --profile full`
- `uv run python scripts/generate_post06_figures.py`
- `uv run jupyter execute notebooks/post-06-trajectory-length.ipynb --inplace`
- `uv run ruff check .`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run kups-tutorial verify-artifacts`
- `git diff --check`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29360919260` for website commit
  `aac0e52f2cbfc388afc884073e36172cd26e4c9e`
- GitHub Actions snapshot run `29361099780`
- GitHub Actions tutorial verification run `29371910390` for tutorial commit
  `0993f2f940f66501fd2e4318bd7b9a8663edbfec`
- GitHub Actions deploy run `29371909883` for website commit
  `9260ea3910a111ff76adbd8b837fa7938b9314b6`
- GitHub Actions snapshot run `29372062650`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-06/`.
- Smoke and full outputs are committed under `results/post-06/`.
- The workflow uses a deterministic correlated observable with a known
  equilibrium mean, stationary variance, equilibration decay, and correlation
  time.
- The workflow now also writes `argon_observable_samples.csv`, a compact
  reduced-unit FCC argon Langevin trajectory-length diagnostic for potential
  energy per atom across independent replicas and checkpoints.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 06.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating uncertainty or plotting implementation details.

Open items:

- Add larger GPU kUPS observable diagnostics before treating the post as final.
  The compact argon check exercises real atomistic coordinates and a physical
  potential-energy observable, but it is not yet a production kUPS trajectory
  study.

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
- The full-profile compact argon diagnostic uses 108 atoms, five replicas, and
  potential energy per atom as the physical observable. Effective samples grow
  from about `34.9` to `114.8`, and autocorrelation-adjusted standard error
  falls from about `0.0186` to `0.0117`.
- Replica standard error increases from about `0.0304` to `0.0479` across the
  argon checkpoints, so the conservative interval does not shrink. This is not
  hidden: it is the review signal that independent reduced-unit replicas still
  disagree and that more production sampling or a different observable protocol
  is needed before final claims.

Open items:

- The website prose should not imply that the known mean exists in real MD. In
  production, replica agreement and uncertainty diagnostics replace access to
  the answer key.
- The final article should connect this compact energy observable to larger
  GPU kUPS observables such as density, RDF coordination, or time-correlation
  estimates.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-06/trajectory_length_diagnostics_snapshot.png`
- `snapshots/post-06/trajectory_length_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable, running means visibly retain
  early-history memory, uncertainty bars clearly separate naive and
  block/replica-aware estimates, and the ESS panel increases with trajectory
  length.
- Compact argon physical-observable refresh: the fourth panel is visible in
  `snapshots/post-06/trajectory_length_diagnostics_full_snapshot.png`; `PE /
  atom` labels fit, checkpoint error bars are visible, and pale replica traces
  show residual disagreement without obscuring the checkpoint means.
- The current figure includes a physical reduced-unit argon observable, but it
  does not yet show density, RDF coordination, long-time dynamics, or GPU kUPS
  production behavior.

Open items:

- Add larger production-observable trajectory-length figures after GPU kUPS
  diagnostics are implemented.

## Notebook Review

- `notebooks/post-06-trajectory-length.ipynb` executes from a clean kernel.
- The notebook loads smoke and full configurations, displays committed summary
  values, reports compact argon potential-energy-per-atom checkpoint
  uncertainty, and regenerates the full-profile diagnostic figure from
  committed result files.
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
- Refreshed the hidden page to describe the compact reduced-unit argon
  potential-energy-per-atom diagnostic and its residual replica disagreement.
- The expanded prose keeps the scope clear: the committed result is a
  controlled correlated-observable diagnostic plus a compact reduced-unit argon
  physical-observable check, not a final GPU kUPS physical-observable
  trajectory-length study.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29360919260` succeeded for commit
  `aac0e52f2cbfc388afc884073e36172cd26e4c9e`.
- Snapshot workflow run `29361099780` captured the expanded hidden page.
- Snapshot workflow run `29372062650` captured the compact argon observable
  refresh for website commit `9260ea3910a111ff76adbd8b837fa7938b9314b6`.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post06-expanded-snapshots/`.
- Refreshed snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post06-argon-observable-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-expanded-snapshots/manifest.json`.
- Refreshed manifest reviewed:
  `/tmp/kups-post06-argon-observable-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`;
  both returned HTTP 200 with page title
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post06-expanded-snapshots/post-06-desktop.png` and
  `/tmp/kups-post06-expanded-snapshots/post-06-mobile.png`.
- Refreshed rendered snapshots visually inspected:
  `/tmp/kups-post06-argon-observable-snapshots/post-06-desktop.png` and
  `/tmp/kups-post06-argon-observable-snapshots/post-06-mobile.png`.

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
- Refreshed desktop capture renders the compact argon observable article end
  to end with the updated source links, controlled and argon diagnostic tables,
  four-panel figure, reproduction code block, practical checklist,
  current-status section, references, and footer visible. No blank page,
  missing figure, obvious clipping, or broken page chrome was found in the
  inspected snapshot.
- Refreshed mobile capture renders the updated page with the four-panel figure
  visible and the argon panel present. The narrow left navigation and tables
  remain tight, consistent with prior hidden-page captures, but no blocking
  clipping or missing asset was found in the inspected snapshot.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Add larger GPU kUPS trajectory-length diagnostics for physical observables
  before treating this post as final.
- Re-run the page snapshot workflow again after the final production
  physical-observable figures and citations are added.

## Coordination-Observable Refresh

- Date: 2026-07-15.
- Scope: strengthen the compact argon physical-observable diagnostic so post 06
  is not limited to potential energy per atom.
- Added `coordination_cutoff` to the post 06 argon-observable config and
  validation. The committed smoke and full profiles use `rc = 1.5` in
  reduced Lennard-Jones units.
- The argon sample CSV now records both potential energy per atom and
  per-replica coordination number. The summary JSON now reports independent
  naive, autocorrelation-aware, replica-aware, conservative, and 95 percent
  half-width diagnostics for both observables.
- The fourth figure panel now overlays potential-energy checkpoint uncertainty
  with coordination-number checkpoint uncertainty on a right-hand axis.
- The hidden website draft now describes the compact physical-observable check
  as potential energy per atom plus coordination number, while still stating
  that this is not the final GPU kUPS production trajectory-length study.

Commands:

- `uv run ruff check src/kups_md_tutorials/config.py src/kups_md_tutorials/trajectory_length.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_config.py`
- `uv run pytest tests/test_config.py::test_load_trajectory_length_spec -q`
- `uv run kups-tutorial run 06 --profile smoke`
- `uv run kups-tutorial verify 06 --profile smoke`
- `uv run kups-tutorial run 06 --profile full`
- `uv run kups-tutorial verify 06 --profile full`
- `uv run python scripts/generate_post06_figures.py`
- `uv run jupyter execute notebooks/post-06-trajectory-length.ipynb --inplace`

Scientific review:

- Smoke profile: 32 atoms, three replicas, `rc = 1.5`. Coordination effective
  samples increase from about `34.4` at 1000 steps to about `97.3` at 3000
  steps.
- Full profile: 108 atoms, five replicas, `rc = 1.5`.
- Full potential-energy effective samples increase from about `34.9` at 3000
  steps to about `114.8` at 12000 steps.
- Full coordination-number effective samples increase from about `55.2` at
  3000 steps to about `368.1` at 12000 steps.
- Full coordination means remain near `12.30`, with checkpoint means
  `12.307`, `12.308`, and `12.292`.
- Full coordination conservative 95 percent half-widths are about `0.074`,
  `0.100`, and `0.115`. The interval does not shrink monotonically because
  the conservative review interval follows the largest uncertainty signal, not
  only the autocorrelation estimate.

Figure feedback:

- Reviewed
  `snapshots/post-06/trajectory_length_diagnostics_snapshot.png`.
- Reviewed
  `snapshots/post-06/trajectory_length_diagnostics_full_snapshot.png`.
- The full-profile snapshot shows the right-hand coordination axis, the
  `rc = 1.50` annotation, visible potential-energy and coordination
  checkpoint error bars, and no blocking label overlap or clipped panel text.
- The smoke-profile snapshot gives the same visual structure on shorter
  trajectories. The coordination error bars are visible and the fourth panel
  remains readable.

Website review status:

- The hidden website page has been updated in
  `../sungsoo-ahn.github.io/_pages/kups-md-post-06-trajectory-length.md`.
- `nav: false` remains set, so the page stays hidden from normal navigation
  and direct-link reachable only.
- Website commit `ff83d44c4ca14c562017557bcb00003e32a6fbfa` deployed in
  GitHub Actions run `29387640167`.
- Snapshot workflow run `29387756210` captured the deployed coordination
  refresh.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post06-coordination-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-coordination-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`;
  both returned HTTP 200 with page title
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post06-coordination-snapshots/post-06-desktop.png`
  (`1440 x 12217`) and
  `/tmp/kups-post06-coordination-snapshots/post-06-mobile.png`
  (`629 x 18508`).
- Live cache-busted HTML check returned HTTP 200 and contained
  `coordination number`, `coordination-number`, and `rc = 1.5`.

Rendered page feedback:

- Desktop capture renders the hidden Post 06 draft end to end with sidebar
  TOC, hidden-draft note, source links, controlled and argon diagnostic tables,
  display equation, refreshed four-panel figure, reproduction block, Practical
  Checklist, Current Status, references, and footer present.
- The refreshed figure is visible in the article body; the fourth panel shows
  the coordination axis and is not clipped.
- Mobile capture renders the long page through the mobile layout with title,
  hidden-draft note, tables, figure, caption, reproduction block, Current
  Status, references, and footer present. Tables and the figure are dense at
  mobile width but contained, with no blocking clipping or missing asset found
  in the inspected snapshot.

Final-release blockers:

- Run larger GPU kUPS trajectory-length diagnostics for physical observables
  before public indexing. The compact reduced-unit argon diagnostic now covers
  potential energy per atom and coordination number, but it is not a
  production GPU kUPS trajectory-length study.
- Add final citations for autocorrelation, effective sample size, blocking
  analysis, equilibration diagnostics, and physical-observable convergence.
- Re-run rendered desktop and mobile page snapshots after the production
  physical-observable figures and citations are added.
