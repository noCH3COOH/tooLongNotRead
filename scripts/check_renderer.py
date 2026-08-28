#!/usr/bin/env python3
"""Check that a Too Long Not Read renderer URL can load its Markdown source."""

from __future__ import annotations

import argparse
import sys
from typing import Iterable
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen


def fetch_text(url: str) -> tuple[int, str]:
    request = Request(url, headers={"Cache-Control": "no-cache"})
    with urlopen(request, timeout=10) as response:
        status = int(response.status)
        charset = response.headers.get_content_charset() or "utf-8"
        return status, response.read().decode(charset, errors="replace")


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate that a local HTML Markdown renderer URL is wired to the expected artifact."
    )
    parser.add_argument("renderer_url", help="Renderer URL printed by serve_markdown.py.")
    parser.add_argument(
        "--expect",
        action="append",
        default=[],
        help="Text that must appear in the Markdown source. Can be provided multiple times.",
    )
    args = parser.parse_args(argv)

    parsed = urlparse(args.renderer_url)
    src_values = parse_qs(parsed.query).get("src")
    if not src_values:
        return fail("renderer URL has no src query parameter")

    renderer_status, renderer_html = fetch_text(args.renderer_url)
    if renderer_status != 200:
        return fail(f"renderer returned HTTP {renderer_status}")
    if "Too Long Not Read Markdown Renderer" not in renderer_html:
        return fail("renderer HTML does not look like the bundled renderer")

    markdown_url = urljoin(args.renderer_url, src_values[0])
    markdown_status, markdown_text = fetch_text(markdown_url)
    if markdown_status != 200:
        return fail(f"Markdown source returned HTTP {markdown_status}: {markdown_url}")

    missing = [snippet for snippet in args.expect if snippet not in markdown_text]
    if missing:
        return fail(f"Markdown source is missing expected text: {missing}")

    print(f"OK renderer: {args.renderer_url}")
    print(f"OK markdown: {markdown_url}")
    print(f"OK bytes: {len(markdown_text.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
