# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [SemVer](https://semver.org/).

## [Unreleased]

Nothing yet.

## [0.1.2] — 2026-11-13

Second review pass, looking for a different failure family than 0.1.1: not mechanisms
that ran and lied, but **claims that nothing checked at all**. Ten defects, two of them
introduced by the 0.1.1 fixes themselves. Full record: `tests/records/2026-11-13-second-pass.md`.

### Fixed

- **The example run asserted decisions it never recorded.** `decisions/` was empty while
  the round record and plan referred to a scale authorisation and a stop decision, all of
  which `CORE_SPEC` requires as entities. Added `DEC-001` (scale) and `DEC-002` (stop,
  naming the rule that fired and the four that did not).
- **The run stopped with no report.** `CORE_SPEC` §5 says `report.md` is written when the
  run stops; the run stopped by S5 and had none. Written now, with every band `weak` and
  the unresolved table full — the honest output for a run that never collected evidence.
- **Version drift.** README announced v0.1.0 after the packages moved to 0.1.1.
- **A stopped run with no recorded uncertainties.** The report described its open
  questions in prose and noted that no `UNC` entities existed. Workflow 06 requires them,
  and the prose version could not be audited. Three `UNC` records added, each naming what
  would resolve it and which hypothesis it would move.
- **A spec clause with no field behind it.** `CORE_SPEC` §4 required `PRD.basis[]` to
  resolve; `prediction.schema.json` has no such property, so the clause could not fail.
  Now covers premises only, with the reason stated.
- **An enforced hash with no documented algorithm.** The `fact_snapshot` recipe is now in
  `CORE_SPEC` §5 down to sort order and separator, because the validator rejects any other
  convention.
- **"Validated by cross-reference checks" was untrue.** The seven prose-led entities were
  loaded by nothing. The validator now loads `claims/`, `conflicts/`, `assumptions/`,
  `decisions/`, `uncertainties/` and resolves their references.
- **The anchor check did not exist.** T4 claimed broken-anchor detection; `#` targets were
  skipped. Now resolved against each file's headings.
- **Band vocabulary versus practice.** A band must be one of the five, and may carry a
  qualifier (`weak, untested`) because `weak` otherwise conflates thin evidence with no
  evidence.
- **A stale count in prose.** "118 checks" removed from the comparison record; counts in
  prose rot and are not evidence.
- **`requirements.txt` was not registered as required** in `check_structure.py`.

### Verified

All gates re-run from a copy with no `.git` and no prior state: build in sync, skill
check clean, structure 250 checks, good fixture 63 checks, broken fixture failing on all
7 planted defects, example run 154 checks. Negative tests confirmed to fail for the right
reason: broken anchor, dangling `DEC` reference, whitespace-in-path, missing reference
target, tampered fact against a frozen hash.

## [0.1.1] — 2026-11-13

Fixes from an external review that simulated a third-party agent fetching the
published repository, exporting `HEAD` into a clean directory and running every
documented gate from there. Full findings: `tests/records/2026-11-13-external-review.md`.
Four of the nine defects were consequential; three of those were invisible from the
author's own working directory.

### Fixed

- **Corrupted file paths in every generated package.** `core_root` in
  `packaging/platforms.json` held a prose sentence instead of a path token, and it was
  substituted verbatim into four references per package and into a fenced shell
  command, producing instructions like `python the repository root containing core/ …/tests/scripts/validate_state.py`. Now `$OIR_ROOT`; `build.py` refuses a `core_root` containing whitespace and validates every substitution.
- **Validator reported PASS while skipping its schema layer.** With `jsonschema`
  absent it printed one warning and then `result: PASS`, exit 0, after running 37 of 50
  checks. Now exits **3** with `result: INCOMPLETE`. This also makes README §F's claim
  ("it does not claim a pass") true, which it was not.
- **Skill checker could not fail on the reference that broke.** It skipped every
  backticked reference starting with `/` or containing placeholder syntax — i.e. all of
  them. Paths are now resolved through `$OIR_ROOT`; whitespace in a path, an unresolved
  `{{` placeholder, and a missing target are all errors instead of silence or warnings.
