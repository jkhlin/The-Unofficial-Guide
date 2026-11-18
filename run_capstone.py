#!/usr/bin/env python3
"""
Capstone test harness: runs the five criteria in criteria.md, three trials.

    python run_capstone.py --label before
    python run_capstone.py --label after          # after the improvement

Writes everything it saw to results/capstone_<label>/ :
    trial<N>/c1_log.jsonl ...   the service's own logs, one file per server start
    trial<N>/result.json        every number and the evidence for each criterion
    run_log.md                  the five-row table plus pasted evidence

Each trial starts fresh servers (new process, new empty log, new empty cache),
so nothing carries over between trials. The targets are the ones in
criteria.md and are written here as constants. They must not be edited after
results exist.
"""

import argparse
import json
import os
import socket
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import questions as q  # noqa: E402
import gate  # noqa: E402

# ─── Targets, copied from criteria.md ────────────────────────────────────────
FIELDS = ["ts", "request_id", "route", "status", "question", "answer", "refused",
          "best_distance", "sources", "latency_ms", "cache_hit", "model_calls",
          "prompt_tokens", "output_tokens", "error"]
MEDIAN_MAX_MS = 1200
SLOWEST_MAX_MS = 2500
COST_MAX = 0.0004
PRICE_IN, PRICE_OUT = 0.30, 2.50          # USD per million tokens
TOKENS_MAX_PER_REQUEST = 1500
BAD_MODEL = "gemini-does-not-exist"

IN_SCOPE = [item["question"] for item in q.answered()]
OUT_OF_SCOPE = list(q.OUT_OF_SCOPE)


