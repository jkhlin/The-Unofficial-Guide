# Capstone run log — before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves one complete, consistent log record | 12 of 12 records correct | ✔ 12/12 | ✔ 12/12 | ✔ 12/12 | MET |
| 2. Bad input / failing model: clean error, a record, service stays up | 4 of 4 handled | ✔ 4/4 | ✔ 4/4 | ✔ 4/4 | MET |
| 3. Warm live latency | median <= 1.2s, max <= 2.5s | ✔ median 0.79s / max 1.09s | ✔ median 0.95s / max 1.92s | ✔ median 0.64s / max 1.16s | MET |
| 4. Cost per live answer, from the log | mean <= $0.0004, tokens in (0, 1500] | ✔ $0.000251 mean | ✔ $0.000245 mean | ✔ $0.000245 mean | MET |
| 5. Web service agrees with the CLI | 10/10 decisions, 5/5 sources | ✔ 10/10 & 5/5 | ✔ 10/10 & 5/5 | ✔ 10/10 & 5/5 | MET |

(✔ = that trial met the target, ✘ = it did not.)


Cold start and warm latencies (criterion 3 detail):
- trial 1 cold-start latency: 2.3s; warm latencies (ms): [520, 875, 798, 994, 595, 847, 785, 1085, 647, 570]
- trial 2 cold-start latency: 2.9s; warm latencies (ms): [606, 1616, 770, 1019, 584, 1917, 1011, 761, 896, 1140]
- trial 3 cold-start latency: 2.4s; warm latencies (ms): [609, 621, 657, 586, 840, 499, 788, 679, 1161, 513]
