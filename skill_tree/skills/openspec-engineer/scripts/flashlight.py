"""Offline, read-only pytest flashlight with a default-deny network guard."""
from __future__ import annotations

import argparse
import contextlib
import os
import socket
from collections.abc import Iterator, Sequence
from typing import Callable

try:
    from .audit_log import AuditLogger, redact
except ImportError:  # pragma: no cover - supports direct script execution
    from audit_log import AuditLogger, redact


class OfflineNetworkError(RuntimeError):
    """Raised when a test attempts to use a network operation."""


@contextlib.contextmanager
def network_guard(
    audit: AuditLogger,
    *,
    allow_network: bool = False,
) -> Iterator[None]:
    """Deny network primitives for the duration of a local test run."""
    if allow_network:
        audit.record("network.guard", status="allowed", policy="explicit_opt_in")
        yield
        return

    audit.record("network.guard", status="denied", policy="default_deny")

    def deny(operation: str, target: object = "") -> Callable[..., object]:
        def blocked(*_: object, **__: object) -> object:
            safe_target = redact(str(target))
            audit.record(
                "network.blocked",
                status="denied",
                operation=operation,
                target=safe_target,
            )
            raise OfflineNetworkError(
                f"offline policy denied {operation} for {safe_target}"
            )

        return blocked

    original = {
        "connect": socket.socket.connect,
        "connect_ex": socket.socket.connect_ex,
        "create_connection": socket.create_connection,
        "getaddrinfo": socket.getaddrinfo,
        "gethostbyname": socket.gethostbyname,
        "gethostbyname_ex": socket.gethostbyname_ex,
    }
    socket.socket.connect = deny("socket.connect")  # type: ignore[assignment]
    socket.socket.connect_ex = deny("socket.connect_ex")  # type: ignore[assignment]
    socket.create_connection = deny("socket.create_connection")  # type: ignore[assignment]
    socket.getaddrinfo = deny("socket.getaddrinfo")  # type: ignore[assignment]
    socket.gethostbyname = deny("socket.gethostbyname")  # type: ignore[assignment]
    socket.gethostbyname_ex = deny("socket.gethostbyname_ex")  # type: ignore[assignment]
    try:
        yield
    finally:
        socket.socket.connect = original["connect"]  # type: ignore[assignment]
        socket.socket.connect_ex = original["connect_ex"]  # type: ignore[assignment]
        socket.create_connection = original["create_connection"]  # type: ignore[assignment]
        socket.getaddrinfo = original["getaddrinfo"]  # type: ignore[assignment]
        socket.gethostbyname = original["gethostbyname"]  # type: ignore[assignment]
        socket.gethostbyname_ex = original["gethostbyname_ex"]  # type: ignore[assignment]


def run_pytest(
    paths: Sequence[str],
    *,
    audit: AuditLogger | None = None,
    allow_network: bool = False,
    pytest_args: Sequence[str] = (),
) -> int:
    """Run pytest in-process under the offline policy and return its exit code."""
    logger = audit or AuditLogger()
    requested_paths = list(paths) or ["tests"]
    logger.record(
        "flashlight.start",
        status="started",
        paths=requested_paths,
        network_policy="allow" if allow_network else "deny",
    )
    previous_autoload = os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD")
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    try:
        try:
            import pytest
        except ImportError as exc:
            logger.record("flashlight.complete", status="error", error=str(exc))
            return 2

        args = ["-q", *pytest_args, *requested_paths]
        with network_guard(logger, allow_network=allow_network):
            exit_code = int(pytest.main(args))
        logger.record("flashlight.complete", status="passed" if exit_code == 0 else "failed",
                      exit_code=exit_code)
        return exit_code
    except OfflineNetworkError as exc:
        logger.record("flashlight.complete", status="denied", error=str(exc))
        return 3
    except BaseException as exc:
        logger.record("flashlight.complete", status="error", error=str(exc))
        raise
    finally:
        if previous_autoload is None:
            os.environ.pop("PYTEST_DISABLE_PLUGIN_AUTOLOAD", None)
        else:
            os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = previous_autoload


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pytest locally with network access denied by default."
    )
    parser.add_argument("paths", nargs="*", help="pytest paths; defaults to tests")
    parser.add_argument(
        "--audit-log",
        metavar="PATH",
        help="append redacted JSONL events to PATH; '-' writes to stderr",
    )
    parser.add_argument(
        "--allow-network",
        action="store_true",
        help="explicitly opt out of the default-deny network guard",
    )
    parser.add_argument(
        "--pytest-arg",
        action="append",
        default=[],
        help="pass one additional argument to pytest (repeatable)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    with AuditLogger(args.audit_log) as audit:
        return run_pytest(
            args.paths,
            audit=audit,
            allow_network=args.allow_network,
            pytest_args=args.pytest_arg,
        )


if __name__ == "__main__":
    raise SystemExit(main())
