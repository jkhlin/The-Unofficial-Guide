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
