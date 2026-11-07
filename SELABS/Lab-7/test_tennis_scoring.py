"""Lab 7 - Fuzz tests for tennis_scoring.py using Hypothesis.

Name : Muhammad Affan Dumba
SRN  : PES1UG24CS280

Run with:  pytest test_tennis_scoring.py   (or  python -m pytest test_tennis_scoring.py)

Contract that the hardened module must honour
---------------------------------------------
* parse_score / game_lead / set_spread must NEVER raise on any input
  (default, non-strict mode).
* Valid input   -> the documented result.
* Invalid input -> None (a safe, explicit "rejected" value).
* strict=True   -> invalid input raises ValueError instead of returning None.
* main() keeps asking until it gets valid input and exits cleanly on EOF/Ctrl+C.
"""
import pytest
from hypothesis import given, example, strategies as st

import tennis_scoring
from tennis_scoring import parse_score, game_lead, set_spread

# Any kind of junk a caller might hand us (not only strings).
ANYTHING = st.one_of(
    st.none(), st.text(), st.integers(), st.floats(allow_nan=True),
    st.booleans(), st.binary(),
    st.lists(st.integers(), max_size=5),
    st.dictionaries(st.text(max_size=3), st.integers(), max_size=3),
)

POINT_LABELS = ["0", "15", "30", "40"]


# ---------------------------------------------------------------------------
# 1. Required "no crash" fuzz tests (one per function) - text | None
#    @example(...) pins counter-examples found against the original buggy code,
#    so they are always replayed as regression tests.
# ---------------------------------------------------------------------------
@given(st.text() | st.none())
@example(None)
@example("")
@example("abc")
@example("3-")
@example("-")
@example("1-2-3")
@example("a-b")
@example("-3-2")
@example("\u0663-\u0662")        # Arabic-Indic digits
@example("\u00b2-1")             # superscript two: str.isdigit() True, int() fails
@example("9" * 5000 + "-1")      # int() digit-limit DoS (Python >= 3.11)
def test_parse_score_no_crash(s):
    try:
        parse_score(s)
    except Exception as e:
        assert False, f"parse_score crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example("40")
@example("40-")
@example("-30")
@example("40-30-15")
@example("50-30")
@example("AD-40")
@example(" 40 - 30 ")
@example("\x00-\x00")
def test_game_lead_no_crash(s):
    try:
        game_lead(s)
    except Exception as e:
        assert False, f"game_lead crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example(",")
@example("6,,4")
@example("6,4,")
@example("six,four")
@example("6,-4")
@example("1.5,2")
@example("\u00b2,1")
@example("9" * 5000 + ",1")
def test_set_spread_no_crash(s):
    try:
        set_spread(s)
    except Exception as e:
        assert False, f"set_spread crashed with: {e!r} on input {s!r}"


# ---------------------------------------------------------------------------
# 2. Wider fuzzing: arbitrary (non-string) types must not crash either.
# ---------------------------------------------------------------------------
@given(ANYTHING)
def test_parse_score_any_type_no_crash(x):
    parse_score(x)


@given(ANYTHING)
def test_game_lead_any_type_no_crash(x):
    game_lead(x)


@given(ANYTHING)
def test_set_spread_any_type_no_crash(x):
    set_spread(x)


# ---------------------------------------------------------------------------
# 3. Property tests: valid input must give correct answers.
# ---------------------------------------------------------------------------
@given(st.integers(0, 10 ** 18 - 1), st.integers(0, 10 ** 18 - 1))
def test_parse_score_roundtrip(a, b):
    assert parse_score(f"{a}-{b}") == (a, b)


@given(st.integers(0, 99), st.integers(0, 99),
       st.text(" \t", max_size=3), st.text(" \t", max_size=3))
def test_parse_score_ignores_surrounding_whitespace(a, b, pad1, pad2):
    assert parse_score(f"{pad1}{a}-{b}{pad2}") == (a, b)


