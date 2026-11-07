# Lab 7 — Fuzzing for Input Validation Bugs (Tennis Scoring)

Assigned repo: `L6_L7_34_tennis_scoring` (folder `lab7`)

**Name:** Muhammad Affan Dumba  
**SRN:** PES1UG24CS280

## About

A small Python module with three functions: `parse_score` (turns `"3-2"` into `(3, 2)`), `game_lead` (lead in a game such as `"40-30"`) and `set_spread` (max minus min of games won, from a CSV such as `"6,4,7"`). The original versions crashed on bad input. I used the Hypothesis fuzzing library to find the bugs, then hardened the code.

The handout calls the files `processor.py` / `test_processor.py`; in this assigned repo they are `tennis_scoring.py` / `test_tennis_scoring.py`.

## Files

| File | Description |
|------|-------------|
| `tennis_scoring.py` | Fixed, hardened module |
| `test_tennis_scoring.py` | Completed Hypothesis tests (28 tests) |
| `Lab7_Fuzz_Testing_Affan_Dumba_PES1UG24CS280.pdf` | Report with the screenshots of every step, the bug table and both source files |
| `screenshots/` | The 11 terminal screenshots used in the report, numbered as in the PDF |
| `original_code/tennis_scoring.py` | The original buggy module, untouched |
| `original_code/test_pure_fuzz.py` | Tiny Hypothesis test with no hand-written examples, used to show Hypothesis finding the bugs on its own |

## How to run

```bash
pip install hypothesis pytest pytest-cov
cd SELABS/Lab-7

python tennis_scoring.py                 # interactive program
python -m pytest test_tennis_scoring.py -v   # 28 tests, all pass
python -m pytest test_tennis_scoring.py -q --cov=tennis_scoring --cov-branch --cov-report=term-missing

# the same test file against the original code (fails):
cp test_tennis_scoring.py original_code/ && cd original_code && python -m pytest test_tennis_scoring.py
```

## Results

| Stage | Result |
|-------|--------|
| Original code, my 28 tests | **18 failed, 10 passed** |
| Fixed code, my 28 tests | **28 passed** |
| Coverage of the fixed module | **100 %** (73 statements, 24 of 24 branches) |

## Bugs found in the original code

| Function | Input | Failure |
|----------|-------|---------|
| all three | `None`, bytes | `AttributeError` / `TypeError` |
| `parse_score`, `game_lead` | `""`, `"abc"`, `"40"` | `ValueError` (unpack) |
| `parse_score`, `game_lead` | `"1-2-3"`, `"-3-2"`, `"40-30-15"` | `ValueError` (too many values) |
| `parse_score`, `set_spread` | `"3-"`, `"a-b"`, `"1.5-2"`, `"6,,4"`, `"6,4,"`, `""` | `ValueError` (`int()` on bad text) |
| `parse_score`, `set_spread` | 5000-digit number | `ValueError` (Python's 4300-digit `int()` limit, a denial-of-service risk) |
| `parse_score` | Arabic-Indic digits | Silently accepted |
| `game_lead` | `"50-30"`, `"AD-40"`, `" 40 - 30"`, `"-30"` | `KeyError` |
| `set_spread` | `"6,-4"` | Silently returns 10 (negative games accepted) |

## What the fix does

- Every function checks the input is a `str` of at most 100,000 characters.
- `parse_score` and `set_spread` validate with a strict regular expression: ASCII digits only, 1 to 18 digits per number.
- `game_lead` accepts `0`, `15`, `30`, `40` and `AD` (advantage, only against 40, case-insensitive).
- Spaces around values and commas are ignored.
- By default invalid input returns `None` and the functions never raise. With `strict=True` they raise a `ValueError` with a clear message instead.
- `main()` asks again after a bad entry and exits cleanly on Ctrl+C or end of input.

## Extra checks

- Test suite re-run with several Hypothesis seeds: always 28 passed.
- 30,000 random inputs per check compared against an independent regex reference version: no differences.
- Mutation check: the code was deliberately broken in 19 small ways and the tests failed every time.
- Both source files parse as Python 3.8 syntax; tests were run on Python 3.13.7.
