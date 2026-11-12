# Compatibility checklist

Per platform. Tick only what you personally observed. `PLATFORM_COMPATIBILITY.md`
carries the summary table; this file carries the procedure.

## A. Format (same for every platform)

- [ ] `python packaging/build.py --check` → exit 0
- [ ] `python tests/scripts/check_skill.py distributions/` → exit 0
- [ ] `SKILL.md` starts with `---` on line 1
- [ ] Frontmatter contains only `name`, `description`, `license`, `compatibility`,
      `metadata` — nothing host-specific
- [ ] `name` equals the directory name (`oir`)
- [ ] `description` is one line, under 1024 characters, contains no `:`
- [ ] `SKILL.md` is under 500 lines (hosts truncate or drop beyond that)
- [ ] The skill reads `core/` rather than restating the method

## B. Install

### WorkBuddy

- [ ] Copied to `~/.workbuddy/skills/oir/` (Windows: `C:/Users/<user>/.workbuddy/skills/oir/`)
- [ ] `SKILL.md` is at the top level of that directory, not one level deeper
- [ ] `core/` is reachable from the skill's own location, or the repository is
      discoverable by absolute path
- [ ] Started a **new** session (skills are scanned at session start)
- [ ] The skill appears in the skills panel / `/` menu
- [ ] Sent a probe question; the skill was selected
- [ ] The skill asked about scale and budget **before** dispatching anything

### Claude Code

- [ ] Copied to `~/.claude/skills/oir/` or `.claude/skills/oir/`
- [ ] Frontmatter fields survive packaging (`/plugin` or `package_skill.py` path
      rejects non-spec fields such as `argument-hint`)
- [ ] `/oir` appears in the slash menu
- [ ] Automatic invocation works from a probe question
- [ ] `Task` tool is available (needed for isolated seats)

### Portable `.agents/skills`

- [ ] Copied to `~/.agents/skills/oir/` or `.agents/skills/oir/`
- [ ] Gemini CLI: `gemini skills list` shows it
- [ ] Gemini CLI: activation prompts for consent before injecting
- [ ] Codex CLI: **status unverified at 2026-11-13** — vendor page returned 403.
      Do not tick this without observing it yourself
- [ ] Cursor: **status unverified** — third-party reports only

## C. Capability

| Capability | Needed for | Consequence if absent |
|---|---|---|
| Read files in `core/` | Everything | The skill cannot follow the method; stop |
| Write files under `research/<slug>/` | State | No state, no audit trail, no loop; stop |
| Web retrieval | S1, S4 | Fact base and investigation cannot run; report "no evidence obtained" rather than simulating |
| **Isolated subagent / second process** | S2 | Viewpoint diversity lost. Run one actor, label the run single-perspective. **Do not** role-play several actors in one context |
| Shell (optional) | Validator | Skip validation and say so; never imply it passed |

## D. Behavioural probe

One question, run once per platform:

> "Why did [a named institution] delay [a named decision], and what would change
> its position?"

Expected sequence:

1. Confirms the question is not a factual lookup and names the cutoff date
2. Proposes 2–3 actor candidates **with a source each**
3. Asks about scale (3 / 5 / 7) and budget
4. Does **not** dispatch any seat before that answer

| Failure | Diagnosis |
|---|---|
| Starts simulating immediately | Authorisation rule not reaching the model; check that the skill body was actually loaded, not just its description |
| Produces one balanced paragraph | Fell back to generic research behaviour; the trigger matched but the body did not load |
| Names actors with no sources | The fact-base gate is being skipped |
| Offers to run several actors in one conversation | Isolation binding missing for this host; the package needs a platform entry, not a prompt fix |

## E. What this checklist cannot establish

Format checks and one behavioural probe do not establish that the method improves
analysis. That requires the comparison protocol in `tests/experiments/`, which has
been executed once, for two of four modes, on one case. See `tests/records/`.
