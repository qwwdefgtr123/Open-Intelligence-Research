#!/usr/bin/env python3
"""Build platform distributions from one template.

    python packaging/build.py            # build all platforms
    python packaging/build.py --check    # build nothing, verify generated files match
    python packaging/build.py --only workbuddy

Stamping one template is the whole point: three hand-maintained near-identical
SKILL.md files diverge within a month, and the divergence is always in the
methodology, which is the part that must not fork.

Exit 0 = ok, 1 = error or (with --check) drift detected.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "packaging" / "skill.template.md"
PLATFORMS = REPO / "packaging" / "platforms.json"
OUT_ROOT = REPO / "distributions"

PLACEHOLDERS = [
    "{{SKILL_NAME}}",
    "{{DESCRIPTION}}",
    "{{COMPATIBILITY}}",
    "{{VERSION}}",
    "{{UPSTREAM}}",
    "{{CORE_ROOT}}",
    "{{DISPATCH_BLOCK}}",
]


def render(template: str, skill: dict, platform: dict) -> str:
    core_root = skill["core_root"]
    # A placeholder substituted into file paths and a shell command must be a path
    # token, not prose. This guard exists because a sentence once shipped here and
    # silently corrupted every path in all three generated skills.
    if len(core_root) > 24 or any(c.isspace() for c in core_root):
        raise SystemExit(
            f"skill.core_root must be a short path token with no spaces, got {core_root!r}. "
            "Put the explanation in packaging/skill.template.md instead."
        )
    install_lines = "\n".join(
        f"| {i['scope']} | `{i['path']}` |" + (f" also `{i['windows']}`" if i.get("windows") else "")
        for i in platform["install"]
    )
    dispatch = platform["dispatch"].strip()
    dispatch_block = (
        f"**Platform: {platform['display']}**\n\n"
        f"Install locations:\n\n| Scope | Path |\n|---|---|\n{install_lines}\n\n"
        f"{dispatch}"
    )

    out = template
    for key, val in {
        "{{SKILL_NAME}}": skill["name"],
        "{{DESCRIPTION}}": skill["description"],
        "{{COMPATIBILITY}}": platform["compatibility"],
        "{{VERSION}}": skill["version"],
        "{{UPSTREAM}}": skill["upstream"],
        "{{CORE_ROOT}}": skill["core_root"],
        "{{DISPATCH_BLOCK}}": dispatch_block,
    }.items():
        out = out.replace(key, val)

    leftovers = [p for p in PLACEHOLDERS if p in out]
    if leftovers:
        raise SystemExit(f"unresolved placeholders: {leftovers}")

    # Every core-root reference must be a plain path tail, including inside fenced
    # code blocks, where an inline-backtick checker cannot see it. This is the check
    # that would have caught a prose sentence being substituted into `python <path>`.
    for m in re.finditer(r"\$OIR_ROOT([^\s`]*)", out):
        tail = m.group(1)
        if not re.fullmatch(r"(/[A-Za-z0-9_./<>-]+)?", tail):
            raise SystemExit(
                f"core-root reference is not a clean path: '$OIR_ROOT{tail}'. "
                "Check skill.core_root in packaging/platforms.json and the template."
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", default=None)
    args = ap.parse_args()

    cfg = json.loads(PLATFORMS.read_text(encoding="utf-8"))
    template = TEMPLATE.read_text(encoding="utf-8")
    skill = cfg["skill"]

    drift = 0
    for platform in cfg["platforms"]:
        if args.only and platform["id"] != args.only:
            continue
        content = render(template, skill, platform)
        target = OUT_ROOT / platform["id"] / "skills" / skill["name"] / "SKILL.md"
        rel = target.relative_to(REPO).as_posix()

        if args.check:
            if not target.is_file():
                print(f"  ! missing: {rel}")
                drift += 1
            elif target.read_text(encoding="utf-8") != content:
                print(f"  ! stale: {rel} (template changed, rebuild required)")
                drift += 1
            else:
                print(f"  ok {rel}")
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        lines = content.count("\n") + 1
        print(f"  wrote {rel} ({lines} lines)")

    if args.check:
        if drift:
            print(f"result: DRIFT ({drift} file(s)) - run python packaging/build.py")
            return 1
        print("result: in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
