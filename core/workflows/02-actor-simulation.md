# 02 · Actor simulation

Stage **S2** (+ S2b adjudication). Dispatches one isolated seat per actor; the
Director then adjudicates interaction.

Read `roles/actor-simulation.md` for the seat's contract and the exact prompt
preamble.

---

## 1. Purpose

Produce, for each party to the question, a model of what that party can do, what
constrains it, and how it would respond under stated conditions — from inside that
party's position, not from a neutral observer's summary of it.

The output is an **instrument**, not a claim about reality. A model says "if this
actor's structure is as described, it would prefer X and reject Y". It never says
"this actor wants X".

---

## 2. Precondition

- `fact_snapshot` frozen and hashed (workflow 01 gate).
- Actor list approved; each actor justified by a `FACT` ID.
- Scale authorised. Standard tier = 3 actor seats.

If any of these is missing, do not dispatch.

---

## 3. Dispatch

One execution unit per actor. Each receives **exactly three inputs**:

1. The frozen fact snapshot (all `FACT` and `CLM` records, no analysis).
2. Its own actor brief: identity, the question, and the structural prompts.
3. The output schema (`actor.schema.json`) and the required prose sections.

Each receives **none** of:

- Other actors' outputs or names of other seats
- The Director's hypothesis or preferred reading
- The previous round's conclusions
- Any hint about the expected answer

Record `simulation_input_hash` (hash of inputs 1 and 2) in `index.json`. Two actors
with the same hash means the isolation failed — the validator fails the run.

### Anti-anticipation preamble (inject verbatim)

```
You are modelling ONE actor in a multi-party situation. Rules:

1. Reason only from this actor's position, interests and constraints. Do not adopt
   a neutral, balanced, observer voice.
2. Do not anticipate, imagine, or accommodate what other parties will say or want.
   You cannot see them; do not guess at a consensus.
3. Do not soften your reading to make it acceptable. If your model says this actor
   would act in a way that seems unreasonable to an outsider, say so and explain
   the internal logic.
4. Public statements by this actor are evidence of what it chose to say. They are
   not evidence of what it wants. Note the gap where you see one.
5. Everything you assert about the world must trace to a FACT or CLM id. If you
   need something that is not there, list it under "premises I need but do not
   have" instead of inventing it.
6. End with: "The judgement I would defend even if every other seat disagreed:"
   followed by one sentence.
```

---

## 4. What each seat must answer

Written into `simulations/SIM-<ACT>-r<N>.md` as prose, and into `actors/ACT-*.json`
as structure. The seven questions:

1. **Core goal and greatest fear.** What is this actor trying to obtain, and what
   is it most afraid of losing? Both are required; an actor defined only by
   ambition is a caricature.
2. **Internal structure.** Which factions, departments, or constituencies exist
   inside this actor? Rough weights. Who can veto? An actor with no internal
   tension is almost always a modelling error.
3. **Resources and constraints.** What can it actually deploy? What legally,
   politically, financially or physically prevents it from doing what it wants?
4. **Feasible actions, and the ones it rules out.** List options. For each rejected
   option, state why — the rejected set is often more diagnostic than the chosen
   one.
5. **Reaction function — conditional, not dispositional.** "If X does A, this actor
   does B; if X does C, it does D." A single sentence like "will respond firmly"
   is not a reaction function and is rejected at review.
6. **Beliefs about others, at declared order.** 0th: facts about the situation.
   1st: what I think party X will do. 2nd: what I think party X thinks I will do.
   Stop at 2. Deeper nesting is unverifiable and models produce rhetoric rather
   than reasoning there.
7. **Falsifiers.** What observable developments would show this model is wrong?
   At least two, specific enough that a reader could check them.

---

## 5. Adjudication (S2b) — Director only

Simulation produces *intentions*. Adjudication produces *what actually happens*,
because intentions collide.

### Procedure

1. Collect every actor's feasible action set.
2. Intersect: which combinations are mutually compatible? Where two actors would
   both act in ways that cannot coexist, record a `CFL`.
3. Apply the constraints from the fact base: legal, physical, budgetary. An action
   that the facts make impossible does not occur, however much the actor wants it.
4. Produce the interaction outcome as a set of "who does what, under which
   constraint", with the `FACT` IDs that make each feasible or infeasible.

### Two prohibitions

- **Never accept an actor's own claim of success.** An actor seat that reports "my
  party prevails" is producing narrative, not analysis. Only the adjudication step
  decides outcomes.
- **Never let adjudication invent facts.** If the outcome depends on something not
  in the snapshot, it is a `UNC` or a new investigation task — not an assumption.

Adjudication output goes to `conflicts/CFL-*.json` and a short
`simulations/adjudication-r<N>.md`.

---

## 6. Diversity check (mandatory, cheap)

Before S3, compute a crude overlap diagnostic across actor outputs: shared
sentences, shared distinctive phrases, and identical option lists.

- If two actor models are near-identical in their **interests and constraints**
  (not their prose), the decomposition failed: the two "actors" are one interest
  structure wearing two labels. Merge them, or re-derive the split.
- If actor models share prose but differ structurally, that is acceptable — style
  converges, positions should not.

Report the diagnostic as a number with its method named. Do not report it as a
score of quality; it measures redundancy, not correctness.

---

## 7. Outputs

| File | Content |
|---|---|
| `actors/ACT-001.json` | Structured model per `actor.schema.json` |
| `simulations/SIM-ACT-001-r1.md` | The seat's prose, all seven sections present |
| `simulations/adjudication-r1.md` | Director's interaction outcome, with fact citations |
| `conflicts/CFL-*.json` | Incompatible action pairs and their resolution |

---

## 8. Gate to S3

- [ ] One execution unit per actor; distinct `simulation_input_hash` per seat
- [ ] All seven questions answered; reaction function is conditional
- [ ] At least two falsifiers per actor, each checkable
- [ ] Every `premises` reference resolves to a `FACT` or `CLM`
- [ ] Adjudication cites facts, not actor narration
- [ ] Diversity diagnostic computed and reported

---

## 9. Failure modes

| Symptom | What went wrong | Fix |
|---|---|---|
| Actors all recommend the reasonable middle course | Anti-anticipation clause missing or actors not isolated | Re-run isolated with the preamble verbatim |
| Actor model reads like a Wikipedia summary of the country | No internal structure; unitary-actor fallacy | Force factions and veto holders |
| Reaction function is one adjective | Seat answered a disposition, not a function | Re-ask with the conditional template |
| Every actor's plan succeeds in adjudication | Adjudication absent or deferring to narration | Adjudicate against constraints; record `CFL`s |
| All actors cite the same three sources | Fact base too thin | Return to workflow 01; the snapshot is starving the simulation |
| Actor model contains a "fact" not in the snapshot | Invented premise | Delete it; add to "premises I need" and open an `INV` |
