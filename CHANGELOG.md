# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [SemVer](https://semver.org/).

## [Unreleased]

Nothing yet.

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
