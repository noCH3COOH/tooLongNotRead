#!/usr/bin/env python3
"""Serve a Markdown artifact through the bundled static HTML renderer.

The server uses only the Python standard library. Full Markdown rendering is
handled in the browser by assets/markdown-renderer.html via Marked, DOMPurify,
Mermaid, and highlight.js.
"""

from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import socket
from typing import Iterable
from urllib.parse import quote, unquote, urlparse


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
    workspace = Path.cwd().resolve()
    renderer = RENDERER_PATH.resolve()
    if not renderer.is_file():
        raise FileNotFoundError(f"Missing static renderer: {renderer}")

    artifact_id = hashlib.sha256(str(artifact).encode("utf-8")).hexdigest()[:12]
    artifact_short_route = f"/artifact/{artifact_id}"
    artifact_prefix = f"/artifacts/{artifact_id}/"
    artifact_route = f"/artifacts/{artifact_id}/{artifact.name}"
    encoded_artifact_route = f"/artifacts/{artifact_id}/{quote(artifact.name)}"
    artifact_title = f"{workspace.name} / {artifact.name}"

    def is_safe_markdown(candidate: Path) -> bool:
        try:
            candidate.relative_to(artifact.parent)
        except ValueError:
            return False
        return candidate.is_file() and candidate.suffix.lower() in {".md", ".markdown"}

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, payload: bytes, content_type: str) -> None:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            path = unquote(urlparse(self.path).path)
            if path in {"/", "/index.html", "/renderer.html"}:
                self.send_bytes(renderer.read_bytes(), "text/html; charset=utf-8")
                return

            if path in {artifact_short_route, artifact_route}:
                self.send_bytes(artifact.read_bytes(), "text/markdown; charset=utf-8")
                return

            if path.startswith(artifact_prefix):
                relative_name = path[len(artifact_prefix) :]
                candidate = (artifact.parent / relative_name).resolve()
                if is_safe_markdown(candidate):
                    self.send_bytes(candidate.read_bytes(), "text/markdown; charset=utf-8")
                    return

            if path == "/artifact-info.json":
                info = {
                    "artifact": str(artifact),
                    "artifact_id": artifact_id,
                    "artifact_short_route": artifact_short_route,
                    "artifact_route": artifact_route,
                    "artifact_prefix": artifact_prefix,
                    "project": str(workspace),
                    "title": artifact_title,
                }
                self.send_bytes(
                    json.dumps(info, ensure_ascii=False, indent=2).encode("utf-8"),
                    "application/json; charset=utf-8",
                )
                return

            if path == "/artifact.md":
                message = (
                    "Generic /artifact.md is disabled to avoid opening artifacts from "
                    "the wrong project. Restart the renderer and use the generated "
                    f"{artifact_route} URL."
                )
                self.send_response(410)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(message.encode("utf-8"))
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
    print(f"Project root: {workspace}", flush=True)
    print(f"Artifact short route: {artifact_short_route}", flush=True)
    print(f"Artifact route: {artifact_route}", flush=True)
    print(f"Renderer: {renderer}", flush=True)
    print(
        "Open: "
        f"http://127.0.0.1:{actual_port}/?src={encoded_artifact_route}"
        f"&title={quote(artifact_title)}",
        flush=True,
    )
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
