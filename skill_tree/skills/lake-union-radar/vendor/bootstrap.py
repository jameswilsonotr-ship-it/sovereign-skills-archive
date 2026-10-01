"""Put vendored site-packages on sys.path."""
from __future__ import annotations
import sys
from pathlib import Path
SITE = Path(__file__).resolve().parent / "site-packages"
def load() -> Path:
    p = str(SITE)
    if SITE.is_dir() and p not in sys.path:
        sys.path.insert(0, p)
    return SITE
