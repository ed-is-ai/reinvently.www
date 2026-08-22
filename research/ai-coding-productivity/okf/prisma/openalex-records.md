---
type: Raw Record Snapshot
title: Raw OpenAlex record snapshot
description: Newline-delimited raw OpenAlex API records for the 29 July 2026 search snapshot.
resource: https://reinvently.co.uk/research/ai-coding-productivity/prisma/openalex-records.jsonl
tags: [ai-coding-productivity, prisma, systematic-review]
status: stable
generated: { by: claude-code/claude-sonnet-5, at: 2026-08-22T21:25:19Z }
---

# Schema

Newline-delimited JSON; one full OpenAlex work record per line (id, doi,
title, publication_year, publication_date, type, language,
primary_location, and other OpenAlex API fields). No fixed column
schema — this is a raw external-API dump, not a curated table.

# Provenance

Underlies the [screening register](screening-register.md)'s `openalex_id`
column. Not every screening-register row has a corresponding record here:
rows carried over from the [existing corpus](existing-corpus.md) predate
this snapshot and were never looked up against it.
