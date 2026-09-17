"""Small standard-library HTTP surface for the phone health contract."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from .policy import DEFAULT_POLICY, CapabilityPolicy

SERVICE_NAME = "atomic-phone"
SCHEMA_VERSION = "1"


def health_payload(policy: CapabilityPolicy = DEFAULT_POLICY) -> dict[str, object]:
    """Build the deterministic JSON payload returned by ``GET /health``."""

    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "schema_version": SCHEMA_VERSION,
        "capabilities": policy.snapshot(),
    }


def _json_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


class HealthHandler(BaseHTTPRequestHandler):
    """Serve only the health stub and a JSON 404 for every other route."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if urlsplit(self.path).path == "/health":
            body = _json_bytes(health_payload())
            self.send_response(200)
        else:
            body = _json_bytes({"status": "not_found"})
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        """Keep the stub quiet and deterministic in offline harnesses."""

        del format, args


def create_server(host: str = "127.0.0.1", port: int = 8080) -> ThreadingHTTPServer:
    """Create a server without starting it."""

    return ThreadingHTTPServer((host, port), HealthHandler)


def main() -> None:
    server = create_server()
    print(f"{SERVICE_NAME} listening on http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
