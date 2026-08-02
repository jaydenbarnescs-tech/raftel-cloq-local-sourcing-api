#!/usr/bin/env python3
"""Upload form-sales sourcing rows from a CSV file."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from api_client import post


def clean(row: dict[str, str]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in row.items():
        value = (value or "").strip()
        if not value:
            continue
        if key == "confidence":
            out[key] = float(value)
        elif key == "employee_count":
            out[key] = int(value)
        else:
            out[key] = value
    return out


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 examples/upload_csv.py examples/form-sales-sourcing.csv")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"CSVが見つかりません: {path}")
        return 2
    ok = 0
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            payload = clean(row)
            if not payload.get("company_name"):
                print("skip: company_name が空です")
                continue
            result = post("/tables/partner_company_enrichment/rows", {"row": payload})
            ok += 1
            print(f"OK rowid={result.get('rowid')} company={payload.get('company_name')}")
    print(f"done: {ok} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

