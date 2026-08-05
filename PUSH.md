# The demo repository

A deliberately breakable sample service. Pulse needs a **real** repo with a
**real** red build — a mocked failure would not be judged, and would not
exercise the log-reading path at all.

This directory is committed as-is so anyone can reproduce the demo. The live
copy used for the recording is [plox-sumit/pulse-demo](https://github.com/plox-sumit/pulse-demo).

## The break

`app.py` retries transient upload failures. The retry budget and the failure
threshold have to agree:

```python
@backoff.on_exception(backoff.expo, UploadError, max_tries=3, jitter=None)
def upload(payload, _attempts=None):
    if _attempts is not None:
        _attempts.append(payload)
        if len(_attempts) < 3:          # succeeds on the third attempt
            raise UploadError(...)
```

Change `max_tries=3` to `max_tries=2` — as if tightening latency — and they no
longer agree. Backoff gives up after two tries; the success path on attempt
three is never reached.

```
FAILED test_app.py::test_upload_retries_transient_failures
1 failed, 3 passed
```

**Three of four tests still pass.** That is what makes it realistic: nothing
obviously exploded, and the error message alone does not explain the cause.
Reading `ModuleNotFoundError` off a log is pattern-matching; connecting
`max_tries=2` to a test expecting three attempts is reasoning.

## Set it up

1. Create an empty **public** repo named `pulse-demo`. No README, no .gitignore,
   no licence — it must be empty.

2. Push this directory:

   ```bash
   cd demo-repo
   git init -b main
   git add .
   git commit -m "Add uploader with retry"
   git remote add origin https://github.com/<you>/pulse-demo.git
   git push -u origin main
   ```

   Or, from the repository root, without putting a token in a remote URL:

   ```bash
   python push_demo.py <you>/pulse-demo
   ```

   `push_demo.py` uses the Git Data API and reads `GITHUB_TOKEN` from `.env`.
   Note that writing `.github/workflows/` through the API needs the `workflow`
   token scope — without it GitHub returns a misleading `404`.

3. Point Pulse at it in `.env`:

   ```
   GITHUB_REPO=<you>/pulse-demo
   ```

## Running the demo

Leave the repo **green**, start Pulse, then break it live — that way the
recording shows the transition rather than opening on an existing failure.

```bash
python run.py --interval 20      # baselines existing failures, then watches
# edit app.py: max_tries=3  ->  max_tries=2
python push_demo.py <you>/pulse-demo
```

Then watch the log: `new failure` → `cold-emailed` → `notified`.

See [`../demo-assets/video-script.md`](../demo-assets/video-script.md) for
timings and a shot list.