@given(st.sampled_from(POINT_LABELS), st.sampled_from(POINT_LABELS))
def test_game_lead_valid_scores(x, y):
    expected = POINT_LABELS.index(x) - POINT_LABELS.index(y)
    assert game_lead(f"{x}-{y}") == expected
    assert -3 <= game_lead(f"{x}-{y}") <= 3


@given(st.sampled_from(POINT_LABELS), st.sampled_from(POINT_LABELS))
def test_game_lead_is_antisymmetric(x, y):
    assert game_lead(f"{x}-{y}") == -game_lead(f"{y}-{x}")


@given(st.lists(st.integers(0, 10 ** 18 - 1), min_size=1, max_size=20))
def test_set_spread_valid_lists(games):
    csv = ",".join(map(str, games))
    result = set_spread(csv)
    assert result == max(games) - min(games)
    assert result >= 0


@given(st.lists(st.integers(0, 99), min_size=1, max_size=10),
       st.text(" \t", max_size=2))
def test_set_spread_ignores_spaces_around_commas(games, pad):
    csv = (pad + "," + pad).join(map(str, games))
    assert set_spread(csv) == max(games) - min(games)


@given(st.integers(0, 99))
def test_set_spread_single_value_is_zero(g):
    assert set_spread(str(g)) == 0


# ---------------------------------------------------------------------------
# 4. Advantage (AD) scoring
# ---------------------------------------------------------------------------
def test_advantage_scores():
    assert game_lead("AD-40") == 1
    assert game_lead("40-AD") == -1
    assert game_lead("ad-40") == 1
    assert game_lead(" Ad - 40 ") == 1


@given(st.sampled_from(["AD", "ad", "Ad", "aD"]))
def test_advantage_is_case_insensitive_and_antisymmetric(ad):
    assert game_lead(f"{ad}-40") == 1
    assert game_lead(f"40-{ad}") == -1


def test_advantage_only_valid_against_forty():
    for bad in ("AD-AD", "AD-30", "AD-15", "AD-0", "0-AD", "15-AD", "30-AD"):
        assert game_lead(bad) is None, bad


# ---------------------------------------------------------------------------
# 5. Invalid input must be rejected (None) rather than guessed at.
# ---------------------------------------------------------------------------
@given(st.text(alphabet="abcxyz,-+ .", max_size=12))
def test_alpha_garbage_is_rejected(s):
    assert parse_score(s) is None
    assert game_lead(s) is None
    assert set_spread(s) is None


BAD_SCORES = (None, "", "abc", "3-", "-3", "1-2-3", "-3-2", "3--2", "1.5-2",
              "\u00b2-1", "\u0663-\u0662", "9" * 5000 + "-1", "9" * 19 + "-1",
              "1-" + "9" * 19, b"3-2", 5, ["3-2"], "3 2", "+3-2")
BAD_LEADS = (None, "", "40", "40-", "-30", "40-30-15", "50-30", "15--0", "4-0",
             "00-30", "\u0663-30", "A-40", "AD-AD", "AD-30", b"40-30", 40, "40 30")
BAD_SPREADS = (None, "", ",", "6,,4", "6,4,", ",6", "six,four", "6,-4", "1.5,2",
               "\u00b2,1", "9" * 5000 + ",1", "9" * 19 + ",1", b"6,4", 6, [6, 4],
               "6 4", "6;4", "+6,4")


def test_explicit_invalid_inputs_return_none():
    for bad in BAD_SCORES:
        assert parse_score(bad) is None, bad
    for bad in BAD_LEADS:
        assert game_lead(bad) is None, bad
    for bad in BAD_SPREADS:
        assert set_spread(bad) is None, bad


def test_documented_examples():
    assert parse_score("3-2") == (3, 2)
    assert game_lead("40-30") == 1
    assert game_lead("0-40") == -3
    assert set_spread("6,4,7") == 3


