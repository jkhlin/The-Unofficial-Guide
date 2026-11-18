# The Unofficial Guide

Jason Lin Campus_Life corpus

---

# Unit 1

## What This Does

The Unofficial Guide is a RAG system that answers questions using the campus_life corpus. The documents contain student-focused information about topics such as housing, dining, courses, campus jobs, and university services. The system splits the documents into chunks, creates embeddings for them, and retrieves the most relevant chunks for a user's question. It then generates an answer using only the retrieved information and refuses questions that are too far outside the corpus.

## Chunking Strategy

**Chunk size:** Up to 700 characters. I originally used the starter's fixed 800-character chunks, but my campus_life documents are mostly short posts with natural paragraph boundaries. Many of the documents already contain one focused topic, so cutting them at an arbitrary character count could split a complete thought unnecessarily. I changed the chunker to split around paragraphs and combine related short paragraphs up to about 700 characters.

**Overlap:** 0 characters. I used no overlap because the chunks are split at natural paragraph boundaries instead of in the middle of sentences. This lets the chunks keep their context without repeating text between neighboring chunks. After re-indexing, the corpus produced 88 chunks from 88 documents, with chunk lengths ranging from 178 to 549 characters.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: admin_add_drop_deadline.txt#0 `` — produced by: chunker.py::split_documents``

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a Won your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

**Chunk 2** — source: course_biol_160.txt#0 `` — produced by: chunker.py::split_documents``

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

**Chunk 3** — source: course_hist_118_workload.txt#0 `` — produced by: chunker.py::split_documents``

Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

**Chunk 4** — source: dining_pellew_dining_hall_followup.txt#0 `` — produced by: chunker.py::split_documents``

Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

**Chunk 5** — source: housing_innisfree_hall.txt#0 `` — produced by: chunker.py::split_documents``

Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question: ** How is the workload in CS 340?

**Answer:** 

(best distance 0.255, cutoff 0.69)

The workload for CS 340 is 6 hours a week early on, increasing to 15 hours a week in the last three weeks when the project lands, and it is front-loaded sothe first month is heavier than the rest. 

Source: `course_cs_340_workload.txt`

Sources retrieved: course_cs_210_workload.txt, course_cs_340_workload.txt, course_stat_150_workload.txt

**My relevance cutoff:** 0.69

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---:|
| How is the workload in CS 340? | Yes | 0.2547 |
| When does study abroad programs start? | Yes | 0.3165 |
| What is Innisfree Hall condition like? | Yes | 0.4858 |
| How many on campus jobs are there? | Yes | 0.4956 |
| What food does The Atrium have? | Yes | 0.5615 |
| What is the capital of Mongolia? | No | 0.8246 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| Who won the 1994 World Cup? | No | 0.8859 |
| How do I write a for loop in Rust? | No | 0.8960 |
| How do I change the oil in a diesel engine? | No | 0.9340 |

I compared the best retrieval distance for questions that my corpus covers with questions that are clearly outside the corpus. The in-corpus questions I tested had best distances between about 0.25 and 0.56, while the out-of-scope questions had best distances between about 0.82 and 0.93. Since there was a large gap between the highest relevant distance and the lowest out-of-scope distance, I chose a cutoff of 0.69, near the middle of that gap.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** One way I used AI was while designing my chunking strategy. I showed the AI examples from my corpus and asked how I could improve the starter's fixed 800-character chunker. It suggested splitting around paragraph boundaries and keeping short headings attached to their content. The first version was more complicated than I wanted, so I simplified it while keeping the main idea of preserving complete thoughts instead of cutting text at arbitrary character positions.

**2.** I also used AI while tuning retrieval in Milestone 4. I gave it the distance scores from my in-corpus and out-of-scope questions and asked how to interpret them. It pointed out the gap between my highest in-corpus distance, about 0.56, and my lowest out-of-scope distance, about 0.82. I used that observation to choose a relevance cutoff of 0.69. I also changed top-k from 5 to 3 after looking at my retrieval results because the useful chunks were usually already among the first few results and later results were often less relevant.

