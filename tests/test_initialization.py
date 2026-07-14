from pathlib import Path

import numpy as np

from kups_md_tutorials.config import load_tutorial_spec
from kups_md_tutorials.initialization import (
    initialize_atoms,
    load_initialization_summary,
    write_initialization_outputs,
)


def test_smoke_config_loads() -> None:
    spec = load_tutorial_spec("01", "smoke")
    assert spec.post == "01"
    assert spec.profile == "smoke"
    assert spec.system.kind == "argon_fcc"
    assert spec.initialization.seed == 2026071401


def test_initialization_is_deterministic_and_stationary() -> None:
    spec = load_tutorial_spec("01", "smoke")
    first = initialize_atoms(spec)
    second = initialize_atoms(spec)
    np.testing.assert_allclose(first.positions, second.positions)
    np.testing.assert_allclose(first.get_momenta(), second.get_momenta())
    np.testing.assert_allclose(np.sum(first.get_momenta(), axis=0), 0.0, atol=1.0e-12)


def test_initialization_outputs_are_compact(tmp_path: Path) -> None:
    spec = load_tutorial_spec("01", "smoke")
    output_dir = write_initialization_outputs(spec, output_root=tmp_path)
    summary_path = output_dir / "initialization_summary.json"
    assert summary_path.exists()
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "initial_state.extxyz").exists()
    summary = load_initialization_summary(summary_path)
    assert summary.atom_count == 32
    np.testing.assert_allclose(summary.number_density, 0.0213)
