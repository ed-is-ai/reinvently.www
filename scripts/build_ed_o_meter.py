#!/usr/bin/env python3
"""Rebuild the Ed-o-meter board data from featherbench's consolidated results.

Reads ``results/summary.json`` from the featherbench repository and rewrites
``tools/ed-o-meter/data.js`` with freshly derived numbers, then writes a
Markdown report describing what moved and which editorial claims on the page
those movements put in doubt.

Only numeric fields are derived. Presentation and provenance fields — id, hex,
panel, and the footnote references pNote/rNote/cNote/sNote — are editorial
judgements that live in data.js and are carried across unchanged. A model that
appears in the results but not on the board is reported, never invented: it
needs a colour and a default-panel decision from a human.

Usage:
    build_ed_o_meter.py <summary.json> [--report PATH] [--check]

``--check`` writes nothing and exits 1 if data.js is out of date, for CI.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DATA_JS = ROOT / "tools" / "ed-o-meter" / "data.js"
PAGE = ROOT / "tools" / "ed-o-meter" / "index.html"

# Board category keys, in the fixed corner order the ring charts draw.
CATEGORY_KEYS = {
    "coding": "cv",
    "data": "dv",
    "realworld": "rv",
    "security": "sv",
    "tool-use": "tv",
}


# --------------------------------------------------------------------------
# derivation
# --------------------------------------------------------------------------


def wilson(passed: int, total: int, z: float = 1.959963985) -> tuple[int, int]:
    """95% Wilson score interval, as whole percentages."""
    if total == 0:
        return (0, 0)
    p = passed / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return (round(100 * max(0.0, centre - half)), round(100 * min(1.0, centre + half)))


def latest_run(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the records of a model's most recent logical run.

    A logical run is a run_date: featherbench resumes a run under a new run_id
    when it is interrupted, so a single date's records partition the task set
    rather than duplicating it. Consolidation has already applied the
    resume-supersedes-base policy, so grouping by date is safe here.
    """
    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_date[record["run_date"]].append(record)
    return by_date[max(by_date)]


