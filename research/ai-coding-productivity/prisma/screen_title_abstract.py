#!/usr/bin/env python3
"""Apply the documented AI-assisted title/abstract screening decisions."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
REGISTER = HERE / "screening-register.csv"

FULL_TEXT_TITLES = {
    "A Small-scale Exploratory Study of Static Code Analysis in AI-Assisted Software Development : Developer Perceptions, Expectations, and Adoption Challenges",
    "A Study of Library Usage in Agent-Authored Pull Requests",
    "A Survey of Vibe Coding with Large Language Models",
    "Agent-Driven Design & Development: An Empirical Study of Solo Developer Productivity with LLM Coding Agents",
    "Agentic AI-Driven Developer Experience for Telecom Capabilities",
    "Agentic Much? Adoption of Coding Agents on GitHub",
    "AgenticFlict: A Large-Scale Dataset of Merge Conflicts in AI Coding Agent Pull Requests on GitHub",
    "AI-assisted Software Development in Digital Dentistry: A Technical Innovation Report with Three Open-Source Applications",
    "AI based software re-engineering : case AQUATOX",
    "AI-Enhanced Unit Testing with xUnit: Optimizing Test Creation through GitHub Copilot",
    "An Empirical Study: Leveraging Prompt Engineering with AI Coding Assistants to Develop Energy-Efficient Code (2025)",
    "Analyzing Developer Use of ChatGPT Generated Code in Open Source GitHub Projects",
    "Architectural Entropy in AI-Assisted Software Development",
    "Artificially Insecure: Examining GitHub Copilot’s AI-based Vulnerability Prevention System",
    "Assessing GitHub Copilot in Solidity Development: Capabilities, Testing, and Bug Fixing",
    "Building web applications with AI: a comparative study",
    "Can generative AI bridge the gap? A quasi-experimental study of non-programmers with AI vs. programmers without AI",
    "Can LLMs Generate Higher Quality Code Than Humans? An Empirical Study",
    "Can You Trust Your Copilot? A Privacy Scorecard for AI Coding Assistants",
    "Chatting with AI: Deciphering Developer Conversations with ChatGPT",
    "Coding Agents in the Wild: Failure Modes and Rejection Patterns of AI-Generated Pull Requests",
    "Cognitive Apprenticeship and Artificial Intelligence Coding Assistants",
    "Der Einfluss KI-basierter Programmierassistenten auf die Zusammenarbeit in Softwareentwicklungsteams",
    "Developer Experiences with a Contextualized AI Coding Assistant: Usability, Expectations, and Outcomes",
    "Developer Perceptions on the Maintainability of AI-generated Code : A Survey-based Study",
    "DevGPT: Studying Developer-ChatGPT Conversations",
    "Disrupting Test Development with AI Assistants",
    "Disrupting Test Development with AI Assistants: Building the Base of the Test Pyramid with Three AI Coding Assistants",
    "Domain ambiguity in AI-assistedsoftware development : A controlled study of how an AI agent handlesinconsistent business-domain context",
    "En jämförande säkerhetsutvärdering av manuell och AI-assisterad utveckling av webbapplikationer",
    "Evaluating AI-Generated T-SQL Code Review Reports in an Enterprise-Scale Codebase",
    "Evaluating the Educational Benefits and Risks of AI Coding Assistants Among Novice Programming Students in Sri Lanka",
    "Experience with GitHub Copilot for Developer Productivity at Zoominfo",
    "Exploring and modelling human-AI collaboration effectiveness in software engineering using behavioural analysis and machine learning",
    "Exploring Ethical Awareness and Practices in Software Development : Study of AI Coding Assistant Tools Usage Among Developers",
    "Exploring the Challenges and Opportunities of AI-assisted Codebase Generation",
    "Fork-Triggerable AI Coding Agents in CI: A Wide-Net Survey",
    "From Developer Pairs to AI Copilots: A Comparative Study on Knowledge Transfer",
    "From Meeting to Pull Request : An End-to-End Evaluation of LLM-Based Software Development Automation",
    "From Preventive to Reactive: How AI Coding Assistants Transform Developers' Security Awareness",
    "From Problem Solving to Output Validation: Breakdowns in Thinking and Work Practices in AI-Assisted Software Development",
    "From Specifications to Implementation in the Gen-AI Era: Lessons from a Project-Based Software Engineering Course",
    "GitHub Copilot Developer Experience: A Study Comparing Novice and Experienced Developers' Perspectives",
    "Good Vibrations? A Qualitative Study of Co-Creation, Communication, Flow, and Trust in Vibe Coding",
    "How Do Developers Interact with AI? An Exploratory Study on Modeling Developer Programming Behavior",
    "How far are AI-powered programming assistants from meeting developers' needs?",
    "How Safe Are AI-Generated Patches? A Large-scale Study on Security Risks in LLM and Agentic Automated Program Repair on SWE-bench",
    "Human-Written vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and Complexity",
    "Insecure by design? A human-centric security perspective on AI-assisted software development",
    "Is Agentic Code Review Helpful? Mining Developers' Feedback to CodeRabbit Reviews in the Wild",
    "Limitations and improvements of context for GitHub Copilot in professional software development",
    "LLM impact on BLV programming",
    "Multi-Simulation as Labor Compression: A Solo Operator Ships a Concurrency-Robust Product in One Session — An Experience Report",
    "\"My productivity is boosted, but ...\" Demystifying Users' Perception on AI Coding Assistants",
    "On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub",
    "Psychological Ownership in AI-Assisted Software Development: A Qualitative Study of Developer’s Authorship, Responsibility and Cognitive Engagement in Collaborative Projects",
    "Security Weaknesses in LLM-Generated Source Code: An Empirical Vulnerability Analysis of Iterative AI-Assisted Development v1.0",
    "Self-Admitted GenAI Usage in Open-Source Software",
    "Seniority, Spillovers, and AI-Enhanced Code Contributions: Evidence from a Major Enterprise",
    "Shifting Roles And Emerging Competencies in Ai-Assisted Software Development : A Qualitative Study of Professional Developers",
    "Tab to Autocomplete: The Effects of AI Coding Assistants on Web Accessibility",
    "The Impact of Generative AI Coding Assistants on Developers Who Are Visually Impaired",
    "The Influence of AI Code Assistants on Programming Learning : A Descriptive Study of Student Dependence",
    "The Invisible Bottom Line : How GitHub Copilot Reshapes Decision-Making and Operational Workflows in Energy Trading Operations",
    "The New Developer: AI Skill Threat, Identity Change &amp;amp; Developer Thriving in the Transition to AI-Assisted Software Development",
    "\"Trusting the Pipeline, Not the AI\": Agency and Adoption in AI-Assisted Software Development",
    "Understanding and Predicting Accepted Code Suggestions in AI-Assisted Programming",
    "What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests",
    "\"You're on a bicycle with a little motor\": Benefits and Challenges of Using AI Code Assistants",
}


def normalise(value: str) -> str:
    value = value.replace("&amp;amp;", "&").replace("&amp;", "&")
    value = re.sub(r"\s+", " ", value)
    return value.strip().casefold()


def main() -> None:
    selected = {normalise(title) for title in FULL_TEXT_TITLES}
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    full_text: list[dict[str, str]] = []
    for row in rows:
        if row["record_sources"] != "OpenAlex":
            continue
        if normalise(row["title"]) in selected:
            row["human_decision"] = "seek_full_text"
            row["exclusion_reason"] = ""
            full_text.append(row)
        else:
            row["human_decision"] = "exclude_title_abstract"
            row["exclusion_reason"] = (
                "No eligible empirical developer, team or repository outcome indicated"
            )

    with REGISTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with (HERE / "full-text-candidates.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(full_text)

    summary_path = HERE / "search-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["title_abstract_records_screened"] = sum(
        row["record_sources"] == "OpenAlex" for row in rows
    )
    summary["reports_sought_for_full_text"] = len(full_text)
    summary["title_abstract_exclusions_after_review"] = sum(
        row["human_decision"] == "exclude_title_abstract" for row in rows
    )
    summary["pending_human_review"] = 0
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
