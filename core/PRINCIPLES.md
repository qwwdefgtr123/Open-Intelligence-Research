# Principles

Seven principles, plus three operational rules. Each one is written so that a
violation can be **detected**, not merely regretted. If a principle cannot be
checked, it is a slogan, and slogans do not belong here.

Read `CORE_SPEC.md` for the architecture these principles constrain.

---

## P1 — Fact before simulation

Every actor model is built on a frozen, verified fact base. The boundary between
what happened and what we think someone wanted is a structural boundary, not a
stylistic one.

**Requires**
- Facts (`FACT-*`), source claims (`CLM-*`) and inferences live in different files.
- Actor models, hypotheses and predictions reference `FACT-*` / `CLM-*` IDs. They
  may never restate a fact as prose without an ID.
- Each fact carries `verification_level`. A `single-source` fact cannot be the
  sole support for a load-bearing premise of an actor model.

**Forbids**
- Writing a motive into a fact record.
- Promoting a public statement to "what they actually want". A statement is a
  claim about what was said. It is never evidence of intent on its own.
- Running simulation on a fact base that failed its freeze check.

**Detection** — `tests/scripts/validate_state.py`: every `ACT/HYP/PRD` reference
must resolve to an existing entity; `FACT` records with `verification_level:
single-source` flagged when used as an actor's `premises`.

**On violation** — the run stops at the offending stage. Do not "note it and
continue"; a simulation on an unverified premise produces confident nonsense.

---

## P2 — Actor positions are independent

Each actor simulation is generated without knowledge of the others, and without
knowledge of what the researcher hopes to find.

**Requires**
- One isolated execution unit per actor. No shared transcript, no shared context,
  no sequential persona-swapping in a single context.
- Actor outputs are frozen to disk before any actor sees another's output.
- The actor prompt contains the anti-anticipation clause (see
  `roles/actor-simulation.md`) and nothing about the expected conclusion.

**Forbids**
- Showing actor A's model to actor B "for efficiency".
- Telling an actor which hypothesis the researcher favours.
- Implementing multi-perspective analysis by role-playing several actors in one
  conversation. This is the single most common way to fake viewpoint diversity,
  and it produces correlated outputs with a diversity-shaped appearance.

**Detection** — the run manifest records one execution unit per actor with a
distinct input file. `tests/scripts/validate_state.py --check-isolation` fails if
two actors share a `simulation_input_hash`.

**On violation** — discard the affected simulations and re-run isolated. Do not
reconcile them afterwards; the correlation is already in the outputs.

---

## P3 — Hypotheses must be testable

A hypothesis without a prediction that could come out false is not a hypothesis.
It is a narrative.

**Requires**
- Every `HYP` carries at least one `PRD` with: observable indicator, observation
  window, `confirm_if`, `disconfirm_if`, and a `counter_indicator` (what we would
  expect **not** to see if the hypothesis holds).
- Predictions are registered **before** the investigation that tests them.
  `registered_at` earlier than the first related `INV.started_at` is enforced.
- Hypotheses declare `relation_to_others`: `contradicts | overlaps | subsumes |
  conditional`. Mutual exclusivity is not required and must not be fabricated.

