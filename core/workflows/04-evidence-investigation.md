# 04 · Evidence investigation

Stage **S4**. Executed by the Evidence seat (Standard/Extended) or the Director
(degradation, declared). Runs once per round.

Read `roles/evidence-investigator.md`.

---

## 1. Purpose

Obtain material that **separates** live hypotheses, and account for it honestly —
including the material that turned out not to exist.

The failure this stage exists to prevent: an investigator who searches for support
for the leading hypothesis, finds it, and reports success.

---

## 2. Ranking: where to spend retrieval

Investigations compete for budget. Rank them, take the top *k*.

```
score(INV) = Σ over live hypothesis pairs P that INV can separate: 1
             × obtainability   (0.2 = unlikely | 0.5 = plausible | 1.0 = likely)
             ÷ cost            (1 = one query | 2 = several | 3 = document retrieval / paywalled)
```

Then sort descending and cut at the round budget.

**This is an ordinal heuristic, not a probability.** It answers "which of these is
most worth trying first". It must never be reported as an expected information
gain, a likelihood, or a percentage. Doing so would be exactly the fake precision
`PRINCIPLES.md` P6 forbids.

### The admission test

An investigation must name the pair it separates:

```json
"separates": [["HYP-001", "HYP-003"]]
```

If you cannot fill this field, the task is "search the topic", not "investigate".
Rejected at intake. Topical relevance is not a justification.

### Prefer high-blast-radius assumptions

An `ASM` with `blast_radius` naming several hypotheses outranks an investigation
that touches one, at equal obtainability — it can move more of the register per
query.

---

## 3. Procedure per investigation

1. **State the discriminating question.** Not "what is the state of X" but "did the
   ministry's cost estimate exceed the ceiling — yes or no, and where is it
   recorded?"
2. **Predict both answers before looking.** Write into `INV.expected_if`:
   what the world looks like if the first hypothesis holds, and if the second does.
   This is the anti-confirmation-bias device: you commit to what would surprise you
   before you can be surprised.
3. **Retrieve.** Prefer primary documents over reporting about them. When using
   reporting, trace what it cites.
4. **Record sources with dependency.** `SRC.derived_from` for anything syndicated,
   translated, or sourced from another outlet. See workflow 01 §B3.
5. **Write evidence** with direction, target hypotheses, strength, independence
   accounting, and at least one alternative reading.
6. **Record the null result** if nothing was found. `null_result: true` plus what
   was searched and where. This prevents the next round repeating the same search
   and prevents "we found nothing" from silently becoming "there is nothing".

---

## 4. Evidence records

Every `EVD` needs:

| Field | Content |
|---|---|
| `description` | What the material says, in one or two sentences, without interpretation |
| `source` | `SRC` IDs |
| `direction` | `supports` / `undermines` / `neutral` |
| `targets` | Array of `{hypothesis, weight}` — `weight` in `decisive`/`strong`/`weak` |
| `strength` | `strong` / `moderate` / `weak` |
| `independence_note` | Integer effective independent count + reasoning |
| `alternative_readings` | ≥1 other explanation of the same material |
| `obtained_by` | `INV` ID |

### `alternative_readings` is the quality control

Material that fits one hypothesis usually also fits another. If you cannot state a
second reading, you have not evaluated the evidence — you have quoted it. An
evidence record with a single reading scores as `weak` by default, regardless of
how authoritative the source looks.

### Redundancy handling

| Situation | Handling |
|---|---|
| Two outlets, same wire copy | One root source; second is `redundant`, contributes 0 to independence |
| Official statement + reporting on it | Statement is the source; reporting is derived |
| Two genuinely separate investigations reaching the same conclusion | Two roots; count 2 |
| One source quoted by five analysands | One root |

The effective independent count is the number that goes into the assessment table
in the report. The URL count does not.

---

## 5. Judging predictions

When evidence bears on a `PRD`, judge it — and only after the window or on
decisive material:

| Judgement | When |
|---|---|
| `confirmed` | `confirm_if` met, within window |
| `disconfirmed` | `disconfirm_if` met, within window |
| `inconclusive` | Window closed, neither threshold met |
| `pending` | Window still open |
| `not-observable` | The indicator cannot be observed with available access |

A `disconfirmed` prediction is the most valuable output of this stage. It forces
the model-revision check in workflow 06. Treat it as a result, not a setback, and
never re-label it `inconclusive` to protect a hypothesis.

If a prediction is judged before `registered_at` was locked, mark `late: true` and
exclude it from the record count.

---

## 6. What to do when evidence contradicts the fact base

Occasionally an investigation turns up something that contradicts a frozen `FACT`.

Do not silently overwrite. Instead:

1. Create a new `FACT` with `supersedes: "FACT-007"`.
2. Write `DEC` kind `fact-revision` with what changed and which actor models,
   hypotheses and predictions depended on the old version.
3. Bump `fact_snapshot` to v2.
4. Flag affected `ACT` records as `stale: true`. Their revision happens in
   workflow 06, not here.

This is the mechanism that lets evidence correct the simulation instead of being
absorbed by it.

---

## 7. Outputs

| File | Content |
|---|---|
| `investigations/INV-00N.json` | Question, `separates`, expected_if, result, `null_result` |
| `evidence/EVD-00N.json` | Per §4 |
| `sources/SRC-00N.json` | New or amended sources with dependency |
| `index.json` | Counters: queries, `prediction` judgements |

---

## 8. Gate to S5

- [ ] Every `INV` has non-empty `separates`
- [ ] Every `INV` decided and closed, including null results
- [ ] Every `EVD` has `alternative_readings` ≥1 and a numeric independence count
- [ ] No two `EVD` share a single root source counted as two independent supports
- [ ] Every `PRD` touched by evidence has a judgement, or is explicitly left `pending`
- [ ] Queries counted against budget

---

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| All evidence supports the leading hypothesis | Investigator knows the leading hypothesis | Strip the ranking before dispatch; re-run with `separates` only |
| Ten sources, all saying the same thing | Dependency graph not applied | Recount by root; expect the count to collapse |
| Investigation returns a topic overview | No discriminating question | Rewrite as a yes/no with a locatable record |
| Null results missing | Only successes logged | Require `null_result` field on every `INV` |
| Prediction judged `inconclusive` right after being refuted | Protective relabelling | Re-judge against `disconfirm_if` only |
| Every `EVD` is `strong` | No alternative readings | Downgrade to `weak` until a second reading exists |
