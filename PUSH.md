# Pushing the demo repo

Pulse needs a real repo with a real red build. This one fails for a real reason:
`app.py` imports `backoff`, `requirements.txt` doesn't declare it.

Verified locally — in a clean venv with only `requirements.txt` installed:

```
E   ModuleNotFoundError: No module named 'backoff'
1 error in 0.18s
```

…and with `backoff` installed, `4 passed`. So the fix Pulse suggests is provably correct.

## 1. Create an empty PUBLIC repo on GitHub

Name it `pulse-demo`. **Do not** add a README, .gitignore, or licence — it must be empty.

## 2. Push main (this makes CI go red)

```bash
cd demo-repo
git init -b main
git add .
git commit -m "Add uploader with retry"
git remote add origin https://github.com/<you>/pulse-demo.git
git push -u origin main
```

Actions runs and fails. That alone powers `why did CI fail?`

## 3. Open a PR (so `investigate PR #1` also works)

```bash
git checkout -b fix/declare-backoff
printf 'backoff>=2.2\n' >> requirements.txt
git commit -am "Declare backoff dependency"
git push -u origin fix/declare-backoff
```

Open the PR on GitHub. It becomes **PR #1**, and its CI goes *green* — which is the
demo's closing beat: Pulse diagnosed the red build, you applied its suggested fix,
CI recovered.

For a red PR instead, push a branch that changes `app.py` without touching
`requirements.txt`.

## 4. Point Pulse at it

In the Pulse `.env`:

```
GITHUB_REPO=<you>/pulse-demo
```
