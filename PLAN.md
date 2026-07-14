# kUPS Molecular Dynamics Tutorial Series

## Objective

Build a publication-grade, concept-led molecular dynamics tutorial series for
ML researchers who already know machine-learned interatomic potentials, force
fields, and the equations of molecular dynamics, but want the practical
simulation, sampling, and free-energy details needed to trust MD results. This
repository owns simulations, notebooks, tests, and numerical results.
`../sungsoo-ahn.github.io` owns final prose, figures, and published assets.

Stop only when twelve validated 3,500-10,000-word posts, reproducible GPU
experiments, executable notebooks, final figures, passing tests, and a
successful Jekyll build are complete.

## Interfaces and Ownership

- Pin Python 3.13 and kUPS 1.0.3; provide CPU development and CUDA/Hugging Face extras.
- Build `src/kups_md_tutorials/` around system construction, kUPS simulation setup, HDF5 analysis, plotting, and reproducibility manifests.
- Expose `kups-tutorial run <post> --profile smoke|full`, `run-all`, `verify`, and `export-site`.
- Ignore trajectories, model archives, and caches. Commit configurations, notebooks, compact summaries, manifests, and figure sources.
- Record seeds, configuration and lock hashes, git revision, versions, device, precision, and MLFF artifact hash.
- Use fixed seeds and tolerance-based reproducibility across CPU and GPU.
- Keep notebooks as presentation layers; reusable logic belongs in `src/`.

## Website Style Contract

The website posts must follow the existing `sungsoo-ahn.github.io` blog style,
not a standalone tutorial-book style.

- Write each post as an al-folio Jekyll post in `_posts/YYYY-MM-DD-slug.md`
  with `layout: post`, `date`, `last_updated`, `description`, `post_type:
  tutorial`, `authors: ["Sungsoo Ahn"]`, `categories`, `tags`, `toc:
  sidebar: left`, and `related_posts: false`.
- Use one shared series identifier for the twelve MD posts, with
  `series_title`, `series_description`, and `series_order` matching the blog's
  existing series metadata pattern. Do not add custom roadmap blocks that the
  blog layout does not render.
- Start every post with the existing author-note HTML pattern: a muted
  italic `Note:` paragraph that states context, prerequisites, relationship to
  nearby posts, and correction/replication expectations.
- Use the blog's explanatory voice: concept-led, ML-facing, direct, and
  bottom-up from probability, sampling, and energy functions. Introduce jargon
  in plain language before using it technically.
- Prefer narrative sections with concrete questions as headings. Use tables,
  block definitions, equations, and practical checklists where they clarify a
  concept, but avoid turning the post into notebook output.
- Keep computation reproducible in this repository; in the blog, show compact
  code snippets only when they teach the idea. Link back to the corresponding
  notebook, config, summary table, and figure-generation source.
- Store final website images under `assets/img/blog/` and embed them with
  `{% include figure.liquid ... %}` using `class="img-fluid rounded
  z-depth-1"` and `zoomable=true` for static SVG/PNG figures.
- Figure captions should usually have two sentences: what the figure shows and
  what interpretation or mechanism it supports. Use `\(...\)` math in
  captions, not `$...$` or `$$...$$`.
- Source before drawing: use license-compatible existing figures when
  appropriate; draw custom figures only for post-specific concepts, quantitative
  outputs, or synthesis diagrams. Record source URL, license, and modifications
  outside the rendered post body.
- Every text citation must have a matching `## References` entry with
  `cite-*`/`ref-*` anchors and reverse backlinks. Add references as claims are
  introduced, not as an afterthought.
- Use footnotes for terminology or caveats that would distract from the main
  path. Footnote IDs must be short single words without hyphens.
- Update `last_updated` on every edit to a website post, including small
  edits.

## Curriculum