**3.** I used AI while analyzing the results from `run_eval.py`. I showed it the before-run output and the generated answers and asked it to help identify patterns in the failures. This helped me separate two different issues: several question-level failures were caused by my exact-string scorer, while the campus-jobs question exposed a real retrieval limitation because the retrieved chunks did not contain the requested count.

**4.** I also used AI while deciding on an improvement for Milestone 4. Based on the retrieval failure, I asked about hybrid search and used the response to help understand how BM25 could be combined with semantic retrieval. I then implemented hybrid retrieval and reran the full evaluation.

**5.** After the after-run, I used AI again to compare the before and after results. The comparison showed that hybrid search changed some of the secondary retrieved documents, but the criterion-level scores stayed the same and the campus-jobs question was still not answered.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks match the topic of the question | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Having a wrong city or location listed in at least one response | At least 1 | 0/5 | 0/5 | 0/5 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

#### Criterion 1 — Retrieved chunk contains the answer

Produced by: `run_eval.py::main`  
Retrieval: `store.py::search`

Example from Run 1:

Question: `How is the workload in CS 340?`

Retrieved sources:
`course_cs_210_workload.txt`, `course_cs_340_workload.txt`, `course_stat_150_workload.txt`

Actual output:

> The workload for CS 340 requires 6 hours a week early on, increasing to 15 hours a week in the last three weeks when the project lands, and it is front-loaded with the first month being heavier than the rest.
>
> Source: course_cs_340_workload.txt

Four of the five test questions had the answer available in the retrieved chunks. The exception was:

Question: `How many on campus jobs are there?`

Actual output:

> I do not have enough information to answer how many on-campus jobs there are.
>
> Source: money_jobs.txt, admin_campus_jobs_and_financial_aid.txt, housing_aldridge_hall.txt


#### Criterion 2 — Every answer names a source

Produced by: `run_eval.py::main`

Example from Run 1:

Question: `What is Innisfree Hall condition like?`

Actual output:

> Innisfree Hall was built in 1991 and renovated in 2022. It features double rooms arranged in pairs that share one bathroom between two rooms, but it does not have air conditioning.
>
> Source: housing_innisfree_hall.txt

All 5 of 5 answers named at least one source in all three runs.


#### Criterion 3 — Gate stops out-of-corpus questions

Produced by: `run_eval.py::check_out_of_scope`

Actual output:

> refused (best distance 0.825) What is the capital of Mongolia?
> refused (best distance 0.934) How do I change the oil in a diesel engine?
> refused (best distance 0.886) Who won the 1994 World Cup?
> refused (best distance 0.844) What is the recommended dosage of ibuprofen for a headache?
> refused (best distance 0.896) How do I write a for loop in Rust?
> gate refused 5 of 5

## Verdicts

### Criterion 1 — Retrieved chunk contains the answer
**Target:** 4 of 5  
**Runs:** 4/5, 4/5, 4/5  
**Verdict: MET**

The criterion was met because at least 4 of the 5 test questions had the answer present in the retrieved chunks in every run.

### Criterion 2 — Every answer names a source
**Target:** 5 of 5  
**Runs:** 5/5, 5/5, 5/5  
**Verdict: MET**

The criterion was met because all five generated answers named at least one source in all three runs.

### Criterion 3 — Gate stops out-of-corpus questions
**Target:** 4 of 5  
**Runs:** 5/5, 5/5, 5/5  
**Verdict: MET**

The criterion was met because the relevance gate refused all five out-of-corpus questions, exceeding the target of 4 of 5.

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | At least 4 of the 5 questions had the answer available in the retrieved chunks in all three runs, so the 4-of-5 target held every time. |
| 2 | Every answer names a source | MET | All 5 answers named at least one source document in all three runs, meeting the 5-of-5 target. |
| 3 | Relevance gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-corpus questions. Since retrieval and the gate are deterministic, the result is 5/5 for all three run columns, which exceeds the 4-of-5 target. |
| 4 | Retrieved chunks match the topic of the question | MET | For all 5 test questions, at least one of the top three retrieved results matched the main topic being asked about, such as `course_cs_340_workload.txt` for CS 340 and `dining_the_atrium.txt` for The Atrium. |
| 5 | Having a wrong city or location listed in at least one response | MISSED | None of the responses contained a wrong city or location. Because the original criterion literally requires at least one response to contain a wrong city or location, the criterion was not met as written. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

