"""Capstone trials: run each criterion three times and record what happened.

Run it from the project folder, AFTER criteria.md has been committed:

    python capstone_trials.py

It runs the real app (python app.py ask ...) as a separate process for every
question, so what it checks is what a person would see on screen and what ends
up in logs/run_log.jsonl. Results are saved to results/capstone_trials.txt.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import gate
import questions

LOG = Path("logs") / "run_log.jsonl"
RESULTS = Path("results") / "capstone_trials.txt"

BAD_KEY_MESSAGE = (
    "The answer service rejected the API key. Check GEMINI_API_KEY in your .env file."
)
BUDGET_MESSAGE = (
    "This session has made too many requests. Stop the program, look for a loop, "
    "and start again."
)

IN_CORPUS = [
    "How hard is it to change majors in second year?",
    "What should students do if a teammate disappears from a group project?",
    "Is there an advising program for first-generation students?",
    "How many times can students change their meal plan tier and by when?",
    "Who do students speak with about roommate issues?",
]

OUT_OF_SCOPE = [
    item["question"] if isinstance(item, dict) else item
    for item in questions.OUT_OF_SCOPE
][:5]

BAD_KEY_ENV = {"GEMINI_API_KEY": "bad-key-for-testing", "AI201_CACHE": "0"}

BASE_FIELDS = {"timestamp", "question", "outcome", "duration_s"}
EXTRA_FIELDS = {
    "answered": {"best_distance", "sources"},
    "refused": {"best_distance"},
    "model_error": {"reason", "error"},
}

lines = []


def say(text=""):
    print(text, flush=True)
    lines.append(text)


def run_app(args, extra_env=None, stdin=None, code=None):
    """Run the app as its own process and return everything it printed."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env.update(extra_env or {})
    command = [sys.executable, "-c", code] if code else [sys.executable, "app.py", *args]
    done = subprocess.run(
        command,
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=900,
    )
    return (done.stdout or "") + (done.stderr or "")


def log_lines():
    if not LOG.exists():
        return []
    return [l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def new_records(before):
    return [json.loads(l) for l in log_lines()[before:]]


def record_complete(record):
    need = BASE_FIELDS | EXTRA_FIELDS.get(record.get("outcome"), {"<unknown outcome>"})
    return need <= set(record)


def check_key_applied(output):
    if "Sources retrieved:" in output:
        say("STOP: the bad key was not applied (the app still answered).")
        say("Your .env may be overriding the environment. Tell Claude what you see.")
        sys.exit(1)


def trial_bad_key():
    """Criteria 1 and 3, checked on the same runs."""
    c1 = c3 = 0
    for q in IN_CORPUS:
        before = len(log_lines())
        out = run_app(["ask", q], BAD_KEY_ENV)
        check_key_applied(out)
        ok1 = (
            BAD_KEY_MESSAGE in out
            and "ClientError" not in out
            and "INVALID_ARGUMENT" not in out
        )
        recs = new_records(before)
        ok3 = (
            len(recs) == 1
            and recs[0].get("outcome") == "model_error"
            and recs[0].get("reason") == "bad_api_key"
            and "API key not valid" in str(recs[0].get("error", ""))
        )
        c1 += ok1
        c3 += ok3
        say(f"    {'ok ' if ok1 else 'BAD'} screen   | {'ok ' if ok3 else 'BAD'} log record | {q[:50]}")
    return c1, c3


def trial_log_records():
    """Criterion 2: ten questions, ten complete records."""
    before = len(log_lines())
    plan = [(q, None) for q in IN_CORPUS[:4]]
    plan += [(q, None) for q in OUT_OF_SCOPE]
    plan += [(IN_CORPUS[4], BAD_KEY_ENV)]
    for q, env in plan:
        run_app(["ask", q], dict(env or {}, AI201_CACHE="0"))
    recs = new_records(before)
    complete = sum(record_complete(r) for r in recs)
    say(f"    new log lines: {len(recs)} (want 10) | complete records: {complete}")
    outcomes = {}
    for r in recs:
        outcomes[r.get("outcome")] = outcomes.get(r.get("outcome"), 0) + 1
    say(f"    outcomes: {outcomes}")
    return len(recs) == 10 and complete == 10


def trial_budget():
    """Criterion 4: budget patched to 3 inside the test process only."""
    code = (
        "import sys, config; config.SESSION_REQUEST_BUDGET = 3; "
        "sys.argv = ['app.py', 'ask']; import app; app.main()"
    )
    stdin = "\n".join(IN_CORPUS) + "\n\n"
    out = run_app([], {"AI201_CACHE": "0"}, stdin=stdin, code=code)
    blocked = out.count(BUDGET_MESSAGE)
    match = re.search(r"(\d+) model calls", out)
    calls = int(match.group(1)) if match else -1
    say(f"    blocked questions: {blocked} (want 2) | model calls in usage line: {calls} (want 3)")
    return blocked == 2 and calls == 3


def trial_refusals():
    """Criterion 5: five out-of-scope questions."""
    passed = 0
    for q in OUT_OF_SCOPE:
        before = len(log_lines())
        out = run_app(["ask", q])
        recs = new_records(before)
        ok = (
            gate.REFUSAL in out
            and "0 model calls" in out
            and len(recs) == 1
            and recs[0].get("outcome") == "refused"
            and recs[0].get("best_distance", 0) > 0.6
        )
        passed += ok
        dist = recs[0].get("best_distance") if recs else None
        say(f"    {'ok ' if ok else 'BAD'} | best_distance {dist} | {q[:55]}")
    return passed


def main():
    say("CAPSTONE TRIALS  (each criterion run 3 times)")
    say("Files checked: app.py::_ask_one, runlog.py::friendly_error and log_run,")
    say("generate.py::_check_budget, gate.py (REFUSAL), logs/run_log.jsonl")
    say()

    r1, r3 = [], []
    for n in (1, 2, 3):
        say(f"Criteria 1 and 3, trial {n} (bad key, 5 questions):")
        a, b = trial_bad_key()
        r1.append(a)
        r3.append(b)
        say(f"    screen message correct: {a} of 5 | log record correct: {b} of 5")

    r2 = []
    for n in (1, 2, 3):
        say(f"Criterion 2, trial {n} (10 questions, 10 records):")
        r2.append(trial_log_records())

    r4 = []
    for n in (1, 2, 3):
        say(f"Criterion 4, trial {n} (budget set to 3 inside the test process):")
        r4.append(trial_budget())

    r5 = []
    for n in (1, 2, 3):
        say(f"Criterion 5, trial {n} (5 out-of-scope questions):")
        r5.append(trial_refusals())

    say()
    say("=" * 60)
    say("SUMMARY (three trials each)")
    say("=" * 60)
    say(f"1 bad key, plain message      : {r1[0]}/5, {r1[1]}/5, {r1[2]}/5   target 5 of 5")
    say(f"2 ten questions, ten records  : {r2}   target all True")
    say(f"3 failure logged with cause   : {r3[0]}/5, {r3[1]}/5, {r3[2]}/5   target 5 of 5")
    say(f"4 budget stops requests       : {r4}   target all True")
    say(f"5 out-of-scope refused        : {r5[0]}/5, {r5[1]}/5, {r5[2]}/5   target 5 of 5")

    Path("results").mkdir(exist_ok=True)
    RESULTS.write_text("\n".join(lines), encoding="utf-8")
    say()
    say(f"Saved to {RESULTS}")


if __name__ == "__main__":
    main()