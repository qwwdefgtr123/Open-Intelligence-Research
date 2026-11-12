# 06 · Iterative research, synthesis and stop

Stage **S6**, plus the loop control for the next round. Executed by the Synthesis
seat (Extended) or the Director (Lean/Standard, declared).

Read `roles/synthesis-analyst.md`.

---

## 1. Purpose

Update the state honestly, decide whether another round is worth its cost, and —
when the run stops — write a report that a sceptical reader can audit.

Three jobs, in this order. Doing synthesis before the update is how a report ends up
describing a state of knowledge that the ledger no longer holds.

---

## 2. State update (do this first)

### 2.1 Hypothesis status

| Transition | Condition |
|---|---|
| `live` → `strengthened` | ≥1 decisive/strong supporting evidence and no successful attack on its mechanism |
| `live` → `weakened` | ≥1 disconfirmed prediction, or a successful attack on a mechanism link, or the balance of evidence shifted against |
| `live` → `excluded` | A load-bearing link proven false, or all predictions disconfirmed |
| stays `live` | Insufficient movement — and say so, rather than assigning a direction |

Excluding a hypothesis requires a `DEC` with the reason. "It seems unlikely" is
not a reason; a broken mechanism link is.

### 2.2 Prediction judgements

Confirm every `PRD` touched this round has a judgement. `pending` is legitimate;
unnoticed is not.

### 2.3 Model revision check (the step most often skipped)

For every `disconfirmed` prediction, decide **which thing was wrong**:

| Verdict | Test | Consequence |
|---|---|---|
| The hypothesis was wrong | The actor behaved as modelled, but the mechanism linking behaviour to outcome failed | Revise `HYP` only |
| The actor model was wrong | The observed behaviour contradicts the actor's stated reaction function or feasible-action set | Revise `ACT` (new version), and re-run that seat |
| Both | Mechanism and behaviour both off | Revise both; re-derive the hypothesis from the revised model |
| Neither — the evidence is weak | The disconfirmation rests on a single-source or contested item | Downgrade the evidence, leave both intact, open an `INV` |

Write `DEC` kind `model-revision` with the verdict and the reasoning. Update
`ACT.version` and append to `change_log`. Mark dependent hypotheses `stale: true`
until re-derived.

Skipping this check is the failure the whole iteration loop exists to prevent: the
hypothesis gets revised, the model keeps its error, and the same mistake
reappears next round wearing a new prediction.

### 2.4 Conflict and assumption close-out

For each `CFL`: resolve (`revised-model` / `revised-hypothesis`) or leave `open`
with a note. For each `ASM` checked this round: set `checked: true` and record
what was found.

---

## 3. Assessment: four columns, one band

Per live hypothesis, fill the table in `CORE_SPEC.md` §10.

Worked example:

| Hypothesis | Evidence support | Independence | Prediction record | Logic | Band |
|---|---|---|---|---|---|
| HYP-001 | moderate (3 support, 1 contrary) | 2 independent (3 sources, 2 roots) | 2/3 confirmed, 1 pending | minor gaps | **moderate** |
| HYP-002 | weak (1 support, 0 contrary) | 1 (single origin) | 0/2 judged, 2 pending | complete | **weak — untested** |

Then one sentence per band: *what would move it up*. For HYP-002: "a second,
independent record of the same mechanism would move this to moderate."

Rules:

- Never collapse the four columns into a single number.
- Never label a band `strong` when its independence count is 1.
- A hypothesis with zero judged predictions cannot exceed `weak`, however complete
  its mechanism. Elegance is not evidence.

---

## 4. Next-round decision

### 4.1 Value ranking

For each candidate next step, record:

| Field | Content |
|---|---|
| Target | Which hypothesis pair or assumption it would move |
| Obtainability | `likely` / `plausible` / `unlikely` |
| Cost | `1` / `2` / `3` |
| Expected movement | Which band or judgement it could change, and in which direction |

Sort by the same ordinal rule as workflow 04. This is a **ranking**, not a
probability, and not a "value of information" in the decision-theoretic sense —
saying so would be fake precision.

### 4.2 Proceed or stop

Apply the stop rules from `CORE_SPEC.md` §9. Record the evaluation, including the
rules that did **not** fire:

```json
{ "kind": "stop", "fired": null, "checked": ["S1","S2","S3","S4","S5"],
  "note": "S1 not met: PRD-009 and PRD-011 still separable by the scheduled publication.",
  "decision": "continue", "next_round_focus": ["INV-007"] }
```

Progressing to another round requires a named next-round focus that can plausibly
change a band. "Search more" is not a focus. If no focus survives the ranking, S1
has effectively fired even if the wording does not match — stop.

---

## 5. Synthesis and report

Write `report.md` only when the run stops. Structure per
`templates/final-report.md`:

1. **Answer** — the current best judgement, in the first paragraph, with its band.
2. **What would change it** — the specific observations that would move the answer.
3. **Competing explanations** — the register with bands, including weakened and
   excluded ones and why they fell.
4. **What is established** — facts with verification levels.
5. **What is inferred** — with the chain, and where it is weakest.
6. **What is unresolved** — hypotheses still indistinguishable, predictions still
   pending, uncertainties open.
7. **Method record** — tier, seats, runs, queries, rounds, degradation events,
   stop rule that fired.
8. **Sources** — grouped by root source, with dependency noted.

### The dissent rule

If a live hypothesis was held by one seat and rejected by the synthesis, it appears
in the report with its strongest case and the reason it was rejected. Silent
majoritarianism destroys the only thing multi-seat analysis buys.

### The honesty rules

- Do not upgrade a band in the report relative to the ledger.
- Do not describe an untested hypothesis as "holding up well".
- Do not omit a failed investigation because it produced nothing.
- If degradation occurred, it is in the first section, not a footnote.

---

## 6. Outputs

| File | Content |
|---|---|
| `iterations/round-NN.md` | Status changes, judgments, revision verdicts, anti-theatre answers, next-round ranking, stop evaluation |
| `decisions/DEC-*.json` | Status exclusions, model revisions, stop decisions |
| `uncertainties/UNC-*.json` | Open questions with resolution paths |
| `report.md` | Only on stop |
| `index.json` | Counters, final snapshot hash |

---

## 7. Gate (per round, and at stop)

Per round:

- [ ] Every `PRD` touched has a judgement
- [ ] Every `disconfirmed` prediction has a model-revision verdict
- [ ] Every `ACT` revised, or explicitly confirmed unchanged, with reason
- [ ] Assessment table filled with all four columns per live hypothesis
- [ ] Dissent preserved where a seat disagreed
- [ ] Next-round ranking recorded, or stop rule evaluated

At stop:

- [ ] A `DEC` of kind `stop` names the rule that fired
- [ ] Unresolved table complete
- [ ] Method record matches `index.json` counters exactly
- [ ] Degradation events listed in section 1 if any occurred

---

## 8. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Report is more confident than the ledger | Synthesis smoothing | Re-derive bands from the table; do not adjust by feel |
| Model never revised despite disconfirmation | §2.3 skipped | Force the four-way verdict for every disconfirmation |
| Round 3 looks like round 2 with new words | No new discriminating investigation | S1 has effectively fired; stop |
| Minority view disappears | Majority synthesis | Apply the dissent rule; retrieve it from the seat output |
| Costs in the report are round numbers that do not match `index.json` | Estimated instead of copied | Copy the counters |
| "Further research needed" as the conclusion | No band assigned | Assign a band to every live hypothesis before writing |
