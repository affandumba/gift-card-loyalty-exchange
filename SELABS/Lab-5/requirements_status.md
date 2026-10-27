# Lab 5 – Requirements and Status

- **Name:** Muhammad Affan Dumba
- **SRN:** PES1UG24CS280 (Section E)
- **Problem statement:** Online Examination System (`online_exam.py`)
- **Assigned repo:** https://github.com/SETAPESU26/L5_34_online_exam (row 34 of `5E_Lab-5-Repo-Assignemnt.xlsx`)

| # | Requirement (source) | Status | Evidence |
|---|----------------------|--------|----------|
| 1 | Set up a Python virtual environment (handout, Software Requirements) | ✅ Done | `python -m venv venv` (folder is git-ignored) |
| 2 | Install Pylint, Bandit and Flake8 (handout) | ✅ Done | Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 |
| 3 | Download the script from the assigned repo (handout) | ✅ Done | `online_exam.py`, cloned from the repo above |
| 4 | Run the program first and note its output (handout Step 1, README) | ✅ Done | Output recorded; identical before and after the fixes |
| 5 | Run Pylint, Bandit and Flake8 and save the reports (handout Step 2) | ✅ Done | `reports/before/` |
| 6 | Document the issues in a table (handout Step 3, README `issues.md`) | ✅ Done | `issues.md`: 16 issues, the handout's 5 columns |
| 7 | Fix at least 4 issues, high and medium severity first (handout, README) | ✅ Done | 16 fixed, both High-severity findings first |
| 8 | Handle all issues reported by Bandit (handout Step 4.1) | ✅ Done | 4 of 4 resolved; "No issues identified" and `#nosec` count is 0 |
| 9 | Pylint score above 9.5 (handout Step 4.2, README) | ✅ Done | 5.65 to **10.00 / 10** |
| 10 | Handle all formatting issues raised by Flake8 (handout Step 4.3) | ✅ Done | 4 of 4 fixed; `reports/after/flake8_report.txt` shows a count of 0 (4 before) |
| 11 | Re-run the tools and verify the fixes (handout Step 4.4 and 4.5) | ✅ Done | `reports/after/` (`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`) |
| 12 | The program still does its job (README) | ✅ Done | Same output; 0 differences on 3000 random classes (10,370 students). Only change: `topper()` returns `None` for an empty class instead of crashing |
| 13 | 3 commits for the fixes, one per tool (handout Deliverables) | ✅ Done | Bandit, Flake8 and Pylint fix commits in `git log` (plus starter, baseline and documentation commits around them) |
| 14 | Pylint, Bandit and Flake8 reports, before and after (handout Deliverables) | ✅ Done | before: `reports/before/`; after: `reports/after/` (same three file names in each; commands in `reports/README.md`) |
| 15 | Cleaned `online_exam.py` with at least 4 issues fixed (README, handout) | ✅ Done | Final file in this folder |
| 16 | `issues.md` (README) | ✅ Done | Present |
| 17 | `reflection.md`, answers to the reflection questions (README, handout) | ✅ Done | Present; four questions with answers, covering all five learning outcomes of the handout |
| 18 | Do not raise a PR to the original repo (course rule) | ✅ Respected | Nothing has been pushed to SETAPESU26 |
| 19 | Push to my own GitHub and submit the repo link | ✅ Done | https://github.com/affandumba/gift-card-loyalty-exchange/tree/main/SELABS/Lab-5 |
