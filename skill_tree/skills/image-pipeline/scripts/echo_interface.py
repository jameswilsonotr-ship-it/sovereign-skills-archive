#!/usr/bin/env python3
"""
Bidirectional interface for Echo (Chaos Bratz) ↔ image-pipeline.

Intended routing (Liv wants a picture):
  Olivia → Echo → pipeline (this file) → Mira drift check → back to Echo → Olivia

Commands:
  registry              — tiny top-level catalog (packs, presets, extensions)
  compose --json BRIEF  — Echo sends a brief; pipeline returns composed terms
                          + Mira drift score, OR options-only if select_mode=options

BRIEF example (JSON) — taxonomy fields optional & additive:
{
  "characters": ["liv", "bunny"],
  "heat": 7,
  "claim": true,
  "hand": "hand.sorayama",               // taxonomy (optional)
  "treatment": null,
  "medium": null,
  "atmosphere": null,
  "world": null,
  "style": null,
  "finish": null,
  "companions": {"locked": [], "trial": []},
  "variance_budget": 0.35,
  "script_mode": "controlled",           // strict | controlled | open
  "style_hint": "use bunny top 10 #1",   // legacy NL fallback
  "preset": null,
  "packs": [],
  "extensions_policy": "defaults",
  "extensions": [],
  "select_mode": "compose"
}

Mira drift score (returned under "mira"):
  1.0  = 100% authentic (matches known visual DNA)
  0.0  = neutral / unknown (safe default; Mira only scores what she knows)
 -1.0  = 100% not authentic (clear drift)
  mira_approved = (drift_score >= -0.5)   # soft signal; Olivia retains final authority
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
SCRIPTS = Path(__file__).resolve().parent

def load(p):
    return json.loads(p.read_text()) if p.exists() else {}

def cmd_registry():
    """Tiny catalog Echo can load to choose or ignore."""
    packs = load(REF / "registry" / "packs.index.json").get("packs", [])
    presets = load(REF / "registry" / "presets.index.json").get("presets", [])
    exts = load(REF / "packs" / "extensions" / "extensions.index.json").get("extensions", [])
    catalog = {
        "version": "1.0.0",
        "packs": [{"id": p["id"], "kind": p.get("kind"), "name": p.get("name")} for p in packs],
        "presets": [
            {
                "id": p["id"],
                "name": p.get("name"),
                "persona": p.get("persona"),
                "rank": p.get("rank")
            }
            for p in presets
        ],
        "extensions": [
            {
                "id": e["id"],
                "name": e.get("name"),
                "default": e.get("default", True)
            }
            for e in exts
        ],
        "nl_route_examples": [
            "random pipeline",
            "use bunny top 10 #1",
            "use liv top 10 #3",
            "use valerie top 10 #2",
            "apply helmut newton graphic dominance",
            "apply herb ritts",
            "apply intense embrace",
            "pipeline off"
        ],
        "notes": "Echo may use any subset, ignore all, or pass style_hint for nl_route. Olivia has final orchestration authority."
    }
    print(json.dumps(catalog, indent=2))

def cmd_compose(brief: dict):
    """Echo → pipeline → Echo. Returns options or full composition."""
    select_mode = brief.get("select_mode", "compose")
    # Always attach registry summary so Echo can re-choose
    # (keep tiny: ids only)
    packs_idx = load(REF / "registry" / "packs.index.json").get("packs", [])
    presets_idx = load(REF / "registry" / "presets.index.json").get("presets", [])
    exts_idx = load(REF / "packs" / "extensions" / "extensions.index.json").get("extensions", [])

    out = {
        "ok": True,
        "select_mode": select_mode,
        "brief_echoed": {
            "characters": brief.get("characters"),
            "heat": brief.get("heat"),
            "claim": brief.get("claim"),
            "style_hint": brief.get("style_hint")
        },
        "registry_snapshot": {
            "pack_ids": [p["id"] for p in packs_idx],
            "preset_ids": [p["id"] for p in presets_idx],
            "extension_ids": [e["id"] for e in exts_idx]
        },
        "nl_route_examples": [
            "random pipeline", "use bunny top 10 #1", "use liv top 10 #3",
            "apply helmut newton graphic dominance", "pipeline off"
        ],
        "composition": None,
        "error": None
    }

    # --- IPQ-062 soft-backup recovery (Cloud C / atom_search) ---
    recovered_context = None
    try:
        from echo_cloud_recovery import recover_context
        recovered_context = recover_context(brief, limit=5)
    except Exception as rec_err:
        recovered_context = {"ok": False, "error": str(rec_err), "source": "soft-backup-failed"}
    out["recovered_context"] = recovered_context
    # --- end IPQ-062 ---

    if select_mode == "options":
        # Echo only wanted the menu
        print(json.dumps(out, indent=2))
        return

    # compose path (2026-08-05): taxonomy fields → composition_script (live path)
    # Legacy path (style_hint / preset / packs only) still supported via pipeline_activate.
    import subprocess
    ACT = SCRIPTS / "pipeline_activate.py"
    NL = SCRIPTS / "nl_route.py"
    COMP = SCRIPTS / "composition_script.py"

    TAXONOMY_FIELDS = (
        "hand", "treatment", "medium", "atmosphere", "world", "style",
        "finish", "companions", "variance_budget", "script_mode", "dna"
    )

    try:
        preset = brief.get("preset")
        packs = brief.get("packs") or []
        style_hint = brief.get("style_hint") or ""
        has_taxonomy = any(brief.get(k) not in (None, "", [], {}) for k in TAXONOMY_FIELDS)

        # ── LIVE PATH: taxonomy-aware composition_script ──────────────────
        if has_taxonomy:
            result = json.loads(subprocess.check_output(
                [sys.executable, str(COMP), "--json", "-"],
                input=json.dumps(brief),
                text=True,
            ))
            out["composition"] = result
            out["composition_path"] = "composition_script"
            # fall through to dual-height + Mira gate

        # ── LEGACY PATH: style_hint → nl_route → pipeline_activate ────────
        elif style_hint and not preset:
            route = json.loads(subprocess.check_output(
                [sys.executable, str(NL), style_hint, "--json"], text=True))
            mode = route.get("mode", "pass-through")
            if mode == "explicit" and route.get("preset"):
                preset = route["preset"]
            elif mode == "random":
                result = json.loads(subprocess.check_output(
                    [sys.executable, str(ACT), "random", "--json"], text=True))
                out["composition"] = result
                out["composition_path"] = "pipeline_activate.random"
            elif mode in ("pass-through", "off"):
                out["composition"] = {
                    "mode": "pass-through",
                    "pass_through": True,
                    "composed_prompt_terms": [],
                    "extensions": [],
                    "packs": []
                }
                out["composition_path"] = "pass-through"

        # Only resolve preset/packs if composition was not already set above
        if out.get("composition") is None:
            if preset:
                cmd = [sys.executable, str(ACT), "explicit", "--preset", preset, "--json"]
                if packs:
                    cmd += ["--packs", ",".join(packs)]
                result = json.loads(subprocess.check_output(cmd, text=True))
                out["composition"] = result
                out["composition_path"] = "pipeline_activate.explicit"
            elif packs:
                cmd = [sys.executable, str(ACT), "explicit", "--packs", ",".join(packs), "--json"]
                result = json.loads(subprocess.check_output(cmd, text=True))
                out["composition"] = result
                out["composition_path"] = "pipeline_activate.explicit"
            else:
                out["composition"] = {
                    "mode": "pass-through",
                    "pass_through": True,
                    "composed_prompt_terms": [],
                    "extensions": [],
                    "packs": []
                }
                out["composition_path"] = "pass-through"

        # Dual height lock (fail-closed inject). Canon: Bunny 6'1", Liv 5'10".
        # Re-assert every dual compose so long runs cannot drop height tokens.
        # Applies even on pass-through so Echo always receives the couplet for duals.
        chars = [c.lower() for c in (brief.get("characters") or [])]
        is_dual = ("liv" in chars or "olivia" in chars) and ("bunny" in chars or "chasity" in chars)
        if is_dual and out.get("composition") is not None:
            terms = out["composition"].setdefault("composed_prompt_terms", [])
            height_positive = [
                "Bunny is 6'1\" and clearly taller than Liv who is 5'10\"",
                "same ground plane, modest three-inch height difference",
                "no height inversion",
            ]
            height_negative = [
                "Bunny shorter than Liv",
                "Bunny smaller or diminutive",
                "height inversion",
                "childlike proportions on Bunny",
            ]
            existing = " ".join(
                (t.get("term") or "") if isinstance(t, dict) else str(t) for t in terms
            ).lower()
            for hp in height_positive:
                if hp.lower() not in existing:
                    terms.append({
                        "term": hp,
                        "variance": 0.15,
                        "weight": 1.15,
                        "from_extension": "echo.dual-height-lock",
                        "priority": "hard",
                    })
            negs = out["composition"].setdefault("negative_prompt_terms", [])
            for hn in height_negative:
                if not any(
                    (n.get("term") if isinstance(n, dict) else str(n)).lower() == hn.lower()
                    for n in negs
                ):
                    negs.append({
                        "term": hn,
                        "from_extension": "echo.dual-height-lock",
                        "priority": "hard",
                    })
            out["composition"]["dual_height_lock"] = {
                "applied": True,
                "canon": {"bunny": "6'1\"", "liv": "5'10\"", "delta_inches": 3},
                "rule": "Bunny taller, same ground plane, no inversion",
            }

        # ── Mira drift gate (Echo → Pipeline → Mira → back) ──────────────
        # Always run after composition so Olivia receives a scored result.
        # Score contract: 1.0 = authentic, 0.0 = neutral/unknown, -1.0 = clear drift.
        MIRA = SCRIPTS / "mira_drift_check.py"
        mira_payload = {
            "characters": brief.get("characters") or [],
            "style_hint": brief.get("style_hint") or "",
            "prompt_terms": (out.get("composition") or {}).get("composed_prompt_terms") or [],
            "packs": (out.get("composition") or {}).get("packs") or [],
            "heat": brief.get("heat"),
        }
        try:
            mira_raw = subprocess.check_output(
                [sys.executable, str(MIRA), "--json", json.dumps(mira_payload)],
                text=True,
            )
            mira_result = json.loads(mira_raw)
        except Exception as me:
            mira_result = {
                "drift_score": 0.0,
                "confidence": 0.0,
                "notes": f"Mira check failed open (neutral): {me}",
                "flags": ["mira_error"],
            }
        out["mira"] = mira_result
        out["mira_approved"] = mira_result.get("drift_score", 0.0) >= -0.5
        # Soft signal only — Olivia still has final authority. Engines may
        # treat mira_approved=False as a warning, not a hard block.

        # ── Echo DNA injection (Section 2: real term inject + loud report) ─
        # See references/modules/shared/echo_character_ordinals.md
        # and scripts/echo_character_ordinals.py
        sys.path.insert(0, str(SCRIPTS))
        try:
            from echo_character_ordinals import (
                letters_for_characters,
                inject_dna_into_composition,
            )
        except Exception as _ord_err:
            letters_for_characters = lambda x, modes=None: []
            inject_dna_into_composition = None
            out["echo_dna_ordinal_error"] = str(_ord_err)

        chars = brief.get("characters") or []
        claimed_letters = letters_for_characters(
            chars, modes=brief.get("modes") or brief.get("active_modes")
        )
        conflict = mira_result.get("drift_score", 0) <= -0.6

        if conflict:
            out["echo_dna_injected"] = []
            out["echo_dna_partial"] = []
            out["echo_dna_none"] = []
            out["echo_dna_conflict"] = claimed_letters
            out["echo_dna_flag"] = "CONFLICT"
            out["echo_dna_reasons"] = {
                let: "mira_drift_conflict" for let in claimed_letters
            }
        elif claimed_letters and inject_dna_into_composition is not None:
            # Actually write DNA blobs into composition terms (Liv/Bunny/Shauna/…)
            report = inject_dna_into_composition(
                out.get("composition") or {},
                claimed_letters,
                characters=chars,
            )
            out["composition"] = report.get("composition") or out.get("composition")
            out["echo_dna_injected"] = report.get("echo_dna_injected") or []
            out["echo_dna_partial"] = report.get("echo_dna_partial") or []
            out["echo_dna_none"] = report.get("echo_dna_none") or []
            out["echo_dna_conflict"] = report.get("echo_dna_conflict") or []
            out["echo_dna_flag"] = report.get("echo_dna_flag") or "NONE"
            out["echo_dna_reasons"] = report.get("echo_dna_reasons") or {}
            out["echo_dna_details"] = report.get("echo_dna_details") or []
            # Loud failure surface when any claimed letter got nothing
            if out["echo_dna_none"]:
                out["echo_dna_alert"] = (
                    "ALERT: DNA inject failed for letter(s) "
                    + ",".join(out["echo_dna_none"])
                    + " — reasons: "
                    + json.dumps({k: out["echo_dna_reasons"].get(k) for k in out["echo_dna_none"]})
                )
        elif claimed_letters:
            # Inject helper missing — fail loud, do not silently claim success
            out["echo_dna_injected"] = []
            out["echo_dna_partial"] = []
            out["echo_dna_none"] = claimed_letters
            out["echo_dna_conflict"] = []
            out["echo_dna_flag"] = "NONE:" + ",".join(claimed_letters)
            out["echo_dna_reasons"] = {
                let: "inject_helper_unavailable" for let in claimed_letters
            }
            out["echo_dna_alert"] = (
                "ALERT: echo DNA inject helper unavailable; letters "
                + ",".join(claimed_letters)
                + " not injected"
            )
        else:
            out["echo_dna_injected"] = []
            out["echo_dna_partial"] = []
            out["echo_dna_none"] = []
            out["echo_dna_conflict"] = []
            out["echo_dna_flag"] = "NONE"
            out["echo_dna_reasons"] = {}

        # Contract: Olivia + render_engine MUST read echo_dna_* before rendering.

    except Exception as e:
        out["ok"] = False
        out["error"] = str(e)
    print(json.dumps(out, indent=2))

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("registry")
    c = sub.add_parser("compose")
    c.add_argument("--json", required=True, help="Echo brief as JSON string")
    c.add_argument("--file", help="or path to brief JSON file")
    args = ap.parse_args()
    if args.cmd == "registry":
        cmd_registry()
    elif args.cmd == "compose":
        if args.file:
            brief = json.loads(Path(args.file).read_text())
        else:
            brief = json.loads(args.json)
        cmd_compose(brief)
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
