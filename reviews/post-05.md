# Post 05 Review Notes

## Scope

- Post: 05
- Profiles reviewed: smoke and full
- Current status: controlled scalar-volume pressure/cell diagnostic workflow,
  compact reduced-unit argon cell-response workflow, committed smoke/full
  outputs, notebook, full-profile diagnostic figure, expanded hidden website
  draft, rendered page snapshots, and self-review artifact are in place; the
  final dynamic argon/kUPS NPT diagnostic is still pending.

## Commands

- `uv run kups-tutorial run 05 --profile smoke`
- `uv run kups-tutorial verify 05 --profile smoke`
- `uv run kups-tutorial run 05 --profile full`
- `uv run kups-tutorial verify 05 --profile full`
- `uv run python scripts/generate_post05_figures.py`
- `uv run jupyter execute notebooks/post-05-barostats.ipynb --inplace`
- `uv run ruff check .`
- `uv run pytest tests/test_config.py tests/test_cli.py tests/test_figures.py -q`
- `uv run kups-tutorial verify-artifacts`
- `git diff --check`
- `python3 scripts/validate_kups_pages.py` in `../sungsoo-ahn.github.io`
- `python3 scripts/validate_blog.py` in `../sungsoo-ahn.github.io`
- GitHub Actions deploy run `29360083501` for website commit
  `13ea87083b474465450efdcc503a0fdee06c6e6e`
- GitHub Actions snapshot run `29360274825`
- GitHub Actions tutorial verification run `29370738271` for tutorial commit
  `1e4d7724b5dabdeffab5406156e34bb744f67bff`
- GitHub Actions deploy run `29370738331` for website commit
  `943dde4d9094385516588f7c831dbf8512c3919f`
- GitHub Actions snapshot run `29370897946`
- `uv run kups-tutorial verify-reviews`

## Code And Reproducibility Review

- Configs are committed under `configs/post-05/`.
- Smoke and full outputs are committed under `results/post-05/`.
- The workflow uses a deterministic scalar-volume Ornstein-Uhlenbeck model with
  known NPT-like volume and pressure fluctuation targets.
- The workflow now also writes `argon_cell_response.csv`, a deterministic
  reduced-unit FCC argon pressure-volume sweep using affine box scaling,
  minimum-image periodic boundaries, and the Lennard-Jones virial pressure.
- The manifest records config hash, Git revision, Python/platform metadata, and
  kUPS/NumPy versions.
- `kups-tutorial run`, `verify`, and `run-all` include post 05.
- The notebook imports reusable logic from `src/kups_md_tutorials/` rather than
  duplicating barostat or plotting implementation details.

Open items:

- Add a dynamic argon/kUPS NPT diagnostic before treating this post as final.
  The current scalar model isolates fluctuation and memory concepts, and the
  compact argon sweep checks real coordinates/cell scaling, but it does not yet
  exercise moving-cell MD sampling.

## Scientific Review

- The full profile compares scalar barostat relaxation times `0.5`, `2.0`, and
  `8.0` at target pressure `1.0`, volume `1000`, compressibility `0.01`, and
  `kT = 1`.
- Full-profile volume and pressure variance estimates are within about 15% of
  the analytical targets.
- Volume autocorrelation time increases from about `2.0` for the fast barostat
  to about `22.5` for the slow barostat, supporting the claim that barostat
  time constants change memory and effective sampling.
- The compact full-profile argon response uses 108 atoms, reference reduced
  density `1.0`, volume factors `0.90` through `1.10`, fitted reduced-unit bulk
  response about `42.1`, and pressure span about `8.7`. The pressure decreases
  with expansion, so the virial sign and affine scaling are qualitatively
  consistent for this wiring check.
- The smoke profile uses fewer samples; verification tolerances are deliberately
  wider for fluctuation variance than for the full scientific review.

Open items:

- The website prose should not imply that pressure itself is tightly controlled
  instant by instant. Pressure fluctuations are the signal in small-system NPT.
- The final article should discuss isotropic versus flexible-cell coupling and
  finite-size effects using a dynamic argon/kUPS NPT workflow.

## Figure Snapshot Review

Snapshot reviewed:

- `snapshots/post-05/barostat_diagnostics_snapshot.png`
- `snapshots/post-05/barostat_diagnostics_full_snapshot.png`

