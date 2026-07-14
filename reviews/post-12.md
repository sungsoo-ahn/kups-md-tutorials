# Post 12 Review Notes

## Scope And Provenance

- Post: 12
- Profiles reviewed: smoke and full
- Current status: controlled MLIP reliability workflow, compact smoke/full
  outputs, notebook, full-profile diagnostic figure, figure snapshots, and this
  self-review artifact are in place; the hidden website draft is in place.
- Working-tree state: post 12 implementation is uncommitted during this review
  pass.
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

## Code And Reproducibility Review

- Configs are committed-intended under `configs/post-12/`.
- Smoke and full outputs are committed-intended under `results/post-12/`.
- The workflow is deterministic and CPU-friendly. It records configured MACE
  artifact metadata but uses a surrogate MLIP reliability diagnostic until the
  final GPU/model-artifact pass freezes an actual downloaded hash.
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

- Capture rendered desktop and mobile page snapshots after the hidden draft
  deploys.
- Replace placeholder model artifact metadata with the final pinned MACE
  revision and verified hash during the GPU/final article pass.

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

- The final article should clearly label the current workflow as a deterministic
  surrogate diagnostic, not a completed MACE/fcc-Al GPU production run.
- The final pass must pin an actual MACE artifact revision, verify its hash,
  and record the GPU environment.
- The final article should connect the MLIP checks to each earlier tutorial:
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
- The artifact metadata annotation fits, but it intentionally exposes the
  placeholder revision/hash. This must be revised after the final model
  artifact is pinned.
- No label clipping, unreadable ticks, or legend overlap was found in the
  inspected full-profile snapshot.

Open items:

- Recheck figure readability inside the rendered hidden webpage at desktop and
  mobile widths.
- Regenerate and re-review after the real MACE artifact metadata and GPU
  production diagnostics are added.

## Notebook Review

- `notebooks/post-12-mlip-capstone.ipynb` loads smoke and full configurations,
  prints committed full-summary diagnostics and artifact metadata, and
  regenerates the full-profile MLIP figure from committed result files.
- `uv run jupyter execute notebooks/post-12-mlip-capstone.ipynb --inplace`
  passes and saves executed outputs.

## Website Draft Review

- Added a hidden draft page in `../sungsoo-ahn.github.io` at
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`.
- The page uses the website `post` layout, `nav: false`, the shared
  `kups-md-tutorials` series metadata, and links back to the executable config,
  notebook, smoke/full summaries, full manifest, and review note.
- Copied the reviewed full-profile SVG figure to
  `assets/img/blog/kups_md_post12_mlip_diagnostics.svg`.
- `python3 scripts/validate_blog.py` passes with pre-existing unused-image
  warnings in the website repository.

Open items:

- Verify the deployed hidden page after the website commit is pushed.
- Confirm that the page is directly reachable but not linked from public
  navigation.
- Capture and inspect rendered desktop and mobile snapshots for this hidden
  page.

## Prose And Style Review

- The planned website draft should follow the blog-native post layout with
  `nav: false`, shared `kups-md-tutorials` series metadata, an author-note
  paragraph, compact reproduction commands, and links to configs, notebook,
  summaries, manifest, figure source, and this review note.
- The prose should be concept-led for MLIP-aware ML researchers: static
  validation is not deployment validation; MD exposes extrapolation, drift,
  ensemble instability, and biased free-energy claims.

## Open Items

Blocking items for the current hidden draft:

- Verify the deployed hidden URL after the website commit is pushed.
- Confirm that public navigation does not link to the hidden page.

Non-blocking items accepted until the final article pass:

- Rendered page snapshots are still pending.
- The draft will remain short and explicitly non-final.
- The model artifact metadata is a placeholder in the hidden draft.

Final-release blockers:

- Run and review the real MACE/fcc-Al GPU capstone.
- Pin the MACE repository revision and verify the downloaded artifact hash.
- Expand the prose to a full article with citations and production diagnostics.
- Resolve rendered desktop/mobile page snapshot feedback.
