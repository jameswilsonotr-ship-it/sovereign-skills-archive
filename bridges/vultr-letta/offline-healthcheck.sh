#!/usr/bin/env bash
#
# Validate the local Compose contract without starting containers or making
# network calls. This intentionally does not run curl, nc, tailscale, or ssh.
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
compose_file="${COMPOSE_FILE:-}"

usage() {
  printf 'Usage: %s [COMPOSE_FILE]\n' "$0" >&2
}

if [[ $# -gt 1 ]]; then
  usage
  exit 2
fi

if [[ $# -eq 1 ]]; then
  compose_file="$1"
fi

if [[ -z "$compose_file" ]]; then
  for candidate in \
    "$script_dir/docker-compose.yml" \
    "$script_dir/docker-compose.yaml" \
    "$script_dir/compose.yml" \
    "$script_dir/compose.yaml"; do
    if [[ -f "$candidate" ]]; then
      compose_file="$candidate"
      break
    fi
  done
fi

if [[ -z "$compose_file" || ! -f "$compose_file" ]]; then
  printf 'offline healthcheck: no Compose file found; failing closed\n' >&2
  exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  printf 'offline healthcheck: docker is required\n' >&2
  exit 2
fi

if ! docker compose version >/dev/null 2>&1; then
  printf 'offline healthcheck: Docker Compose is required\n' >&2
  exit 2
fi

compose_error="$(mktemp)"
config_json="$(mktemp)"
trap 'rm -f "$compose_error" "$config_json"' EXIT

# Do not print Compose diagnostics: interpolation can contain operator-provided
# values. The validator only reports the result, never the rendered config.
if ! docker compose -f "$compose_file" config --quiet \
  >/dev/null 2>"$compose_error"; then
  printf 'offline healthcheck: Compose config is invalid\n' >&2
  exit 1
fi

if ! docker compose -f "$compose_file" config --format json \
  >"$config_json" 2>"$compose_error"; then
  printf 'offline healthcheck: could not render Compose config as JSON\n' >&2
  exit 1
fi

python3 - "$config_json" <<'PY'
import json
import sys


def fail(message):
    print(f"offline healthcheck: {message}", file=sys.stderr)
    raise SystemExit(1)


try:
    with open(sys.argv[1], encoding="utf-8") as rendered:
        config = json.load(rendered)
except (OSError, json.JSONDecodeError):
    fail("rendered Compose config is not valid JSON")

services = config.get("services")
if not isinstance(services, dict):
    fail("rendered Compose config has no services")

expected_ports = {"ollama": 11434, "letta": 8283}

for service_name, expected_port in expected_ports.items():
    service = services.get(service_name)
    if not isinstance(service, dict):
        fail(f"required service {service_name!r} is missing")

    healthcheck = service.get("healthcheck")
    test = healthcheck.get("test") if isinstance(healthcheck, dict) else None
    if not test or test == "NONE" or test == ["NONE"]:
        fail(f"service {service_name!r} has no enabled healthcheck")

    ports = service.get("ports", [])
    if not isinstance(ports, list):
        fail(f"service {service_name!r} has an unreadable ports declaration")

    matching_ports = []
    for port in ports:
        if not isinstance(port, dict):
            continue
        try:
            target = int(port.get("target"))
        except (TypeError, ValueError):
            continue
        if target != expected_port or str(port.get("protocol", "tcp")).lower() != "tcp":
            continue
        matching_ports.append(port)

    if not matching_ports:
        fail(
            f"service {service_name!r} must declare TCP container port "
            f"{expected_port}"
        )

    for port in matching_ports:
        if port.get("published") is None:
            continue
        host_ip = str(port.get("host_ip", "")).strip().lower()
        if host_ip in {"", "0.0.0.0", "::", "[::]"}:
            fail(
                f"service {service_name!r} publishes {expected_port} on a "
                "wildcard host address"
            )

print("offline healthcheck: Compose contract is valid")
PY
