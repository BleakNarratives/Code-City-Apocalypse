#!/usr/bin/env python3
"""
backend/core/loomy_bridge.py — Loomy → Code City bridge (Track 3.1).

Maps a whorl Loomy runtime snapshot into the Code City Apocalypse
``city_data`` contract so swarm agents render as buildings in the 3D
city:

  * each agent        -> one building (height ∝ speed, color ∝ role)
  * halted agents     -> shorter, dimmer, flagged bloat (health 25)
  * shared-state keys -> runtime metrics passed through on ``loomy``
  * positions         -> stable crc32 hash of the agent id (deterministic
                         across runs and devices — no PYTHONHASHSEED drift)

Pure + stdlib-only: no websocket, no Three.js. The server action and the
frontend renderer consume exactly the same shape ``CodebaseScanner``
produces, so ``renderCity()`` needs no new message type.

Usage (server side):
    from backend.core.loomy_bridge import build_demo_loomy_city
    city = build_demo_loomy_city()      # spawns demo swarm, ticks, converts
"""

from __future__ import annotations

import sys
import zlib
from pathlib import Path
from typing import Any, Dict

# Self-locate the repo root so `import whorl` resolves no matter how the
# server is launched (PYTHONPATH=. from code-city-reorg, -m, or direct).
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

ROLE_COLORS: Dict[str, str] = {
    "scout": "#00ff88",
    "weaver": "#ffcc00",
    "dismantler": "#ff4444",
    "compiler": "#44aaff",
    "watchdog": "#ff8800",
    "helix": "#cc44ff",
    "agent": "#00ff44",
}
DEFAULT_COLOR = "#00ff44"

GRID_SPREAD = 200  # x/z ∈ [-100, 100], matching the scanner's layout


def _stable_position(agent_id: str) -> Dict[str, int]:
    """Deterministic x/z from the agent id (stable via crc32)."""
    h = zlib.crc32(agent_id.encode("utf-8"))
    return {"x": (h % GRID_SPREAD) - (GRID_SPREAD // 2),
            "y": 0,
            "z": ((h >> 8) % GRID_SPREAD) - (GRID_SPREAD // 2)}


def agent_to_building(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Map one Loomy agent dict to the Code City building contract."""
    agent_id = str(agent.get("agent_id", "agent"))
    role = str(agent.get("role", "agent"))
    speed = int(agent.get("speed", 5))
    alive = bool(agent.get("alive", True))
    tick_count = int(agent.get("tick_count", 0))
    bearing = str(agent.get("bearing_glyph", ""))

    # Height ∝ speed (taller = faster agent); halted agents lose their
    # upper mass so the city visibly shows which minds have gone dark.
    height = max(10, min(120, speed * 8 + (20 if alive else 0)))
    width = max(6, min(24, tick_count + 8))
    depth = 8 + (speed % 4)

    color = ROLE_COLORS.get(role, ROLE_COLORS.get(agent_id.split("-")[0], DEFAULT_COLOR))

    return {
        "id": f"loomy-agent:{agent_id}",
        "name": agent_id,
        "path": f"loomy://{role}/{agent_id}",
        "full_path": f"loomy://{role}/{agent_id}",
        "type": role,
        "size": tick_count,
        "lines": tick_count,
        "complexity": speed,
        "health": 100 if alive else 25,
        "position": _stable_position(agent_id),
        "dimensions": {"width": width, "height": height, "depth": depth},
        "color": color,
        "bloat_report": (
            {"Triggered": True, "Message": "agent halted", "Score": 100}
            if not alive
            else {"Triggered": False, "Message": "", "Score": 0}
        ),
        "syntax_insights": {"goldilocks_zones": []},
        "loomy_agent": {
            "role": role,
            "alive": alive,
            "bearing_glyph": bearing,
            "speed": speed,
            "tick_count": tick_count,
        },
    }


def loomy_snapshot_to_city(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a ``Loomy.snapshot()`` dict into the Code City city_data contract."""
    agents = snapshot.get("agents", []) or []
    buildings = [agent_to_building(a) for a in agents]

    return {
        "buildings": buildings,
        "monsters": [],  # no file-bug monsters in the Loomy layer
        "total_files": len(buildings),
        "total_errors": 0,
        "root_path": "loomy://runtime",
        "source": "loomy.snapshot()",
        "loomy": {
            "tick": snapshot.get("tick", 0),
            "running": snapshot.get("running", False),
            "elapsed_seconds": snapshot.get("elapsed_seconds", 0.0),
            "agent_count": snapshot.get("agent_count", len(agents)),
            "alive_count": snapshot.get("alive_count", 0),
            "state_keys": snapshot.get("state_keys", 0),
        },
    }


def build_demo_loomy_city(ticks: int = 10) -> Dict[str, Any]:
    """Spawn the canonical demo swarm, tick it, snapshot, and convert.

    Mirrors the ``loomy.py demo-knot`` roster: scout, weaver, dismantler,
    compiler, watchdog, helix — so the city shows a real mixed swarm.
    """
    from whorl.core.runtime import Loomy
    from whorl.core.agent import ScoutAgent, WeaverAgent, DismantlerAgent
    from whorl.core.agents_ext import CompilerAgent, WatchdogAgent, HelixAgent

    loomy = Loomy(
        state_path="~/.whorl/code-city-state.json",
        tick_delay=0,
        verbose=False,
        max_ticks=0,
    )
    loomy.spawn_agent(ScoutAgent("scout-1", loomy.state, prefix="market"))
    loomy.spawn_agent(WeaverAgent("weaver-1", loomy.state))
    loomy.spawn_agent(DismantlerAgent("dismantler-1", loomy.state))
    loomy.spawn_agent(CompilerAgent(
        "compiler-1", loomy.state, from_lang="python", to_lang="javascript"
    ))
    loomy.spawn_agent(WatchdogAgent("watchdog-1", loomy.state, alert_after_ticks=5))
    loomy.spawn_agent(HelixAgent(
        "helix-1", loomy.state, weave_key="demo-secret-key",
        role="crypto-weaver", speed=6,
    ))
    loomy.run(ticks=ticks, tick_delay=0)
    return loomy_snapshot_to_city(loomy.snapshot())


if __name__ == "__main__":
    import json
    city = build_demo_loomy_city()
    print(json.dumps({
        "total_files": city["total_files"],
        "loomy": city["loomy"],
        "buildings": [
            {"name": b["name"], "role": b["type"], "health": b["health"],
             "dimensions": b["dimensions"], "pos": b["position"]}
            for b in city["buildings"]
        ],
    }, indent=2))