### Criterion 5 — Wrong city or location

**Stage:** Criterion design (observed at generation)

Criterion 5 was missed because none of the 15 generated answers contained an unsupported city or location. This is not actually a failure of the RAG system. The original criterion was written backwards: it treats producing a wrong location as a successful result.

The generation stage is specifically instructed in `generate.py` to use only the retrieved documents and not introduce outside information. Because the retrieved context did not contain unrelated locations and the grounding prompt tells the model not to guess, the system avoided the behavior that Criterion 5 accidentally requires.

The mechanism behind this miss is therefore a problem with how I defined the criterion rather than a failure in the retrieval or generation pipeline. A better criterion would measure whether zero responses introduce unsupported locations.

### Scorer mismatch

**Stage:** Evaluation/scoring

Several answers contained the correct information but were still marked as `fail` because `scorer.py` checks whether the exact `expects` string appears in the generated answer.

For example:

**Question:** `When does study abroad programs start?`

**Expected:** `In the month of October.`

**Actual output:**

> Applications for study abroad open in October for the following academic year.

The answer contains the correct information, but it does not contain the exact expected phrase, so the scorer marked it as `fail`.

The same issue happened with questions such as CS 340 and Innisfree Hall. The generated answers contained relevant information, but the wording did not exactly match the `expects` string.

---

### Campus jobs question

**Stage:** Retrieval

**Question:** `How many on campus jobs are there?`

**Retrieved documents:**

- `admin_campus_jobs_and_financial_aid.txt`
- `housing_aldridge_hall.txt`
- `money_jobs.txt`

**Actual output:**

> I do not have enough information to answer how many on-campus jobs there are.

The retriever found documents related to campus jobs, but the retrieved chunks did not contain the specific number needed to answer the question.

Because the answer was not available in the retrieved context, the model correctly refused to invent a number.

The failure happened at the retrieval stage because semantic search found documents about the correct topic, but not a chunk containing the exact fact the question required.

---

### Pattern across the failures

There were two main patterns in the failed question-level results.

First, several failures were caused by the scorer requiring an exact phrase instead of accepting a correct paraphrase.

Second, the campus jobs question exposed a real retrieval limitation. The system retrieved documents about the correct topic, but the specific fact needed to answer the question was not present in the retrieved chunks.

Criterion 1 still met its original target of `4/5`, but it only met the minimum threshold. If I tightened this criterion to `5/5`, the campus jobs question would expose this retrieval weakness more clearly.

## The Improvement

**What I changed:**
I changed retrieval from semantic search only to hybrid search. The new retrieval method combines the existing embedding-based similarity search with BM25 keyword search so that exact words and phrases can influence which chunks are returned.

**Why I picked it:**
I chose hybrid search because my diagnosis showed a retrieval weakness on the question How many on campus jobs are there?. The original semantic search found documents related to campus jobs, but it did not retrieve enough specific information to answer the requested count. BM25 may help because it gives more weight to exact terms such as campus, jobs, and other wording from the question.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks match the topic of the question | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Having a wrong city or location listed in at least one response | At least 1 | 0/5 | 0/5 | 0/5 | MISSED |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

The hybrid-search change affected which secondary documents were retrieved, but it did not improve the criterion-level results.

Before the change, Criterion 1 was `4/5` in all three runs, and after the change it remained `4/5` in all three runs.

The main problem I was trying to fix also remained. For the question `How many on campus jobs are there?`, hybrid search retrieved `admin_campus_jobs_and_financial_aid.txt` and `money_jobs.txt`, but the retrieved context still did not contain the specific number needed to answer the question. The system therefore continued to respond that it did not have enough information.

The change did modify some retrieval results. For example, the CS 340 query retrieved `course_cs_340_exams.txt` after the change, and The Atrium query retrieved `dining_the_atrium.txt` and `dining_the_atrium_followup.txt`. However, these changes did not improve any of the five acceptance-criterion scores.

Therefore, hybrid search did not measurably improve the system on this test set.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

Criterion 5 is still missed after the improvement.

The original criterion says that at least one response should contain a wrong city or location. In both the before and after runs, none of the responses introduced a wrong city or location, so the criterion remained `MISSED` as written.

