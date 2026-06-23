"""Validate local BibTeX reference hygiene for the CASE-Lingxi draft."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BIB = PROJECT_ROOT / "papers/metadata/references.bib"

PROTECTED_TERMS = [
    "AAAI",
    "ACM",
    "AdaRNN",
    "AlphaPROBE",
    "AlphaStock",
    "CI-STHPAN",
    "Chronos",
    "DDG-DA",
    "DeepTrader",
    "DiffsFormer",
    "DLinear",
    "DoubleAdapt",
    "DoubleEnsemble",
    "FactorVAE",
    "FEDformer",
    "FinMamba",
    "FinTSB",
    "HIST",
    "ICML",
    "IJCAI",
    "LLM",
    "LSR-IGRU",
    "LTSF-Linear",
    "MAGRPO",
    "MASTER",
    "MDGNN",
    "MOMENT",
    "Mamba",
    "Moirai",
    "Qlib",
    "RAGEN",
    "THGNN",
    "TINs",
    "TimeFilter",
    "TimeMixer",
    "TimesFM",
    "TTM",
    "TTMs",
    "Transformer",
    "VAE",
]


def parse_entries(text: str) -> list[dict[str, str]]:
    entries = []
    chunks = re.split(r"\n(?=@)", text.strip())
    for chunk in chunks:
        header = re.match(r"@(\w+)\{([^,]+),", chunk)
        if not header:
            continue
        fields = {}
        for match in re.finditer(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", chunk, flags=re.M):
            fields[match.group(1).lower()] = match.group(2)
        entries.append({"type": header.group(1), "key": header.group(2), **fields})
    return entries


def is_protected(title: str, term: str) -> bool:
    spans = [match.span() for match in re.finditer(r"\{[^{}]*\}", title)]
    starts = [match.start() for match in re.finditer(re.escape(term), title)]
    if not starts:
        return True
    for start in starts:
        end = start + len(term)
        if not any(span_start <= start and end <= span_end for span_start, span_end in spans):
            return False
    return True


def main() -> int:
    text = BIB.read_text(encoding="utf-8")
    entries = parse_entries(text)
    errors = []
    keys = [entry["key"] for entry in entries]
    for key in sorted(set(keys)):
        if keys.count(key) > 1:
            errors.append(f"duplicate key: {key}")
    for entry in entries:
        required = ["title", "author", "year"]
        required.append("booktitle" if entry["type"] == "inproceedings" else "journal")
        for field in required:
            if not entry.get(field):
                errors.append(f"{entry['key']} missing {field}")
        combined = " ".join(entry.values())
        if any(marker in combined for marker in ["DRAFT", "UNKNOWN", "pending", "venue unverified"]):
            errors.append(f"{entry['key']} contains draft/unknown marker")
        title = entry.get("title", "")
        for term in PROTECTED_TERMS:
            if term in title and not is_protected(title, term):
                errors.append(f"{entry['key']} title term not protected: {term}")
    print(f"entries={len(entries)}")
    print(f"keys={len(keys)}")
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("REFERENCES_BIB_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
