"""Read and summarize benchmark instrument files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Instrument:
    symbol: str
    start_date: str
    end_date: str


def read_instruments(path: str | Path) -> list[Instrument]:
    instruments: list[Instrument] = []
    with Path(path).open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                raise ValueError(f"invalid instrument row at line {line_number}: {line}")
            instruments.append(Instrument(symbol=parts[0], start_date=parts[1], end_date=parts[2]))
    return instruments


def summarize_instruments(instruments: list[Instrument]) -> dict[str, str]:
    if not instruments:
        return {"count": "0", "start_date": "", "end_date": ""}
    return {
        "count": str(len(instruments)),
        "start_date": min(item.start_date for item in instruments),
        "end_date": max(item.end_date for item in instruments),
    }
