#!/usr/bin/env python3
"""Record the report-level eligibility assessment and assign stable review IDs."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
REGISTER = HERE / "screening-register.csv"


PRODUCTIVITY = {
    "Building web applications with AI: a comparative study": ("low", "E-43"),
    "Can generative AI bridge the gap? A quasi-experimental study of non-programmers with AI vs. programmers without AI": (
        "moderate",
        "E-44",
    ),
    "How far are AI-powered programming assistants from meeting developers' needs?": (
        "low",
        "E-45",
    ),
    "Seniority, Spillovers, and AI-Enhanced Code Contributions: Evidence from a Major Enterprise": (
        "moderate",
        "E-46",
    ),
}

ADJACENT_LOW = {
    "AI based software re-engineering : case AQUATOX",
    "Der Einfluss KI-basierter Programmierassistenten auf die Zusammenarbeit in Softwareentwicklungsteams",
    "Domain ambiguity in AI-assistedsoftware development : A controlled study of how an AI agent handlesinconsistent business-domain context",
    "En jämförande säkerhetsutvärdering av manuell och AI-assisterad utveckling av webbapplikationer",
    "Evaluating AI-Generated T-SQL Code Review Reports in an Enterprise-Scale Codebase",
    "Exploring and modelling human-AI collaboration effectiveness in software engineering using behavioural analysis and machine learning",
    "From Meeting to Pull Request : An End-to-End Evaluation of LLM-Based Software Development Automation",
    "From Specifications to Implementation in the Gen-AI Era: Lessons from a Project-Based Software Engineering Course",
    "GitHub Copilot Developer Experience: A Study Comparing Novice and Experienced Developers' Perspectives",
    "Multi-Simulation as Labor Compression: A Solo Operator Ships a Concurrency-Robust Product in One Session — An Experience Report",
}

ADJACENT_MODERATE = {
    "A Study of Library Usage in Agent-Authored Pull Requests",
    "AgenticFlict: A Large-Scale Dataset of Merge Conflicts in AI Coding Agent Pull Requests on GitHub",
    "Agentic AI-Driven Developer Experience for Telecom Capabilities",
    "Agentic Much? Adoption of Coding Agents on GitHub",
    "An Empirical Study: Leveraging Prompt Engineering with AI Coding Assistants to Develop Energy-Efficient Code (2025)",
    "Analyzing Developer Use of ChatGPT Generated Code in Open Source GitHub Projects",
    "Artificially Insecure: Examining GitHub Copilot’s AI-based Vulnerability Prevention System",
    "Assessing GitHub Copilot in Solidity Development: Capabilities, Testing, and Bug Fixing",
    "Can LLMs Generate Higher Quality Code Than Humans? An Empirical Study",
    "Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests",
    "Disrupting Test Development with AI Assistants",
    "Exploring the Challenges and Opportunities of AI-assisted Codebase Generation",
    "Fork-Triggerable AI Coding Agents in CI: A Wide-Net Survey",
    "From Developer Pairs to AI Copilots: A Comparative Study on Knowledge Transfer",
    "From Preventive to Reactive: How AI Coding Assistants Transform Developers' Security Awareness",
    "How Do Developers Interact with AI? An Exploratory Study on Modeling Developer Programming Behavior",
    "How Safe Are AI-Generated Patches? A Large-scale Study on Security Risks in LLM and Agentic Automated Program Repair on SWE-bench",
    "Human-Written vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and Complexity",
    "LLM impact on BLV programming",
    "On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub",
    "Security Weaknesses in LLM-Generated Source Code: An Empirical Vulnerability Analysis of Iterative AI-Assisted Development v1.0",
    "Tab to Autocomplete: The Effects of AI Coding Assistants on Web Accessibility",
    "The Impact of Generative AI Coding Assistants on Developers Who Are Visually Impaired",
    "Understanding and Predicting Accepted Code Suggestions in AI-Assisted Programming",
    "What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests",
}

SECONDARY: set[str] = set()

UPGRADE_EXISTING = {
    "Self-Admitted GenAI Usage in Open-Source Software",
}

EXTRA_STUDY_IDS = {
    "AgenticFlict: A Large-Scale Dataset of Merge Conflicts in AI Coding Agent Pull Requests on GitHub": "ST-97",
    "Evaluating AI-Generated T-SQL Code Review Reports in an Enterprise-Scale Codebase": "ST-98",
    "What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests": "ST-99",
}

DUPLICATES = {
    "Disrupting Test Development with AI Assistants: Building the Base of the Test Pyramid with Three AI Coding Assistants": (
        "Earlier report of the included conference paper"
    ),
    "Is Agentic Code Review Helpful? Mining Developers' Feedback to CodeRabbit Reviews in the Wild": (
        "Replication package for existing study ST-42"
    ),
}

EXCLUSIONS = {
    "A Survey of Vibe Coding with Large Language Models": (
        "Broad secondary survey without an extractable synthesis of measured productivity"
    ),
    "A Small-scale Exploratory Study of Static Code Analysis in AI-Assisted Software Development : Developer Perceptions, Expectations, and Adoption Challenges": (
        "Qualitative interview study; retained only as potential context"
    ),
    "Agent-Driven Design & Development: An Empirical Study of Solo Developer Productivity with LLM Coding Agents": (
        "No productivity baseline or comparator"
    ),
    "AI-assisted Software Development in Digital Dentistry: A Technical Innovation Report with Three Open-Source Applications": (
        "Technical case report without a baseline or comparator"
    ),
    "AI-Enhanced Unit Testing with xUnit: Optimizing Test Creation through GitHub Copilot": (
        "No inspectable quantitative comparison"
    ),
    "Architectural Entropy in AI-Assisted Software Development": (
        "Experience report without a measured comparative outcome"
    ),
    "Can You Trust Your Copilot? A Privacy Scorecard for AI Coding Assistants": (
        "Policy comparison rather than a development-workflow outcome"
    ),
    "Chatting with AI: Deciphering Developer Conversations with ChatGPT": (
        "Descriptive conversation taxonomy without an eligible outcome"
    ),
    "Cognitive Apprenticeship and Artificial Intelligence Coding Assistants": (
        "Non-empirical conceptual chapter"
    ),
    "Developer Experiences with a Contextualized AI Coding Assistant: Usability, Expectations, and Outcomes": (
        "Self-reported effects without a baseline or comparator"
    ),
    "Developer Perceptions on the Maintainability of AI-generated Code : A Survey-based Study": (
        "Survey evidence; contextual only under the eligibility rules"
    ),
    "DevGPT: Studying Developer-ChatGPT Conversations": (
        "Dataset description without an eligible measured outcome"
    ),
    "Evaluating the Educational Benefits and Risks of AI Coding Assistants Among Novice Programming Students in Sri Lanka": (
        "Survey evidence; contextual only under the eligibility rules"
    ),
    "Experience with GitHub Copilot for Developer Productivity at Zoominfo": (
        "Acceptance telemetry and self-report without a productivity comparator"
    ),
    "Exploring Ethical Awareness and Practices in Software Development : Study of AI Coding Assistant Tools Usage Among Developers": (
        "Qualitative interview study; contextual only"
    ),
    "From Problem Solving to Output Validation: Breakdowns in Thinking and Work Practices in AI-Assisted Software Development": (
        "Qualitative evidence; contextual only"
    ),
    "Good Vibrations? A Qualitative Study of Co-Creation, Communication, Flow, and Trust in Vibe Coding": (
        "Qualitative evidence; contextual only"
    ),
    "Insecure by design? A human-centric security perspective on AI-assisted software development": (
        "Non-empirical briefing paper"
    ),
    "Limitations and improvements of context for GitHub Copilot in professional software development": (
        "Literature-based thesis without a primary empirical evaluation"
    ),
    "\"My productivity is boosted, but ...\" Demystifying Users' Perception on AI Coding Assistants": (
        "User-review perception study; contextual only"
    ),
    "Psychological Ownership in AI-Assisted Software Development: A Qualitative Study of Developer’s Authorship, Responsibility and Cognitive Engagement in Collaborative Projects": (
        "Qualitative interview study; contextual only"
    ),
    "Shifting Roles And Emerging Competencies in Ai-Assisted Software Development : A Qualitative Study of Professional Developers": (
        "Qualitative interview study; contextual only"
    ),
    "The Influence of AI Code Assistants on Programming Learning : A Descriptive Study of Student Dependence": (
        "Descriptive survey; contextual only"
    ),
    "The Invisible Bottom Line : How GitHub Copilot Reshapes Decision-Making and Operational Workflows in Energy Trading Operations": (
        "Qualitative case study without a measured comparative outcome"
    ),
    "The New Developer: AI Skill Threat, Identity Change &amp;amp; Developer Thriving in the Transition to AI-Assisted Software Development": (
        "Survey evidence; contextual only under the eligibility rules"
    ),
    "\"Trusting the Pipeline, Not the AI\": Agency and Adoption in AI-Assisted Software Development": (
        "Qualitative interview study; contextual only"
    ),
    "\"You're on a bicycle with a little motor\": Benefits and Challenges of Using AI Code Assistants": (
        "Qualitative interview study; contextual only"
    ),
}


def normalise(value: str) -> str:
    value = value.replace("&amp;amp;", "&").replace("&amp;", "&")
    return re.sub(r"\s+", " ", value).strip().casefold()


def normalised_map(values: dict[str, object] | set[str]) -> dict[str, object]:
    if isinstance(values, set):
        return {normalise(value): value for value in values}
    return {normalise(key): value for key, value in values.items()}


def main() -> None:
    product = normalised_map(PRODUCTIVITY)
    adjacent_low = normalised_map(ADJACENT_LOW)
    adjacent_moderate = normalised_map(ADJACENT_MODERATE)
    secondary = normalised_map(SECONDARY)
    upgrades = normalised_map(UPGRADE_EXISTING)
    extra_study_ids = normalised_map(EXTRA_STUDY_IDS)
    duplicates = normalised_map(DUPLICATES)
    exclusions = normalised_map(EXCLUSIONS)

    with REGISTER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    added_fields = [
        "full_text_decision",
        "full_text_reason",
        "study_id",
        "estimate_id",
        "confidence",
    ]
    for field in added_fields:
        if field not in fieldnames:
            fieldnames.append(field)

    study_number = 61
    assessed: list[dict[str, str]] = []
    for row in rows:
        if row["human_decision"] != "seek_full_text":
            continue

        key = normalise(row["title"])
        row.update(
            {
                "full_text_decision": "",
                "full_text_reason": "",
                "study_id": "",
                "estimate_id": "",
                "confidence": "",
            }
        )

        if key in product:
            confidence, estimate_id = product[key]
            row["full_text_decision"] = "include_productivity"
            row["full_text_reason"] = (
                "Quantitative development outcome with a baseline or comparator"
            )
            row["study_id"] = str(
                extra_study_ids.get(key, f"ST-{study_number:02d}")
            )
            row["estimate_id"] = estimate_id
            row["confidence"] = confidence
            if key not in extra_study_ids:
                study_number += 1
        elif key in adjacent_low or key in adjacent_moderate:
            row["full_text_decision"] = "include_adjacent"
            row["full_text_reason"] = (
                "Measured review, quality, security, maintainability, skills or interaction outcome"
            )
            row["study_id"] = str(
                extra_study_ids.get(key, f"ST-{study_number:02d}")
            )
            row["confidence"] = "low" if key in adjacent_low else "moderate"
            if key not in extra_study_ids:
                study_number += 1
        elif key in secondary:
            row["full_text_decision"] = "include_secondary"
            row["full_text_reason"] = "Eligible secondary synthesis"
        elif key in upgrades:
            row["full_text_decision"] = "upgrade_existing_adjacent"
            row["full_text_reason"] = (
                "Peer-reviewed version replaces an existing contextual report"
            )
            row["study_id"] = "ST-60"
            row["confidence"] = "moderate"
        elif key in duplicates:
            row["full_text_decision"] = "duplicate_report"
            row["full_text_reason"] = str(duplicates[key])
        elif key in exclusions:
            row["full_text_decision"] = "exclude_full_text"
            row["full_text_reason"] = str(exclusions[key])
        else:
            raise RuntimeError(f"No eligibility decision for {row['title']!r}")

        assessed.append(row)

    if len(assessed) != 69:
        raise RuntimeError(f"Expected 69 assessed reports, found {len(assessed)}")

    with REGISTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with (HERE / "report-assessments.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(assessed)

    counts: dict[str, int] = {}
    for row in assessed:
        decision = row["full_text_decision"]
        counts[decision] = counts.get(decision, 0) + 1

    summary_path = HERE / "search-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary.update(
        {
            "reports_assessed_for_eligibility": len(assessed),
            "report_assessment_decisions": counts,
            "new_source_documents_included": (
                counts.get("include_productivity", 0)
                + counts.get("include_adjacent", 0)
                + counts.get("include_secondary", 0)
            ),
            "updated_source_documents": 154,
            "updated_empirical_studies": 99,
            "updated_productivity_studies": 44,
            "updated_adjacent_studies": 55,
            "updated_productivity_effect_estimates": 46,
            "updated_secondary_syntheses": 2,
            "updated_contextual_documents": 53,
            "updated_confidence": {
                "high": 11,
                "moderate": 63,
                "low": 25,
            },
        }
    )
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
