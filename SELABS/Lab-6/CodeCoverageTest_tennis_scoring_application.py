"""
Lab 6 - Code (line) coverage tests for tennis_scoring.py
Name : Muhammad Affan Dumba
SRN  : PES1UG24CS280

Goal of this file: make sure every function is called and the main
statements in each function are executed at least once (line coverage).
Run with:
    coverage run -m pytest CodeCoverageTest_tennis_scoring_application.py
    coverage report -m
"""
import pytest
from tennis_scoring import game_score, set_winner, match_status


# ---------------- game_score ----------------
def test_game_start():
    assert game_score(0, 0) == "0-0"


def test_game_mid_score():
    # normal score, goes through the POINTS lookup at the bottom
    assert game_score(2, 1) == "30-15"


def test_game_negative_points_raises():
    with pytest.raises(ValueError):
        game_score(-1, 0)


def test_game_deuce():
    assert game_score(3, 3) == "deuce"


def test_game_won_by_a_from_deuce_zone():
    assert game_score(5, 3) == "game A"


def test_game_won_by_b_from_deuce_zone():
    assert game_score(3, 5) == "game B"


def test_game_advantage_a():
    assert game_score(4, 3) == "advantage A"


def test_game_advantage_b():
    assert game_score(3, 4) == "advantage B"


def test_game_won_by_a_straight():
    assert game_score(4, 1) == "game A"


def test_game_won_by_b_straight():
    assert game_score(0, 4) == "game B"


# ---------------- set_winner ----------------
def test_set_undecided():
    assert set_winner(3, 2) is None


def test_set_won_by_a():
    assert set_winner(6, 2) == "A"


def test_set_won_by_b():
    assert set_winner(1, 6) == "B"


# ---------------- match_status ----------------
def test_match_a_wins():
    assert match_status(2, 0, 3) == "A wins"


def test_match_b_wins():
    assert match_status(1, 2, 3) == "B wins"


def test_match_decider():
    assert match_status(1, 1, 3) == "decider"


def test_match_in_progress():
    assert match_status(1, 0, 3) == "in progress"
