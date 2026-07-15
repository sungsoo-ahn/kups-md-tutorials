# Rendered Page Snapshot Review

## Scope and Provenance

- Date: 2026-07-14.
- Scope: hidden kUPS MD tutorial pages in `../sungsoo-ahn.github.io`.
- Pages: posts 01-12 under `/kups-md-tutorials/post-XX-.../`.
- Capture tool added: `../sungsoo-ahn.github.io/scripts/capture_kups_snapshots.js`.
- Intended output directory: `snapshots/pages/` in this repository.
- Website state reviewed: hidden draft pages are direct-link reachable and not
  indexed from the homepage or blog listing.

## Required Snapshot Command

From `../sungsoo-ahn.github.io`:

```bash
node scripts/capture_kups_snapshots.js \
  --posts 01,02,03,04,05,06,07,08,09,10,11,12 \
  --output-dir ../kups-md-tutorials/snapshots/pages \
  --base-url https://sungsoo-ahn.github.io
```

The script captures:

- desktop viewport: 1440 by 1200 px, full page;
- mobile viewport: 390 by 1200 px, full page;
- one `manifest.json` recording URL, status, title, post number, and viewport.

## Current Attempt

Command attempted from `../sungsoo-ahn.github.io`:

```bash
node scripts/capture_kups_snapshots.js --posts 12 --output-dir snapshots/kups-md-pages
```

Result: blocked before page rendering. Playwright could start the capture flow
but Chromium could not launch because the host is missing required Linux browser
libraries.

The suggested dependency command failed in this environment:

```bash
sudo npx playwright install-deps
```

Reason: sudo requires a password and this session has no interactive sudo
access. Direct `apt-get update` also failed with permission denied on the apt
lock. No local fallback renderer was available: `chromium`, `google-chrome`,
`firefox`, `wkhtmltoimage`, and `cutycapt` were not installed.

## Feedback Status

- Desktop page snapshot feedback: not yet captured.
- Mobile page snapshot feedback: not yet captured.
- Blocking issue for current hidden drafts: none from the absence of public
  indexing; hidden status is intentional.
- Final-release blocker: capture desktop and mobile rendered snapshots for all
  twelve posts, inspect layout and readability, record concrete feedback, revise
  pages or figures as needed, and rerun the capture.

## Unblock Instructions

On a machine with sudo or browser dependencies already installed:

```bash
cd ../sungsoo-ahn.github.io
npm install
npx playwright install chromium
sudo npx playwright install-deps
node scripts/capture_kups_snapshots.js \
  --posts 01,02,03,04,05,06,07,08,09,10,11,12 \
  --output-dir ../kups-md-tutorials/snapshots/pages \
  --base-url https://sungsoo-ahn.github.io
```

If using a local Jekyll build instead of the deployed site, start Jekyll and
replace `--base-url` with the local server URL.

## CI Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29354941319`.
- Website commit: `ca3ba0b9fac267aaf382c063a64adcbfa69aced0`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-page-snapshots/`.
- Manifest reviewed: `/tmp/kups-page-snapshots/manifest.json`.
- Capture command used by workflow:

```bash
node scripts/capture_kups_snapshots.js \
  --base-url "https://sungsoo-ahn.github.io" \
  --posts "01,02,03,04,05,06,07,08,09,10,11,12" \
  --output-dir snapshots/kups-md-pages
```

Manifest coverage:

- 24 rendered snapshots captured.
- 12 desktop snapshots and 12 mobile snapshots.
- All twelve posts have both viewports.
- All captured URLs returned HTTP 200.
- First URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`.
- Last URL:
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`.

Snapshots visually inspected in this pass:

- `/tmp/kups-page-snapshots/post-01-desktop.png`
- `/tmp/kups-page-snapshots/post-01-mobile.png`
- `/tmp/kups-page-snapshots/post-12-desktop.png`
- `/tmp/kups-page-snapshots/post-12-mobile.png`

Feedback:

- Post 01 desktop renders the hidden page with the expected blog chrome,
  sidebar table of contents, title, author note, equation, provenance links,
  initialization table, full-profile figure, reproduction code block, current
  status, and references. No blank-page, missing-image, or obvious clipping
  issue was found in the inspected full-page capture.
- Post 01 mobile renders the same content through the mobile navigation. The
  initialization table and reproduction code block are narrow, but they remain
  readable and are not clipped in the inspected snapshot. Keep this as a final
  article polish item because longer final prose may change wrapping.
- Post 12 desktop renders the capstone table, figure, reproduction code block,
  current-status section, and references without visible clipping or missing
  assets in the inspected full-page capture.
- Post 12 mobile renders the long title, author note, capstone table, MLIP
  diagnostic figure, code block, and references without clipping. The title
  wraps heavily but remains readable.

Revision decisions:

- No blocking layout issue was found in the inspected sample snapshots.
- The hidden draft pages can remain direct-link reachable and hidden from public
  navigation while content matures.
- Final-release blocker remains: inspect all 24 captured snapshots, not only
  the representative samples above, after the full prose and final figures are
  in place.
- Final article polish item: recheck mobile table/code wrapping after posts are
  expanded to full length.

## Expanded Post 01 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29356548516`.
- Website commit: `6534a212ddd9baa6403c57558b19c9b6daab8d15`.
- Deploy run for that commit: `29356354203`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post01-final-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post01-final-snapshots/manifest.json`.
- Capture scope: post 01 only, after expansion to about 3,765 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-01-initialization/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do You Initialize an MD Simulation Without Biasing the Result? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post01-final-snapshots/post-01-desktop.png`
- `/tmp/kups-post01-final-snapshots/post-01-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, equations, two tables, figure, reproduction code blocks,
  current-status section, references, and footer present. No blank page,
  missing figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, author note, section headings, equations, figure, code blocks,
  current-status section, references, and footer present. The initialization
  and minimization/warmup tables are narrow but remain readable and are not
  clipped in the inspected snapshot.
- The final capture was taken after replacing inline `\(...\)` notation with
  plain notation in prose where the deployed Jekyll stack rendered inline math
  delimiters as ordinary parentheses.

Revision decisions:

- No blocking layout issue was found for the expanded post 01 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 02 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29357589065`.
- Website commit: `53af3daa4dae1c5508ff143ee9fddf490634e86e`.
- Deploy run for that commit: `29357398623`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post02-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post02-expanded-snapshots/manifest.json`.
- Capture scope: post 02 only, after expansion to about 3,633 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-02-integrators/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Does an MD Integrator Actually Approximate? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post02-expanded-snapshots/post-02-desktop.png`
- `/tmp/kups-post02-expanded-snapshots/post-02-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, display equations, harmonic-oscillator configuration table,
  diagnostic figure, methods-practice table, reproduction code block,
  current-status section, references, and footer present. No blank page,
  missing figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, author note, equations, figure, code block, current-status section,
  references, and footer present. The methods-practice table is tight but
  readable and is not clipped in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 02 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 03 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29358450830`.
- Website commit: `ebf717a523ff21f9475abc6e04515db8e98e13e4`.
- Deploy run for that commit: `29358250043`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post03-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post03-expanded-snapshots/manifest.json`.
- Capture scope: post 03 only, after expansion to about 3,703 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post03-expanded-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-expanded-snapshots/post-03-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, mechanism table, diagnostic figure, timestep-choice table,
  reproduction code block, current-status section, references, and footer
  present. No blank page, missing figure, obvious text clipping, or broken page
  chrome was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, author note, tables, figure, code block, current-status section,
  references, and footer present. The two tables are tight but readable and are
  not clipped in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 03 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The argon/kUPS NVE diagnostic remains a final-release blocker for post 03.
- The page remains hidden from public navigation and direct-link reachable.

## Post 03 Runtime Provenance Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29390961441`.
- Tutorial commit:
  `b0ed74d482a449d3064c7602c8f310d4c6696fc5`.
- Website commit: `29827b0`.
- Deploy run for that commit: `29390809533`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post03-runtime-provenance-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/manifest.json`.
- Capture scope: post 03 only, after adding runtime-device and GPU-readiness
  provenance to the NVE diagnostic summary and hidden article.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/post-03-desktop.png`
  (`1440 x 11678`).
- `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/post-03-mobile.png`
  (`461 x 18612`).
- `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/post-03-figure-crop.png`.
- `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/post-03-mobile-figure-crop.png`.
- `/tmp/kups-post03-runtime-provenance-snapshots/kups-md-page-snapshots/post-03-mobile-status-check-1.png`.

Feedback:

