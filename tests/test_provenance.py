from pathlib import Path

from kups_md_tutorials.provenance import provenance


def test_provenance_records_lock_device_and_precision() -> None:
    record = provenance(Path("configs/post-01/smoke.json"))

    assert record.config_sha256
    assert record.lock_path == "uv.lock"
    assert record.lock_sha256 is not None
    assert record.runtime_device
    assert record.precision_policy.startswith("jax_enable_x64=")
