#!/usr/bin/env python3
"""Apply title/abstract and report-level decisions to the journal hand-search."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
REGISTER = HERE / "journal-screening-register.csv"

EMPIRICAL = {
    "More than a Judge: An Empirical Study of Agent-Human Interaction in Crowdsourced Testing Assessment": (
        "ST-100",
        "moderate",
    ),
    "On Developers’ Self-Declaration of AI-Generated Code: An Analysis of Practices": (
        "ST-101",
        "moderate",
    ),
    "Understanding and Enhancing CS Students’ Interaction Experience with AI Coding Assistant Tools": (
        "ST-102",
        "moderate",
    ),
    "Unveiling the Role of ChatGPT in Software Development: Insights from Developer-ChatGPT Interactions on GitHub": (
        "ST-103",
        "moderate",
    ),
    "AI support for data scientists: An empirical study on workflow and alternative code recommendations": (
        "ST-104",
        "moderate",
    ),
    "An empirical study on developers’ shared conversations with ChatGPT in GitHub pull requests and issues": (
        "ST-105",
        "moderate",
    ),
    "How students use generative AI for software testing: An observational study": (
        "ST-106",
        "moderate",
    ),
    "What characteristics make ChatGPT effective for software issue resolution? An empirical study of task, project, and conversational signals in GitHub issues": (
        "ST-107",
        "moderate",
    ),
    "AI-Assisted Collaboration: Exploring Developer Experience with GitHub Copilot and Windsurf": (
        "ST-108",
        "low",
    ),
    "From Disruptions to Discussions: How GenAI Impacts Human Interactions in Software Development": (
        "ST-109",
        "moderate",
    ),
    "How Can ChatGPT Support Human Security Testers to Help Mitigate Supply Chain Attacks?": (
        "ST-110",
        "moderate",
    ),
    "LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation": (
        "ST-111",
        "moderate",
    ),
    "Do comments and expertise still matter? An experiment on programmers’ adoption of AI-generated JavaScript code": (
        "ST-112",
        "high",
    ),
    "Exploring the problems, their causes and solutions of AI pair programming: A study on GitHub and Stack Overflow": (
        "ST-113",
        "moderate",
    ),
    "“Will I be replaced?” Assessing ChatGPT's effect on software development and programmer perceptions of AI tools": (
        "ST-114",
        "low",
    ),
    "Is GitHub’s Copilot as bad as humans at introducing vulnerabilities in code?": (
        "ST-115",
        "moderate",
    ),
    "GitHub Copilot AI pair programmer: Asset or Liability?": (
        "ST-116",
        "moderate",
    ),
}

CONTEXTUAL = {
    "Accountability in Code Review: The Role of Intrinsic Drivers and the Impact of LLMs",
    "Engagement in Code Review: Emotional, Behavioral, and Cognitive Dimensions in Peer vs. LLM Interactions",
    "Investigating the Role of Cultural Values in Adopting Large Language Models for Software Engineering",
    "Navigating the Complexity of Generative AI Adoption in Software Engineering",
    "Continuance use of AI coding assistants among South Korean Industry Developers: A survey case study with large language models",
    "Empirical analysis of generative AI tool adoption in software development",
    "Still just personal assistants? – A multiple case study of generative AI adoption in software organizations",
    "Using AI-based coding assistants in practice: State of affairs, perceptions, and ways forward",
}

NEW_SYNTHESES = {
    "Using LLMs to enhance code quality: A systematic literature review",
    "Generative AI solutions for software quality: Assessing industrial readiness",
}

REPLACEMENT_SYNTHESES = {
    "The Impact of LLM-Assistants on Software Developer Productivity: A Systematic Review and Mapping Study",
}

FULL_TEXT_EXCLUSIONS = {
    "A Framework for Evaluating GenAI Adoption and Use in Software Engineering": (
        "Evaluates the quality of GenAI-based products rather than AI assistance in a software-development workflow"
    ),
    "Generative AI for Requirements Engineering: A Systematic Literature Review": (
        "Secondary requirements-engineering review without an extractable productivity, delivery or adjacent coding outcome"
    ),
}


def normalise(value: str) -> str:
    value = value.replace("&amp;", "&")
    return re.sub(r"\s+", " ", value).strip().casefold()


def normalised_map(values: dict[str, object] | set[str]) -> dict[str, object]:
    if isinstance(values, set):
        return {normalise(value): value for value in values}
    return {normalise(key): value for key, value in values.items()}


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    empirical = normalised_map(EMPIRICAL)
    contextual = normalised_map(CONTEXTUAL)
    new_syntheses = normalised_map(NEW_SYNTHESES)
    replacements = normalised_map(REPLACEMENT_SYNTHESES)
    exclusions = normalised_map(FULL_TEXT_EXCLUSIONS)
    sought = set(empirical) | set(contextual) | set(new_syntheses) | set(replacements) | set(exclusions)

    with REGISTER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    added_fields = [
        "human_decision",
        "title_abstract_reason",
        "full_text_decision",
        "full_text_reason",
        "study_id",
        "evidence_weight",
    ]
    for field in added_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    assessed: list[dict[str, str]] = []
    full_text: list[dict[str, str]] = []
    for row in rows:
        if row["dedupe_status"].startswith("duplicate_included"):
            row["human_decision"] = "not_screened_duplicate"
            row["title_abstract_reason"] = "Duplicate of a report already in the included corpus"
            continue

        key = normalise(row["title"])
        if key not in sought:
            row["human_decision"] = "exclude_title_abstract"
            row["title_abstract_reason"] = (
                "No eligible developer, team or repository workflow outcome indicated"
            )
            continue

        row["human_decision"] = "seek_full_text"
        row["title_abstract_reason"] = "Potentially eligible developer, team or repository evidence"
        full_text.append(row)

        if key in empirical:
            study_id, evidence_weight = empirical[key]
            row["full_text_decision"] = "include_adjacent"
            row["full_text_reason"] = (
                "Primary study of review, quality, security, skills, adoption or interaction"
            )
            row["study_id"] = str(study_id)
            row["evidence_weight"] = str(evidence_weight)
        elif key in contextual:
            row["full_text_decision"] = "include_contextual"
            row["full_text_reason"] = (
                "Survey or qualitative evidence retained to interpret adoption and workflow context"
            )
        elif key in new_syntheses:
            row["full_text_decision"] = "include_secondary_synthesis"
            row["full_text_reason"] = "Eligible secondary synthesis of quality evidence"
        elif key in replacements:
            row["full_text_decision"] = "replace_existing_synthesis"
            row["full_text_reason"] = (
                "Peer-reviewed journal version replaces the included preprint"
            )
        else:
            row["full_text_decision"] = "exclude_full_text"
            row["full_text_reason"] = str(exclusions[key])
        assessed.append(row)

    write_csv(REGISTER, rows, fieldnames)
    write_csv(HERE / "journal-full-text-candidates.csv", full_text, fieldnames)
    write_csv(HERE / "journal-report-assessments.csv", assessed, fieldnames)

    summary_path = HERE / "journal-search-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary.pop("unique_records_screened", None)
    summary.update(
        {
            "records_screened_or_reassessed": sum(
                row["human_decision"] != "not_screened_duplicate" for row in rows
            ),
            "title_abstract_exclusions": sum(
                row["human_decision"] == "exclude_title_abstract" for row in rows
            ),
            "reports_assessed": len(assessed),
            "included_new_empirical_studies": sum(
                row["full_text_decision"] == "include_adjacent" for row in assessed
            ),
            "included_new_secondary_syntheses": sum(
                row["full_text_decision"] == "include_secondary_synthesis"
                for row in assessed
            ),
            "included_new_contextual_documents": sum(
                row["full_text_decision"] == "include_contextual" for row in assessed
            ),
            "replacement_reports": sum(
                row["full_text_decision"] == "replace_existing_synthesis"
                for row in assessed
            ),
            "full_text_exclusions": sum(
                row["full_text_decision"] == "exclude_full_text" for row in assessed
            ),
        }
    )
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    combined_path = HERE / "search-summary.json"
    combined = json.loads(combined_path.read_text(encoding="utf-8"))
    combined.pop("updated_confidence", None)
    combined.pop("initial_corpus_retrieval_attribution", None)
    combined["journal_search_update"] = summary
    combined.update(
        {
            "agentic_retrieval_source_breakdown": {
                "arXiv": 40,
                "ACM": 14,
                "Other web/publisher": 61,
            },
            "total_new_source_documents_included": 66,
            "updated_source_documents": 181,
            "updated_empirical_studies": 116,
            "updated_productivity_studies": 44,
            "updated_adjacent_studies": 72,
            "updated_productivity_effect_estimates": 46,
            "updated_secondary_syntheses": 4,
            "updated_contextual_documents": 61,
        }
    )
    combined_path.write_text(json.dumps(combined, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
