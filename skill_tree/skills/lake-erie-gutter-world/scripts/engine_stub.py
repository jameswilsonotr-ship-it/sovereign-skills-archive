#!/usr/bin/env python3
"""
Lake Erie Gutter World - Time-Bus Kernel Stub
Phase 1 implementation for the lake-erie-gutter-world skill.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

class TimeBusKernel:
    def __init__(self, state_path="data/state.json"):
        self.state_path = Path(state_path)
        self.state = self._load_state()

    def _load_state(self):
        if self.state_path.exists():
            with open(self.state_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "current_time": "2026-06-17T18:00:00Z",
                "current_season": "summer",
                "tick_count": 0,
                "active_events": [],
                "character_heat": {}
            }

    def _save_state(self):
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)

    def tick(self, hours: int = 12):
        """Advance simulation time."""
        current = datetime.fromisoformat(self.state["current_time"].replace("Z", "+00:00"))
        new_time = current + timedelta(hours=hours)
        self.state["current_time"] = new_time.isoformat().replace("+00:00", "Z")
        self.state["tick_count"] += 1

        # Simple heat decay simulation (stub)
        for char_id in list(self.state.get("character_heat", {}).keys()):
            current_heat = self.state["character_heat"][char_id]
            decay = max(0.5, current_heat * 0.03)  # 3% decay per tick minimum
            self.state["character_heat"][char_id] = round(max(1, current_heat - decay), 1)

        self._save_state()
        return {
            "new_time": self.state["current_time"],
            "tick_count": self.state["tick_count"],
            "message": f"Advanced {hours} hours. Heat values decayed slightly."
        }

    def get_status(self):
        return {
            "current_time": self.state["current_time"],
            "current_season": self.state.get("current_season", "summer"),
            "tick_count": self.state["tick_count"],
            "active_characters": len(self.state.get("character_heat", {}))
        }


if __name__ == "__main__":
    kernel = TimeBusKernel()
    result = kernel.tick(12)
    print(json.dumps(result, indent=2))
    print("\nCurrent Status:")
    print(json.dumps(kernel.get_status(), indent=2))