The problem is with the wording of the criterion rather than the system behavior. The system avoiding unsupported locations is actually the behavior I want. If I continued working on this project, I would revise the criterion so that it measures whether the system avoids introducing unsupported cities or locations.

I would change it to something like:

`None of the 5 test-question responses should introduce a city or location that is not supported by the retrieved documents.`

I stopped here because the assignment only requires one measured improvement, and my Milestone 4 change focused on the retrieval weakness identified in the campus-jobs question.

The campus-jobs question also remains a limitation even though Criterion 1 still technically passes at `4/5`. The system continues to retrieve documents related to campus jobs without retrieving the specific count needed to answer `How many on campus jobs are there?`

If I continued improving the system, I would inspect the underlying corpus to confirm whether the number `2` is actually present in a chunk. If it is present, I would further tune retrieval to make that chunk rank higher. If the information is not present in the corpus, retrieval cannot solve the problem and the corpus itself would need to include that fact.


## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

If I wrote the acceptance criteria again, I would change Criterion 5 because its wording accidentally treats a wrong location as a successful result. I intended to measure the opposite: whether the system avoids introducing locations that are unsupported by the retrieved documents.

I would also consider making Criterion 1 stricter. The original target was `4 of 5`, which the system met in every run, but the same campus-jobs question failed consistently. A `5 of 5` target would have made that retrieval weakness more visible.


---

# Capstone

**The System**

I'm extending **The Unofficial Guide**, the campus_life RAG system from Units 1 and 2 (this repository). It's the system whose weak points I know best from writing its Unit 2 criteria, run log and diagnoses. It already has retrieval, a relevance gate, a grounded prompt, and a Flask wrapper (`serve.py`) that serves the same `app.py::ask_pipeline` over HTTP.

**The Shape**

I picked **Shape A: Deploy and instrument**, on **Path B (local with logs)**. The system has only ever run as a one-shot command (`app.py`) or as a bare Flask shell (`serve.py`) with, by design, no logging, no timing and no metrics. What I'm adding is the operational layer:

- a structured JSON-lines log, one record per request, with named fields: timestamp, question in, answer out, whether it was refused, best distance, sources, and end-to-end latency;
- timing and token counts around the stages of a request, so I can report latency and cost per run from measurement rather than from the docs;
- a single documented command that starts the service from a clean checkout, written up in `RUNNING.md` along with what the environment needs (Python version, pinned dependencies, the roughly 80 MB local embedding model);
- a committed run record: a real session's log pasted into this README as text.

I'm taking Path B because the system carries a local ONNX embedding model, which is a poor fit for a 512 MB free host, and because Path B makes me write down a run that someone else can reproduce.

**Out of Scope**

- **No change to retrieval or answer quality.** I'm not touching the chunker, the threshold, the hybrid/BM25 search, or the prompt. I considered finally fixing the campus-jobs retrieval miss from Unit 2, but that would be Shape C, and it would change the system I'm measuring.
- **No cloud deployment.** No hosting account, container image or URL. Path B only; a hosted run is a stretch goal I'm not committing to.
- **No new interface and no metrics stack.** I'm not building a dashboard, Prometheus, or a log shipper. The log is a plain `.jsonl` file that I summarize with a short script.
- **No hardening.** I'm not adding retries, timeouts or failure injection beyond what `generate.py` already does. That is Shape B.

**Size check**

Roughly an hour of building: wrap `/ask` in `serve.py` with timing and a JSONL writer, capture token usage from the generation call, rewrite `RUNNING.md`, and write a small summarizing script. If the token-usage capture turns out to need changes deep inside `generate.py`, I will fall back to measuring cost from latency and the model's published per-token price, and say so.


**Instrumentation**

Every `/ask` request writes one JSON line (see `instrument.py` for the field list) to `logs/requests.jsonl`, or to the path in `AI201_LOG_PATH`. Errors and rejected input are logged the same way as successful answers, so a failure leaves a record instead of an absence. The log is written by `serve.py` around `app.py::ask_pipeline`, which is unchanged. `python summarize_log.py <file>` reads it back.

