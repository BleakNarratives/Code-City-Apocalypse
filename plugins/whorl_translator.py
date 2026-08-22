#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: core, dataclasses, datetime, os,, pathlib, plugins, typing
# ROLE: whorl_translator.py — Whorl ↔ JANUS Universal Adapter
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
whorl_translator.py — Whorl ↔ JANUS Universal Adapter
Bridges Whorl's helical agent physics into the JANUS ecosystem.
Ingests .whr files, runs simulations, emits to Loom/Dashboard/Three.js.
"""

import os, sys, json, math, time, subprocess, uuid, hashlib
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Dynamic project root: MUST be defined before any usage below ──
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import the native Whorl runtime
# ── Whorl core import: try external Whorl system first, fall back to local ──
_WHORL_CORE_CANDIDATES = [
    os.path.expanduser("~/RootBase/Whorl/extracted_whorl/vortex_source/whorl/strands/python/whorl_core.py"),
    os.path.join(_PROJECT_ROOT, "whorl_core.py"),
]
WHORL_CORE_PATH = None
for candidate in _WHORL_CORE_CANDIDATES:
    if os.path.exists(candidate):
        WHORL_CORE_PATH = candidate
        break

if WHORL_CORE_PATH is None:
    # Whorl core not found — define fully functional stubs so the translator degrades gracefully
    # These stubs implement the full WhorlRuntime/Agent/GravityWell interface with no-ops
    class _StubAgent:
        def __init__(self, name="", r=0, theta=0, z=0, omega=0, entropy=100):
            self.id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:12]
            self.name = name
            self.r, self.theta, self.z = r, theta, z
            self.omega, self.entropy = omega, entropy
            self.fitness, self.breed_fitness = 0.0, 0.0
            self.instruction = "SPAWN"
            self.signature = ""
            self.thread_depth_val = 0
            self.fossil = False
            self.lineage = []
    
    class _StubWell:
        def __init__(self, id="", r=0, theta=0, z=0, mass=1):
            self.id, self.r, self.theta, self.z, self.mass = id, r, theta, z, mass
    
    class _StubRuntime:
        def __init__(self, state_file=None):
            self.tick = 0
            self.agents = []
            self.wells = []
            self.state_file = state_file
        def run_tick(self):
            self.tick += 1
        def add_agent(self, agent):
            self.agents.append(agent)
        def add_well(self, well):
            self.wells.append(well)
    
    whorl_core = type('whorl_stub', (), {
        'WhorlRuntime': _StubRuntime,
        'Agent': _StubAgent,
        'GravityWell': _StubWell,
    })()
else:
    import importlib.util
    spec = importlib.util.spec_from_file_location("whorl_core", WHORL_CORE_PATH)
    whorl_core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(whorl_core)

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox
from plugins.loom_graph import LoomGraph

# ── Whorl Grammar Tokenizer ──────────────────────

class WhorlTokenizer:
    """Simple tokenizer for .whr files based on the EBNF grammar."""
    
    KEYWORDS = {
        'helix', 'agent', 'well', 'monster', 'step', 'spawn', 'learn',
        'attack', 'cleanup', 'observe', 'forge', 'cost', 'fossil',
        'mutation', 'phaselock', 'cycle', 'origin', 'pitch', 'entropy',
        'state', 'momentum', 'role', 'position', 'mass', 'target',
        'counter', 'offspring', 'jitter', 'inherit', 'threshold',
        'delta_r', 'delta_theta', 'delta_z', 'variance', 'radius',
        'synchronize', 'move', 'resolve', 'detect', 'run', 'apply',
        'agents', 'wells', 'collisions', 'instructions', 'monsters'
    }
    
    @classmethod
    def tokenize(cls, source: str) -> list:
        tokens = []
        i = 0
        while i < len(source):
            c = source[i]
            if c.isspace():
                i += 1
                continue
            if c == '#':
                while i < len(source) and source[i] != '\n':
                    i += 1
                continue
            if c.isalpha() or c == '_':
                start = i
                while i < len(source) and (source[i].isalnum() or source[i] == '_'):
                    i += 1
                word = source[start:i]
                if word in cls.KEYWORDS:
                    tokens.append(('KEYWORD', word))
                else:
                    tokens.append(('IDENT', word))
                continue
            if c.isdigit() or (c == '-' and i+1 < len(source) and source[i+1].isdigit()):
                start = i
                if source[i] == '-':
                    i += 1
                while i < len(source) and (source[i].isdigit() or source[i] == '.'):
                    i += 1
                tokens.append(('FLOAT', float(source[start:i])))
                continue
            if c in '(){}':
                tokens.append(('DELIM', c))
                i += 1
                continue
            if c == ',':
                tokens.append(('COMMA', ','))
                i += 1
                continue
            i += 1
        return tokens


# ── Whorl Parser ─────────────────────────────────

@dataclass
class ParsedHelix:
    name: str
    origin: tuple = (0.0, 0.0, 0.0)
    pitch: float = 0.2
    entropy: float = 100.0

@dataclass
class ParsedAgent:
    name: str
    state: tuple = (0.5, 0.0, 0.0)
    momentum: float = 0.1
    entropy: float = 100.0
    role: str = ""

@dataclass
class ParsedWell:
    name: str
    position: tuple = (0.0, 0.0, 0.0)
    mass: float = 1.0

@dataclass
class ParsedWhorlProgram:
    helices: List[ParsedHelix] = field(default_factory=list)
    agents: List[ParsedAgent] = field(default_factory=list)
    wells: List[ParsedWell] = field(default_factory=list)
    cycles: int = 10

class WhorlParser:
    """Parse tokenized .whr into structured program."""
    
    @staticmethod
    def parse(tokens: list) -> ParsedWhorlProgram:
        program = ParsedWhorlProgram()
        i = 0
        while i < len(tokens):
            if tokens[i] == ('KEYWORD', 'helix'):
                helix, i = WhorlParser._parse_helix(tokens, i+1)
                program.helices.append(helix)
            elif tokens[i] == ('KEYWORD', 'agent'):
                agent, i = WhorlParser._parse_agent(tokens, i+1)
                program.agents.append(agent)
            elif tokens[i] == ('KEYWORD', 'well'):
                well, i = WhorlParser._parse_well(tokens, i+1)
                program.wells.append(well)
            elif tokens[i] == ('KEYWORD', 'cycle'):
                _, i = WhorlParser._parse_cycle(tokens, i+1)
            else:
                i += 1
        return program
    
    @staticmethod
    def _parse_helix(tokens, i):
        name = tokens[i][1] if tokens[i][0] == 'IDENT' else 'unnamed'
        i += 1
        helix = ParsedHelix(name=name)
        if i < len(tokens) and tokens[i] == ('DELIM', '{'):
            i += 1
            while i < len(tokens) and tokens[i] != ('DELIM', '}'):
                if tokens[i] == ('KEYWORD', 'origin'):
                    i += 2  # skip '('
                    x, y, z = tokens[i][1], tokens[i+2][1], tokens[i+4][1]
                    helix.origin = (x, y, z)
                    i += 6  # skip x, comma, y, comma, z, ')'
                elif tokens[i] == ('KEYWORD', 'pitch'):
                    helix.pitch = tokens[i+1][1]
                    i += 2
                elif tokens[i] == ('KEYWORD', 'entropy'):
                    helix.entropy = tokens[i+1][1]
                    i += 2
                else:
                    i += 1
            i += 1
        return helix, i
    
    @staticmethod
    def _parse_agent(tokens, i):
        name = tokens[i][1] if tokens[i][0] == 'IDENT' else 'unnamed'
        i += 1
        agent = ParsedAgent(name=name)
        if i < len(tokens) and tokens[i] == ('DELIM', '{'):
            i += 1
            while i < len(tokens) and tokens[i] != ('DELIM', '}'):
                if tokens[i] == ('KEYWORD', 'state'):
                    i += 2
                    x, y, z = tokens[i][1], tokens[i+2][1], tokens[i+4][1]
                    agent.state = (x, y, z)
                    i += 6
                elif tokens[i] == ('KEYWORD', 'momentum'):
                    agent.momentum = tokens[i+1][1]
                    i += 2
                elif tokens[i] == ('KEYWORD', 'entropy'):
                    agent.entropy = tokens[i+1][1]
                    i += 2
                elif tokens[i] == ('KEYWORD', 'role'):
                    agent.role = tokens[i+1][1]
                    i += 2
                else:
                    i += 1
            i += 1
        return agent, i
    
    @staticmethod
    def _parse_well(tokens, i):
        name = tokens[i][1] if tokens[i][0] == 'IDENT' else 'unnamed'
        i += 1
        well = ParsedWell(name=name)
        if i < len(tokens) and tokens[i] == ('DELIM', '{'):
            i += 1
            while i < len(tokens) and tokens[i] != ('DELIM', '}'):
                if tokens[i] == ('KEYWORD', 'position'):
                    i += 2
                    x, y, z = tokens[i][1], tokens[i+2][1], tokens[i+4][1]
                    well.position = (x, y, z)
                    i += 6
                elif tokens[i] == ('KEYWORD', 'mass'):
                    well.mass = tokens[i+1][1]
                    i += 2
                else:
                    i += 1
            i += 1
        return well, i
    
    @staticmethod
    def _parse_cycle(tokens, i):
        if i < len(tokens) and tokens[i] == ('DELIM', '{'):
            i += 1
            while i < len(tokens) and tokens[i] != ('DELIM', '}'):
                i += 1
            i += 1
        return None, i


# ── Whorl ↔ JANUS Bridge ─────────────────────────

class WhorlTranslator:
    """
    Universal Adapter: Whorl ↔ JANUS ecosystem.
    
    Capabilities:
    - Parse .whr files into executable simulations
    - Run WhorlRuntime inside JANUS
    - Convert agents/wells/state → Loom graph nodes
    - Emit live state to dashboard (via callback)
    - Generate Three.js scene JSON from Whorl state
    - Bridge to other strands (bash, go, lua, js, rust)
    """
    
    # ── Strand paths: try external Whorl system first, fall back to local project ──
    STRAND_PATHS = {
        'bash': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'bash', 'whorl_metal.sh'),
        'go': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'go', 'whorl_nerves.go'),
        'js': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'js', 'whorl_eyes.js'),
        'lua': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'lua', 'whorl_scout.lua'),
        'rust': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'rust'),
        'python': os.path.join(_PROJECT_ROOT, 'whorl_strands', 'python', 'whorl_core.py'),
    }
    
    def __init__(self, janebox=None, loom=None, dashboard_callback=None):
        self.jb = janebox or JaneBox()
        self.loom = loom or LoomGraph(self.jb)
        self.runtime = whorl_core.WhorlRuntime(state_file=os.path.join(_PROJECT_ROOT, 'whorl_state.json'))
        self.dashboard_callback = dashboard_callback
        self.simulation_active = False
        self.last_state_snapshot = {}
        
    def parse_file(self, filepath: str) -> ParsedWhorlProgram:
        """Parse a .whr file into a structured program."""
        with open(filepath, 'r') as f:
            source = f.read()
        tokens = WhorlTokenizer.tokenize(source)
        return WhorlParser.parse(tokens)
    
    def load_program_to_runtime(self, program: ParsedWhorlProgram):
        """Convert parsed program into runtime agents and wells."""
        self.runtime = whorl_core.WhorlRuntime(state_file=os.path.join(_PROJECT_ROOT, 'whorl_state.json'))
        for pa in program.agents:
            agent = whorl_core.Agent(
                name=pa.name,
                r=pa.state[0],
                theta=pa.state[1],
                z=pa.state[2],
                omega=pa.momentum,
                entropy=pa.entropy
            )
            self.runtime.add_agent(agent)
        for pw in program.wells:
            well = whorl_core.GravityWell(
                id=pw.name,
                r=pw.position[0],
                theta=pw.position[1],
                z=pw.position[2],
                mass=pw.mass
            )
            self.runtime.add_well(well)
        deposit_sediment("whorl_translator", "LOAD_PROGRAM", "runtime",
                        "loaded", {"agents": len(program.agents), "wells": len(program.wells)})
    
    def run_tick(self) -> dict:
        """Execute one tick and return state snapshot."""
        self.runtime.run_tick()
        return self.get_state_snapshot()
    
    def get_state_snapshot(self) -> dict:
        """Capture current Whorl state as a dictionary."""
        snapshot = {
            "tick": self.runtime.tick,
            "agents": [],
            "wells": [],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        for agent in self.runtime.agents:
            if not agent.fossil:
                snapshot["agents"].append({
                    "id": agent.id,
                    "name": agent.name,
                    "r": agent.r,
                    "theta": agent.theta,
                    "z": agent.z,
                    "omega": agent.omega,
                    "entropy": agent.entropy,
                    "fitness": agent.fitness,
                    "breed_fitness": agent.breed_fitness,
                    "instruction": agent.instruction,
                    "signature": agent.signature,
                    "thread_depth": agent.thread_depth_val,
                    "fossil": agent.fossil,
                    "lineage": agent.lineage
                })
        for well in self.runtime.wells:
            snapshot["wells"].append({
                "id": well.id,
                "r": well.r,
                "theta": well.theta,
                "z": well.z,
                "mass": well.mass
            })
        self.last_state_snapshot = snapshot
        return snapshot
    
    def weave_into_loom(self):
        """Convert current Whorl state into Loom graph nodes and edges."""
        snapshot = self.get_state_snapshot()
        for agent_data in snapshot["agents"]:
            self.loom.weave(
                {"id": agent_data["id"], "type": "WhorlAgent", "data": agent_data},
                "IS_AGENT",
                {"id": f"tick_{snapshot['tick']}", "type": "WhorlTick"},
                {"tick": snapshot["tick"]}
            )
            # Connect agents that are phase-locked (close theta)
            for other in snapshot["agents"]:
                if other["id"] != agent_data["id"]:
                    if abs(agent_data["theta"] - other["theta"]) < 0.15:
                        self.loom.weave(
                            {"id": agent_data["id"], "type": "WhorlAgent"},
                            "PHASE_LOCKED",
                            {"id": other["id"], "type": "WhorlAgent"},
                            {"tick": snapshot["tick"]}
                        )
        for well_data in snapshot["wells"]:
            self.loom.weave(
                {"id": well_data["id"], "type": "WhorlWell", "data": well_data},
                "EXERTS_FORCE",
                {"id": f"tick_{snapshot['tick']}", "type": "WhorlTick"},
                {"mass": well_data["mass"]}
            )
        deposit_sediment("whorl_translator", "WEAVE_LOOM", f"tick_{snapshot['tick']}",
                        "woven", {"agents": len(snapshot["agents"]), "wells": len(snapshot["wells"])})
    
    def to_threejs_scene(self) -> dict:
        """Convert Whorl state to a Three.js-compatible scene description."""
        snapshot = self.last_state_snapshot or self.get_state_snapshot()
        scene = {
            "objects": [],
            "lights": [
                {"type": "ambient", "color": "#222244", "intensity": 0.5},
                {"type": "point", "position": [0, 3, 3], "color": "#ffaa00", "intensity": 1.0}
            ],
            "camera": {"position": [0, 1.5, 4], "lookAt": [0, 0, 0]}
        }
        
        # Convert agents to spheres (r, theta, z) → (x, y, z) mapping
        for agent in snapshot["agents"]:
            r, theta, z = agent["r"], agent["theta"], agent["z"]
            x = r * math.cos(theta)
            y = z * 2  # scale z for visibility
            z_pos = r * math.sin(theta)
            scene["objects"].append({
                "type": "sphere",
                "id": agent["id"],
                "name": agent["name"],
                "position": [x, y, z_pos],
                "radius": 0.05 + agent["entropy"] * 0.001,
                "color": "#00ff88" if agent["instruction"] == "SPAWN" else
                         "#4488ff" if agent["instruction"] == "LEARN" else
                         "#ff4444" if agent["instruction"] == "ATTACK" else
                         "#aaaaaa",
                "opacity": 0.3 if agent["fossil"] else 0.9,
                "rotation_speed": agent["omega"]
            })
        
        # Wells as larger translucent spheres
        for well in snapshot["wells"]:
            r, theta, z = well["r"], well["theta"], well["z"]
            x = r * math.cos(theta)
            y = z * 2
            z_pos = r * math.sin(theta)
            scene["objects"].append({
                "type": "sphere",
                "id": well["id"],
                "name": well["id"],
                "position": [x, y, z_pos],
                "radius": 0.02 * well["mass"],
                "color": "#ffaa00",
                "opacity": 0.4,
                "is_well": True
            })
        
        return scene
    
    def emit_to_strand(self, target_language: str, output_file: str = None) -> str:
        """Convert current state into a target strand language file."""
        snapshot = self.last_state_snapshot or self.get_state_snapshot()
        
        if target_language == 'python':
            code = self._emit_python(snapshot)
        elif target_language == 'bash':
            code = self._emit_bash(snapshot)
        elif target_language == 'js':
            code = self._emit_js(snapshot)
        elif target_language == 'json':
            code = json.dumps(snapshot, indent=2)
        else:
            code = f"// Strand {target_language} not yet implemented for state emission"
        
        if output_file:
            with open(os.path.expanduser(output_file), 'w') as f:
                f.write(code)
            deposit_sediment("whorl_translator", "EMIT_STRAND", target_language,
                           "emitted", {"file": output_file})
        
        return code
    
    def _emit_python(self, snapshot):
        lines = ["# Auto-generated by Whorl Translator", "from whorl_core import *", ""]
        lines.append(f"# Tick: {snapshot['tick']}")
        lines.append("runtime = WhorlRuntime(state_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whorl_state.json'))")
        for a in snapshot["agents"]:
            lines.append(f"runtime.add_agent(Agent('{a['name']}', r={a['r']}, theta={a['theta']}, z={a['z']}, omega={a['omega']}, entropy={a['entropy']}))")
        for w in snapshot["wells"]:
            lines.append(f"runtime.add_well(GravityWell('{w['id']}', r={w['r']}, theta={w['theta']}, z={w['z']}, mass={w['mass']}))")
        return "\n".join(lines)
    
    def _emit_bash(self, snapshot):
        lines = ["#!/bin/bash", "# Whorl state emitted to bash", f"# Tick: {snapshot['tick']}", ""]
        for a in snapshot["agents"]:
            lines.append(f"echo 'Agent {a['name']}: r={a['r']} theta={a['theta']} z={a['z']} entropy={a['entropy']}'")
        return "\n".join(lines)
    
    def _emit_js(self, snapshot):
        lines = ["// Whorl state for Three.js", f"// Tick: {snapshot['tick']}", ""]
        lines.append("const whorlState = " + json.dumps(self.to_threejs_scene(), indent=2) + ";")
        return "\n".join(lines)
    
    def call_strand(self, language: str, input_data: str = "") -> str:
        """Execute another strand via subprocess."""
        strand_path = os.path.expanduser(self.STRAND_PATHS.get(language, ""))
        if not strand_path or not os.path.exists(strand_path.split()[0] if ' ' in strand_path else strand_path):
            return f"Strand {language} not found at {strand_path}"
        
        try:
            if language == 'bash':
                result = subprocess.run(['bash', strand_path], capture_output=True, text=True, timeout=5)
            elif language == 'python':
                result = subprocess.run(['python3', strand_path], capture_output=True, text=True, timeout=5, input=input_data)
            elif language == 'go':
                result = subprocess.run(['go', 'run', strand_path], capture_output=True, text=True, timeout=5)
            elif language == 'lua':
                result = subprocess.run(['lua', strand_path], capture_output=True, text=True, timeout=5)
            elif language == 'js':
                result = subprocess.run(['node', strand_path], capture_output=True, text=True, timeout=5)
            else:
                return f"Execution not configured for {language}"
            
            deposit_sediment("whorl_translator", "CALL_STRAND", language,
                           "executed", {"stdout": result.stdout[:200]})
            return result.stdout or result.stderr
        except Exception as e:
            return f"Strand error: {e}"


# ── Live Simulation Runner (for dashboard) ───────

class WhorlSimulationRunner:
    """Runs Whorl ticks on an interval, feeds dashboard via callback."""
    
    def __init__(self, translator: WhorlTranslator, tick_interval: float = 1.0):
        self.translator = translator
        self.tick_interval = tick_interval
        self.running = False
        
    def start(self, max_ticks: int = 0):
        self.running = True
        ticks = 0
        while self.running:
            snapshot = self.translator.run_tick()
            if self.translator.dashboard_callback:
                self.translator.dashboard_callback('whorl_tick', snapshot)
            ticks += 1
            if max_ticks > 0 and ticks >= max_ticks:
                break
            time.sleep(self.tick_interval)
        self.running = False
    
    def stop(self):
        self.running = False


def seed_whorl_translator():
    """Quick demo: load a program and run a few ticks."""
    wt = WhorlTranslator()
    # Try multiple locations for demo.whr
    demo_candidates = [
        os.path.expanduser("~/RootBase/Whorl/extracted_whorl/vortex_source/whorl/examples/demo.whr"),
        os.path.join(_PROJECT_ROOT, "demo.whr"),
        os.path.join(_PROJECT_ROOT, "..", "demo.whr"),
    ]
    demo_path = None
    for candidate in demo_candidates:
        if os.path.exists(candidate):
            demo_path = candidate
            break
    if demo_path is None:
        print("⚠️  No demo.whr found — Whorl Translator initialized with empty runtime")
        return wt
    program = wt.parse_file(demo_path)
    wt.load_program_to_runtime(program)
    for _ in range(5):
        wt.run_tick()
    wt.weave_into_loom()
    print(f"✅ Whorl Translator seeded — {len(wt.runtime.agents)} agents, tick {wt.runtime.tick}")
    return wt
