from __future__ import annotations

from threading import Thread

import httpx
from http.server import ThreadingHTTPServer

from sovereign_harness.phone_mcp import PhoneRequestHandler, health_payload


def test_health_payload_has_only_v0_capabilities() -> None:
    payload = health_payload()

    assert payload["status"] == "ok"
    assert payload["service"] == "phone-bridge"
    assert payload["capabilities"] == ("health", "offline-fixtures")
    assert "sms" not in payload
    assert "camera" not in payload


def test_termux_health_endpoint() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), PhoneRequestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/health"
        response = httpx.get(url, timeout=2.0)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()
