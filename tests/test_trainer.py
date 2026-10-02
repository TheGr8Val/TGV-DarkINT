import copy

import pytest

from tgv_darkint.cli import main, run_quiz
from tgv_darkint.trainer import find_module, load_data, score_answers, validate


@pytest.fixture(scope="module")
def data():
    return load_data()


def test_bundled_data_is_valid(data):
    assert validate(data) == []
    assert len(data["modules"]) == 4


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
    right, total = run_quiz(quiz, "t", ask=lambda _: next(replies), out=lambda _: None)
    assert (right, total) == (1, 1)


def test_cli_validate_and_modules(capsys):
    assert main(["validate"]) == 0
    assert main(["modules"]) == 0
    assert "M1" in capsys.readouterr().out


def test_cli_unknown_module():
    assert main(["show", "ZZ"]) == 2
