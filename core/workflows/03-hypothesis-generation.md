# 03 · Hypothesis generation

Stage **S3**. Executed by the Director in the Hypothesis Analyst seat (see
`roles/hypothesis-analyst.md`). This is the stage where most research fails
quietly: a single plausible explanation is formed, and everything afterwards
serves it.

---

## 1. Purpose

Turn actor models and adjudicated interaction into **competing explanations**, each
with a mechanism and a pre-registered, falsifiable prediction set.

The output is not "the answer". It is a register of live rivals plus the
instrumentation needed to separate them.

---

## 2. Where hypotheses come from

Three legitimate sources, in this order:

1. **Actor models.** If actor A's structure makes behaviour X rational while an
   observer would call X irrational, the explanation of X is a hypothesis. This is
   the highest-value source, because it is the thing a search engine cannot give you.
2. **Adjudicated interaction.** Where two feasible actions collided, the resolution
   mechanism is itself a hypothesis ("the outcome reflects A's veto, not A's
   preference").
3. **Documented interpretations in the material.** What analysts and officials say
   is going on. Lowest value — it is the most available and the most contested.

**Not a source:** the researcher's prior, the most-upvoted take, or the framing
implied by the question. If the question presupposes an answer ("why is X
escalating?" presupposes escalation), name the presupposition as an `ASM` and
generate a hypothesis that denies it.

---

## 3. Anatomy of a hypothesis

Every `HYP` needs all of the following. Missing fields block the gate.

| Field | Requirement | Why it is not optional |
|---|---|---|
| `statement` | One sentence, declarative | Multi-clause hypotheses cannot be disconfirmed |
| `mechanism` | The causal chain, step by step: A because B because C | A conclusion without a mechanism cannot generate novel predictions, only restate its evidence |
| `scope` | Where and when it claims to hold | Unbounded hypotheses are unfalsifiable |
| `premises` | `FACT`/`CLM` IDs it rests on | Enables the revision check in workflow 06 |
| `assumptions` | `ASM` IDs it needs | Feeds the key-assumptions check |
| `predictions` | ≥1 `PRD`, pre-registered | P3 |
| `supporting` / `undermining` | `EVD` IDs, filled as evidence arrives | Keeps the ledger honest in both directions |
| `relation_to_others` | `contradicts` / `overlaps` / `subsumes` / `conditional` | Determines which pairs are worth investigating |
| `status` | `draft` → `live` → `weakened` / `strengthened` / `excluded` | Drives the stop rule |

### On mutual exclusivity

Do **not** manufacture exclusivity to look rigorous. Real explanations frequently:

- overlap (two mechanisms both operating),
- nest (one is a special case of another),
- hold conditionally (each true under different conditions).

Record the relation instead. The value of a rival is that evidence can discriminate
it — not that it contradicts.

---

## 4. Mechanism discipline

A mechanism must be a chain with identifiable links, each of which could break.

Weak: "The delay was caused by internal opposition."
Strong: "The delay came from the finance ministry's veto (ASM-002): the programme
requires co-signature (FACT-011), the ministry's cost estimate exceeded the
statutory ceiling (FACT-014), and the ministry's own constituency bears the cost
(ACT-002 factions). If the ceiling were raised, the veto would disappear — the
prediction in PRD-004 tests exactly this."

The strong version names the links, so a single broken link is a finding.

---

## 5. Predictions: pre-registration is the whole point

For each hypothesis, write predictions **before** any investigation that could
test them. The register is timestamped and frozen.

Each `PRD` requires:

| Field | Content | Bad example | Good example |
|---|---|---|---|
| `observable` | What a researcher could actually look at | "increased tension" | "the ministry's published implementation schedule" |
| `indicator` | The specific signal and its source type | "statements" | "any revision to the schedule in the official gazette" |
| `window` | `from` / `to` | — | 2026-12-01 → 2027-03-31 |
| `confirm_if` | Threshold for support | "if things change" | "schedule revised within 60 days of the ceiling vote" |
| `disconfirm_if` | Threshold for refutation | — | "schedule proceeds unchanged past the window" |
| `counter_indicator` | What we would expect **not** to see | — | "no new cost estimate is published" |
| `strength` | `strong` / `moderate` / `weak` | — | strong = the rival hypothesis predicts the opposite |

### The `counter_indicator` field is not decoration

It is what makes a prediction discriminating rather than merely directional. A
prediction whose absence-of-signal is identical under both hypotheses cannot
separate them, and belongs in the register as `strength: weak` with that stated.

### Discriminating predictions

For each prediction, name the hypothesis pair it can separate:

- If hypothesis A holds → indicator present.
- If hypothesis B holds → indicator absent, or a different indicator present.

If you cannot state both branches, the prediction is not yet a discriminator.
Keep it (it may still be useful), mark it `strength: weak`, and keep looking for a
better one.

---

## 6. Procedure

1. Re-read actor models and the adjudication note. Do not re-read the web.
2. List candidate explanations without filtering. Aim for one more than feels
   natural — the last one is usually the one the researcher did not want.
3. For each, write the mechanism chain. Drop any that cannot be chained; keep them
   in `hypotheses/` as `draft` with a note on the missing link.
4. Assign `relation_to_others` pairwise.
5. Write predictions per hypothesis, including `counter_indicator`.
6. Freeze `prediction_set` in `index.json` with a timestamp.
7. Promote to `live` only those with a mechanism and ≥1 prediction.

A useful default is 3–5 live hypotheses. Fewer than three usually means the
question was framed to have one answer; more than six usually means the
distinctions are cosmetic.

---

## 7. Key assumptions check (inline, not a separate ceremony)

For every load-bearing assumption, record an `ASM`:

```json
{
  "id": "ASM-002",
  "statement": "The finance ministry can block the programme unilaterally",
  "held_by": ["HYP-001", "HYP-003"],
  "falsifier": "A programme that proceeded over the ministry's objection",
  "blast_radius": "If false, HYP-001 loses its mechanism and HYP-003 gains",
  "checked": false
}
```

`blast_radius` is what makes this useful: it tells the investigator which
assumption to test first. An assumption with a large blast radius and no check is
the highest-value investigation target in the whole run.

---

## 8. Outputs

| File | Content |
|---|---|
| `hypotheses/HYP-00N.json` | Per `hypothesis.schema.json` |
| `predictions/PRD-00N.json` | Per `prediction.schema.json`, `registered_at` set |
| `assumptions/ASM-00N.json` | With falsifier and blast radius |
| `index.json` | `prediction_set` frozen |

---

## 9. Gate to S4

- [ ] ≥3 live hypotheses, or a written justification for fewer
- [ ] Every live hypothesis has a mechanism chain with named links
- [ ] Every live hypothesis has ≥1 prediction with all seven fields
- [ ] Every prediction names the pair it can separate, or is marked `weak`
- [ ] At least one prediction per hypothesis has a non-empty `counter_indicator`
- [ ] `prediction_set` frozen before any `INV` is created
- [ ] Presuppositions in the original question are recorded as `ASM`

---

## 10. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| All hypotheses agree in direction, differ in emphasis | Not rivals, just shades | Generate one that predicts the opposite; if impossible, the question has one answer and OIR is the wrong tool |
| Predictions all read "X continues / X intensifies" | No thresholds, no windows | Force `disconfirm_if` first, then derive the rest |
| Every prediction is `weak` | Mechanism too vague to derive specifics | Return to §4; a mechanism that implies nothing is not a mechanism |
| Assumptions listed but never used | `blast_radius` missing | Add it; sort investigation order by it |
| Hypotheses cite only supporting evidence at creation | Premature commitment | Leave `undermining: []` empty rather than filling it with weak items; it is filled in S4 |