The extract below is the **complete, unedited** record of a 12-request session, committed as `results/m3_instrumentation.jsonl`. It was run with the cache on, so it contains a mix of live answers, cache hits and refusals. The three non-200 entries at the end are the failure path: two rejected inputs (an empty body and a whitespace-only question, both `400`) and one real server error (`500`), which I forced by starting the service with `AI201_MODEL=gemini-does-not-exist` so the model call failed. Nothing failed on its own during normal use.

```json
{"ts": "2026-11-18T05:10:34.389+00:00", "request_id": "02e1e4e9", "route": "/ask", "status": 200, "question": "When does study abroad programs start?", "latency_ms": 9357.5, "answer": "Applications for the study abroad program open in October for the following academic year (admin_study_abroad.txt).", "refused": false, "best_distance": 0.3165, "sources": ["admin_add_drop_deadline.txt", "admin_study_abroad.txt", "course_cs_340.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 383, "output_tokens": 24, "error": null}
{"ts": "2026-11-18T05:10:34.901+00:00", "request_id": "6878c8c6", "route": "/ask", "status": 200, "question": "How is the workload in CS 340?", "latency_ms": 236.2, "answer": "The workload for CS 340 requires 6 hours a week early on, increasing to 15 hours a week during the last three weeks when the project lands (course_cs_340_workload.txt). It is front-loaded, meaning the first month is heavier than the rest, partly because you are learning the format (course_cs_340_workload.txt).", "refused": false, "best_distance": 0.2547, "sources": ["course_cs_210_workload.txt", "course_cs_340_exams.txt", "course_cs_340_workload.txt"], "cache_hit": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T05:10:36.028+00:00", "request_id": "9d6a27ee", "route": "/ask", "status": 200, "question": "What is Innisfree Hall condition like?", "latency_ms": 831.6, "answer": "Innisfree Hall was built in 1991 and renovated in 2022. It features double rooms arranged in pairs that share one bathroom between two rooms, but it lacks air conditioning. \n\n*(Source: housing_innisfree_hall.txt)*", "refused": false, "best_distance": 0.4858, "sources": ["housing_innisfree_hall.txt", "housing_innisfree_hall_laundry.txt", "housing_innisfree_hall_noise.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 449, "output_tokens": 57, "error": null}
{"ts": "2026-11-18T05:10:37.154+00:00", "request_id": "1397874f", "route": "/ask", "status": 200, "question": "What food does The Atrium have?", "latency_ms": 844.2, "answer": "The Atrium has genuinely good sandwiches in grab-and-go refrigerated cases. \n\nSources: `dining_the_atrium.txt` and `dining_the_atrium_followup.txt`", "refused": false, "best_distance": 0.5615, "sources": ["dining_the_atrium.txt", "dining_the_atrium_followup.txt", "dining_verrill_street_grill.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 483, "output_tokens": 44, "error": null}
{"ts": "2026-11-18T05:10:38.313+00:00", "request_id": "dd797441", "route": "/ask", "status": 200, "question": "How many on campus jobs are there?", "latency_ms": 877.0, "answer": "Based on the provided documents, there is no mention of the total number of on-campus jobs available. \n\nSource: `money_jobs.txt` and `admin_campus_jobs_and_financial_aid.txt`", "refused": false, "best_distance": 0.4956, "sources": ["admin_campus_jobs_and_financial_aid.txt", "admin_wifi_and_accounts.txt", "money_jobs.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 352, "output_tokens": 48, "error": null}
{"ts": "2026-11-18T05:10:38.819+00:00", "request_id": "804cf72a", "route": "/ask", "status": 200, "question": "How is the workload in CS 340?", "latency_ms": 239.7, "answer": "The workload for CS 340 requires 6 hours a week early on, increasing to 15 hours a week during the last three weeks when the project lands (course_cs_340_workload.txt). It is front-loaded, meaning the first month is heavier than the rest, partly because you are learning the format (course_cs_340_workload.txt).", "refused": false, "best_distance": 0.2547, "sources": ["course_cs_210_workload.txt", "course_cs_340_exams.txt", "course_cs_340_workload.txt"], "cache_hit": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T05:10:39.371+00:00", "request_id": "7d34072d", "route": "/ask", "status": 200, "question": "What food does The Atrium have?", "latency_ms": 259.2, "answer": "The Atrium has genuinely good sandwiches in grab-and-go refrigerated cases. \n\nSources: `dining_the_atrium.txt` and `dining_the_atrium_followup.txt`", "refused": false, "best_distance": 0.5615, "sources": ["dining_the_atrium.txt", "dining_the_atrium_followup.txt", "dining_verrill_street_grill.txt"], "cache_hit": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T05:10:39.906+00:00", "request_id": "096905fe", "route": "/ask", "status": 200, "question": "What is the capital of Mongolia?", "latency_ms": 229.6, "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.8246, "sources": [], "cache_hit": false, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T05:10:40.451+00:00", "request_id": "1abfa5f8", "route": "/ask", "status": 200, "question": "How do I write a for loop in Rust?", "latency_ms": 259.3, "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.9002, "sources": [], "cache_hit": false, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T05:10:40.742+00:00", "request_id": "53cdb7d1", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.1, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
{"ts": "2026-11-18T05:10:41.048+00:00", "request_id": "55a8a930", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.2, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
{"ts": "2026-11-18T05:11:02.642+00:00", "request_id": "7f816e6d", "route": "/ask", "status": 500, "question": "Where can I print on campus?", "latency_ms": 10401.3, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": null, "prompt_tokens": null, "output_tokens": null, "error": "ClientError: 404 NOT_FOUND. {'error': {'code': 404, 'message': 'models/gemini-does-not-exist is not found for API version v1beta, or is not supported for generateContent. Call ModelService.ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}"}
```

