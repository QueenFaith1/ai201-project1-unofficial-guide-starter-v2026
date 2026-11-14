"""Structured run log: one JSON line per question, including failures."""

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("logs") / "run_log.jsonl"


def log_run(question, outcome, duration_s, **extra):
    """Append one record. outcome: answered, refused, or model_error."""
    LOG_PATH.parent.mkdir(exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "question": question,
        "outcome": outcome,
        "duration_s": round(duration_s, 3),
        **extra,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")


def friendly_error(exc):
    """Return (reason, message for the user). The raw error goes in the log."""
    text = str(exc).lower()
    if exc.__class__.__name__ == "QuotaGuard":
        return "session_budget", "This session has made too many requests. Stop the program, look for a loop, and start again."
    if "api key" in text or "api_key" in text:
        return "bad_api_key", "The answer service rejected the API key. Check GEMINI_API_KEY in your .env file."
    if "429" in text or ("rate" in text and "limit" in text):
        return "rate_limited", "The answer service is busy right now. Wait a minute and try again."
    if "timed out" in text or "timeout" in text or "connection" in text:
        return "network", "Couldn't reach the answer service. Check your internet connection and try again."
    return "unknown_error", "Something went wrong while answering your question. The details were saved to the log."