- Desktop capture renders the hidden draft end to end with sidebar table of
  contents, runtime-device table rows, diagnostic figure, reproduction block,
  Current Status section, references, and footer present. No blank page,
  missing figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Desktop figure crop shows the NVE panel legend label `runtime: CPU fallback`
  without clipping or hiding the drift traces.
- Mobile capture renders the long article, figure, status lists, references,
  and footer within the viewport. The runtime label is small at mobile width
  but visible, and the nearby prose explicitly states that the artifact is a
  CPU-fallback run rather than a completed GPU production run.
- Mobile status crop confirms the page lists runtime-device/GPU-readiness
  provenance as implemented and the real CUDA/GPU kUPS production NVE
  diagnostic as remaining work.
- Live cache-busted checks on the hidden post confirmed the deployed HTML
  contains `production_gpu_ready`, `runtime_device`, `jax:cpu;devices:cpu`,
  `CPU fallback`, and `CUDA/GPU`.
- Live checks of `/` and `/blog/` found no `kups-md-tutorials` or
  `post-03-errors` links.

Revision decisions:

- No blocking layout issue was found for the runtime-provenance hidden draft.
- The hidden post remains direct-link reachable and absent from public
  homepage/blog navigation.
- Real CUDA/GPU kUPS production NVE remains a final-release blocker for post
  03.

## Expanded Post 04 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29359320951`.
- Website commit: `7aa89addc2ee2fa2e334bdc2f2b9a38fecb22a07`.
- Deploy run for that commit: `29359119367`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post04-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post04-expanded-snapshots/manifest.json`.
- Capture scope: post 04 only, after expansion to about 3,630 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post04-expanded-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-expanded-snapshots/post-04-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, equations, multiple tables, thermostat diagnostic figure,
  reproduction code block, current-status section, references, and footer
  present. No blank page, missing figure, obvious text clipping, or broken page
  chrome was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, author note, equations, tables, figure, code block, current-status
  section, references, and footer present. The tables are tight but readable
  and are not clipped in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 04 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The argon/kUPS thermostat diagnostic remains a final-release blocker for post
  04.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 05 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29360274825`.
- Website commit: `13ea87083b474465450efdcc503a0fdee06c6e6e`.
- Deploy run for that commit: `29360083501`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post05-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-expanded-snapshots/manifest.json`.
- Capture scope: post 05 only, after expansion to about 3,606 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post05-expanded-snapshots/post-05-desktop.png`
- `/tmp/kups-post05-expanded-snapshots/post-05-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, scalar NPT-like diagnostic tables,
  full-profile barostat figure, reproduction code block, practical checklist,
  current-status section, references, and footer present. No blank page, missing
  figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, navigation, hidden-draft note, tables, figure, code block,
  current-status section, and references present. The tables are tight but
  readable and are not clipped in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 05 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The argon/kUPS NPT diagnostic with actual cell degrees of freedom remains a
  final-release blocker for post 05.
- The page remains hidden from public navigation and direct-link reachable.

## Post 05 Compact Argon Cell Response Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29370897946`.
- Website commit: `943dde4d9094385516588f7c831dbf8512c3919f`.
- Deploy run for that commit: `29370738331`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post05-argon-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-argon-cell-snapshots/manifest.json`.
- Capture scope: post 05 only, after adding the compact reduced-unit argon
  cell-response panel and website prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post05-argon-cell-snapshots/post-05-desktop.png`
- `/tmp/kups-post05-argon-cell-snapshots/post-05-mobile.png`

Feedback:

- Desktop capture renders the updated article end to end with the hidden-draft
  note, source links, scalar barostat tables, compact argon configuration
  table, four-panel full-profile figure, reproduction code block, practical
  checklist, current-status section, references, and footer present. No blank
  page, missing figure, obvious text clipping, or broken page chrome was found
  in the inspected snapshot.
- Mobile capture renders the updated article with the four-panel figure visible
  and legible. The narrow left navigation and tables are tight, consistent with
  prior hidden-page captures, but no blocking clipping or missing asset was
  found in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the compact argon cell-response
  refresh.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Dynamic argon/kUPS NPT sampling with moving cell degrees of freedom remains a
  final-release blocker for post 05.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 06 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29361099780`.
- Website commit: `aac0e52f2cbfc388afc884073e36172cd26e4c9e`.
- Deploy run for that commit: `29360919260`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post06-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-expanded-snapshots/manifest.json`.
- Capture scope: post 06 only, after expansion to about 3,534 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post06-expanded-snapshots/post-06-desktop.png`
- `/tmp/kups-post06-expanded-snapshots/post-06-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, trajectory-length diagnostic
  tables, display equation, full-profile figure, reproduction code block,
  practical checklist, current-status section, references, and footer present.
  No blank page, missing figure, obvious text clipping, or broken page chrome
  was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, navigation, hidden-draft note, tables, equation, figure, code block,
  current-status section, and references present. The tables are tight but
  readable and are not clipped in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 06 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- The argon/kUPS physical-observable trajectory-length diagnostic remains a
  final-release blocker for post 06.
- The page remains hidden from public navigation and direct-link reachable.

## Post 06 Compact Argon Observable Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29372062650`.
- Website commit: `9260ea3910a111ff76adbd8b837fa7938b9314b6`.
- Deploy run for that commit: `29371909883`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post06-argon-observable-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-argon-observable-snapshots/manifest.json`.
- Capture scope: post 06 only, after adding the compact reduced-unit argon
  potential-energy-per-atom panel and website prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post06-argon-observable-snapshots/post-06-desktop.png`
- `/tmp/kups-post06-argon-observable-snapshots/post-06-mobile.png`

Feedback:

- Desktop capture renders the updated article end to end with the hidden-draft
  note, source links, controlled and argon diagnostic tables, four-panel
  full-profile figure, reproduction code block, practical checklist,
  current-status section, references, and footer present. No blank page,
  missing figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the updated article with the four-panel figure visible
  and the argon panel present. The narrow left navigation and tables are tight,
  consistent with prior hidden-page captures, but no blocking clipping or
  missing asset was found in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the compact argon observable refresh.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Larger GPU kUPS trajectory-length diagnostics for physical observables remain
  a final-release blocker for post 06.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 07 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29361900585`.
- Website commit: `2ae2434e4933fde7fe3f2241e18be00af913d159`.
- Deploy run for that commit: `29361737064`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post07-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-expanded-snapshots/manifest.json`.
- Capture scope: post 07 only, after expansion to about 3,528 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post07-expanded-snapshots/post-07-desktop.png`
- `/tmp/kups-post07-expanded-snapshots/post-07-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, observable-estimator tables,
  display equation, full-profile RDF/coordination/VACF figure, reproduction
  code block, practical checklist, current-status section, references, and
  footer present. No blank page, missing figure, obvious text clipping, or
  broken page chrome was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, navigation, hidden-draft note, tables, equation, figure, code block,
  current-status section, and references present. The title wraps heavily but
  remains readable; tables and code block remain within the page.

Revision decisions:

- No blocking layout issue was found for the expanded post 07 hidden draft.
- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- The argon/kUPS production trajectory-observable diagnostic remains a
  final-release blocker for post 07.
- The page remains hidden from public navigation and direct-link reachable.

## Post 07 Compact Argon Trajectory Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29373158618`.
- Website commit: `184a54fd81c3b4a38fe659839ee9427666d46324`.
- Deploy run for that commit: `29372999672`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post07-argon-trajectory-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-argon-trajectory-snapshots/manifest.json`.
- Capture scope: post 07 only, after adding the compact reduced-unit argon
  trajectory observable workflow and four-panel diagnostic figure.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post07-argon-trajectory-snapshots/post-07-desktop.png`
- `/tmp/kups-post07-argon-trajectory-snapshots/post-07-mobile.png`

Feedback:

- Desktop capture renders the refreshed hidden article end to end with sidebar
  table of contents, source links, compact trajectory table, full-profile
  four-panel diagnostic figure, reproduction code block, current-status
  section, references, and footer present. The trajectory RDF panel is visible
  in the figure and no blank page, missing asset, obvious text clipping, or
  broken page chrome was found in the inspected snapshot.
- Mobile capture renders the updated article through the mobile layout with
  the title, compact trajectory table, four-panel figure, code block,
  current-status section, and references present. The figure is necessarily
  dense on mobile, but it scales within the page and the caption/prose make the
  trajectory RDF panel identifiable.

Revision decisions:

- No blocking layout issue was found for the compact argon trajectory refresh.
- Keep mobile figure readability and table wrapping as final typography-polish
  items after the rest of the article content is final.
