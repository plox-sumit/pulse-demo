# pulse-demo

A deliberately breakable sample service, used to demonstrate **Pulse** — an
autonomous engineering teammate that notices CI failures, investigates them,
and reaches the engineer who caused them.

This repository exists to be broken on purpose. It is not a real service.

## The bug it demonstrates

`upload()` retries transient failures. The retry budget and the failure
threshold have to agree with each other:

```python
@backoff.on_exception(backoff.expo, UploadError, max_tries=3, jitter=None)
def upload(payload, _attempts=None):
    if _attempts is not None:
        _attempts.append(payload)
        if len(_attempts) < 3:          # succeeds on the third attempt
            raise UploadError(...)
```

Tighten `max_tries` to `2` — a plausible latency optimisation — and they no
longer agree. Backoff gives up after two tries, so the success path on attempt
three is never reached and the retry test fails forever.

Three of the four tests still pass, so nothing obviously explodes. The error
message alone does not explain the cause, which is the point: it takes reading
the code alongside the log to work out that the retry budget and the failure
threshold are off by one.

## What Pulse does with it

Nobody files a ticket. Pulse polls GitHub Actions, notices the run went red,
downloads the log archive, works out the cause, and then **emails the author of
the failing commit** — someone who has never messaged it — while posting the
full report to Slack and a short alert to Telegram.

See `PUSH.md` for how to set this up yourself.
