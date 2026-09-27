Chunk 1 - source: thread_bike_commute.txt#0 | produced by: chunker.py::split_documents

THREAD: Is a bike worth it for a 20 minute walk commute?

 reply 1 (14 votes) 
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage, covered bike parking exists at three buildings and is full by 9am at all three.

Chunk 2 - source: thread_first_gen.txt#1 
produced by: chunker.py::split_documents

THREAD: Anything specific for first-generation students?

reply 2 (41 votes) 
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

Chunk 3,  source: thread_laptop_specs.txt#2  produced by: chunker.py::split_documents

THREAD: How much laptop do I actually need for CS courses?

reply 3 (12 votes) 
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.

Chunk 4, source: thread_parking.txt#1 | produced by: chunker.py::split_documents

THREAD: Worth getting a parking permit?

 reply 2 (21 votes) 
Street parking on Verrill is legal and free and unmarked, which is why half the upper years do it.

Chunk 5,  source: thread_sleep_schedule.txt#1  produced by: chunker.py::split_documents

THREAD: Everyone says fix your sleep. Does it actually matter?

 reply 2 (37 votes) 
The library being open until 2am is a trap. It's a resource, not a schedule.

## Chunking Strategy

**Chunk size:** I didn't use a fixed size. My chunker splits documents wherever a reply starts, so chunk size depends on how long each reply happens to be.

**Overlap:** None. Each reply becomes its own separate chunk, so nothing repeats between them.

When I ran the original chunker on my corpus, it printed a chunk that was only 2 characters long, basically a broken fragment with nothing useful in it. My corpus is made of threads where each post follows the same pattern: a thread title, then several replies marked like "--- reply 1 (14 votes) ---". Since that structure was already there in the text, I split at those reply markers instead of guessing at a character count. Each chunk keeps the thread title attached so it still makes sense on its own, without needing the other replies around it.

**My relevance cutoff:** 0.6 — the default turned out to be right in the middle of a clean gap.

| Question | In corpus? | Best distance |
|---|---|---|
| How hard is it to change majors in second year? | Yes | 0.208 |
| What should students do if a teammate disappears? | Yes | 0.234 |
| Is there an advising program for first-gen students? | Yes | 0.159 |
| How many times can students change meal plan tier? | Yes | 0.234 |
| Who do students speak with about roommate issues? | Yes | 0.291 |
| What is the capital of Mongolia? | No | 0.893 |
| How do I change oil in a diesel engine? | No | 0.896 |
| Who won the 1994 World Cup? | No | 0.893 |
| Recommended dosage of ibuprofen? | No | 0.807 |
| How do I write a for loop in Rust? | No | 0.835 |

**Question:** How many times can students change their meal plan tier and by when?

**Answer:**
Students can only change their meal plan tier once and only in the first ten days (thread_meal_plan_tier.txt).

Source: thread_meal_plan_tier.txt

## What This Does

I picked the advice_threads corpus, made up of real style student discussion threads. My system answers questions students actually ask each other like changing majors, what to do when a group project teammate disappears, first-gen advising resources, meal plan tiers, and roommate conflicts. Basically everything needed to survive college. It retrieves the most relevant reply from a thread and answers using only that source, naming the file it came from.

## How I Used AI

1. I asked Claude to help me write a custom chunker for my advice_threads corpus, since the starter's fixed-size chunker was cutting threads into meaningless 800-character pieces. It suggested splitting on the "--- reply" markers instead. My first version lost the thread title on each chunk, so I had it add that back in so each chunk could stand alone without the surrounding context.

2. I used Claude to pressure-test my acceptance criteria and test questions before committing to them. It pointed out that several of my original questions (like "are students aware of X") were opinion-based with no checkable right answer, so I rewrote them into specific factual questions with an exact word or phrase the correct answer had to contain.

## Run Log — Before

