#!/usr/bin/env python3
"""Rhythm report for A Young Delegate's Notebook.

Measures sentence length and paragraph length per chapter against the targets in
AGENTS.md, and flags the tic words AGENTS.md says to audit. It is a mirror, not a judge: it always exits 0, and every flag is
something to weigh case by case.

    python lint.py                    every chapter, one summary row each
    python lint.py ch-01              one chapter, with the flagged spots listed
    python lint.py ch-01 ch-01.rev    compare a chapter with its revision
    python lint.py -v                 every chapter, with the flagged spots listed
"""
from __future__ import annotations

import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"

# Targets from AGENTS.md. Change them here and in AGENTS.md together.
MEAN_LOW, MEAN_HIGH = 10, 13  # average words per sentence
SOFT_CAP = 25                 # past this a sentence needs a reason
HARD_CAP = 35                 # past this it gets split
SHORT = 9                     # "short" means under 10 words
MAX_SHORT_RUN = 3             # never more than three short sentences in a row
MAX_LONG_RUN = 1              # never two sentences over the soft cap in a row
MIN_VARIETY = 0.35            # spread of lengths relative to the mean
MAX_PARA_WORDS = 55           # paragraphs of 55 words at most

ABBREV = ["p.m.", "a.m.", "U.S.", "etc.", "St.", "Dr.", "Mr.", "Mrs."]
DOT = "\u2024"  # stands in for a period inside an abbreviation while splitting
SPLIT = re.compile(r"(?<=[.?!])[\"')\]]*\s+(?=[\"'(A-Z0-9])")
LIST_ITEM = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
TIC = re.compile(r"\b(?:door\w*|carr(?:y|ies|ied|ying)|reach\w*)\b", re.IGNORECASE)


def count_words(text: str) -> int:
    return sum(1 for w in text.split() if re.search(r"[A-Za-z0-9]", w))


def blank_comments(text: str) -> str:
    """Remove HTML comments but keep the line count, so line numbers stay true."""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def strip_markup(line: str) -> str:
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)  # links keep their text
    return re.sub(r"[*`]", "", line)


def split_sentences(text: str):
    for a in ABBREV:
        text = text.replace(a, a.replace(".", DOT))
    for part in SPLIT.split(text):
        part = part.replace(DOT, ".").strip()
        if count_words(part):
            yield part


def parse(path: Path):
    """Return (sentences, paragraphs) for one chapter file.

    Headings, blockquotes (the epigraph), tables, and rules
    are skipped. Each list item counts as its own sentence run but not as a
    paragraph. A heading or a box edge starts a new block, and runs never cross blocks.
    """
    text = blank_comments(path.read_text(encoding="utf-8"))
    sentences: list[dict] = []
    paragraphs: list[tuple[int, int]] = []
    block = 0
    para_start: int | None = None
    para_words = 0

    def close_para() -> None:
        nonlocal para_start, para_words
        if para_start is not None:
            paragraphs.append((para_start, para_words))
        para_start, para_words = None, 0

    for no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            close_para()
            continue
        if line.startswith(("#", "<div", "</div")):
            close_para()
            block += 1
            continue
        if line.startswith((">", "|", "---")):
            close_para()
            continue
        is_item = bool(LIST_ITEM.match(raw))
        if is_item:
            close_para()
            line = LIST_ITEM.sub("", raw).strip()
        elif para_start is None:
            para_start = no
        for s in split_sentences(strip_markup(line)):
            sentences.append({"line": no, "words": count_words(s), "text": s, "block": -no if is_item else block})
            if not is_item:
                para_words += count_words(s)
    close_para()
    return sentences, paragraphs


def find_tics(path: Path) -> list[tuple[int, str, str]]:
    """Every tic word AGENTS.md says to audit (door, carry, reach in any form), with its line."""
    text = blank_comments(path.read_text(encoding="utf-8"))
    hits: list[tuple[int, str, str]] = []
    for no, raw in enumerate(text.splitlines(), 1):
        line = strip_markup(raw).strip()
        for m in TIC.finditer(line):
            hits.append((no, m.group(0), line))
    return hits


def find_runs(sentences: list[dict], test, min_len: int) -> list[list[dict]]:
    """Runs of consecutive sentences that pass `test`, within one block, at least min_len long."""
    found: list[list[dict]] = []
    cur: list[dict] = []

    def flush() -> None:
        if len(cur) >= min_len:
            found.append(list(cur))

    for s in sentences:
        if test(s) and (not cur or cur[-1]["block"] == s["block"]):
            cur.append(s)
        else:
            flush()
            cur = [s] if test(s) else []
    flush()
    return found


def measure(sentences: list[dict], paragraphs: list[tuple[int, int]]) -> dict | None:
    words = [s["words"] for s in sentences]
    n = len(words)
    if n == 0:
        return None
    mean = sum(words) / n
    ordered = sorted(words)
    return {
        "n": n,
        "mean": mean,
        "p90": ordered[min(n - 1, int(n * 0.9))],
        "max": ordered[-1],
        "soft": sum(w > SOFT_CAP for w in words),
        "hard": sum(w > HARD_CAP for w in words),
        "short_pct": 100 * sum(w <= SHORT for w in words) / n,
        "variety": statistics.pstdev(words) / mean if mean else 0.0,
        "short_runs": find_runs(sentences, lambda s: s["words"] <= SHORT, MAX_SHORT_RUN + 1),
        "long_runs": find_runs(sentences, lambda s: s["words"] > SOFT_CAP, MAX_LONG_RUN + 1),
        "fat_paras": [p for p in paragraphs if p[1] > MAX_PARA_WORDS],
    }


