"""Render real TGV-DarkINT output to SVG files for the README.

Usage: python scripts/screenshots.py [output_dir]   (default: docs/img)
"""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console

from tgv_darkint.cli import banner, list_modules, run_quiz, show_module
from tgv_darkint.trainer import find_module, load_data
from tgv_darkint.ui import Ui


def render(name: str, title: str, out: Path, draw, width: int = 100) -> None:
    console = Console(record=True, width=width, force_terminal=True, color_system="truecolor", highlight=False)
    ui = Ui(rich=True)
    ui.console = console
    draw(ui)
    path = out / f"{name}.svg"
    console.save_svg(str(path), title=title)
    print(f"wrote {path}")


def fake_answers(console: Console, answers: list[str]):
    it = iter(answers)

    def ask(prompt: str) -> str:
        answer = next(it)
        console.print(f"[bold #ec4899]{prompt}[/]{answer}")
        return answer

    return ask


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/img")
    out.mkdir(parents=True, exist_ok=True)
    data = load_data()
    m5 = find_module(data, "M5")

    def home(ui: Ui) -> None:
        banner(ui)
        list_modules(data, ui)

    def setup(ui: Ui) -> None:
        sections = dict(m5)
        sections["content"] = {k: v for k, v in m5["content"].items() if k in ("overview", "setup_options")}
        show_module(sections, ui)

    def session(ui: Ui) -> None:
        sections = dict(m5)
        keep = ("rules", "first_session")
        sections["content"] = {k: v for k, v in m5["content"].items() if k in keep}
        show_module(sections, ui)

    def quiz(ui: Ui) -> None:
        ui.ask = fake_answers(ui.console, ["2", "1", "2"])
        run_quiz(data["modules"][0]["content"]["quiz"], "Surface vs Deep vs Dark Web", ui)

    render("menu", "tgv-darkint modules", out, home)
    render("tor-setup", "tgv-darkint show M5", out, setup, width=110)
    render("tor-first-session", "tgv-darkint show M5", out, session)
    render("quiz", "tgv-darkint quiz M1", out, quiz, width=90)


if __name__ == "__main__":
    main()
