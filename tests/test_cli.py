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
