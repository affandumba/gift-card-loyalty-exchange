# Gift Card & Loyalty Point Exchange

> Requirements analysis and use-case modeling for a wallet application that converts loyalty points from linked merchant accounts into a unified exchange credit, redeemable for digital gift cards.

## Overview

This repository contains the requirements engineering artifacts for a system that:
- Aggregates loyalty points across multiple linked merchant accounts
- Converts aggregated points into a single exchange credit balance
- Allows users to redeem that credit for digital gift cards from any participating merchant

## Repository Contents

| File | Description |
|------|-------------|
| `requirements-table.xlsx` | Functional and non-functional requirements, including priority, acceptance criteria, and rationale |
| `usecase-diagram.drawio` | UML use-case diagram showing system actors and their relationships to core use cases |
| `usecase-flow-redeem-giftcard.rtf` | Detailed flow specification for the Redeem Gift Card use case |

## Actors

- **Account Holder** — the end user of the wallet app
- **System** — the voucher and ledger engine
- **Merchant Partner** — receives redemption notifications
- **Exchange Rate Service** — supplies point-to-credit conversion rates

## Use Cases

1. Link Merchant Loyalty Account
2. Convert Points to Credits
3. Redeem Gift Card
4. Lock Voucher *(include)*
5. Notify Merchant *(include)*
6. Flag Suspicious Redemption *(extend)*

## Featured Flow: Redeem Gift Card

The `usecase-flow-redeem-giftcard.rtf` document details the primary redemption flow, including:
- Preconditions and postconditions
- Main success scenario (catalogue browsing → confirmation → credit deduction → voucher generation → merchant notification)
- Alternate flow for insufficient credit balance

---

*Software Engineering coursework — requirements specification and use-case modeling.*