def derive(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Derive one board row from one model's most recent run."""
    total = len(records)
    passed = sum(1 for r in records if r["passed"])
    lo, hi = wilson(passed, total)

    rubrics = [r["rubric_mean"] for r in records if r.get("rubric_mean") is not None]
    latencies = [r["latency_s"] for r in records if r.get("latency_s") is not None]
    cost = sum(r.get("cost_usd") or 0 for r in records)

    # Footnote 4: a refused or blocked trial emits almost nothing and is billed
    # at $0, so including it in the per-task mean makes a model that declined
    # work look cheap. Cost per task is charged against answering trials only.
    answering = [r for r in records if not r.get("refusal")]
    cost_task = cost / len(answering) if answering else 0.0

    row: dict[str, Any] = {
        "pass": round(100 * passed / total),
        "lo": lo,
        "hi": hi,
        "rubric": round(sum(rubrics) / len(rubrics), 1) if rubrics else None,
        "cost": round(cost, 3 if cost < 0.1 else 2),
        "ttft": round(statistics.median(latencies), 1) if latencies else None,
        "costTask": round(cost_task, 4),
        "_run_date": records[0]["run_date"],
        "_trials": total,
        "_rubric_coverage": len(rubrics),
        "_refusals": len(records) - len(answering),
    }

    for category, key in CATEGORY_KEYS.items():
        subset = [r for r in records if r.get("category") == category]
        row[key] = round(100 * sum(1 for r in subset if r["passed"]) / len(subset)) if subset else None

    row["sec"] = row["sv"]
    row["secTxt"] = f"{row['sv']}%" if row["sv"] is not None else "—"
    return row


def board_rows(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in summary["records"]:
        by_model[record["model"]].append(record)
    return {model: derive(latest_run(records)) for model, records in by_model.items()}


# --------------------------------------------------------------------------
# data.js read/write — editorial fields are preserved, never regenerated
# --------------------------------------------------------------------------

EDITORIAL_MODEL_FIELDS = ("id", "name", "hex", "panel", "pNote", "rNote", "cNote", "sNote")


def parse_data_js(text: str) -> tuple[list[dict[str, Any]], str]:
    """Parse the existing data.js into model dicts, preserving declaration order."""
    block = re.search(r"const MODELS = \[\n(.*?)\n\];", text, re.S)
    if not block:
        raise SystemExit("data.js: could not find the MODELS array")
    source_run = re.search(r"sourceRun:'([^']*)'", text)

    models = []
    for line in block.group(1).splitlines():
        line = line.strip().rstrip(",")
        if not line.startswith("{"):
            continue
        row: dict[str, Any] = {}
        for key, raw in re.findall(r"(\w+)\s*:\s*('[^']*'|\[[^\]]*\]|[^,}]+)", line):
            raw = raw.strip()
            if raw.startswith("'"):
                row[key] = raw[1:-1]
            elif raw.startswith("["):
                row[key] = [int(n) for n in re.findall(r"\d+", raw)]
            elif raw in ("true", "false"):
                row[key] = raw == "true"
            elif raw == "null":
                row[key] = None
            else:
                row[key] = float(raw) if "." in raw else int(raw)
        models.append(row)
    return models, (source_run.group(1) if source_run else "")


def render_data_js(models: list[dict[str, Any]], cats: list[dict[str, Any]],
                   source_run: str, generated: str) -> str:
    def fmt(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, list):
            return "[" + ",".join(str(v) for v in value) + "]"
        if isinstance(value, str):
            return f"'{value}'"
        if value is None:
            return "null"
        return str(value)

    # `rubric` is emitted even when null: the board renders a dash for it, and
    # dropping the key would leave the page reading a stale value from nowhere.
    always = {"rubric"}

    def row(fields: list[tuple[str, Any]]) -> str:
        kept = [(k, v) for k, v in fields if v is not None or k in always]
        return "  {" + ", ".join(f"{k}:{fmt(v)}" for k, v in kept) + "},"

    model_lines = []
    for m in models:
        fields = [(k, m.get(k)) for k in ("id", "name", "hex", "panel")]
        fields += [(k, m.get(k)) for k in ("pass", "lo", "hi")]
        fields += [("pNote", m.get("pNote")), ("rubric", m.get("rubric")), ("rNote", m.get("rNote"))]
        fields += [("cost", m.get("cost")), ("ttft", m.get("ttft")), ("costTask", m.get("costTask"))]
        fields += [("cNote", m.get("cNote")), ("sec", m.get("sec")), ("secTxt", m.get("secTxt")),
                   ("sNote", m.get("sNote"))]
        model_lines.append(row(fields))

    cat_lines = [row([(k, c.get(k)) for k in ("name", "ref", "cv", "dv", "rv", "sv", "tv")]) for c in cats]

    return (
        "/* Ed-o-meter board data.\n"
        "   Generated by scripts/build_ed_o_meter.py from featherbench results/summary.json.\n"
        "   Numeric fields are derived; id/name/hex/panel and the footnote refs\n"
        "   (pNote/rNote/cNote/sNote) are editorial and preserved across refreshes.\n"
        "   Loaded as a plain script so the page still works from file://. */\n"
        f"const EOM_META = {{sourceRun:'{source_run}', generated:'{generated}'}};\n\n"
        "const MODELS = [\n" + "\n".join(model_lines) + "\n];\n\n"
        "const CATS = [\n" + "\n".join(cat_lines) + "\n];\n"
    )


# --------------------------------------------------------------------------
# the editorial report — what moved, and what prose that puts in doubt
# --------------------------------------------------------------------------


def prose_blocks(page: str) -> list[tuple[str, str]]:
    """Return (label, text) for each hand-written block that cites the data."""
    blocks: list[tuple[str, str]] = []

    verdict = re.search(r'<p class="verdict">(.*?)</p>', page, re.S)
    if verdict:
        blocks.append(("verdict box", verdict.group(1)))

    for heading, body in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', page, re.S):
        blocks.append((f'tile "{strip_tags(heading)[:44]}"', body))

    for index, note in enumerate(re.findall(r'<p><sup>\d+</sup>(.*?)</p>', page, re.S), start=1):
        blocks.append((f"footnote {index}", note))

    return [(label, strip_tags(text)) for label, text in blocks]


def strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def excerpt(text: str, limit: int = 200) -> str:
    return text[:limit] + ("…" if len(text) > limit else "")


def stale_figures(text: str, before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    """Figures the prose prints verbatim that the new numbers contradict."""
    stale = []
    for field, render in (
        ("pass", lambda v: f"{v}%"),
        ("sec", lambda v: f"{v}%"),
        ("rubric", lambda v: f"{v:.1f}"),
        ("ttft", lambda v: f"{v:.1f}-second"),
        ("cost", lambda v: f"${v:.2f}"),
        ("costTask", lambda v: f"${v:.4f}"),
    ):
        old, new = before.get(field), after.get(field)
        if old is None or old == new:
            continue
        printed = render(old)
        # Word-boundary match so "96%" does not hit inside "196%".
        if re.search(rf"(?<![\d.]){re.escape(printed)}", text):
            stale.append(printed)
    return stale


def material(before: dict[str, Any], after: dict[str, Any]) -> bool:
    """Is the movement big enough that prose about the model may need rewriting?"""
    if abs((after.get("pass") or 0) - (before.get("pass") or 0)) >= 2:
        return True
    if (after.get("sec") or 0) != (before.get("sec") or 0):
        return True
    if after.get("rubric") is None and before.get("rubric") is not None:
        return True
    old_cost, new_cost = before.get("cost") or 0, after.get("cost") or 0
    return old_cost > 0 and abs(new_cost - old_cost) / old_cost >= 0.10


def build_report(old: list[dict[str, Any]], new: dict[str, dict[str, Any]],
                 page: str, summary: dict[str, Any]) -> str:
    lines = ["## Ed-o-meter data refresh", ""]
    lines.append(f"Source: featherbench `results/summary.json`, generated {summary['generated_utc']}.")
    lines.append(f"{summary['counts']['records']} records; "
                 f"{summary['counts']['rescored_vs_source']} re-scored against current checkers; "
                 f"{summary['counts']['overridden']} overridden.")
    lines.append("")

    by_name = {m["name"]: m for m in old}
    moved: dict[str, list[str]] = {}

    lines.append("### Board changes")
    lines.append("")
    changed = False
    for name, row in sorted(new.items(), key=lambda kv: -kv[1]["pass"]):
        previous = by_name.get(name)
        if previous is None:
            changed = True
            lines.append(f"- **NEW: {name}** — {row['pass']}% pass, rubric "
                         f"{row['rubric']}, ${row['cost']}. Not on the board: needs a "
                         f"`hex` colour and a `panel` decision before it can be added.")
            continue
        deltas = []
        for field, label, unit in (("pass", "pass", "%"), ("rubric", "rubric", ""),
                                   ("cost", "cost", ""), ("ttft", "TTFT", "s"),
                                   ("sec", "security", "%")):
            before, after = previous.get(field), row.get(field)
            if before == after:
                continue
            if after is None:
                deltas.append(f"{label} {before}{unit} → none "
                              f"(no judged trials in the latest run)")
            else:
                deltas.append(f"{label} {before}{unit} → {after}{unit}")
        if deltas:
            changed = True
            moved[name] = {"deltas": deltas, "before": previous, "after": row}
            lines.append(f"- **{name}** — " + "; ".join(deltas))

    for name in by_name:
        if name not in new:
            changed = True
            lines.append(f"- **{name}** is on the board but absent from the results — "
                         f"it was removed upstream, or its run was dropped.")

    if not changed:
        lines.append("No numeric changes.")
    lines.append("")

    # Which hand-written claims are now contradicted by the data?
    #
    # Two strengths of evidence. A block that literally prints a figure that has
    # changed is wrong on its face and is reported first. A block that merely
    # names a model whose numbers moved may or may not need rewording, so it is
    # reported only when the movement is material — a 1-point pass wobble on a
    # model mentioned in passing is noise, and drowning the real hits in it
    # would make the whole report ignorable.
    lines.append("### Editorial claims to re-check")
    lines.append("")
    quoted: list[str] = []
    mentions: list[str] = []

    for label, text in prose_blocks(page):
        for name, change in sorted(moved.items()):
            if name not in text:
                continue
            stale = [f"`{s}`" for s in stale_figures(text, change["before"], change["after"])]
            if stale:
                quoted.append(f"- **{label}** prints {', '.join(stale)} for `{name}`, "
                              f"now {'; '.join(change['deltas'])}")
                quoted.append(f"  > {excerpt(text)}")
            elif material(change["before"], change["after"]):
                mentions.append(f"- **{label}** cites `{name}` — {'; '.join(change['deltas'])}")

    if quoted:
        lines.append("**Figures printed in prose that are now wrong:**")
        lines.append("")
        lines.extend(quoted)
        lines.append("")
    if mentions:
        lines.append("**Blocks naming a model that moved materially:**")
        lines.append("")
        lines.extend(sorted(set(mentions)))
        lines.append("")
    if not quoted and not mentions:
        lines.append("No prose on the page is contradicted by the new numbers.")
        lines.append("")

    # Provenance the footnotes depend on.
    gaps = [f"`{n}` ({r['_rubric_coverage']}/{r['_trials']} trials judged)"
            for n, r in sorted(new.items()) if 0 < r["_rubric_coverage"] < r["_trials"]]
    missing = [f"`{n}`" for n, r in sorted(new.items()) if r["_rubric_coverage"] == 0]
    if gaps or missing:
        lines.append("### Rubric provenance")
        lines.append("")
        if gaps:
            lines.append("Partial rubric coverage — footnote 1 applies: " + ", ".join(gaps) + ".")
        if missing:
            lines.append("No rubric at all, `rubric` emitted as null: " + ", ".join(missing) + ".")
        lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="path to featherbench results/summary.json")
    parser.add_argument("--report", type=Path, default=None, help="write the Markdown report here")
    parser.add_argument("--check", action="store_true", help="exit 1 if data.js is stale; write nothing")
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    derived = board_rows(summary)

    existing_text = DATA_JS.read_text(encoding="utf-8")
    existing, _ = parse_data_js(existing_text)
    page = PAGE.read_text(encoding="utf-8")

    report = build_report(existing, derived, page, summary)

    # Merge: derived numbers onto preserved editorial fields, board order kept.
    merged: list[dict[str, Any]] = []
    cats: list[dict[str, Any]] = []
    for model in existing:
        row = derived.get(model["name"])
        if row is None:
            merged.append(model)  # absent upstream; leave it alone and report it
            continue
        keep = {k: model[k] for k in EDITORIAL_MODEL_FIELDS if k in model}
        merged.append({**keep, **{k: v for k, v in row.items() if not k.startswith("_")}})
        cats.append({"name": model["name"], "ref": not model.get("panel", False),
                     **{k: row[k] for k in ("cv", "dv", "rv", "sv", "tv")}})

    merged.sort(key=lambda m: (-m["pass"], m["name"]))
    cats.sort(key=lambda c: [m["name"] for m in merged].index(c["name"]))

    latest = max(r["run_id"] for r in summary["records"])
    rendered = render_data_js(merged, cats, latest, summary["generated_utc"])

    if args.report:
        args.report.write_text(report, encoding="utf-8")

    if args.check:
        if rendered != existing_text:
            print(report)
            print("data.js is out of date — run without --check to regenerate.", file=sys.stderr)
            return 1
        print("data.js is up to date.")
        return 0

    DATA_JS.write_text(rendered, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
