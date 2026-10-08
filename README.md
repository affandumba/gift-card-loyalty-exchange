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
└── Lab3/   Component Modelling & Architectural Pattern Selection
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

---

*PES University — Dept. of CSE — Software Engineering Lab coursework.*
