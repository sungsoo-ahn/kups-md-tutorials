import json
from pathlib import Path

import pytest

from kups_md_tutorials.cli import main
from kups_md_tutorials.workflows import run_post, verify_post


def test_cli_run_and_verify_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "01", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    manifest = json.loads(
        (tmp_path / "post-01" / "smoke" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["execution"]["elapsed_seconds"] > 0.0
    assert manifest["execution"]["max_full_profile_seconds"] == 3600
    assert (
        manifest["execution"]["measured_by"]
        == "kups_md_tutorials.workflows.run_post"
    )
    assert (
        main(["verify", "01", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post02_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "02", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "02", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post03_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "03", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "03", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post04_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "04", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "04", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post05_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "05", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "05", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post06_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "06", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "06", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post07_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "07", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "07", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post08_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "08", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "08", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post09_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "09", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "09", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post10_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "10", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "10", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post11_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "11", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "11", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_cli_run_and_verify_post12_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "12", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )
    assert (
        main(["verify", "12", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
    )


def test_full_run_requires_verified_smoke_outputs(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="missing expected output files"):
        run_post("02", "full", output_root=tmp_path)


def test_full_run_succeeds_after_smoke_verification(tmp_path: Path) -> None:
    run_post("02", "smoke", output_root=tmp_path)
    verify_post("02", "smoke", output_root=tmp_path)

    run_post("02", "full", output_root=tmp_path)
    verify_post("02", "full", output_root=tmp_path)
