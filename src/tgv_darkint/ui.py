"""Terminal presentation: styled with rich on a TTY, plain text otherwise."""

from __future__ import annotations

import re
import sys
from collections.abc import Callable, Sequence

try:
    from rich import box
    from rich.console import Console
    from rich.markup import escape
    from rich.padding import Padding
    from rich.panel import Panel
    from rich.table import Table

    HAVE_RICH = True
except ImportError:  # pragma: no cover - rich is a declared dependency
    HAVE_RICH = False

EMOJI_RE = re.compile(r"[\U0001F000-\U0001FFFF←-⇿☀-➿⬀-⯿️]")

PURPLE, PINK, TEAL, AMBER, RED, GREEN = "#a855f7", "#ec4899", "#2dd4bf", "#fbbf24", "#f87171", "#4ade80"


def _clean(line: str) -> str:
    if not EMOJI_RE.search(line):
        return line
    indent = line[: len(line) - len(line.lstrip())]
    body = EMOJI_RE.sub("", line.lstrip())
    return indent + re.sub(r" {2,}", " ", body.lstrip())


class Ui:
    """Output helper. ``rich=None`` auto-detects a TTY; ``rich=False`` forces plain text."""

    def __init__(self, rich: bool | None = None, out: Callable[[str], None] = print):
        want = sys.stdout.isatty() if rich is None else rich
        self.rich = bool(want and HAVE_RICH)
        if self.rich:  # emoji and box-drawing need UTF-8 (Windows consoles default to cp1252)
            for stream in (sys.stdout, sys.stderr):
                if hasattr(stream, "reconfigure"):
                    stream.reconfigure(encoding="utf-8", errors="replace")
        self.out = out
        self.console = Console(highlight=False) if self.rich else None

    def _emit(self, text: str) -> None:
        """Plain-mode output: strip emoji and symbols so logs and ASCII consoles stay clean."""
        self.out("\n".join(_clean(line) for line in text.split("\n")))

    # -- basics -------------------------------------------------------------
    def line(self, text: str = "") -> None:
        if self.rich:
            indent = len(text) - len(text.lstrip(" "))
            self.console.print(Padding(escape(text.lstrip(" ")), (0, 0, 0, indent)))
        else:
            self._emit(text)

    def banner(self, name: str, tagline: str, icon: str = "") -> None:
        if self.rich:
            head = f"{icon} {name}" if icon else name
            body = f"[bold {PINK}]{escape(head)}[/]\n[{PURPLE}]{escape(tagline)}[/]"
            self.console.print(Panel(body, border_style=PURPLE, box=box.DOUBLE, padding=(1, 4), expand=False))
        else:
            self._emit(f"=== {name} ===\n{tagline}")

    def heading(self, text: str) -> None:
        if self.rich:
            self.console.print()
            self.console.rule(f"[bold {PINK}]{escape(text)}[/]", style=PURPLE)
        else:
            self._emit(f"\n{'=' * 60}\n{text}\n{'=' * 60}\n")

    def section(self, text: str) -> None:
        if self.rich:
            self.console.print(f"\n[bold {TEAL}]{escape(text)}[/]")
        else:
            self._emit(f"\n## {text}\n")

    def kv(self, label: str, value: str, indent: int = 2) -> None:
        pad = " " * indent
        if self.rich:
            self.console.print(f"{pad}[{PURPLE}]{escape(label)}:[/] {escape(str(value))}")
        else:
            self._emit(f"{pad}{label}: {value}")

    def bullets(self, items: Sequence[str], mark: str = "-", color: str | None = None) -> None:
        for item in items:
            if self.rich:
                grid = Table.grid(padding=(0, 1))
                grid.add_column(width=3, justify="right")
                grid.add_column()
                grid.add_row(f"[{color or PURPLE}]{escape(mark)}[/]", escape(item))
                self.console.print(grid)
            else:
                self._emit(f"  {mark if mark.isascii() else '-'} {item}")

    # -- status -------------------------------------------------------------
    def good(self, text: str) -> None:
        self._status(text, "OK", "✔", GREEN)

    def bad(self, text: str) -> None:
        self._status(text, "X", "✘", RED)

    def warn(self, text: str) -> None:
        self._status(text, "!", "⚠", AMBER)

    def _status(self, text: str, plain_mark: str, mark: str, color: str) -> None:
        if self.rich:
            self.console.print(f"[bold {color}]{mark}[/] {escape(text)}")
        else:
            self._emit(f"[{plain_mark}] {text}")

    def meter(self, right: int, total: int, width: int = 20) -> None:
        pct = right / total * 100 if total else 0
        filled = round(width * right / total) if total else 0
        if self.rich:
            color = GREEN if pct >= 70 else AMBER if pct >= 40 else RED
            bar = f"[{color}]{'█' * filled}[/][dim]{'░' * (width - filled)}[/]"
            self.console.print(f"\n[bold]Score[/] {bar} [bold {color}]{right}/{total}[/] ({pct:.0f}%)")
        else:
            self._emit(f"Score: {right}/{total} ({pct:.0f}%)")

    # -- structured ---------------------------------------------------------
    def panel(self, title: str, rows: Sequence[tuple[str, str]], color: str = PURPLE) -> None:
        if self.rich:
            w = max((len(k) for k, _ in rows), default=0)
            body = "\n".join(f"[{PURPLE}]{escape(k.ljust(w))}[/]  {escape(str(v))}" for k, v in rows)
            self.console.print(Panel(body, title=f"[bold {PINK}]{escape(title)}[/]", border_style=color, expand=False))
        else:
            self._emit(title)
            for k, v in rows:
                self._emit(f"  {k}: {v}")

    def table(
        self,
        title: str,
        columns: Sequence[str],
        rows: Sequence[Sequence[str]],
        status_colors: dict[str, str] | None = None,
    ) -> None:
        status_colors = status_colors or {}
        if self.rich:
            t = Table(title=f"[bold {PINK}]{escape(title)}[/]", box=box.ROUNDED, border_style=PURPLE, header_style=f"bold {TEAL}")
            for c in columns:
                t.add_column(c, overflow="fold")
            for row in rows:
                t.add_row(*[
                    f"[{status_colors[c]}]{escape(c)}[/]" if c in status_colors else escape(str(c)) for c in row
                ])
            self.console.print(t)
        else:
            self._emit(f"{title}")
            for row in rows:
                self._emit(f"- {row[0]}")
                for col, val in zip(columns[1:], row[1:]):
                    self._emit(f"    {col}: {val}")

    def ask(self, prompt: str) -> str:
        if self.rich:
            return self.console.input(f"[bold {PINK}]{escape(prompt)}[/]")
        return input(prompt)
