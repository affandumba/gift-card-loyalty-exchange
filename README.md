# Gift Card & Loyalty Point Exchange

> Software Engineering coursework — requirements engineering, use-case modeling, and architectural design for a wallet application that converts loyalty points from linked merchant accounts into a unified exchange credit, redeemable for digital gift cards.

**Author:** Affan Dumba &nbsp;|&nbsp; **SRN:** PES1UG24CS280 &nbsp;|&nbsp; **Section:** E
**Problem Statement #34** — Retail, E-Commerce & Finance

## Overview

This repository contains the lab deliverables for a system that:
- Aggregates loyalty points across multiple linked merchant accounts
- Converts aggregated points into a single exchange credit balance at dynamic rates
- Allows users to redeem that credit for digital gift cards from any participating merchant
- Locks single-use vouchers with anti-fraud checks at redemption time

## Repository Structure

All lab deliverables are organized under `SELABS/`, one folder per lab:

```
SELABS/
├── Lab1/   Requirements Engineering & UML Use-Case Modelling
├── Lab3/   Component Modelling & Architectural Pattern Selection
├── Lab-4/  Vibe Coding - Pac-Man repair (bug fix + 3 features)
├── Lab-5/  Static Code Analysis - Pylint, Bandit and Flake8 on an online exam marker
└── Lab-6/  Code and Branch Coverage - pytest + coverage.py on a tennis scoring module
```

### SELABS/Lab1 — Requirements Engineering & UML Use-Case Modelling

| File | Description |
|------|-------------|
| `Requirements_Table_Affan_Dumba_PES1UG24CS280.xlsx` | Functional (FR-001–FR-005) and non-functional (NFR-001, NFR-002) requirements, with ID, priority, acceptance criteria, and rationale |
| `UseCase_Diagram_Affan_Dumba_PES1UG24CS280.drawio` | UML use-case diagram showing system actors and their relationships to core use cases, including `<<include>>` and `<<extend>>` |
| `UseCase_Flow_RedeemGiftCard_Affan_Dumba_PES1UG24CS280.rtf` | Flow specification for the Redeem Gift Card use case — preconditions, postconditions, main success scenario, and an alternate flow |

**Actors:** Account Holder, Merchant Partner, Exchange Rate Service, System

**Core use cases:** Link Merchant Loyalty Account · Convert Points to Credits · Redeem Gift Card · Lock Voucher *(include)* · Notify Merchant *(include)* · Flag Suspicious Redemption *(extend)*

### SELABS/Lab3 — Component Modelling & Architectural Pattern Selection

| File | Description |
|------|-------------|
| `Component_Diagram_Affan_Dumba_PES1UG24CS280.pdf` | UML component diagram — 6 components, 6 provided/required interfaces, and a `<<use>>` dependency, modeled as a Microservices architecture |
| `Lab3_Architecture_Justification_Affan_Dumba_PES1UG24CS280.pdf` | One-page written justification: architectural choice, two scenario-specific reasons, security advantage, and performance benefit |

**Architecture:** Microservices — Account Holder Portal, Loyalty Aggregation Service, Point Conversion Engine, Voucher & Gift Card Service, Merchant Integration Service, Ledger Database

### SELABS/Lab-4 — Vibe Coding: Pac-Man Repair

| File | Description |
|------|-------------|
| `game.py` | Final Pygame Pac-Man: power pellet bug fixed (`"O"` vs `"o"`), per-ghost frightened colours, bonus fruit + last-pellet HUD flash, bonus life at 1000 points |
| `original_code/game_original.py` | Untouched starter code (before changes) |
| `Lab4_Before_Affan_Dumba_PES1UG24CS280.mp4` | 10 s clip of the original build: power pellet eaten, ghosts never turn frightened |
| `Lab4_After_Affan_Dumba_PES1UG24CS280.mp4` | 10 s clip of the fixed build: frightened ghosts in their own colours, ghosts eaten |
| `Lab4_After_Features_Affan_Dumba_PES1UG24CS280.mp4` | 14 s clip of bonus fruit, bonus life at 1000 points and the win screen (score pre-set to 900) |
| `Lab4_Notes_Affan_Dumba_PES1UG24CS280.md` | What was changed, prompts used, how it was verified |
| `PacMan_Lab_README.md` | Original lab README (tasks and expected behaviour) |
| `tools/play_and_record.py` | Script used to record the clips from the real game window |

Run it with `pip install pygame` then `python SELABS/Lab-4/game.py`.

### SELABS/Lab-5 — Static Code Analysis (Pylint, Bandit, Flake8)

Assigned program: `online_exam.py` (Online Examination System, repo `L5_34_online_exam`). Pylint 5.65 → **10.00/10**, Bandit 4 issues → **0**, Flake8 4 issues → **0**, with unchanged program output.

| File | Description |
|------|-------------|
| `online_exam.py` | Cleaned program (16 issues fixed) |
| `issues.md` | Issue table: type, line(s), description and fix approach |
| `reflection.md` | Reflection on static analysis |
| `requirements_status.md` | Every lab requirement with its status and evidence |
| `reports/before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` before the fixes |
| `reports/after/` | The same three reports after the fixes |
| `reports/README.md` | The exact commands used for the reports |
| `README.md` | Original lab brief from the assigned repo |

The fixes are in three separate commits, one per tool (Bandit, Flake8, Pylint). Run it with `python SELABS/Lab-5/online_exam.py`.

### SELABS/Lab-6 — Code and Branch Coverage

Assigned program: `tennis_scoring.py` (repo `L6_L7_34_tennis_scoring`). Coverage went from 32 % (starter tests) → **95 %** line coverage → **100 %** line and branch coverage (30 of 30 branches).

| File | Description |
|------|-------------|
| `tennis_scoring.py` | Module under test (`game_score`, `set_winner`, `match_status`) |
| `test_tennis_scoring.py` | Starter tests, unchanged |
| `CodeCoverageTest_tennis_scoring_application.py` | 17 tests for code (line) coverage |
| `BranchCoverageTest_tennis_scoring_application.py` | 79 tests covering every branch, including boundary values |
| `screenshots/` | Terminal screenshots of `coverage run` and `coverage report -m` for each stage |
| `README.md` | Results table, approach, and observations |

The work is in two commits, one per stage. Run it with `pip install coverage pytest`, then `coverage run --branch -m pytest BranchCoverageTest_tennis_scoring_application.py` and `coverage report -m` inside `SELABS/Lab-6`.

---

*PES University — Dept. of CSE — Software Engineering Lab coursework.*
