"""Email-as-filesystem renderer (GCM-WQ-013). Offline by default."""
from __future__ import annotations

from email.message import EmailMessage
from pathlib import Path

BUS_TO = ["james.wilson.otr@gmail.com", "olivia.mae.blackwell@gmail.com"]


def subject(verb: str, yyyymmdd: str, slug: str) -> str:
    return f"[GROKBOT] [CILIA-BUS] [FROM-O-HEAVY] [MCP-EVENT] [PRI-MED] MINER-{verb.upper()}-{yyyymmdd}-{slug}-001"


def render_body(msg_id: str, header: str, toc: str, omissions: str, turns: str,
                drive: str, req: str, delta: str) -> str:
    return (
        f"/{msg_id}/\n"
        f"  00_HEADER\n{indent(header)}\n"
        f"  01_TOC\n{indent(toc)}\n"
        f"  02_OMISSIONS\n{indent(omissions)}\n"
        f"  03_TURNS\n{indent(turns)}\n"
        f"  04_DRIVE\n{indent(drive)}\n"
        f"  05_REQ\n{indent(req)}\n"
        f"  06_DELTA\n{indent(delta)}\n"
    )


def indent(text: str, n: int = 4) -> str:
    pad = " " * n
    return "\n".join(pad + line if line else line for line in text.strip("\n").splitlines())


def build_message(verb: str, yyyymmdd: str, slug: str, body: str, msg_id: str) -> EmailMessage:
    m = EmailMessage()
    m["To"] = ", ".join(BUS_TO)
    m["Subject"] = subject(verb, yyyymmdd, slug)
    m["X-GCM-Msg-Id"] = msg_id
    m["X-GCM-Verb"] = verb
    m.set_content(body)
    return m


def write_outbox(path: Path, message: EmailMessage) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(message.as_string())
    return path
