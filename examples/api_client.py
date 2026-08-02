#!/usr/bin/env python3
"""Small stdlib-only client for the Raftel/CLOQ local sourcing API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = os.environ.get("SETOYAMA_API_BASE", "https://mgc-pass-proxy.duckdns.org/setoyama-api").rstrip("/")
TOKEN = os.environ.get("SETOYAMA_API_TOKEN", "").strip()
COOKIE_FILE = Path(os.environ.get("SETOYAMA_COOKIE_FILE", "setoyama.cookies"))
DEVICE_ID = os.environ.get("SETOYAMA_DEVICE_ID", "").strip()


class ApiError(RuntimeError):
    pass


def _cookie_header() -> str:
    if not COOKIE_FILE.exists():
        return ""
    cookies: list[str] = []
    for line in COOKIE_FILE.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            cookies.append(line.strip())
    return "; ".join(cookies)


def _save_cookie(headers: Any) -> None:
    raw = headers.get("Set-Cookie")
    if not raw:
        return
    cookie = raw.split(";", 1)[0].strip()
    if cookie:
        COOKIE_FILE.write_text(cookie + "\n", encoding="utf-8")


def request(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    if not TOKEN:
        raise ApiError("SETOYAMA_API_TOKEN が設定されていません")
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/json",
    }
    if DEVICE_ID:
        headers["X-Setoyama-Device-Id"] = DEVICE_ID
    cookie = _cookie_header()
    if cookie:
        headers["Cookie"] = cookie
    req = urllib.request.Request(BASE_URL + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            _save_cookie(resp.headers)
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip

                data = gzip.decompress(data)
            return json.loads(data.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        data = exc.read()
        try:
            parsed = json.loads(data.decode("utf-8"))
        except Exception:
            parsed = {"error": data.decode("utf-8", errors="replace")}
        raise ApiError(f"HTTP {exc.code}: {json.dumps(parsed, ensure_ascii=False)}") from exc


def get(path: str) -> dict[str, Any]:
    return request("GET", path)


def post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    return request("POST", path, payload)


def patch(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    return request("PATCH", path, payload)


def delete(path: str) -> dict[str, Any]:
    return request("DELETE", path)
