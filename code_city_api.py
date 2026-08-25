#!/usr/bin/env python3
"""
code_city_api.py — Lightweight HTTP API on the Code City scanner.

Accepts POST /crash with disaster data → spawns monsters in the city.
Also serves GET /city to inspect current city state.
GET /health for liveness check.

Zero deps — stdlib http.server only. No Flask, no pip installs.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse, parse_qs

# ─── PATH MAGIC — pull in existing Code City modules ──────────

THIS_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(THIS_DIR))
sys.path.insert(0, str(THIS_DIR / "backend"))

try:
    from code_city_apocalypse_v3 import CodeCityApocalypse
    CITY_ENGINE = "v3"
except ImportError:
    CITY_ENGINE = "none"
    CodeCityApocalypse = None

try:
    from backend.server import CodeCityScanner
    SCANNER_ENGINE = "backend"
except ImportError:
    SCANNER_ENGINE = "none"
    CodeCityScanner = None


# ─── In-memory city state ─────────────────────────────────────

PORT = int(os.getenv("CITY_API_PORT", "8765"))
SCAN_PATH = os.getenv("CITY_SCAN_PATH", str(Path(__file__).parent.absolute()))

city_v3: Optional[Any] = None
city_scanner: Optional[Any] = None
spawn_log: List[Dict[str, Any]] = []
error_count: int = 0


def init_city():
    """Initialize Code City engine(s) on startup."""
    global city_v3, city_scanner

    if CodeCityApocalypse:
        city_v3 = CodeCityApocalypse()
        city_v3.scan_project(SCAN_PATH)
        print(f"[city] V3 engine loaded: {len(city_v3.buildings)} buildings")

    if CodeCityScanner:
        city_scanner = CodeCityScanner()
        print(f"[city] Backend scanner loaded")

    if not city_v3:
        print("[city] WARNING: No Code City engine available. Running in log-only mode.")


def spawn_monster(error_type: str, file_path: str, error_message: str,
                  severity: int = 3, monster_type: str = "Crash Beast",
                  monster_symbol: str = "👾", source: str = "crash_feeder") -> Dict[str, Any]:
    """
    Spawn a monster in Code City from a crash event.

    Maps through the existing trigger_disaster() interface on the V3 engine.
    Falls back to scanner-backed injection if V3 isn't available.
    """
    global error_count, city_v3, city_scanner

    # Map crash severity to Code City disaster severity
    # Code City severity: 2=fire, 3=monster, 4=red baron, 5=alien invasion
    codecity_severity = min(severity, 5)

    result = {
        "spawned": False,
        "error_type": error_type,
        "file_path": file_path,
        "error_message": error_message[:500],
        "severity": severity,
        "monster_type": monster_type,
        "monster_symbol": monster_symbol,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Try V3 engine first
    if city_v3:
        try:
            # Use the disaster type that maps to monsters
            disaster_map = {
                5: "memory_error",    # Alien Invasion 🛸
                4: "import_error",    # Red Baron Strike ✈️
                3: "runtime_error",   # Monster Attack 👾
                2: "logic_error",     # Earthquake 🌋
                1: "syntax_error",    # Building Fire 🔥
            }
            mapped_type = disaster_map.get(codecity_severity, "runtime_error")

            # Create a building for the crashed file if it doesn't exist
            if file_path and file_path not in [b.get("path", "") for b in getattr(city_v3, "buildings", [])]:
                building = {
                    "name": file_path.split("/")[-1] if "/" in file_path else file_path,
                    "path": file_path,
                    "height": 20,
                    "health": 100,
                    "errors": [],
                    "symbol": "🏚️",
                }
                if not hasattr(city_v3, "buildings"):
                    city_v3.buildings = []
                city_v3.buildings.append(building)

            disaster = city_v3.trigger_disaster(mapped_type, file_path, error_message)

            # Override the monster type and symbol for crash-specific flair
            if hasattr(city_v3, "monsters") and city_v3.monsters:
                latest_monster = city_v3.monsters[-1]
                latest_monster["name"] = monster_type
                latest_monster["symbol"] = monster_symbol

            result["spawned"] = True
            result["disaster"] = disaster if isinstance(disaster, dict) else {"type": mapped_type}
            result["method"] = "v3_trigger_disaster"

            error_count += 1
        except Exception as e:
            result["error"] = str(e)

    # Try backend scanner for structured monster data
    elif city_scanner:
        try:
            # Build a synthetic monster entry compatible with the scanner format
            monster = {
                "id": f"crash:{error_type}:{datetime.now(timezone.utc).timestamp()}",
                "type": error_type,
                "building_id": file_path,
                "file_path": file_path,
                "file_name": file_path.split("/")[-1] if "/" in file_path else file_path,
                "position": {
                    "x": hash(error_message) % 100 - 50,
                    "y": severity * 10,
                    "z": hash(file_path) % 100 - 50,
                },
                "severity": severity,
                "message": f"[{source}] {monster_type}: {error_message[:200]}",
                "line": hash(error_message) % 100 + 1,
                "health": severity * 10,
                "color": _severity_color(severity),
                "monster_type": monster_type,
            }
            result["monster"] = monster
            result["spawned"] = True
            result["method"] = "scanner_synthetic"
            error_count += 1
        except Exception as e:
            result["error"] = str(e)

    else:
        # Log-only mode
        result["spawned"] = True  # We recorded it
        result["method"] = "log_only"
        error_count += 1

    spawn_log.append(result)
    # Keep only last 500 spawns
    if len(spawn_log) > 500:
        spawn_log[:] = spawn_log[-200:]

    return result


def _severity_color(severity: int) -> str:
    colors = {5: "#ff0000", 4: "#ff4400", 3: "#ff8800", 2: "#ffcc00", 1: "#888888"}
    return colors.get(severity, "#ff4444")


def get_city_state() -> Dict[str, Any]:
    """Return current city state snapshot."""
    state: Dict[str, Any] = {
        "error_count": error_count,
        "spawn_count": len(spawn_log),
        "engine": CITY_ENGINE,
        "scanner": SCANNER_ENGINE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if city_v3:
        state["buildings"] = len(city_v3.buildings)
        state["monsters"] = len(city_v3.monsters)
        state["disasters"] = len(city_v3.disasters)
        state["planes"] = len(city_v3.planes)

    # Return recent spawns (last 10)
    state["recent_spawns"] = spawn_log[-10:]

    return state


# ─── HTTP Handler ─────────────────────────────────────────────

class CityAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Code City crash API."""

    def log_message(self, format, *args):
        """Suppress default http.server logging — we do our own."""
        pass

    def _send_json(self, data: Dict[str, Any], status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        # Use default=str to handle datetime and other non-serializable types
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False,
                                    default=str).encode("utf-8"))

    def _read_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json({
                "status": "ok",
                "engine": CITY_ENGINE,
                "error_count": error_count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        elif path == "/city":
            self._send_json(get_city_state())
        elif path == "/spawns":
            limit = int(parse_qs(parsed.query).get("limit", ["20"])[0])
            self._send_json({"spawns": spawn_log[-limit:]})
        else:
            self._send_json({
                "endpoints": {
                    "GET /health": "Liveness check",
                    "GET /city": "Full city state snapshot",
                    "GET /spawns?limit=N": "Recent monster spawns",
                    "POST /crash": "Spawn a monster from a crash event",
                }
            })

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/crash":
            try:
                body = self._read_body()

                if not body:
                    self._send_json({"error": "Empty body"}, 400)
                    return

                required = ["error_type", "error_message"]
                missing = [k for k in required if k not in body]
                if missing:
                    self._send_json({
                        "error": f"Missing required fields: {missing}",
                        "required_format": {
                            "error_type": "string — crash type (oom_kill, segfault, etc)",
                            "error_message": "string — human-readable crash description",
                            "file_path": "string (optional) — affected file path",
                            "severity": "int (optional) — 1-5, default 3",
                            "monster_type": "string (optional) — custom monster name",
                            "monster_symbol": "string (optional) — emoji symbol",
                            "source": "string (optional) — crash source identifier",
                        },
                    }, 400)
                    return

                result = spawn_monster(
                    error_type=body["error_type"],
                    file_path=body.get("file_path", ""),
                    error_message=body["error_message"],
                    severity=body.get("severity", 3),
                    monster_type=body.get("monster_type", "Crash Beast"),
                    monster_symbol=body.get("monster_symbol", "👾"),
                    source=body.get("source", "api"),
                )

                if result["spawned"]:
                    monster_info = f"{body.get('monster_symbol', '👾')} {body.get('monster_type', 'Crash Beast')}"
                    print(f"[API] {monster_info} spawned via {result['method']}: {body['error_message'][:80]}")
                    self._send_json(result, 201)
                else:
                    self._send_json({"error": "Failed to spawn", "details": result}, 500)

            except json.JSONDecodeError:
                self._send_json({"error": "Invalid JSON"}, 400)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": f"Unknown endpoint: {path}"}, 404)

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    global SCAN_PATH

    print("═══ CODE CITY CRASH API ═══")
    print(f"Port: {PORT}")
    print(f"Scan path: {SCAN_PATH}")
    print()

    init_city()

    server = HTTPServer(("127.0.0.1", PORT), CityAPIHandler)
    print(f"Server listening on http://127.0.0.1:{PORT}")
    print(f"Endpoints:")
    print(f"  GET  http://127.0.0.1:{PORT}/health")
    print(f"  GET  http://127.0.0.1:{PORT}/city")
    print(f"  GET  http://127.0.0.1:{PORT}/spawns")
    print(f"  POST http://127.0.0.1:{PORT}/crash")
    print()
    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n═══ API STOPPED ═══")
        print(f"Total monsters spawned: {error_count}")
        server.shutdown()


if __name__ == "__main__":
    main()