Produced by `run_eval.py::main` (criteria 1–3) and `python app.py ask` with
caching disabled via `$env:AI201_CACHE = "0"` (criterion 5). Full files
committed in `results/`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks read as complete thought | 4 of 5 | 15/15 | — | — | MET |
| 5. Explains both sides (revised, 1 question) | 1 of 1 | Yes | Yes | Yes | MET |

Criterion 3 is identical across all three columns on purpose — the gate is a
distance-vs-cutoff comparison, not a generation, so it can't vary run to run.
Criterion 4 was checked once against a 15-chunk sample rather than three
times, since re-reading the same static chunks three times wouldn't produce
new information.

### Sample output — Criterion 1

Best distance: 0.2085 (passed the gate)
Sources retrieved: thread_changing_major.txt, thread_transfer_credits.txt

Retrieved chunk (`thread_changing_major.txt`, reply 1):
Administratively trivial — it's a form. The real question is whether the
credits you've taken map onto the new requirements.

Generated answer:
Administratively, changing majors is trivial because it is just a form; the
real question is whether your credits map onto the new requirements
(thread_changing_major.txt).

Produced by run_eval.py::run_once → store.py::search → generate.py::answer_from_chunks.

### Sample output — Criterion 5

Yes, a bike can be worth it because it cuts an 18-minute walk down to about
6 minutes, though storage can be an issue since covered bike parking fills
up by 9 am (thread_bike_commute.txt). Another user notes they keep a cheap
$120 bike for September to November and walk the rest of the year, while a
counterpoint warns that salt from November to March can destroy a
drivetrain in one season (thread_bike_commute.txt).

Produced by app.py::cmd_ask → generate.py::answer_from_chunks, cache disabled.

## Verdicts

### 1. Retrieved chunks contain the answer
Target: 4 of 5 questions. Result was 5/5 across all three runs.**MET.** I confirmed this by reading the raw retrieved chunk text (via`--show-prompt`), not the model's phrased up answer. For all 5 questions,at least one retrieved chunk contained the literal answer. Retrieval is deterministic, so this number can't change between runs, the same question was asked; only the generated wording changes, which criterion 1 isn't measuring.

### 2. Every answer names a source
Target: 5 of 5. Result was  5/5. **MET.** Every one of the 15 generations (5 questions × 3 runs) ended with an explicit filename, either as "Source: `file.txt`" or "(file.txt)". No exceptions.

### 3. The relevance gate stops out-of-corpus questions
Target: 4 of 5. Result was  5/5 (single deterministic pass).**MET.** All 5 out of scope questions had best distances between 0.807 and 0.896,comfortably clear of the 0.6 cutoff, not a close call. Verified live with one question directly, confirming 0 model calls were made for a refusal.

### 4. Sampled chunks read as a complete thought
Target: 4 of 5. Result was 15 of 15 sampled chunks read cleanly,there was no cutoff sentences. **MET.** I sampled 15 of the corpus's 75 chunks (20%) and read each one by hand. None showed the fragment problem that motivated this criterion. Caveat: this doesn't prove the 2-character chunk I originally saw is  from the other 60 chunks. It's a sample, not a full audit.

### 5. Explains both sides of a disagreement (revised)
Revised target: for the 1 question where my corpus has genuine disagreement, the answer explains both sides rather than stating one opinion as fact. Result: 3  out of 3 runs mentioned both the upside (time saved) and the downside(winter drivetrain damage / storage), sourced correctly, with no cache hits.**MET, with a caveat worth being honest about:** all three runs open with aconfident "Yes" and fold the disagreement in as a "but here's a downside,"rather than presenting it as two people actually disagreeing. Only run 3explicitly used the word "counterpoint" and named it as an opposing view.This is a real, repeatable pattern, not a fluke, and it's a softer version of exactly the flattening this criterion exists to catch. I'm calling it MET because the required information, both sides is present every time, but this is the one verdict where a stricter reader could reasonably disagree with me.