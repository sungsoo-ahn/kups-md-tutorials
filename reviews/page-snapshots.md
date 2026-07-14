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
