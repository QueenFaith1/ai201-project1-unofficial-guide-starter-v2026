"""Measure what one question costs: ten real questions, cache OFF.

Run it from the project folder:

    python measure_cost.py

Each question goes through app._ask_one, so every run also writes a record to
logs/run_log.jsonl. Tokens and seconds are read from the real calls (generate.py
counts what the service reports), not worked out from a pricing page.
"""

import os

# The cache has to be off BEFORE config is imported, or repeat questions would
# be served from disk and cost nothing.
os.environ["AI201_CACHE"] = "0"

import time
from pathlib import Path

import app
import config
import generate as gen

QUESTIONS = [
    "How hard is it to change majors in second year?",
    "What should students do if a teammate disappears from a group project?",
    "Is there an advising program for first-generation students?",
    "How many times can students change their meal plan tier and by when?",
    "Who do students speak with about roommate issues?",
    "Is a bike worth it for a 20 minute walk commute?",
    "How much laptop do I need for CS courses?",
    "Is it worth getting a parking permit?",
    "Does fixing my sleep schedule actually matter?",
    "What should first-generation students know that nobody tells them?",
]

rows = []
for number, question in enumerate(QUESTIONS, 1):
    tokens_before = gen.token_counts()["total"]
    calls_before = gen.call_count()
    started = time.time()

    app._ask_one(question, config.CORPUS, "default", None, None, show_distances=False)

    seconds = time.time() - started
    calls = gen.call_count() - calls_before
    tokens = gen.token_counts()["total"] - tokens_before
    rows.append((number, question, seconds, calls, tokens))

answered = [r for r in rows if r[3] > 0]

lines = []
lines.append("")
lines.append("=" * 70)
lines.append("COST MEASUREMENT (cache off)")
lines.append("=" * 70)
lines.append(f"{'#':<3} {'seconds':<9} {'model calls':<12} {'tokens':<8} question")
for number, question, seconds, calls, tokens in rows:
    lines.append(f"{number:<3} {seconds:<9.2f} {calls:<12} {tokens:<8} {question[:50]}")

lines.append("")
lines.append(f"questions run:                 {len(rows)}")
lines.append(f"questions that called model:   {len(answered)}")
lines.append(f"questions refused by the gate: {len(rows) - len(answered)}")
if answered:
    avg_tokens = sum(r[4] for r in answered) / len(answered)
    lines.append(f"average tokens per answered question: {avg_tokens:.1f}")
    lines.append(f"average seconds per answered question: {sum(r[2] for r in answered) / len(answered):.2f}")
lines.append(f"average seconds across all {len(rows)} questions: {sum(r[2] for r in rows) / len(rows):.2f}")
lines.append("")
lines.append(gen.usage())

report = "\n".join(lines)
print(report)

Path("results").mkdir(exist_ok=True)
Path("results", "cost_measurement.txt").write_text(report, encoding="utf-8")
print("\nSaved to results/cost_measurement.txt")