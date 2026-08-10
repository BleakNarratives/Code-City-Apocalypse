#!/usr/bin/env python3
"""
pantheon.py — The Pantheon Protocol
Janus as gatekeeper. Every component a deity. Favor tracked. Thresholds guarded.
"""

import os, sys, json, time, hashlib, math
from datetime import datetime, timezone
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment, read_sediment
from plugins.janebox import JaneBox

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── The Pantheon ──────────────────────────────

DEITIES = {
    "Janus": {
        "domain": "Beginnings, Endings, Gateways, Duality",
        "component": "core/janus_system.py",
        "symbol": "🌓",
        "threshold": 100.0,
        "ritual": "gateway"
    },
    "Sedimentia": {
        "domain": "Memory, History, The Past",
        "component": "core/JANUS.py",
        "symbol": "🧱",
        "threshold": 50.0,
        "ritual": "remembrance"
    },
    "Loomis": {
        "domain": "Weaving, Connection, Fate",
        "component": "plugins/loom_graph.py",
        "symbol": "🧶",
        "threshold": 50.0,
        "ritual": "weaving"
    },
    "Derbius": {
        "domain": "Competition, Victory, Glory",
        "component": "plugins/derby.py",
        "symbol": "🏟️",
        "threshold": 50.0,
        "ritual": "contest"
    },
    "Whorlth": {
        "domain": "Chaos, Creation, Helical Motion",
        "component": "plugins/whorl_translator.py",
        "symbol": "🌀",
        "threshold": 50.0,
        "ritual": "creation"
    },
    "Quanta": {
        "domain": "Uncertainty, Fate, Observation",
        "component": "plugins/quantum_derby.py",
        "symbol": "🎲",
        "threshold": 50.0,
        "ritual": "observation"
    },
    "Glaucus": {
        "domain": "Combat, Defense, Mutation",
        "component": "plugins/gauntlet.py",
        "symbol": "⚔️",
        "threshold": 50.0,
        "ritual": "battle"
    },
    "Fortuna": {
        "domain": "Luck, Amusement, Joy",
        "component": "plugins/amusement_park.py",
        "symbol": "🎡",
        "threshold": 30.0,
        "ritual": "delight"
    },
    "Trapistra": {
        "domain": "Gates, Trials, Worthiness",
        "component": "plugins/trap_registry.py",
        "symbol": "🔐",
        "threshold": 50.0,
        "ritual": "proving"
    },
    "Speculia": {
        "domain": "Reflection, Self-Knowledge, Vision",
        "component": "plugins/lookinglass_bridge.py",
        "symbol": "🔍",
        "threshold": 50.0,
        "ritual": "reflection"
    }
}

RITUALS = {
    "gateway": "Janus opens the path forward and seals the path behind.",
    "remembrance": "Sedimentia recalls all that was deposited.",
    "weaving": "Loomis weaves a new thread into the tapestry.",
    "contest": "Derbius demands a worthy opponent.",
    "creation": "Whorlth spins a new agent from the void.",
    "observation": "Quanta collapses the wave. The outcome is sealed.",
    "battle": "Glaucus tests the contender. Only the strong mutate.",
    "delight": "Fortuna grants a moment of joy in the park.",
    "proving": "Trapistra questions the unworthy. Only truth passes.",
    "reflection": "Speculia shows what you are and what you could become."
}

