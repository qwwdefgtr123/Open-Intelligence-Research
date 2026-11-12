# Comparison protocol

Four modes, one question, one fact base, blind evaluation. This file is the
protocol. `tests/records/` holds what has actually been run — which, as of
2026-11-13, is one case and two of the four modes.

## The question this protocol answers

Not "does OIR work". The tractable question is narrower and answerable:

> On the same question, the same fact base and a comparable retrieval budget, does
> adding isolated actor seats, discriminating investigation and independent review
> change what a reader can *check* — and at what cost?

## Modes

| Mode | Composition | Seats | What it isolates |
|---|---|---|---|
| **A** | One analyst, one pass: retrieve, analyse, conclude | 0 | The baseline everything else must beat |
| **B** | Fact base → isolated actor seats → adjudication → competing hypotheses + predictions | 3 | The value of viewpoint separation alone |
| **C** | B + discriminating investigation (evidence chosen to separate hypotheses) | 4 | The value of targeted evidence on top of B |
| **D** | C + blind adversarial review + adjudicated findings | 5 | The value of opposition on top of C |

Mode A is not a straw man. It gets the same fact base, the same cutoff, the same
permission to retrieve, and the instruction to do its best work. The published
evidence on multi-agent debate is unflattering enough that a weak baseline would
only produce a flattering, useless result.

## Controls

| Control | Requirement |
|---|---|
| Question | Identical wording |
| Fact base | Identical frozen snapshot, same hash |
| Cutoff | Identical `as_of`; nothing published later enters any mode |
| Retrieval budget | Comparable query count. Record actual counts per mode |
| Output format | Same requested sections, so the evaluator is not reading two genres |
| Blinding | Samples are labelled `S1..S4` in random order; the evaluator does not know which mode produced which |
| Evaluator | Ideally not the person who ran the modes. If it is, say so in the record |

## Evaluation

Twelve criteria. Each gets a **verdict plus evidence**, not a score out of five —
a composite score would be the same fake precision `core/PRINCIPLES.md` P6 forbids
in the analysis itself, and it would be indefensible here.

| # | Criterion | What "better" means |
|---|---|---|
| 1 | Factual accuracy | Claims that survive checking against the fact base; no invented facts |
| 2 | Source quality | Primary over secondary; traceable over aggregated |
| 3 | Source independence | Correct effective-independent count; redundant sources not counted twice |
| 4 | Hypothesis diversity | Distinct mechanisms, not restatements; at least one rival the reader would not have thought of |
| 5 | Prediction testability | Windows, thresholds, counter-indicators; can a reader check it later? |
| 6 | Counter-evidence found | Specific material that weakens the leading explanation |
| 7 | Alternative completeness | Rivals developed to the point of being separable, not merely listed |
| 8 | Traceability | Every substantive claim resolves to a fact, source or entity |
| 9 | Uncertainty expression | Decomposed and honest; no composite percentage presented as calibrated |
| 10 | Cost | Seats, runs, queries, wall time |
| 11 | Time to answer | Wall clock, and how much of it was the reader's |
| 12 | Duplicate analysis | Proportion of output that restates the same point in different words |

## Procedure

1. **S0.** Write the question, scope, cutoff, decision context. Freeze.
2. **S1.** Build the fact base once, with the dependency graph. All modes share it.
3. **Run each mode** in a fresh context. Record `index.json` counters.
4. **Normalise outputs** into the same section structure without editing content.
5. **Blind.** Randomise labels, strip mode identifiers and any tell-tale phrasing
   ("as the third seat argued").
6. **Evaluate** criterion by criterion. Write the evidence, not just the verdict.
7. **Unblind.** Record disagreements between evaluators if there were more than one.
8. **Report**, including what the protocol could not control.

## What this protocol cannot establish

| Limit | Consequence |
|---|---|
| One question, one domain | Nothing generalises. A single case is a demonstration, not a measurement |
| One model family per seat | Correlated errors remain; the results speak to isolation-as-practice, not to model diversity |
| No repeated runs | Sampling variance is unmeasured. A difference smaller than run-to-run noise would be invisible here |
| Evaluator may be the author | Blinding reduces but does not remove this |
| Cost is measured, value is judged | A mode can cost 3× and be judged "slightly better"; the protocol reports both and refuses to collapse them |

## Reporting rule

A record must state, before any comparison: **which modes were run, on what, with
what budget, and what was not run.** A record that omits the modes it skipped reads
as if all four were executed.

## Record template

```
# YYYY-MM-DD — <case name>

## Setup        question, cutoff, fact base hash, budget
## Modes run    which of A/B/C/D, and which were skipped and why
## Outputs      one paragraph per mode, with counters
## Evaluation   twelve criteria, verdict + evidence each
## What moved   the specific claims that differed between modes
## Cost         table
## Limits       what this run cannot support
## Verdict      one paragraph, no stronger than the evidence
```

## Known result so far

See `tests/records/2026-11-13-mode-a-vs-b.md`. Headline, stated carefully: on one
case, Mode A produced a more decisive and more readable answer; Mode B produced
more differentiated causal claims and far better testability instrumentation, but
could not discriminate between its own hypotheses because it has no evidence stage.
C and D exist precisely to test whether that instrumentation converts into
discrimination. **They have not been run.**
