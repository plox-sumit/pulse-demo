# pulse-demo

A deliberately broken sample service, used to demo [Pulse](https://github.com/) —
an autonomous engineering teammate that investigates CI failures across channels.

`app.py` imports `backoff` for its retry decorator, but `requirements.txt` only
declares `pytest`. It runs fine on a laptop that happens to have `backoff`
installed and fails in CI — the classic "works on my machine".

Ask Pulse `why did CI fail?` on Slack or Telegram and it reads the Actions logs
and tells you.
