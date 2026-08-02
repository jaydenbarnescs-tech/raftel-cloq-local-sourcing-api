#!/usr/bin/env python3
"""Check token, device approval, and table access."""

from api_client import get


data = get("/tables")
print("OK: APIに接続できました")
print("tables:")
for name in data.get("tables", []):
    print(f"- {name}")