- Larger GPU kUPS production trajectory observables remain a final-release
  blocker for post 07.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 08 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29362752198`.
- Website commit: `80f1adec082720e3db395ff0c078c166fe3113f7`.
- Deploy run for that commit: `29362569505`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post08-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-expanded-snapshots/manifest.json`.
- Capture scope: post 08 only, after expansion to about 3,501 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post08-expanded-snapshots/post-08-desktop.png`
- `/tmp/kups-post08-expanded-snapshots/post-08-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, PMF diagnostic tables, display
  equations, full-profile free-energy figure, reproduction code block,
  practical checklist, current-status section, references, and footer present.
  No blank page, missing figure, obvious text clipping, or broken page chrome
  was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, navigation, hidden-draft note, tables, display equations, figure, code
  block, current-status section, and references present. The title wraps but
  remains readable; tables are tight but contained.

Revision decisions:

- No blocking layout issue was found for the expanded post 08 hidden draft.
- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- The argon/kUPS RDF-derived PMF diagnostic linked back to post 07 remains a
  final-release blocker for post 08.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 09 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29363609573`.
- Website commit: `4c32e635190a3aa15f270c6c04cfb3c8dc06bdb0`.
- Deploy run for that commit: `29363423337`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post09-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-expanded-snapshots/manifest.json`.
- Capture scope: post 09 only, after expansion to about 3,503 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post09-expanded-snapshots/post-09-desktop.png`
- `/tmp/kups-post09-expanded-snapshots/post-09-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, estimator/ESS tables,
  full-profile estimator figure, reproduction code block, practical checklist,
  current-status section, references, and footer present. No blank page, missing
  figure, obvious text clipping, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, navigation, hidden-draft note, tables, figure, code block,
  current-status section, and references present. The tables are tight but
  contained, and the figure remains readable.

Revision decisions:

- No blocking layout issue was found for the expanded post 09 hidden draft.
- Keep mobile table wrapping as a final typography-polish item after the rest
  of the articles are expanded.
- Any final MBAR/WHAM production figure remains a final-release blocker for
  post 09 until implemented and snapshot-reviewed.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 10 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29364628807`.
- Website commit: `82e9508717fe8a8e826eaae040949e3fa8b18fe7`.
- Deploy run for that commit: `29364446798`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post10-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post10-expanded-snapshots/manifest.json`.
- Capture scope: post 10 only, after expansion to about 3,602 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Does Umbrella Sampling Actually Sample? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post10-expanded-snapshots/post-10-desktop.png`
- `/tmp/kups-post10-expanded-snapshots/post-10-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, dense/sparse umbrella table,
  full-profile umbrella diagnostics figure, methods/protocol sections,
  practical checklist, reproduction code block, current-status section,
  references, and footer present. No blank page, missing figure, obvious text
  clipping, or broken page chrome was found in the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, hidden-draft note, tables, figure, caption, code block,
  current-status section, and references present. The title wraps across
  multiple lines and the tables are tight, but both remain contained and
  readable in the inspected snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 10 hidden draft.
- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Production MD context, final uncertainty diagnostics, and any added
  WHAM/MBAR or hysteresis figures remain final-release blockers until
  implemented and snapshot-reviewed.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 11 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29365419119`.
- Website commit: `38df18dbbe3a785ed1d380d499735b6473dc09d1`.
- Deploy run for that commit: `29365244839`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post11-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post11-expanded-snapshots/manifest.json`.
- Capture scope: post 11 only, after expansion to about 3,544 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post11-expanded-snapshots/post-11-desktop.png`
- `/tmp/kups-post11-expanded-snapshots/post-11-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, adaptive-bias and
  nonequilibrium-work tables, full-profile enhanced-sampling figure,
  protocol/methods sections, practical checklist, reproduction code block,
  current-status section, references, and footer present. No blank page,
  missing figure, obvious text clipping, or broken page chrome was found in
  the inspected snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, hidden-draft note, tables, figure, caption, code block,
  current-status section, and references present. The title wraps heavily and
  the tables are tight, but all remain contained and readable in the inspected
  snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 11 hidden draft.
- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- Production MD context, final uncertainty diagnostics, and any real steered-MD
  trajectory or hysteresis figures remain final-release blockers until
  implemented and snapshot-reviewed.
- The page remains hidden from public navigation and direct-link reachable.

## Expanded Post 12 Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29366249219`.
- Website commit: `c540d524e37527a8a586175d53cbefc76474492a`.
- Deploy run for that commit: `29366058404`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post12-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post12-expanded-snapshots/manifest.json`.
- Capture scope: post 12 only, after expansion to about 3,518 words.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots both captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Changes When the Potential Is a Machine-Learned Interatomic Potential? | Sungsoo Ahn`.

Snapshots visually inspected in this pass:

- `/tmp/kups-post12-expanded-snapshots/post-12-desktop.png`
- `/tmp/kups-post12-expanded-snapshots/post-12-mobile.png`

Feedback:

- Desktop capture renders the expanded article end to end with sidebar table of
  contents, hidden-draft note, source links, capstone regime table,
  provenance table, production-readiness table, full-profile MLIP diagnostic
  figure, practical checklist, reproduction code block, current-status
  section, references, and footer present. No blank page, missing figure,
  obvious text clipping, or broken page chrome was found in the inspected
  snapshot.
- Mobile capture renders the long article through the mobile layout with the
  title, hidden-draft note, tables, figure, caption, code block,
  current-status section, and references present. The title wraps heavily and
  the tables are tight, but all remain contained and readable in the inspected
  snapshot.

Revision decisions:

- No blocking layout issue was found for the expanded post 12 hidden draft.
- Keep mobile title and table wrapping as final typography-polish items after
  the rest of the articles are expanded.
- The real MACE/fcc-Al GPU capstone, pinned model artifact hash, final
  production diagnostics, and regenerated MLIP figure remain final-release
  blockers until implemented and snapshot-reviewed.
- The page remains hidden from public navigation and direct-link reachable.

## All Expanded Drafts Consistency Snapshot Capture

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29367230234`.
- Website commit: `c540d524e37527a8a586175d53cbefc76474492a`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-all-expanded-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-all-expanded-snapshots/manifest.json`.
- Capture scope: posts 01-12 after all hidden drafts had expanded article
  prose and individual snapshot reviews.

Manifest coverage:

- 24 rendered snapshots captured.
- Desktop and mobile snapshots were captured for posts 01-12.
- All captured URLs returned HTTP 200.
- Desktop captures are present for posts:
  `01,02,03,04,05,06,07,08,09,10,11,12`.
- Mobile captures are present for posts:
  `01,02,03,04,05,06,07,08,09,10,11,12`.

Snapshots visually inspected in this pass:

- Contact sheet:
  `/tmp/kups-all-expanded-snapshots/contact-sheets/desktop-contact.png`.
- Contact sheet:
  `/tmp/kups-all-expanded-snapshots/contact-sheets/mobile-contact.png`.
- Narrow/mobile spot checks:
  `/tmp/kups-all-expanded-snapshots/post-03-mobile.png`,
  `/tmp/kups-all-expanded-snapshots/post-11-mobile.png`, and
  `/tmp/kups-all-expanded-snapshots/post-05-mobile.png`.

Feedback:

- Desktop contact-sheet inspection shows all twelve expanded hidden pages
  render end to end with sidebar table of contents, hidden-draft note, source
  links, article sections, at least one diagnostic figure, reproduction block,
  current-status section, references, and footer present. No blank page, missing
  figure, or broken page chrome was visible in the inspected contact sheet.
- Mobile contact-sheet inspection shows all twelve pages reach references and
  footer. Titles wrap heavily on the longest posts, but no title overlap or
  page breakage was visible in the contact sheet.
- Narrow/mobile spot checks confirm table-heavy and long-title pages remain
  contained. Post 03 at 390 px, post 11 at 390 px, and post 05 at 616 px all
  render titles, hidden notes, tables, figures, code blocks, current-status
  sections, references, and footer without clipping or overlap.

Revision decisions:

- No blocking layout issue was found in the all-expanded-drafts consistency
  pass.
- Keep mobile title and table wrapping as final typography-polish items when
  pages are made public.
- This pass resolves the older "recapture after all other articles are
  expanded" review item for posts 01-04.
- The pages remain hidden from public navigation and direct-link reachable.
- Final-release scientific blockers remain: argon/kUPS production diagnostics,
  final estimator/enhanced-sampling figures where applicable, real MACE/fcc-Al
  GPU diagnostics, pinned model artifact metadata, and another rendered
  snapshot pass after final figure/publication changes.

