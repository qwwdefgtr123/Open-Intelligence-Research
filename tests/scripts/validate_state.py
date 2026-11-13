#!/usr/bin/env python3
"""Validate an OIR research directory.

Checks, in order:
  1. Every JSON file parses.
  2. Every entity validates against its schema in core/schemas/.
  3. Every cross-entity ID reference resolves.
  4. Predictions were registered before the investigations that tested them.
  5. Source dependency has no cycles; independence counts do not exceed roots.
  6. Actor seats ran in distinct execution units with distinct input hashes.
  7. A hypothesis with no predictions is not above `draft`.
  8. No composite confidence figure anywhere in a hypothesis.
  9. `fact_snapshot.hash` matches a recomputed sha256 over the frozen facts - a
     frozen snapshot that cannot be verified is decoration, not a freeze.

Exit codes:
  0  all checks passed, including schema validation
  1  failures found
  3  INCOMPLETE - jsonschema is not installed, so the schema layer did not run.
     This is deliberately not 0: a check that did not run must not report a pass.

Usage:
    python tests/scripts/validate_state.py research/<slug>
    python tests/scripts/validate_state.py research/<slug> --check-isolation
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ENTITY_DIRS = {
    "facts": ("FACT", "fact.schema.json"),
    "sources": ("SRC", "source.schema.json"),
    "actors": ("ACT", "actor.schema.json"),
    "hypotheses": ("HYP", "hypothesis.schema.json"),
    "predictions": ("PRD", "prediction.schema.json"),
    "evidence": ("EVD", "evidence.schema.json"),
    "investigations": ("INV", "investigation.schema.json"),
}

# Prose-led entities: no JSON Schema (see CORE_SPEC §4), but their references must
# still resolve. Without this they were loaded by nothing, which made the spec's
# claim that they are "validated by cross-reference checks" untrue.
EXTRA_DIRS = {
    "claims": "CLM",
    "conflicts": "CFL",
    "assumptions": "ASM",
    "decisions": "DEC",
    "uncertainties": "UNC",
}

ID_RE = re.compile(r"^(FACT|SRC|CLM|ACT|SIM|HYP|PRD|EVD|INV|CFL|ASM|DEC|UNC|ITR)-(\d{3,})$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks = 0
        self.schema_checked = False

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> None:
        self.checks += 1

    def dump(self, label: str) -> int:
        print(f"\n=== validate_state: {label} ===")
        print(f"checks passed: {self.checks}")
        if self.warnings:
            print(f"warnings: {len(self.warnings)}")
            for w in self.warnings:
                print(f"  ~ {w}")
        if self.errors:
            print(f"FAILURES: {len(self.errors)}")
            for e in self.errors:
                print(f"  ! {e}")
            print("result: FAIL")
            return 1
        if not self.schema_checked:
            print("result: INCOMPLETE - the schema layer did not run")
            print("        install jsonschema (pip install -r requirements.txt) and re-run.")
            print("        Do not report this run as validated.")
            return 3
        print("result: PASS")
        return 0


def load_json(path: Path, rep: Report):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        rep.error(f"{path.name}: invalid JSON ({exc})")
        return None


def collect(root: Path, rep: Report) -> dict[str, dict]:
    """Load every entity, keyed by id."""
    store: dict[str, dict] = {}
    dirs: dict[str, tuple[str, str | None]] = dict(ENTITY_DIRS)
    for folder, prefix in EXTRA_DIRS.items():
        dirs[folder] = (prefix, None)

    for folder, (prefix, _schema) in dirs.items():
        d = root / folder
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            obj = load_json(p, rep)
            if obj is None:
                continue
            eid = obj.get("id")
            if not isinstance(eid, str) or not ID_RE.match(eid):
                rep.error(f"{folder}/{p.name}: missing or malformed id")
                continue
            if not eid.startswith(prefix + "-"):
                rep.error(f"{folder}/{p.name}: id {eid} does not match folder prefix {prefix}")
                continue
            if eid in store:
                rep.error(f"duplicate id {eid}")
                continue
            obj["__file"] = f"{folder}/{p.name}"
            store[eid] = obj
            rep.ok()
    return store


def validate_schemas(root: Path, store: dict[str, dict], schemas_dir: Path, rep: Report) -> None:
    if jsonschema is None:
        rep.warn("jsonschema not installed - schema layer skipped, result will be INCOMPLETE")
        return
    rep.schema_checked = True
    for folder, (_prefix, schema_name) in ENTITY_DIRS.items():
        d = root / folder
        if not d.is_dir():
            continue
        schema_path = schemas_dir / schema_name
        if not schema_path.is_file():
            rep.warn(f"schema missing: {schema_name} - {folder} not schema-validated")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        for p in sorted(d.glob("*.json")):
            obj = load_json(p, rep)
            if obj is None:
                continue
            for err in sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path)):
                loc = "/".join(str(x) for x in err.absolute_path) or "(root)"
                rep.error(f"{folder}/{p.name}: {loc}: {err.message}")
            rep.ok()


def check_references(store: dict[str, dict], rep: Report, known_res: str | None = None) -> None:
    def refs_of(obj: dict):
        for key, val in obj.items():
            if key.startswith("__") or key == "id":
                continue
            if isinstance(val, str) and ID_RE.match(val):
                yield key, val
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, str) and ID_RE.match(item):
                        yield key, item
                    elif isinstance(item, dict):
                        for k2, v2 in item.items():
                            if isinstance(v2, str) and ID_RE.match(v2):
                                yield f"{key}[].{k2}", v2
                            elif isinstance(v2, list):
                                for v3 in v2:
                                    if isinstance(v3, str) and ID_RE.match(v3):
                                        yield f"{key}[][].{k2}", v3

    for eid, obj in store.items():
        for field, target in refs_of(obj):
            if target == eid:
                rep.error(f"{eid}: self-reference in {field}")
                continue
            if target not in store:
                if target.startswith("RES-"):
                    if target == known_res:
                        rep.ok()
                    else:
                        rep.error(f"{eid}: {field} references {target}, but this run is {known_res or 'unnamed'}")
                else:
                    rep.error(f"{eid}: {field} references missing {target}")
            else:
                rep.ok()


def check_prediction_timing(store: dict[str, dict], rep: Report) -> None:
    for pid, pred in store.items():
        if not pid.startswith("PRD-"):
            continue
        judged = pred.get("judgement", "pending")
        if judged == "pending":
            continue
        judge_ev = pred.get("judged_by")
        if not judge_ev or judge_ev not in store:
            rep.error(f"{pid}: judged '{judged}' without a resolvable judged_by evidence id")
            continue
        ev = store[judge_ev]
        inv_id = ev.get("obtained_by")
        inv = store.get(inv_id or "")
        if not inv:
            rep.warn(f"{pid}: cannot resolve investigation behind {judge_ev}")
            continue
        started = inv.get("started_at")
        registered = pred.get("registered_at")
        if started and registered and registered > started:
            if not pred.get("late"):
                rep.error(f"{pid}: registered ({registered}) after investigation started ({started}) and not marked late")
            else:
                rep.warn(f"{pid}: late-registered prediction, excluded from hit rate")
        rep.ok()


def root_of(sid: str, store: dict[str, dict], seen: set[str] | None = None) -> str:
    seen = seen or set()
    if sid in seen:
        raise ValueError(f"dependency cycle at {sid}")
    seen.add(sid)
    src = store.get(sid, {})
    parents = src.get("derived_from") or []
    if not parents:
        return sid
    return root_of(parents[0], store, seen)


def check_independence(store: dict[str, dict], rep: Report) -> None:
    for sid, src in store.items():
        if not sid.startswith("SRC-"):
            continue
        try:
            root_of(sid, store)
        except ValueError as exc:
            rep.error(str(exc))
            continue
        derived = src.get("derived_from") or []
        cls = src.get("independence_class")
        expected = "derived" if derived else "root"
        if cls and cls not in {expected, "unknown"}:
            rep.error(f"{sid}: independence_class '{cls}' contradicts derived_from ({expected})")
        rep.ok()

    for eid, ev in store.items():
        if not eid.startswith("EVD-"):
            continue
        note = ev.get("independence_note") or {}
        claimed = note.get("effective_independent")
        srcs = [s for s in ev.get("source", []) if s in store]
        if not isinstance(claimed, int) or not srcs:
            continue
        try:
            roots = {root_of(s, store) for s in srcs}
        except ValueError:
            # a dependency cycle is reported separately; fall back to the cited
            # sources so an overcount is still caught rather than skipped
            roots = set(srcs)
        if claimed > len(roots):
            rep.error(
                f"{eid}: claims {claimed} independent sources but the {len(srcs)} cited "
                f"sources collapse to {len(roots)} root(s)"
            )
        elif claimed < len(roots):
            rep.warn(f"{eid}: claims {claimed} independent but {len(roots)} roots exist (under-counting is safe, verify)")
        rep.ok()


def check_isolation(index: dict, store: dict[str, dict], rep: Report, strict: bool) -> None:
    runs = (index.get("actor_set") or {}).get("runs") or []
    if not runs:
        if strict:
            rep.error("actor_set.runs is empty - isolation cannot be verified")
        else:
            rep.warn("actor_set.runs empty - isolation not verified")
        return
    units = {}
    hashes = {}
    for run in runs:
        unit = run.get("execution_unit")
        h = run.get("simulation_input_hash")
        actor = run.get("actor")
        if unit in units and units[unit] != actor:
            rep.error(f"isolation failure: {actor} and {units[unit]} share execution unit '{unit}'")
        units[unit] = actor
        if h in hashes and hashes[h] != actor:
            rep.error(f"isolation failure: {actor} and {hashes[h]} have identical simulation_input_hash")
        hashes[h] = actor
        rep.ok()


def check_hypothesis_rules(store: dict[str, dict], rep: Report) -> None:
    for hid, hyp in store.items():
        if not hid.startswith("HYP-"):
            continue
        preds = hyp.get("predictions") or []
        status = hyp.get("status")
        if not preds and status not in {"draft", "excluded"}:
            rep.error(f"{hid}: status '{status}' with no predictions (only draft/excluded allowed)")
        for banned in ("confidence", "confidence_score", "probability"):
            if banned in hyp:
                rep.error(f"{hid}: composite '{banned}' field is forbidden - use the four assessment columns")
        if status in {"live", "strengthened"} and not hyp.get("mechanism"):
            rep.error(f"{hid}: promoted without a mechanism")
        rep.ok()


def check_missing_mechanism_len(store: dict[str, dict], rep: Report) -> None:
    for hid, hyp in store.items():
        if not hid.startswith("HYP-"):
            continue
        mech = hyp.get("mechanism") or ""
        if hyp.get("status") != "draft" and len(mech) < 60:
            rep.warn(f"{hid}: mechanism shorter than 60 chars - likely a gesture, not a chain")


def check_snapshot_hash(index: dict, store: dict[str, dict], rep: Report) -> None:
    """The freeze is only a freeze if the hash can be recomputed from the facts."""
    snap = index.get("fact_snapshot") or {}
    recorded = snap.get("hash")
    ids = snap.get("ids") or []
    if not recorded or not ids:
        return
    missing = [i for i in ids if i not in store]
    for i in missing:
        rep.error(f"fact_snapshot lists {i}, which does not exist")
    if missing:
        return
    payload = "\n".join(f"{i}\t{store[i].get('statement', '')}" for i in sorted(ids))
    actual = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    if recorded != actual:
        rep.error(
            "fact_snapshot.hash does not match the frozen facts "
            f"(recorded {recorded[:16]}..., recomputed {actual[:16]}...). "
            "If a fact was intentionally revised, bump fact_snapshot.version and record "
            "a DEC of kind fact-revision; otherwise a fact was edited after the freeze."
        )
    else:
        rep.ok()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("research_dir")
    ap.add_argument("--schemas", default=None, help="path to core/schemas (default: <repo>/core/schemas)")
    ap.add_argument("--check-isolation", action="store_true")
    args = ap.parse_args()

    root = Path(args.research_dir).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 1
    schemas_dir = Path(args.schemas) if args.schemas else None
    if schemas_dir is None:
        probe = root
        for _ in range(6):
            candidate = probe / "core" / "schemas"
            if candidate.is_dir():
                schemas_dir = candidate
                break
            if probe.parent == probe:
                break
            probe = probe.parent
    if schemas_dir is None:
        schemas_dir = root.parent.parent / "core" / "schemas"

    rep = Report()
    index = load_json(root / "index.json", rep)
    if index is None:
        rep.dump(str(root))
        return 1

    if jsonschema is not None and (schemas_dir / "research-state.schema.json").is_file():
        schema = json.loads((schemas_dir / "research-state.schema.json").read_text(encoding="utf-8"))
        for err in jsonschema.Draft202012Validator(schema).iter_errors(index):
            loc = "/".join(str(x) for x in err.absolute_path) or "(root)"
            rep.error(f"index.json: {loc}: {err.message}")
        rep.ok()

    store = collect(root, rep)
    validate_schemas(root, store, schemas_dir, rep)
    check_snapshot_hash(index, store, rep)
    check_references(store, rep, (index.get("research") or {}).get("id"))
    check_prediction_timing(store, rep)
    check_independence(store, rep)
    check_isolation(index, store, rep, args.check_isolation)
    check_hypothesis_rules(store, rep)
    check_missing_mechanism_len(store, rep)

    return rep.dump(str(root))


if __name__ == "__main__":
    sys.exit(main())
