# Platform compatibility

Verification date for every row: **2026-11-13**. A row is only marked compatible on
the basis stated in its evidence column. "Reads `SKILL.md`" is a format fact;
"can isolate seats" is a capability fact. They are recorded separately because they
fail separately.

Status vocabulary: `full` · `partial` · `needs-adaptation` · `unsupported` ·
`unverified`.

## 1. Capability matrix

| Platform | Native skill support | Multi-agent / isolation | Tool calls | State management | Status | Degradation if not available |
|---|---|---|---|---|---|---|
| **WorkBuddy** | Yes — `SKILL.md` with YAML frontmatter, directory under `~/.workbuddy/skills/` or `<workspace>/.workbuddy/skills/` | Yes — dedicated subagent dispatch, one fresh context per call | Yes — filesystem, web retrieval, shell | File-based (`research/<slug>/`); no platform state store needed | **full** (installed, dispatch exercised; trigger *not* verified, see §2) | — |
| **Claude Code** | Yes — `~/.claude/skills/<name>/SKILL.md`, `.claude/skills/`; all frontmatter fields optional, `description` recommended | Yes — Task tool, general-purpose subagent; `context: fork` runs the skill itself in a forked subagent | Yes — filesystem, web fetch, bash | File-based | **full** (documented, not executed here) | — |
| **Gemini CLI** | Yes — since v0.26.0; `~/.gemini/skills/` or `~/.agents/skills/`, `.gemini/skills/` or `.agents/skills/` | **unverified** — the docs describe skill activation and consent, not a general subagent API | Yes | File-based | **needs-adaptation** | If no isolation mechanism exists, run **one actor seat** and label the run single-perspective. Do not simulate several actors in one context |
| **OpenAI Codex CLI** | **unverified** — vendor page `developers.openai.com/codex/skills` returned HTTP 403 at verification time; third-party summaries report `.agents/skills`, `~/.agents/skills`, `/etc/codex/skills` and an optional `agents/openai.yaml` | **unverified** — separate-process invocation (`codex exec` per seat, read-only sandbox) is a plausible route, not a confirmed API | Yes | File-based | **unverified** | Assume no isolation until confirmed: one seat, explicit single-perspective label |
| **Cursor** | Reported as supported since 2.4 (Jan 2026), scanning `.cursor/skills/`, `.agents/skills/`, and legacy `.claude/skills/` | **unverified** | Yes | File-based | **unverified** | As above |
| **Generic agent with file access only** | Maybe | No | Read-only | File-based | **partial** | Skill degrades to a *procedure document*: the agent follows `core/` manually, one perspective. The method still works; the viewpoint diversity does not |

## 2. Evidence

| Platform | Basis | What was actually checked |
|---|---|---|
| WorkBuddy | **Installed and exercised.** Skill copied to `C:/Users/<user>/.workbuddy/skills/oir/` (30 files: `SKILL.md` + `core/` + the state validator) and validated with `check_skill.py` / `check_structure.py` on 2026-11-13; the installed copy's own validator was then run against the example state directory and passed. Subagent dispatch was exercised in the single-case comparison run (`tests/records/`). **Not verified:** that the description triggers automatically in a fresh session — that needs a new session, which a build run cannot start. Do not read this row as "trigger tested" | |
| Claude Code | **Vendor documentation**, `code.claude.com/docs/en/skills`, read 2026-11-13 | Personal/project/enterprise/nested/plugin paths; field list; the 500-line guidance; the constraint that cross-tool packaging accepts only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` |
| Gemini CLI | **Vendor documentation**, `geminicli.com/docs/cli/skills`, read 2026-11-13 | Four discovery tiers, `~/.agents/skills/` alias precedence, `activate_skill` + consent flow, `/skills link` and `gemini skills install` |
| Codex CLI | **Failed verification.** Vendor page returned 403. Paths taken from third-party articles only | Nothing first-hand. Treated as unverified and not shipped as a supported target |
| Cursor | Third-party summaries only | Nothing first-hand |

## 3. The one capability that actually matters

OIR needs isolated seats. Every other platform feature is convenience.

Isolation means: two actor models are produced without either seeing the other, and
without either seeing the researcher's preference. If a platform cannot do that, OIR
still runs — as a single-perspective structured analysis with hypothesis registers,
pre-registered predictions, discriminating investigation and adversarial review.
What is lost is the competing-viewpoint generation, which is the *first* of the three
things that make OIR distinctive (`core/CORE_SPEC.md` §1). The run must say so.

Two failures to avoid:

| Failure | Why it is worse than degrading |
|---|---|
| Simulating three actors by role-playing in one context | Produces correlated output with a diversity-shaped appearance. The reader cannot tell it apart from real isolation |
| Claiming full compatibility because the frontmatter parses | Format compatibility is not capability compatibility. This is how a method silently loses its central mechanism |

## 4. Frontmatter portability

The generated `SKILL.md` uses only these fields, because they survive every
packaging path observed:

```yaml
---
name: oir
description: ...
license: MIT
compatibility: ...
metadata:
  version: "0.1.0"
  upstream: "Open-Intelligence-Research"
---
```

Deliberately avoided: `allowed-tools` (experimental, parsed differently across
hosts), `argument-hint`, `context`, `paths`, `model`, `hooks`. Any of them would tie
the package to one host and break cross-tool packaging, which rejects non-spec
fields outright.

## 5. Re-verification

This table decays. Before publishing a compatibility claim:

1. Open the vendor's current skill documentation; note the date.
2. Run `python packaging/build.py --check` and `check_skill.py`.
3. If possible, install and trigger once. Record what you observed, not what the
   docs promised.
4. Downgrade any row you did not re-check to `unverified`. An out-of-date `full` is
   worse than an honest `unverified`.
