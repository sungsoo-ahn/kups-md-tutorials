import numpy as np

from kups_md_tutorials.systems import aluminum_fcc, argon_fcc, argon_gas


def test_argon_fcc_matches_requested_density() -> None:
    atoms = argon_fcc(2, number_density=0.02)
    assert len(atoms) == 32
    np.testing.assert_allclose(len(atoms) / atoms.get_volume(), 0.02)


def test_argon_gas_is_seeded() -> None:
    first = argon_gas(8, seed=7)
    second = argon_gas(8, seed=7)
    np.testing.assert_allclose(first.positions, second.positions)


def test_aluminum_supercell_size() -> None:
    assert len(aluminum_fcc(2)) == 32
