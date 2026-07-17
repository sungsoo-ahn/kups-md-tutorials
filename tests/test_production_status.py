import json
from pathlib import Path

import pytest

from kups_md_tutorials.cli import main
from kups_md_tutorials.production_status import (
    collect_gpu_status,
    format_gpu_status,
    gpu_status_json,
    verify_selected_gpu_reruns,
)


def test_collect_gpu_status_reports_pending_rerun(tmp_path: Path) -> None:
    result_dir = tmp_path / "post-03" / "full"
    result_dir.mkdir(parents=True)
    summary_path = result_dir / "error_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "post": "03",
                "argon_nve_protocol": {
                    "target_requests_gpu": True,
                    "production_gpu_ready": False,
                    "gpu_blocking_reason": "runtime was jax:cpu;devices:cpu",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    records = collect_gpu_status(
        results_root=tmp_path,
        review_dir=tmp_path / "reviews",
    )

    assert len(records) == 1
    record = records[0]
    assert record.post == "03"
    assert record.profile == "full"
    assert record.summary_path == summary_path
    assert record.record_path == "argon_nve_protocol"
    assert record.status_label == "gpu-target-cpu-fallback"
    assert record.rerun_command == (
        "uv run kups-tutorial run 03 --profile full && "
        "uv run kups-tutorial verify 03 --profile full"
    )

    report = format_gpu_status(records)
    assert "pending GPU reruns: 1" in report
    assert "blocking reason: runtime was jax:cpu;devices:cpu" in report
    assert "uv run kups-tutorial run 03 --profile full" in report

    payload = gpu_status_json(records)
    assert payload["records"] == 1
    assert payload["production_ready"] == 0
    assert payload["pending_gpu_reruns"] == 1
    assert payload["items"][0]["post"] == "03"
    assert payload["items"][0]["status"] == "gpu-target-cpu-fallback"
    assert payload["items"][0]["rerun_command"] == record.rerun_command


def test_collect_gpu_status_adds_review_gpu_blocker_without_runtime_record(
    tmp_path: Path,
) -> None:
    results_root = tmp_path / "results"
    review_dir = tmp_path / "reviews"
    review_dir.mkdir()
    (review_dir / "post-12.md").write_text(
        "# Review\n\n"
        "Final-release blockers:\n\n"
        "- Run and review the real MACE/fcc-Al GPU capstone.\n"
        "- Re-run rendered desktop/mobile snapshots after final diagnostics.\n",
        encoding="utf-8",
    )

    records = collect_gpu_status(results_root=results_root, review_dir=review_dir)

    assert len(records) == 1
    record = records[0]
    assert record.post == "12"
    assert record.source == "review"
    assert record.summary_path == review_dir / "post-12.md"
    assert record.record_path == "final_release_blockers"
    assert record.status_label == "review-gpu-blocker"
    assert record.gpu_blocking_reason == (
        "Run and review the real MACE/fcc-Al GPU capstone."
    )
    assert record.rerun_command == (
        "uv run kups-tutorial run 12 --profile full && "
        "uv run kups-tutorial verify 12 --profile full"
    )


def test_verify_selected_gpu_reruns_filters_to_selected_posts(tmp_path: Path) -> None:
    result_dir = tmp_path / "post-03" / "full"
    result_dir.mkdir(parents=True)
    (result_dir / "error_summary.json").write_text(
        json.dumps(
            {
                "argon_nve_protocol": {
                    "target_requests_gpu": True,
                    "production_gpu_ready": False,
                    "gpu_blocking_reason": "runtime was jax:cpu;devices:cpu",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    records = collect_gpu_status(
        results_root=tmp_path,
        review_dir=tmp_path / "reviews",
    )

    assert verify_selected_gpu_reruns(records, posts=("01", "01")) == ("01",)
    with pytest.raises(ValueError, match="post-03 argon_nve_protocol"):
        verify_selected_gpu_reruns(records, posts=("03",))


def test_verify_gpu_rerun_cli_rejects_pending_selected_post(
    tmp_path: Path,
    capsys,
) -> None:
    result_dir = tmp_path / "post-03" / "full"
    result_dir.mkdir(parents=True)
    (result_dir / "error_summary.json").write_text(
        json.dumps(
            {
                "argon_nve_protocol": {
                    "target_requests_gpu": True,
                    "production_gpu_ready": False,
                    "gpu_blocking_reason": "runtime was jax:cpu;devices:cpu",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as error:
        main(
            [
                "verify-gpu-rerun",
                "--posts",
                "03,04",
                "--results-root",
                str(tmp_path),
                "--review-dir",
                str(tmp_path / "reviews"),
            ]
        )

    assert error.value.code == 1
    assert "Selected GPU rerun is incomplete:" in capsys.readouterr().err


def test_verify_gpu_rerun_cli_accepts_space_separated_posts(
    tmp_path: Path,
    capsys,
) -> None:
    assert (
        main(
            [
                "verify-gpu-rerun",
                "--posts",
                "01 02",
                "--results-root",
                str(tmp_path / "results"),
                "--review-dir",
                str(tmp_path / "reviews"),
            ]
        )
        == 0
    )

    assert "Selected GPU rerun passed for 2 posts: 01, 02" in capsys.readouterr().out


def test_gpu_status_cli_prints_current_pending_records(capsys) -> None:
    assert main(["gpu-status"]) == 0

    output = capsys.readouterr().out

    assert "GPU production status" in output
    assert "pending GPU reruns: 9" in output
    assert "post-03 argon_nve_protocol: gpu-target-cpu-fallback" in output
    assert "post-11 pair_distance_steered: gpu-target-cpu-fallback" in output
    assert "post-12 final_release_blockers: review-gpu-blocker" in output
    assert "Run and review the real MACE/fcc-Al GPU capstone." in output
    assert "uv run kups-tutorial run 03 --profile full" in output


def test_gpu_status_cli_prints_json(capsys) -> None:
    assert main(["gpu-status", "--format", "json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload["records"] == 9
    assert payload["production_ready"] == 0
    assert payload["pending_gpu_reruns"] == 9
    assert payload["items"][0]["post"] == "03"
    assert payload["items"][0]["record_path"] == "argon_nve_protocol"
    assert payload["items"][0]["source"] == "summary"
    assert payload["items"][0]["status"] == "gpu-target-cpu-fallback"
    assert (
        payload["items"][0]["rerun_command"]
        == "uv run kups-tutorial run 03 --profile full && "
        "uv run kups-tutorial verify 03 --profile full"
    )
    assert payload["items"][-1]["post"] == "12"
    assert payload["items"][-1]["source"] == "review"
    assert payload["items"][-1]["status"] == "review-gpu-blocker"
