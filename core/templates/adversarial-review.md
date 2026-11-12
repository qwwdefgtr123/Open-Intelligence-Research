# Adversarial review — round {{NN}}

> Seat: Red Team, isolated execution unit. Input de-identified: actor names replaced
> by PARTY-A/B/C, no proposer identity, no Director ranking. Substitution map held in
> `index.json` for adjudication only.

## Input defects noted by the reviewer

- {{e.g. "finding anchors reference EVD-007 which is absent from the input"}}
- {{none}}

## Findings

### {{F-01}} — surface {{A2}} — target {{HYP-002}} — severity {{high}}

**Anchor:** {{ASM-004, EVD-011}}

**Claim:** {{the mechanism assumes the regulator can act before the deadline; EVD-011 shows the statutory clock runs past the window.}}

**What would change my mind:** {{a filing showing an emergency procedure exists.}}

**Verdict:** {{ACCEPT}} · **DEC:** {{DEC-008}}

**Rationale:** {{EVD-011 establishes the clock; HYP-002's mechanism requires action before it. Mechanism revised; PRD-007 re-judged inconclusive.}}

---

### {{F-02}} — surface {{A4}} — target {{EVD-004}} — severity {{high}}

**Anchor:** {{SRC-007, SRC-012}}

**Claim:** {{the two corroborating reports both derive from SRC-004; the effective independent count is 1, not 2.}}

**What would change my mind:** {{evidence that SRC-012 conducted separate reporting.}}

**Verdict:** {{PARTIAL}} · **DEC:** {{DEC-009}}

**Rationale:** {{SRC-012 adds an independent interview in paragraph 4, so the count is 2 but not 3. Record amended.}}

---

## Surface coverage

Every surface must be answered. A skipped surface reads as clean, which is a false signal.

| Surface | Findings | Or "no finding, because…" |
|---|---|---|
| A1 Leading hypothesis | {{F-01}} | — |
| A2 Mechanism chains | {{F-01}} | — |
| A3 Premises and assumptions | {{none}} | {{ASM-002 already tested by INV-003 and confirmed}} |
| A4 Evidence independence | {{F-02}} | — |
| A5 Missing parties | {{F-03}} | — |
| A6 Discriminating power | {{none}} | {{all four live predictions name distinct observable thresholds}} |

## Closing lines

```
Strongest single objection to the leading view: {{...}}
Minority point most worth preserving: {{...}}
```

---

## Adjudication summary (Director)

| Finding | Verdict | Change produced |
|---|---|---|
| F-01 | ACCEPT | HYP-002 mechanism revised; PRD-007 re-judged |
| F-02 | PARTIAL | EVD-004 independence count 2, not 3 |
| F-03 | REJECT | PARTY-D has no feasible action per FACT-018; rationale in DEC-010 |

### Anti-theatre test

1. Did any finding change a status band, a prediction judgement, or an actor model?
   **{{Yes — 2 of 3 findings produced a change.}}**
2. Was any REJECT justified by material the red team could not see?
   **{{No.}}**

> If both answers are "no" / "yes-with-hidden-material" for two consecutive rounds,
> the review is not functioning. Say so and treat the round as no-progress.

## Hypotheses that survived

| Hypothesis | Surfaces withstood | Surfaces not attacked |
|---|---|---|
| {{HYP-001}} | {{A1, A4}} | {{A6 — untested, not clean}} |
