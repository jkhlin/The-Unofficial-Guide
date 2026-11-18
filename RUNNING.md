# Running The Unofficial Guide (Path B: local, with logs)

The system runs on this machine as a small web service. It is started by one
command and writes a structured log of every request.

## Environment

| Needs | Detail |
|---|---|
| Python | 3.11, 3.12 or 3.13 (not 3.14) |
| Dependencies | pinned with upper and lower bounds in `requirements.txt` |
| Local model | all-MiniLM-L6-v2 (ONNX), about 80 MB, downloaded automatically on first run from `chroma-onnx-models.s3.amazonaws.com` |
| Vector index | `chroma_db/`, about 16 MB, built locally (it is not committed) |
| API key | `GEMINI_API_KEY` in `.env`. The only paid dependency |

## One-time setup (from a clean checkout)

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env          # then paste your key into .env
python test.py                  # should end: "10 passed, 0 failed"
python app.py index             # builds chroma_db/ (the first run downloads the 80 MB model)
```

macOS / Linux: `python3 -m venv .venv && source .venv/bin/activate`, then the
same `pip install`, `cp .env.example .env`, `python test.py`, `python app.py index`.

## The command that starts it

```
python serve.py
```

It listens on `http://localhost:5000` (set `PORT` to change it).

It does not reload when you edit code. After changing any `.py` file, stop it
(Ctrl-C) and start it again, or it keeps serving the old version (and, for
example, will not write the log).

## Using it

```powershell
curl.exe http://localhost:5000/health
curl.exe -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d "{\"question\": \"How is the workload in CS 340?\"}"
```

## Where the record goes

Every `/ask` request appends one JSON line to `logs/requests.jsonl` (change it
with `AI201_LOG_PATH`). The fields are listed at the top of `instrument.py`:
timestamp, request id, question, answer, refused, best distance, sources,
latency in milliseconds, cache hit, model calls, token counts and any error.

Read it back with:

```
python summarize_log.py
python summarize_log.py --price-in <USD per 1M in> --price-out <USD per 1M out>
```

## Measuring honestly

Repeat questions are answered from `.cache/` with no API call. That is about 60x
faster and costs nothing, so a "cold" measurement needs `AI201_CACHE=0` in the
environment (or a cleared `.cache/`). Each log record has a `cache_hit` field,
and `summarize_log.py` reports live, cached and refused requests separately.

The original command-line interface still works:
`python app.py ask "is the housing lottery random?"`.
