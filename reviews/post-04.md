# Post 04 Review Notes

## Scope

- Post: 04
- Profiles reviewed: smoke and full
- Current status: controlled BAOAB Langevin thermostat diagnostic workflow plus
  a 256-atom, three-replica reduced-unit argon Langevin thermostat-to-NVE
  handoff diagnostic, committed smoke/full outputs, notebook, full-profile
  diagnostic figure, expanded hidden website draft, rendered page snapshots,
  and self-review artifact are in place.

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
- `uv run kups-tutorial export-site --profile full`
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
- The workflow now also includes a deterministic 256-atom argon Langevin
  diagnostic: reduced-unit Lennard-Jones argon FCC cells, seeded velocities,
  three independent velocity/noise replicas per thermostat case, vectorized
  minimum-image forces, BAOAB Langevin updates, and downsampled
  kinetic-temperature traces in `argon_langevin_samples.csv`.
- Each argon thermostat run now continues into a deterministic NVE handoff
  segment from the final thermostatted state. Downsampled handoff energy traces
  are committed in `argon_handoff_samples.csv`, and aggregate handoff drift
  metrics are recorded in `argon_langevin_protocol`.
- The output writer reuses computed argon trajectories for summaries and both
  CSV files. An initial full-profile run was interrupted after summary
  generation because the earlier writer recomputed the same many-body
  trajectories for each compact output.
- CSV writers now use Unix line endings so regenerated and exported result
  files pass `git diff --check`.
- The manifest records config hash, Git revision, Python/platform metadata, and
  ASE/kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 04.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating thermostat or plotting implementation details.

Open items:

- Replace or augment the CPU-fallback reduced-unit argon handoff check with a
  real CUDA/GPU kUPS production thermostat and NVE-handoff diagnostic before
  treating this post as final. The current argon run is a stronger many-body
  sanity check, not the target production MD experiment described in the plan.

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
- The full argon Langevin protocol contains 256 atoms at reduced density
  `0.65` and target temperature `0.70`, with 3 velocity/noise replicas for each
  thermostat coupling `gamma = 0.2`, `1.0`, and `4.0`.
- Across the 9 argon thermostat runs, the maximum absolute
  kinetic-temperature relative error is `5.86e-2`, and the mean absolute
  kinetic-temperature relative error is `2.43e-2`.
- Across the 9 post-thermostat NVE handoff runs, the maximum absolute
  normalized energy drift is `1.14e-5`, the mean absolute normalized drift is
  `5.02e-6`, the maximum relative energy error is `5.29e-5`, and no handoff run
  is marked unstable.
- The argon result supports a many-body thermostat-to-NVE handoff sanity check
  with initialization/noise sensitivity represented by replicas, but it is not
  a CUDA/GPU kUPS production thermostat benchmark and should not be described
  as final production evidence.

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
- Earlier compact argon pass: the first four-panel full-profile snapshot at
  `1728 x 1120` showed the argon kinetic-temperature traces clearly, but the
  title "Argon temperature remains controlled" overstated the weak-coupling
  trace, which sat below target in the compact run.
- Revised the argon panel title to "Argon thermostat temperature response",
  added a white legend frame, regenerated
  `snapshots/post-04/thermostat_diagnostics_full_snapshot.png`, and inspected
  the second pass. The revised figure no longer overclaims the compact argon
  result, the legend remains readable, and no panel labels or tick labels are
  clipped.
- New handoff pass: regenerated `figures/post-04/thermostat_diagnostics_full.svg`
  and `snapshots/post-04/thermostat_diagnostics_full_snapshot.png` after
  replacing the fourth panel with a 256-atom, three-replica NVE handoff drift
  bar chart. The snapshot is `1728 x 1120`; labels fit, the log-scale drift
  axis is readable, the replica error bars are visible, and the annotation
  naming 256 atoms, 3 replicas, and 1000 NVE steps does not cover the bars.
