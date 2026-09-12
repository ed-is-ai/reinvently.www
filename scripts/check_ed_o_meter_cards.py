#!/usr/bin/env python3
"""Check Ed-o-meter promotional cards against the current board metadata."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "ed-o-meter" / "data.js"

CARDS = {
    "tools/index.html": re.compile(
        r'<a class="post-card" href="/tools/ed-o-meter/">(.*?)</a>', re.S
    ),
    "news/index.html": re.compile(
        r'<a class="post-card" href="/tools/ed-o-meter/">(.*?)</a>', re.S
    ),
    "index.html": re.compile(
        r'<a href="/tools/ed-o-meter/" data-tags="tools".*?>(.*?)</a>', re.S
    ),
}


ONES = ("zero", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
        "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
TENS = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety")


def number_words(value: int) -> str:
    if value < 20:
        return ONES[value]
    tens, remainder = divmod(value, 10)
    return TENS[tens] if remainder == 0 else f"{TENS[tens]}-{ONES[remainder]}"


def current_metadata() -> tuple[int, str]:
    text = DATA.read_text(encoding="utf-8")
    models = re.search(r"const MODELS = \[(.*?)\n\];", text, re.S)
    generated = re.search(r"generated:'(\d{4}-\d{2}-\d{2})", text)
    if models is None or generated is None:
        raise ValueError(f"could not read board metadata from {DATA}")
    count = len(re.findall(r"^\s*\{id:", models.group(1), re.M))
    if not count:
        raise ValueError(f"no models found in {DATA}")
    y, m, d = (int(part) for part in generated.group(1).split("-"))
    stamp = date(y, m, d).strftime("%-d %B %Y")
    return count, stamp


def main() -> int:
    count, stamp = current_metadata()
    expected_counts = (f"{count} models", f"{number_words(count).capitalize()} models")
    expected_date = f"Updated {stamp}"
    errors: list[str] = []

    for relative, pattern in CARDS.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        matches = pattern.findall(text)
        if len(matches) != 1:
            errors.append(f"{relative}: expected one Ed-o-meter card, found {len(matches)}")
            continue
        card = matches[0]
        if not any(expected in card for expected in expected_counts):
            errors.append(f"{relative}: missing current model count ({' or '.join(expected_counts)})")
        if expected_date not in card:
            errors.append(f"{relative}: missing current update date ({expected_date})")

    if errors:
        print("Ed-o-meter card drift detected:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Ed-o-meter cards match {expected_counts[0]} and {stamp}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
