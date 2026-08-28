#!/usr/bin/env python3
"""Serve a Markdown artifact through the bundled static HTML renderer.

The server uses only the Python standard library. Full Markdown rendering is
handled in the browser by assets/markdown-renderer.html via Marked, DOMPurify,
Mermaid, and highlight.js.
"""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
from typing import Iterable
from urllib.parse import urlparse


RENDERER_PATH = Path(__file__).resolve().parents[1] / "assets" / "markdown-renderer.html"


def find_port(preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            probe.bind(("127.0.0.1", 0))
            return int(probe.getsockname()[1])


def serve(markdown_path: Path, port: int) -> None:
    artifact = markdown_path.resolve()
    renderer = RENDERER_PATH.resolve()
    if not renderer.is_file():
        raise FileNotFoundError(f"Missing static renderer: {renderer}")

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, payload: bytes, content_type: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in {"/", "/index.html", "/renderer.html"}:
                self.send_bytes(renderer.read_bytes(), "text/html; charset=utf-8")
                return

            if path == "/artifact.md":
                self.send_bytes(artifact.read_bytes(), "text/markdown; charset=utf-8")
                return

            if path == "/healthz":
                self.send_bytes(b"ok", "text/plain; charset=utf-8")
                return

            self.send_error(404)

        def log_message(self, format: str, *args: object) -> None:
            return

    actual_port = find_port(port)
    server = ThreadingHTTPServer(("127.0.0.1", actual_port), Handler)
    print(f"Serving Markdown artifact: {artifact}", flush=True)
    print(f"Renderer: {renderer}", flush=True)
    print(f"Open: http://127.0.0.1:{actual_port}/?src=/artifact.md", flush=True)
    server.serve_forever()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Serve a Markdown file through the bundled HTML renderer."
    )
    parser.add_argument("markdown_file", help="Path to the Markdown artifact.")
    parser.add_argument("--port", type=int, default=8765, help="Preferred localhost port.")
    args = parser.parse_args(argv)

    path = Path(args.markdown_file)
    if not path.is_file():
        parser.error(f"Markdown file does not exist: {path}")
    serve(path, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
