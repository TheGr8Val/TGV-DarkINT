import copy

import pytest

from tgv_darkint.cli import main, run_quiz, show_module
from tgv_darkint.trainer import find_module, load_data, score_answers, validate
from tgv_darkint.ui import EMOJI_RE, Ui


@pytest.fixture(scope="module")
def data():
    return load_data()


def plain():
    lines: list[str] = []
    return Ui(rich=False, out=lines.append), lines


def test_bundled_data_is_valid(data):
    assert validate(data) == []
    assert [m["module_id"] for m in data["modules"]] == ["M1", "M2", "M3", "M4", "M5"]


def test_find_module_is_case_insensitive(data):
    assert find_module(data, " m3 ")["module_id"] == "M3"
    assert find_module(data, "nope") is None


def test_validate_catches_bad_correct_index(data):
    bad = copy.deepcopy(data)
    bad["assessment"]["final_quiz"][0]["correct"] = 99
    assert any("valid option index" in p for p in validate(bad))


def test_score_answers(data):
    quiz = data["assessment"]["final_quiz"]
    assert score_answers(quiz, [q["correct"] for q in quiz]) == (len(quiz), len(quiz))
    assert score_answers(quiz, [-1] * len(quiz)) == (0, len(quiz))


def test_run_quiz_retries_invalid_input(data):
    quiz = data["assessment"]["final_quiz"][:1]
    replies = iter(["x", "0", str(quiz[0]["correct"] + 1)])
    ui, lines = plain()
    ui.ask = lambda _: next(replies)
    assert run_quiz(quiz, "t", ui) == (1, 1)
    assert any("Score: 1/1" in line for line in lines)


def test_every_module_renders_in_plain_mode_without_emoji(data):
    ui, lines = plain()
    for m in data["modules"]:
        show_module(m, ui)
    text = "\n".join(lines)
    assert not EMOJI_RE.search(text)
    assert "Ahmia" in text and "Whonix" in text and "Tails" in text


def test_rich_mode_renders_every_module(data, capsys):
    ui = Ui(rich=True)
    for m in data["modules"]:
        show_module(m, ui)
    out = capsys.readouterr().out
    assert "Your First Time on Tor" in out and "Ahmia" in out


def test_first_time_module_covers_the_essentials(data):
    c = find_module(data, "M5")["content"]
    names = " ".join(o["name"] for o in c["setup_options"]).lower()
    assert all(k in names for k in ("tails", "whonix", "vpn", "tor browser"))
    steps = " ".join(s["detail"] for s in c["first_session"]).lower()
    assert "duckduckgo" in steps and "ahmia" in steps and "hidden wiki" in steps


def test_cli_validate_and_modules(capsys):
    assert main(["--plain", "validate"]) == 0
    assert main(["--plain", "modules"]) == 0
    assert "M5" in capsys.readouterr().out


def test_cli_unknown_module():
    assert main(["--plain", "show", "ZZ"]) == 2
