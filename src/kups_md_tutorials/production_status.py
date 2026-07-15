"""Operational status helpers for final production GPU runs."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class GpuStatusRecord:
    """One GPU readiness record found in a compact summary."""

    post: str
    profile: str
    summary_path: Path
    record_path: str
    target_requests_gpu: bool
    production_gpu_ready: bool
    gpu_blocking_reason: str | None

    @property
    def rerun_command(self) -> str:
        return (
            f"uv run kups-tutorial run {self.post} --profile {self.profile} "
            "&& "
            f"uv run kups-tutorial verify {self.post} --profile {self.profile}"
        )

    @property
    def status_label(self) -> str:
        if self.production_gpu_ready:
            return "production-gpu-ready"
        if self.target_requests_gpu:
            return "gpu-target-cpu-fallback"
        return "not-gpu-targeted"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "post": self.post,
            "profile": self.profile,
            "summary_path": self.summary_path.as_posix(),
            "record_path": self.record_path,
            "target_requests_gpu": self.target_requests_gpu,
            "production_gpu_ready": self.production_gpu_ready,
            "gpu_blocking_reason": self.gpu_blocking_reason,
            "status": self.status_label,
            "rerun_command": (
                self.rerun_command
                if self.target_requests_gpu and not self.production_gpu_ready
                else None
            ),
        }


def collect_gpu_status(
    *,
    results_root: Path = Path("results"),
    profile: str = "full",
) -> tuple[GpuStatusRecord, ...]:
    """Collect GPU readiness records from compact tutorial summaries."""

    records: list[GpuStatusRecord] = []
    for result_dir in sorted(results_root.glob(f"post-*/{profile}")):
        post = result_dir.parent.name.removeprefix("post-")
        for summary_path in sorted(result_dir.glob("*_summary.json")):
            try:
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            _collect_gpu_records(
                summary,
                post=post,
                profile=profile,
                summary_path=summary_path,
                record_path="",
                records=records,
            )
    return tuple(records)


def format_gpu_status(records: tuple[GpuStatusRecord, ...]) -> str:
    """Format GPU readiness records as a compact human-readable report."""

    if not records:
        return "No GPU readiness records found."

    pending = [
        record
        for record in records
        if record.target_requests_gpu and not record.production_gpu_ready
    ]
    ready = [record for record in records if record.production_gpu_ready]
    lines = [
        "GPU production status",
        f"- records: {len(records)}",
        f"- production ready: {len(ready)}",
        f"- pending GPU reruns: {len(pending)}",
        "",
    ]
    for record in records:
        lines.append(
            f"post-{record.post} {record.record_path}: {record.status_label}"
        )
        lines.append(f"  summary: {record.summary_path.as_posix()}")
        if record.gpu_blocking_reason:
            lines.append(f"  blocking reason: {record.gpu_blocking_reason}")
        if record.target_requests_gpu and not record.production_gpu_ready:
            lines.append(f"  rerun: {record.rerun_command}")
    return "\n".join(lines)


def gpu_status_json(records: tuple[GpuStatusRecord, ...]) -> dict[str, Any]:
    """Return a machine-readable GPU readiness report."""

    pending = [
        record
        for record in records
        if record.target_requests_gpu and not record.production_gpu_ready
    ]
    ready = [record for record in records if record.production_gpu_ready]
    return {
        "records": len(records),
        "production_ready": len(ready),
        "pending_gpu_reruns": len(pending),
        "items": [record.to_json_dict() for record in records],
    }


def _collect_gpu_records(
    value: object,
    *,
    post: str,
    profile: str,
    summary_path: Path,
    record_path: str,
    records: list[GpuStatusRecord],
) -> None:
    if isinstance(value, dict):
        required_keys = {
            "target_requests_gpu",
            "production_gpu_ready",
            "gpu_blocking_reason",
        }
        if required_keys <= set(value):
            target_requests_gpu = value.get("target_requests_gpu")
            production_gpu_ready = value.get("production_gpu_ready")
            gpu_blocking_reason = value.get("gpu_blocking_reason")
            if isinstance(target_requests_gpu, bool) and isinstance(
                production_gpu_ready, bool
            ):
                records.append(
                    GpuStatusRecord(
                        post=post,
                        profile=profile,
                        summary_path=summary_path,
                        record_path=record_path or "<root>",
                        target_requests_gpu=target_requests_gpu,
                        production_gpu_ready=production_gpu_ready,
                        gpu_blocking_reason=(
                            gpu_blocking_reason
                            if isinstance(gpu_blocking_reason, str)
                            else None
                        ),
                    )
                )
        for key, child in value.items():
            child_path = f"{record_path}.{key}" if record_path else key
            _collect_gpu_records(
                child,
                post=post,
                profile=profile,
                summary_path=summary_path,
                record_path=child_path,
                records=records,
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{record_path}[{index}]"
            _collect_gpu_records(
                child,
                post=post,
                profile=profile,
                summary_path=summary_path,
                record_path=child_path,
                records=records,
            )
