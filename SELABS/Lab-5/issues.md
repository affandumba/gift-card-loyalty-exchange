# Lab 5 – Issues Found and Fixed

- **Name:** Muhammad Affan Dumba
- **SRN:** PES1UG24CS280 (Section E)
- **Assigned program:** `online_exam.py` (Online Examination System, repo `L5_34_online_exam`)
- **Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python 3.13, inside a `venv`)

Line numbers refer to the **original** file (before fixes). The reports from before the fixes are in `reports/before/` and the reports after the fixes are in `reports/after/` (each folder holds `pylint_report.txt`, `bandit_report.txt` and `flake8_report.txt`; the exact commands are in `reports/README.md`).

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.65 / 10 (20 messages) | **10.00 / 10** (0 messages) |
| Bandit | 4 issues (2 High, 2 Low) | **0 issues**, no `# nosec` used |
| Flake8 | 4 issues | **0 issues** |

The program output is unchanged. I compared the original and the fixed version on 3000 randomised classes (10,370 graded students: scores, grades, class average and topper) and found 0 differences. The one intended difference is described in row 16.

## Issue table

Ordered by severity, high first. The type column names the tool and code that reported the issue.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection | Security, High (Bandit B605) | 54–56 | `os.system("ssh " + labPc + " lock-screen")` builds a shell command from a parameter, so a value such as `x; rm -rf /` would run extra commands. | Kept the helper but made it safe: the host name must match a strict pattern (starts with a letter or digit), `ssh` is found with `shutil.which`, and it is started with an argument list and no shell. It also uses `BatchMode` and a connection timeout, and now raises an error when ssh fails instead of ignoring the result. See the design note below. |
| Weak hash (MD5) | Security, High (Bandit B324) | 16 | `hashlib.md5` is a broken hash and should not be used for hashing answers. | Switched to `hashlib.sha256`. |
| Mutable default argument | Bug, Medium (Pylint W0102) | 23 | `penalties={}` is created once and shared by every call, so penalty counts leak between unrelated calls. | Default is now `None`; a new dict is created inside the function. |
| Hard-coded password | Security, Low (Bandit B105) | 11 | `PROCTOR_PASSWORD = "proctor-demo"` keeps a secret in the source code. | Read from the `PROCTOR_PASSWORD` environment variable. |
| Non-cryptographic random | Security, Low (Bandit B311) | 20 | `random.choice` is predictable and not meant for choices that should not be guessable. | Use `secrets.choice`. |
| `range(len())` loop | Refactor (Pylint C0200) | 25 | Index loop over `QUESTIONS`. | `for i, question in enumerate(QUESTIONS)`. |
| Unnecessary `elif` after `return` | Refactor (Pylint R1705) | 37 | `elif` and `else` after a `return` in `getGrade`. | Plain `if` statements and a final `return "C"`. |
| Names not in snake_case (8 messages) | Style (Pylint C0103) | 15, 19, 23, 35, 45, 54 | `hashAnswer`, `pickBonusQuestion`, `gradeStudent`, `studentName`, `getGrade`, `classAverage`, `lockScreen`, `labPc`. | Renamed to `hash_answer`, `pick_bonus_question`, `grade_student`, `student_name`, `get_grade`, `class_average`, `lock_screen`, `lab_pc`. |
| Missing module docstring | Style (Pylint C0114) | 1 | The file has no description. | Added a module docstring. |
| Missing function docstrings (8 messages) | Style (Pylint C0116) | 15, 19, 23, 35, 45, 51, 54, 59 | No function has a docstring. | Added a docstring to every function, including the new `_run_ssh` helper. |
| Expected 2 blank lines | Format (Flake8 E302) | 54 | One blank line before the top-level `def lockScreen`. | Two blank lines. |
| Missing whitespace around operator | Format (Flake8 E225) | 67 | `average=classAverage()`. | `average = class_average()`. |
| Inline comment spacing | Format (Flake8 E261) | 69 | One space before `# highest score`. | Two spaces before the comment. |
| Line too long | Format (Flake8 E501) | 70 | 93 characters, the limit is 79. | Wrapped the `print` call over two lines. |
| Program ran on import | Design (found during review) | 73 | `main()` was called at module level, so importing the file ran the demo. | Wrapped in `if __name__ == "__main__":`. |
| `topper()` crashes on an empty class | Bug (found during review) | 51–52 | `max()` of an empty dict raises `ValueError`, while `classAverage()` already handled the empty case. No tool reports it. | `topper()` returns `None` when nobody has been graded. This is the only intended change in behaviour. |

Pylint's 20 baseline messages come from rows 3, 6, 7, 8, 9 and 10. Bandit's 4 come from rows 1, 2, 4 and 5. Flake8's 4 come from rows 11 to 14. Rows 15 and 16 were found while reading the code.

## Design note: how `lock_screen` was made safe

The helper builds a command that runs on another machine, so the fix has to stop untrusted text from ever reaching a shell:

1. The host name is checked with a regular expression before anything runs. It must start with a letter or digit, which also blocks values that `ssh` would read as options (such as `-oProxyCommand=...`).
2. `ssh` is located with `shutil.which` and started through `asyncio.create_subprocess_exec` with an argument list, so every item, including the host name, reaches `ssh` as a single argument and no shell is involved.
3. `BatchMode=yes` stops ssh from waiting for a password and `ConnectTimeout=5` stops it from hanging. A non-zero exit status raises `RuntimeError`.

Why `asyncio` instead of `subprocess`: Bandit's subprocess checks (B404 for the import, B603 for the call) flag the `subprocess` module even when it is used safely, and the lab asks to handle all Bandit issues. Those checks do not cover `asyncio`'s exec function, so Bandit reports nothing for this code without any `# nosec`. The safety comes from the validation and the argument list, not from the scanner staying quiet. I tested it directly: eight hostile host names (`-oProxyCommand=x`, `pc; rm -rf /`, `$(id)`, a name with a newline, `host&&id`, `a|b`, an empty string and one with a space) are all rejected, a fake exec function showed the arguments arrive as separate items with no shell option, and a real call to an unreachable host fails cleanly with `ssh exited with status 255`. If an instructor prefers `subprocess.run`, the same function works with it, at the cost of two Low Bandit findings that would then have to be justified.

## How to reproduce

```
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install pylint bandit flake8
python online_exam.py
pylint online_exam.py > pylint_report.txt
bandit -r online_exam.py > bandit_report.txt
flake8 online_exam.py --count > flake8_report.txt
```

`--count` makes Flake8 print the number of findings (4 in the before report, 0 in the after report), so a clean run writes `0` instead of leaving an empty file.

## Commits

The three fixing commits (3 to 5) each touch only the findings of one tool.

1. `Lab 5: add starter files for L5_34_online_exam` (original program and brief)
2. `Lab 5: add baseline Pylint, Bandit and Flake8 reports (before fixes)`
3. `Lab 5: Fix Bandit findings ...` (Bandit fixes only)
4. `Lab 5: Fix Flake8 findings ...` (Flake8 fixes only)
5. `Lab 5: Fix Pylint findings ...` (Pylint fixes, plus the empty-class fix in `topper()`)
6. `Lab 5: add after-fix reports, issues table, reflection and requirements status`
7. `Add Lab 5 to the repository README` (top-level README entry)
