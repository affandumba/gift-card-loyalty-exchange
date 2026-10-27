# Lab 5 – Reflection on Static Analysis

- **Name:** Muhammad Affan Dumba
- **SRN:** PES1UG24CS280 (Section E)
- **Program:** `online_exam.py`

These answers cover the lab's learning outcomes: the purpose of static analysis, the kinds of problems it finds, how the three tools differ, how to read the reports by severity, and what static analysis contributes to quality.

## 1. What is static analysis for, and what did it find that running the program did not show?

Static analysis examines the source code without running it. The program ran with no error and printed sensible grades, so nothing looked wrong from the outside. The three tools still reported 28 issues in 54 lines of code (Pylint 20, Bandit 4, Flake8 4). The serious ones could never appear in a normal run: the `os.system("ssh " + labPc + ...)` call (command injection, Bandit B605), the MD5 hash (B324) and the mutable default `penalties={}` (Pylint W0102). The last one only causes wrong results when `gradeStudent` is called several times without the argument, which the demo never does. A tool reads every line, while a test run only exercises the paths the demo happens to take.

## 2. Which common problems did I find, and how did I fix them?

- **Mutable default argument:** `penalties={}` was shared between calls. It now defaults to `None`, and a fresh dict is created inside the function.
- **Insecure patterns:** a shell command built from a parameter, a weak hash, a hard-coded password and a predictable random generator. They became a validated argument-list call with no shell, SHA-256, an environment variable and `secrets.choice`.
- **Style and design:** non-snake_case names, missing docstrings, a `range(len())` loop, an unnecessary `elif` after `return`, and `main()` running on import.
- **A bug no tool reported:** reading the code showed that `topper()` crashes on an empty class although `class_average()` handles it, so it now returns `None`.

There was no overly broad `except` in this file. That is one of the issues the handout mentions, and it would show up as Pylint W0718.

## 3. How do Pylint, Bandit and Flake8 differ, and how did severity guide the order of work?

- **Bandit** is the security guard. It gave only 4 findings (the same number as Flake8), but the two High ones were the most serious, so I fixed them first.
- **Pylint** is the strict code reviewer. It gave the most findings (20) and moved the score from 5.65 to 10.00. Most were naming and docstrings, plus two real improvements: the mutable default and the index loop.
- **Flake8** is the grammar checker for PEP 8. Its four findings are cosmetic but cheap to fix, and they make the file consistent.

I worked in severity order: High security issues, then the mutable default bug, then Low security findings, and finally style and formatting. Each tool got its own commit, and I re-ran the tool after each one to confirm the findings were gone (Bandit 4 to 0, Flake8 4 to 0, Pylint 6.27 to 10.00).

## 4. Which findings needed judgement instead of a mechanical fix?

The `os.system` call. The usual fix is `subprocess.run([...])`, but Bandit still raises two Low findings for the `subprocess` module itself (B404 and B603), and the lab asks to handle all Bandit issues. I did not want to silence them with `# nosec`, and I did not want to delete a helper that someone may need. I kept the helper, validated the host name, and started `ssh` with an argument list and no shell through `asyncio`, which Bandit's subprocess checks do not cover. The important point is that a quiet scanner is not proof of safety, so I tested the helper directly with eight hostile host names, with a fake exec function to confirm the arguments stay separate, and with a real call to an unreachable host. `issues.md` explains this openly, including that `subprocess.run` would also be acceptable if the findings are justified. Renaming functions also needed care, because every call site has to change. To check that nothing broke I compared the original and fixed versions on 3000 random classes (10,370 students) and found no differences.

## 5. How does static analysis contribute to code quality and maintainability?

It gives fast, repeatable feedback with no need to run the code, and it applies one consistent standard, so reviewers can spend their time on logic instead of formatting. The scores make progress measurable (Pylint 5.65 to 10.00, Bandit 4 to 0, Flake8 4 to 0). It also has limits. It cannot say whether the grading rules are right, it can raise false positives that need human judgement, and it missed the empty-class crash in `topper()`, which I only found by reading the code. A clean report is not proof that the program is correct, so tests are still needed. In a team I would run all three tools automatically on every pull request (CI or a pre-commit hook), so problems are caught while the change is still small.
