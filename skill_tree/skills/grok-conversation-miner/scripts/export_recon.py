"""L8 xAI export recon — flag only. Export is not SSoT."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def index_export(payload: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    convos = payload.get("conversations") or payload.get("conversation") or []
    if isinstance(convos, dict):
        convos = list(convos.values())
    for c in convos:
        if isinstance(c, dict):
            for k in ("id", "conversation_id", "uuid"):
                if c.get(k):
                    ids.add(str(c[k]))
    assets = payload.get("assets") or []
    for a in assets:
        if isinstance(a, dict) and a.get("id"):
            ids.add(str(a["id"]))
        elif isinstance(a, str):
            ids.add(a)
    return ids


def _as_idset(obj) -> set[str]:
    from pathlib import Path as P
    import json as _json
    if obj is None:
        return set()
    if isinstance(obj, (set, list, tuple)):
        return set(map(str, obj))
    p = P(obj)
    if p.exists():
        data = _json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return set(map(str, data))
        return index_export(data)
    return set()


def recon(export_ids, lake_ids=None, sunset_ids=None):
    e = _as_idset(export_ids)
    l = _as_idset(lake_ids)
    s = _as_idset(sunset_ids)
    if sunset_ids is None:
        s = l
    return {
        "IN_LAKE": sorted(e & l),
        "IN_EXPORT_ONLY": sorted(e - l - s),
        "IN_SUNSET_ONLY": sorted(s - e),
        "ASSET_MISSING": sorted((l - e)),
    }


def recon_sets(export_ids: set[str], lake_ids: set[str], sunset_ids: set[str]) -> dict[str, list[str]]:
    return {
        "IN_LAKE": sorted(export_ids & lake_ids),
        "IN_EXPORT_ONLY": sorted(export_ids - lake_ids - sunset_ids),
        "IN_SUNSET_ONLY": sorted(sunset_ids - export_ids),
        "ASSET_MISSING": sorted(lake_ids - export_ids),
    }


def render(date: str, table: dict[str, list[str]]) -> str:
    lines = [f"# EXPORT_RECON_{date}", "", "xAI export is recon, not SSoT.", ""]
    for k, v in table.items():
        lines.append(f"## {k} ({len(v)})")
        lines.extend(f"- `{i}`" for i in v) if v else lines.append("- (none)")
        lines.append("")
    return "\n".join(lines)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())
