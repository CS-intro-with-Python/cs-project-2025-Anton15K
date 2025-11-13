#!/usr/bin/env python3
"""
Simpler "test user" that verifies all API endpoints are reachable using the
popular 'requests' library for clarity and brevity.

Usage:
    python scripts/test_user_requests.py [--base-url http://localhost:5001] [--no-wait] [-v]

Notes:
- Requires 'requests'. Install it with:  pip install requests
- Exits non-zero if any check fails.
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


DEFAULT_BASE_URL = "http://localhost:5001"
API_PREFIX = "/api/v1"
TIMEOUT = 8  # seconds per HTTP call


@dataclass
class Check:
    name: str
    method: str
    path: str
    expected_status: int
    body: Optional[Dict[str, Any]] = None


def make_request(sess: requests.Session, base_url: str, method: str, path: str, body: Optional[dict] = None) -> Tuple[int, str]:
    url = base_url.rstrip("/") + path
    method = method.upper()
    try:
        resp = sess.request(method, url, json=body, timeout=TIMEOUT)
        # We don't raise for status so we can compare expected vs actual cleanly
        content = resp.text if (resp.headers.get("Content-Type", "").startswith("application/json") or resp.text) else ""
        return resp.status_code, content
    except requests.RequestException as e:
        raise RuntimeError(f"Request error contacting {url}: {e}") from e


def wait_for_health(sess: requests.Session, base_url: str, timeout_sec: float = 15.0) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            status, _ = make_request(sess, base_url, "GET", f"{API_PREFIX}/health")
            if status == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def main(argv: Optional[List[str]] = None) -> int:


    base = "http://127.0.0.1:5001"

    sess = requests.Session()
    sess.headers.update({"Accept": "application/json"})

    time.sleep(2)

    checks: List[Check] = [
        Check("Index", "GET", "/", 200),
        Check("Health", "GET", f"{API_PREFIX}/health", 200),
        Check("Users: me", "GET", f"{API_PREFIX}/users/me", 200),
        Check("Problems: list", "GET", f"{API_PREFIX}/problems", 200),
        Check("Problems: create", "POST", f"{API_PREFIX}/problems", 201, {"cf_id": "9999Z", "title": "Demo Problem"}),
        Check("Problems: get one", "GET", f"{API_PREFIX}/problems/1", 200),
        Check("Problems: estimate", "GET", f"{API_PREFIX}/problems/1/estimate", 200),
        Check("Auth: register", "POST", f"{API_PREFIX}/auth/register", 201, {"username": "alice", "email": "alice@example.com", "password": "secret"}),
        Check("Auth: login", "POST", f"{API_PREFIX}/auth/login", 200, {"username": "alice", "password": "secret"}),
        Check("Auth: logout", "POST", f"{API_PREFIX}/auth/logout", 200),
        Check("Attempts: start", "POST", f"{API_PREFIX}/attempts/start", 201, {"problem_id": 42}),
        Check("Attempts: complete", "POST", f"{API_PREFIX}/attempts/complete", 200, {"attempt_id": 100, "result": "solved"}),
        Check("Attempts: history", "GET", f"{API_PREFIX}/attempts/history", 200),
        Check("Ratings: adjust", "POST", f"{API_PREFIX}/ratings/adjust", 200, {"problem_id": 42, "delta": 10}),
    ]

    total = len(checks)
    passed = 0
    failures: List[str] = []

    print(f"Running {total} API reachability checks against {base}\n")

    for chk in checks:
        try:
            status, body = make_request(sess, base, chk.method, chk.path, chk.body)
            ok = status == chk.expected_status
            icon = "✓" if ok else "✗"
            print(f"[{icon}] {chk.name:<22} {chk.method} {chk.path} -> {status} (expected {chk.expected_status})")
            if ok:
                passed += 1
            else:
                failures.append(f"{chk.name}: got {status}, expected {chk.expected_status}. Body: {body[:300]}...")
        except Exception as e:
            print(f"[✗] {chk.name:<22} {chk.method} {chk.path} -> error: {e}")
            failures.append(f"{chk.name}: exception: {e}")

    print(f"\nSummary: {passed}/{total} passed")
    if failures:
        print("\nFailures:")
        for f in failures:
            print(" - " + f)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
