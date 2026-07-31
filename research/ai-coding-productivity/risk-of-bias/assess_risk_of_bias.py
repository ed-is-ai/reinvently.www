#!/usr/bin/env python3
"""Generate the formal risk-of-bias register for the AI coding review.

The register contains one assessment per empirical study. Productivity studies
retain links to all applicable effect estimates, while adjacent-outcome studies
identify the primary outcome family cited in the review. Risk of bias remains
separate from the review's broader evidence-weight grade.
"""

from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTICLE = ROOT / "blog/ai-coding-productivity-evidence/index.html"
OUT_DIR = Path(__file__).resolve().parent
ASSESSMENT_DATE = date(2026, 7, 29).isoformat()


ROB2 = {1, 2, 4, 9, 10, 23, 48, 52, 56, 58}
ROBINS_I = {11, 12, 13, 14, 15, 16, 17, 18, 22, 24, 34, 35, 36, 37, 46, 49, 57, 93}
JBI_QUASI = {3, 5, 6, 7, 8, 19, 20, 27, 28, 32, 54, 70, 86, 94}
JBI_ANALYTICAL = {
    25, 30, 33, 41, 42, 43, 44, 45, 47, 50, 51, 59, 60, 61, 63, 66,
    72, 73, 77, 78, 80, 82, 83, 84, 85, 89, 91, 95, 96, 97, 99,
}
JBI_CASE_BENCHMARK = {
    21, 26, 29, 31, 38, 39, 40, 53, 55, 62, 64, 65, 67, 68, 69,
    71, 74, 75, 76, 79, 81, 87, 88, 90, 92, 98,
}


def p(overall: str, rationale: str, *domains: tuple[str, str]) -> dict:
    return {"overall": overall, "rationale": rationale, "domains": domains}


