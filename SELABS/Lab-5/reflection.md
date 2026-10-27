# Lab 5 – Reflection on Static Analysis

- **Name:** Muhammad Affan Dumba
- **SRN:** PES1UG24CS280 (Section E)
- **Program:** `online_exam.py`

The four reflection questions below cover the lab's learning outcomes: the purpose and scope of static analysis, the common problems it finds, how Pylint, Bandit and Flake8 are used and how their reports are read by severity, and what static analysis adds to code quality and maintainability.

## 1. What is static analysis for, and what kinds of issues did the three tools find that running the program did not show?

Static analysis examines source code without running it, so it can check every line instead of only the paths one run happens to take. The program ran with no error and printed sensible grades, so nothing looked wrong from the outside. The three tools still reported 28 issues in 54 lines of code (Pylint 20, Bandit 4, Flake8 4):

- **Common programming problems (Pylint):** a mutable default argument (`penalties={}`, W0102) shared between calls, a `range(len())` loop, an unnecessary `elif` after `return`, non-snake_case names and missing docstrings.
- **Insecure patterns (Bandit):** a shell command built from a parameter (`os.system("ssh " + labPc ...)`, B605, command injection), an MD5 hash (B324), a hard-coded password (B105) and a predictable random generator (B311).
- **Style problems (Flake8):** missing blank lines, missing spaces around an operator, comment spacing and a 93-character line.

There was no overly broad `except` in this file. The handout lists it as a common issue, and it would show up as Pylint W0718. The most serious findings could never appear in a normal run: the demo never calls `lockScreen`, and the mutable default only causes wrong results when `gradeStudent` is called several times without the argument.

## 2. How did severity guide the order of work, and how were the main issues fixed?

I read the three reports together, documented every finding in `issues.md`, and fixed them in severity order, one tool per commit, re-running the tool after each commit:

- **Bandit first (4 to 0):** the two High findings were the most serious. MD5 became SHA-256, the shell call became a validated argument-list call with no shell, the password now comes from an environment variable, and `random.choice` became `secrets.choice`.
- **Flake8 next (4 to 0):** four small formatting fixes, with no change in behaviour.
- **Pylint last (6.27 to 10.00):** docstrings, snake_case names, the mutable default (now `None` with a fresh dict per call), `enumerate`, a flattened `if` chain, and a `__main__` guard so importing the file no longer runs the demo.

The finished program prints exactly the same output as the original. I compared the original and the fixed version on 3000 random classes (10,370 students) and found no differences in scores, grades, average or topper.

## 3. What needed judgement or was difficult, and what did the tools miss?

The `os.system` call. The usual fix is `subprocess.run([...])`, but Bandit then raises two Low findings for the `subprocess` module itself (B404 and B603), and the lab asks to handle all Bandit issues. I did not want to hide them with `# nosec`, and I did not want to delete a helper that someone may need. I kept the helper, validated the host name, and started `ssh` with an argument list and no shell through `asyncio`, which Bandit's subprocess checks do not cover. A quiet scanner is not proof of safety, so I tested the helper directly with eight hostile host names, with a fake exec function to confirm the arguments stay separate, and with a real call to an unreachable host. `issues.md` explains this openly, including that `subprocess.run` would also be acceptable if its findings are justified.

The tools also missed something: `topper()` crashes on an empty class although `class_average()` handles it, and no tool reported it. I only found it by reading the code, so it now returns `None`. Renaming the functions needed care too, because every call site has to change; the comparison on random classes was how I checked that nothing broke.

## 4. How does static analysis contribute to code quality and maintainability, and how would I use it in future?

It gives fast, repeatable feedback with no need to run the code, and it applies one consistent standard, so reviewers can spend their time on logic instead of formatting. The scores make progress measurable (Pylint 5.65 to 10.00, Bandit 4 to 0, Flake8 4 to 0). It also has limits. It cannot say whether the grading rules are right, it can raise false positives that need human judgement, and a clean report is not proof that the program is correct, so tests are still needed. In a team project I would run all three tools automatically on every pull request (CI or a pre-commit hook) so problems are caught while the change is still small, keep security findings at the top of the review, and add tests alongside them.
