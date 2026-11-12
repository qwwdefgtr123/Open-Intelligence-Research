# 01 · Research intake and fact base

Stages **S0** and **S1**. Executed by the Research Director. No seats are
dispatched in this file. Everything downstream depends on the fact snapshot
produced here, so a shortcut taken now becomes a false premise in every actor
model later.

Read `roles/research-director.md` before running this.

---

## Part A — Intake (S0)

### A1. Classify the request

Answer three questions before anything else.

**Is the request answerable by retrieval?** If there is a single correct answer
that a search returns (a date, a name, a figure, a quote), say so and answer it
directly. Write `DEC` kind `refuse-oir` with the reason. Simulation on a factual
lookup produces a confident wrong answer wrapped in methodology.

**Is there strategic interaction?** OIR earns its cost when at least two parties
with different interests act on each other. One party with no counterparty is a
role-play, and a plain analysis does it better and cheaper. If the answer is no,
decline and explain.

**What decision does this inform?** Write it into `RES.decision_context`. An open
question with no consumer produces a report nobody can use and no criterion for
stopping. If the user cannot name one, propose one and ask.

### A2. Bound the scope

| Field | Content |
|---|---|
| `question` | The question, restated in one sentence with the ambiguity removed |
| `scope_in` | What is inside: time range, geography, actors of interest |
| `scope_out` | What is explicitly excluded, and why |
| `as_of` | Information cutoff. Everything after this is invisible to the analysis |
| `decision_context` | Who uses the answer, for what |

The cutoff matters: without it, the run silently absorbs later information and
every prediction looks prescient.

### A3. Draft the candidate actor list — from facts, not imagination

Do a first retrieval pass (10–20 queries) before naming actors. Then list
candidates and, for each, the evidence that it is a party to the question.

Naming actors from priors is how a simulation ends up modelling a textbook instead
of the situation. If a candidate actor has no `FACT` justifying its inclusion, it
does not enter.

### A4. Choose scale and budget

Use `CORE_SPEC.md` §6. State the tier, the seat count, the planned runs, queries
and rounds, and the stop rules that will apply. This is an **authorisation
point**: the user approves scale and budget before seats are dispatched. Do not
increase either later without a new authorisation.

### A5. Write the plan

`plan.md` must contain: question, scope, cutoff, decision context, actor
candidates with justification, tier, seat allocation, budget plan, what would
make the run stop early, and what output format the user wants.

---

## Part B — Fact base (S1)

### B1. Retrieve by tier, not by convenience

Source tiers, evaluated differently — never pooled into one "credibility" score:

| Tier | Examples | Standard applied |
|---|---|---|
| `primary` | Treaties, statutes, filings, court records, datasets, transcripts, product documentation | Does it say what is claimed? Is the version current? |
| `official` | Government statements, press releases, corporate announcements | Accurate as a record of *what was said*. Not evidence of intent |
| `media` | Reported coverage | Trace to what it cites. If it cites nothing, it is `single-source` at best |
| `ngo` / `research` | Reports, academic work | Check method and funder interest |
| `social` / `anonymous` | Posts, unattributed leaks | Corroboration required before any load-bearing use |

A statement by an actor is a `CLM`, not a `FACT`. "Ministry X said Y on date Z" is
a fact about the statement. "Ministry X wants Y" is an inference and belongs in an
actor model, cited to the claim.

### B2. Record triple structure

For every retrieved item:

1. `SRC-*` — where it came from, when published, when retrieved, tier, and
   **`derived_from`**.
2. `CLM-*` — if it contains a statement by a party: who, where, when, verbatim or
   close paraphrase, type (`statement` / `denial` / `leak` / `analysis`).
3. `FACT-*` — if it establishes something about the world: the statement,
   `as_of`, sources, `verification_level`.

`verification_level`:

| Level | Meaning |
|---|---|
| `confirmed` | Primary document or direct observation, current version |
| `corroborated` | Two or more **independent** sources (see B3) |
| `single-source` | One origin only, or several that all derive from one |

### B3. Collapse the dependency graph before counting

For every source, ask: does this derive from another source already in the
ledger? Wire service copy, syndicated columns, translations, and "according to
Reuters" reports all derive from one origin.

`SRC.derived_from: ["SRC-004"]` — and the derived source contributes **zero**
additional independence.

Effective independent count for a set of sources = number of distinct root
sources. Record it in `EVD.independence_note` and, at fact level, in
`FACT.verification_level`.

This is the single most load-bearing accounting rule in OIR. It is also the exact
error that structured analytic techniques have been shown to *worsen*: when
redundant sources are made salient, ACH-trained analysts double-counted them more
often, not less (`references/METHODS.md` §2). Do not rely on noticing redundancy —
compute it.

### B4. Freeze

Write `index.json`:

```json
{
  "research": { "id": "RES-001", "question": "...", "as_of": "2026-11-01", "scale": "standard" },
  "fact_snapshot": { "ids": ["FACT-001", "..."], "hash": "<sha256 of sorted ids+statements>" },
  "counters": { "runs": 0, "queries": 37, "rounds": 0 }
}
```

The hash exists so a later round can prove the actors all read the same base. If
the snapshot is amended after freeze, bump it to `fact_snapshot_v2`, write
`DEC` kind `fact-revision`, and note which actor models are now stale.

---

## Gate: what must be true before S2

- [ ] Question typed; scope and cutoff fixed
- [ ] `decision_context` non-empty
- [ ] Actor candidates each justified by a `FACT` ID
- [ ] Scale and budget authorised by the user, recorded in `DEC`
- [ ] Every load-bearing fact has ≥1 `SRC`; `single-source` items marked
- [ ] Dependency graph built; no source counted twice as independent
- [ ] `fact_snapshot` frozen with hash
- [ ] Anything the run cannot establish is already listed in `plan.md` as a known gap

If the gate fails on "load-bearing fact has no source", stop and report the gap.
Simulating on an empty base produces elegant fiction.

---

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Actors named before any retrieval | Priors substituted for evidence | Delete the actor list, retrieve first |
| Every fact is `corroborated` | Dependency graph not built | Rebuild `derived_from`; expect levels to drop |
| Facts and inferences in the same sentence | No entity separation | Split: the observation is `FACT`, the reading is `ASM` or `ACT` |
| No cutoff date | Absorbing post-hoc information | Fix `as_of`, re-retrieve anything after it |
| Scope covers "everything about X" | No decision context | Ask what decision this serves, narrow to it |