- **`fact_snapshot.hash` was unverifiable decoration.** Placeholder strings now replaced
  by real sha256 digests, recomputed and compared by the validator. The check
  immediately caught an unintended post-freeze edit to a fixture during this review.
- **The negative test could pass for the wrong reason.** A missing fixture directory
  also exits 1, so `validate_state.py tests/fixtures/broken` "passed" without testing
  anything. The fixture is now committed as well as generated.
- **Undocumented dependency.** No `requirements.txt` and no install note, which is what
  made the silent-degradation path reachable by any first-time user.
- `tests/schema-validation.md` and `tests/workflow-tests.md` updated: exit-code table,
  fixture generation step, and three new mechanical tests (T9 incomplete-check,
  T10 freeze hash, T11 no-prose-in-paths).

### Known at release

- `.gitignore` is missing from the published repository (no dotfiles on the remote at
  all). File-level fix is local; the push is the owner's to redo.
- No CI. Deliberately not added in this release: a workflow that has never run would be
  another unverified claim.

## [0.1.0] — 2026-11-13

First working version. Phase 1 research plus Phase 2 implementation, in one
release, because the method and its evidence base were developed together.

### Added

- **Core contract.** `core/CORE_SPEC.md` (stages, 15 entity types, ID scheme, state
  layout, seat tiers, budget, degradation ladder, stop rules, uncertainty
  vocabulary) and `core/PRINCIPLES.md` (7 principles + 3 operating rules, each with
  a stated detection method).
- **Six workflows.** Intake and fact base / actor simulation and adjudication /
  hypothesis generation / evidence investigation / adversarial review / iterative
  research, synthesis and stop.
- **Six role definitions**, each with the prompt preamble that must be injected
  verbatim (actor seats, red team) and an explicit prohibition list.
- **Eight JSON Schemas** (Draft 2020-12): research state, fact, source, actor,
  hypothesis, prediction, evidence, investigation.
- **Six Markdown templates** for the human-readable artefacts.
- **Three platform distributions** generated from one template: WorkBuddy,
  Claude Code, portable `.agents/skills`. `packaging/build.py --check` fails on
  drift between template and generated files.
- **Three validation scripts.** `validate_state.py` (schema + cross-reference +
  prediction timing + independence count + isolation), `check_skill.py`
  (frontmatter and naming rules), `check_structure.py` (no empty files, no broken
  links, README index accuracy, platform-independence scan of `core/`).
- **Research record.** `references/METHODS.md` (14 inherited methods with
  modification and rationale, plus 8 explicitly rejected practices),
  `references/PROJECTS.md` (10 projects with licence and read-depth), two dated
  research notes.
- **Test protocol** for a four-mode comparison (A single agent / B actor simulation /
  C + discriminating investigation / D + independent review), and one executed
  A-vs-B record.

### Decisions worth recording

- **Multi-round debate removed.** Three independent 2025 studies find multi-agent
  debate does not beat single-agent baselines at equal compute, and that sycophancy
  drives premature consensus. Cross-examination is capped at one round and blinded.
  See `references/METHODS.md` §3.
- **ACH scoring matrix rejected.** Two experiments with intelligence analysts found
  ACH did not improve accuracy and increased inconsistency; one found ACH *worsened*
  handling of correlated sources. OIR keeps ACH's question and drops its arithmetic.
  See `references/METHODS.md` §2.
- **Source dependency graph made mandatory.** Because the correlated-source error is
  the one a language model commits by default, and the one ACH amplified. Effective
  independent count is computed from root sources, not URL count.
- **Decomposed uncertainty instead of a confidence figure.** Composite percentages
  fuse four incommensurable things and cannot be audited.

### Known gaps

- Four-mode comparison not executed; only A vs B, one case, one round.
- Codex CLI and Cursor compatibility unverified (vendor page 403 / third-party only).
- No non-English source handling beyond `SRC.language`.
- Trigger activation of the packaged skill not verified — needs a fresh session.
