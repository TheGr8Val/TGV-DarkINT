"""Command-line interface for TGV-DarkINT."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from . import __version__
from .trainer import find_module, load_data, score_answers, validate
from .ui import AMBER, GREEN, RED, Ui

TAGLINE = "Learn the dark web's vocabulary and tradecraft without going there."


def banner(ui: Ui) -> None:
    ui.banner(f"TGV-DarkINT v{__version__}", TAGLINE, "🕸️")
    ui.warn("Educational OSINT trainer. Synthetic data only. This tool never connects to Tor.")


def show_module(module: dict[str, Any], ui: Ui) -> None:
    ui.heading(f"{module['module_id']} · {module['title']}")
    c = module["content"]
    if "overview" in c:
        ui.line(c["overview"])
    if "definitions" in c:
        ui.section("📖 Definitions")
        for term, text in c["definitions"].items():
            ui.kv(term.replace("_", " ").title(), text)
    if "key_differences" in c:
        ui.section("🔍 Key differences")
        ui.bullets(c["key_differences"], "•")
    if "service_categories" in c:
        rows = [
            (n.replace("_", " ").title(), i["description"], i["detection_relevance"])
            for n, i in c["service_categories"].items()
        ]
        ui.section("🏪 Service categories")
        ui.table("Dark-web service types", ["Category", "What it is", "Detection relevance"], rows)
    if "setup_options" in c:
        ui.section("🧰 Pick your setup")
        rows = [(o["name"], o["what"], o["good_for"], o["watch_out"]) for o in c["setup_options"]]
        ui.table("Setup options", ["Option", "What it is", "Good for", "Watch out"], rows)
    if "rules" in c:
        ui.section("✅ Do")
        ui.bullets(c["rules"]["do"], "✓", GREEN)
        ui.section("🚫 Don't")
        ui.bullets(c["rules"]["dont"], "✗", RED)
    if "first_session" in c:
        ui.section("🚀 Your first session, step by step")
        for s in c["first_session"]:
            ui.kv(f"Step {s['step']}", s["action"], indent=0)
            ui.line(f"    {s['detail']}")
    if "legal_ethics" in c:
        ui.section("⚖️  Legal and ethics")
        ui.bullets(c["legal_ethics"], "!", AMBER)
    if "ttps" in c:
        ui.section("🎯 TTPs")
        for t in c["ttps"]:
            ui.panel(
                f"{t['ttp_id']} · {t['name']}",
                [
                    ("What", t["description"]),
                    ("MITRE", ", ".join(t["mitre_mapping"])),
                    ("Hypothesis", t["detection_hypothesis"]),
                    ("Data sources", ", ".join(t["data_sources"])),
                    ("Synthetic IOC", t["synthetic_indicators"]["log_example"]),
                ],
            )
    if "detection_exercise" in c:
        ex = c["detection_exercise"]
        rule = ex["detection_rule_template"]
        ui.section("🧪 Detection engineering exercise")
        ui.kv("Scenario", ex["scenario"])
        ui.line("  Log entries:")
        for entry in ex["log_entries"]:
            ui.line(f"    {entry}")
        ui.kv("Expected TTPs", ", ".join(ex["expected_ttps"]))
        ui.panel(
            f"Rule template · {rule['name']}", [("Logic", rule["logic"]), ("Severity", rule["severity"])]
        )
    if "workflow_steps" in c:
        sc = c["scenario"]
        ui.section(f"🕵️  OSINT workflow simulation: {sc['title']}")
        ui.kv("Background", sc["background"])
        for k, v in sc["synthetic_intel"].items():
            ui.kv(k.replace("_", " ").title(), v)
        ui.section("Workflow steps")
        for s in c["workflow_steps"]:
            ui.kv(f"Step {s['step']}", s["action"], indent=0)
            ui.line(f"    Guidance: {s['guidance']}")
            ui.line(f"    Expected output: {s['synthetic_output']}")


def run_quiz(questions: list[dict[str, Any]], heading: str, ui: Ui) -> tuple[int, int]:
    ui.heading(f"🧠 Quiz: {heading}")
    answers = []
    for i, q in enumerate(questions, 1):
        ui.line(f"Question {i}/{len(questions)}: {q['question']}")
        for j, opt in enumerate(q["options"], 1):
            ui.line(f"  {j}. {opt}")
        while True:
            raw = ui.ask(f"\nYour answer (1-{len(q['options'])}): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(q["options"]):
                break
            ui.warn(f"Enter a number between 1 and {len(q['options'])}.")
        pick = int(raw) - 1
        answers.append(pick)
        if pick == q["correct"]:
            ui.good(f"Correct. {q['explanation']}\n")
        else:
            ui.bad(f"Incorrect. Answer: {q['options'][q['correct']]}")
            ui.line(f"  {q['explanation']}\n")
    right, total = score_answers(questions, answers)
    if total:
        ui.meter(right, total)
    return right, total


def show_exercise(data: dict[str, Any], ui: Ui) -> None:
    ex = data["assessment"]["practical_exercise"]
    ui.heading("🛠️  Practical exercise")
    ui.kv("Task", ex["task"])
    ui.section("Requirements")
    ui.bullets(ex["requirements"], "•")
    ui.section("Example solution")
    for k, v in ex["example_solution"].items():
        ui.kv(k.replace("_", " ").title(), v)


def list_modules(data: dict[str, Any], ui: Ui) -> None:
    rows = [(m["module_id"], m["title"], str(len(m["content"].get("quiz", [])))) for m in data["modules"]]
    ui.table("Modules", ["ID", "Title", "Quiz questions"], rows)


def interactive(data: dict[str, Any], ui: Ui) -> None:
    banner(ui)
    while True:
        ui.heading("Main menu")
        ui.line("1. 📚 Browse modules\n2. 🏁 Final quiz\n3. 🛠️  Practical exercise\n4. 👋 Exit")
        choice = ui.ask("\nSelect (1-4): ").strip()
        if choice == "1":
            list_modules(data, ui)
            module = find_module(data, ui.ask("\nModule id (or 'b' to go back): "))
            if module is None:
                continue
            show_module(module, ui)
            quiz = module["content"].get("quiz")
            if quiz and ui.ask("\nTake this module's quiz? (y/n): ").strip().lower() == "y":
                run_quiz(quiz, module["title"], ui)
        elif choice == "2":
            run_quiz(data["assessment"]["final_quiz"], "Final assessment", ui)
        elif choice == "3":
            show_exercise(data, ui)
        elif choice == "4":
            ui.line("\nEducational use only. Stay curious, stay legal. 💜")
            return
        else:
            ui.warn("Invalid option.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tgv-darkint", description="Dark-web terminology and TTP trainer (synthetic data)."
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--data", help="path to an alternative training JSON file")
    p.add_argument("--plain", action="store_true", help="disable colours and emoji")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("modules", help="list modules")
    s = sub.add_parser("show", help="print a module")
    s.add_argument("module_id")
    q = sub.add_parser("quiz", help="take a module quiz, or 'final'")
    q.add_argument("target", help="module id or 'final'")
    sub.add_parser("exercise", help="print the practical exercise")
    sub.add_parser("validate", help="check the training data structure")
    return p


def main(argv: list[str] | None = None, ui: Ui | None = None) -> int:
    args = build_parser().parse_args(argv)
    ui = ui or Ui(rich=False if args.plain else None)
    try:
        data = load_data(args.data)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        if args.cmd is None:
            interactive(data, ui)
        elif args.cmd == "modules":
            list_modules(data, ui)
        elif args.cmd == "show":
            module = find_module(data, args.module_id)
            if module is None:
                print(f"error: unknown module '{args.module_id}'", file=sys.stderr)
                return 2
            show_module(module, ui)
        elif args.cmd == "quiz":
            if args.target.lower() == "final":
                run_quiz(data["assessment"]["final_quiz"], "Final assessment", ui)
            else:
                module = find_module(data, args.target)
                quiz = module["content"].get("quiz") if module else None
                if not quiz:
                    print(f"error: no quiz for '{args.target}'", file=sys.stderr)
                    return 2
                run_quiz(quiz, module["title"], ui)
        elif args.cmd == "exercise":
            show_exercise(data, ui)
        elif args.cmd == "validate":
            problems = validate(data)
            ui.line("OK" if not problems else "\n".join(problems))
            return 1 if problems else 0
    except (KeyboardInterrupt, EOFError):
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
