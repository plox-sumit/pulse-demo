"""A tiny uploader with retry — the subject of Pulse's demo investigation."""

import backoff  # noqa: F401  <- installed locally, NOT declared in requirements.txt


class UploadError(RuntimeError):
    pass


@backoff.on_exception(backoff.expo, UploadError, max_tries=3, jitter=None)
def upload(payload: dict, _attempts: list | None = None) -> dict:
    """Upload a payload, retrying transient failures with exponential backoff."""
    if _attempts is not None:
        _attempts.append(payload)
        if len(_attempts) < 3:
            raise UploadError("transient upstream failure")
    if not payload:
        raise ValueError("payload must not be empty")
    return {"status": "ok", "bytes": len(str(payload))}