- The smoke snapshot `snapshots/post-04/thermostat_diagnostics_snapshot.png`
  is also `1728 x 1120`; it shows the smaller 32-atom, 2-replica smoke handoff
  panel. Labels and annotation remain readable, and the smoke/full distinction
  is clear from the atom/replica annotation.
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
- The notebook markdown now describes the 256-atom, three-replica argon
  thermostat-to-NVE handoff diagnostic and keeps the CPU-fallback/non-production
  limitation explicit.
- The notebook keeps the explanation focused on sampling and dynamics rather
  than becoming the implementation source.

Open items:

- Re-execute the notebook if the final article adds a kinetic-energy histogram,
  empirical CDF, or real CUDA/GPU kUPS production thermostat figure.

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
- GitHub Pages deploy `29369669516` built and deployed updated website commit
  `5761fc19fb122c4d381bbdc89da2ec36b8830004` successfully after adding the
  compact argon thermostat figure/prose refresh.
- GitHub Pages deploy `29384989661` built and deployed website commit
  `1635add74771cfbe02fc42e0d93ce59b1da8f716` successfully after adding the
  256-atom, three-replica thermostat-to-NVE handoff refresh.
- The deployed page snapshot manifest from workflow `29359320951` contains
  desktop and mobile captures for the hidden URL, both HTTP 200, with title
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.
- The deployed page snapshot manifest from workflow `29369851547` contains
  desktop and mobile captures for the updated hidden URL, both HTTP 200, with
  title `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.
- The deployed page snapshot manifest from workflow `29385110755` contains
  desktop and mobile captures for the handoff hidden URL, both HTTP 200, with
  title `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post04-expanded-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-expanded-snapshots/post-04-mobile.png`
- `/tmp/kups-post04-argon-thermostat-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-argon-thermostat-snapshots/post-04-mobile.png`
- `/tmp/kups-post04-handoff-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-handoff-snapshots/post-04-mobile.png`

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
- Updated desktop full-page capture at `1440 x 11564` renders the revised
  four-panel thermostat figure, caption, equations, multiple tables,
  reproduction block, current-status section, references, and footer. No
  missing figure, blank page, obvious clipped text, or broken page chrome was
  found in the inspected snapshot.
- Updated mobile full-page capture at `410 x 18232` renders the long title,
  hidden-draft note, equations, tables, revised figure, caption, code block,
  current-status list, references, and footer within the viewport. The
  four-panel figure is small at mobile width but contained; tables and code are
  narrow but not clipped.
- Handoff desktop capture at `1440 x 11724` renders the hidden draft end to end
  with sidebar TOC, equations, coupling and canonical-target tables, refreshed
  four-panel handoff figure, revised caption, reproduction block, Current
  Status section, references, and footer present. No missing figure, clipped
  table, blank page region, or broken page chrome was found.
- Handoff mobile capture at `410 x 18512` renders the long title, hidden-draft
  note, equations, tables, refreshed figure, caption, code block, Current
  Status section, references, and footer. Tables are dense but contained, and
  the figure is small at mobile width but not clipped.
- Live checks with cache-buster `?v=1635add` confirmed the direct hidden post
  contains `thermostat-to-NVE`/`NVE handoff` and `256-atom`; the hidden kUPS
  index links to Post 04; `/` and `/blog/` do not expose `kups-md-tutorials` or
  `post-04-thermostats`.

Open items:

- The page remains intentionally hidden from public navigation.
- Add a larger GPU kUPS production thermostat and NVE-handoff diagnostic before
  treating this post as final.

## Update 2026-07-15: Thermostat Runtime Provenance Gate

Commands added in this pass:

- `uv run ruff check src/kups_md_tutorials/provenance.py src/kups_md_tutorials/error_diagnostics.py src/kups_md_tutorials/thermostats.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py tests/test_provenance.py`
- `uv run python -m py_compile src/kups_md_tutorials/provenance.py src/kups_md_tutorials/error_diagnostics.py src/kups_md_tutorials/thermostats.py src/kups_md_tutorials/figures.py src/kups_md_tutorials/workflows.py`
- `uv run kups-tutorial run 04 --profile smoke`
- `uv run kups-tutorial verify 04 --profile smoke`
- `uv run kups-tutorial run 04 --profile full`
- `uv run kups-tutorial verify 04 --profile full`
- `uv run python scripts/generate_post04_figures.py`
- `uv run jupyter execute notebooks/post-04-thermostats.ipynb --inplace`
- `uv run pytest tests/test_provenance.py tests/test_config.py tests/test_cli.py tests/test_figures.py tests/test_notebooks.py -q`
- `python3 scripts/validate_kups_pages.py` in
  `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- `git diff --check` in `../sungsoo-ahn.github.io`