## Post 03 Compact Argon NVE Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29368819123`.
- Website commit: `c33b1adc726f91eb4a1f258f6e2a5e2e3651d69d`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post03-argon-nve-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post03-argon-nve-snapshots/manifest.json`.
- Capture scope: post 03 after adding the compact argon NVE figure panel,
  exported compact result files, and updated hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- Both captured URLs returned HTTP 200.
- Page title in both captures:
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post03-argon-nve-snapshots/post-03-desktop.png`
- `/tmp/kups-post03-argon-nve-snapshots/post-03-mobile.png`

Feedback:

- Desktop capture at `1440 x 10796` renders the updated hidden draft end to
  end with sidebar table of contents, source links, mechanism table, revised
  four-panel diagnostic figure, caption, timestep-choice table, reproduction
  block, current-status section, references, and footer present. No missing
  figure, blank page, obvious clipped text, or broken page chrome was found in
  the inspected snapshot.
- Mobile capture at `390 x 16893` renders the title, hidden-draft note, tables,
  revised four-panel figure, caption, code block, current-status section,
  references, and footer. The figure is necessarily small at mobile width, but
  it remains contained; table wrapping is tight but not clipped.

Revision decisions:

- No blocking layout issue was found for the updated post 03 hidden draft.
- The compact argon NVE figure/prose update is snapshot-reviewed for the hidden
  draft state.
- Keep mobile table and title wrapping as final typography-polish items.
- A larger GPU kUPS production NVE diagnostic remains a final-release blocker
  before public indexing.
- The page remains hidden from public navigation and direct-link reachable.

## Post 04 Compact Argon Thermostat Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29369851547`.
- Website commit: `5761fc19fb122c4d381bbdc89da2ec36b8830004`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post04-argon-thermostat-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post04-argon-thermostat-snapshots/manifest.json`.
- Capture scope: post 04 after adding the compact argon thermostat figure
  panel, exported compact result files, and updated hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`.
- Both captured URLs returned HTTP 200.
- Page title in both captures:
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post04-argon-thermostat-snapshots/post-04-desktop.png`
- `/tmp/kups-post04-argon-thermostat-snapshots/post-04-mobile.png`

Feedback:

- Desktop capture at `1440 x 11564` renders the updated hidden draft end to
  end with sidebar table of contents, source links, equations, multiple
  tables, revised four-panel diagnostic figure, caption, reproduction block,
  current-status section, references, and footer present. No missing figure,
  blank page, obvious clipped text, or broken page chrome was found in the
  inspected snapshot.
- Mobile capture at `410 x 18232` renders the title, hidden-draft note,
  equations, tables, revised four-panel figure, caption, code block,
  current-status section, references, and footer. The figure is small at mobile
  width but remains contained; table and code wrapping is tight but not
  clipped.

Revision decisions:

- No blocking layout issue was found for the updated post 04 hidden draft.
- The compact argon thermostat figure/prose update is snapshot-reviewed for the
  hidden draft state.
- Keep mobile table and title wrapping as final typography-polish items.
- A larger GPU kUPS production thermostat and NVE-handoff diagnostic remains a
  final-release blocker before public indexing.
- The page remains hidden from public navigation and direct-link reachable.

## Hidden Index And Post 08 RDF-PMF Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29374285478`.
- Website commit: `c049640dc27e3ce763b6b744358fe34dde491cf1`.
- Deploy run for that commit: `29374143464`.
- Tutorial commit reviewed:
  `535c48586c6fe30ad14887b2343887d74ae53be8`.
- Tutorial verify run for that commit: `29374144064`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post08-index-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-index-snapshots/manifest.json`.
- Capture scope: hidden tutorial index plus post 08 after adding the compact
  argon trajectory RDF-derived PMF panel, exported result files, refreshed
  prose, and blog-style hidden index.

Manifest coverage:

- 4 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/`.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.
- All captured URLs returned HTTP 200.
- Page titles:
  `kUPS MD Tutorials | Sungsoo Ahn` and
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post08-index-snapshots/post-index-desktop.png`
- `/tmp/kups-post08-index-snapshots/post-index-mobile.png`
- `/tmp/kups-post08-index-snapshots/post-08-desktop.png`
- `/tmp/kups-post08-index-snapshots/post-08-mobile.png`

Feedback:

- Desktop index capture renders the hidden tutorial series in the existing
  blog-list style, with all twelve draft posts linked from the direct-link
  index and no kUPS link added to the public navigation.
- Mobile index capture renders the full list, hidden/direct-link status, and
  repository block. The clone command wraps tightly, but remains readable and
  contained in the inspected snapshot.
- Desktop post 08 capture renders the refreshed long article end to end with
  the four-panel diagnostic figure, including the compact argon RDF-PMF panel,
  current-status section, references, and footer present.
- Mobile post 08 capture keeps the diagnostic figure inside the article column
  and shows no obvious overlap with surrounding text. Tables and title wrapping
  remain tight but readable.

Revision decisions:

- No blocking layout issue was found for the hidden index or refreshed post 08
  hidden draft.
- The compact argon RDF-PMF page refresh is snapshot-reviewed for the hidden
  draft state.
- The index can serve as the blog-style entry point while remaining
  direct-link reachable only.
- Keep mobile title, table, and command wrapping as final typography-polish
  items before public indexing.
- Larger GPU kUPS RDF-derived PMF diagnostics, block/replica uncertainty, and
  final citations remain final-release blockers for post 08.
- The page series remains hidden from public navigation and direct-link
  reachable.

## Post 09 Multi-State Estimator Bridge Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29375440197`.
- Website commit: `d0144d9f96023e9c5fa57a44dcd9d3a729f0603b`.
- Deploy run for that commit: `29375280052`.
- Tutorial commit reviewed:
  `dabe886cc2021f96badc89c6d8d98605f4b0ac90`.
- Tutorial verify run for that commit: `29375269908`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-post09-bridge-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-bridge-snapshots/manifest.json`.
- Capture scope: post 09 after adding the dense-vs-sparse multi-state
  estimator bridge diagnostic, exported compact result files, refreshed
  four-panel figure, and updated hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post09-bridge-snapshots/post-09-desktop.png`
- `/tmp/kups-post09-bridge-snapshots/post-09-mobile.png`

Feedback:

- Desktop capture renders the refreshed long article end to end with sidebar
  table of contents, hidden-draft note, source links, estimator tables,
  updated WHAM/MBAR bridge prose, four-panel diagnostic figure, reproduction
  block, current-status section, references, and footer present. No missing
  figure, blank page, obvious clipped text, or broken page chrome was found in
  the inspected snapshot.
- Mobile capture renders the title, hidden-draft note, tables, four-panel
  figure, code block, current-status section, references, and footer. The long
  title and tables are tight, but they remain contained; the figure scales
  inside the article column.
- The bridge panel remains legible in both viewports. The sparse endpoint-only
  curve has a visible missing middle, matching the prose claim that a broken
  adjacent-overlap network is a protocol failure.

Revision decisions:

- No blocking layout issue was found for the updated post 09 hidden draft.
- The multi-state estimator bridge figure/prose update is snapshot-reviewed
  for the hidden draft state.
- Keep mobile title and table wrapping as final typography-polish items.
- Re-run rendered snapshots if publication indexing changes or if a later
  public article adds a chemistry-specific estimator figure.
- The page remains hidden from public navigation and direct-link reachable.

## Hidden Index And Post 10 Umbrella Replica-Disagreement Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- GitHub Actions run: `29376446171`.
- Website commit: `41f0674ecf059ba84c58d9e8f71657b67d203c88`.
- Deploy run for that commit: `29376297732`.
- Tutorial commit reviewed:
  `f56985cb9915ad0a6f001ed1d56364d915ae8c92`.
- Tutorial verify run for that commit: `29376292286`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy: `/tmp/kups-index-post10-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-index-post10-snapshots/manifest.json`.
- Capture scope: hidden tutorial index plus post 10 after adding the
  replica-disagreement umbrella diagnostic, refreshed four-panel figure,
  exported compact result files, and blog-style hidden index text.

Manifest coverage:

- 4 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/`.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`.
- All captured URLs returned HTTP 200.
- Page titles:
  `kUPS MD Tutorials | Sungsoo Ahn` and
  `What Does Umbrella Sampling Actually Sample? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-index-post10-snapshots/post-index-desktop.png`
- `/tmp/kups-index-post10-snapshots/post-index-mobile.png`
- `/tmp/kups-index-post10-snapshots/post-10-desktop.png`
- `/tmp/kups-index-post10-snapshots/post-10-mobile.png`

Feedback:

