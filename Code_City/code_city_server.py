#!/usr/bin/env python3
import os
import json
import asyncio
import websockets
import random
import time
from pathlib import Path
from typing import Dict, List, Any

# --- GLOBAL CONFIGURATION ---
ROOT_PATH = os.getcwd() # Default path; override with sys.argv[1] in main()
DECAY_INTERVAL = 10     # Seconds between state decay/chaos events
MONSTER_DECAY_RATE = 2  # Health points lost per decay cycle
CHAOS_SPAWN_CHANCE = 0.2 # Chance of a new monster spawning on a random file

# --- AGENT DEFINITIONS (7 Agents + Syntax AI) ---
AGENT_SWARM = [
    'aFiREFLY Refactor',    # Focus: Code Quality & Readability
    'EquiLex Security',     # Focus: Compliance & Auth Bypass
    'Vibe Coder Cleaner',   # Focus: Removing Low-Code Bloat
    'Blue Sky Architect',   # Focus: Re-indexing & Structural Integrity
    'ModMind Synthesizer',  # Focus: Data Flow & Cross-Platform Sync
    'Quantum Debugger'      # Focus: Runtime & Performance Issues
]
SYNTAX_AI = 'Syntax AI (Full Module Fix)' # The ultimate agent for a clean slate

class AgentManager:
    """Handles the deployment and effect of all agents."""
    def __init__(self):
        self.deployed_agents = {}

    def deploy_agent(self, monster: Dict[str, Any], building_id: str, agent_type: str, scanner: 'CodebaseScanner') -> Dict[str, Any]:
        """Deploys an agent and executes the fix logic."""
        
        # 1. Execute Fix Logic
        if agent_type == SYNTAX_AI:
            # Syntax AI: Fixes ALL monsters on the target building
            fixed_count = scanner.fix_all_monsters_on_building(building_id)
            fix_result = f"SYNTAX AI initiated. Full module fix executed, resolving {fixed_count} threats."
            
        else:
            # Swarm/Single Agent: Fixes only the selected monster
            scanner.fix_monster_by_id(monster['id'])
            fix_result = f"Agent {agent_type} eliminated Threat ID {monster['id'][:6]}."

        # 2. Record Deployment
        agent_data = {
            'monster_id': monster['id'],
            'building_id': building_id,
            'agent_type': agent_type,
            'deployment_time': time.time(),
            'status_message': fix_result
        }
        self.deployed_agents[time.time()] = agent_data
        
        return agent_data