Code and reproducibility review:

- Shared provenance helpers now identify GPU-targeted configurations,
  GPU/non-GPU runtime strings, and the exact fallback blocking reason.
- `ArgonThermostatProtocolSummary` now records `runtime_device`,
  `target_requests_gpu`, `production_gpu_ready`, and `gpu_blocking_reason`.
- Post 04 verification now requires runtime-device provenance and requires a
  blocking reason whenever a GPU-targeted argon thermostat protocol falls back
  from GPU execution.
- The full profile still targets `cuda_or_cpu_fallback`, but the generated
  artifact records `runtime_device = jax:cpu;devices:cpu`,
  `production_gpu_ready = false`, and the blocking reason `target device
  requests CUDA/GPU, but generated artifact runtime was
  jax:cpu;devices:cpu`.
- The notebook now prints target device, runtime device, production GPU
  readiness, and GPU blocking reason next to the loaded full-profile summary.

Scientific review:

- The numerical thermostat and handoff metrics are unchanged by the provenance
  schema change. The full profile still reports 256 atoms, 3 replicas, maximum
  absolute kinetic-temperature relative error `5.86e-2`, maximum absolute NVE
  handoff normalized drift `1.14e-5`, maximum NVE handoff relative energy
  error `5.29e-5`, and zero unstable handoff runs.
- The new fields prevent the argon handoff panel from being mistaken for a
  completed GPU production thermostat benchmark. The current artifact is a
  CPU-fallback production-path diagnostic with explicit evidence for why the
  final GPU blocker remains.
- Local execution again reported that an NVIDIA GPU may be present, but a
  CUDA-enabled `jaxlib` is not installed, so JAX/kUPS fell back to CPU.

Figure feedback:

- Full-profile figure snapshot inspected:
  `snapshots/post-04/thermostat_diagnostics_full_snapshot.png`
  (`1728 x 1120`).
- Smoke-profile figure snapshot inspected:
  `snapshots/post-04/thermostat_diagnostics_snapshot.png`
  (`1728 x 1120`).
- Intended visual claim: the fourth panel should show a many-body
  thermostat-to-NVE handoff drift diagnostic while making clear that the
  artifact is CPU fallback, not a completed GPU production run.
- Full-profile feedback: the handoff annotation now includes `runtime: CPU
  fallback` below the 256-atom/3-replica/NVE-step text. The annotation remains
  in the upper-left, does not cover the drift bars or uncertainty bars, and
  the log-scale tick labels remain readable.
- Smoke-profile feedback: the same runtime label appears for the 32-atom,
  2-replica handoff panel. The annotation is contained, and the two smoke bars
  and uncertainty bars remain visible.
- Revision decision: no additional figure edit was needed after adding the
  runtime label and inspecting both snapshots.

Website review status:

- Complete for this pass. Tutorial commit
  `ff0df9deae3cde52ae647e7e88e862839046f16e` was exported to the website and
  deployed as website commit `b4f424f`.
- GitHub Pages deploy `29391896848` succeeded for the hidden post 04 refresh.
- GitHub Actions snapshot workflow `29392014572` captured the deployed hidden
  page. The artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post04-runtime-provenance-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/manifest.json`.
  It contains desktop and mobile captures for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`, both
  HTTP 200, with title
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Rendered snapshots reviewed:

- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-desktop.png`
  (`1440 x 12111`).
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-mobile.png`
  (`410 x 19022`).
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-desktop-runtime-table-crop.png`.
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-desktop-figure-crop.png`.
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-desktop-status-check-2.png`.
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-mobile-runtime-table-check-2.png`.
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-mobile-figure-crop.png`.
- `/tmp/kups-post04-runtime-provenance-snapshots/kups-md-page-snapshots/post-04-mobile-status-check-3.png`.

Rendered feedback:

- Desktop capture renders the hidden draft end to end with sidebar table of
  contents, the new runtime-device/GPU-readiness table, refreshed diagnostic
  figure, reproduction block, Current Status section, references, and footer
  present. No missing figure, clipped table, blank region, or broken page
  chrome was found in the inspected snapshot.
- Desktop runtime-table crop shows `cuda_or_cpu_fallback`,
  `jax:cpu;devices:cpu`, `false`, and the blocking reason in a readable table.
  The crop cuts below the final row, but the full-page capture confirms the
  table remains in the content column.
- Desktop figure crop shows the embedded four-panel figure with the `runtime:
  CPU fallback` label in the handoff panel and the revised caption naming a
  CPU-fallback handoff protocol. The label is small but readable and does not
  cover the bars or uncertainty bars.
- Mobile runtime-table crop confirms the long blocking reason wraps inside the
  table rather than overflowing the viewport.
- Mobile figure crop shows the figure contained within the article column. The
  figure text is small at mobile width, but the caption and adjacent prose
  explicitly carry the CPU-fallback limitation.
- Mobile Current Status crop confirms the implemented-list item for
  machine-readable target-device, runtime-device, GPU-readiness, and blocking
  reason provenance, plus the remaining-list item for a larger GPU kUPS
  production thermostat/NVE-handoff diagnostic.
- Live cache-busted checks on
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/?v=b4f424f`
  confirmed the deployed HTML contains `production GPU ready`,
  `runtime device`, `jax:cpu;devices:cpu`, `CPU fallback`,
  `cuda_or_cpu_fallback`, and `machine-readable`.
- Live checks of `/` and `/blog/` found no `kups-md-tutorials` or
  `post-04-thermostats` links, so the page remains direct-link reachable and
  hidden from public navigation.

Blocking items for current hidden draft:

- None. The hidden draft explicitly states the CPU-fallback status.

Non-blocking items accepted until final article pass:

- Mobile figure/table density remains accepted for the hidden draft.
- The reduced-unit LJ thermostat handoff protocol remains a teaching
  diagnostic rather than a final GPU production study.

Final-release blockers:

- Run and review the real CUDA/GPU kUPS production thermostat and NVE-handoff
  diagnostic before public indexing.
- Re-run rendered desktop/mobile snapshots after the production GPU thermostat
  diagnostic or any public-indexing change.

## Citation Backlink Refresh 2026-07-15

Scope and provenance:

- Website commit reviewed: `d244d57`.
- Website deploy run: `29413487745`.
- Snapshot workflow: `29413685814`.
- Snapshot artifact downloaded to `/tmp/kups-citation-backlinks-snapshots/`.
- Live cache-busted HTML checked with `?v=d244d57`.

Website and prose review:

- Added BAOAB stochastic-splitting context with a Leimkuhler/Matthews citation.
- Added thermostat-family context with Bussi/Donadio/Parrinello and Tuckerman
  citations.
- Added matching `ref-*` anchors and reverse backlinks in `## References`.
- Live HTML contains the new `cite-*`, `ref-*`, and `href="#cite-*"` backlink
  anchors for all three references.
- Live `/` and `/blog/` checks found no `kups-md-tutorials` or
  `post-04-thermostats` links, so the page remains direct-link only.

Rendered snapshots reviewed:

- `/tmp/kups-citation-backlinks-snapshots/post-04-desktop.png`
  (`1440 x 12207`).
- `/tmp/kups-citation-backlinks-snapshots/post-04-mobile.png`
  (`410 x 19214`).

Rendered feedback:

- Desktop capture shows the added thermostat citations in context; tables,
  figure, code block, references, and footer remain contained.
- Mobile capture keeps the edited paragraphs, dense tables, figure, current
  status, and References section within the article width. Backlink markers are
  readable at the bottom.
- No figure asset changed, so no new figure snapshot was required.

Revision decision:

- Accepted for the hidden draft citation-backlink pass.