- [ ] 1. **How Do You Initialize an MD Simulation Without Biasing the Result?** Structures, density/cell setup, minimization, velocity initialization, Maxwell-Boltzmann sampling, center-of-mass removal, warmup, seeds, and provenance.
- [ ] 2. **What Does an MD Integrator Actually Approximate?** Operator splitting, velocity Verlet, force-update conventions, reversibility, symplectic structure, shadow energy, and why integrator details matter beyond the equation of motion.
- [ ] 3. **How Do Timestep, Precision, and Force Error Become Simulation Error?** Stability limits, bounded energy oscillations versus drift, mixed precision, noisy MLIP forces, neighbor-list update effects, and diagnostic NVE tests.
- [ ] 4. **How Do Thermostats Change Sampling and Dynamics?** BAOAB Langevin, CSVR, coupling strengths, kinetic-energy distributions, canonical checks, dynamical distortion, and when to switch to NVE production.
- [ ] 5. **How Should Pressure and Cell Degrees of Freedom Be Coupled?** NPT sampling, CSVR-NPT, BAOAB NPT Langevin, pressure fluctuations, compressibility, barostat time constants, flexible-cell behavior, and finite-size effects.
- [ ] 6. **When Is a Trajectory Long Enough to Trust?** Equilibration, warmup removal, running statistics, autocorrelation, effective sample size, block averaging, replica agreement, and uncertainty reporting.
- [ ] 7. **How Do Trajectories Become Physical Observables?** Time versus ensemble averages, observable definitions, RDF as an estimator rather than a toy endpoint, coordination integrals, time-correlation functions, finite-size effects, and error bars.
- [ ] 8. **How Do Equilibrium Samples Become Free Energies?** Collective variables, histograms, PMFs, \(F(s)=-k_BT\log p(s)\), RDF-derived potentials of mean force, binning bias, reweighting basics, and uncertainty.
- [ ] 9. **What Do Free-Energy Estimators Assume?** Free-energy perturbation, Bennett acceptance ratio, WHAM/MBAR concepts, overlap, effective sample size, estimator variance, and failure diagnostics.
- [ ] 10. **What Does Umbrella Sampling Actually Sample?** Harmonic biasing, window placement, overlap checks, reconstruction, hysteresis, replica consistency, and interpretation of biased trajectories.
- [ ] 11. **How Do Adaptive and Nonequilibrium Enhanced-Sampling Methods Work?** Metadynamics, well-tempered bias, steered MD, Jarzynski/Crooks intuition, path-measure corrections, and links to ML sampling ideas.
- [ ] 12. **What Changes When the Potential Is a Machine-Learned Interatomic Potential?** MACE/fcc-Al capstone using the same initialization, integrator, ensemble, free-energy, and uncertainty diagnostics; cover extrapolation, instability, ensemble drift, uncertainty, and static-metric blind spots.

## Execution Checkpoints

- [x] Persist the approved plan and start a durable goal.
- [ ] Implement packaging, typed configurations, system builders, simulation runner, analysis, plotting, manifests, and tests.
- [ ] Add smoke and full profiles for every tutorial; require smoke verification before full runs.
- [ ] Run final experiments on a GPU and freeze compact summaries after statistical review.
- [ ] Create one executable notebook and final figure set per tutorial.
- [ ] Self-review each tutorial package before considering it complete: code,
  configs, notebook, numerical summaries, figures, and website post must be
  reviewed against this plan and the scientific rules below.
- [ ] Collect rendered snapshots for every final figure and every website post,
  record feedback, revise, and repeat until the figures and page layout are
  publication-ready.
- [ ] Write all twelve website posts with one publication date, blog-style front matter, author notes, references, code links, final figures, and shared series metadata.
- [ ] Validate both repositories and visually inspect rendered posts.

## Goal Execution Protocol

When `/goal` is used to continue this project, every substantial milestone must
include an explicit self-review and visual-review loop before it can be marked
complete.

Before implementing or finalizing a post, `/goal` must maintain a live checklist
for the current milestone. The checklist must include simulation/config work,
notebook execution, figure generation, figure snapshot review, website draft or
post work, rendered page snapshot review, validation commands, and commit/push
status. A milestone is incomplete if any review artifact is still written in
future tense, if snapshot feedback has not been recorded, or if the final answer
does not state which checks passed and which open items remain.

For each post, `/goal` must create or update `reviews/post-XX.md` with these
sections before the post can be called done:

1. **Scope and provenance.** Record the post number, profiles reviewed, current
   Git commit or working-tree state, commands run, generated files inspected,
   and any hidden website draft URL.
2. **Code and reproducibility review.** Check config determinism, seed handling,
   unit assumptions, output paths, manifest contents, dependency versions, test
   coverage, notebook execution from a clean kernel, and whether every table or
   figure can be regenerated from committed code and compact committed outputs.
