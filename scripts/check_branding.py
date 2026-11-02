#!/usr/bin/env python3
"""Check approved branding locally; --remote adds public, read-only HTTPS GETs."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import struct
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
MAX_RESPONSE = 8 * 1024 * 1024


def fetch(url):
    request = Request(url, headers={"User-Agent": "NuvemAggilli-BrandingCheck/1",
                                    "Cache-Control": "no-cache"})
    with urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError("HTTP " + str(response.status))
        final = urlsplit(response.url)
        if final.scheme != "https" or final.hostname != urlsplit(url).hostname:
            raise ValueError("unexpected redirect destination")
        body = response.read(MAX_RESPONSE + 1)
        if len(body) > MAX_RESPONSE:
            raise ValueError("response exceeds 8 MiB")
        return body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote", action="store_true", help="Also check live public endpoints")
    parser.add_argument("--base-url", help="Override the HTTPS origin for staging checks")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "config/branding.json").read_text(encoding="utf-8"))
    failures = []

    def check(label, condition):
        print(("OK   " if condition else "FAIL ") + label)
        if not condition:
            failures.append(label)

    for relative, expected in manifest["assets"].items():
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents:
            raise ValueError("asset is outside repository")
        data = path.read_bytes()
        check(relative + " SHA-256", hashlib.sha256(data).hexdigest() == expected["sha256"])
        is_png = len(data) >= 33 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR"
        check(relative + " PNG", is_png)
        if is_png:
            width, height = struct.unpack(">II", data[16:24])
            check(relative + " dimensions", (width, height) == (expected["width"], expected["height"]))
            check(relative + " RGBA channel", data[24:26] == bytes([8, 6]))

    if args.remote:
        base = (args.base_url or manifest["base_url"]).rstrip("/")
        parsed = urlsplit(base)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or parsed.path not in ("", "/")):
            raise ValueError("base URL must be a credential-free HTTPS origin")
        try:
            page = html.unescape(fetch(base + "/login").decode("utf-8"))
            check("login HTTP 200", True)
            for key, value in manifest["values"].items():
                check("login contains " + key, value in page)
        except Exception as error:
            check("login request: " + type(error).__name__, False)
        for key, relative in manifest["images"].items():
            try:
                body = fetch(base + "/apps/theming/image/" + key)
                check("public " + key + " SHA-256",
                      hashlib.sha256(body).hexdigest() == manifest["assets"][relative]["sha256"])
            except Exception as error:
                check("public " + key + " request: " + type(error).__name__, False)

    print("No writes performed. Functional tests are outside this check.")
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(2)
