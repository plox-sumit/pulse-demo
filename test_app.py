import pytest

from app import UploadError, upload


def test_upload_succeeds():
    assert upload({"a": 1})["status"] == "ok"


def test_upload_retries_transient_failures():
    attempts = []
    assert upload({"a": 1}, _attempts=attempts)["status"] == "ok"
    assert len(attempts) == 3


def test_upload_rejects_empty_payload():
    with pytest.raises(ValueError):
        upload({})


def test_upload_error_is_runtime_error():
    assert issubclass(UploadError, RuntimeError)
