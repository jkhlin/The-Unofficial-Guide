# Acceptance criteria — Capstone (Shape A: deploy and instrument)

Five criteria for the operational layer I added to The Unofficial Guide: the
web service in `serve.py`, its structured request log, and the numbers read
back from that log. Written before any trial has been run. (The Unit 1
criteria that used to be in this file are in git history and in the Unit 2
Verdicts section of the README.)

**How a criterion is judged.** Each criterion is tested in 3 trials. A
criterion is **met** only if all 3 trials meet its target. One bad trial
makes it **missed**, because anything that touches a model or a network can
come out differently twice.

**Words used below.**
- *Cold request*: the first request after `python serve.py` starts. It loads
  the embedding model and builds the keyword index.
- *Warm request*: any later request to the same running process.
- *Live request*: a request that reaches the Gemini API (cache off, question
  passes the gate). *Cached*: answered from `.cache/`. *Refused*: stopped by
  the relevance gate.
- *Trial*: a fresh start of `python serve.py` with a new empty log file, then
  the requests the criterion describes.

**What I already knew when I set the numbers.** In Milestone 3 I measured 10
live requests: about 405 input and 45 output tokens, warm latency 0.74 to
1.26 s, one 10.2 s cold start. These are the only results I have. I set the
targets below to leave some margin over them, not to be certain passes.

Criteria 1 to 4 are about the extension. Criterion 5 is about the system
underneath.

---

## 1. Every request leaves one complete, internally consistent log record

In each trial I send 12 requests: 4 live, 3 cached (repeats of the live ones),
3 refused (out of scope), 2 rejected (empty body, whitespace-only question).
The log file must then have **exactly 12 records**, every record must contain
**all 15 fields** (`ts`, `request_id`, `route`, `status`, `question`,
`answer`, `refused`, `best_distance`, `sources`, `latency_ms`, `cache_hit`,
`model_calls`, `prompt_tokens`, `output_tokens`, `error`, with the field
present even when its value is null), and the class of each record must
match what I sent: live means `model_calls = 1` and tokens above 0, cached
means `cache_hit = true`, `model_calls = 0` and tokens 0, refused means
`refused = true` and `model_calls = 0`. **12 of 12 records correct, 0 missing,
0 extra, in all 3 trials.**

**Why this target:** The log is the only evidence Milestone 5 has, so one
missing or mislabelled record is a hole in the evidence, not a rounding
error. That is why the target is all 12 and not "most". It is exact because
the number of requests I send is known and the log should match it. The
class check matters because the token fields are computed as before-and-after
differences of counters in `generate.py`, and a wrong cache-hit label would
silently corrupt every cost number.

---

## 2. Bad input and a failing model call return a clean error, leave a record, and don't take the service down

In each trial I send 4 failures: an empty JSON body, a whitespace-only
question, a body that is not JSON at all, and (on a second server started with
`AI201_MODEL` set to a model name that does not exist) one valid question
whose model call fails. Each must (a) return the right HTTP status (`400` for
the three bad inputs, `500` for the failed model call) with a JSON `error`
message and no stack trace in the response, (b) leave a log record with that
same `status` and a non-empty `error` field, and (c) be followed by a normal
question that returns `200`, to show the service is still up. **4 of 4
failures handled and 4 of 4 followed by a successful request, in all 3
trials.**

**Why this target:** A failure that shows up only as a missing log line is the
kind I can't diagnose later, so the record is part of the criterion, not just
the status code. The follow-up request is there because the way a small Flask
service really dies is by crashing on one bad request and then answering
nothing, and the only way to see that is to ask again. I include a non-JSON
body because `serve.py` reads the body with `get_json(silent=True)` and I
believe, but have not tested, that this turns it into an empty question. The
real model failure is the case that actually costs something: it is the
one where a user waited and got nothing.

---

## 3. Warm live requests are fast and have no long tail

In each trial I start the service, discard the cold request, then send 10
live requests (`AI201_CACHE=0`, in-scope questions only, one at a time).
**Median latency of the 10 is at most 1.2 s, and the slowest of the 10 is at
most 2.5 s**, as recorded in `latency_ms`. This criterion is about warm
requests only. The cold request is excluded and is reported separately, not
judged.