What the session shows, from `python summarize_log.py results/m3_instrumentation.jsonl`: 4 live answers, 3 cache hits, 2 gate refusals, 3 non-200. Median latency was about 0.9 s for a live answer, about 0.24 s for a cache hit and about 0.23 s for a refusal. The slowest live answer (about 9.4 s) was the first request after the service started, which pays for loading the embedding model and building the BM25 index. Later live requests were around 1 s, so "warm" and "first request" are different numbers and the criteria will say which one they mean.

**What It Costs**

*Measurement.* I started the service with `AI201_CACHE=0` so that every request is a real model call, then sent my five test questions from `questions.py` twice each (10 requests). The service logged the token counts that the Gemini API reported back for each request (`usage_metadata`), and `summarize_log.py` averaged them. The raw record is committed as `results/m3_cost_runs.jsonl`. I also checked one raw response: `thoughts_token_count` was empty and the total was exactly prompt plus output tokens, so there are no hidden "thinking" tokens missing from the count.

| | Measured over 10 live runs |
|---|---|
| Input tokens per run | 405 on average (352 to 483) |
| Output tokens per run | 45 on average (22 to 77) |
| Latency, first request (cold start) | 10.2 s |
| Latency, the other 9 (warm) | 0.95 s on average (0.74 to 1.26 s) |

*Cost per run:* about **$0.00023**, or about **$0.23 per 1,000 questions**. That is 405 tokens at $0.30 per million plus 45 tokens at $2.50 per million. The tokens are measured. The two prices are not: I took them from third-party pricing pages, not from Google's own page, so treat the dollar figure as an estimate built on a measured token count. Output tokens are about 10% of the tokens but about half of the cost. Under this course's free tier the actual spend is $0.

A cache hit or a refused question makes no model call, so it costs nothing and its token fields are 0. The $0.00023 applies only to a question that reaches the model.


**Capstone Run Log**

Run with `python run_capstone.py --label before --trials 3` (harness: `run_capstone.py`; targets copied from `criteria.md`, which was committed before any trial). Everything the run produced is in `results/capstone_before/`, including each trial's own service logs and `run_log.md`. Before the official run I did one throwaway trial to debug the harness itself. Its output was deleted and is not counted.

