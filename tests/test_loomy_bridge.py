#!/usr/bin/env python3
"""Dependency-light tests for the Loomy -> Code City bridge (Track 3.1)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from backend.core.loomy_bridge import (  # noqa: E402
    agent_to_building,
    build_demo_loomy_city,
    loomy_snapshot_to_city,
)

MINIMAL_SNAPSHOT = {
    "tick": 7,
    "running": True,
    "elapsed_seconds": 0.42,
    "agent_count": 2,
    "alive_count": 2,
    "state_keys": 3,
    "agents": [
        {"agent_id": "scout-1", "role": "scout", "alive": True,
         "bearing_glyph": "◇", "speed": 7, "tick_count": 4},
        {"agent_id": "watchdog-1", "role": "watchdog", "alive": False,
         "bearing_glyph": "○", "speed": 5, "tick_count": 9},
    ],
}


class LoomyBridgeContractTests(unittest.TestCase):
    def test_snapshot_to_city_maps_each_agent_to_a_building(self) -> None:
        city = loomy_snapshot_to_city(MINIMAL_SNAPSHOT)

        self.assertEqual(city["total_files"], 2)
        self.assertEqual(city["total_errors"], 0)
        self.assertEqual(city["root_path"], "loomy://runtime")
        self.assertEqual(city["source"], "loomy.snapshot()")
        self.assertEqual(len(city["buildings"]), 2)
        self.assertEqual(city["loomy"]["tick"], 7)
        self.assertEqual(city["loomy"]["agent_count"], 2)
        self.assertEqual(city["loomy"]["alive_count"], 2)
        self.assertEqual(city["loomy"]["state_keys"], 3)

    def test_building_contract_fields_match_scanner_shape(self) -> None:
        building = agent_to_building(MINIMAL_SNAPSHOT["agents"][0])

        # Fields the frontend renderCity()/createBuilding() read.
        for key in ("id", "name", "path", "full_path", "type", "size",
                    "lines", "complexity", "health", "position",
                    "dimensions", "color", "bloat_report", "syntax_insights"):
            self.assertIn(key, building)

        self.assertEqual(building["name"], "scout-1")
        self.assertEqual(building["type"], "scout")
        self.assertIn("x", building["position"])
        self.assertIn("z", building["position"])
        for dim in ("width", "height", "depth"):
            self.assertIn(dim, building["dimensions"])
        self.assertIn("loomy_agent", building)
        self.assertEqual(building["loomy_agent"]["speed"], 7)
        self.assertEqual(building["loomy_agent"]["bearing_glyph"], "◇")

    def test_positions_are_stable_and_deterministic(self) -> None:
        a = agent_to_building({"agent_id": "weaver-1", "role": "weaver",
                               "speed": 5, "alive": True, "tick_count": 2})
        b = agent_to_building({"agent_id": "weaver-1", "role": "weaver",
                               "speed": 5, "alive": True, "tick_count": 2})
        self.assertEqual(a["position"], b["position"])
        # Different agents land on different lots (crc32 spread).
        c = agent_to_building({"agent_id": "scout-1", "role": "scout",
                               "speed": 7, "alive": True, "tick_count": 1})
        self.assertNotEqual(a["position"], c["position"])

    def test_halted_agent_is_flagged_and_loses_health(self) -> None:
        building = agent_to_building(MINIMAL_SNAPSHOT["agents"][1])

        self.assertEqual(building["health"], 25)
        self.assertTrue(building["bloat_report"]["Triggered"])
        self.assertEqual(building["bloat_report"]["Message"], "agent halted")
        self.assertFalse(building["loomy_agent"]["alive"])

    def test_demo_city_builds_a_real_swarm(self) -> None:
        city = build_demo_loomy_city(ticks=3)

        self.assertGreaterEqual(city["total_files"], 3)  # scout+weaver+dismantler
        roles = {b["type"] for b in city["buildings"]}
        self.assertIn("scout", roles)
        self.assertIn("weaver", roles)
        # Every building carries the loomy_agent marker for the frontend.
        self.assertTrue(all("loomy_agent" in b for b in city["buildings"]))


if __name__ == "__main__":
    unittest.main()