Feedback loop:

- First full-profile pass: labels are readable, target lines are visible in the
  volume and pressure panels, and the autocorrelation panel clearly increases
  with relaxation time.
- Compact argon cell-response refresh: the fourth panel is visible in the
  full-profile snapshot, the `V / V0` axis and reduced pressure labels fit, the
  pressure-volume trend is clear, and the `Kfit = 42.13`, `N = 108` annotation
  does not obscure the interpretation.
- The figure does not yet show dynamic NPT density relaxation or
  anisotropic/flexible-cell behavior. That is acceptable for this draft, but
  the final post should add a production cell-dynamics diagnostic if
  flexible-cell claims are made.

Open items:

- Add a production-cell dynamics figure after argon/kUPS NPT diagnostics are
  implemented.

## Notebook Review

- `notebooks/post-05-barostats.ipynb` executes from a clean kernel.
- The notebook loads both smoke and full configurations, displays committed
  outputs, reports the compact argon response summary, and regenerates the
  full-profile diagnostic figure from committed result files.
- The notebook keeps the explanation focused on pressure fluctuations and cell
  memory rather than becoming the implementation source.

Open items:

- Add citations for NPT ensemble fluctuations, compressibility relations,
  barostat coupling, and finite-size pressure fluctuations before final
  publication.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post05_barostat_diagnostics.svg`.
- Expanded the hidden page from the short draft to about 3,606 words. The
  expanded prose explains pressure fluctuations, scalar-volume NPT-like
  diagnostics, barostat relaxation time, effective samples, initialization
  before NPT, cell-degree choices, thermostat/barostat interaction, and the
  compact atomistic argon cell-response check.
- The expanded prose keeps the scope clear: the committed result is a
  controlled scalar diagnostic plus a static argon pressure-volume sweep, not a
  final production NPT workflow with moving cell degrees of freedom.
- `python3 scripts/validate_kups_pages.py` passes in the website repository.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.
- `git diff --check` passes in the website repository.
- Website deploy run `29360083501` succeeded for commit
  `13ea87083b474465450efdcc503a0fdee06c6e6e`.
- Snapshot workflow run `29360274825` captured the expanded hidden page.
- Snapshot workflow run `29370897946` captured the compact argon cell-response
  refresh for website commit `943dde4d9094385516588f7c831dbf8512c3919f`.
- Snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post05-expanded-snapshots/`.
- Refreshed snapshot artifact `kups-md-page-snapshots` was downloaded to
  `/tmp/kups-post05-argon-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-expanded-snapshots/manifest.json`.
- Refreshed manifest reviewed:
  `/tmp/kups-post05-argon-cell-snapshots/manifest.json`.
- Manifest coverage: desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`; both
  returned HTTP 200 with page title
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.
- Rendered snapshots visually inspected:
  `/tmp/kups-post05-expanded-snapshots/post-05-desktop.png` and
  `/tmp/kups-post05-expanded-snapshots/post-05-mobile.png`.
- Refreshed rendered snapshots visually inspected:
  `/tmp/kups-post05-argon-cell-snapshots/post-05-desktop.png` and
  `/tmp/kups-post05-argon-cell-snapshots/post-05-mobile.png`.

Rendered page feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-page note, source links, several tables, full-profile
  barostat figure, reproduction code block, current-status section, references,
  and footer present. No blank page, missing figure, obvious clipping, or broken
  page chrome was found in the inspected snapshot.
- Mobile capture renders the same content through the mobile layout with the
  title, navigation, author note, tables, figure, code block, current-status
  section, and references present. Tables are tight but readable and are not
  clipped in the inspected snapshot.
- Refreshed desktop capture renders the compact argon cell-response article
  end to end with the updated four-panel figure, the argon configuration table,
  the reproduction command, current-status section, and references visible. No
  blank page, missing figure, obvious clipping, or broken page chrome was found
  in the inspected snapshot.
- Refreshed mobile capture renders the updated page with the four-panel figure
  present and legible. The narrow left navigation and tables are tight, as in
  earlier captures, but no blocking clipping or missing asset was found in the
  inspected snapshot.

Open items:

- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Add the dynamic argon/kUPS NPT diagnostic with moving cell degrees of freedom
  before treating this post as final.
- Re-run the page snapshot workflow again after the final production-cell
  figure and citations are added.
