#!/usr/bin/env python3
"""Repository structure checks.

  1. No empty files (the spec forbids structural filler).
  2. Every JSON file parses.
  3. Every relative markdown link resolves.
  4. Every path in the README repository-index code block exists.
  5. Every file required by the delivery contract exists.
  6. No file under core/ names a specific product or tool (platform independence).

Usage:
    python tests/scripts/check_structure.py
    python tests/scripts/check_structure.py --root .

Exit 0 = pass, 1 = failure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".workbuddy", "__pycache__", "node_modules", ".venv", "research"}

REQUIRED = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "core/CORE_SPEC.md",
    "core/PRINCIPLES.md",
    "core/workflows/01-research-intake.md",
    "core/workflows/02-actor-simulation.md",
    "core/workflows/03-hypothesis-generation.md",
    "core/workflows/04-evidence-investigation.md",
    "core/workflows/05-adversarial-review.md",
    "core/workflows/06-iterative-research.md",
    "core/roles/research-director.md",
    "core/roles/actor-simulation.md",
    "core/roles/hypothesis-analyst.md",
    "core/roles/evidence-investigator.md",
    "core/roles/red-team-analyst.md",
    "core/roles/synthesis-analyst.md",
    "core/schemas/research-state.schema.json",
    "core/schemas/actor.schema.json",
    "core/schemas/hypothesis.schema.json",
    "core/schemas/prediction.schema.json",
    "core/schemas/evidence.schema.json",
    "core/schemas/source.schema.json",
    "core/schemas/fact.schema.json",
    "core/schemas/investigation.schema.json",
    "packaging/PACKAGING.md",
    "packaging/PLATFORM_COMPATIBILITY.md",
    "references/METHODS.md",
    "references/PROJECTS.md",
    "tests/workflow-tests.md",
    "tests/schema-validation.md",
    "tests/compatibility-checklist.md",
]

PLATFORM_WORDS = [
    "Claude Code", "claude-code", "WorkBuddy", "workbuddy", "Codex", "codex",
    "Gemini CLI", "Cursor", "OpenAI", "Anthropic", "ChatGPT",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TREE_PATH_RE = re.compile(r"^[│├└─\s]*([\w./-]+\.(?:md|json|py|txt|yaml|yml))\s*(?:#.*)?$")


def walk(root: Path):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    errors: list[str] = []
    warnings: list[str] = []
    checks = 0

    files = list(walk(root))
    by_rel = {p.relative_to(root).as_posix(): p for p in files}

    print(f"\n=== check_structure: {len(files)} files under {root.name} ===")

    for rel, p in by_rel.items():
        if p.suffix in {".md", ".py", ".json", ".txt", ".yaml", ".yml"} and p.stat().st_size == 0:
            errors.append(f"empty file: {rel}")
        checks += 1

    for rel, p in by_rel.items():
        if p.suffix == ".json":
            try:
                json.loads(p.read_text(encoding="utf-8"))
                checks += 1
            except Exception as exc:
                errors.append(f"invalid JSON: {rel} ({exc})")

    for rel, p in by_rel.items():
        if p.suffix != ".md":
            continue
        text = p.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#")[0].strip()
            if not clean:
                continue
            resolved = (p.parent / clean).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: broken link -> {target}")
            else:
                checks += 1

    readme = by_rel.get("README.md")
    if readme:
        text = readme.read_text(encoding="utf-8")
        in_block = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                in_block = not in_block
                continue
            if not in_block:
                continue
            m = TREE_PATH_RE.match(line)
            if not m:
                continue
            candidate = m.group(1)
            if candidate.endswith("/"):
                continue
            if candidate not in by_rel:
                errors.append(f"README tree lists a missing file: {candidate}")
            else:
                checks += 1

    for rel in REQUIRED:
        if rel not in by_rel:
            errors.append(f"required file missing: {rel}")
        else:
            checks += 1

    for rel, p in by_rel.items():
        if not rel.startswith("core/"):
            continue
        text = p.read_text(encoding="utf-8")
        for word in PLATFORM_WORDS:
            if word in text:
                errors.append(f"{rel}: names platform-specific '{word}' - core/ must stay platform-independent")

    print(f"checks passed: {checks}")
    for w in warnings:
        print(f"  ~ {w}")
    if errors:
        for e in errors:
            print(f"  ! {e}")
        print(f"result: FAIL ({len(errors)} error(s))")
        return 1
    print("result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
