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
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
