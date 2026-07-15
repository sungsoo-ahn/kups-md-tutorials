from pathlib import Path

from kups_md_tutorials.provenance import (
    gpu_blocking_reason,
    provenance,
    runtime_is_gpu,
    target_requests_gpu,
)


def test_provenance_records_lock_device_and_precision() -> None:
    record = provenance(Path("configs/post-01/smoke.json"))

    assert record.config_sha256
    assert record.lock_path == "uv.lock"
    assert record.lock_sha256 is not None
    assert record.runtime_device
    assert record.precision_policy.startswith("jax_enable_x64=")


def test_gpu_target_helpers_explain_cpu_fallback() -> None:
    runtime = "jax:cpu;devices:cpu"

    assert target_requests_gpu("cuda_or_cpu_fallback")
    assert target_requests_gpu("gpu")
    assert not target_requests_gpu("cpu")
    assert not runtime_is_gpu(runtime)
    assert runtime_is_gpu("jax:gpu;devices:gpu")
    assert gpu_blocking_reason("cpu", runtime) is None
    assert gpu_blocking_reason("cuda_or_cpu_fallback", runtime) == (
        "target device requests CUDA/GPU, but generated artifact runtime "
        "was jax:cpu;devices:cpu"
    )