PROFILES = {
    "rob2_some": p(
        "Some concerns",
        "Random allocation supports comparability, but open-label tool use and incomplete information about prespecified analysis leave residual concerns.",
        ("Randomisation process", "Low"),
        ("Deviations from intended intervention", "Some concerns"),
        ("Missing outcome data", "Low"),
        ("Outcome measurement", "Low"),
        ("Selection of reported result", "Some concerns"),
    ),
    "rob2_some_missing": p(
        "Some concerns",
        "Random allocation is credible, but attrition, diary completion or incomplete outcome capture could differ by condition; selective-reporting information is limited.",
        ("Randomisation process", "Low"),
        ("Deviations from intended intervention", "Some concerns"),
        ("Missing outcome data", "Some concerns"),
        ("Outcome measurement", "Some concerns"),
        ("Selection of reported result", "Some concerns"),
    ),
    "rob2_high": p(
        "High",
        "The crossover comparison is vulnerable to carry-over and differential tool use, while missingness and outcome interpretation could materially change the result.",
        ("Randomisation process", "Some concerns"),
        ("Deviations from intended intervention", "High"),
        ("Missing outcome data", "Some concerns"),
        ("Outcome measurement", "Some concerns"),
        ("Selection of reported result", "Some concerns"),
    ),
    "robins_moderate": p(
        "Moderate",
        "The quasi-experimental discontinuity or matching strategy addresses major baseline differences, but residual confounding and analysis-selection risk remain.",
        ("Confounding", "Moderate"),
        ("Classification of intervention", "Low"),
        ("Selection into study", "Moderate"),
        ("Missing data", "Low"),
        ("Outcome measurement", "Low"),
        ("Selection of reported result", "Moderate"),
    ),
    "robins_serious": p(
        "Serious",
        "AI adoption was not random. Self-selection, concurrent process changes and differences between adopters and controls could explain a material part of the observed association.",
        ("Confounding", "Serious"),
        ("Classification of intervention", "Moderate"),
        ("Selection into study", "Serious"),
        ("Missing data", "Moderate"),
        ("Outcome measurement", "Moderate"),
        ("Selection of reported result", "Moderate"),
    ),
    "robins_serious_measurement": p(
        "Serious",
        "Non-random adoption and an inferred or indirect AI-exposure measure create serious confounding and classification risk, despite large-scale outcome telemetry.",
        ("Confounding", "Serious"),
        ("Classification of intervention", "Serious"),
        ("Selection into study", "Moderate"),
        ("Missing data", "Moderate"),
        ("Outcome measurement", "Moderate"),
        ("Selection of reported result", "Moderate"),
    ),
    "jbi_quasi_some": p(
        "Some concerns",
        "The intervention precedes the measured outcome and a comparator is present, but allocation concealment, follow-up completeness or repeated pre/post measurement is unclear.",
        ("Cause and effect clear", "Yes"),
        ("Participants compared similarly", "Unclear"),
        ("Control group present", "Yes"),
        ("Repeated pre/post measures", "Unclear"),
        ("Follow-up complete", "Unclear"),
        ("Outcomes measured similarly", "Yes"),
        ("Outcomes measured reliably", "Yes"),
        ("Analysis appropriate", "Yes"),
    ),
    "jbi_quasi_high": p(
        "High",
        "The comparison is weakly controlled or materially confounded, and incomplete reporting prevents the observed difference from being attributed securely to AI assistance.",
        ("Cause and effect clear", "Yes"),
        ("Participants compared similarly", "No"),
        ("Control group present", "Unclear"),
        ("Repeated pre/post measures", "No"),
        ("Follow-up complete", "Unclear"),
        ("Outcomes measured similarly", "Yes"),
        ("Outcomes measured reliably", "Unclear"),
        ("Analysis appropriate", "Unclear"),
    ),
    "jbi_analytical_some": p(
        "Some concerns",
        "The sample and measured outcome are suitable for a descriptive association, but exposure classification, unmeasured confounding or incomplete repository coverage limits causal interpretation.",
        ("Inclusion criteria defined", "Yes"),
        ("Setting and sample described", "Yes"),
        ("Exposure measured validly", "Unclear"),
        ("Confounders identified", "Unclear"),
        ("Confounders addressed", "Unclear"),
        ("Outcome measured validly", "Yes"),
        ("Analysis appropriate", "Yes"),
        ("Reporting sufficiently complete", "Unclear"),
    ),
    "jbi_analytical_high": p(
        "High",
        "A small, selected or self-reported sample and limited control of confounding make the measured association vulnerable to substantial selection and measurement bias.",
        ("Inclusion criteria defined", "Unclear"),
        ("Setting and sample described", "Yes"),
        ("Exposure measured validly", "Unclear"),
        ("Confounders identified", "Unclear"),
        ("Confounders addressed", "No"),
        ("Outcome measured validly", "Unclear"),
        ("Analysis appropriate", "Unclear"),
        ("Reporting sufficiently complete", "Unclear"),
    ),
    "jbi_case_some": p(
        "Some concerns",
        "The benchmark or case defines its inputs and measured outputs, but prompt selection, reference validity and selective reporting constrain generalisation beyond the evaluated setting.",
        ("Case or benchmark criteria clear", "Yes"),
        ("Inputs and setting described", "Yes"),
        ("Intervention or model identified", "Yes"),
        ("Reference standard credible", "Unclear"),
        ("Runs or cases consecutive/complete", "Unclear"),
        ("Outcomes measured consistently", "Yes"),
        ("Failures and exclusions reported", "Unclear"),
        ("Analysis appropriate", "Yes"),
        ("Selective reporting addressed", "Unclear"),
        ("Generalisability bounded", "Yes"),
    ),
    "jbi_case_high": p(
        "High",
        "This is a selected organisational case, small demonstration or repeated single-operator comparison without a concurrent control. Attribution and selective-reporting risks are substantial.",
        ("Case or benchmark criteria clear", "Unclear"),
        ("Inputs and setting described", "Yes"),
        ("Intervention or model identified", "Yes"),
        ("Reference standard credible", "No"),
        ("Runs or cases consecutive/complete", "Unclear"),
        ("Outcomes measured consistently", "Unclear"),
        ("Failures and exclusions reported", "No"),
        ("Analysis appropriate", "Unclear"),
        ("Selective reporting addressed", "No"),
        ("Generalisability bounded", "Yes"),
    ),
}


PROFILE_IDS = {
    "rob2_some": {1, 2, 4, 10, 23, 48, 52, 56},
    "rob2_some_missing": {58},
    "rob2_high": {9},
    "robins_moderate": {13, 46},
    "robins_serious": {11, 14, 15, 16, 17, 18, 22, 24, 34, 35, 36, 37, 49, 57, 93},
    "robins_serious_measurement": {12},
    "jbi_quasi_some": {3, 6, 7, 8, 19, 20, 27, 54, 94},
    "jbi_quasi_high": {5, 28, 32, 70, 86},
    "jbi_analytical_some": {
        25, 33, 41, 42, 43, 44, 45, 47, 50, 51, 59, 61, 63, 72, 78,
        80, 85, 91, 96, 97, 99,
    },
    "jbi_analytical_high": {30, 60, 66, 73, 77, 82, 83, 84, 89, 95},
    "jbi_case_some": {53, 55, 65, 67, 68, 71, 76, 79, 87, 88, 92, 98},
    "jbi_case_high": {21, 26, 29, 31, 38, 39, 40, 62, 64, 69, 74, 75, 81, 90},
}


