# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
I picked 4 of 5 because my group project question ("what should students do if a teammate disappears") is fairly specific, and the answer word 'document' appears early in one particular reply rather than being repeated across the whole thread,  so I expect that question might be the hardest one for retrieval to nail."
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
I picked 5 of 5 because the system's code forces a source to be included with every answer. If no source is found, it returns an error instead of a made up answer. So this isn't about how hard the question is, it's about whether the code is doing its job every single time.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
I picked 4 of 5 because the gate relies on a single distance cutoff (0.6), and any single number is a compromise. An out of corpus question that happens to share similar wording with something in my corpus could land close enough to the cutoff to slip through
---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

At least 4 of 5 sampled chunks read as a complete thought, with no sentence cut off at either end.

**Why this target:**
I picked 4 of 5 because when I ran index, one chunk came back only 2 characters long, which told me my current chunking sometimes cuts a document in a way that leaves a fragment with no real content


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->
For at least 2 of 3 questions where my corpus contains disagreeing replies, the answer explains both sides of the trade-off (not just states one opinion as fact).

**Why this target:**
I picked 2 of 3 because my corpus is full of threads where people disagree (like the bike thread), and a system that flattens that disagreement into one confident answer would be misleading students rather than helping them.

I picked 2 of 3 because my corpus is full of threads where people disagree (like the bike thread), and a system that flattens that disagreement into one confident answer would be misleading students rather than helping them.

> **Revised in unit 2:** For the 1 question where my corpus contains a thread
> with clear, explicit disagreement (people directly contradicting each
> other, not just adding separate tips), the answer explains both sides of
> the trade-off rather than stating one opinion as fact.
>
> **Why revised:** When I went looking for the 3 disagreement questions this
> criterion needed, I found only one thread in my corpus with genuine,
> explicit disagreement — thread_bike_commute.txt, where one reply says a
> bike is worth it and the next opens with "Counterpoint, I sold mine" and
> argues the opposite. The rest of my threads are people adding different
> useful tips, not contradicting each other. The criterion assumed disagreement
> was common in my corpus; it isn't, so "2 of 3" had nothing real to measure
> against. This isn't a case of missing my target — the target couldn't be
> tested as written.
---

## Capstone criteria

### 1. A bad key shows a plain message, never the raw error

With an invalid `GEMINI_API_KEY` in `.env`, I ask an in-corpus question with `python app.py ask "..."`. The screen shows "The answer service rejected the API key. Check GEMINI_API_KEY in your .env file." and does not contain the text `ClientError` or `INVALID_ARGUMENT`, in 5 of 5 tries.

**Why this target:** A bad key fails the same way every time, so there is no randomness to allow for. The raw text is supposed to go only to the log, so even one leak means the fix doesn't work.

### 2. Every question leaves exactly one complete log record

I note the line count of `logs/run_log.jsonl`, ask 10 questions (a mix of in-corpus, out-of-scope, and one with a bad key), and count again. The file has exactly 10 new lines, and each has `timestamp`, `question`, `outcome` and `duration_s`. Answered and refused records also have `best_distance`, and `model_error` records have `reason` and `error`. I check by loading each line and comparing its keys. Target: 10 of 10 records.

**Why this target:** The log is the only place I can find out why a question failed. A missing or half-empty record defeats the point, so 9 of 10 would not be good enough.

### 3. A failed question is logged with the real cause

With an invalid key, I ask 5 in-corpus questions. Each one adds a log record with `outcome` set to `model_error`, `reason` set to `bad_api_key`, and a non-empty `error` that contains "API key not valid", in 5 of 5 tries.

**Why this target:** The screen hides the raw error, so the log has to keep it. If the record is missing or the reason is wrong, the failure can't be diagnosed afterward.

### 4. The session budget stops runaway requests

In `config.py` I temporarily set `SESSION_REQUEST_BUDGET = 3`, turn the cache off with `$env:AI201_CACHE="0"`, and run `python app.py ask` in interactive mode. I ask 5 in-corpus questions in a row. Questions 4 and 5 show "This session has made too many requests. Stop the program, look for a loop, and start again." and the usage line at exit says 3 model calls, in 3 of 3 runs. I set the budget back to 300 afterward.

**Why this target:** The real budget is 300 requests, and testing that would burn a lot of calls. Setting it to 3 tests the same check cheaply. The guard is a counter, so it should behave the same every run.

### 5. Out-of-scope questions are refused, logged, and cost nothing

I run the 5 `OUT_OF_SCOPE` questions from `questions.py` through `python app.py ask`. Each one prints exactly "I don't have enough information about that.", adds a log record with `outcome` set to `refused` and `best_distance` greater than 0.6, and the usage line says 0 model calls, in 5 of 5 questions.

**Why this target:** A refused question never reaches the model, so a wrong answer here means the gate failed. An earlier criterion allowed 4 of 5, and this time I want to see whether all 5 hold when the log is also checked.

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
