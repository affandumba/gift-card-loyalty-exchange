# Lab 6 — Code and Branch Coverage (Tennis Scoring)

Assigned repo: `L6_L7_34_tennis_scoring`

**Name:** Muhammad Affan Dumba  
**SRN:** PES1UG24CS280

## About

A small Python module that tracks tennis scoring at game, set and match level.

## Files

| File | Description |
|------|-------------|
| `tennis_scoring.py` | The module under test (`game_score`, `set_winner`, `match_status`) |
| `test_tennis_scoring.py` | Starter test file (2 tests, left as given) |
| `CodeCoverageTest_tennis_scoring_application.py` | Tests written for code (line) coverage |
| `BranchCoverageTest_tennis_scoring_application.py` | Tests written for branch coverage |
| `screenshots/1_code_coverage_report.png` | Terminal output after reaching > 90 % line coverage |
| `screenshots/2_branch_coverage_report.png` | Terminal output after reaching > 90 % branch coverage |

## How to run

```bash
pip install coverage pytest
cd SELABS/Lab-6

# code (line) coverage
coverage run -m pytest CodeCoverageTest_tennis_scoring_application.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_tennis_scoring_application.py
coverage report -m
```

## Results

| Stage | Tests | `tennis_scoring.py` coverage | Missing |
|-------|-------|------------------------------|---------|
| Starter tests (`coverage run --branch`) | 2 | 32 % (14 of 38 statements run) | lines 6, 8-16, 18, 20, 26, 28, 30, 32, 37-44 |
| Code coverage tests (line) | 17 | **95 %** (36 of 38 statements) | lines 30, 32 |
| Same tests measured with `--branch` | 17 | 94 % | lines 30, 32 (2 partial branches) |
| Branch coverage tests (`--branch`) | 79 | **100 %** (38 statements, 30 of 30 branches) | none |

## Approach

**Code coverage.** First I read the three functions and listed every `return`/`raise`
statement, then wrote one test for each of them: the negative-points error, each of the
normal scores, deuce, advantage A/B, game A/B (both from the deuce zone and straight wins),
set winner A/B/undecided and the four `match_status` results. This reached 95 %. I
left out the two tie-break returns (`7-6` and `6-7`) in this round on purpose, which is why
lines 30 and 32 show up as missing and why the `--branch` figure is slightly lower (94 %)
than the line figure.

**Branch coverage.** Line coverage only asks whether a line ran. Branch coverage asks
whether every `if` went both ways. For the second file I went through every decision and made sure
it was both True and False, and I added boundary values around each condition:

- `game_score`: `a < 0 or b < 0` is True through `a` and through `b`; the `a >= 3 and b >= 3`
  check is tried with only one side at 3 (e.g. 3-2, 2-3) so the `and` is False for each
  operand; the 2-point lead checks use exactly-2 and larger leads; deuce is tested at 3-3, 4-4, 5-5 and 10-10.
- `set_winner`: 6-4 and 8-6 (two-game lead), 6-5 / 5-6 (only a one-game lead), 6-6, 7-5,
  and the two tie-break results 7-6 and 6-7, plus 7-7 where `a == 7` is True but `b == 6` is False.
- `match_status`: best-of-3 (needed = 2) and best-of-5 (needed = 3) for every outcome, plus
  cases where only one side is at `needed - 1` so the `and` is False for each operand.

Result: all 30 branches in `tennis_scoring.py` are taken, 100 % line and branch coverage.

## Things I noticed while testing

- `match_status(0, 0, 1)` returns `"decider"` because for `best_of = 1` we get
  `needed - 1 == 0` for both players. That looks odd for a one-set match, so there is a test
  (`test_match_best_of_1_behaviour`) that records the current behaviour.
- `set_winner` does not reject impossible set scores such as 7-7 or 9-3; it just returns the
  result by the two-game-lead rule or `None`.
- 100 % branch coverage does not mean the code is bug free; it only shows every decision was
  exercised by at least one test.

## Commits

1. Code coverage test cases + screenshot (95 % line coverage)
2. Branch coverage test cases + screenshot + README (100 % branch coverage)
