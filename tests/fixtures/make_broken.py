#!/usr/bin/env python3
"""Generate the `broken` fixture from the `good` one, planting one defect per rule.

A validator that passes a valid state proves nothing. This fixture exists so the
test can prove each rule actually fires. If `validate_state.py` passes this
directory, the validator is broken.

    python tests/fixtures/make_broken.py
    python tests/scripts/validate_state.py tests/fixtures/broken --check-isolation   # must exit 1
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "good"
DST = HERE / "broken"

PLANTED: list[str] = []


def load(rel: str) -> dict:
    return json.loads((DST / rel).read_text(encoding="utf-8"))


def save(rel: str, obj: dict) -> None:
    (DST / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    if not SRC.is_dir():
        print(f"missing source fixture: {SRC}")
        return 1
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    fact = load("facts/FACT-001.json")
    fact["sources"] = ["SRC-099"]
    save("facts/FACT-001.json", fact)
    PLANTED.append("FACT-001 -> dangling source SRC-099")

    hyp2 = load("hypotheses/HYP-002.json")
    hyp2["predictions"] = []
    hyp2["status"] = "live"
    save("hypotheses/HYP-002.json", hyp2)
    PLANTED.append("HYP-002 -> status live with no predictions")

    prd2 = load("predictions/PRD-002.json")
    prd2["registered_at"] = "2026-10-05T00:00:00Z"
    prd2["judgement"] = "confirmed"
    prd2["judged_at"] = "2026-10-06T00:00:00Z"
    prd2["judged_by"] = "EVD-001"
    prd2.pop("late", None)
    save("predictions/PRD-002.json", prd2)
    PLANTED.append("PRD-002 -> registered after INV-001 started, late flag unset")

    evd = load("evidence/EVD-001.json")
    evd["independence_note"]["effective_independent"] = 3
    save("evidence/EVD-001.json", evd)
    PLANTED.append("EVD-001 -> claims 3 independent from a single root")

    src1 = load("sources/SRC-001.json")
    src1["derived_from"] = ["SRC-002"]
    save("sources/SRC-001.json", src1)
    src2 = load("sources/SRC-002.json")
    src2["derived_from"] = ["SRC-001"]
    save("sources/SRC-002.json", src2)
    PLANTED.append("SRC-001 <-> SRC-002 -> dependency cycle")

    hyp1 = load("hypotheses/HYP-001.json")
    hyp1["confidence"] = 0.7
    save("hypotheses/HYP-001.json", hyp1)
    PLANTED.append("HYP-001 -> forbidden composite confidence field")

    act2 = load("actors/ACT-002.json")
    act2["version"] = 1
    save("actors/ACT-002.json", act2)
    index = load("index.json")
    index["actor_set"]["runs"][1]["simulation_input_hash"] = index["actor_set"]["runs"][0]["simulation_input_hash"]
    index["actor_set"]["runs"][1]["execution_unit"] = index["actor_set"]["runs"][0]["execution_unit"]
    save("index.json", index)
    PLANTED.append("ACT-001/ACT-002 -> shared execution unit and input hash")

    print(f"wrote {DST.relative_to(HERE.parent.parent)} with {len(PLANTED)} planted defects:")
    for p in PLANTED:
        print(f"  - {p}")
    print("\nexpected: validate_state.py exits 1 and names every item above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
