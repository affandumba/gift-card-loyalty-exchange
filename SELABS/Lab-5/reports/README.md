# Static analysis reports

The same three tools were run on `online_exam.py` before and after the fixes (Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1, Python 3.13, inside a `venv`).

| Folder | When | File analysed |
|--------|------|---------------|
| `before/` | before any fix | the original `online_exam.py` (first commit of this folder) |
| `after/` | after all fixes | the final `online_exam.py` |

Commands used for both folders (run from the folder that contains `online_exam.py`; `python -m` is the same as calling the tool directly):

```
pylint online_exam.py > pylint_report.txt
bandit -r online_exam.py > bandit_report.txt
flake8 online_exam.py --count > flake8_report.txt
```

`--count` is the only addition to the commands in the lab handout. It makes Flake8 print the number of findings, so a clean run writes `0` instead of leaving an empty file.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.65 / 10 (20 messages) | 10.00 / 10 |
| Bandit | 4 issues (2 High, 2 Low) | No issues identified |
| Flake8 | 4 findings | 0 |
