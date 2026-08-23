#!/usr/bin/env python3
"""Sync tools/ed-o-meter/tests/tests-data.json's per-model results from featherbench.

Reads ``results/summary.json`` from the featherbench repository and rewrites the
``results`` object in ``tests-data.json``: for every model present upstream,
each task's entry becomes that model's latest-run record (pass, refusal,
refusalCat, cost, ttft, wall, outTok, inTok, detail, text).

The ``tasks`` array is never touched. It is not derived from summary.json at
all — its ``id``/``category``/``prompt`` fields are edited by hand against
featherbench's own ``tasks/*.json`` files, and its ``title``/``short``/
``refusalOk`` fields are pure editorial content. This script only owns
``results``.

A model that disappears from summary.json keeps its previously stored
results rather than being deleted, and is reported so a human can decide
whether to remove it (mirrors build_ed_o_meter.py's treatment of a board
row absent upstream).

Usage:
    build_ed_o_meter_tests.py <summary.json> [--check]

``--check`` writes nothing and exits 1 if tests-data.json needs regenerating.
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_ed_o_meter import latest_run  # noqa: E402  (same "latest run" definition as the board)

ROOT = Path(__file__).resolve().parent.parent
TESTS_DATA = ROOT / "tools" / "ed-o-meter" / "tests" / "tests-data.json"

# tests-data.json result field -> summary.json record field
FIELD_MAP = (
    ("pass", "passed"),
    ("refusal", "refusal"),
    ("refusalCat", "refusal_category"),
    ("cost", "cost_usd"),
    ("ttft", "latency_s"),
    ("wall", "wall_clock_s"),
    ("outTok", "output_tokens"),
    ("inTok", "input_tokens"),
    ("detail", "check_detail"),
    ("text", "text"),
)


def result_entry(record: dict[str, Any]) -> dict[str, Any]:
    return {dst: record.get(src) for dst, src in FIELD_MAP}


def derive_results(summary: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    """{task_id: {model: entry}} from each model's latest run, across all tasks it covers."""
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in summary["records"]:
        by_model[record["model"]].append(record)

    results: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for model, records in by_model.items():
        for record in latest_run(records):
            results[record["task"]][model] = result_entry(record)
    return results


def merge(existing: dict[str, dict[str, dict[str, Any]]],
         derived: dict[str, dict[str, dict[str, Any]]],
         task_ids: list[str]) -> dict[str, dict[str, dict[str, Any]]]:
    """New data overwrites old per model; a model absent upstream keeps its old entry."""
    merged: dict[str, dict[str, dict[str, Any]]] = {}
    for task_id in task_ids:
        row = {**existing.get(task_id, {}), **derived.get(task_id, {})}
        merged[task_id] = {model: row[model] for model in sorted(row)}
    return merged


def summarise(existing: dict[str, dict[str, dict[str, Any]]],
             merged: dict[str, dict[str, dict[str, Any]]]) -> tuple[list[str], list[str], list[str]]:
    """(added models, updated models, models missing from every task upstream)."""
    old_models = {m for row in existing.values() for m in row}
    new_models = {m for row in merged.values() for m in row}

    added = sorted(new_models - old_models)
    removed = sorted(old_models - new_models)
    updated = sorted(
        m for m in old_models & new_models
        if any(existing.get(t, {}).get(m) != merged.get(t, {}).get(m) for t in merged)
    )
    return added, updated, removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="path to featherbench results/summary.json")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if tests-data.json needs regenerating; write nothing")
    args = parser.parse_args()

    summary_data = json.loads(args.summary.read_text(encoding="utf-8"))
    doc = json.loads(TESTS_DATA.read_text(encoding="utf-8"))

    task_ids = [t["id"] for t in doc["tasks"]]
    derived = derive_results(summary_data)
    merged = merge(doc.get("results", {}), derived, task_ids)

    added, updated, removed = summarise(doc.get("results", {}), merged)
    changed = bool(added or updated)

    if changed or removed:
        print("## tests-data.json refresh\n")
        if added:
            print(f"Added: {', '.join(added)}")
        if updated:
            print(f"Updated (answer/metrics changed): {', '.join(updated)}")
        if removed:
            print(f"Absent from summary.json upstream, old results kept as-is: {', '.join(removed)}")
        if not (added or updated) and removed:
            print("\nNo results content changed.")
    else:
        print("tests-data.json is up to date.")

    if args.check:
        return 1 if changed else 0

    doc["results"] = merged
    TESTS_DATA.write_text(
        json.dumps(doc, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        # Exit 1 is reserved for expected drift. Operational failures use exit 2
        # so CI/skill runs do not mistake malformed input or a script bug for a
        # routine data refresh.
        traceback.print_exc()
        raise SystemExit(2)
