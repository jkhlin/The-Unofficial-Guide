#!/usr/bin/env python3
"""
Summarize logs/requests.jsonl — answers questions about past runs without
touching the running service.

    python summarize_log.py                       # default log
    python summarize_log.py path/to/log.jsonl
    python summarize_log.py --price-in 0.10 --price-out 0.40
        # prices in USD per 1,000,000 tokens, copied from the provider's pricing
        # page for the model in config.MODEL. Not assumed here: the token counts
        # are measured, the prices are whatever you pass in.
"""

import argparse
import json
import statistics
from pathlib import Path

import instrument


def percentile(values, pct):
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, round(pct / 100 * (len(ordered) - 1)))
    return ordered[index]


def fmt(value, suffix=""):
    return "n/a" if value is None else f"{value:.1f}{suffix}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log", nargs="?", default=str(instrument.LOG_PATH))
    parser.add_argument("--price-in", type=float, help="USD per 1M input tokens")
    parser.add_argument("--price-out", type=float, help="USD per 1M output tokens")
    args = parser.parse_args()

    path = Path(args.log)
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not records:
        raise SystemExit(f"{path} has no records.")

    ok = [r for r in records if r["status"] == 200]
    errors = [r for r in records if r["status"] != 200]
    refused = [r for r in ok if r["refused"]]
    cached = [r for r in ok if r["cache_hit"]]
    live = [r for r in ok if not r["refused"] and not r["cache_hit"]]

    print(f"{path}: {len(records)} requests")
    print(f"  answered live (model call) : {len(live)}")
    print(f"  served from cache          : {len(cached)}")
    print(f"  refused by the gate        : {len(refused)}")
    print(f"  non-200 (errors / bad input): {len(errors)}")

    for name, group in (("live", live), ("cached", cached), ("refused", refused)):
        latencies = [r["latency_ms"] for r in group]
        if latencies:
            print(
                f"  latency {name:<8} n={len(latencies):<3} "
                f"p50={fmt(percentile(latencies, 50), ' ms')}  "
                f"p95={fmt(percentile(latencies, 95), ' ms')}  "
                f"max={fmt(max(latencies), ' ms')}"
            )

    if live:
        prompt = [r["prompt_tokens"] for r in live]
        output = [r["output_tokens"] for r in live]
        mean_in, mean_out = statistics.mean(prompt), statistics.mean(output)
        print(
            f"  tokens per live run: {mean_in:.0f} in + {mean_out:.0f} out "
            f"(measured over {len(live)} runs)"
        )
        if args.price_in is not None and args.price_out is not None:
            cost = (mean_in * args.price_in + mean_out * args.price_out) / 1_000_000
            print(f"  cost per live run  : ${cost:.6f}  (${cost * 1000:.4f} per 1,000 runs)")
        else:
            print("  (pass --price-in and --price-out to turn tokens into dollars)")


if __name__ == "__main__":
    main()
