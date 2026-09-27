## Baseline Run Log

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

### Evidence

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