- Desktop index capture renders the hidden tutorial series in the same
  blog-list style as the main `/blog/` page, with all twelve draft tutorials
  linked from the direct-link index.
- Mobile index capture keeps the heading, status row, tutorial list, and
  repository block readable and contained.
- Public navigation in both captures shows only the normal site links; kUPS is
  still hidden from public navigation.
- Desktop post 10 capture renders the refreshed long article end to end with
  source links, diagnostic tables, the updated four-panel umbrella figure,
  reproduction block, current-status section, references, and footer present.
- Mobile post 10 capture keeps the four-panel figure inside the article column.
  The figure is small at mobile width, but the caption wraps correctly and no
  obvious text overlap or broken asset was found.

Revision decisions:

- No blocking layout issue was found for the blog-style hidden index or the
  refreshed post 10 hidden draft.
- The local replica-disagreement figure/prose update is snapshot-reviewed for
  the hidden draft state.
- Keep mobile title/table/figure density as final typography-polish items.
- Re-run rendered snapshots after any final production MD additions or public
  indexing change.
- The page series remains hidden from public navigation and direct-link
  reachable.

## Post 11 Steered-Trajectory Hysteresis Snapshot Refresh

- Capture date: 2026-07-14.
- Website workflow: `Capture kUPS snapshots`.
- Final GitHub Actions run: `29377552573`.
- First-pass snapshot run after figure/prose refresh: `29377264543`.
- Website commits:
  `8e7dfec3f3a3f56fb346d85fb99a6b7a11cce2de` and final status correction
  `ba3944c7bd14b1b8966d6676b88a8af9fc662d40`.
- Deploy runs:
  `29377110434` and final deploy `29377412704`.
- Tutorial commit reviewed:
  `cc48b6e98842111e8bba2882545d19a21e4d0bcd`.
- Tutorial verify run for that commit: `29377110812`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded final review copy:
  `/tmp/kups-post11-final-hysteresis-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post11-final-hysteresis-snapshots/manifest.json`.
- Capture scope: post 11 after adding the path-level fast/slow steered
  hysteresis diagnostic, refreshed four-panel figure, exported compact result
  files, updated notebook output, and hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post11-final-hysteresis-snapshots/post-11-desktop.png`
- `/tmp/kups-post11-final-hysteresis-snapshots/post-11-mobile.png`

Feedback:

- Desktop capture renders the refreshed hidden draft end to end with source
  links, adaptive-bias and nonequilibrium-work tables, the updated four-panel
  diagnostic figure, protocol-design prose, Current Status, references, and
  footer present.
- The fourth figure panel is visible in the article column and shows the fast
  protocol's hysteresis gap much larger than the slow protocol's gap. The
  caption matches the figure's claim.
- Mobile capture keeps the long title, tables, figure, caption, reproduction
  block, Current Status, references, and footer contained. The four-panel
  figure is small at mobile width but remains readable enough for the hidden
  draft.
- The page remains hidden from public navigation and direct-link reachable.

Revision decisions:

- No blocking layout issue was found for the refreshed post 11 hidden draft.
- The fast/slow steered hysteresis figure/prose update is snapshot-reviewed
  for the hidden draft state.
- The first-pass snapshots showed the page was layout-safe; a final second
  pass was captured after moving rendered snapshots from the missing list to
  implemented status.
- Keep mobile title/table/figure density as final typography-polish items.
- Replace the controlled path model with real atomistic steered trajectories
  before public indexing.
- Re-run rendered snapshots after any final production MD or public-indexing
  change.

## Post 12 Pinned MACE Artifact Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29378598376`.
- Website commit reviewed:
  `a755ec8f3a2f2d3cf48081e9bd48f4b9c178c588`.
- Website deploy run: `29378460379`.
- Tutorial commit reviewed:
  `35f16fe7df747b97c77e474312d529e3865f7707`.
- Initial tutorial verify run for that commit: `29378375343`; it failed only
  because the release-readiness test still expected a placeholder-artifact
  violation after the placeholder was removed. The test has been updated to
  assert the remaining real GPU capstone blocker instead.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post12-pinned-artifact-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post12-pinned-artifact-snapshots/manifest.json`.
- Capture scope: post 12 after replacing placeholder MACE metadata with pinned
  `mace-mp-0b3-medium.model` provenance, refreshing exported JSON summaries,
  replacing the website figure asset, and updating hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-12-mlip-capstone/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Changes When the Potential Is a Machine-Learned Interatomic Potential? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post12-pinned-artifact-snapshots/post-12-desktop.png`
- `/tmp/kups-post12-pinned-artifact-snapshots/post-12-mobile.png`

Feedback:

- Desktop capture renders the refreshed hidden draft end to end with the
  pinned-artifact note, source links, diagnostic tables, updated MLIP figure,
  production-readiness table, reproduction block, Current Status, references,
  and footer present.
- The figure annotation now shows `mace-mp-0b3-medium.model` and revision
  `e291ace`; no placeholder artifact wording appears in the rendered page.
- Mobile capture keeps the title, tables, figure, caption, reproduction block,
  Current Status, references, and footer contained. Tables are dense but
  readable enough for the hidden draft.
- Live hidden-route check with `?v=a755ec8` confirmed the full SHA-256 hash is
  present and the word `placeholder` is absent from the HTML body.
- The page remains hidden from public navigation and direct-link reachable.

Revision decisions:

- No blocking layout issue was found for the pinned-artifact post 12 hidden
  draft.
- The artifact-provenance update is snapshot-reviewed for the hidden draft
  state.
- Keep mobile title/table/figure density as final typography-polish items.
- Replace the deterministic CPU surrogate with a real MACE/fcc-Al GPU
  production run before public indexing.
- Re-run rendered snapshots after final production diagnostics or any
  public-indexing change.

## Post 09 Index-Refresh Snapshot Review

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29379023705`.
- Website commit reviewed:
  `a755ec8f3a2f2d3cf48081e9bd48f4b9c178c588`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post09-index-refresh-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post09-index-refresh-snapshots/manifest.json`.
- Capture scope: post 09 after the hidden series index was reshaped to match
  the blog listing style and after later hidden-page updates changed deployed
  site state.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-09-estimators/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Do Free-Energy Estimators Assume? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post09-index-refresh-snapshots/post-09-desktop.png`
- `/tmp/kups-post09-index-refresh-snapshots/post-09-mobile.png`

Feedback:

- Desktop capture renders the hidden post 09 draft end to end with sidebar
  table of contents, author note, executable-artifact links, estimator tables,
  four-panel diagnostic figure, reproduction block, Current Status,
  references, and footer present.
- The diagnostic figure remains inside the article column and its four panels
  are still readable. No missing figure, blank page, clipped table, or broken
  page chrome was found.
- Mobile capture keeps the title, author note, estimator tables, four-panel
  figure, code block, Current Status, references, and footer contained. Tables
  are dense but do not overlap neighboring content.
- The page remains hidden from public navigation and direct-link reachable.

Revision decisions:

- No blocking layout issue was found for the post 09 hidden draft after the
  indexing/page-state refresh.
- The previous final-release item asking for rendered snapshots after
  publication-index changes is resolved for this deployed hidden state.
- Keep mobile table density as a final typography-polish item.
- Re-run rendered snapshots if a chemistry-specific estimator figure is added
  or if the page is made public.

## Post 05 Moving-Cell Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29379867440`.
- Website commit reviewed:
  `1d822d55239551f8a1c07299f2386c5fe1fd4d31`.
- Website deploy run: `29379768876`.
- Tutorial commit reviewed:
  `15d4536179235efbef89db82b03b02cbe26d2873`.
- Tutorial verify run for that commit: `29379747365`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post05-moving-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-moving-cell-snapshots/manifest.json`.
- Capture scope: post 05 after adding the reduced-unit argon moving-cell
  diagnostic, exported `argon_npt_dynamics.csv`, updated four-panel figure,
  and refreshed hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post05-moving-cell-snapshots/post-05-desktop.png`
- `/tmp/kups-post05-moving-cell-snapshots/post-05-mobile.png`

Feedback:

- Desktop capture renders the hidden draft end to end with the updated author
  note, source links, barostat tables, moving-cell diagnostic figure,
  reproduction block, Practical Checklist, Current Status, references, and
  footer present.
- The fourth figure panel is visible in the article column and now shows the
  reduced-unit argon moving-cell volume-factor trajectory with pressure and
  effective-sample annotations. The caption matches the revised claim.
- Mobile capture keeps the title, navigation, tables, figure, caption,
  reproduction block, Current Status, references, and footer contained. The
  left navigation and tables are dense at mobile width, but no overlap,
  clipped figure, missing asset, or broken page chrome was found.
