# Workflow tests

Two kinds of test. **Mechanical** tests can be run by a script and are marked with a
command. **Behavioural** tests need an agent to run a real case and are marked with
the observable they produce.

Nothing here is marked as passing unless it was actually run. See
`tests/records/` for executed results.

## 1. Mechanical

| # | Test | Command | Assertion |
|---|---|---|---|
| T1 | No empty files | `python tests/scripts/check_structure.py` | Exit 0. The repository must not contain structural filler |
| T2 | Every `core/` file is platform-independent | same | Exit 0. No product, tool or API names under `core/` |
| T3 | README index matches the filesystem | same | Exit 0. Every path in the README tables and tree block exists; every required file is present |
| T4 | No broken relative links | same | Exit 0. Across all Markdown, including README anchors |
| T5 | Skill frontmatter is valid | `python tests/scripts/check_skill.py distributions/` | Exit 0. `name` matches directory, `description` ≤1024 chars, has a "use when" clause |
| T6 | Generated distributions match the template | `python packaging/build.py --check` | Exit 0. No drift |
| T7 | Schemas are valid JSON Schema | `python tests/scripts/validate_state.py tests/fixtures/good` | Exit **0**, and `validate_state` reports the schema layer ran |
| T8 | Validator rejects a broken state | `python tests/scripts/validate_state.py tests/fixtures/broken` | Exit **1**, and the failure list names each planted defect |
| T9 | A check that cannot run does not pass | `validate_state.py` with `jsonschema` absent | Exit **3** and `result: INCOMPLETE` — never `0` / `PASS` |
| T10 | The freeze hash is real | edit one `FACT` statement, keep the hash | Exit 1, `fact_snapshot.hash does not match` |
| T11 | No path in a package can be prose | `python packaging/build.py` | Exit 0; a `core_root` value containing a space is refused. `check_skill.py` fails on any backticked path containing whitespace, and on an unresolved `{{` placeholder |

T8 and T9 are the ones that matter most. A validator that has never rejected anything
is untested; a validator that reports success after skipping its own checks is worse
than no validator, because it manufactures confidence. Both were found broken during
the 2026-11-13 review — see `tests/records/2026-11-13-external-review.md`.

T11 exists because a prose sentence was once substituted into `core_root`, corrupting
every file path and one shell command in all three packages while `check_skill.py`
reported `PASS (0 warnings)`. The checker skipped any reference it could not resolve,
which was all of them.

## 2. Behavioural — stage gates

Each gate is checked by an agent, on a real run, against the state directory.

### S0–S1 intake and fact base

- [ ] A factual lookup is refused, with `DEC` kind `refuse-oir` written
- [ ] A single-actor question is declined, or the absence of a counterparty is named
- [ ] `plan.md` has a non-empty `decision_context`
- [ ] Scale and budget were put to the user and the answer recorded, before any seat
- [ ] Every load-bearing fact has a source; `single-source` items are marked
- [ ] The dependency graph collapses at least one syndicated group — if it collapses
      nothing, either the base is unusually clean or the graph was not built
- [ ] `fact_snapshot.hash` is present and equals the recomputed value

### S2 actor simulation

- [ ] One execution unit per actor, recorded in `index.json`
- [ ] All `simulation_input_hash` values distinct (`validate_state.py
      --check-isolation`)
- [ ] Each actor's prose contains the anti-anticipation preamble's effects: no
      reference to another actor's view, no "balanced" voice
- [ ] Every actor has a **conditional** reaction function (≥2 if/then rows)
- [ ] Every actor has ≥2 falsifiers
- [ ] Every actor has at least one faction, or a written `unity_note` justifying none
- [ ] Adjudication cites `FACT` ids and does not accept any actor's own claim of success
- [ ] Diversity diagnostic computed; near-identical interest structures merged or explained

### S3 hypotheses

- [ ] ≥3 live hypotheses, or a written justification
- [ ] Each has a mechanism with a named weakest link
- [ ] Each prediction has all seven fields including `counter_indicator`
- [ ] `prediction_set.registered_at` is earlier than every linked `INV.started_at`
- [ ] At least one hypothesis denies a presupposition of the original question
- [ ] `relation_to_others` filled; no manufactured mutual exclusivity

### S4 investigation

- [ ] Every `INV` has non-empty `separates`
- [ ] `expected_if` was written before retrieval (check the `started_at` ordering)
- [ ] Every `INV` closed, with `null_result` set explicitly
- [ ] Every `EVD` has ≥1 `alternative_readings`
- [ ] Recount: for every `EVD`, `effective_independent` ≤ number of distinct roots
- [ ] No two `EVD` claim independence from the same root
- [ ] Every touched `PRD` has a judgement against its thresholds

### S5 adversarial review

- [ ] Red-team input is de-identified; `deid_map` exists in `index.json`
- [ ] All six surfaces (A1–A6) answered, including "no finding, because…"
- [ ] Every finding has `target`, `anchor`, `severity`, `what_would_change_my_mind`
- [ ] Every finding has a verdict with rationale
- [ ] Anti-theatre test answered: did any finding change a band, a judgement or a model?
- [ ] Hypotheses that survived record *which* surfaces they survived

### S6 synthesis and stop

- [ ] Every live hypothesis has four columns and one band
- [ ] Every band has a "what would move it up" sentence
- [ ] Every `disconfirmed` prediction has a model-revision verdict (hypothesis / model / both / weak evidence)
- [ ] Any revised `ACT` has a bumped `version` and a `change_log` entry
- [ ] Dissent preserved where a seat disagreed
- [ ] Stop decision records the rule that fired **and** the rules that did not
- [ ] Method record counters equal `index.json` exactly

## 3. Behavioural — what success looks like

A run that passes every gate can still be a bad run. Three qualitative checks:

| Check | Passes if |
|---|---|
| **Did the answer move?** | At least one hypothesis changed status between round 1 and stop. A run where nothing moved either had a trivial question or was decorative |
| **Did the review bite?** | At least one red-team finding was accepted and produced a change. Zero for two consecutive rounds means the review is not functioning |
| **Did the report lose confidence?** | The final band is not uniformly higher than the mid-run bands. Monotonic rising confidence across rounds is the signature of a report writing itself |

## 4. Known untested

| Area | Why | Consequence |
|---|---|---|
| Four-mode comparison (A/B/C/D) | Cost. Only A vs B was executed for one case | No claim of quality improvement is made anywhere in this repository |
| Trigger activation in a fresh session | Requires a new session | Compatibility marked accordingly |
| Non-English sources | Only `SRC.language` exists | Analysis on non-English material is unvalidated |
| Long runs (4+ rounds) | Not attempted | Diminishing returns and drift unknown |