# ─── Server helpers ──────────────────────────────────────────────────────────

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Server:
    """One `python serve.py` process with its own log and cache."""

    def __init__(self, trial_dir, name, cache=True, model=None):
        self.port = free_port()
        self.log = trial_dir / f"{name}_log.jsonl"
        self.cache_dir = trial_dir / f"{name}_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env.update(PORT=str(self.port), AI201_LOG_PATH=str(self.log),
                   AI201_CACHE_DIR=str(self.cache_dir),
                   AI201_CACHE="1" if cache else "0", PYTHONIOENCODING="utf-8")
        if model:
            env["AI201_MODEL"] = model
        self.proc = subprocess.Popen([sys.executable, "serve.py"], cwd=ROOT, env=env,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.base = f"http://127.0.0.1:{self.port}"
        deadline = time.time() + 90
        while time.time() < deadline:
            try:
                urllib.request.urlopen(self.base + "/health", timeout=2).read()
                return
            except Exception:
                time.sleep(0.5)
        self.stop()
        raise RuntimeError(f"server {name} did not come up")

    def post(self, body, raw=False):
        """POST /ask. Returns (http_status, parsed_json_or_text, raw_text)."""
        data = body.encode() if raw else json.dumps(body).encode()
        req = urllib.request.Request(self.base + "/ask", data=data, method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                text = resp.read().decode("utf-8")
                return resp.status, json.loads(text), text
        except urllib.error.HTTPError as err:
            text = err.read().decode("utf-8")
            try:
                return err.code, json.loads(text), text
            except ValueError:
                return err.code, None, text

    def ask(self, question):
        return self.post({"question": question})

    def records(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines() if line.strip()]

    def stop(self):
        if self.proc.poll() is None:
            if sys.platform == "win32":
                # /T kills this process and its children only (the venv launcher
                # starts the real interpreter as a child).
                subprocess.run(["taskkill", "/PID", str(self.proc.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass


# ─── Criteria ────────────────────────────────────────────────────────────────

def criterion_1(trial_dir):
    """12 requests -> exactly 12 complete, correctly classified records."""
    plan = ([("live", s) for s in IN_SCOPE[:4]]
            + [("cached", s) for s in IN_SCOPE[:3]]
            + [("refused", s) for s in OUT_OF_SCOPE[:3]]
            + [("rejected", ""), ("rejected", "   ")])
    srv = Server(trial_dir, "c1", cache=True)
    try:
        for kind, text in plan:
            srv.ask(text)
        records = srv.records()
    finally:
        srv.stop()

    problems, correct = [], 0
    for i, (kind, text) in enumerate(plan):
        if i >= len(records):
            problems.append(f"request {i + 1} ({kind}): no record")
            continue
        r = records[i]
        missing = [f for f in FIELDS if f not in r]
        ok = not missing and r["question"] == text.strip()
        if kind == "live":
            ok = ok and r["status"] == 200 and r["refused"] is False and r["cache_hit"] is False \
                and r["model_calls"] == 1 and r["prompt_tokens"] > 0 and r["output_tokens"] > 0
        elif kind == "cached":
            ok = ok and r["status"] == 200 and r["cache_hit"] is True and r["model_calls"] == 0 \
                and r["prompt_tokens"] == 0 and r["output_tokens"] == 0
        elif kind == "refused":
            ok = ok and r["status"] == 200 and r["refused"] is True and r["model_calls"] == 0
        else:
            ok = ok and r["status"] == 400
        if ok:
            correct += 1
        else:
            problems.append(f"request {i + 1} ({kind}): missing={missing} record={json.dumps(r)[:200]}")
    extra = max(0, len(records) - len(plan))
    if extra:
        problems.append(f"{extra} extra record(s)")
    met = correct == 12 and len(records) == 12
    return {"met": met, "value": f"{correct}/12", "records": len(records),
            "problems": problems, "evidence": records[:12]}


def criterion_2(trial_dir):
    """Four failures: right status, JSON error, a log record, and the service still up."""
    cases = []  # (label, expected_status, request fn, follow-up question)
    good = Server(trial_dir, "c2_good", cache=True)
    bad = Server(trial_dir, "c2_badmodel", cache=True, model=BAD_MODEL)
    results = []
    try:
        for label, body, raw in [("empty JSON body", {}, False),
                                 ("whitespace-only question", {"question": "   "}, False),
                                 ("body is not JSON", "{this is not json", True)]:
            status, parsed, text = good.post(body, raw=raw)
            follow_status, _, _ = good.ask(IN_SCOPE[0])
            results.append({"case": label, "server": good, "expected": 400, "status": status,
                            "json_error": bool(parsed and parsed.get("error")),
                            "no_traceback": "Traceback" not in text, "follow": follow_status})
        status, parsed, text = bad.ask(IN_SCOPE[1])
        follow_status, _, _ = bad.ask(OUT_OF_SCOPE[0])  # gate refusal needs no model call
        results.append({"case": "model call fails (nonexistent model)", "server": bad,
                        "expected": 500, "status": status,
                        "json_error": bool(parsed and parsed.get("error")),
                        "no_traceback": "Traceback" not in text, "follow": follow_status})
        good_records, bad_records = good.records(), bad.records()
    finally:
        good.stop()
        bad.stop()

    # good server log order: fail, follow, fail, follow, fail, follow
    handled, evidence, problems = 0, [], []
    for i, res in enumerate(results):
        if res["server"] is good:
            fail_rec = good_records[2 * i] if len(good_records) > 2 * i else None
        else:
            fail_rec = bad_records[0] if bad_records else None
        log_ok = bool(fail_rec and fail_rec.get("status") == res["expected"] and fail_rec.get("error"))
        ok = (res["status"] == res["expected"] and res["json_error"] and res["no_traceback"]
              and log_ok and res["follow"] == 200)
        handled += ok
        evidence.append({"case": res["case"], "http_status": res["status"], "follow_up_status": res["follow"],
                         "log_record": fail_rec})
        if not ok:
            problems.append(f"{res['case']}: status={res['status']} (want {res['expected']}) "
                            f"json_error={res['json_error']} no_traceback={res['no_traceback']} "
                            f"log_ok={log_ok} follow_up={res['follow']}")
    return {"met": handled == 4, "value": f"{handled}/4", "problems": problems, "evidence": evidence}


def criterion_3_and_4(trial_dir):
    """10 warm live requests -> latency (criterion 3) and cost (criterion 4)."""
    srv = Server(trial_dir, "c3", cache=False)
    try:
        t0 = time.perf_counter()
        srv.ask(IN_SCOPE[0])                      # the cold request, discarded
        cold_wall = (time.perf_counter() - t0) * 1000
        for i in range(10):
            srv.ask(IN_SCOPE[i % len(IN_SCOPE)])
        records = srv.records()
    finally:
        srv.stop()

    cold, warm = records[0], records[1:11]
    lat = [r["latency_ms"] for r in warm]
    median, slowest = statistics.median(lat), max(lat)
    c3 = {"met": len(warm) == 10 and median <= MEDIAN_MAX_MS and slowest <= SLOWEST_MAX_MS,
          "value": f"median {median / 1000:.2f}s / max {slowest / 1000:.2f}s",
          "median_ms": median, "max_ms": slowest, "cold_ms": cold["latency_ms"],
          "latencies_ms": lat, "evidence": records}

    costs = [(r["prompt_tokens"] * PRICE_IN + r["output_tokens"] * PRICE_OUT) / 1e6 for r in warm]
    mean_cost = statistics.mean(costs)
    bad_tokens = [r["request_id"] for r in warm
                  if r["prompt_tokens"] + r["output_tokens"] == 0
                  or r["prompt_tokens"] + r["output_tokens"] > TOKENS_MAX_PER_REQUEST]
    c4 = {"met": len(warm) == 10 and mean_cost <= COST_MAX and not bad_tokens,
          "value": f"${mean_cost:.6f} mean",
          "mean_cost": mean_cost, "bad_token_requests": bad_tokens,
          "mean_tokens_in": statistics.mean(r["prompt_tokens"] for r in warm),
          "mean_tokens_out": statistics.mean(r["output_tokens"] for r in warm),
          "evidence": warm}
    return c3, c4


def criterion_5(trial_dir):
    """The web service and `python app.py ask` agree on refuse/answer and on sources."""
    srv = Server(trial_dir, "c5", cache=True)
    env = dict(os.environ, AI201_CACHE_DIR=str(srv.cache_dir), AI201_CACHE="1", PYTHONIOENCODING="utf-8")
    rows, decisions_agree, sources_agree = [], 0, 0
    try:
        for question in IN_SCOPE + OUT_OF_SCOPE:
            _, web, _ = srv.ask(question)
            cli = subprocess.run([sys.executable, "app.py", "ask", question], cwd=ROOT, env=env,
                                 capture_output=True, text=True, encoding="utf-8", timeout=180)
            out = cli.stdout
            cli_sources = None
            for line in out.splitlines():
                if line.startswith("Sources retrieved:"):
                    cli_sources = sorted(s.strip() for s in line.split(":", 1)[1].split(","))
            cli_refused = cli_sources is None and gate.REFUSAL in out
            web_refused = bool(web and web.get("refused"))
            same_decision = web is not None and cli_refused == web_refused
            in_scope = question in IN_SCOPE
            same_sources = in_scope and web is not None and sorted(web.get("sources") or []) == (cli_sources or [])
            decisions_agree += same_decision
            sources_agree += bool(same_sources)
            rows.append({"question": question, "web_refused": web_refused, "cli_refused": cli_refused,
                         "web_sources": web.get("sources") if web else None,
                         "web_error": web.get("error") if web else None, "cli_sources": cli_sources,
                         "same_decision": same_decision, "same_sources": same_sources if in_scope else None})
    finally:
        srv.stop()
    return {"met": decisions_agree == 10 and sources_agree == 5,
            "value": f"{decisions_agree}/10 & {sources_agree}/5", "evidence": rows}


# ─── Orchestration ───────────────────────────────────────────────────────────

QUIET_SECONDS = 65  # the free tier allows 15 model calls per minute, shared by every server


def quiet_period(why):
    """Wait out the per-minute quota so one criterion's calls can't starve the next one's."""
    print(f"  (waiting {QUIET_SECONDS}s so {why} starts with a clean per-minute quota)", flush=True)
    time.sleep(QUIET_SECONDS)


def run_trial(out_dir, n):
    trial_dir = out_dir / f"trial{n}"
    trial_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    print(f"\n=== trial {n} ===", flush=True)
    result["c1"] = criterion_1(trial_dir);                 print("  c1", result["c1"]["value"], flush=True)
    quiet_period("criterion 2")
    result["c2"] = criterion_2(trial_dir);                 print("  c2", result["c2"]["value"], flush=True)
    quiet_period("criteria 3 and 4")
    result["c3"], result["c4"] = criterion_3_and_4(trial_dir)
    print("  c3", result["c3"]["value"], "| c4", result["c4"]["value"], flush=True)
    quiet_period("criterion 5")
    result["c5"] = criterion_5(trial_dir);                 print("  c5", result["c5"]["value"], flush=True)
    (trial_dir / "result.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    return result


TARGETS = {
    "c1": ("1. Every request leaves one complete, consistent log record", "12 of 12 records correct"),
    "c2": ("2. Bad input / failing model: clean error, a record, service stays up", "4 of 4 handled"),
    "c3": ("3. Warm live latency", f"median <= {MEDIAN_MAX_MS / 1000:.1f}s, max <= {SLOWEST_MAX_MS / 1000:.1f}s"),
    "c4": ("4. Cost per live answer, from the log", f"mean <= ${COST_MAX}, tokens in (0, {TOKENS_MAX_PER_REQUEST}]"),
    "c5": ("5. Web service agrees with the CLI", "10/10 decisions, 5/5 sources"),
}


def write_run_log(out_dir, label, trials):
    lines = [f"# Capstone run log — {label}", "",
             "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|"]
    for key, (name, target) in TARGETS.items():
        cells = []
        for t in trials:
            cells.append(("✔ " if t[key]["met"] else "✘ ") + t[key]["value"])
        verdict = "MET" if all(t[key]["met"] for t in trials) else "MISSED"
        lines.append(f"| {name} | {target} | " + " | ".join(cells) + f" | {verdict} |")
    lines += ["", "(✔ = that trial met the target, ✘ = it did not.)", ""]
    for key in TARGETS:
        for i, t in enumerate(trials, 1):
            for problem in t[key].get("problems", []):
                lines.append(f"- {key} trial {i}: {problem}")
    extra = [f"- trial {i} cold-start latency: {t['c3']['cold_ms'] / 1000:.1f}s; warm latencies (ms): "
             f"{[round(x) for x in t['c3']['latencies_ms']]}" for i, t in enumerate(trials, 1)]
    lines += ["", "Cold start and warm latencies (criterion 3 detail):", *extra, ""]
    (out_dir / "run_log.md").write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # the table uses check marks
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, help="before or after")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()
    out_dir = ROOT / "results" / f"capstone_{args.label}"
    out_dir.mkdir(parents=True, exist_ok=True)
    trials = []
    for n in range(1, args.trials + 1):
        if n > 1:
            quiet_period(f"trial {n}")
        trials.append(run_trial(out_dir, n))
    print("\n" + write_run_log(out_dir, args.label, trials))


if __name__ == "__main__":
    main()
