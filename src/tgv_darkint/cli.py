"""Command-line interface for TGV-DarkINT."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

from . import __version__
from .trainer import find_module, load_data, score_answers, validate

BANNER = f"""\
=== TGV-DarkINT v{__version__} ===
Educational OSINT trainer. Synthetic data only. Never touches the dark web.
"""


def title(text: str, out: Callable[[str], None] = print) -> None:
    out(f"\n{'=' * 60}\n{text}\n{'=' * 60}\n")


def show_module(module: dict[str, Any], out: Callable[[str], None] = print) -> None:
    title(f"MODULE {module['module_id']} - {module['title']}", out)
    c = module["content"]
    if "definitions" in c:
        out("## DEFINITIONS\n")
        for term, text in c["definitions"].items():
            out(f"{term.replace('_', ' ').title()}:\n  {text}\n")
    if "key_differences" in c:
        out("## KEY DIFFERENCES\n")
        for d in c["key_differences"]:
            out(f"  - {d}")
        out("")
    if "service_categories" in c:
        out("## SERVICE CATEGORIES\n")
        for name, info in c["service_categories"].items():
            out(f"{name.replace('_', ' ').title()}:\n  {info['description']}")
            out(f"  Detection relevance: {info['detection_relevance']}\n")
    if "ttps" in c:
        out("## TTPs\n")
        for t in c["ttps"]:
            out(f"{t['ttp_id']}: {t['name']}\n  {t['description']}")
            out(f"  MITRE ATT&CK: {', '.join(t['mitre_mapping'])}")
            out(f"  Detection hypothesis: {t['detection_hypothesis']}")
            out(f"  Data sources: {', '.join(t['data_sources'])}")
            out(f"  Synthetic indicator: {t['synthetic_indicators']['log_example']}\n")
    if "detection_exercise" in c:
        ex = c["detection_exercise"]
        out(f"## DETECTION EXERCISE\n\nScenario: {ex['scenario']}\n\nLog entries:")
        for line in ex["log_entries"]:
            out(f"  {line}")
        rule = ex["detection_rule_template"]
        out(f"\nExpected TTPs: {', '.join(ex['expected_ttps'])}")
        out(f"\nRule template:\n  Name: {rule['name']}\n  Logic: {rule['logic']}\n  Severity: {rule['severity']}\n")
    if "workflow_steps" in c:
        sc = c["scenario"]
        out(f"## OSINT WORKFLOW SIMULATION\n\n{sc['title']}\n\nBackground: {sc['background']}\n\nSynthetic intel:")
        for k, v in sc["synthetic_intel"].items():
            out(f"  {k.replace('_', ' ').title()}: {v}")
        out("\n## WORKFLOW STEPS\n")
        for s in c["workflow_steps"]:
            out(f"Step {s['step']}: {s['action']}\n  Guidance: {s['guidance']}")
            out(f"  Expected output: {s['synthetic_output']}\n")


def run_quiz(
    questions: list[dict[str, Any]],
    heading: str,
    ask: Callable[[str], str] = input,
    out: Callable[[str], None] = print,
) -> tuple[int, int]:
    title(f"QUIZ: {heading}", out)
    answers = []
    for i, q in enumerate(questions, 1):
        out(f"Question {i}: {q['question']}")
        for j, opt in enumerate(q["options"], 1):
            out(f"  {j}. {opt}")
        while True:
            raw = ask(f"\nYour answer (1-{len(q['options'])}): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(q["options"]):
                break
            out(f"Enter a number between 1 and {len(q['options'])}.")
        pick = int(raw) - 1
        answers.append(pick)
        if pick == q["correct"]:
            out(f"Correct. {q['explanation']}\n")
        else:
            out(f"Incorrect. Answer: {q['options'][q['correct']]}\n  {q['explanation']}\n")
    right, total = score_answers(questions, answers)
    out(f"Score: {right}/{total} ({right / total * 100:.0f}%)" if total else "No questions.")
    return right, total


def show_exercise(data: dict[str, Any], out: Callable[[str], None] = print) -> None:
    ex = data["assessment"]["practical_exercise"]
    title("PRACTICAL EXERCISE", out)
    out(f"Task: {ex['task']}\n\nRequirements:")
    for r in ex["requirements"]:
        out(f"  - {r}")
    out("\nExample solution:")
    for k, v in ex["example_solution"].items():
        out(f"  {k.replace('_', ' ').title()}: {v}")


def list_modules(data: dict[str, Any], out: Callable[[str], None] = print) -> None:
    for m in data["modules"]:
        n = len(m["content"].get("quiz", []))
        out(f"{m['module_id']}: {m['title']} ({n} quiz questions)")


def interactive(data: dict[str, Any]) -> None:
    print(BANNER)
    while True:
        title("MAIN MENU")
        print("1. Browse modules\n2. Final quiz\n3. Practical exercise\n4. Exit")
        choice = input("\nSelect (1-4): ").strip()
        if choice == "1":
            list_modules(data)
            module = find_module(data, input("\nModule id (or 'b' to go back): "))
            if module is None:
                continue
            show_module(module)
            quiz = module["content"].get("quiz")
            if quiz and input("\nTake this module's quiz? (y/n): ").strip().lower() == "y":
                run_quiz(quiz, module["title"])
        elif choice == "2":
            run_quiz(data["assessment"]["final_quiz"], "Final assessment")
        elif choice == "3":
            show_exercise(data)
        elif choice == "4":
            print("\nEducational use only. Stay curious, stay legal.")
            return
        else:
            print("Invalid option.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tgv-darkint", description="Dark-web terminology and TTP trainer (synthetic data)."
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--data", help="path to an alternative training JSON file")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("modules", help="list modules")
    s = sub.add_parser("show", help="print a module")
    s.add_argument("module_id")
    q = sub.add_parser("quiz", help="take a module quiz, or 'final'")
    q.add_argument("target", help="module id or 'final'")
    sub.add_parser("exercise", help="print the practical exercise")
    sub.add_parser("validate", help="check the training data structure")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = load_data(args.data)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        if args.cmd is None:
            interactive(data)
        elif args.cmd == "modules":
            list_modules(data)
        elif args.cmd == "show":
            module = find_module(data, args.module_id)
            if module is None:
                print(f"error: unknown module '{args.module_id}'", file=sys.stderr)
                return 2
            show_module(module)
        elif args.cmd == "quiz":
            if args.target.lower() == "final":
                run_quiz(data["assessment"]["final_quiz"], "Final assessment")
            else:
                module = find_module(data, args.target)
                quiz = module["content"].get("quiz") if module else None
                if not quiz:
                    print(f"error: no quiz for '{args.target}'", file=sys.stderr)
                    return 2
                run_quiz(quiz, module["title"])
        elif args.cmd == "exercise":
            show_exercise(data)
        elif args.cmd == "validate":
            problems = validate(data)
            print("OK" if not problems else "\n".join(problems))
            return 1 if problems else 0
    except (KeyboardInterrupt, EOFError):
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
