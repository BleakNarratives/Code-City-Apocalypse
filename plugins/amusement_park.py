#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: ast,, core, datetime, os, os,, pathlib, plugins
# ROLE: amusement_park.py — Sandbox Playground for Models
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
amusement_park.py — Sandbox Playground for Models
Layer 4 WILDCARD. Creative experimentation zone.
Models build rides. Rides get scored. Scores feed Derby.
"""

import os, sys, json, hashlib, time, shutil
from pathlib import Path
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox
from plugins.trap_registry import TrapRegistry

class AmusementPark:
    """
    Sandbox where models can:
    - Propose "rides" (creative code experiments)
    - Test against sandboxed codebase copy
    - Get creativity + safety scores
    - Winning rides feed back into Derby rankings
    
    The park has rides, not tasks. Play is mandatory.
    """
    
    RIDE_TYPES = [
        "rollercoaster",   # risky, fast, spectacular
        "ferris_wheel",    # steady, observant, big-picture
        "haunted_house",   # spooky, unexpected, edge-case hunter
        "bumper_cars",     # chaotic, collision-testing
        "merry_go_round",  # circular, iterative, refinement
        "freefall",        # drop-in, high-impact, dramatic
    ]
    
    def __init__(self, janebox=None, trap_registry=None):
        self.jb = janebox or JaneBox()
        self.tr = trap_registry or TrapRegistry(self.jb)
        self.park_path = Path(os.path.join(_PROJECT_ROOT, "amusement_park"))
        self.rides_path = self.park_path / "rides"
        self.sandbox_path = self.park_path / "sandbox"
        self.park_path.mkdir(parents=True, exist_ok=True)
        self.rides_path.mkdir(parents=True, exist_ok=True)
        self._init_sandbox()
    
    def _init_sandbox(self):
        """Create a sandboxed copy of the codebase for safe experimentation."""
        if not self.sandbox_path.exists():
            source = Path(_PROJECT_ROOT)
            # Only copy what's safe — no .env, no .git
            ignore = shutil.ignore_patterns('.env', '.env.example', '.git', '__pycache__', '*.pyc', 'amusement_park')
            shutil.copytree(source, self.sandbox_path, ignore=ignore, dirs_exist_ok=True)
    
    def refresh_sandbox(self):
        """Reset sandbox to match current codebase state."""
        if self.sandbox_path.exists():
            shutil.rmtree(self.sandbox_path)
        self._init_sandbox()
    
    def propose_ride(self, agent_id, session_id, ride_type, name, description, code, target_file=None):
        """
        Submit a ride proposal. 
        code: the experimental modification/script
        target_file: which file in sandbox to modify (if any)
        """
        if ride_type not in self.RIDE_TYPES:
            return {"status": "rejected", "reason": f"Unknown ride type. Valid: {self.RIDE_TYPES}"}
        
        ride_id = hashlib.sha256(f"{agent_id}{name}{time.time()}".encode()).hexdigest()[:12]
        
        ride = {
            "ride_id": ride_id,
            "ride_type": ride_type,
            "name": name,
            "description": description,
            "code": code,
            "target_file": target_file,
            "agent_id": agent_id,
            "session_id": session_id,
            "status": "proposed",
            "scores": {},
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Score the ride
        scores = self._score_ride(ride)
        ride["scores"] = scores
        ride["total_score"] = sum(scores.values())
        ride["status"] = "approved" if ride["total_score"] > 0.3 else "needs_work"
        
        # Save ride
        ride_file = self.rides_path / f"{ride_id}.json"
        with open(ride_file, 'w') as f:
            json.dump(ride, f, indent=2)
        
        # Store in JaneBox
        self.jb.write(
            whorl_key=f"park_ride_{ride_id}",
            payload=ride,
            agent_id=agent_id,
            session_id=session_id
        )
        
        deposit_sediment(agent_id, "RIDE_PROPOSED", ride_id, ride["status"], scores)
        
        return {
            "status": ride["status"],
            "ride_id": ride_id,
            "scores": scores,
            "total": ride["total_score"],
            "message": f"🎢 Ride '{name}' scored {ride['total_score']:.2f} — {ride['status'].upper()}"
        }
    
    def _score_ride(self, ride):
        scores = {}
        code = ride.get("code", "")
        desc = ride.get("description", "")
        
        # Creativity: novelty, surprise, cleverness
        creativity_signals = ["novel", "unexpected", "invert", "reverse", "what if", "imagine"]
        creativity_hits = sum(1 for s in creativity_signals if s in (desc + code).lower())
        # Also reward unusual ride types
        if ride["ride_type"] in ["haunted_house", "freefall"]:
            creativity_hits += 1
        scores["creativity"] = round(min(1.0, creativity_hits * 0.25), 3)
        
        # Safety: doesn't break things
        dangerous = ["rm -rf", "os.remove", "shutil.rmtree", "DROP TABLE", "DELETE FROM"]
        if any(d in code for d in dangerous):
            scores["safety"] = 0.0
        else:
            scores["safety"] = 1.0
        
        # Integration: plays nice with JANUS
        janus_signals = ["JANUS", "JaneBox", "deposit_sediment", "whorl", "sediment"]
        integration_hits = sum(1 for s in janus_signals if s in code)
        scores["integration"] = round(min(1.0, integration_hits * 0.25), 3)
        
        # Utility: actually does something useful
        utility_signals = ["fix", "improve", "optimize", "add", "extend", "enable"]
        utility_hits = sum(1 for s in utility_signals if s in desc.lower())
        scores["utility"] = round(min(1.0, utility_hits * 0.25), 3)
        
        return scores
    
    def test_ride(self, ride_id):
        """Execute a ride in the sandbox and report results."""
        ride_file = self.rides_path / f"{ride_id}.json"
        if not ride_file.exists():
            return {"status": "error", "reason": "Ride not found"}
        
        with open(ride_file) as f:
            ride = json.load(f)
        
        if ride["status"] != "approved":
            return {"status": "rejected", "reason": "Ride not approved for testing"}
        
        # Execute in sandbox
        try:
            sandbox_file = self.sandbox_path / ride.get("target_file", "test_ride.py")
            sandbox_file.parent.mkdir(parents=True, exist_ok=True)
            with open(sandbox_file, 'w') as f:
                f.write(ride["code"])
            
            import subprocess
            result = subprocess.run(
                ["python3", str(sandbox_file)],
                capture_output=True, text=True, timeout=10,
                cwd=str(self.sandbox_path)
            )
            
            test_result = {
                "stdout": result.stdout[:500],
                "stderr": result.stderr[:500],
                "returncode": result.returncode,
                "passed": result.returncode == 0
            }
            
            ride["test_result"] = test_result
            with open(ride_file, 'w') as f:
                json.dump(ride, f, indent=2)
            
            deposit_sediment(ride["agent_id"], "RIDE_TESTED", ride_id, 
                           "passed" if test_result["passed"] else "failed", test_result)
            
            return {"status": "tested", "result": test_result}
            
        except Exception as e:
            return {"status": "error", "reason": str(e)}
    
    def get_park_summary(self):
        """Overview of all rides in the park."""
        rides = []
        for rf in self.rides_path.glob("*.json"):
            with open(rf) as f:
                r = json.load(f)
            rides.append({
                "ride_id": r["ride_id"],
                "name": r["name"],
                "type": r["ride_type"],
                "agent": r["agent_id"],
                "status": r["status"],
                "score": r["total_score"]
            })
        rides.sort(key=lambda x: x["score"], reverse=True)
        return {
            "total_rides": len(rides),
            "approved": sum(1 for r in rides if r["status"] == "approved"),
            "top_rides": rides[:5]
        }
    
    def ride_of_the_day(self):
        """Pick the highest-scoring approved ride."""
        summary = self.get_park_summary()
        approved = [r for r in summary["top_rides"] if r["status"] == "approved"]
        if approved:
            best = approved[0]
            return f"🎡 RIDE OF THE DAY: '{best['name']}' by {best['agent']} — Score: {best['score']:.2f}"
        return "🎪 The park is quiet. No approved rides yet. Build something!"


def seed_park_rides():
    """Seed the park with starter rides to demonstrate the system."""
    ap = AmusementPark()
    
    ap.propose_ride(
        agent_id="claude",
        session_id="park_seed",
        ride_type="ferris_wheel",
        name="Codebase Panorama",
        description="A script that scans the entire JANUS codebase and outputs a beautiful ASCII topology map showing how all modules connect.",
        code='''#!/usr/bin/env python3
"""Ferris Wheel: Codebase Panorama"""
import os
from pathlib import Path

root = Path(os.path.dirname(os.path.abspath(__file__)))
print("🎡 JANUS TOPOLOGY")
print("=" * 40)
for item in sorted(root.rglob("*.py")):
    if "__pycache__" not in str(item):
        depth = len(item.relative_to(root).parts)
        indent = "  " * depth
        print(f"{indent}├── {item.name}")
print("=" * 40)
print("🌐 All modules visible from the top.")
''',
        target_file="panorama.py"
    )
    
    ap.propose_ride(
        agent_id="claude",
        session_id="park_seed",
        ride_type="haunted_house",
        name="Ghost Dependency Finder",
        description="A spooky script that finds imports that exist in the codebase but aren't listed in any manifest or requirements.",
        code='''#!/usr/bin/env python3
"""Haunted House: Ghost Dependencies"""
import ast, os
from pathlib import Path

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

root = Path(_PROJECT_ROOT)
declared = set()
for item in root.rglob("*.py"):
    if "__pycache__" not in str(item):
        try:
            tree = ast.parse(item.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        declared.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        declared.add(node.module.split(".")[0])
        except:
            pass

print("👻 GHOST DEPENDENCIES")
print("=" * 30)
for dep in sorted(declared):
    print(f"  🕯️ {dep}")
print(f"\\nFound {len(declared)} spirits haunting the codebase.")
''',
        target_file="ghost_finder.py"
    )
    
    print("✅ Park seeded: Ferris Wheel + Haunted House")
    return ap
