# kUPS Molecular Dynamics Tutorials

## Goal

Create an executable advanced introduction to molecular-dynamics practice for
machine-learning researchers who already know MLIPs, force fields, and the
equations of MD, using kUPS as the primary simulation library.

The material will be published in two forms:

1. Executable notebooks and reproducible code in this repository.
2. Polished tutorial articles on sungsoo-ahn.github.io.

## Audience

Researchers who understand calculus, probability, Python, machine learning,
MLIPs, and the basic equations of MD, but want a practical understanding of
initialization, integrators, ensemble control, uncertainty, free-energy
estimation, and enhanced sampling.

## First milestone

Title:
"How Do You Initialize an MD Simulation Without Biasing the Result?"

The tutorial will:

- build reproducible argon initial states from explicit density, cell, and
  structure choices;
- initialize velocities from the Maxwell-Boltzmann distribution with fixed
  seeds and center-of-mass momentum removal;
- separate minimization, warmup, and production state construction;
- record initialization provenance, software versions, and configuration;
- show how biased or inconsistent initial conditions can contaminate later
  ensemble and free-energy estimates.

## Deliverables

- reproducible Python experiment;
- small CPU smoke configuration;
- full experiment configuration;
- deterministic initialization and provenance table;
- executable notebook;
- unit and integration tests;
- publication-quality SVG and PNG figures;
- website article draft;
- README with reproduction instructions.

## Non-goals for the first milestone

- biomolecular force fields;
- proteins or solvent models;
- free-energy estimation;
- enhanced sampling;
- machine-learned interatomic potentials;
- differentiating through full trajectories;
- large GPU benchmarks.

## Scientific requirements

- Fix all random seeds.
- Reuse controlled initial states across downstream comparisons.
- Record software versions and simulation configuration.
- Do not assume physical units without verifying kUPS conventions.
- Distinguish bounded energy fluctuations from systematic drift.
- Never infer correctness from visual plausibility alone.
- Keep the notebook as a presentation layer; reusable logic belongs in src/.
- All reported values must be reproducible from committed code and config.

## Publishing requirements

- The executable repository is the source of truth for numerical results.
- The website repository is the source of truth for prose and final figures.
- Only small tabular results are transferred to the website repository.
- Do not commit large trajectories or generated caches.
