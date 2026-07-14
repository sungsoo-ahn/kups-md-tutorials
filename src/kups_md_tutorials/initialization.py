"""Deterministic initial-state construction for the tutorial series."""

from dataclasses import asdict, dataclass
from pathlib import Path
import json

import ase
from ase import Atoms
from ase.io import write
from ase.md.velocitydistribution import Stationary, thermalize_momenta
import kups
import numpy as np

from kups_md_tutorials.config import TutorialSpec
from kups_md_tutorials.provenance import provenance
from kups_md_tutorials.systems import aluminum_fcc, argon_fcc


@dataclass(frozen=True)
class InitializationSummary:
    """Compact diagnostics for one initialized molecular state."""

    post: str
    profile: str
    atom_count: int
    chemical_formula: str
    volume: float
    number_density: float
    target_temperature_k: float
    instantaneous_temperature_k: float
    kinetic_energy_ev: float
    center_of_mass_speed: float
    seed: int
    config_sha256: str


def build_system(spec: TutorialSpec) -> Atoms:
    """Construct the configured atomic system."""

    system = spec.system
    if system.kind == "argon_fcc":
        if system.number_density is None:
            msg = "argon_fcc requires number_density"
            raise ValueError(msg)
        return argon_fcc(system.repetitions, system.number_density)
    if system.kind == "aluminum_fcc":
        lattice_constant = 4.05 if system.lattice_constant is None else system.lattice_constant
        return aluminum_fcc(system.repetitions, lattice_constant)

    msg = f"unsupported system kind: {system.kind}"
    raise ValueError(msg)


def initialize_atoms(spec: TutorialSpec) -> Atoms:
    """Construct atoms and initialize momenta with a seeded Maxwell distribution."""

    atoms = build_system(spec)
    init = spec.initialization
    rng = np.random.RandomState(init.seed)
    thermalize_momenta(
        atoms,
        init.temperature_k,
        exact_temperature=init.force_exact_temperature,
        rng=rng,
    )
    if init.remove_center_of_mass:
        Stationary(atoms, preserve_temperature=True)
    return atoms


def summarize_initialization(
    atoms: Atoms, spec: TutorialSpec, config_sha256: str
) -> InitializationSummary:
    """Compute compact deterministic diagnostics for an initialized state."""

    momenta = atoms.get_momenta()
    masses = atoms.get_masses()
    total_momentum = np.sum(momenta, axis=0)
    total_mass = float(np.sum(masses))
    center_of_mass_speed = float(np.linalg.norm(total_momentum / total_mass))

    return InitializationSummary(
        post=spec.post,
        profile=spec.profile,
        atom_count=len(atoms),
        chemical_formula=atoms.get_chemical_formula(),
        volume=float(atoms.get_volume()),
        number_density=float(len(atoms) / atoms.get_volume()),
        target_temperature_k=spec.initialization.temperature_k,
        instantaneous_temperature_k=float(atoms.get_temperature()),
        kinetic_energy_ev=float(atoms.get_kinetic_energy()),
        center_of_mass_speed=center_of_mass_speed,
        seed=spec.initialization.seed,
        config_sha256=config_sha256,
    )


def write_initialization_outputs(
    spec: TutorialSpec,
    output_root: Path = Path("results"),
    config_root: Path = Path("configs"),
) -> Path:
    """Initialize a state and write compact outputs for later review."""

    output_dir = output_root / spec.result_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_root / f"post-{spec.post}" / f"{spec.profile}.json"
    config_sha256 = provenance(config_path).config_sha256
    atoms = initialize_atoms(spec)
    summary = summarize_initialization(atoms, spec, config_sha256)

    summary_path = output_dir / "initialization_summary.json"
    manifest_path = output_dir / "manifest.json"
    structure_path = output_dir / "initial_state.extxyz"

    summary_path.write_text(
        json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write(structure_path, atoms, format="extxyz")
    manifest = {
        "config": asdict(spec),
        "summary_file": summary_path.name,
        "structure_file": structure_path.name,
        "provenance": asdict(provenance(config_path)),
        "versions": {
            "ase": ase.__version__,
            "kups": kups.__version__,
            "numpy": np.__version__,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_dir


def load_initialization_summary(path: Path) -> InitializationSummary:
    """Read a previously written initialization summary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    return InitializationSummary(**data)
