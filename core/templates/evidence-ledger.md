# Evidence ledger — {{RES-ID}} round {{NN}}

## Investigation log

| ID | Question | Separates | Obtainability | Cost | Rank | Result | Null? |
|---|---|---|---|---:|---:|---|---|
| {{INV-001}} | {{discriminating question}} | {{001 vs 003}} | {{likely}} | {{1}} | {{2.0}} | {{cost estimate exceeded ceiling}} | {{false}} |
| {{INV-002}} | {{...}} | {{002 vs 003}} | {{plausible}} | {{2}} | {{0.5}} | {{no record found in gazette}} | **{{true}}** |

Rank is an ordinal heuristic (pairs × obtainability ÷ cost). It is **not** a
probability and must never be reported as one.

## Evidence

### {{EVD-001}} — {{one-line description}}

| | |
|---|---|
| Sources | {{SRC-004, SRC-007}} |
| Direction | {{supports}} |
| Targets | {{HYP-001: decisive}} |
| Strength | {{strong}} |
| Obtained by | {{INV-001}} |

**Independence**

| | |
|---|---|
| Effective independent count | **{{2}}** |
| Reasoning | {{SRC-007 reports on SRC-004's statement; SRC-004 is the root, SRC-007 is derived and contributes 0. SRC-004 and SRC-009 are separate investigations.}} |
| Redundant | {{false}} |

**Alternative readings** (minimum one; without one this record is `weak` by default)

1. {{the same material also fits HYP-003 if the ceiling was advisory}}
2. {{...}}

---

## Independence audit

Root-source collapse is the most common way a small evidence base looks large.

| Root | Sources derived from it | Counted |
|---|---|---:|
| {{SRC-004}} | {{SRC-007, SRC-012, SRC-015}} | 1 |

**Totals:** {{9 records · 4 roots · 5 records flagged redundant}}

## Prediction judgements

| PRD | Hypothesis | Judged | Basis | Note |
|---|---|---|---|---|
| {{PRD-001}} | {{HYP-001}} | {{confirmed}} | {{EVD-001}} | {{within window}} |
| {{PRD-003}} | {{HYP-002}} | {{disconfirmed}} | {{EVD-011}} | {{triggers model-revision check}} |
| {{PRD-005}} | {{HYP-003}} | {{pending}} | — | {{window closes 2027-03}} |
| {{PRD-006}} | {{HYP-001}} | {{inconclusive}} | {{EVD-014}} | {{window closed, neither threshold met}} |

## Fact revisions triggered this round

| New fact | Supersedes | Dependents flagged stale |
|---|---|---|
| {{FACT-021}} | {{FACT-007}} | {{ACT-002, HYP-001}} |

## Budget

| | Used | Cap |
|---|---:|---:|
| Queries this round | {{24}} | {{35}} |
| Investigations dropped | {{2}} | — |