3. **Scientific review.** For each numerical claim, record the diagnostic that
   supports it, the uncertainty or effective-sample-size evidence, comparison
   controls, failure modes, and whether any ambiguous or negative result should
   be stated in the prose instead of hidden.
4. **Figure feedback review.** Generate snapshot PNGs from the exact SVG/PNG
   assets intended for publication. Inspect desktop and mobile-relevant sizes
   for label overlap, clipped text, unreadable tick labels, color contrast,
   misleading scales, caption mismatch, and whether the figure actually
   supports the stated mechanism. Record concrete feedback and the revision
   made; if any blocking issue is found, regenerate the figure and capture a
   new snapshot. Record the exact snapshot file path, the inspected figure file
   path, the viewport or raster size if applicable, and whether the inspected
   snapshot is the first pass or a revised pass.
5. **Website page review.** Capture rendered desktop and mobile snapshots from
   a local or deployed Jekyll build. Inspect equations, figures, captions, code
   blocks, tables, navigation state, link targets, overflow, and small-screen
   readability. Record the snapshot source, URL or local build path, viewport
   sizes, feedback, and revisions before marking the page ready.
6. **Prose and style review.** Check the post against the website style
   contract: concept-led, ML-facing, citation-complete, blog-native front
   matter, restrained code snippets, final figure assets under
   `assets/img/blog/`, and no notebook-transcript structure.
7. **Open items.** Separate blocking issues from accepted limitations. A hidden
   draft may have open items; a final post may not have unresolved blocking
   items in code, science, figure readability, page rendering, or citations.

Snapshot feedback is required work, not optional polish. Preserve final figure
snapshots under `snapshots/post-XX/` or record equivalent lightweight snapshot
references in the review note. Do not commit large browser caches, raw
trajectories, model archives, or bulky intermediate render outputs.

When a hidden draft is intentionally not final, the review note must say so
explicitly and split open items into:

- blocking items for the current hidden draft;
- non-blocking items accepted until the final article pass;
- final-release blockers that must be resolved before public indexing.

The final response for each `/goal` continuation must summarize the review
status, list the snapshot artifacts inspected, report validation commands run,
and state whether the page remains hidden or has been made public.

## Scientific Rules

- Reuse the same initial state for controlled comparisons.
- Report normalized energy drift, bounded fluctuation, uncertainty, and instability separately.
- Diagnose equilibration and autocorrelation instead of relying on visual plausibility.
- Predefine comparisons and report unexpected or negative results honestly.
- Use toy 1D/2D examples only for free-energy and enhanced-sampling intuition;
  keep executable kUPS experiments centered on argon through post 11 and
  MLIP aluminum for post 12.
- Keep each full tutorial reproduction under one hour on the target GPU and provide a short CPU smoke profile.
- Pin the MACE artifact by repository revision and verify its downloaded hash.

## Verification

- `uv run pytest`
- `uv run ruff check .`
- `uv run kups-tutorial run-all --profile smoke`
- `uv run kups-tutorial verify`
- Execute all notebooks from clean kernels.
- Reproduce committed summaries from full GPU configurations.
- Review each post's self-review artifact and confirm every blocking item is
  resolved.
- Capture and inspect figure snapshots for all final figures.
- Capture and inspect desktop and mobile snapshots of all rendered posts.
- Run `python3 scripts/validate_blog.py` in the website repository.
- Run `bundle exec jekyll build`, using Homebrew Ruby on macOS when applicable.
- Inspect all posts at desktop and mobile widths for equations, figures, captions, code overflow, and broken links.
- Run `git diff --check` in both repositories.
- Confirm that no trajectories, model archives, caches, or oversized generated files are tracked.

## Progress Log

- 2026-07-14: Plan approved. Audience, eight-post scope, concept-led Python API approach, standalone publication, shared release date, GPU execution, argon progression, and MACE/fcc-Al capstone locked.
- 2026-07-14: Curriculum revised to twelve advanced posts for MLIP-aware ML researchers, with emphasis on initialization, integrators, ensemble control, free-energy estimation, enhanced sampling, and an MLIP-Al capstone.
- 2026-07-14: Added `/goal` execution expectations for self-review artifacts,
  figure snapshot feedback, and rendered page snapshot review before milestone
  completion.
