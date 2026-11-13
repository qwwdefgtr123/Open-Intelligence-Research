# 2026-11-13 — External review of `qwwdefgtr123/Open-Intelligence-Research`

Simulated a third-party agent: fetched the remote repository metadata, compared the
published file set with the local tree, exported `HEAD` into a clean directory, and
ran every documented gate **from inside that export** rather than from the working
directory. The point of the exercise was to stop trusting "the checks pass on my
machine".

**Nine defects found, four of them consequential. All are fixed in this commit.**

## What was checked

| Check | Method |
|---|---|
| Does the repo exist and is it public | GitHub API, `2026-11-13` |
| Is the published file set the intended one | remote tree vs `git ls-files`, set comparison |
| Do the gates pass from a clean export | all five commands, run from `git archive HEAD` |
| Do the negative tests actually fail | planted-defect fixture, exit codes captured without a pipe |
| Is the validator honest when it cannot run | forced `ImportError` on `jsonschema` |
| Do README links and anchors resolve | relative-link resolution + slug comparison against headings |
| Are the packaged skills coherent | read the generated `SKILL.md` as a consumer would |

## Findings

### S1 — Severe: prose substituted into file paths in every package

`packaging/platforms.json` defined `core_root` as a **sentence** ("the repository root
containing core/ - resolve it from…") instead of a path token. `build.py` substituted
it verbatim, so all three generated `SKILL.md` files contained:

```
| `the repository root containing core/ - resolve it from the skill's own location,
  or from the installed copy if the repository was cloned alongside/core/PRINCIPLES.md` |
```

and, worse, a fenced command that cannot be executed:

```
python the repository root containing core/ - resolve it from ... /tests/scripts/validate_state.py research/<slug> --check-isolation
```

Four corrupted references per package × 3 packages, plus the copy installed at
`~/.workbuddy/skills/oir/`. An agent following that instruction would fail, or guess.

**Cause:** a placeholder used both as a path fragment and as a human explanation.
**Fix:** `core_root` is now `$OIR_ROOT`; the explanation lives in `skill.template.md`,
where it is platform-neutral. `build.py` refuses any `core_root` containing whitespace
or longer than 24 characters, and validates that every `$OIR_ROOT` occurrence is
followed by a clean path tail — including inside fenced code blocks, which an
inline-backtick checker cannot see.

### S2 — Severe: the validator reported PASS while skipping its own schema layer

With `jsonschema` absent, `validate_state.py` printed one warning and then
`result: PASS`, exit 0 — after silently running 37 checks instead of 50. Thirteen
schema validations never executed and the exit code said the state was valid.

This is the worst class of defect in a repository whose selling point is mechanical
checks: it manufactures confidence. It also made README §F false, since that section
claimed the validator "does not claim a pass".

**Fix:** exit code 3 and `result: INCOMPLETE` when the schema layer cannot run. No
`PASS` is printed. README and `tests/schema-validation.md` document the three codes.

### S3 — Moderate: the skill checker was blind to exactly what broke

`check_skill.py` skipped any backticked reference starting with `/` or containing
placeholder syntax — which was every `core/` reference in every skill. So it reported
`PASS (0 warnings)` on the package corrupted by S1. The check existed, ran, and could
not fail.

**Fix:** references are resolved after stripping `$OIR_ROOT/`; a path containing
whitespace is now an **error** (that is what prose-in-a-path looks like); an
unresolved `{{` placeholder is an error; a missing target file is now an error rather
than a warning.

### S4 — Moderate: the freeze hash was decorative

`fact_snapshot.hash` held `"casehash-intel-magdeburg-v1"` and
`"fixturehash0000…"` — strings that satisfied `minLength: 16` and were never
verified. A freeze that cannot be recomputed is not a freeze.

**Fix:** both are now real sha256 digests over the sorted frozen facts, and the
validator recomputes and compares. This has already paid for itself: the check fired
during this review on an unintended edit to a fixture fact, which is precisely the
event it exists to catch.

### S5 — Moderate: the published repository differs from the documented policy

Remote file set: 111 blobs. Local tracked: 99. The difference is both directions:

- `.gitignore` is **absent from the remote** (no dotfiles at all). Anyone cloning gets
  no ignore rules — `__pycache__`, `.venv` and `research/` outputs become commit noise.
- `tests/fixtures/broken/` **is on the remote**, though the repository's `.gitignore`
  said it was generated, not committed.

**Fix (local):** the broken fixture is now deliberately committed, so the negative test
runs from a fresh clone with no generation step, and `.gitignore` says so explicitly.
`.gitignore` itself is still missing remotely — that is a push-side problem, not a
file problem, and requires the owner to re-upload or push it.

### S6 — Minor: a documented behaviour that did not exist

README §F asserted the validator "degrades … and says so; it does not claim a pass".
It was untrue until S2 was fixed. Documentation that describes an aspiration as a
behaviour is the same failure the method forbids in analysis.

### S7 — Minor: the negative test could pass for the wrong reason

`tests/schema-validation.md` said to run the broken fixture without saying to generate
it first. The directory is missing on a fresh checkout that honours `.gitignore`, and a
missing directory also exits 1 — so the "must exit 1" test would pass while testing
nothing. Fixed by committing the fixture, documenting the generation step, and
distinguishing the exit codes.

### S8 — Minor: the dependency was neither declared nor installed

No `requirements.txt`, and no mention of `jsonschema` in the install instructions. That
omission is what made S2 reachable by any first-time user.

**Fix:** `requirements.txt`, referenced from README §D, §F and §G.

### S9 — Observation: no CI

Every mechanical check has only ever run on the author's machine. For a repository
whose argument is "these rules are enforced, not advised", that is a credibility gap.
Not fixed here: adding a workflow that has never executed would itself be an unverified
claim. Recommended next, with the first run observed before it is described as passing.

## What came back clean

- Every tracked file except `.gitignore` is on the remote, and nothing extra beyond the
  fixture divergence in S5.
- All relative links and all six README anchors resolve.
- `build.py --check` in a clean export: in sync.
- `check_structure.py` in a clean export: 222 checks, pass (243 in the working tree,
  which includes the committed fixture).
- `validate_state.py` on the example run: 119 checks, pass, including schema layer.
- The 7 planted defects are all still caught after every change above.
- Licence, version and description are consistent across `LICENSE`, frontmatter and
  `packaging/platforms.json`.

## Why these were missed the first time

The original verification ran from the working directory, where `core/` is adjacent to
`distributions/`, so a relative reference resolved by accident of layout. The corrupted
path was in a **fenced code block**, which the reference checker never inspected. And
the false pass required a machine without `jsonschema` — the author's machine had it
installed, so the degradation path was never executed.

The general lesson, and the reason this record exists: **run the checks as a stranger,
in a copy, without your own environment.** Three of the four severe findings were
invisible from inside the author's setup. This is the same argument the method makes
about isolated actor seats, applied to testing — and the author failed to apply it to
their own work until forced.
