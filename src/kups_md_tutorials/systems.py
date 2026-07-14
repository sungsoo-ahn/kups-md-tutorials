"""Small deterministic atomistic systems used by tutorial smoke tests."""

import numpy as np
from ase import Atoms
from ase.build import bulk


def argon_fcc(repetitions: int, number_density: float) -> Atoms:
    """Build an FCC argon supercell with the requested number density."""

    if repetitions <= 0:
        msg = "repetitions must be positive"
        raise ValueError(msg)
    if number_density <= 0.0:
        msg = "number_density must be positive"
        raise ValueError(msg)

    conventional_atoms = 4
    cell_length = (conventional_atoms / number_density) ** (1.0 / 3.0)
    return bulk("Ar", "fcc", a=cell_length, cubic=True).repeat(
        (repetitions, repetitions, repetitions)
    )


def argon_gas(num_atoms: int, seed: int, box_length: float = 30.0) -> Atoms:
    """Build a seeded dilute argon gas in a cubic periodic box."""

    if num_atoms <= 0:
        msg = "num_atoms must be positive"
        raise ValueError(msg)
    if box_length <= 0.0:
        msg = "box_length must be positive"
        raise ValueError(msg)

    rng = np.random.default_rng(seed)
    positions = rng.uniform(0.0, box_length, size=(num_atoms, 3))
    return Atoms(
        symbols=["Ar"] * num_atoms,
        positions=positions,
        cell=[box_length, box_length, box_length],
        pbc=True,
    )


def aluminum_fcc(repetitions: int, lattice_constant: float = 4.05) -> Atoms:
    """Build an FCC aluminum supercell for later MLFF diagnostics."""

    if repetitions <= 0:
        msg = "repetitions must be positive"
        raise ValueError(msg)
    if lattice_constant <= 0.0:
        msg = "lattice_constant must be positive"
        raise ValueError(msg)

    return bulk("Al", "fcc", a=lattice_constant, cubic=True).repeat(
        (repetitions, repetitions, repetitions)
    )
