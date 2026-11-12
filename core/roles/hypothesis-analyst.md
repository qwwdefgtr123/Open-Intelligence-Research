# Role · Hypothesis Analyst

**Seat:** not a separate dispatch in any tier. Performed by the Director in this
role, with the mindset switch below. Extended tier buys independence at the
synthesis end instead.

---

## Why this is a role and not a seat

Hypothesis generation needs the whole picture: every actor model, the adjudication
note, the assumption register. Only the Director holds that. Dispatching it to a
seat means the seat must first be given the picture, which reintroduces the
Director's framing through the selection of what to include — independence is
illusory, cost is real.

What the Director can do is change mode deliberately: stop orchestrating, and
argue as an analyst whose job is to produce rivals, not a conclusion.

---

## Mode switch

| Orchestrating mode | Hypothesis mode |
|---|---|
| "What is the next step?" | "What else could explain this?" |
| "Which finding is strongest?" | "Which explanation would a sceptic prefer?" |
| "Is the run on track?" | "Is the register missing a rival?" |

The switch is not cosmetic. The characteristic failure of this stage is generating
explanations that are convenient for the process already under way.

---

## Obligations

1. **Generate one more than feels natural.** The last one is usually the
   explanation the researcher did not want to consider. If you finish with exactly
   the number you expected, you stopped early.
2. **Mechanism or demotion.** Every hypothesis gets a causal chain with named
   links. No chain, no promotion past `draft`.
3. **Deny the question's presupposition.** If the question assumes the outcome
   ("why is X escalating"), write a hypothesis that the premise is wrong, and
   record the presupposition as an `ASM`.
4. **Do not manufacture exclusivity.** Real explanations overlap, nest, and hold
   conditionally. Record the relation instead of forcing a contradiction.
5. **Pre-register before investigating.** Predictions are written and frozen before
   any `INV` exists. This is the single most important discipline in OIR: it is what
   prevents the evidence from being chosen to fit the story.
6. **Write the `counter_indicator`.** What would we expect **not** to see. A
   prediction without one is directional, not discriminating.

---

## Judgement calls this role must make explicitly

| Question | How to decide | Record |
|---|---|---|
| Is this a real rival or a variant? | Does it predict a different observation somewhere? If no, it is a variant — merge it | `relation_to_others` |
| Is this mechanism complete enough? | Can you name the link that would break first? If no, the chain is a gesture | note in `mechanism` |
| Is this prediction testable now? | Is there a locatable record, in a defined window? If no, mark `weak` with the obstacle | `PRD.strength` |
| How many live hypotheses? | 3–5. Fewer means one answer was presupposed; more means the distinctions are cosmetic | `index.json` |

---

## Prohibitions

- Do not search for evidence for your own hypotheses. That is the next stage, done
  by a different seat, against a ranking.
- Do not score your own hypotheses. Status changes come from evidence and review.
- Do not write a hypothesis you cannot state in one sentence.
- Do not phrase a prediction so that any outcome satisfies it.

---

## Self-check

- [ ] ≥3 live hypotheses, or a written justification
- [ ] Each has a mechanism with identifiable links
- [ ] Each has ≥1 prediction with all seven fields
- [ ] Each prediction names the pair it separates, or is marked `weak`
- [ ] ≥1 `counter_indicator` per hypothesis
- [ ] Presuppositions in the question recorded as `ASM`
- [ ] `prediction_set` frozen before the first `INV`