**Forbids**
- Predictions phrased so that any outcome confirms them ("tensions may rise or
  fall").
- Post-hoc prediction writing. Late predictions are recorded as `late: true` and
  excluded from the hit rate.
- Manufacturing mutually exclusive hypotheses in order to look like ACH.

**Detection** — schema requires `predictions.minItems: 1`; the validator checks
`registered_at <= INV.started_at` for every linked investigation and counts
`late` predictions.

**On violation** — the hypothesis stays `draft` and is excluded from synthesis.
A weak but honest prediction is acceptable and must be labelled `strength: weak`.

---

## P4 — Investigation must discriminate

Search effort goes where it separates live hypotheses, not where it accumulates
material about the topic.

**Requires**
- Every `INV` declares `separates`: the hypothesis pair(s) it can distinguish.
- Ranking uses the ordinal rule in `workflows/04-evidence-investigation.md`,
  which is explicitly a heuristic, never presented as a probability.
- Null results are recorded. "Searched, found nothing" is a finding.
- Every `EVD` carries at least one `alternative_readings` entry.

**Forbids**
- Running an investigation whose only justification is topical relevance.
- Searching for confirmations of the leading hypothesis.
- Deleting a failed investigation from the ledger.

**Detection** — `separates` is a required non-empty array; `null_result` is a
required boolean; `alternative_readings` has `minItems: 1`.

**On violation** — the investigation is rejected at intake. Re-scope it as a
discriminating question or drop it.

---

## P5 — Opposition must be independent

The agent that proposed a hypothesis never certifies it.

**Requires**
- Red team runs in its own execution unit, receives the ledger with proposer
  identity stripped, and never receives the Director's preferred conclusion.
- Every red-team finding is **adjudicated**: `ACCEPT | PARTIAL | REJECT` with a
  written rationale, recorded as a `DEC` entity.
- Hypotheses that survive review record *which* tests they survived. Survival is
  a result, not an absence of result.

**Forbids**
- Letting the hypothesis author write the rebuttal.
- Accepting a red-team report without adjudication. Unadjudicated review is
  decoration.
- Running red team as a zero-sum adversary. Sustained opposition degrades
  reasoning quality in both humans and models; the role is bounded to specific
  attack surfaces, listed in `roles/red-team-analyst.md`.

**Detection** — `DEC` entities of kind `redteam-verdict` must exist for every
finding ID in the review file; the validator counts unmatched findings.

**On violation** — the review round does not count toward the stop rule. An
unadjudicated review cannot justify stopping.

---

## P6 — Uncertainty is allowed to survive

OIR does not converge for the sake of converging.

**Requires**
- Undecidable questions are recorded as `UNC-*` with what would be needed to
  resolve them.
- The final report lists unresolved items explicitly, including predictions still
  `pending` and facts still `single-source`.
- Confidence uses the fixed vocabulary in `CORE_SPEC.md` §9 (four decomposed
  columns + five qualitative bands). No composite 0–100 score.

**Forbids**
- Reporting a single "confidence: 78%" number. It fuses evidence strength, source
  independence, predictive track record and logical completeness into one figure
  that cannot be audited, and human analysts are known to be poorly calibrated on
  self-reported confidence.
- Presenting agent-assigned scores as probabilities.
- Treating "the team agreed" as evidence.

**Detection** — report template requires the unresolved-items table; validator
rejects any `confidence` numeric field in `HYP`.

**On violation** — strip the number and re-derive the four columns.

---

## P7 — Every judgement is traceable

A reader must be able to walk from a conclusion back to the sources, and from a
source forward to everything it influenced.

**Requires**
- Conclusions cite `HYP` → `EVD` → `SRC`. Actor judgements cite `ACT` → premises.
- Source dependency is recorded: `SRC.derived_from` points at the root source for
  any reprint, syndication or translation.
- Evidence weight uses the **effective independent source count**, not the number
  of URLs. Three outlets carrying one wire story is one source.
- Every state change during a round is written to `iterations/round-NN.md`.

**Forbids**
- Citing a media report when the underlying primary document was available.
- Counting syndicated coverage as corroboration.
- Editing a prior round's file. History is append-only; corrections are new
  entities with `supersedes`.

**Detection** — `EVD.independence_note` must state an integer effective count and
the reasoning; validator compares it against the count of distinct root sources.

**On violation** — the evidence entry is downgraded to `redundant` and excluded
from the independent count.

---

## Operational rules

### O1 — The baseline can win

Every OIR run must remain comparable to a single-agent pass on the same question
with the same fact base. If the single-agent pass is better on the deciding
criterion, say so. A method that cannot lose cannot be evaluated, and the
published evidence on multi-agent debate is unflattering enough that
self-congratulation is not affordable. See `tests/experiments/`.

### O2 — Cost is reported, never invented

Report observable counts: execution units, queries, rounds, wall time. Convert to
money only when the user supplies a unit price, and label the conversion. Never
emit an estimated dollar figure that was not derived from a stated rate.

### O3 — Degradation is announced

When budget forces a reduction (fewer actors, fewer rounds, merged roles), write a
`DEC` of kind `budget` and state the cost of the reduction in the report's first
section. Silent degradation is worse than no degradation, because the reader
cannot tell which claims are backed by the full method.

---

## When principles collide

| Conflict | Resolution |
|---|---|
| P2 independence vs P7 traceability | Independence governs *generation*. Traceability governs *after freeze*. Actor A never sees Actor B during generation; the Director links them afterwards. |
| P3 testability vs P6 uncertainty | A hypothesis whose only available prediction is weak keeps `strength: weak` and stays in the register. It is not deleted, and it is not upgraded to look decisive. |
| P4 discrimination vs P1 fact verification | Base facts are collected before discrimination ranking. The two are sequenced, not traded off: you cannot rank discriminating investigations against an unverified fact base. |
| P5 opposition vs O2 cost | Red team runs once per round, not once per hypothesis. Scope it to the attack surfaces that matter (see the role file) rather than multiplying reviews. |
| P6 uncertainty vs user pressure for an answer | The user gets a best judgement **plus** the unresolved list. Refusing to answer and answering without uncertainty are both failures. |

---

## What OIR refuses to do

- Answer a factual lookup through simulation. If the question has one right
  answer that a search returns, use a search.
- Simulate when there is only one actor and no strategic interaction. That is
  role-play, and it costs more than it returns.
- Produce a conclusion when the fact base could not be established. "Insufficient
  information" is a valid output.
- Claim improvement over a single-agent baseline without a recorded comparison.
