# Schema validation

Eight schemas in `core/schemas/`, Draft 2020-12. This file records what each
enforces, why the strictness sits where it does, and how to prove the rules fire.

## 1. What each schema enforces

| Schema | The one thing it exists to prevent |
|---|---|
| `research-state.schema.json` | A run without a cutoff date, a decision context, or current counters — i.e. a run that cannot be audited or stopped |
| `fact.schema.json` | `corroborated` claimed on the strength of one root source; a statement-of-record mistaken for evidence of intent |
| `source.schema.json` | Syndicated copy counted as independent (via required `derived_from` + `independence_class`) |
| `actor.schema.json` | A unitary actor with no factions and no falsifiers; a "reaction function" that is one adjective; invented premises |
| `hypothesis.schema.json` | A conclusion with no mechanism; a hypothesis admitted to synthesis without a prediction; a composite confidence number |
| `prediction.schema.json` | A prediction with no window, no threshold, or no `counter_indicator` — i.e. one that cannot fail |
| `evidence.schema.json` | A single-reading record; an independence count that exceeds the number of roots |
| `investigation.schema.json` | A topic search posing as an investigation (`separates` required non-empty); a lost null result |

## 2. Deliberate design choices

**`additionalProperties: true` everywhere.** Agents will add fields. Closing the
schema turns a useful extra field into a hard failure and encourages deleting data
to pass validation. The required set is what matters; extras are tolerated.

**Enums over free text for the fields that get compared.** `status`, `judgement`,
`direction`, `strength`, `tier`, `independence_class`. These are aggregated across
entities; free text makes aggregation impossible and lets "mostly confirmed" become
a category.

**`counter_indicator` is required, not optional.** It is the field that converts a
directional guess into a discriminating test. Making it optional guarantees it is
skipped.

**No `confidence` field exists on `hypothesis`.** Not optional — absent. The four
assessment columns live in the iteration record and the report, so that a number
cannot be smuggled into the entity and then quoted as if it were calibrated.

**`mechanism` has `minLength: 60`.** A crude proxy for "is this a chain or a
gesture". It only catches the most obvious case; the workflow does the real work.

## 3. Cross-entity rules the schemas cannot express

JSON Schema validates one document at a time. These need the script:

| Rule | Implemented in |
|---|---|
| Every ID reference resolves to an existing entity | `check_references` |
| A prediction was registered before the investigation that tested it | `check_prediction_timing` |
| `derived_from` has no cycles | `root_of` |
| `effective_independent` ≤ number of distinct roots | `check_independence` |
| Two actors did not share an execution unit or input hash | `check_isolation` |
| A hypothesis with no predictions is not above `draft` | `check_hypothesis_rules` |

## 4. How to run

```bash
python tests/scripts/validate_state.py tests/fixtures/good
python tests/scripts/validate_state.py tests/fixtures/broken          # must exit 1
python tests/scripts/validate_state.py research/<slug> --check-isolation
```

Requires `jsonschema`. Without it the script degrades to structural and
cross-reference checks only, and says so — it does not silently claim a pass:

```
~ jsonschema not installed - schema validation skipped (structural checks still run)
```

## 5. Fixtures

`tests/fixtures/good` — a minimal but complete two-actor, two-hypothesis run. Small
enough to read in one screen, complete enough to exercise every cross-reference rule.

`tests/fixtures/broken` — the same run with one defect planted per rule:

| Fixture defect | Rule it must trigger |
|---|---|
| `FACT-001` references a missing `SRC-099` | dangling reference |
| `HYP-002` has `predictions: []` but `status: live` | no prediction, no hypothesis |
| `PRD-001.judged_at` before `registered_at`, `late` unset | prediction timing |
| `EVD-001` claims 3 independent from 1 root | independence overcount |
| `SRC-003.derived_from` contains a cycle | dependency cycle |
| `HYP-003` carries `confidence: 0.7` | forbidden composite figure |
| both actors share `simulation_input_hash` | isolation failure |

The point of T8 is that the validator's output names each of these. A validator
passing the `good` fixture proves nothing; a validator passing the `broken` one is
broken.

## 6. Versioning

`schema_version` is `"1.0"` and appears in `research/.../index.json`. A change that
makes an existing valid state invalid requires a minor-version bump and a migration
note in `CHANGELOG.md`. Adding an optional field does not.