Each trial starts new `python serve.py` processes with a new empty log and a new empty cache, so nothing carries over between trials or between criteria. Because the Gemini free tier allows only 15 model calls per minute, the harness waits 65 s between criteria. That keeps each criterion's result about my service and not about the previous criterion using up the quota.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves one complete, consistent log record | 12 of 12 records correct | 12/12 | 12/12 | 12/12 | MET |
| 2. Bad input / failing model: clean error, a record, service stays up | 4 of 4 handled | 4/4 | 4/4 | 4/4 | MET |
| 3. Warm live latency | median ≤ 1.2 s and max ≤ 2.5 s | 0.79 s / 1.09 s | 0.95 s / 1.92 s | 0.64 s / 1.16 s | MET |
| 4. Cost per live answer, from the log | mean ≤ $0.0004, no request at 0 or over 1,500 tokens | $0.000251 | $0.000245 | $0.000245 | MET |
| 5. Web service agrees with the CLI | 10/10 decisions and 5/5 sources | 10/10 and 5/5 | 10/10 and 5/5 | 10/10 and 5/5 | MET |

All five criteria were met in all three trials. Criterion 3 in trial 2 came closest to missing (slowest warm request 1.92 s against the 2.5 s limit).

*Am I really re-running?* Yes. In every trial all 10 warm requests in criteria 3 and 4 were live model calls (`model_calls = 1`, `cache_hit = false`, 30 of 30), and the latency and cost numbers differ from trial to trial. The input-token counts repeat exactly because I send the same five prompts each time, and the output tokens (which the model chooses) are what move the cost.

*Evidence from trial 1.* Each block is raw output, unedited, from `results/capstone_before/trial1/`.

**Criterion 1.** One record of each class from `c1_log.jsonl` (live, cached, refused, rejected), written by `instrument.py::write_record` and called from `serve.py::ask`. The file holds all 12 records. The harness check is `run_capstone.py::criterion_1`.

```json
{"ts": "2026-11-18T06:42:26.914+00:00", "request_id": "2e388c5a", "route": "/ask", "status": 200, "question": "When does study abroad programs start?", "latency_ms": 2906.4, "answer": "Applications for study abroad open in October for the following academic year (admin_study_abroad.txt).", "refused": false, "best_distance": 0.3165, "sources": ["admin_add_drop_deadline.txt", "admin_study_abroad.txt", "course_cs_340.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 383, "output_tokens": 22, "error": null}
{"ts": "2026-11-18T06:42:30.234+00:00", "request_id": "48e50991", "route": "/ask", "status": 200, "question": "When does study abroad programs start?", "latency_ms": 79.1, "answer": "Applications for study abroad open in October for the following academic year (admin_study_abroad.txt).", "refused": false, "best_distance": 0.3165, "sources": ["admin_add_drop_deadline.txt", "admin_study_abroad.txt", "course_cs_340.txt"], "cache_hit": true, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T06:42:30.527+00:00", "request_id": "4207cf3c", "route": "/ask", "status": 200, "question": "What is the capital of Mongolia?", "latency_ms": 56.4, "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.8246, "sources": [], "cache_hit": false, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": null}
{"ts": "2026-11-18T06:42:30.647+00:00", "request_id": "afb31b8e", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.1, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
```

**Criterion 2.** The four failures, with the HTTP status the client got, the status of the follow-up request, and the status in the log record. `serve.py::ask` produced the responses and `instrument.py::write_record` the log lines below; the harness check is `run_capstone.py::criterion_2`.

| Failure | HTTP status | Follow-up request | Status in log |
|---|---|---|---|
| empty JSON body | 400 | 200 | 400 |
| whitespace-only question | 400 | 200 | 400 |
| body is not JSON | 400 | 200 | 400 |
| model call fails (nonexistent model) | 500 | 200 | 500 |

```json
{"ts": "2026-11-18T06:43:39.158+00:00", "request_id": "5db72a14", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.1, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
{"ts": "2026-11-18T06:43:41.410+00:00", "request_id": "2443491f", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.3, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
{"ts": "2026-11-18T06:43:41.500+00:00", "request_id": "4ce7d779", "route": "/ask", "status": 400, "question": "", "latency_ms": 0.1, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "error": "no question in request"}
{"ts": "2026-11-18T06:43:43.795+00:00", "request_id": "b8ea526c", "route": "/ask", "status": 500, "question": "How is the workload in CS 340?", "latency_ms": 2231.7, "answer": null, "refused": null, "best_distance": null, "sources": [], "cache_hit": null, "model_calls": null, "prompt_tokens": null, "output_tokens": null, "error": "ClientError: 404 NOT_FOUND. {'error': {'code': 404, 'message': 'models/gemini-does-not-exist is not found for API version v1beta, or is not supported for generateContent. Call ModelService.ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}"}
```

