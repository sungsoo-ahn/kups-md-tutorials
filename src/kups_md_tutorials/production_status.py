"""Operational status helpers for final production GPU runs."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import re


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
    source: str = "summary"

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
        if self.source == "review":
            return "review-gpu-blocker"
        if self.target_requests_gpu:
            return "gpu-target-cpu-fallback"
        return "not-gpu-targeted"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "post": self.post,
            "profile": self.profile,
            "summary_path": self.summary_path.as_posix(),
            "record_path": self.record_path,
            "source": self.source,
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
    review_dir: Path = Path("reviews"),
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
    _collect_review_gpu_blockers(
        review_dir=review_dir,
        profile=profile,
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


def _collect_review_gpu_blockers(
    *,
    review_dir: Path,
    profile: str,
    records: list[GpuStatusRecord],
) -> None:
    if not review_dir.exists():
        return

    pending_runtime_posts = {
        record.post
        for record in records
        if record.source == "summary"
        and record.target_requests_gpu
        and not record.production_gpu_ready
    }
    for review_path in sorted(review_dir.glob("post-*.md")):
        post = review_path.stem.removeprefix("post-")
        if post in pending_runtime_posts:
            continue
        text = review_path.read_text(encoding="utf-8")
        blockers = [
            blocker
            for blocker in _final_release_blockers(text)
            if _is_gpu_production_blocker(blocker)
        ]
        if not blockers:
            continue
        records.append(
            GpuStatusRecord(
                post=post,
                profile=profile,
                summary_path=review_path,
                record_path="final_release_blockers",
                target_requests_gpu=True,
                production_gpu_ready=False,
                gpu_blocking_reason="; ".join(blockers),
                source="review",
            )
        )


def _final_release_blockers(text: str) -> tuple[str, ...]:
    match = re.search(
        r"^(?:##\s+)?Final-release blockers(?: after this refresh)?:?\s*\n\s*\n?"
        r"(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        return ()
    section = match.group(1)
    blockers: list[str] = []
    current: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("-"):
            if current:
                blockers.append(" ".join(current))
            current = [stripped.removeprefix("-").strip()]
        elif current and line.startswith((" ", "\t")):
            current.append(stripped)
    if current:
        blockers.append(" ".join(current))
    return tuple(blockers)


def _is_gpu_production_blocker(blocker: str) -> bool:
    lowered = blocker.lower()
    if lowered.startswith("re-run rendered") or "snapshot" in lowered:
        return False
    gpu_terms = ("gpu", "cuda", "mace/fcc-al")
    production_terms = ("production", "capstone", "diagnostic", "run")
    return any(term in lowered for term in gpu_terms) and any(
        term in lowered for term in production_terms
    )