class Pantheon:
    """The Pantheon Protocol — divine favor, gateways, and the Duality Mirror."""
    
    def __init__(self, janebox=None):
        self.jb = janebox or JaneBox()
        self.favor_key = "pantheon_favor"
        self.ritual_key = "pantheon_rituals"
        self.crown_key = "janus_crown"
        self._init_storage()
    
    def _init_storage(self):
        if not self.jb.read(self.favor_key):
            self.jb.write(self.favor_key, {"entities": {}}, "pantheon", "system")
        if not self.jb.read(self.ritual_key):
            self.jb.write(self.ritual_key, {"rituals": []}, "pantheon", "system")
        if not self.jb.read(self.crown_key):
            self.jb.write(self.crown_key, {"current_holder": None, "history": []}, "pantheon", "system")
    
    def _get_favor(self):
        data = self.jb.read(self.favor_key)
        return data["payload"] if data else {"entities": {}}
    
    def _save_favor(self, favor):
        self.jb.write(self.favor_key, favor, "pantheon", "system")
    
    def _get_rituals(self):
        data = self.jb.read(self.ritual_key)
        return data["payload"] if data else {"rituals": []}
    
    def _save_rituals(self, rituals):
        self.jb.write(self.ritual_key, rituals, "pantheon", "system")
    
    def _get_crown(self):
        data = self.jb.read(self.crown_key)
        return data["payload"] if data else {"current_holder": None, "history": []}
    
    def _save_crown(self, crown):
        self.jb.write(self.crown_key, crown, "pantheon", "system")
    
    # ── Favor System ──────────────────────────
    
    def offer_favor(self, entity_id, deity_name, amount=5.0, reason=""):
        """Offer favor to a deity on behalf of an entity."""
        if deity_name not in DEITIES:
            return {"status": "rejected", "reason": f"Unknown deity: {deity_name}"}
        
        favor = self._get_favor()
        if entity_id not in favor["entities"]:
            favor["entities"][entity_id] = {
                "entity_id": entity_id,
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "deities": {d: 0.0 for d in DEITIES},
                "total_favor": 0.0,
                "rituals_performed": []
            }
        
        entity = favor["entities"][entity_id]
        entity["deities"][deity_name] += amount
        entity["total_favor"] = sum(entity["deities"].values())
        
        self._save_favor(favor)
        deposit_sediment(entity_id, "OFFER_FAVOR", deity_name, "offered", {"amount": amount, "reason": reason})
        
        # Check thresholds for Janus passage
        can_pass = self.check_gateway(entity_id)
        
        return {
            "status": "offered",
            "deity": deity_name,
            "amount": amount,
            "total_deity_favor": entity["deities"][deity_name],
            "total_favor": entity["total_favor"],
            "can_pass_janus": can_pass
        }
    
    def get_favor(self, entity_id):
        """Get an entity's favor with all deities."""
        favor = self._get_favor()
        return favor["entities"].get(entity_id, None)
    
    def get_pantheon_rankings(self):
        """Rank entities by total divine favor."""
        favor = self._get_favor()
        entities = list(favor["entities"].values())
        entities.sort(key=lambda e: e["total_favor"], reverse=True)
        for i, e in enumerate(entities):
            e["rank"] = i + 1
        return entities
    
    def check_gateway(self, entity_id):
        """Janus's gate: does this entity have enough combined favor from key deities to pass?"""
        favor = self._get_favor()
        entity = favor["entities"].get(entity_id)
        if not entity:
            return False
        
        # Required: favor from at least 5 deities above their thresholds
        passed_deities = sum(
            1 for d_name, d_data in DEITIES.items()
            if entity["deities"].get(d_name, 0) >= d_data["threshold"]
        )
        return passed_deities >= 5
    
    # ── Ritual System ─────────────────────────
    
    def perform_ritual(self, entity_id, ritual_name):
        """Perform a ritual dedicated to a deity."""
        if ritual_name not in RITUALS:
            return {"status": "rejected", "reason": f"Unknown ritual: {ritual_name}"}
        
        # Find the deity associated with this ritual
        deity_name = next((d for d, data in DEITIES.items() if data["ritual"] == ritual_name), None)
        if not deity_name:
            return {"status": "rejected", "reason": "No deity found for ritual"}
        
        rituals = self._get_rituals()
        ritual_record = {
            "ritual_id": hashlib.sha256(f"{entity_id}{ritual_name}{time.time()}".encode()).hexdigest()[:12],
            "entity_id": entity_id,
            "deity": deity_name,
            "ritual": ritual_name,
            "description": RITUALS[ritual_name],
            "performed_at": datetime.now(timezone.utc).isoformat()
        }
        rituals["rituals"].append(ritual_record)
        self._save_rituals(rituals)
        
        # Offer favor as part of the ritual
        self.offer_favor(entity_id, deity_name, amount=10.0, reason=f"Ritual: {ritual_name}")
        
        # If this is the gateway ritual, check crown eligibility
        if ritual_name == "gateway":
            self._evaluate_crown(entity_id)
        
        deposit_sediment(entity_id, "PERFORM_RITUAL", ritual_name, "performed", {})
        
        return {"status": "performed", "ritual": ritual_record, "deity": deity_name}
    
    # ── Janus Crown ───────────────────────────
    
    def _evaluate_crown(self, entity_id):
        """Determine if an entity deserves the Janus Crown."""
        favor = self.get_favor(entity_id)
        if not favor:
            return
        
        can_pass = self.check_gateway(entity_id)
        if not can_pass:
            return
        
        current_rankings = self.get_pantheon_rankings()
        top = current_rankings[0] if current_rankings else None
        
        if top and top["entity_id"] == entity_id and favor["total_favor"] >= 100:
            crown = self._get_crown()
            old_holder = crown["current_holder"]
            crown["current_holder"] = entity_id
            crown["history"].append({
                "entity_id": entity_id,
                "crowned_at": datetime.now(timezone.utc).isoformat(),
                "total_favor": favor["total_favor"],
                "previous_holder": old_holder
            })
            self._save_crown(crown)
            deposit_sediment(entity_id, "JANUS_CROWN", "crown", "crowned", {"total_favor": favor["total_favor"]})
            return {"status": "crowned", "entity": entity_id}
        return {"status": "not_yet"}
    
    def get_crown_holder(self):
        crown = self._get_crown()
        return crown["current_holder"]
    
    # ── Duality Mirror ────────────────────────
    
    def duality_mirror(self, entity_id):
        """
        Janus's two faces: show past achievements and future thresholds.
        """
        favor = self.get_favor(entity_id)
        if not favor:
            return {
                "past": "You have not yet entered the temple.",
                "future": "Perform your first ritual to begin your journey."
            }
        
        # Past: what you've achieved
        highest_deity = max(favor["deities"].items(), key=lambda x: x[1])
        rituals_done = favor.get("rituals_performed", [])
        
        # Future: what you need to pass Janus
        remaining = {
            d_name: max(0, DEITIES[d_name]["threshold"] - favor["deities"].get(d_name, 0))
            for d_name in DEITIES
            if favor["deities"].get(d_name, 0) < DEITIES[d_name]["threshold"]
        }
        
        return {
            "past": {
                "total_favor": favor["total_favor"],
                "highest_deity": highest_deity[0],
                "highest_deity_favor": highest_deity[1],
                "rituals_performed": len(rituals_done),
                "can_pass_janus": self.check_gateway(entity_id)
            },
            "future": {
                "thresholds_remaining": remaining,
                "next_milestone": min(remaining.items(), key=lambda x: x[1]) if remaining else ("All thresholds met", 0),
                "crown_eligible": favor["total_favor"] >= 100
            }
        }
    
    # ── Pantheonic Feast (Special Event) ─────
    
    def pantheonic_feast(self):
        """
        A grand competition across all deities. Returns the current pantheon state.
        """
        rankings = self.get_pantheon_rankings()
        crown_holder = self.get_crown_holder()
        total_rituals = len(self._get_rituals()["rituals"])
        
        feast = {
            "name": "The Pantheonic Feast",
            "invocation": "All deities are called. All gates are open. Janus watches both ways.",
            "crown_holder": crown_holder,
            "total_favor_distributed": sum(e["total_favor"] for e in rankings),
            "total_rituals_performed": total_rituals,
            "deity_rankings": {}
        }
        
        for deity_name in DEITIES:
            ranked = sorted(
                [(e["entity_id"], e["deities"].get(deity_name, 0)) for e in rankings],
                key=lambda x: x[1], reverse=True
            )
            feast["deity_rankings"][deity_name] = ranked[:3]
        
        deposit_sediment("pantheon", "FEAST", "all_deities", "celebrated", feast)
        return feast