**Why this target:** Median 1.2 s is about 25% above the 0.95 s average I
measured in Milestone 3, which is tight enough that a real slowdown shows up
and loose enough to absorb normal variation. The maximum is the stricter half
on purpose: the median hides the occasional slow call to the Gemini API, and
that slow call is what a user would notice. 2.5 s is about double the worst
warm request I have seen (1.26 s). Both numbers are for a request that calls
the model, because that is the slowest warm path; cached and refused requests
were around 0.24 s and don't need a separate target. I may miss this one if
the API has a slow patch, and that would be an honest result.

---

## 4. A live answer costs at most $0.0004, as computed from the log alone

In each trial, over the same 10 live requests as criterion 3,
`summarize_log.py` reads the log and computes the mean cost per live request
from the logged `prompt_tokens` and `output_tokens`, at **$0.30 per million
input tokens and $2.50 per million output tokens**. **Mean cost is at most
$0.0004 per live request, and no single live request is logged with 0 tokens
or with more than 1,500 tokens in total.**

**Why this target:** My Milestone 3 measurement was $0.00023 per live
request, so $0.0004 leaves about 70% headroom. It is not a number the system
can meet by accident: if a change made the prompt carry far more retrieved
text, or the model started giving long answers (output tokens cost about 8
times as much as input tokens), the mean would cross it. The per-request
bounds catch two failures that a mean can hide: a request logged with 0
tokens that actually called the model (a broken counter) and a single
runaway-sized prompt. The prices are list prices from third-party pages, not
Google's page, so this is a cost estimate on measured tokens; I'm writing the
target in dollars because that is the unit a person budgets in.

---

## 5. The web service gives the same answer decisions as the command line

For the 5 in-scope questions in `questions.py` and the 5 out-of-scope ones,
`POST /ask` and `python app.py ask` must agree on whether the question is
refused, and for the in-scope ones the web service must name the same set of
source files. **10 of 10 questions agree on the refused/answered decision, and
5 of 5 in-scope questions return the same sources, in all 3 trials.**

**Why this target:** `serve.py` is supposed to be a thin wrapper around
`app.py::ask_pipeline`, and the new code sits between the request and that
function. This is my regression check that the instrumentation did not change
how the system answers. I'm only comparing the decision and the sources, not
the answer text, because the model's wording legitimately varies between
runs and comparing it would measure the model, not my code. The target is all
10 because the gate is a plain threshold on retrieval, which is deterministic
for a given index, so any disagreement would be a real bug and not noise.

---

## Self-check

| # | Names a number or something visible? | Can I run it and read the result? | One thing, not several? | Could it actually be missed? |
|---|---|---|---|---|
| 1 | 12 of 12 records, 15 fields | count lines, check keys with a script | one theme (log integrity) | yes, if any field or label is wrong |
| 2 | 4 of 4 handled, status codes | send the requests, read statuses and log | one theme (bad path) | yes, the non-JSON body is untested |
| 3 | median 1.2 s, max 2.5 s | `latency_ms` in the log | warm latency only | yes, API slow patches |
| 4 | $0.0004, 0 or 1,500 tokens | `summarize_log.py` | cost only | less likely, but the per-request bounds can trip |
| 5 | 10 of 10, 5 of 5 | run both paths and compare | wrapper equivalence | yes, if the wrapper drifted |

None of these turns on "works", "reliable", "good" or "fast" without a
number next to it. Criterion 4 is the one I expect to meet; if it is the only
one I meet, the other targets were probably the right level of hard.

---

## Supplementary probe (added in Milestone 6, not one of the five)

**Added after the first results, and I am saying so.** The five criteria above
were written before any trial. After the first test run showed that the
Gemini free tier allows 15 model calls per minute while `config.py` lets the
service make 30, I added one probe for that gap. It does not replace or
change any of the five, and it is not counted in their verdicts.

**Probe:** send 20 live requests back to back with no pacing (cache off,
in-scope questions, one at a time). **Target: 20 of 20 return `200`.** It is
written down here before the probe is run. Three trials, same as the rest.

**Why 20 of 20:** a user who sends 20 questions in a row should get 20
answers. A `500` caused by the service exceeding its own provider's quota is
a failure of the service, not of the user.