NOTES = {
    1: "The objective time outcome is direct, but the small field sample produces imprecision rather than additional bias.",
    2: "Three company experiments improve replication; treatment awareness and company-specific implementation can still affect behaviour.",
    4: "Randomised task allocation is strong, although participants could not be blinded and estimated task time is partly behavioural.",
    9: "The source itself reports high risk of bias; crossover carry-over and condition adherence are material concerns.",
    11: "Matching cannot eliminate differences in adoption timing, developer motivation, project maturity or concurrent tooling.",
    12: "AI authorship is inferred from public code, so exposure misclassification compounds non-random tool use.",
    14: "Synthetic controls improve the counterfactual, but adoption is inferred and integration changes may have other causes.",
    15: "Matched difference-in-differences depends on parallel trends and accurate adoption timing.",
    16: "A time discontinuity can be affected by concurrent organisational changes at deployment.",
    17: "The natural experiment compares ecosystems that may differ independently of Copilot availability.",
    18: "The field setting is valuable, but treatment users were identified and paired with comparable controls rather than randomly assigned.",
    22: "Repository adoption is selected and the persistent quality outcomes can be affected by changing task mix.",
    29: "Two disclosed organisational estimates use different workflows and both lack a concurrent external comparator.",
    31: "Two frontier-team estimates are retained as separate targets, but case selection and counterfactual baselines are not independently auditable.",
    34: "Vendor telemetry is broad, but customer selection and unmeasured organisational maturity can drive both adoption and performance.",
    35: "The longitudinal vendor dataset is useful for association, not isolated causal attribution.",
    36: "Customer telemetry and survey linkage leave residual selection, exposure and outcome-definition risk.",
    37: "Observed companies differ in adoption intensity and engineering systems; residual confounding is substantial.",
    48: "Randomisation supports the bounded quality result, but the public report does not expose a complete prespecified analysis record.",
    52: "Randomised safety trials are appraised for the trial result cited; the later production experiment is interpreted separately as observational evidence.",
    58: "Randomisation is strong, while diary completion and self-reported productivity create missingness and measurement concerns.",
    69: "One developer repeated tool-specific builds without a manual baseline.",
    70: "AI access is confounded with programming experience, so group differences cannot isolate the tool effect.",
    86: "The small student sample and censoring materially affect the reported time comparison.",
    93: "Phased rollout provides temporal variation, but seniority, adoption and team spillovers remain non-random.",
}


INSTRUMENTS = {
    "RoB 2": ("RoB 2", "22 August 2019"),
    "ROBINS-I": ("ROBINS-I V2", "draft, 20 November 2025"),
    "JBI quasi": ("JBI quasi-experimental checklist with prespecified overall-risk rule", "2024"),
    "JBI analytical": ("JBI analytical cross-sectional/cohort checklist with prespecified overall-risk rule", "2025–2026"),
    "JBI case": ("JBI-derived software benchmark/case checklist with prespecified overall-risk rule", "2020–2026 tools"),
}


def clean(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(fragment).split())


def extract_studies(source: str) -> dict[int, dict[str, str]]:
    section = source.split("<h3>A. Included empirical studies (99)</h3>", 1)[1].split("</details>", 1)[0]
    matches = re.findall(
        r'<li><code>ST-(\d+)</code> — <a href="([^"]+)">(.*?)</a>(.*?)</li>',
        section,
        re.S,
    )
    studies = {}
    for raw_id, url, title, note in matches:
        studies[int(raw_id)] = {
            "study_id": f"ST-{int(raw_id):02d}",
            "title": clean(title),
            "url": url,
            "register_note": clean(note).strip(" —."),
        }
    return studies


def extract_effects(source: str) -> list[dict[str, str]]:
    section = source.split('<h2 id="effect-register"', 1)[1].split("</table>", 1)[0]
    effects = []
    for raw_effect, row in re.findall(r'<tr id="E-(\d+)">(.*?)</tr>', section, re.S):
        cells = re.findall(r"<td(?: [^>]*)?>(.*?)</td>", row, re.S)
        study_match = re.search(r"ST-(\d+)", cells[0])
        if not study_match:
            raise ValueError(f"No study identifier for E-{raw_effect}")
        effects.append(
            {
                "effect_id": f"E-{int(raw_effect):02d}",
                "study_number": int(study_match.group(1)),
                "target_result": f"{clean(cells[1])}; reported effect: {clean(cells[3])}",
            }
        )
    return effects


