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
