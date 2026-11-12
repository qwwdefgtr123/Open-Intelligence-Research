# 05 · Adversarial review

Stage **S5**. Executed by the Red Team seat, in its own execution unit. One review
per round.

Read `roles/red-team-analyst.md`.

---

## 1. Purpose

Attempt to break the run's own conclusions, and make the attempt auditable.

This stage exists because a hypothesis's author cannot certify it, and because a
review that produces no change is indistinguishable from a review that did not
happen. Both problems are addressed structurally: blind input, bounded attack
surface, and mandatory adjudication of every finding.

---

## 2. Blind input

The Red Team seat receives a **de-identified** ledger:

| Included | Excluded |
|---|---|
| `HYP` statement, mechanism, scope, predictions, evidence links | Which actor seat or analyst produced it |
| `EVD` descriptions, sources, independence notes | The Director's ranking or preference |
| `ACT` models with actor names replaced by `PARTY-A/B/C` | Actor names, seat identities, round history |
| `ASM` register with `blast_radius` | Prior rounds' conclusions |

Why this is not paranoia: identity markers measurably skew how language models
weigh arguments — they adopt a peer's position based on who said it rather than on
the argument, and stripping identity improves reliability (arXiv:2510.07517,
recorded in `references/METHODS.md` §3). Removing names costs nothing and removes
a known bias channel.

Implementation: write `review/redteam-input-r<N>.md` with the anonymised ledger, and
record the substitution map in `index.json` so adjudication can re-identify later.

---

## 3. Bounded attack surface

Six attack surfaces. The seat must address all six; it may add more.

| # | Surface | What to attack |
|---|---|---|
| A1 | **Leading hypothesis** | Construct the strongest case that it is wrong. Steelman it first, then break it |
| A2 | **Mechanism chains** | Find the weakest link in each chain. Which step is asserted rather than shown? |
| A3 | **Premises and assumptions** | Which `ASM` has the largest `blast_radius` and has not been checked? What happens to the register if it is false? |
| A4 | **Evidence independence** | Which "corroborations" reduce to one root source? Which evidence was selected because it fits? |
| A5 | **Missing parties** | Which actor with a real interest is absent from the model? Whose reaction is unmodelled? |
| A6 | **Discriminating power** | Which predictions cannot actually separate the hypotheses — because both predict the same observation? |

### Explicitly out of scope

The seat is **not** asked to argue the opposite of everything, produce a "balanced
view", or generate alternative hypotheses at volume. Sustained zero-sum opposition
degrades reasoning quality in both humans and models; unbounded contrarianism
produces noise that the Director then has to filter, which converts a review into
a second opinion poll. The output is targeted attacks on named entities, not a
contrary essay.

---

## 4. Finding format

Every finding is an entity-anchored claim:

```json
{
  "finding": "F-03",
  "surface": "A2",
  "target": "HYP-002",
  "anchor": ["ASM-004", "EVD-011"],
  "claim": "The mechanism assumes the regulator can act before the deadline; EVD-011 shows the statutory clock runs past the window.",
  "severity": "high",
  "what_would_change_my_mind": "A filing showing an emergency procedure exists."
}
```

Requirements:

- `target` must be an existing ID. A finding that attacks "the analysis in general"
  is rejected.
- `anchor` must cite the specific entities the attack rests on.
- `severity`: `high` (would change a status band) / `medium` (would change a
  prediction judgement) / `low` (presentation or minor).
- `what_would_change_my_mind` is mandatory. It is the reviewer's own falsifier and
  the main defence against a review that is itself unfalsifiable.

---

## 5. Adjudication (Director, mandatory)

Every finding gets a verdict. This is the step that separates a review from
decoration.

| Verdict | Meaning | Obligation |
|---|---|---|
| `ACCEPT` | The attack lands | Update the target entity; the change appears in `iterations/round-NN.md` |
| `PARTIAL` | Part of the attack lands | State which part; update accordingly |
| `REJECT` | The attack does not land | Write **why**, citing entities |

```json
{
  "id": "DEC-008",
  "kind": "redteam-verdict",
  "finding": "F-03",
  "verdict": "ACCEPT",
  "rationale": "EVD-011 establishes the statutory clock; HYP-002's mechanism requires action before it. Mechanism revised; PRD-007 re-judged inconclusive.",
  "refs": ["HYP-002", "EVD-011", "PRD-007"]
}
```

### The anti-theatre test

After adjudication, answer two questions in `iterations/round-NN.md`:

1. **Did any finding change a status band, a prediction judgement, or an actor
   model?** If no, and this is the second consecutive round with no change, the
   review is not functioning. Say so explicitly and treat the round as failed for
   stop-rule purposes (S3 no-progress applies to the review too).
2. **Was any `REJECT` justified by a source the red team could not see?** If so,
   that is a blind-input defect, not a red-team failure. Fix the input set next
   round.

A review that survives with zero accepted findings in round 1 is suspicious. One
that survives with zero accepted findings twice is broken.

---

## 6. Survival is a result

For hypotheses that withstand review, record what they survived:

```json
"survived": ["A1 steelman", "A4 independence audit", "A6 discriminating power"]
```

The report states this. "No findings against HYP-003 on surfaces A1 and A4" is
information a reader needs, and it is the only thing that distinguishes a
well-tested hypothesis from an untested one.

Conversely, a hypothesis that was never attacked on a surface is **untested on that
surface** — not "clean". The report must not present untested as verified.

---

## 7. Outputs

| File | Content |
|---|---|
| `review/redteam-input-r<N>.md` | Anonymised ledger handed to the seat |
| `review/redteam-findings-r<N>.md` | Findings F-01.., all six surfaces answered |
| `decisions/DEC-*.json` | One `redteam-verdict` per finding |
| `iterations/round-NN.md` | Anti-theatre test answers and the resulting changes |

---

## 8. Gate to S6

- [ ] All six surfaces addressed (A1–A6), each with at least one finding or an
      explicit "no finding, because…"
- [ ] Every finding has `target`, `anchor`, `severity`,
      `what_would_change_my_mind`
- [ ] Every finding has a verdict with rationale
- [ ] Every `ACCEPT`/`PARTIAL` verdict has produced a concrete change or a written
      reason why the change is deferred to the next round
- [ ] Anti-theatre test answered in the iteration record
- [ ] De-identification map stored for adjudication

---

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Findings read "the analysis could be deeper" | No entity anchoring | Reject findings without `target` ID |
| Red team produces five alternative hypotheses | Role confusion — it is not a second hypothesis generator | Restrict to the six surfaces |
| All findings `REJECT`, all with plausible reasons | Adjudicator protecting the work | Re-examine `PARTIAL` as the default; require entity citation for every `REJECT` |
| Red team attacks a hypothesis the Director already excluded | Stale input set | Pass the current status in the ledger |
| Zero findings on A4 (independence) | Reviewer lacks source detail | Include `independence_note` in the input; it is the highest-yield surface |
| Review takes as long as the investigation | Scope creep | Cap at one review per round; the surfaces are fixed |