def profile_for(study_number: int) -> tuple[str, dict]:
    matches = [name for name, ids in PROFILE_IDS.items() if study_number in ids]
    if len(matches) != 1:
        raise ValueError(f"ST-{study_number:02d} has {len(matches)} profiles: {matches}")
    name = matches[0]
    return name, PROFILES[name]


def instrument_for(study_number: int) -> tuple[str, str, str]:
    if study_number in ROB2:
        key = "RoB 2"
    elif study_number in ROBINS_I:
        key = "ROBINS-I"
    elif study_number in JBI_QUASI:
        key = "JBI quasi"
    elif study_number in JBI_ANALYTICAL:
        key = "JBI analytical"
    elif study_number in JBI_CASE_BENCHMARK:
        key = "JBI case"
    else:
        raise ValueError(f"ST-{study_number:02d} has no instrument")
    name, version = INSTRUMENTS[key]
    return key, name, version


def main() -> None:
    source = ARTICLE.read_text(encoding="utf-8")
    studies = extract_studies(source)
    effects = extract_effects(source)

    routed = ROB2 | ROBINS_I | JBI_QUASI | JBI_ANALYTICAL | JBI_CASE_BENCHMARK
    profiled = set().union(*PROFILE_IDS.values())
    expected = set(range(1, 100))
    assert set(studies) == expected
    assert routed == expected
    assert profiled == expected
    assert len(effects) == 46

    effects_by_study = defaultdict(list)
    for effect in effects:
        effects_by_study[effect["study_number"]].append(effect)
    productivity_studies = set(effects_by_study)

    rows = []
    for number in range(1, 100):
        study = studies[number]
        targets = effects_by_study[number]
        effect_ids = "; ".join(target["effect_id"] for target in targets)
        target_result = (
            " | ".join(target["target_result"] for target in targets)
            if targets
            else "Primary adjacent outcome family cited in the review"
        )
        profile_name, profile = profile_for(number)
        instrument_key, instrument, version = instrument_for(number)
        row = {
            "assessment_id": f"RB-{study['study_id']}",
            "study_id": study["study_id"],
            "effect_ids": effect_ids,
            "evidence_stream": "productivity/delivery" if targets else "adjacent outcome",
            "title": study["title"],
            "url": study["url"],
            "target_results": target_result,
            "instrument": instrument,
            "instrument_version": version,
            "profile": profile_name,
            "overall_risk_of_bias": profile["overall"],
            "study_specific_note": NOTES.get(number, study["register_note"]),
            "decision_rationale": profile["rationale"],
            "appraisal_basis": "Linked report and methods/results information available to the single AI-assisted reviewer",
            "assessor": "Single AI-assisted reviewer; not independently duplicated",
            "assessment_date": ASSESSMENT_DATE,
        }
        for index in range(1, 11):
            row[f"domain_{index}"] = ""
        for index, (label, judgement) in enumerate(profile["domains"], start=1):
            row[f"domain_{index}"] = f"{label}: {judgement}"
        row["_instrument_key"] = instrument_key
        rows.append(row)

    assert len(rows) == len(studies) == 99

    fieldnames = [
        "assessment_id", "study_id", "effect_ids", "evidence_stream", "title",
        "url", "target_results", "instrument", "instrument_version", "profile",
        *[f"domain_{index}" for index in range(1, 11)],
        "overall_risk_of_bias", "study_specific_note", "decision_rationale",
        "appraisal_basis", "assessor", "assessment_date",
    ]
    with (OUT_DIR / "risk-of-bias-register.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})

    study_summary = Counter()
    for row in rows:
        study_summary[(row["_instrument_key"], row["overall_risk_of_bias"])] += 1

    summary = {
        "assessment_date": ASSESSMENT_DATE,
        "empirical_studies": len(studies),
        "study_level_assessments": len(rows),
        "productivity_effect_estimates": len(effects),
        "adjacent_outcome_studies": len(studies) - len(productivity_studies),
        "independent_duplicate_appraisal": False,
        "study_level_counts": {
            instrument: dict(sorted(
                ((risk, count) for (name, risk), count in study_summary.items() if name == instrument),
                key=lambda item: item[0],
            ))
            for instrument in INSTRUMENTS
        },
    }
    (OUT_DIR / "risk-of-bias-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
