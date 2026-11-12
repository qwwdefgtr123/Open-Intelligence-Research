# Round 01 — RES-001

## Inputs frozen
- `fact_snapshot` v1: FACT-001 … FACT-005 (hash `casehash-intel-magdeburg-v1`)
- `prediction_set`: PRD-001 … PRD-006, registered 2026-11-13T02:15:00Z, before any
  `INV` exists
- `actor_set`: ACT-001, ACT-002, ACT-003 with distinct execution units and distinct
  input hashes

## What this round did and did not do

This run exists as the **Mode B** arm of the A-vs-B comparison. By design it executed
S0, S1, S2/S2b and S3 only. It did **not** execute S4 (discriminating investigation)
or S5 (blind review), because those define Modes C and D, not Mode B.

Consequence, stated plainly: **no hypothesis changed status this round, and no
prediction was judged.** There is no evidence ledger, so nothing could be judged. All
five hypotheses remain `live`, all six predictions remain `pending`.

## Adjudication (S2b)

The three seats produced incompatible causal claims, which is the point of running
them separately:

| Seat | Claim about the cause | Consequence |
|---|---|---|
| ACT-001 Intel | Option value plus a cash-gated capital rule; "demand" is the polite form of "we ranked you last" | The decision was fiscal-financial, and irreversible |
| ACT-002 Germany | The fate was settled in Berlin's budget line; the finance ministry was always going to reclaim the earmark | The decision was political-fiscal on the *German* side, and Intel's cancellation merely ratified it |
| ACT-003 Saxony-Anhalt | Intel will not return; the state's rational play is to keep the site warm and move the blame upward | No actor in the system has both the means and the motive to restart the project |

Resolution attempt: ACT-001 and ACT-002 are **compatible at different causal layers**
(Intel's cash constraint and Berlin's reclamation push the same way); ACT-003 is a
prediction about the future rather than a claim about the past, and it constrains what
evidence would count next round.

No conflict was recorded as `CFL` because none of the three claims can be shown
incompatible without the evidence this round did not collect — and inventing a
conflict to look rigorous would be worse than leaving it open.

## Assessment

Four columns, no composite. Every band is `weak` for the same reason.

| Hypothesis | Evidence support | Independence | Predictions | Logic | Band |
|---|---|---|---|---|---|
| HYP-001 | none registered | — | 0/2 judged, 2 pending | minor gaps (Magdeburg sunk cost unverified) | **weak, untested** |
| HYP-002 | none registered | — | 0/1 judged, 1 pending | major gaps (FACT-004 single-source, dispute not resolution) | **weak, untested** |
| HYP-003 | none registered | — | 0/1 judged, 1 pending | major gaps (argued from absence of evidence) | **doubtful only** |
| HYP-004 | none registered | — | 0/1 judged, 1 pending | minor gaps | **weak, untested** |
| HYP-005 | none registered | — | 0/1 judged, 1 pending | major gaps (aid decision text not retrieved) | **weak, untested** |

What would move each up one band:
- HYP-001: one capex document showing total capex flat while the EU site is cut.
- HYP-002: the budget line's post-2024 status, or one non-aggregated German source.
- HYP-003: a single named European anchor customer that existed and was lost — or a
  second confirmation that none existed.
- HYP-004: Ohio construction milestones in the cancellation window.
- HYP-005: the Commission's aid decision text.

## Next-round ranking (ordinal, not a probability)

| Target | Investigation | Separates | Obtainability | Cost | Note |
|---|---|---|---|---|---|
| PRD-005 / PRD-001 | Ohio construction milestones vs total capex guidance | HYP-004 vs HYP-001 | likely | 2 | Highest value: the two leading rivals predict opposite things here |
| PRD-003 | Status of the EUR 9.9bn in federal budget documents | HYP-002 vs HYP-001 | plausible | 2 | Also repairs the weakest premise in the register (FACT-004) |
| PRD-006 | Commission state-aid register for the site | HYP-005 vs HYP-001 | likely | 1 | Cheap, and tests a mechanism nobody else covers |
| PRD-004 | Node generation of new European capacity | HYP-003 vs HYP-005 | plausible | 3 | Most expensive; lowest marginal value this round |

## Stop decision

`DEC` kind `stop`, rule **S5 (user stop)**: this run was commissioned as a bounded
comparison case, one round by design. Rules checked and **not** fired: S1 (discrimination is
nowhere near exhausted — the ranking above is full), S2 (budget: 4 of 13 runs,
6 of 120 queries), S3 (no-progress cannot be assessed in a one-round run), S4 (the key
windows are open, not unobservable).

Recording S5 rather than a substantive rule matters: the run stopped because it was
told to, not because the question was answered. A report claiming otherwise would be
the exact failure mode `PRINCIPLES.md` P6 forbids.
