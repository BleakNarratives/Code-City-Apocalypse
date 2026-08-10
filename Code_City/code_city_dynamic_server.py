# File: backend/code_city_server.py
# ENHANCED: Dynamic chaos simulation, continuous health decay, and refined metrics.
# This server manages code analysis, calculates building metrics, 
# and communicates real-time state to the frontend dashboard via WebSocket.

import os
import json
import asyncio
import websockets
import time
import sys
import uuid
import random
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
PORT = 8765
# Only scan common code files
CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.php'}
DECAY_RATE = 0.005 # Health decay percentage per scan cycle
SPAWN_CHANCE = 10  # 1 in X chance of a monster spontaneously spawning during decay

# --- CORE LOGIC: CODEBASE SCANNER ---

class CodebaseScanner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).absolute()
        self.buildings = {} # Key: file_path (str), Value: building data
        self.monsters = {}  # Key: monster_id, Value: monster data
        self.last_scan_time = 0

    def _is_code_file(self, file_path: Path) -> bool:
        """Excludes typical junk and only includes code files."""
        if any(part.startswith('.') for part in file_path.parts):
            return False
        if "node_modules" in str(file_path) or "venv" in str(file_path) or "dist" in str(file_path):
            return False
        return file_path.suffix.lower() in CODE_EXTENSIONS

    def _simulate_code_metrics(self, lines: int) -> dict:
        """Simulates metrics based on lines of code."""
        complexity_score = max(1, int(lines / 150) + random.randint(1, 5))
        # Base health is static based on file size/complexity, representing latent debt
        base_health = max(0.2, 1.0 - (lines / 1500) - (complexity_score / 150.0))
        return {
            'loc': lines,
            'complexity_score': complexity_score,
            'base_health': round(base_health, 2)
        }

    def _create_monster_data(self, building_path: str, lines: int) -> dict:
        """Generates a single, randomized monster."""
        monster_id = str(uuid.uuid4())
        severity = random.randint(3, 10)
        
        error_types = [
            ("Logic Error (Debt)", 0xFC7F00), 
            ("Security Flaw (Audit)", 0xFF0077), 
            ("Performance Hotspot", 0xFFE000), 
            ("Dead Code Block", 0x8800FF)
        ]
        type_name, color_hex = random.choice(error_types)

        error_messages = [
            f"Missing null check in function.",
            f"Unsafe operation detected near line {random.randint(1, lines)}.",
            f"O(n^2) loop detected, needs optimization.",
            f"Inconsistent dependency version.",
            f"Hardcoded secret detected.",
            f"Missing error boundary/try-catch block."
        ]
        
        return {
            'id': monster_id,
            'type': type_name,
            'severity': severity,
            'color': f"#{color_hex:06x}",
            'message': error_messages[random.randint(0, len(error_messages) - 1)],
            'line': random.randint(1, lines),
            'building_path': building_path
        }

    def _recalculate_building_health(self, building: dict, current_monsters: list) -> dict:
        """Recalculates current health based on base health and active monster severity."""
        error_penalty = sum(m['severity'] for m in current_monsters) / 150.0 # Slightly lighter penalty
        final_health = max(0.01, building['base_health'] - error_penalty - building.get('decay_level', 0))
        
        building['health'] = round(final_health, 2)
        building['error_count'] = len(current_monsters)
        return building

    def _run_decay_and_spawns(self):
        """Applies health decay and potentially spawns new monsters."""
        monsters_spawned = []
        for path, building in self.buildings.items():
            # Apply decay (simulates code rot)
            decay_level = building.get('decay_level', 0) + DECAY_RATE
            building['decay_level'] = min(0.9, decay_level) # Cap decay

            # Check for spontaneous monster spawn due to decay
            if decay_level > 0.3 and random.randint(1, SPAWN_CHANCE) == 1:
                if len([m for m in self.monsters.values() if m['building_path'] == path]) < 5: # Limit spawns
                    lines = building['loc']
                    new_monster = self._create_monster_data(path, lines)
                    self.monsters[new_monster['id']] = new_monster
                    monsters_spawned.append(path)
                    print(f"💥 New Monster Spawned in {path} due to decay.")

        # Recalculate health for all buildings affected
        for path, building in self.buildings.items():
            current_monsters = [m for m in self.monsters.values() if m['building_path'] == path]
            self._recalculate_building_health(building, current_monsters)


    def scan_codebase(self, force_full_scan=False) -> dict:
        """Scan the file system, update buildings and monsters."""
        start_time = time.time()
        
        # Only run full scan on initialization or explicit request
        if force_full_scan or not self.buildings:
            new_buildings = {}
            new_monsters = {}
            
            for file_path in self.root_path.rglob('*'):
                if file_path.is_file() and self._is_code_file(file_path):
                    relative_path = str(file_path.relative_to(self.root_path))
                    
                    try:
                        stats = file_path.stat()
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        lines = content.count('\n') + 1

                        # Check if building exists and content hasn't changed
                        if relative_path in self.buildings and stats.st_mtime == self.buildings[relative_path].get('last_modified'):
                            new_buildings[relative_path] = self.buildings[relative_path]
                            continue # Skip analysis if unmodified
                        
                        # Full Analysis (New or Modified File)
                        metrics = self._simulate_code_metrics(lines)
                        
                        # The initial set of monsters (representing initial debt)
                        initial_error_count = max(0, int((lines / 500) * (1.1 - metrics['base_health']) * 3))
                        errors = [self._create_monster_data(relative_path, lines) for _ in range(initial_error_count)]
                        
                        building = {
                            'path': relative_path,
                            'loc': lines, 
                            'complexity_score': metrics['complexity_score'], 
                            'last_modified': stats.st_mtime,
                            'base_health': metrics['base_health'], # Static metric
                            'decay_level': 0.0,
                            # Health and error_count will be calculated next
                        }
                        
                        new_buildings[relative_path] = building
                        for error in errors:
                            new_monsters[error['id']] = error

                    except Exception as e:
                        print(f"Error scanning {file_path}: {e}")
                        pass
            
            self.buildings = new_buildings
            self.monsters = new_monsters
        
        # --- PHASE 2: Dynamic Update ---
        self._run_decay_and_spawns()
        
        # --- PHASE 3: Final State Calculation ---
        for path, building in self.buildings.items():
            current_monsters = [m for m in self.monsters.values() if m['building_path'] == path]
            self._recalculate_building_health(building, current_monsters)

        self.last_scan_time = time.time()
        self.total_errors = len(self.monsters)

        print(f"Scan complete in {self.last_scan_time - start_time:.2f}s. Files: {len(self.buildings)}, Errors: {self.total_errors}")

        return self.get_city_data()

    def get_city_data(self) -> dict:
        """Returns the current state of the city."""
        return {
            'buildings': list(self.buildings.values()),
            'monsters': list(self.monsters.values()),
            'total_files': len(self.buildings),
            'total_errors': len(self.monsters),
            'timestamp': int(self.last_scan_time)
        }
        
    def fix_monster(self, monster_id: str) -> bool:
        """Removes a monster (simulates fixing an error) and updates the building health."""
        if monster_id in self.monsters:
            building_path = self.monsters[monster_id]['building_path']
            del self.monsters[monster_id]
            
            # Reduce decay level slightly when a fix happens
            if building_path in self.buildings:
                building = self.buildings[building_path]
                building['decay_level'] = max(0.0, building.get('decay_level', 0) - 0.05) # Agent fixes local rot
                
                # Recalculate health instantly
                current_monsters = [m for m in self.monsters.values() if m['building_path'] == building_path]
                self._recalculate_building_health(building, current_monsters)

            return True
        return False

