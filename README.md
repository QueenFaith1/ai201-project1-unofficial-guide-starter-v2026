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