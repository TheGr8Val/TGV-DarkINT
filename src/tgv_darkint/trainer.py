"""Data loading and quiz logic. No I/O besides reading the training JSON."""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

REQUIRED_TOP_LEVEL = ("tool_name", "version", "legal_disclaimer", "modules", "assessment")


def load_data(path: str | None = None) -> dict[str, Any]:
    """Load the training content. Defaults to the JSON bundled with the package."""
    if path:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        text = resources.files("tgv_darkint").joinpath("data/trainer.json").read_text(encoding="utf-8")
        data = json.loads(text)
    problems = validate(data)
    if problems:
        raise ValueError("invalid training data: " + "; ".join(problems))
    return data


def validate_quiz(questions: list[dict[str, Any]], where: str) -> list[str]:
    problems = []
    for i, q in enumerate(questions, 1):
        label = f"{where} question {i}"
        for key in ("question", "options", "correct", "explanation"):
            if key not in q:
                problems.append(f"{label}: missing '{key}'")
        opts, correct = q.get("options", []), q.get("correct")
        if not isinstance(correct, int) or not 0 <= correct < len(opts):
            problems.append(f"{label}: 'correct' is not a valid option index")
    return problems


def validate(data: dict[str, Any]) -> list[str]:
    """Return a list of structural problems (empty list means valid)."""
    problems = [f"missing top-level key '{k}'" for k in REQUIRED_TOP_LEVEL if k not in data]
    if problems:
        return problems
    ids = set()
    for m in data["modules"]:
        mid = m.get("module_id", "?")
        if mid in ids:
            problems.append(f"duplicate module id {mid}")
        ids.add(mid)
        for key in ("module_id", "title", "content"):
            if key not in m:
                problems.append(f"module {mid}: missing '{key}'")
        problems += validate_quiz(m.get("content", {}).get("quiz", []), f"module {mid}")
    problems += validate_quiz(data["assessment"].get("final_quiz", []), "final quiz")
    return problems


def find_module(data: dict[str, Any], module_id: str) -> dict[str, Any] | None:
    wanted = module_id.strip().upper()
    return next((m for m in data["modules"] if m["module_id"].upper() == wanted), None)


def score_answers(questions: list[dict[str, Any]], answers: list[int]) -> tuple[int, int]:
    """Score zero-based answer indexes against a quiz. Returns (correct, total)."""
    right = sum(1 for q, a in zip(questions, answers) if a == q["correct"])
    return right, len(questions)
