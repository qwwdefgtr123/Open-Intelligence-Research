# Packaging

How OIR becomes an installable skill on different agent platforms, without the
methodology forking.

## 1. The rule

**One template, stamped per platform. Never hand-edit a generated `SKILL.md`.**

```
packaging/
├── skill.template.md     # the only place the operating instructions live
├── platforms.json        # per-platform: install paths, dispatch binding, verification
└── build.py              # stamps template + platform -> distributions/
```

Three hand-maintained near-identical skill files diverge within a month, and the
divergence always lands in the methodology — the one part that must stay identical.
`build.py --check` fails the test suite on drift, so the divergence is caught
mechanically rather than by review.

## 2. What is platform-specific, and what is not

| Layer | Platform-specific? | Where |
|---|---|---|
| Principles, entity model, workflows, roles, schemas, templates | **No** | `core/` |
| Install location, frontmatter compatibility, subagent dispatch syntax, tool names | **Yes** | `packaging/platforms.json` → stamped into `distributions/<id>/skills/oir/SKILL.md` |

`core/` names no product, tool or API. A structural check fails the build if one
appears (`tests/scripts/check_structure.py`, platform-word scan). That is what makes
a new platform a translation job rather than a fork.

## 3. Build

```bash
python packaging/build.py                 # write all distributions
python packaging/build.py --check         # verify generated files are current
python packaging/build.py --only workbuddy
python tests/scripts/check_skill.py distributions/
```

Generated output:

```
distributions/
├── workbuddy/skills/oir/SKILL.md
├── claude-code/skills/oir/SKILL.md
└── agents-skills/skills/oir/SKILL.md
```

Each is ~120 lines: enough to route the agent into `core/`, not enough to duplicate
it. The skill body is a **navigation layer plus hard rules**, not a copy of the
method. That is the whole point of progressive disclosure — a skill that inlines
the method costs that context on every trigger, whether or not the run needs it.

## 4. Install

| Platform | User-level | Project-level |
|---|---|---|
| WorkBuddy | `~/.workbuddy/skills/oir/` | `<workspace>/.workbuddy/skills/oir/` |
| Claude Code | `~/.claude/skills/oir/` | `.claude/skills/oir/` |
| Portable (Codex CLI, Cursor, Gemini CLI alias) | `~/.agents/skills/oir/` | `.agents/skills/oir/` |

The directory name must equal the skill name (`oir`). Copy the whole directory; do
not flatten it. Most hosts scan skills at session start — a new session is required
before the description enters context.

The skill needs to find `core/`. Two supported arrangements:

1. **Clone alongside**: keep the `Open-Intelligence-Research` repository on disk and
   have the skill point at its absolute path.
2. **Self-contained**: copy `core/` into the installed skill directory
   (`~/.workbuddy/skills/oir/core/`) so the skill is portable as one folder. This
   duplicates the method on disk but not in the agent's context, and `build.py
   --check` still governs the `SKILL.md` half.

Arrangement 2 is the one to use for distribution to other people. Arrangement 1 is
the one to use while developing.

## 5. Verify an install

```bash
# structure + frontmatter + cross-file references
python tests/scripts/check_skill.py distributions/
python tests/scripts/check_structure.py

# after a real run
python tests/scripts/validate_state.py research/<slug> --check-isolation
```

Manual check, per platform:

1. Start a **new** session.
2. Send a question that should trigger OIR, e.g. *"Why did the ministry delay the
   programme, and what would change its position?"*
3. Confirm the skill is selected and that it reads `core/PRINCIPLES.md` rather than
   improvising a method.
4. Confirm it asks about scale and budget before dispatching any seat.

If step 4 is skipped, the skill is not enforcing the authorisation rule — treat it
as a packaging defect, not a model whim.

## 6. Upgrade

```bash
git pull
python packaging/build.py --check     # drift?
python packaging/build.py             # rebuild if needed
```

Re-copy the skill directory. Version lives in `packaging/platforms.json →
skill.version` and is stamped into the frontmatter `metadata.version`, so an
installed copy can be identified without opening the file.

## 7. Add a platform

1. Append an entry to `packaging/platforms.json` with: `id`, `display`,
   `compatibility`, `install` paths, `dispatch` text, `verified` date, and
   `verification` — the sentence that says **how** you know (vendor doc, or tested).
2. Run `python packaging/build.py --only <id>`.
3. Run `python tests/scripts/check_skill.py distributions/`.
4. Add a row to `packaging/PLATFORM_COMPATIBILITY.md`. If you have not run it, the
   row says `unverified` and the verification column says why.
5. If the platform cannot isolate seats, write that into `dispatch` explicitly. The
   skill must then declare reduced viewpoint diversity rather than silently
   running seats in one context.

## 8. What not to do

| Anti-pattern | Why it breaks |
|---|---|
| Shipping the repository root as one skill | The agent loads the whole method on every trigger; the context cost is paid whether or not it is needed |
| Copying `core/` content into each `SKILL.md` | Immediate fork; three platforms become three methods |
| Hand-fixing a generated `SKILL.md` | The next build silently reverts it. Edit the template |
| Claiming a platform works because it reads `SKILL.md` | Reading the file is not the same as dispatching isolated seats. Capability and format are different questions |
| Adding platform prose to `core/` | Breaks the independence that makes porting cheap; caught by the structural check |
