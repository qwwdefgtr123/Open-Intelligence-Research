#!/usr/bin/env python3
"""Validate Agent Skill packages in distributions/.

Checks per skill directory:
  1. SKILL.md exists and is non-trivial.
  2. YAML frontmatter present, parses, and has `name` + `description`.
  3. `name` matches the directory name and the Agent Skills naming rule
     (lowercase, hyphens, no leading/trailing/double hyphen, <= 64 chars).
  4. `description` <= 1024 chars and states both what it does and when to use it.
  5. Body stays within a reasonable context budget and points at existing files.
  6. No absolute local paths and no secrets patterns (a skill is published).

Usage:
    python tests/scripts/check_skill.py distributions/
    python tests/scripts/check_skill.py distributions/workbuddy/skills/oir

Exit 0 = pass (warnings allowed), 1 = failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
ABS_PATH_RE = re.compile(r"(^|[\s(\"'])((/Users/|/home/|C:\\\\|C:/|/mnt/)[^\s)\"']*)")
MAX_DESC = 1024
MAX_BODY_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    problems: list[str] = []
    if not text.startswith("---"):
        return {}, text, ["no YAML frontmatter (file must start with '---')"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text, ["unterminated frontmatter"]
    raw, body = parts[1], parts[2]
    data: dict[str, str] = {}
    key = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_-]+:", line):
            key, _, val = line.partition(":")
            key = key.strip()
            data[key] = val.strip().strip("\"'")
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
        else:
            problems.append(f"unparseable frontmatter line: {line.strip()!r}")
    return data, body, problems


def check_skill(skill_dir: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: no SKILL.md"], warnings

    text = skill_md.read_text(encoding="utf-8")
    data, body, fm_problems = parse_frontmatter(text)
    errors.extend(f"{skill_dir.name}: {p}" for p in fm_problems)

    name = data.get("name", "")
    desc = data.get("description", "")

    if not name:
        errors.append(f"{skill_dir.name}: frontmatter missing 'name'")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: name '{name}' violates naming rule (lowercase a-z0-9, single hyphens)")
        if len(name) > 64:
            errors.append(f"{skill_dir.name}: name longer than 64 chars")
        if name != skill_dir.name:
            warnings.append(f"{skill_dir.name}: name '{name}' != directory name")

    if not desc:
        errors.append(f"{skill_dir.name}: frontmatter missing 'description'")
    else:
        if len(desc) > MAX_DESC:
            errors.append(f"{skill_dir.name}: description {len(desc)} chars > {MAX_DESC}")
        low = desc.lower()
        if not any(k in low for k in ("use when", "use this", "use for", "load when", "trigger")):
            warnings.append(f"{skill_dir.name}: description lacks an explicit 'use when ...' clause")
        if len(desc) < 80:
            warnings.append(f"{skill_dir.name}: description is short ({len(desc)} chars) - weak trigger surface")
        if ":" in desc:
            warnings.append(f"{skill_dir.name}: description contains ':' which breaks some YAML parsers")

    body_lines = body.count("\n")
    if body_lines > MAX_BODY_LINES:
        warnings.append(f"{skill_dir.name}: body is {body_lines} lines; keep SKILL.md under {MAX_BODY_LINES}")

    for secret in SECRET_RE.findall(text):
        errors.append(f"{skill_dir.name}: possible secret in SKILL.md ({secret[:8]}...)")
    for m in ABS_PATH_RE.finditer(text):
        warnings.append(f"{skill_dir.name}: absolute local path {m.group(2)!r}")

    if "core/" not in text:
        warnings.append(f"{skill_dir.name}: does not reference core/ - the skill may have forked methodology")

    for ref in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|json|py))`", body):
        if ref.startswith(("http", "/")):
            continue
        candidates = [skill_dir / ref, repo_root / ref]
        if not any(c.exists() for c in candidates):
            warnings.append(f"{skill_dir.name}: referenced file not found: {ref}")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="skill dir, or a directory containing skill dirs")
    ap.add_argument("--repo-root", default=None)
    args = ap.parse_args()

    target = Path(args.target).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else target
    while repo_root != repo_root.parent and not (repo_root / "core").is_dir():
        repo_root = repo_root.parent

    if (target / "SKILL.md").is_file():
        skill_dirs = [target]
    else:
        skill_dirs = sorted({p.parent for p in target.rglob("SKILL.md")})

    if not skill_dirs:
        print(f"no SKILL.md found under {target}")
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for d in skill_dirs:
        e, w = check_skill(d, repo_root)
        all_errors.extend(e)
        all_warnings.extend(w)

    print(f"\n=== check_skill: {len(skill_dirs)} skill(s) ===")
    for w in all_warnings:
        print(f"  ~ {w}")
    if all_errors:
        for e in all_errors:
            print(f"  ! {e}")
        print(f"result: FAIL ({len(all_errors)} error(s), {len(all_warnings)} warning(s))")
        return 1
    print(f"result: PASS ({len(all_warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
