"""
Lab 6 - Branch coverage tests for tennis_scoring.py
Name : Muhammad Affan Dumba
SRN  : PES1UG24CS280

Goal of this file: every decision in tennis_scoring.py is forced to go both
True and False, including the boundary values (2-point lead, 6 games,
7-6 tie-break, best-of-N set counts).
Run with:
    coverage run --branch -m pytest BranchCoverageTest_tennis_scoring_application.py
    coverage report -m
"""
import pytest
from tennis_scoring import POINTS, game_score, set_winner, match_status


# =====================================================================
# game_score
# =====================================================================

# --- branch: if a < 0 or b < 0  (True via a, True via b, False) ---
@pytest.mark.parametrize("a, b", [(-1, 0), (0, -1), (-2, -3)])
def test_game_negative_points_raise(a, b):
    with pytest.raises(ValueError, match="negative points"):
        game_score(a, b)


# --- branch: if a >= 3 and b >= 3 -> False (normal scoring, lookup table) ---
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, "0-0"),
        (1, 0, "15-0"),
        (0, 1, "0-15"),
        (2, 2, "30-30"),
        (3, 0, "40-0"),
        (0, 3, "0-40"),
        (3, 2, "40-30"),   # a is 3 but b < 3 -> 'and' short-circuits to False
        (2, 3, "30-40"),   # b is 3 but a < 3
    ],
)
def test_game_normal_scores(a, b, expected):
    assert game_score(a, b) == expected


def test_points_table_is_correct():
    assert POINTS == ["0", "15", "30", "40"]


# --- branch: a >= 3 and b >= 3 -> True, then every inner decision ---
@pytest.mark.parametrize("n", [3, 4, 5, 10])
def test_game_deuce_any_equal_score(n):
    assert game_score(n, n) == "deuce"


@pytest.mark.parametrize("a, b", [(5, 3), (6, 4), (10, 8), (7, 3)])
def test_game_a_wins_with_two_point_lead(a, b):
    assert game_score(a, b) == "game A"


@pytest.mark.parametrize("a, b", [(3, 5), (4, 6), (8, 10), (3, 7)])
def test_game_b_wins_with_two_point_lead(a, b):
    assert game_score(a, b) == "game B"


@pytest.mark.parametrize("a, b", [(4, 3), (5, 4), (9, 8)])
def test_game_advantage_a(a, b):
    assert game_score(a, b) == "advantage A"


@pytest.mark.parametrize("a, b", [(3, 4), (4, 5), (8, 9)])
def test_game_advantage_b(a, b):
    assert game_score(a, b) == "advantage B"


# --- branch: a >= 4 (with b < 3, so the deuce block is skipped) ---
@pytest.mark.parametrize("a, b", [(4, 0), (4, 1), (4, 2)])
def test_game_a_wins_before_deuce_zone(a, b):
    assert game_score(a, b) == "game A"


# --- branch: b >= 4 ---
@pytest.mark.parametrize("a, b", [(0, 4), (1, 4), (2, 4)])
def test_game_b_wins_before_deuce_zone(a, b):
    assert game_score(a, b) == "game B"


# --- a >= 4 False and b >= 4 False -> falls to final return (covered above),
#     plus the 'a>=3 and b>=3' edge where only one side reached 3 ---
def test_game_one_side_only_at_forty():
    assert game_score(3, 1) == "40-15"
    assert game_score(1, 3) == "15-40"


# =====================================================================
# set_winner
# =====================================================================

# --- branch 1: a >= 6 and a - b >= 2 ---
@pytest.mark.parametrize("a, b", [(6, 0), (6, 4), (8, 6), (10, 8)])
def test_set_a_wins_by_two_games(a, b):
    assert set_winner(a, b) == "A"


# --- branch 2: b >= 6 and b - a >= 2 ---
@pytest.mark.parametrize("a, b", [(0, 6), (4, 6), (6, 8), (8, 10)])
def test_set_b_wins_by_two_games(a, b):
    assert set_winner(a, b) == "B"


# --- branch 3: a == 7 and b == 6 (tie-break) ---
def test_set_a_wins_tiebreak():
    assert set_winner(7, 6) == "A"


# --- branch 4: b == 7 and a == 6 ---
def test_set_b_wins_tiebreak():
    assert set_winner(6, 7) == "B"


# --- all four conditions False -> None ---
@pytest.mark.parametrize(
    "a, b",
    [
        (0, 0),
        (3, 2),   # example from the starter file
        (5, 4),
        (6, 5),   # a has 6 games but only a 1 game lead
        (5, 6),   # same for b
        (5, 5),
        (6, 6),   # level, tie-break still to be played
    ],
)
def test_set_not_decided(a, b):
    assert set_winner(a, b) is None


def test_set_seven_games_won_by_two():
    # 7-5 / 5-7 are decided by the normal two-game-lead rule, not the tie-break
    assert set_winner(7, 5) == "A"
    assert set_winner(5, 7) == "B"


def test_set_seven_six_requires_exact_scores():
    # a == 7 is True but b == 6 is False (and vice versa) -> still None
    assert set_winner(7, 7) is None
    assert set_winner(6, 6) is None


# =====================================================================
# match_status
# =====================================================================

# best of 3 -> needed = 2
@pytest.mark.parametrize("sa, sb", [(2, 0), (2, 1)])
def test_match_a_wins_best_of_3(sa, sb):
    assert match_status(sa, sb, 3) == "A wins"


@pytest.mark.parametrize("sa, sb", [(0, 2), (1, 2)])
def test_match_b_wins_best_of_3(sa, sb):
    assert match_status(sa, sb, 3) == "B wins"


def test_match_decider_best_of_3():
    assert match_status(1, 1, 3) == "decider"


@pytest.mark.parametrize("sa, sb", [(0, 0), (1, 0), (0, 1)])
def test_match_in_progress_best_of_3(sa, sb):
    assert match_status(sa, sb, 3) == "in progress"


# best of 5 -> needed = 3
@pytest.mark.parametrize("sa, sb", [(3, 0), (3, 1), (3, 2)])
def test_match_a_wins_best_of_5(sa, sb):
    assert match_status(sa, sb, 5) == "A wins"


@pytest.mark.parametrize("sa, sb", [(0, 3), (1, 3), (2, 3)])
def test_match_b_wins_best_of_5(sa, sb):
    assert match_status(sa, sb, 5) == "B wins"


def test_match_decider_best_of_5():
    assert match_status(2, 2, 5) == "decider"


@pytest.mark.parametrize("sa, sb", [(0, 0), (2, 0), (0, 2), (2, 1), (1, 2), (1, 1)])
def test_match_in_progress_best_of_5(sa, sb):
    assert match_status(sa, sb, 5) == "in progress"


# 'sets_a == needed - 1 and sets_b == needed - 1': True/False on each operand
def test_match_only_one_side_at_needed_minus_one():
    assert match_status(2, 1, 5) == "in progress"   # first True, second False
    assert match_status(1, 2, 5) == "in progress"   # first False, second True


def test_match_best_of_1_behaviour():
    # needed = 1, so a 0-0 start already satisfies needed-1 for both sides.
    # This documents what the code currently does for a one-set match.
    assert match_status(1, 0, 1) == "A wins"
    assert match_status(0, 1, 1) == "B wins"
    assert match_status(0, 0, 1) == "decider"
