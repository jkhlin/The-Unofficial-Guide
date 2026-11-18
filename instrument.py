"""
Instrumentation for the web service (capstone, Shape A).

One structured record per request, appended to a JSON-lines file. Each line is
one JSON object with named fields, so the log can be queried after the fact
(`python summarize_log.py`) without adding any new code to the running service.

Fields written for every /ask request:

    ts               ISO-8601 UTC timestamp of when the request finished
    request_id       short random id, to tell two records apart
    route            "/ask"
    status           HTTP status returned (200, 400, 500)
    question         what came in
    answer           what went out (None on an error)
    refused          True if the relevance gate refused (no model call)
    best_distance    best retrieved cosine distance (lower = closer)
    sources          source files the answer was built from
    latency_ms       wall-clock time for the whole request, in milliseconds
    cache_hit        True if the answer came from .cache/ (no API call)
    model_calls      real calls to the model service made for this request
    prompt_tokens    input tokens the service reported for this request
    output_tokens    output tokens the service reported for this request
    error            "ExceptionType: message" on a failure, else None

Where it writes: logs/requests.jsonl, or the path in AI201_LOG_PATH.
"""

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import config

LOG_PATH = Path(os.getenv("AI201_LOG_PATH", config.ROOT / "logs" / "requests.jsonl"))

_write_lock = threading.Lock()


def new_request_id() -> str:
    return uuid.uuid4().hex[:8]


def write_record(**fields) -> dict:
    """Append one record to the log and return it.

    Logging must never break the request it is describing: if the file can't
    be written, say so on stderr and carry on.
    """
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds")}
    record.update(fields)

    try:
        with _write_lock:
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with LOG_PATH.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        import sys

        print(f"[instrument] could not write log: {exc}", file=sys.stderr)

    return record
