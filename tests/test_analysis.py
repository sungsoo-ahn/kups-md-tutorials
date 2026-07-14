from pathlib import Path

import h5py
import numpy as np

from kups_md_tutorials.analysis import load_energies, summarize_energy


def _trajectory(path: Path) -> None:
    with h5py.File(path, "w") as handle:
        step = handle.create_group("group.step")
        step.create_dataset("array.potential_energy", data=np.array([-2.0, -1.9, -1.8]))
        step.create_dataset("array.kinetic_energy", data=np.array([1.0, 0.9, 0.8]))


def test_energy_loader_and_summary(tmp_path: Path) -> None:
    path = tmp_path / "trajectory.h5"
    _trajectory(path)
    potential, kinetic = load_energies(path)
    np.testing.assert_allclose(potential + kinetic, -1.0)
    summary = summarize_energy(path, sample_dt_fs=1.0)
    assert summary.samples == 3
    assert abs(summary.drift_ev_per_ps) < 1.0e-10