def test_limits_are_enforced_and_fast():
    assert parse_score("9" * 18 + "-0") == (10 ** 18 - 1, 0)       # largest accepted
    assert parse_score("9" * 19 + "-0") is None                    # one digit too many
    assert set_spread(",".join(["1"] * 40_000)) == 0                # long but valid, linear time
    assert set_spread("1," * 60_000) is None                       # too long (> 100,000 chars)
    assert parse_score(" " * 200_000 + "1-2") is None
    assert parse_score("1-2" + " " * 1000) == (1, 2)


# ---------------------------------------------------------------------------
# 6. strict=True: invalid input raises ValueError (with a message).
# ---------------------------------------------------------------------------
def test_strict_mode_raises_valueerror():
    for fn, bad in ((parse_score, "abc"), (parse_score, None), (game_lead, "50-30"),
                    (game_lead, "AD-30"), (game_lead, "40"), (game_lead, 7),
                    (set_spread, "6,,4"), (set_spread, ""), (set_spread, b"1")):
        with pytest.raises(ValueError) as info:
            fn(bad, strict=True)
        assert str(info.value)


def test_strict_mode_returns_normal_results_for_valid_input():
    assert parse_score("3-2", strict=True) == (3, 2)
    assert game_lead("40-AD", strict=True) == -1
    assert set_spread("6, 4 ,7", strict=True) == 3


@given(ANYTHING)
def test_strict_and_default_modes_agree(x):
    for fn in (parse_score, game_lead, set_spread):
        expected = fn(x)
        if expected is None:
            with pytest.raises(ValueError):
                fn(x, strict=True)
        else:
            assert fn(x, strict=True) == expected


# ---------------------------------------------------------------------------
# 7. Command line interface (main) - re-prompts, handles EOF and Ctrl+C.
# ---------------------------------------------------------------------------
def _feed(monkeypatch, answers):
    it = iter(answers)

    def fake_input(prompt=""):
        try:
            item = next(it)
        except StopIteration:
            raise EOFError
        if isinstance(item, BaseException):
            raise item
        return item
    monkeypatch.setattr("builtins.input", fake_input)


def test_main_happy_path(monkeypatch, capsys):
    _feed(monkeypatch, ["3-2", "40-30", "6,4,7"])
    tennis_scoring.main()
    out = capsys.readouterr().out
    assert "(3, 2)" in out and "Lead in Points: 1" in out and "Spread: 3" in out
    assert "Invalid" not in out


def test_main_reprompts_until_valid(monkeypatch, capsys):
    _feed(monkeypatch, ["abc", "", "3-2", "40", "50-30", "AD-40", "6,,4", "6,4,7"])
    tennis_scoring.main()
    out = capsys.readouterr().out
    assert out.count("Invalid input") == 5
    assert "(3, 2)" in out and "Lead in Points: 1" in out and "Spread: 3" in out
    assert "Traceback" not in out


def test_main_survives_eof(monkeypatch, capsys):
    _feed(monkeypatch, ["bad"])           # then input() raises EOFError
    tennis_scoring.main()                  # must not raise
    assert "Invalid input" in capsys.readouterr().out


def test_main_survives_ctrl_c(monkeypatch, capsys):
    _feed(monkeypatch, ["3-2", KeyboardInterrupt()])
    try:
        tennis_scoring.main()
    except KeyboardInterrupt:              # main() must handle Ctrl+C itself
        pytest.fail("main() let KeyboardInterrupt escape")
    assert "Cancelled" in capsys.readouterr().out


def test_script_entry_point(monkeypatch, capsys):
    """`python tennis_scoring.py` runs main() when executed as a script."""
    import runpy
    _feed(monkeypatch, ["3-2", "40-30", "6,4,7"])
    runpy.run_path(tennis_scoring.__file__, run_name="__main__")
    assert "Spread: 3" in capsys.readouterr().out