- The page remains hidden from public navigation and direct-link reachable.

Revision decisions:

- No blocking layout issue was found for the Post 05 moving-cell hidden draft.
- The compact moving-cell figure/prose update is snapshot-reviewed for the
  hidden draft state.
- Keep mobile title/table/navigation density as final typography-polish items.
- Replace the compact reduced-unit moving-cell harness with a real kUPS
  production NPT diagnostic before public indexing.
- Re-run rendered snapshots after final production NPT figures/citations or
  any public-indexing change.

## Post 10 Uncertainty-Status Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29380491599`.
- Website commit reviewed:
  `6901b0ec2115f565db9f6f1fcbaf44411373ea63`.
- Website deploy run: `29380373319`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post10-uncertainty-status-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post10-uncertainty-status-snapshots/manifest.json`.
- Capture scope: post 10 after clarifying that the controlled
  replica-disagreement uncertainty diagnostic is implemented, while production
  MD context and any production-level uncertainty intervals remain
  final-release blockers.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-10-umbrella-sampling/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `What Does Umbrella Sampling Actually Sample? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post10-uncertainty-status-snapshots/post-10-desktop.png`
  (`1440 x 11224`)
- `/tmp/kups-post10-uncertainty-status-snapshots/post-10-mobile.png`
  (`452 x 17062`)

Feedback:

- Desktop capture renders the hidden Post 10 draft end to end with the updated
  author note, source links, umbrella diagnostic tables, four-panel figure,
  practical checklist, reproduction block, Current Status section, references,
  and footer present.
- The Current Status section now names the local replica-disagreement
  diagnostic as an implemented figure/status item and limits the missing
  uncertainty work to production-level claims.
- Mobile capture keeps the title, diagnostic tables, four-panel figure,
  caption, code block, Current Status section, references, and footer
  contained. Tables remain dense but readable, and no overlap or broken page
  chrome was found.
- Live checks with cache-buster `?v=6901b0e` confirmed the direct hidden URL
  contains the updated status text, while `/` and `/blog/` do not expose
  `post-10-umbrella-sampling` or `kups-md-tutorials`.

Revision decisions:

- No blocking layout issue was found for the Post 10 uncertainty-status hidden
  draft.
- The controlled replica-disagreement uncertainty diagnostic is accepted for
  the hidden draft state.
- Keep mobile table density as a final typography-polish item.
- Add production MD context with real atomistic umbrella windows, model checks,
  and any production-level uncertainty intervals needed before public indexing.
- Re-run rendered snapshots after final production MD figures/citations or any
  public-indexing change.

## Post 11 Uncertainty-Status Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29380950365`.
- Website commit reviewed:
  `2db11dae3d88a9d052d30d393fda5b688323a5f8`.
- Website deploy run: `29380833243`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post11-uncertainty-status-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post11-uncertainty-status-snapshots/manifest.json`.
- Capture scope: post 11 after clarifying that controlled Jarzynski/Crooks,
  ESS, and fast/slow hysteresis diagnostics are implemented, while production
  atomistic steered trajectories and any production-level uncertainty
  intervals remain final-release blockers.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-11-enhanced-sampling/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post11-uncertainty-status-snapshots/post-11-desktop.png`
  (`1440 x 11334`)
- `/tmp/kups-post11-uncertainty-status-snapshots/post-11-mobile.png`
  (`390 x 17608`)

Feedback:

- Desktop capture renders the hidden Post 11 draft end to end with the updated
  author note, source links, adaptive-bias and nonequilibrium-work tables,
  four-panel figure, practical checklist, reproduction block, Current Status
  section, references, and footer present.
- The Current Status section now names the Jarzynski/Crooks, ESS, and fast/slow
  hysteresis diagnostics as implemented figure/status items and limits missing
  uncertainty work to production-level claims.
- Mobile capture keeps the long title, tables, four-panel figure, caption,
  code block, Current Status section, references, and footer contained. Tables
  remain dense but readable, the figure is small but legible enough for the
  hidden draft, and no overlap or broken page chrome was found.
- Live checks with cache-buster `?v=2db11da` confirmed the direct hidden URL
  contains the updated status text, while `/` and `/blog/` do not expose
  `post-11-enhanced-sampling` or `kups-md-tutorials`.

Revision decisions:

- No blocking layout issue was found for the Post 11 uncertainty-status hidden
  draft.
- The controlled Jarzynski/Crooks, ESS, and fast/slow hysteresis diagnostics
  are accepted for the hidden draft state.
- Keep mobile title/table/figure density as final typography-polish items.
- Add production MD context with real atomistic steered trajectories, model
  checks, and any production-level uncertainty intervals needed before public
  indexing.
- Re-run rendered snapshots after final production MD figures/citations or any
  public-indexing change.

## Post 08 RDF-PMF Uncertainty Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29381687757`.
- Website commit reviewed:
  `8bff587c0ff672594e6a462b40d6722f60b2b5ef`.
- Website deploy run: `29381569320`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/manifest.json`.
- Capture scope: post 08 after adding compact RDF-PMF block SEM and replica
  disagreement diagnostics, exporting the refreshed full-profile figure and
  compact JSON/CSV assets, and updating hidden-page prose/status.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/post-08-desktop.png`
  (`1440 x 11537`)
- `/tmp/kups-post08-rdf-pmf-uncertainty-snapshots/post-08-mobile.png`
  (`550 x 17669`)

Feedback:

- Desktop capture renders the hidden Post 08 draft end to end with the updated
  author note, source links, PMF diagnostic tables, equations, updated
  four-panel figure, reproduction block, Current Status section, references,
  and footer present.
- The refreshed figure shows the trajectory RDF-PMF panel with block SEM and
  replica-disagreement overlays. The panel remains contained in the article
  column, and the caption matches the updated claim.
- Mobile capture keeps the title, tables, equations, updated figure, caption,
  code block, Current Status section, references, and footer contained. Tables
  remain dense but readable, and no overlap, clipped figure, missing asset, or
  broken page chrome was found.
- Live checks with cache-buster `?v=8bff587` confirmed the direct hidden URL
  contains `block SEM` and `replica disagreement`, while `/` and `/blog/` do
  not expose `post-08-free-energies` or `kups-md-tutorials`.

Revision decisions:

- No blocking layout issue was found for the Post 08 RDF-PMF uncertainty
  hidden draft.
- The compact block/replica RDF-PMF uncertainty diagnostic is snapshot-reviewed
  for the hidden draft state.
- Keep mobile title/table density as a final typography-polish item.
- Add larger GPU kUPS RDF-derived PMF diagnostics and final citations before
  public indexing.
- Re-run rendered snapshots after final production RDF-PMF figures/citations or
  any public-indexing change.

## Post 07 Replica Observable Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29382588504`.
- Website commit reviewed:
  `1c9520bcbabef814ca91e2e58fbe8bb622ba6e53`.
- Website deploy run: `29382464261`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post07-replica-observable-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-replica-observable-snapshots/manifest.json`.
- Capture scope: post 07 after adding compact seed-shifted replica RDF and
  coordination diagnostics, exporting the refreshed full-profile figure and
  JSON/CSV assets, and updating hidden-page prose/status.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post07-replica-observable-snapshots/post-07-desktop.png`
  (`1440 x 14689`)
- `/tmp/kups-post07-replica-observable-snapshots/post-07-mobile.png`
  (`390 x 22356`)

Feedback:

- Desktop capture renders the hidden Post 07 draft end to end with the new
  compact trajectory replica rows, updated uncertainty prose, refreshed
  four-panel figure, revised caption, reproduction block, Current Status
  section, references, and footer present.
- The refreshed figure shows the compact trajectory RDF panel with a replica
  standard-deviation band and `rep SE = 0.028` annotation. The legend and
  annotation remain contained and do not obscure the first RDF peak.
- Mobile capture keeps the title, tables, refreshed figure, caption, code
  block, Current Status section, references, and footer contained. The full
  diagnostic figure remains small on mobile, but no overlap, clipped table,
  missing asset, or broken page chrome was found.
- Live checks confirmed the direct hidden URL contains `coordination replica
  standard error`, while `/` and `/blog/` do not expose
  `post-07-observables` or `kups-md-tutorials`.

Revision decisions:

- No blocking layout issue was found for the Post 07 replica-observable hidden
  draft.
- The compact replica RDF/coordination diagnostic is snapshot-reviewed for the
  hidden draft state.
- Keep mobile title/table/figure density as a final typography-polish item.
- Add larger GPU kUPS trajectory diagnostics for physical observables before
  public indexing.
