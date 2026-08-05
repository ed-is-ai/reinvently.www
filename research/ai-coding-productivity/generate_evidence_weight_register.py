#!/usr/bin/env python3
"""Generate the canonical study-level evidence-weight register.

This consolidates grades that were previously distributed across the
productivity effect audit, the original 59-study appraisal, the OpenAlex
screening update and the direct-journal screening update. It does not
reappraise studies.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTICLE = HERE.parents[1] / "blog" / "ai-coding-productivity-evidence" / "index.html"
RISK_REGISTER = HERE / "risk-of-bias" / "risk-of-bias-register.csv"
OPERATING_MODEL_AUDIT = HERE / "operating-model-audit.csv"
OPENALEX_ASSESSMENTS = HERE / "prisma" / "report-assessments.csv"
JOURNAL_ASSESSMENTS = HERE / "prisma" / "journal-report-assessments.csv"
SEARCH_SUMMARY = HERE / "prisma" / "search-summary.json"
OUTPUT = HERE / "evidence-weight-register.csv"
ASSESSMENT_DATE = date(2026, 8, 4).isoformat()

VALID_WEIGHTS = {"high", "moderate", "low"}
PRODUCTIVITY_WEIGHT_MAP = {"high": "high", "medium": "moderate", "low": "low"}

# The original 59-study synthesis reported 11 high, 35 moderate and 13 low
# studies. Its 40 productivity studies account for 8 high, 19 moderate and
# 13 low grades. The remaining three high grades were the controlled adjacent
# studies below; the other 16 original adjacent studies were moderate.
INITIAL_ADJACENT_HIGH = {"ST-48", "ST-52", "ST-56"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def study_number(study_id: str) -> int:
    return int(study_id.split("-")[1])


def weight_basis(weight: str, stream: str) -> str:
    if stream == "productivity/delivery":
        return (
            "Study-level grade inherited from the linked productivity effects; "
            "all effects from this study carry the same grade."
        )
    if weight == "high":
        return (
            "Controlled primary adjacent outcome with a credible comparator, "
            "direct measure and no identified material limitation likely to "
            "reverse the interpretation."
        )
    if weight == "moderate":
        return (
            "Useful comparative or directly measured adjacent evidence with "
            "residual bias, confounding, indirectness or precision limitations."
        )
    return (
        "Weakly controlled, self-reported or descriptive adjacent evidence with "
        "material attribution, directness or precision limitations."
    )


def main() -> None:
    risk_rows = read_csv(RISK_REGISTER)
    operating_rows = read_csv(OPERATING_MODEL_AUDIT)
    openalex_rows = read_csv(OPENALEX_ASSESSMENTS)
    journal_rows = read_csv(JOURNAL_ASSESSMENTS)

    if len(risk_rows) != 116:
        raise ValueError(f"Expected 116 risk rows, found {len(risk_rows)}")
    risk_by_study = {row["study_id"]: row for row in risk_rows}
    if len(risk_by_study) != len(risk_rows):
        raise ValueError("Risk-of-bias register contains duplicate study IDs")

    effects_by_study: dict[str, list[str]] = defaultdict(list)
    productivity_weights: dict[str, set[str]] = defaultdict(set)
    for row in operating_rows:
        study_id = row["study_id"]
        effects_by_study[study_id].append(row["effect_id"])
        productivity_weights[study_id].add(
            PRODUCTIVITY_WEIGHT_MAP[row["evidence_weight"]]
        )
    inconsistent = {
        study_id: weights
        for study_id, weights in productivity_weights.items()
        if len(weights) != 1
    }
    if inconsistent:
        raise ValueError(f"Studies have inconsistent effect grades: {inconsistent}")

    grades: dict[str, tuple[str, str]] = {}
    for study_id, weights in productivity_weights.items():
        grades[study_id] = (
            next(iter(weights)),
            "operating-model-audit.csv",
        )

    for number in range(41, 60):
        study_id = f"ST-{number:02d}"
        grades[study_id] = (
            "high" if study_id in INITIAL_ADJACENT_HIGH else "moderate",
            "original 59-study evidence appraisal",
        )

    for source_name, source_rows in (
        ("prisma/report-assessments.csv", openalex_rows),
        ("prisma/journal-report-assessments.csv", journal_rows),
    ):
        for row in source_rows:
            study_id = row.get("study_id", "").strip()
            weight = (
                row.get("confidence", "").strip()
                or row.get("evidence_weight", "").strip()
            ).lower()
            if not study_id or study_id in productivity_weights:
                continue
            if weight not in VALID_WEIGHTS:
                continue
            existing = grades.get(study_id)
            if existing and existing[0] != weight:
                raise ValueError(
                    f"{study_id} has conflicting grades: {existing[0]} and {weight}"
                )
            grades[study_id] = (weight, source_name)

    missing = sorted(set(risk_by_study) - set(grades), key=study_number)
    unexpected = sorted(set(grades) - set(risk_by_study), key=study_number)
    if missing or unexpected:
        raise ValueError(
            f"Evidence-weight coverage mismatch; missing={missing}, "
            f"unexpected={unexpected}"
        )

    rows = []
    for study_id in sorted(risk_by_study, key=study_number):
        risk = risk_by_study[study_id]
        weight, grade_source = grades[study_id]
        stream = risk["evidence_stream"]
        rows.append(
            {
                "study_id": study_id,
                "title": risk["title"],
                "effect_ids": "; ".join(effects_by_study.get(study_id, [])),
                "evidence_stream": stream,
                "evidence_weight": weight,
                "overall_risk_of_bias": risk["overall_risk_of_bias"],
                "appraisal_instrument": risk["instrument"],
                "weight_basis": weight_basis(weight, stream),
                "main_limitation": risk["study_specific_note"]
                or risk["decision_rationale"],
                "grade_source": grade_source,
                "assessment_date": ASSESSMENT_DATE,
            }
        )

    totals = Counter(row["evidence_weight"] for row in rows)
    expected_totals = {"high": 12, "moderate": 77, "low": 27}
    if dict(totals) != expected_totals:
        raise ValueError(
            f"Evidence-weight totals changed: {dict(totals)}; "
            f"expected {expected_totals}"
        )

    fieldnames = [
        "study_id",
        "title",
        "effect_ids",
        "evidence_stream",
        "evidence_weight",
        "overall_risk_of_bias",
        "appraisal_instrument",
        "weight_basis",
        "main_limitation",
        "grade_source",
        "assessment_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = json.loads(SEARCH_SUMMARY.read_text(encoding="utf-8"))
    summary["updated_evidence_weight"] = {
        weight: totals[weight] for weight in ("high", "moderate", "low")
    }
    SEARCH_SUMMARY.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )

    article = ARTICLE.read_text(encoding="utf-8")
    article_totals = {
        weight.lower(): int(count)
        for weight, count in re.findall(
            r'<td class="(?:high|medium|low)">'
            r"(High|Moderate|Low)</td><td>(\d+)</td>",
            article,
        )
    }
    if article_totals != expected_totals:
        raise ValueError(
            f"Article evidence-weight table is {article_totals}; "
            f"expected {expected_totals}"
        )

    print(
        f"Wrote {len(rows)} study-level grades to {OUTPUT.relative_to(HERE.parent.parent)}"
    )
    print(
        "Evidence weight: "
        + ", ".join(f"{weight}={totals[weight]}" for weight in ("high", "moderate", "low"))
    )


if __name__ == "__main__":
    main()
