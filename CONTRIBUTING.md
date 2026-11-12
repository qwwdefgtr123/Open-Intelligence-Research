# Contributing

OIR is a method before it is a program. A change to `core/` changes what every
downstream run believes is correct, so the bar is higher than "it reads better".

## Before you change anything

Read `core/PRINCIPLES.md` and `core/CORE_SPEC.md`. If your change contradicts either,
you are proposing a change to the method, not a fix — say so explicitly in the pull
request and expect the discussion to be about evidence, not preference.

## What kinds of change are welcome

| Kind | Welcome | Needs |
|---|---|---|
| A documented failure of the method, with a run that shows it | Yes, highest value | The state directory or an excerpt, and what should have happened |
| A new discriminating investigation pattern | Yes | Which hypothesis pairs it separates and why the existing ranking misses it |
| A platform distribution | Yes | A row in `packaging/platforms.json` with a verification sentence, and an honest `verified` status |
| A schema field | Yes, if it blocks a real judgement | Show the judgement that cannot be recorded today |
| A new workflow stage | Rarely | Justify why an existing stage cannot absorb it; stages are expensive |
| More agents | No, not as a goal | Seat count is a cost, not a feature. Propose what the extra seat can do that no existing seat can |
| Prose polish in `core/` | Yes | Keep the imperative voice; do not soften a prohibition into a preference |

## The consistency rule

A change that touches the stage list, the entity list, the seat map or the
assessment vocabulary must update all of:

```
core/CORE_SPEC.md
the affected workflow(s)
the affected role file(s)
core/templates/*
README.md (index and reading guide)
tests/workflow-tests.md
```

A pull request that changes one of these and not the others will be asked to. This
is the single most common defect in method repositories: the spec moves and the
templates keep describing the old one.

## Checks to run before opening a pull request

```bash
python packaging/build.py --check
python tests/scripts/check_skill.py distributions/
python tests/scripts/check_structure.py
```

All three must pass. `build.py --check` catches the case where you edited a
generated `SKILL.md` instead of the template.

If you added or changed a schema, add a fixture under `tests/fixtures/` and confirm
`validate_state.py` rejects the malformed variant you care about. A schema nobody
has seen reject anything is untested.

## Style

- **Imperative, specific, and checkable.** "Never count syndicated copy as
  independent" beats "be careful about source independence".
- **State the mechanism, not just the rule.** A rule without a reason gets deleted
  by the next contributor who finds it inconvenient.
- **Name the failure mode.** Each prohibition should make clear what goes wrong if
  it is ignored.
- **No unmarked speculation.** If something is inferred rather than established, say
  which. This applies to the documentation as much as to the analysis.
- **English in `core/`.** Platform-neutral and readable by the widest set of
  contributors. README carries a Chinese summary.

## Attribution

If you add a method, record it in `references/METHODS.md` with: origin, what problem
it solved, what was inherited, what was changed, why, and the licence. Borrowed
ideas must be labelled as borrowed. Code reuse requires the original licence to be
compatible and its notice preserved; if the licence is unclear, do not copy.

## Reporting a bad run

The most useful issue is a run that followed the method and still produced a bad
result. Include: the question, the tier, the state directory (redacted as needed),
which stage failed, and what a competent analyst would have produced instead. That
is worth more than any number of feature requests.