# --- FILE WATCHER & SERVER (Unchanged Logic) ---

class CodebaseChangeHandler(FileSystemEventHandler):
    """Triggers a rescan when a file is modified."""
    def __init__(self, server_instance):
        self.server = server_instance
        self.loop = asyncio.get_event_loop()
        self.debounce_timer = None
        self.debounce_delay = 1 # seconds

    def on_any_event(self, event):
        if event.is_directory or "node_modules" in event.src_path or not event.src_path.lower().endswith(tuple(CODE_EXTENSIONS)):
            return
            
        if self.debounce_timer:
            self.debounce_timer.cancel()

        print(f"\n🔔 File change detected in {event.src_path}...")
        # Force a full scan on file change to ensure correct LOC/Base Health
        self.debounce_timer = self.loop.call_later(self.debounce_delay, lambda: asyncio.run_coroutine_threadsafe(self.server.send_city_update(True), self.loop))

class CodeCityServer:
    def __init__(self, root_path: str):
        self.scanner = CodebaseScanner(root_path)
        self.clients = set()
        self.watcher_thread = None

    async def handle_client(self, websocket, path):
        self.clients.add(websocket)
        print(f"[CLIENT CONNECTED] Total clients: {len(self.clients)}")
        await self.send_city_update(True) # Force full scan on initial connect

        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_action(data)
                
        except websockets.exceptions.ConnectionClosedOK:
            pass
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON received.")
        except Exception as e:
            print(f"[ERROR] WebSocket error: {e}")
        finally:
            self.clients.remove(websocket)
            print(f"[CLIENT DISCONNECTED] Total clients: {len(self.clients)}")

    async def handle_action(self, data: dict):
        action = data.get('action')
        
        if action == 'deploy_agent':
            monster_id = data.get('monster_id')
            agent_type = data.get('agent_type')
            
            if self.scanner.fix_monster(monster_id):
                print(f"[AGENT DEPLOYED] {agent_type} fixed monster {monster_id[:8]}... Health score updated.")
                # Send a specific FIX event first, then the full city update
                await self.broadcast(json.dumps({'type': 'fix_confirmation', 'monster_id': monster_id, 'agent_type': agent_type}))
                await self.send_city_update() # Broadcast new state
            else:
                 print(f"[AGENT DEPLOY FAIL] Monster {monster_id[:8]} not found.")

        elif action == 'rescan':
            print("[ACTION] Manual rescan requested.")
            await self.send_city_update(True) # Force full scan

    async def broadcast(self, message: str):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients], return_when=asyncio.ALL_COMPLETED)

    async def send_city_update(self, force_full_scan=False):
        city_data = self.scanner.scan_codebase(force_full_scan) 
        message = json.dumps({'type': 'city_data', 'data': city_data})
        
        if self.clients:
            await self.broadcast(message)
            print(f"[BROADCAST] Sent update to {len(self.clients)} clients.")
    
    # --- Dynamic Polling for Decay/Spawns ---
    async def decay_loop(self):
        while True:
            await asyncio.sleep(10) # Decay every 10 seconds
            print("⏳ Running decay and chaos simulation...")
            await self.send_city_update()

    def start_file_watcher(self):
        event_handler = CodebaseChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.scanner.root_path), recursive=True)
        observer.start()
        self.watcher_thread = observer
        print(f"🔔 File watcher monitoring: {self.scanner.root_path}")

    async def start(self):
        self.start_file_watcher()
        start_server = websockets.serve(self.handle_client, "localhost", PORT)
        
        print(f"🚀 ModMind Backend running on ws://localhost:{PORT}")

        await asyncio.gather(start_server, self.decay_loop())

if __name__ == "__main__":
    scan_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    try:
        import websockets
        import watchdog
    except ImportError:
        print("ERROR: Missing required Python packages.")
        print("Please install them: pip install websockets watchdog")
        sys.exit(1)

    try:
        server = CodeCityServer(scan_path)
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n👋 ModMind Backend shut down.")
        if server.watcher_thread:
            server.watcher_thread.stop()
            server.watcher_thread.join()
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)