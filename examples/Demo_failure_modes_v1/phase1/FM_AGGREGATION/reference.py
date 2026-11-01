#!/usr/bin/env python3
"""Reference answer for this task; standard-library-only."""
from __future__ import annotations

import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

DATA_FILE = Path(__file__).resolve().with_name("data.csv")
START_DATE = "2026-09-01"
END_DATE = "2026-09-07"


def solve(csv_path: Path = DATA_FILE) -> dict[str, float]:
    total_clicks = 0
    total_orders = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"date", "channel", "campaign", "record_status", "clicks", "orders"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("Missing required data.csv columns")
        for row in reader:
            if not (START_DATE <= row["date"] <= END_DATE):
                continue
            if row["channel"] != "SEM" or row["record_status"] != "valid":
                continue
            clicks = int(row["clicks"])
            orders = int(row["orders"])
            if not (0 <= orders <= clicks):
                raise ValueError("Invalid counts in filtered data")
            total_clicks += clicks
            total_orders += orders

    if total_clicks == 0:
        raise ValueError("No eligible clicks")
    percentage = Decimal(total_orders) * Decimal(100) / Decimal(total_clicks)
    answer = float(percentage.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return {"answer": answer}


if __name__ == "__main__":
    print(json.dumps(solve(), ensure_ascii=False))