class CodebaseScanner:
    """Manages the current state of the code city (buildings and monsters)."""
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).absolute()
        self.buildings: List[Dict[str, Any]] = []
        self.monsters: List[Dict[str, Any]] = []

    def _hash_to_pos(self, filepath: Path) -> Dict[str, float]:
        """Deterministic positioning based on file path hash."""
        h = hash(filepath)
        # Use a grid layout for better visualization
        x = (h % 20) * 15 - 150
        z = ((h // 20) % 20) * 15 - 150
        return {'x': float(x), 'z': float(z)}

    def _get_random_error(self, file_path: Path) -> Dict[str, Any]:
        """Simulates finding a random error with severity."""
        error_types = ["Complexity Spike", "Security Leak", "Dead Code Block", "Outdated Dependency", "UX Mismatch"]
        
        # Generate a unique monster ID
        monster_id = f"{file_path.name[:3]}-{int(time.time() * 1000)}-{random.randint(100, 999)}"
        
        return {
            'id': monster_id,
            'type': random.choice(error_types),
            'message': f"Threat detected near line {random.randint(1, 200)}: requires attention.",
            'severity': random.randint(1, 10),
            'line': random.randint(1, 200)
        }

    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Simulates static analysis to get building metrics."""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        loc = len(content.splitlines())
        
        # Mock complexity: higher LOC means potentially higher complexity
        complexity = min(20, loc / 50 + random.uniform(0, 5)) 

        # Initial health based on complexity and LOC
        initial_health = max(50, 100 - complexity * 3)

        return {
            'id': str(hash(file_path)),
            'filepath': str(file_path.relative_to(self.root_path)),
            'loc': loc,
            'complexity': complexity,
            'health': initial_health,
            'position': self._hash_to_pos(file_path),
            'height': max(10, loc / 10),
        }

    def scan_codebase(self) -> Dict[str, Any]:
        """Performs a full scan, resetting buildings and regenerating monsters."""
        print("[Scanner] Full codebase scan initiated...")
        self.buildings = []
        self.monsters = []
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in {'.py', '.js', '.ts', '.html', '.css', '.md'}:
                building = self._analyze_file(file_path)
                self.buildings.append(building)
                
                # Simulating initial monsters (more complex files get more errors)
                num_errors = int(building['complexity'] / 4)
                for _ in range(num_errors):
                    error = self._get_random_error(file_path)
                    error['building_id'] = building['id']
                    self.monsters.append(error)
        
        return self.get_state()

    def apply_decay(self):
        """Reduces building health and spawns new monsters (Chaos Loop)."""
        print("[Decay] Applying chaos and entropy...")
        new_monsters = []
        
        for building in self.buildings:
            # 1. Health Decay
            building['health'] = max(5, building['health'] - MONSTER_DECAY_RATE)

            # 2. Chaos Spawn (Higher chance on low health files)
            decay_chance = CHAOS_SPAWN_CHANCE + (100 - building['health']) / 200
            if random.random() < decay_chance:
                file_path = self.root_path / building['filepath']
                new_error = self._get_random_error(file_path)
                new_error['building_id'] = building['id']
                new_monsters.append(new_error)

        self.monsters.extend(new_monsters)
        print(f"[Decay] {len(new_monsters)} new threats spawned.")
        
    def fix_monster_by_id(self, monster_id: str):
        """Removes a single monster by ID."""
        self.monsters = [m for m in self.monsters if m['id'] != monster_id]

    def fix_all_monsters_on_building(self, building_id: str) -> int:
        """Removes all monsters associated with a building."""
        fixed_count = len([m for m in self.monsters if m['building_id'] == building_id])
        self.monsters = [m for m in self.monsters if m['building_id'] != building_id]
        
        # Restore building health to reflect the fix
        building = next((b for b in self.buildings if b['id'] == building_id), None)
        if building:
            building['health'] = min(100, building['health'] + 10) # Small health boost for a fix
            
        return fixed_count
        
    def get_state(self) -> Dict[str, Any]:
        """Returns the current state for broadcast."""
        return {
            'buildings': self.buildings,
            'monsters': self.monsters,
            'total_files': len(self.buildings),
            'total_errors': len(self.monsters)
        }


class CodeCityServer:
    """Manages WebSocket connections and the game state loop."""
    def __init__(self, root_path: str):
        self.scanner = CodebaseScanner(root_path)
        self.agent_manager = AgentManager()
        self.clients = set()
        
        # Initial scan
        self.scanner.scan_codebase()

    async def broadcast_state(self):
        """Sends the current state to all connected clients."""
        if self.clients:
            message = json.dumps({'type': 'city_data', 'data': self.scanner.get_state()})
            await asyncio.wait([client.send(message) for client in self.clients])

    async def decay_loop(self):
        """The persistent loop for decay and chaos."""
        while True:
            await asyncio.sleep(DECAY_INTERVAL)
            self.scanner.apply_decay()
            await self.broadcast_state()

    async def handle_client(self, websocket, path):
        """Handles a new client connection."""
        self.clients.add(websocket)
        try:
            # Send initial state on connection
            await websocket.send(json.dumps({'type': 'city_data', 'data': self.scanner.get_state()}))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    print(f"[EquiLex Audit] Action: Malformed_JSON, Status: FAIL. Connection maintained.")
                except Exception as e:
                    print(f"Error handling message: {e}")

        finally:
            self.clients.remove(websocket)

    async def handle_message(self, websocket, data):
        """Processes incoming client actions."""
        action = data.get('action')
        
        if action == 'deploy_agent':
            monster_id = data.get('monster_id')
            agent_type = data.get('agent_type')
            
            monster = next((m for m in self.scanner.monsters if m['id'] == monster_id), None)
            
            if monster:
                # Find the building ID associated with the monster
                building_id = monster['building_id']
                
                # Deploy agent and execute fix
                agent_data = self.agent_manager.deploy_agent(monster, building_id, agent_type, self.scanner)
                
                # Confirm deployment to client (for frontend animation)
                await websocket.send(json.dumps({
                    'type': 'agent_deployed',
                    'data': agent_data
                }))
                
                # Broadcast new state immediately after fix
                await self.broadcast_state()
            else:
                 # Failed attempt to fix non-existent monster
                 print(f"[EquiLex Security] Failed fix attempt for missing monster: {monster_id}")


async def main():
    # Allow passing the root path as an argument for the scanner
    root_path = Path(os.getcwd())
    if len(sys.argv) > 1:
        # If an argument is provided, use it as the root path
        root_path = Path(sys.argv[1]).resolve()
    
    print(f"🦖 MODMIND SCANNING CODEBASE AT: {root_path}")
    
    server_instance = CodeCityServer(str(root_path))
    
    # Start the decay loop concurrently with the WebSocket server
    decay_task = asyncio.create_task(server_instance.decay_loop())
    
    # Start WebSocket server
    start_server = websockets.serve(server_instance.handle_client, "localhost", 8765)
    
    print("🚀 EQUINEX HUB BACKEND RUNNING on ws://localhost:8765")
    print(f"📁 Monitoring: {root_path}")
    print("---")
    
    await asyncio.gather(start_server, decay_task)


if __name__ == '__main__':
    # Add simple command line argument handling
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("Usage: python code_city_server.py [path/to/codebase]")
        print("Starts the ModMind backend scanning the specified path (or current directory if none provided).")
    else:
        # Run the main async function
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nShutting down Code City Server...")
        except IndexError:
             # Handle case where main() might try to access sys.argv[1] when it's not present
             # This should be caught by the logic in main(), but is good practice.
             print("Please ensure you run the script with necessary permissions and arguments.")
        except Exception as e:
             print(f"An unexpected error occurred during startup: {e}")

