import json
from pathlib import Path

from kups_md_tutorials.cli import main
from kups_md_tutorials.production_status import collect_gpu_status, format_gpu_status


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

    records = collect_gpu_status(results_root=tmp_path)

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


def test_gpu_status_cli_prints_current_pending_records(capsys) -> None:
    assert main(["gpu-status"]) == 0

    output = capsys.readouterr().out

    assert "GPU production status" in output
    assert "pending GPU reruns: 8" in output
    assert "post-03 argon_nve_protocol: gpu-target-cpu-fallback" in output
    assert "post-11 pair_distance_steered: gpu-target-cpu-fallback" in output
    assert "uv run kups-tutorial run 03 --profile full" in output
