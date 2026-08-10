#!/usr/bin/env python3
"""
janus_system.py — The Integration Nexus
Master orchestrator for JANUS ecosystem.
Wires JaneBox, TrapRegistry, Derby, AmusementPark, LoomGraph into one unified system.
"""

import os, sys, json, time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment, read_sediment
from plugins.janebox import JaneBox
from plugins.trap_registry import TrapRegistry, seed_default_challenges
from plugins.derby import Derby, seed_derby_tasks
from plugins.amusement_park import AmusementPark, seed_park_rides
from plugins.loom_graph import LoomGraph, seed_loom

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class JanusSystem:
    """The JANUS Core System — all components, one interface."""
    
    def __init__(self, auto_seed=True):
        self.jb = JaneBox()
        self.tr = TrapRegistry(self.jb)
        self.derby = Derby(self.jb, self.tr)
        self.park = AmusementPark(self.jb, self.tr)
        self.loom = LoomGraph(self.jb)
        
        if auto_seed:
            self._seed_if_empty()
    
    def _seed_if_empty(self):
        """Seed default data only if no challenges/tasks/rides exist."""
        if not any(self.tr.challenges_path.glob("*.json")):
            seed_default_challenges()
        if not any(self.derby.tasks_path.glob("*.json")):
            seed_derby_tasks()
        if not any(self.park.rides_path.glob("*.json")):
            seed_park_rides()
        # Loom always seeds from sessions
        self.loom = seed_loom()
    
    def ignition(self):
        """Startup sequence: validate all components, return status."""
        status = {
            "janeBox": self.jb.health_check(),
            "trapRegistry": bool(self.tr.challenges_path.glob("*.json")),
            "derby": len(self.derby.list_tasks()) > 0,
            "park": len(self.park.get_park_summary()["top_rides"]) > 0,
            "loom": len(self.loom.G.nodes) > 0 if hasattr(self.loom.G, 'nodes') else len(self.loom.G["nodes"]) > 0,
            "sediment": len(read_sediment(5)) > 0,
        }
        all_green = all(status.values())
        status["all_systems_nominal"] = all_green
        
        deposit_sediment("janus_system", "IGNITION", "system", "startup", status)
        return status
    
    def system_report(self):
        """Generate a full system health report."""
        lb = self.derby.get_leaderboard()
        park_summary = self.park.get_park_summary()
        node_count = len(self.loom.G.nodes) if hasattr(self.loom.G, 'nodes') else len(self.loom.G["nodes"])
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "janeBox": "healthy" if self.jb.health_check() else "unreachable",
            "trapRegistry": f"{len(list(self.tr.challenges_path.glob('*.json')))} challenges active",
            "derby": f"{len(lb['rankings'])} agents ranked, {len(self.derby.list_tasks())} tasks",
            "amusementPark": f"{park_summary['total_rides']} rides, {park_summary['approved']} approved",
            "loom": f"{node_count} nodes woven",
            "leader": lb['rankings'][0]['agent_id'] if lb['rankings'] else "none",
            "rideOfDay": self.park.ride_of_the_day() if park_summary['approved'] > 0 else "none"
        }
    
    def new_agent_ritual(self, agent_id):
        """Complete onboarding for a new agent: session, challenges, entry."""
        session = self.tr.start_session(agent_id)
        scribe_challenge = self.tr.get_challenge("scribe")
        if scribe_challenge:
            # Agent must attempt scribe challenge
            result = self.tr.attempt_challenge(session["session_id"], scribe_challenge["challenge_id"], 
                                               {"modules": ["core/JANUS.py", "plugins/janebox.py", "plugins/trap_registry.py", "plugins/derby.py", "plugins/amusement_park.py"]})
        else:
            result = {"status": "no_challenge"}
        
        # Auto-enter derby if scribe passed
        if result["status"] == "granted":
            tasks = self.derby.list_tasks()
            if tasks:
                self.derby.submit_entry(tasks[0]["task_id"], agent_id, session["session_id"], 
                                       "def placeholder(): pass", 5)
        
        # Weave into loom
        self.loom.weave(agent_id, "ONBOARDED", session["session_id"], {"ritual": "new_agent"})
        
        return {"session": session, "challenge_result": result}