def cell(text: str, width: int, flag: bool) -> str:
    return (text + ("!" if flag else " ")).rjust(width)


def row(name: str, m: dict) -> str:
    return (
        f"{name:<18}"
        + f"{m['n']:>5} "
        + cell(f"{m['mean']:.1f}", 7, not MEAN_LOW <= m["mean"] <= MEAN_HIGH)
        + f"{m['p90']:>5}{m['max']:>5}{m['soft']:>5} "
        + cell(str(m["hard"]), 4, m["hard"] > 0)
        + f"{m['short_pct']:>7.0f}% "
        + cell(f"{m['variety']:.2f}", 7, m["variety"] < MIN_VARIETY)
        + cell(str(len(m["short_runs"])), 6, bool(m["short_runs"]))
        + cell(str(len(m["long_runs"])), 6, bool(m["long_runs"]))
        + cell(str(len(m["fat_paras"])), 6, bool(m["fat_paras"]))
        + cell(str(len(m.get("tics", []))), 6, bool(m.get("tics")))
    )


HEADER = (
    f"{'file':<18}{'sent':>5} {'mean':>7}{'p90':>5}{'max':>5}{'>25':>5} {'>35':>4}"
    f"{'short':>8} {'variety':>7}{'short':>6}{'long':>6}{'fat':>6}{'tic':>6}"
)
SUBHEADER = (
    f"{'':<18}{'':>5} {'':>7}{'':>5}{'':>5}{'':>5} {'':>4}{'':>8} {'':>7}"
    f"{'runs':>6}{'runs':>6}{'paras':>6}{'words':>6}"
)
LEGEND = (
    f"! marks a number outside the AGENTS.md target: mean {MEAN_LOW}-{MEAN_HIGH}, nothing over {HARD_CAP}, "
    f"variety {MIN_VARIETY} or more, no run of {MAX_SHORT_RUN + 1} short sentences or {MAX_LONG_RUN + 1} long ones, "
    f"paragraphs of {MAX_PARA_WORDS} words or fewer, and no tic words (door, carry, reach in any form)."
)


def preview(text: str, width: int = 100) -> str:
    return text if len(text) <= width else text[: width - 3].rstrip() + "..."


def detail(name: str, m: dict, sentences: list[dict]) -> None:
    print(f"\n{name}")
    flagged = False
    over = sorted((s for s in sentences if s["words"] > SOFT_CAP), key=lambda s: -s["words"])
    for s in over[:15]:
        flagged = True
        print(f"  line {s['line']:>4}  {s['words']:>3} words  {preview(s['text'])}")
    if len(over) > 15:
        print(f"  ... and {len(over) - 15} more over {SOFT_CAP} words")
    for run in m["short_runs"]:
        flagged = True
        joined = " ".join(s["text"] for s in run)
        print(f"  line {run[0]['line']:>4}  {len(run)} short sentences in a row: {preview(joined, 110)}")
    for run in m["long_runs"]:
        flagged = True
        print(f"  line {run[0]['line']:>4}  {len(run)} long sentences in a row")
    for line, n in m["fat_paras"]:
        flagged = True
        print(f"  line {line:>4}  paragraph of {n} words")
    for line, word, text in m.get("tics", []):
        flagged = True
        print(f"  line {line:>4}  tic word \"{word}\": {preview(text)}")
    if not flagged:
        print("  nothing flagged")


def resolve(arg: str) -> Path:
    return CHAPTERS / (arg if arg.endswith(".md") else arg + ".md")


def main(argv: list[str]) -> int:
    verbose = "-v" in argv or "--verbose" in argv
    names = [a for a in argv if not a.startswith("-")]
    files = [resolve(a) for a in names] if names else [CHAPTERS / "intro.md", *sorted(CHAPTERS.glob("ch-??.md"))]

    results = []
    combined_sentences: list[dict] = []
    combined_paras: list[tuple[int, int]] = []
    combined_tics: list[tuple[int, str, str]] = []
    for i, f in enumerate(files):
        if not f.exists():
            print(f"warning: {f.name} not found, skipping")
            continue
        sentences, paragraphs = parse(f)
        m = measure(sentences, paragraphs)
        if m is None:
            continue
        m["tics"] = find_tics(f)
        combined_tics.extend(m["tics"])
        results.append((f.stem, m, sentences))
        for s in sentences:  # keep runs from joining across files
            combined_sentences.append({**s, "block": s["block"] + i * 100000})
        combined_paras.extend(paragraphs)

    if not results:
        print("nothing to report")
        return 0

    print(HEADER)
    print(SUBHEADER)
    for name, m, _ in results:
        print(row(name, m))
    if len(results) > 1:
        print("-" * len(HEADER))
        total = measure(combined_sentences, combined_paras)
        total["tics"] = combined_tics
        print(row("all", total))
    print(f"\n{LEGEND}")

    if names or verbose:
        for name, m, sentences in results:
            detail(name, m, sentences)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