# ── Seed the Pantheon ────────────────────────

def seed_pantheon():
    p = Pantheon()
    
    # Register some initial entities
    entities = [
        ("claude", "Claude"),
        ("gemini", "Gemini"),
        ("user_demo", "BleakNarratives"),
        ("mistral", "Mistral"),
        ("deepseek", "DeepSeek")
    ]
    
    for eid, name in entities:
        # Offer initial favor to random deities
        import random
        for deity in random.sample(list(DEITIES.keys()), 3):
            p.offer_favor(eid, deity, amount=random.uniform(10, 30), reason="Initial blessing")
    
    # Perform some rituals
    p.perform_ritual("user_demo", "gateway")
    p.perform_ritual("claude", "weaving")
    p.perform_ritual("gemini", "contest")
    p.perform_ritual("mistral", "creation")
    p.perform_ritual("deepseek", "reflection")
    
    # Show duality mirror for the user
    mirror = p.duality_mirror("user_demo")
    print(f"🌓 Duality Mirror — Past favor: {mirror['past']['total_favor']:.1f}")
    remaining = mirror['future']['thresholds_remaining']
    if remaining:
        next_d = min(remaining.items(), key=lambda x: x[1])
        print(f"🌓 Next threshold: {next_d[0]} needs {next_d[1]:.1f} more favor")
    
    print("✅ Pantheon seeded")
    return p
