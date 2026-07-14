"""Analysis helpers for tutorial trajectory outputs."""

from dataclasses import dataclass
from pathlib import Path

import h5py
import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class EnergySummary:
    """Compact energy-drift diagnostics for one trajectory."""

    samples: int
    initial_energy_ev: float
    final_energy_ev: float
    mean_energy_ev: float
    energy_span_ev: float
    drift_ev_per_ps: float


def _read_dataset(handle: h5py.File, name: str) -> NDArray[np.float64]:
    dataset = handle["group.step"][name]
    return np.asarray(dataset, dtype=np.float64)


def load_energies(path: Path) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Load potential and kinetic energies from a kUPS HDF5 trajectory."""

    with h5py.File(path, "r") as handle:
        potential = _read_dataset(handle, "array.potential_energy")
        kinetic = _read_dataset(handle, "array.kinetic_energy")
    return potential, kinetic


def summarize_energy(path: Path, sample_dt_fs: float) -> EnergySummary:
    """Summarize total-energy stability for regularly sampled trajectory data."""

    if sample_dt_fs <= 0.0:
        msg = "sample_dt_fs must be positive"
        raise ValueError(msg)

    potential, kinetic = load_energies(path)
    total = potential + kinetic
    if total.size == 0:
        msg = "trajectory contains no energy samples"
        raise ValueError(msg)

    elapsed_ps = (total.size - 1) * sample_dt_fs / 1000.0
    drift = 0.0 if elapsed_ps == 0.0 else (total[-1] - total[0]) / elapsed_ps

    return EnergySummary(
        samples=int(total.size),
        initial_energy_ev=float(total[0]),
        final_energy_ev=float(total[-1]),
        mean_energy_ev=float(np.mean(total)),
        energy_span_ev=float(np.max(total) - np.min(total)),
        drift_ev_per_ps=float(drift),
    )