- Re-run rendered snapshots after final production observable figures/citations
  or any public-indexing change.

## Post 03 Replica NVE Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29383922778`.
- Website commit reviewed:
  `e31de95f84635b1ba81a9644b195dcc4f7d6f54d2`.
- Website deploy run: `29383806796`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post03-replica-nve-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post03-replica-nve-snapshots/manifest.json`.
- Capture scope: post 03 after adding the 256-atom, three-replica reduced-unit
  argon NVE protocol, exporting the refreshed full-profile figure and JSON/CSV
  assets, and updating hidden-page prose/status.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-03-errors/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Timestep, Precision, and Force Error Become Simulation Error? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post03-replica-nve-snapshots/post-03-desktop.png`
  (`1440 x 11452`)
- `/tmp/kups-post03-replica-nve-snapshots/post-03-mobile.png`
  (`453 x 18146`)

Feedback:

- Desktop capture renders the hidden Post 03 draft end to end with sidebar TOC,
  updated full-profile NVE protocol table, refreshed four-panel figure,
  reproduction block, Current Status section, references, and footer present.
- The refreshed figure is visible in the article body and the NVE panel/caption
  match the 256-atom, three-replica CPU-fallback protocol claim.
- Mobile capture keeps the long title, hidden-draft note, tables, refreshed
  figure, caption, code block, Current Status section, references, and footer
  contained. Tables are dense but contained, and the figure is small at mobile
  width but not clipped.
- Live checks with cache-buster `?v=e31de95` confirmed the direct hidden post
  contains `gpu_ready_lj_nve_replicas` and `256-atom`; the hidden kUPS index
  links to Post 03; `/` and `/blog/` do not expose `kups-md-tutorials` or
  `post-03-errors`.

Revision decisions:

- No blocking layout issue was found for the Post 03 replica NVE hidden draft.
- The 256-atom, three-replica reduced-unit argon NVE diagnostic is accepted for
  the hidden draft state.
- Keep mobile table/figure density as final typography-polish items.
- Add real CUDA/GPU kUPS production NVE diagnostics before public indexing.
- Re-run rendered snapshots after final production NVE diagnostics or any
  public-indexing change.

## Post 04 Thermostat Handoff Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29385110755`.
- Website commit reviewed:
  `1635add74771cfbe02fc42e0d93ce59b1da8f716`.
- Website deploy run: `29384989661`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post04-handoff-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post04-handoff-snapshots/manifest.json`.
- Capture scope: post 04 after adding the 256-atom, three-replica reduced-unit
  argon Langevin thermostat-to-NVE handoff protocol, exporting the refreshed
  full-profile figure and JSON/CSV assets, and updating hidden-page
  prose/status.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-04-thermostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Thermostats Change Sampling and Dynamics? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post04-handoff-snapshots/post-04-desktop.png`
  (`1440 x 11724`)
- `/tmp/kups-post04-handoff-snapshots/post-04-mobile.png`
  (`410 x 18512`)

Feedback:

- Desktop capture renders the hidden Post 04 draft end to end with sidebar TOC,
  equations, coupling and canonical-target tables, refreshed four-panel handoff
  figure, revised caption, reproduction block, Current Status section,
  references, and footer present.
- The refreshed figure is visible in the article body and the handoff
  panel/caption match the 256-atom, three-replica CPU-fallback protocol claim.
- Mobile capture keeps the long title, hidden-draft note, equations, tables,
  refreshed figure, caption, code block, Current Status section, references,
  and footer contained. Tables are dense but contained, and the figure is small
  at mobile width but not clipped.
- Live checks with cache-buster `?v=1635add` confirmed the direct hidden post
  contains `thermostat-to-NVE`/`NVE handoff` and `256-atom`; the hidden kUPS
  index links to Post 04; `/` and `/blog/` do not expose `kups-md-tutorials` or
  `post-04-thermostats`.

Revision decisions:

- No blocking layout issue was found for the Post 04 thermostat handoff hidden
  draft.
- The 256-atom, three-replica reduced-unit argon Langevin plus NVE-handoff
  diagnostic is accepted for the hidden draft state.
- Keep mobile table/figure density as final typography-polish items.
- Add real CUDA/GPU kUPS production thermostat and NVE-handoff diagnostics
  before public indexing.
- Re-run rendered snapshots after final production thermostat diagnostics or
  any public-indexing change.

## kUPS Index Blog-Style Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29385647867`.
- Website commit reviewed:
  `22bbd77e6cdaff3f86b182c4d7304b96c1c11104`.
- Website deploy run: `29385507777`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-index-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-index-snapshots/manifest.json`.
- Capture scope: hidden series index at `/kups-md-tutorials/` after aligning
  the index metadata and list rendering with the public `/blog/` archive style.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/`.
- Both captured URLs returned HTTP 200.
- Page title: `kUPS MD Tutorials | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-index-snapshots/post-index-desktop.png` (`1440 x 1740`)
- `/tmp/kups-index-snapshots/post-index-mobile.png` (`390 x 2609`)

Feedback:

- Desktop capture renders a blog-archive-like hidden index with the same compact
  title, description, metadata row, and ordered bibliography treatment used by
  the public blog listing. All twelve tutorial links, descriptions, authorship,
  update dates, and read-time metadata are visible without clipping.
- Mobile capture wraps the series-status metadata across two lines, keeps all
  twelve post entries readable, and preserves the public mobile nav without
  adding a visible kUPS navigation item.
- Live checks with cache-buster `?v=22bbd77` confirmed the hidden index
  contains `kUPS MD Tutorials`, `Series status`, `Hidden draft`, and the Post 01
  link; `/` and `/blog/` do not expose `kups-md-tutorials` or the tutorial
  post slugs.

Revision decisions:

- No blocking layout issue was found for the hidden kUPS index.
- The index is acceptable as a direct-link-only page matching the public blog
  archive style while the tutorial series remains hidden from public
  navigation.
- Re-run rendered index snapshots before public indexing or after changing the
  list metadata, navigation state, or series ordering.

## Post 05 Replica Moving-Cell Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29386749372`.
- Website commit reviewed:
  `06cbf7c59f4f40eb79675d60be1d9dc58f588456`.
- Website deploy run: `29386632830`.
- Tutorial commit reviewed:
  `74e974776d0d052e81a50386932788c2ea131f73`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post05-replica-moving-cell-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post05-replica-moving-cell-snapshots/manifest.json`.
- Capture scope: post 05 after adding three full-profile moving-cell replicas,
  kinetic-temperature samples, energy-like samples, pressure SEM, refreshed
  figure assets, exported JSON/CSV assets, and hidden-page prose updates.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-05-barostats/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Should Pressure and Cell Degrees of Freedom Be Coupled? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post05-replica-moving-cell-snapshots/post-05-desktop.png`
  (`1440 x 12267`)
- `/tmp/kups-post05-replica-moving-cell-snapshots/post-05-mobile.png`
  (`616 x 19414`)

Feedback:

- Desktop capture renders the hidden Post 05 draft end to end with sidebar TOC,
  updated three-replica prose, source links, scalar and argon configuration
  tables, refreshed four-panel figure, revised caption, reproduction block,
  Practical Checklist, Current Status, references, and footer present.
- The refreshed figure is visible in the article body; the fourth panel is not
  clipped and the caption now matches the replica uncertainty and
  kinetic-temperature content.
- Mobile capture keeps the long title, hidden-draft note, tables, refreshed
  figure, caption, reproduction block, Current Status, references, and footer
  contained. Tables are dense but contained, and the figure is small at mobile
  width but not broken or missing.
- Live checks with cache-buster `?v=06cbf7c` confirmed the direct hidden post
  contains `three moving-cell replicas`, `0.925 +/- 0.005`, `kinetic
  temperature is 0.699`, and the refreshed figure asset path; `/` and `/blog/`
  do not expose `kups-md-tutorials` or `post-05-barostats`.

Revision decisions:

- No blocking layout issue was found for the Post 05 replica moving-cell hidden
  draft.
- The three-replica reduced-unit moving-cell diagnostic is accepted for the
  hidden draft state.
- Keep mobile table/figure density as a final typography-polish item.
- Add real CUDA/GPU kUPS production NPT diagnostics with full atomistic
  thermostat/barostat settings, GPU provenance, and production stress/cell
  checks before public indexing.
- Re-run rendered snapshots after final production NPT diagnostics, final
  citations, or any public-indexing change.

## Post 06 Coordination-Observable Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29387756210`.
- Website commit reviewed:
  `ff83d44c4ca14c562017557bcb00003e32a6fbfa`.
