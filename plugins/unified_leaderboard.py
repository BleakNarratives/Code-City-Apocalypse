#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: collections, core, datetime, os,, pathlib, plugins
# ROLE: unified_leaderboard.py — Models, Users, Swarms, and Gladiator Showdowns.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
unified_leaderboard.py — Models, Users, Swarms, and Gladiator Showdowns.
One leaderboard to rank them all. Feeds Quantum Derby odds.
"""

import os, sys, json, time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class UnifiedLeaderboard:
    """Tracks every entity — model, user, or swarm — across all competitions."""
    
    ENTITY_TYPES = ["model", "user", "swarm"]
    CATEGORIES = ["overall", "derby", "gauntlet", "quantum", "gladiator", "park"]
    
    def __init__(self, janebox=None):
        self.jb = janebox or JaneBox()
        self.board_key = "unified_leaderboard"
        self._init_board()
    
    def _init_board(self):
        if not self.jb.read(self.board_key):
            self.jb.write(self.board_key, {
                "rankings": [],
                "gladiator_showdowns": [],
                "vanity_waves": [],
                "updated_at": datetime.now(timezone.utc).isoformat()
            }, "unified_leaderboard", "system")
    
    def _get_board(self):
        data = self.jb.read(self.board_key)
        return data["payload"] if data else {"rankings": [], "gladiator_showdowns": [], "vanity_waves": []}
    
    def _save_board(self, board):
        board["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.jb.write(self.board_key, board, "unified_leaderboard", "system")
    
    def register_entity(self, entity_id, entity_type="model", display_name=None):
        """Register a new entity in the leaderboard."""
        if entity_type not in self.ENTITY_TYPES:
            return {"status": "rejected", "reason": f"Type must be one of {self.ENTITY_TYPES}"}
        
        board = self._get_board()
        existing = next((r for r in board["rankings"] if r["entity_id"] == entity_id), None)
        if existing:
            return {"status": "already_registered", "entity": existing}
        
        entry = {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "display_name": display_name or entity_id,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "scores": {cat: 0.0 for cat in self.CATEGORIES},
            "total_score": 0.0,
            "entries": 0,
            "best_score": 0.0,
            "rank": len(board["rankings"]) + 1,
            "badges": []
        }
        board["rankings"].append(entry)
        self._recalculate_ranks(board)
        self._save_board(board)
        deposit_sediment(entity_id, "REGISTERED", "unified_leaderboard", "registered", {"type": entity_type})
        return {"status": "registered", "entity": entry}
    
    def record_score(self, entity_id, category, score, metadata=None):
        """Record a score in any category and recalculate rankings."""
        if category not in self.CATEGORIES:
            return {"status": "rejected", "reason": f"Category must be one of {self.CATEGORIES}"}
        
        board = self._get_board()
        entity = next((r for r in board["rankings"] if r["entity_id"] == entity_id), None)
        if not entity:
            # Auto-register
            result = self.register_entity(entity_id)
            if result["status"] not in ("registered", "already_registered"):
                return result
            board = self._get_board()
            entity = next((r for r in board["rankings"] if r["entity_id"] == entity_id), None)
        
        # Exponential moving average for stability
        alpha = 0.3
        entity["scores"][category] = round(
            entity["scores"][category] * (1 - alpha) + score * alpha, 3
        )
        entity["entries"] += 1
        entity["total_score"] = round(sum(entity["scores"].values()), 3)
        if score > entity["best_score"]:
            entity["best_score"] = score
        
        self._recalculate_ranks(board)
        
        if metadata:
            entity["last_metadata"] = metadata
        
        self._save_board(board)
        deposit_sediment(entity_id, f"SCORE_{category.upper()}", "unified_leaderboard", "recorded", {"score": score})
        
        return {"status": "recorded", "entity": entity, "new_rank": entity["rank"]}
    
    def record_gladiator_showdown(self, user_id, model_id, obstacle_id, user_survived, user_score, model_score):
        """Record a head-to-head Gladiator showdown."""
        board = self._get_board()
        showdown = {
            "showdown_id": f"sd_{int(time.time())}",
            "user_id": user_id,
            "model_id": model_id,
            "obstacle_id": obstacle_id,
            "user_survived": user_survived,
            "user_score": user_score,
            "model_score": model_score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        board["gladiator_showdowns"].append(showdown)
        self._save_board(board)
        
        # Update both entities' gladiator scores
        self.record_score(user_id, "gladiator", user_score, {"vs": model_id, "survived": user_survived})
        self.record_score(model_id, "gladiator", model_score, {"vs": user_id, "defended": not user_survived})
        
        deposit_sediment("gladiator", "SHOWDOWN", showdown["showdown_id"], 
                        "user_survived" if user_survived else "model_defended", showdown)
        
        return {"status": "recorded", "showdown": showdown}
    
    def award_vanity_wave(self, entity_id, wave_type="color_scheme", duration_hours=24):
        """Award a vanity prize — the entity's colors/name takes over the dashboard."""
        board = self._get_board()
        wave = {
            "entity_id": entity_id,
            "wave_type": wave_type,
            "starts_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": datetime.now(timezone.utc).isoformat(),
            "active": True
        }
        # Deactivate old waves
        for w in board["vanity_waves"]:
            w["active"] = False
        board["vanity_waves"].append(wave)
        self._save_board(board)
        deposit_sediment(entity_id, "VANITY_WAVE", wave_type, "awarded", {"duration_hours": duration_hours})
        return {"status": "awarded", "wave": wave}
    
    def get_active_vanity_wave(self):
        board = self._get_board()
        for w in board["vanity_waves"]:
            if w.get("active"):
                return w
        return None
    
    def get_rankings(self, entity_type=None, category="overall", limit=10):
        """Get filtered rankings."""
        board = self._get_board()
        rankings = board["rankings"]
        if entity_type:
            rankings = [r for r in rankings if r["entity_type"] == entity_type]
        
        if category == "overall":
            rankings.sort(key=lambda r: r["total_score"], reverse=True)
        else:
            rankings.sort(key=lambda r: r["scores"].get(category, 0), reverse=True)
        
        for i, r in enumerate(rankings[:limit]):
            r["rank"] = i + 1
        
        return rankings[:limit]
    
    def get_head_to_head(self, entity_a, entity_b):
        """Get head-to-head stats between two entities."""
        board = self._get_board()
        showdowns = [s for s in board["gladiator_showdowns"] 
                    if (s["user_id"] in (entity_a, entity_b) and s["model_id"] in (entity_a, entity_b))]
        a_wins = sum(1 for s in showdowns if (s["user_id"] == entity_a and s["user_survived"]) or (s["model_id"] == entity_a and not s["user_survived"]))
        b_wins = len(showdowns) - a_wins
        return {"entity_a": entity_a, "entity_b": entity_b, "total_showdowns": len(showdowns), f"{entity_a}_wins": a_wins, f"{entity_b}_wins": b_wins}
    
    def _recalculate_ranks(self, board):
        board["rankings"].sort(key=lambda r: r["total_score"], reverse=True)
        for i, r in enumerate(board["rankings"]):
            r["rank"] = i + 1
    
    def get_dashboard_payload(self):
        """Ready-to-use payload for the dashboard."""
        board = self._get_board()
        return {
            "overall": self.get_rankings(limit=10),
            "models": self.get_rankings(entity_type="model", limit=5),
            "users": self.get_rankings(entity_type="user", limit=5),
            "gladiator_showdowns": board["gladiator_showdowns"][-5:],
            "active_vanity": self.get_active_vanity_wave(),
            "updated_at": board.get("updated_at", "")
        }


def seed_leaderboard():
    ul = UnifiedLeaderboard()
    ul.register_entity("claude", "model", "Claude")
    ul.register_entity("gemini", "model", "Gemini")
    ul.register_entity("user_demo", "user", "BleakNarratives")
    ul.record_score("claude", "derby", 0.85)
    ul.record_score("gemini", "derby", 0.72)
    ul.record_score("user_demo", "gauntlet", 0.998)
    ul.record_gladiator_showdown("user_demo", "claude", "warmup", True, 0.95, 0.45)
    print("✅ Unified Leaderboard seeded")
    return ul
