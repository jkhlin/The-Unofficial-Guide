# Burst probe — before

Supplementary check (not one of the five criteria): 20 live requests, back to back, no pacing. Target: 20 of 20 return 200.

| Run | 200s | Non-200s | Median latency | Slowest | Wall time |
|---|---|---|---|---|---|
| 1 | 18/20 | 2 | 1.03 s | 15.5 s | 57.2 s |
| 2 | 20/20 | 0 | 1.04 s | 38.4 s | 68.1 s |
| 3 | 19/20 | 1 | 1.05 s | 15.4 s | 46.2 s |

Verdict: MISSED

- trial 1 error: RuntimeError: Still rate limited after 4 attempts. Wait a minute and try again — your key is fine.
Last error: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, '
- trial 3 error: RuntimeError: Still rate limited after 4 attempts. Wait a minute and try again — your key is fine.
Last error: 429 RESOURCE_EXHAUSTED. {'error': {'code': 429, '