- Website deploy run: `29387640167`.
- Tutorial commit reviewed:
  `f5f5fd99157d4eb1eb4ecafb5bb677b6d374a328`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post06-coordination-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post06-coordination-snapshots/manifest.json`.
- Capture scope: post 06 after adding compact reduced-unit argon coordination
  number alongside potential energy per atom, refreshing the figure assets,
  exporting JSON/CSV assets, and updating hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-06-trajectory-length/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `When Is a Trajectory Long Enough to Trust? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post06-coordination-snapshots/post-06-desktop.png`
  (`1440 x 12217`)
- `/tmp/kups-post06-coordination-snapshots/post-06-mobile.png`
  (`629 x 18508`)

Feedback:

- Desktop capture renders the hidden Post 06 draft end to end with sidebar
  TOC, updated coordination-observable prose, source links, diagnostic tables,
  display equation, refreshed four-panel figure, reproduction block, Practical
  Checklist, Current Status, references, and footer present.
- The refreshed figure is visible in the article body; the fourth panel shows
  the coordination axis and no blocking clipping or missing asset was found.
- Mobile capture keeps the long title, hidden-draft note, tables, figure,
  caption, reproduction block, Current Status, references, and footer
  contained. Tables and the figure are dense at mobile width but not broken in
  the inspected snapshot.
- Live check with cache-buster `?cachebust=post06-coordination-ff83d44`
  returned HTTP 200 and confirmed the deployed HTML contains `coordination
  number`, `coordination-number`, and `rc = 1.5`.

Revision decisions:

- No blocking layout issue was found for the Post 06 coordination-observable
  hidden draft.
- The compact reduced-unit argon coordination diagnostic is accepted for the
  hidden draft state.
- Keep mobile table/figure density as a final typography-polish item.
- Add larger GPU kUPS trajectory-length diagnostics for production physical
  observables before public indexing.
- Re-run rendered snapshots after final production physical-observable
  diagnostics, final citations, or any public-indexing change.

## kUPS Index Blog-Style Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29389348702`.
- Website commit reviewed:
  `37df521`.
- Website deploy run: `29389218444`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-index-37df521-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-index-37df521-snapshots/kups-md-page-snapshots/manifest.json`.
- Capture scope: hidden kUPS series index after aligning the listing copy and
  metadata rhythm with the public `/blog/` index while keeping the page
  direct-link-only.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `kUPS MD Tutorials | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-index-37df521-snapshots/kups-md-page-snapshots/post-index-desktop.png`
  (`1440 x 1763`)
- `/tmp/kups-index-37df521-snapshots/kups-md-page-snapshots/post-index-mobile.png`
  (`390 x 2632`)

Feedback:

- Desktop capture matches the `/blog/` list structure: title, introductory
  note, compact type summary, ordered bibliography list, descriptions, and
  author/date/read-time metadata are all visible without overlap.
- Mobile capture keeps the type summary, long titles, descriptions, and
  metadata contained. The layout remains narrow and blog-like, with no exposed
  kUPS navigation item in the header.
- Live check with cache-buster `?v=37df521` returned HTTP 200 and confirmed
  the deployed HTML contains `Executable molecular-dynamics notes`, `Post
  types`, `Tutorials 12`, and `part 1 of 12`.
- The public homepage check did not expose `kups-md-tutorials`, preserving the
  hidden direct-link-only status.

Revision decisions:

- No blocking layout issue was found for the hidden kUPS index.
- The blog-style index is accepted for the hidden draft state.
- Re-run rendered snapshots after public-indexing changes or major curriculum
  title/description updates.

## Post 08 RDF-PMF Support-Sensitivity Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29390138917`.
- Website commit reviewed:
  `6c08328`.
- Website deploy run: `29390018103`.
- Tutorial commit reviewed:
  `b5e8a88400268edb568b611945dcee85e34143d2`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/manifest.json`.
- Capture scope: Post 08 hidden page after adding RDF-PMF
  support-threshold sensitivity, refreshing the figure/assets, updating the
  notebook/review text, and correcting the page provenance text.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-08-free-energies/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Equilibrium Samples Become Free Energies? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-desktop.png`
  (`1440 x 11817`)
- `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-mobile.png`
  (`550 x 18162`)
- `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-figure-wide.png`
- `/tmp/kups-post08-support-sensitivity-final-snapshots/kups-md-page-snapshots/post-08-mobile-figure-wide.png`

Feedback:

- Desktop capture renders the hidden Post 08 page end to end with sidebar TOC,
  updated support-threshold prose, refreshed diagnostic figure, caption,
  reproduction block, Practical Checklist, Current Status, references, and
  footer present.
- The desktop figure crop shows the trajectory RDF-PMF panel with support
  `0.05`, dotted support `0.02` and `0.10` curves, block SEM, replica
  disagreement, PMF-minimum marker, and `support span = 1.35` annotation
  visible without blocking the panel.
- Mobile capture keeps the support-threshold prose, figure, caption, tables,
  code block, Current Status, and references contained. The figure is dense at
  mobile width but readable, and no text/image overlap was found in the
  inspected crop.
- Live check with cache-buster `?v=6c08328` returned HTTP 200 and confirmed
  the deployed HTML contains `support-threshold sensitivity`, `2.998`,
  `1.355`, and the updated support-threshold figure caption.
- Public homepage and public blog checks did not expose `kups-md-tutorials` or
  `post-08-free-energies`, preserving the hidden direct-link-only status.

Revision decisions:

- No blocking layout issue was found for the Post 08 support-sensitivity
  hidden draft.
- The compact RDF-PMF support-threshold diagnostic is accepted for the hidden
  draft state.
- Keep mobile figure/table density as a final typography-polish item.
- Add larger GPU kUPS RDF-derived PMF diagnostics and final citations before
  public indexing.
- Re-run rendered snapshots after final production RDF-PMF figures/citations
  or any public-indexing change.

## Post 07 VACF Replica Snapshot Refresh

- Capture date: 2026-07-15.
- Website workflow: `Capture kUPS snapshots`.
- Snapshot run: `29388638389`.
- Website commit reviewed:
  `604c4833b14622f14e55a3a19c43148affc18d56`.
- Website deploy run: `29388521392`.
- Tutorial commit reviewed:
  `6b07076c0b7575be24809e281092aa9ba7ff99e8`.
- Artifact name: `kups-md-page-snapshots`.
- Downloaded review copy:
  `/tmp/kups-post07-vacf-snapshots/`.
- Manifest reviewed:
  `/tmp/kups-post07-vacf-snapshots/manifest.json`.
- Capture scope: post 07 after adding compact reduced-unit argon VACF
  replica uncertainty, refreshing the figure assets, exporting JSON/CSV
  assets, and updating hidden-page prose.

Manifest coverage:

- 2 rendered snapshots captured.
- Desktop and mobile snapshots were captured for
  `https://sungsoo-ahn.github.io/kups-md-tutorials/post-07-observables/`.
- Both captured URLs returned HTTP 200.
- Page title:
  `How Do Trajectories Become Physical Observables? | Sungsoo Ahn`.

Snapshots visually inspected:

- `/tmp/kups-post07-vacf-snapshots/post-07-desktop.png`
  (`1440 x 12256`)
- `/tmp/kups-post07-vacf-snapshots/post-07-mobile.png`
  (`541 x 18822`)

Feedback:

- Desktop capture renders the hidden Post 07 draft end to end with sidebar
  TOC, updated VACF-replica prose, source links, diagnostic tables, refreshed
  four-panel figure, reproduction block, Practical Checklist, Current Status,
  references, and footer present.
- The refreshed figure is visible in the article body; the VACF panel is not
  clipped, and the caption now matches the controlled-plus-compact VACF
  replica-band content.
- Mobile capture keeps the long title, hidden-draft note, tables, figure,
  caption, reproduction block, Current Status, references, and footer
  contained. Tables and the figure are dense at mobile width but not broken in
  the inspected snapshot.
- Live check with cache-buster `?cachebust=post07-vacf-604c483` returned HTTP
  200 and confirmed the deployed HTML contains `VACF integral replica SE` and
  `replica band`.

Revision decisions:

- No blocking layout issue was found for the Post 07 VACF-replica hidden
  draft.
- The compact reduced-unit argon VACF replica diagnostic is accepted for the
  hidden draft state.
- Keep mobile table/figure density as a final typography-polish item.
- Add larger GPU kUPS trajectory diagnostics for production physical
  observables before public indexing.
- Re-run rendered snapshots after final production physical-observable
  diagnostics, final citations, or any public-indexing change.
