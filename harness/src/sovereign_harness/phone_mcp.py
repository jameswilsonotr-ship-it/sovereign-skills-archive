"""Phone MCP v0 health endpoint for a local Termux bridge.

The endpoint is intentionally tiny: ``GET /health`` reports readiness and
offline capabilities. It does not send messages and it does not access a
camera.
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from pydantic import BaseModel


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8081


class PhoneHealth(BaseModel):
    status: str = "ok"
    service: str = "phone-bridge"
    version: str = "0.1.0"
    capabilities: tuple[str, ...] = ("health", "offline-fixtures")


def health_payload() -> dict[str, Any]:
    """Return the stable, JSON-serializable health response."""

    return PhoneHealth().model_dump()


class PhoneRequestHandler(BaseHTTPRequestHandler):
    """Serve only the v0 health resource."""

    server_version = "sovereign-phone-mcp/0.1"

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path != "/health":
            self.send_error(404, "only /health is available")
            return

        body = json.dumps(health_payload()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        # Keep Termux output useful without leaking request data.
        return


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Run the local health server, defaulting to Termux port 8081."""

    with ThreadingHTTPServer((host, port), PhoneRequestHandler) as server:
        server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    serve(args.host, args.port)


if __name__ == "__main__":
    main()
