#!/data/data/com.termux/files/usr/bin/sh
# termux-services foreground runner for the offline phone health bridge.
set -eu

ROOT=${PHONE_MCP_ROOT:-"$HOME/sovereign-skills-archive"}
PYTHON=${PHONE_MCP_PYTHON:-"$ROOT/harness/.venv/bin/python"}
PORT=${PHONE_MCP_PORT:-8081}

if [ ! -x "$PYTHON" ]; then
    PYTHON=python
fi

if ! command -v tailscale >/dev/null 2>&1; then
    echo "tailscale is required; refusing to bind outside the tailnet" >&2
    exit 1
fi

set -- $(tailscale ip -4)
TAILNET_IP=${PHONE_MCP_HOST:-${1:-}}
case "$TAILNET_IP" in
    100.*) ;;
    *)
        echo "no IPv4 Tailscale address found; refusing to start" >&2
        exit 1
        ;;
esac

export PYTHONPATH="$ROOT/harness/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$PYTHON" -m sovereign_harness.phone_mcp \
    --host "$TAILNET_IP" \
    --port "$PORT"
