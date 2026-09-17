"""Spoken emotion verbs → PAD axis math + NRC tag names."""
from __future__ import annotations
EMOTIONS = {
    "sad": {"axis": "low pleasure", "sort": ("pleasure", "ASC"), "p": ("lt", 0.20), "nrc": "sadness",
            "aliases": ["sad", "sadness", "down", "blue", "hurt", "sour", "unhappy"]},
    "happy": {"axis": "high pleasure", "sort": ("pleasure", "DESC"), "p": ("gt", 0.50), "nrc": "joy",
              "aliases": ["happy", "glad", "joy", "joyful", "good", "sweet", "cheerful"]},
    "hot": {"axis": "high arousal", "sort": ("arousal", "DESC"), "a": ("gt", 0.78), "nrc": "anticipation",
            "aliases": ["hot", "horny", "intense", "amped", "wired", "aroused", "heat"]},
    "calm": {"axis": "low arousal", "sort": ("arousal", "ASC"), "a": ("lt", 0.55),
             "aliases": ["calm", "quiet", "soft", "still", "peaceful"]},
    "bored": {"axis": "low arousal + mid pleasure", "sort": ("arousal", "ASC"), "a": ("lt", 0.55),
              "p": ("gt", 0.15), "p2": ("lt", 0.45), "aliases": ["bored", "flat", "meh", "numb"]},
    "overwhelmed": {"axis": "low dominance + high arousal", "sort": ("dominance", "ASC"),
                    "d": ("lt", 0.15), "a": ("gt", 0.65), "nrc": "fear",
                    "aliases": ["overwhelmed", "scared", "spinning", "flooded", "small"]},
    "claimed": {"axis": "high dominance", "sort": ("dominance", "DESC"), "d": ("gt", 0.45),
                "aliases": ["claimed", "powerful", "in-control", "dominant", "in control"]},
    "tender": {"axis": "high pleasure + mid/low arousal", "sort": ("pleasure", "DESC"),
               "p": ("gt", 0.40), "a": ("lt", 0.70), "nrc": "trust",
               "aliases": ["tender", "soft-love", "nesting", "gentle"]},
    "angry": {"axis": "low pleasure + high arousal", "sort": ("pleasure", "ASC"),
              "p": ("lt", 0.15), "a": ("gt", 0.65), "nrc": "anger",
              "aliases": ["angry", "mad", "fight", "sharp", "pissed"]},
    "lonely": {"axis": "low pleasure + low dominance", "sort": ("pleasure", "ASC"),
               "p": ("lt", 0.25), "d": ("lt", 0.25), "aliases": ["lonely", "alone", "isolated"]},
    "afraid": {"axis": "high fear (NRC) / low dominance", "sort": ("dominance", "ASC"),
               "d": ("lt", 0.20), "nrc": "fear", "aliases": ["afraid", "fear", "fearful", "anxious", "worry"]},
    "trusting": {"axis": "high trust (NRC) / mid-high pleasure", "sort": ("pleasure", "DESC"),
                 "p": ("gt", 0.30), "nrc": "trust", "aliases": ["trusting", "trust", "safe"]},
    "disgusted": {"axis": "high disgust (NRC) / low pleasure", "sort": ("pleasure", "ASC"),
                  "p": ("lt", 0.25), "nrc": "disgust", "aliases": ["disgusted", "disgust", "gross"]},
    "surprised": {"axis": "high surprise (NRC) / high arousal", "sort": ("arousal", "DESC"),
                  "a": ("gt", 0.70), "nrc": "surprise", "aliases": ["surprised", "surprise", "shocked"]},
    "anticipating": {"axis": "high anticipation (NRC)", "sort": ("arousal", "DESC"),
                     "nrc": "anticipation", "aliases": ["anticipating", "anticipation", "hungry", "waiting"]},
}
def resolve(word):
    w = (word or "").strip().lower().replace("_", " ")
    if not w:
        return None, None
    for name, spec in EMOTIONS.items():
        if w == name or w in spec["aliases"]:
            return name, spec
    return None, None
def _ok(val, rule):
    if val is None or rule is None:
        return True
    op, thr = rule
    return val < thr if op == "lt" else val > thr if op == "gt" else True
def matches(pad, spec):
    p = pad.get("pleasure") if pad else None
    a = pad.get("arousal") if pad else None
    d = pad.get("dominance") if pad else None
    return _ok(p, spec.get("p")) and _ok(p, spec.get("p2")) and _ok(a, spec.get("a")) and _ok(d, spec.get("d"))
def sort_key(row, spec):
    axis, direction = spec.get("sort") or ("pleasure", "ASC")
    val = (row.get("pad_mean") or {}).get(axis) or 0.0
    return val if direction == "ASC" else -val