**Criterion 3.** Latencies of the 10 warm live requests in ms, from the `latency_ms` field written by `serve.py::ask`: `[520.4, 875.1, 797.5, 993.7, 595.1, 847.1, 784.9, 1085.4, 646.9, 569.6]`. Median 791 ms, maximum 1085 ms. The cold request that was discarded took 2324 ms. Two of the raw records:

```json
{"ts": "2026-11-18T06:45:16.233+00:00", "request_id": "53df70c0", "route": "/ask", "status": 200, "question": "When does study abroad programs start?", "latency_ms": 520.4, "answer": "Applications for the study abroad program open in October for the following academic year (admin_study_abroad.txt).", "refused": false, "best_distance": 0.3165, "sources": ["admin_add_drop_deadline.txt", "admin_study_abroad.txt", "course_cs_340.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 383, "output_tokens": 24, "error": null}
{"ts": "2026-11-18T06:45:17.120+00:00", "request_id": "c990f7a7", "route": "/ask", "status": 200, "question": "How is the workload in CS 340?", "latency_ms": 875.1, "answer": "The workload for CS 340 is 6 hours a week early on, and 15 hours a week in the last three weeks when the project lands. It is front-loaded, meaning the first month is heavier than the rest. \n\nSources: `course_cs_340_workload.txt`", "refused": false, "best_distance": 0.2547, "sources": ["course_cs_210_workload.txt", "course_cs_340_exams.txt", "course_cs_340_workload.txt"], "cache_hit": false, "model_calls": 1, "prompt_tokens": 360, "output_tokens": 68, "error": null}
```

**Criterion 4.** Computed by `run_capstone.py::criterion_3_and_4` from the same 10 log records. Input tokens `[383, 360, 449, 483, 352, 383, 360, 449, 483, 352]`, output tokens `[24, 68, 59, 47, 48, 22, 88, 56, 61, 44]`. At $0.30 and $2.50 per million that is a mean of $0.000251 per live answer; no request had 0 tokens or more than 1,500.

**Criterion 5.** The ten questions through `POST /ask` (`serve.py::ask`) and through `python app.py ask` (`app.py::cmd_ask`), compared by `run_capstone.py::criterion_5`. Sources are the web service's; the CLI printed the same set for every answered question.

| Question | Web | CLI | Sources | Same sources? |
|---|---|---|---|---|
| When does study abroad programs start? | answered | answered | admin_add_drop_deadline.txt, admin_study_abroad.txt, course_cs_340.txt | same |
| How is the workload in CS 340? | answered | answered | course_cs_210_workload.txt, course_cs_340_exams.txt, course_cs_340_workload.txt | same |
| What is Innisfree Hall condition like? | answered | answered | housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_innisfree_hall_noise.txt | same |
| What food does The Atrium have? | answered | answered | dining_the_atrium.txt, dining_the_atrium_followup.txt, dining_verrill_street_grill.txt | same |
| How many on campus jobs are there? | answered | answered | admin_campus_jobs_and_financial_aid.txt, admin_wifi_and_accounts.txt, money_jobs.txt | same |
| What is the capital of Mongolia? | refused | refused | - | - |
| How do I change the oil in a diesel engine? | refused | refused | - | - |
| Who won the 1994 World Cup? | refused | refused | - | - |
| What is the recommended dosage of ibuprofen for a headache? | refused | refused | - | - |
| How do I write a for loop in Rust? | refused | refused | - | - |

**What this run does not cover.** The pacing means the 15-per-minute API limit was never hit during the official trials. In the throwaway trial, where I did not pace, it was hit: the service answered `500` with `Still rate limited after 4 attempts`, because `config.py` allows 30 calls per minute while the free tier allows 15 and the retries wait only 15 s in total. I did not write a criterion for that, so it is a finding and not a verdict. Also, the empty body, whitespace-only question and non-JSON body all return `400` with the same log line (`"no question in request"`), so the log cannot tell them apart.
