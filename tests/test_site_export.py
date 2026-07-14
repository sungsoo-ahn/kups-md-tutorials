from pathlib import Path
import json

from kups_md_tutorials.cli import main
from kups_md_tutorials.site_export import export_site_assets


def _write_export_inputs(root: Path) -> tuple[Path, Path, Path]:
    figures_root = root / "figures"
    results_root = root / "results"
    site_root = root / "site"

    figure_dir = figures_root / "post-01"
    figure_dir.mkdir(parents=True)
    (figure_dir / "initialization_diagnostics_full.svg").write_text(
        "<svg><text>full</text></svg>\n",
        encoding="utf-8",
    )
    (figure_dir / "initialization_diagnostics_full.png").write_bytes(b"png")

    result_dir = results_root / "post-01" / "full"
    result_dir.mkdir(parents=True)
    (result_dir / "manifest.json").write_text('{"post": "01"}\n', encoding="utf-8")
    (result_dir / "summary.json").write_text('{"ok": true}\n', encoding="utf-8")
    (result_dir / "samples.csv").write_text("x,y\n1,2\n", encoding="utf-8")
    (result_dir / "raw.extxyz").write_text("raw\n", encoding="utf-8")

    return figures_root, results_root, site_root


def test_export_site_assets_copies_figures_and_compact_results(tmp_path: Path) -> None:
    figures_root, results_root, site_root = _write_export_inputs(tmp_path)

    manifest_path = export_site_assets(
        site_root=site_root,
        profile="full",
        results_root=results_root,
        figures_root=figures_root,
        posts=("01",),
    )

    assert (
        site_root / "assets/img/blog/kups_md_post01_initialization_diagnostics.svg"
    ).exists()
    assert (
        site_root / "assets/img/blog/kups_md_post01_initialization_diagnostics.png"
    ).exists()
    assert (
        site_root
        / "assets/json/kups-md-tutorials/post-01/full/manifest.json"
    ).exists()
    assert (
        site_root / "assets/json/kups-md-tutorials/post-01/full/samples.csv"
    ).exists()
    assert not (
        site_root / "assets/json/kups-md-tutorials/post-01/full/raw.extxyz"
    ).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["profile"] == "full"
    assert len(manifest["files"]) == 5
    assert {item["kind"] for item in manifest["files"]} == {
        "compact-result",
        "figure",
    }


def test_cli_export_site(tmp_path: Path) -> None:
    figures_root, results_root, site_root = _write_export_inputs(tmp_path)

    assert (
        main(
            [
                "export-site",
                "--site-root",
                str(site_root),
                "--profile",
                "full",
                "--results-dir",
                str(results_root),
                "--figures-dir",
                str(figures_root),
                "--posts",
                "1",
            ]
        )
        == 0
    )
    assert (site_root / "assets/json/kups-md-tutorials/manifest.json").exists()
