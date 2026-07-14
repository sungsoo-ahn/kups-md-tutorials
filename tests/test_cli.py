from pathlib import Path

from kups_md_tutorials.cli import main


def test_cli_run_and_verify_smoke(tmp_path: Path) -> None:
    assert (
        main(["run", "01", "--profile", "smoke", "--output-dir", str(tmp_path)])
        == 0
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
