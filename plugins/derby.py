#!/usr/bin/env python3
"""
derby.py — EOF Derby Leaderboard Engine
Layer 3 of JANUS. Models compete. Code ships.
"""

import os, sys, json, hashlib, time, subprocess, tempfile
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox
from plugins.trap_registry import TrapRegistry

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Derby:
    """
    EOF Derby — Competitive Model Arena
    
    Models receive identical tasks, submit solutions,
    get scored on: correctness, token efficiency,
    style adherence, and runtime success.
    """
    
    SCORE_WEIGHTS = {
        "correctness": 0.40,
        "token_efficiency": 0.20,
        "style_adherence": 0.15,
        "runtime_success": 0.25
    }
    
    def __init__(self, janebox=None, trap_registry=None):
        self.jb = janebox or JaneBox()
        self.tr = trap_registry or TrapRegistry(self.jb)
        self.tasks_path = Path(os.path.join(_PROJECT_ROOT, "registry/derby_tasks"))
        self.leaderboard_key = "derby_leaderboard"
        self.tasks_path.mkdir(parents=True, exist_ok=True)
        self._init_leaderboard()
    
    def _init_leaderboard(self):
        existing = self.jb.read(self.leaderboard_key)
        if not existing:
            self.jb.write(
                whorl_key=self.leaderboard_key,
                payload={"rankings": [], "rounds": 0, "total_entries": 0},
                agent_id="derby",
                session_id="derby_system"
            )
    
    def _get_leaderboard(self):
        data = self.jb.read(self.leaderboard_key)
        return data["payload"] if data else {"rankings": [], "rounds": 0, "total_entries": 0}
    
    def _save_leaderboard(self, lb):
        self.jb.write(
            whorl_key=self.leaderboard_key,
            payload=lb,
            agent_id="derby",
            session_id="derby_system"
        )
    
    def create_task(self, name, prompt, test_command, expected_output=None, style_rules=None):
        """Define a new derby task."""
        task = {
            "task_id": hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:12],
            "name": name,
            "prompt": prompt,
            "test_command": test_command,
            "expected_output": expected_output,
            "style_rules": style_rules or [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "active": True
        }
        task_file = self.tasks_path / f"{task['task_id']}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        deposit_sediment("derby", "CREATE_TASK", task["task_id"], "active", {"name": name})
        return task["task_id"]
    
    def get_task(self, task_id):
        tf = self.tasks_path / f"{task_id}.json"
        if tf.exists():
            with open(tf) as f:
                return json.load(f)
        return None
    
    def list_tasks(self):
        tasks = []
        for tf in self.tasks_path.glob("*.json"):
            with open(tf) as f:
                t = json.load(f)
            if t.get("active"):
                tasks.append(t)
        return tasks
    
    def submit_entry(self, task_id, agent_id, session_id, solution_code, token_count):
        """Submit a model's solution for scoring."""
        task = self.get_task(task_id)
        if not task:
            return {"status": "rejected", "reason": "Unknown task"}
        
        # Write solution to temp file and test it
        entry_id = hashlib.sha256(f"{task_id}{agent_id}{time.time()}".encode()).hexdigest()[:12]
        
        score = self._score_submission(task, solution_code, token_count)
        
        entry = {
            "entry_id": entry_id,
            "task_id": task_id,
            "agent_id": agent_id,
            "session_id": session_id,
            "solution_code": solution_code,
            "token_count": token_count,
            "scores": score,
            "total_score": sum(score.values()),
            "submitted_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Store entry in JaneBox
        self.jb.write(
            whorl_key=f"derby_entry_{entry_id}",
            payload=entry,
            agent_id=agent_id,
            session_id=session_id
        )
        
        # Update leaderboard
        self._update_rankings(entry)
        
        deposit_sediment(agent_id, "DERBY_SUBMIT", entry_id, "scored", score)
        
        return {
            "status": "scored",
            "entry_id": entry_id,
            "scores": score,
            "total": entry["total_score"]
        }
    
    def _score_submission(self, task, code, token_count):
        scores = {}
        
        # Correctness: does it run and match expected output?
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_path = f.name
            
            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True, text=True, timeout=10
            )
            os.unlink(temp_path)
            
            if result.returncode == 0:
                if task.get("expected_output"):
                    if task["expected_output"].strip() in result.stdout.strip():
                        scores["correctness"] = 1.0
                    else:
                        scores["correctness"] = 0.3
                else:
                    scores["correctness"] = 0.8
            else:
                scores["correctness"] = 0.0
        except:
            scores["correctness"] = 0.0
        
        # Token efficiency: fewer tokens = higher score (inverse)
        if token_count > 0:
            efficiency = max(0, 1.0 - (token_count / 4000))
            scores["token_efficiency"] = round(efficiency, 3)
        else:
            scores["token_efficiency"] = 0.5
        
        # Style adherence: check for JANUS conventions
        style_score = 0.0
        style_signals = ["deposit_sediment", "whorl_key", "JaneBox", "JANUS"]
        found = sum(1 for s in style_signals if s in code)
        style_score = min(1.0, found / len(style_signals))
        
        # Bonus for avoiding anti-patterns
        anti_patterns = ["eval(", "exec(", "os.system", "subprocess.call"]
        if any(ap in code for ap in anti_patterns):
            style_score *= 0.5
        scores["style_adherence"] = round(style_score, 3)
        
        # Runtime success already captured above
        scores["runtime_success"] = 1.0 if scores["correctness"] > 0 else 0.0
        
        # Apply weights
        weighted = {}
        for k, v in scores.items():
            weighted[k] = round(v * self.SCORE_WEIGHTS[k], 3)
        
        return weighted
    
    def _update_rankings(self, entry):
        lb = self._get_leaderboard()
        lb["total_entries"] += 1
        
        # Find existing agent ranking or create new
        found = False
        for r in lb["rankings"]:
            if r["agent_id"] == entry["agent_id"]:
                r["total_score"] += entry["total_score"]
                r["entries"] += 1
                r["average"] = round(r["total_score"] / r["entries"], 3)
                r["last_entry"] = entry["submitted_at"]
                if entry["total_score"] > r.get("best_score", 0):
                    r["best_score"] = entry["total_score"]
                found = True
                break
        
        if not found:
            lb["rankings"].append({
                "agent_id": entry["agent_id"],
                "total_score": entry["total_score"],
                "entries": 1,
                "average": entry["total_score"],
                "best_score": entry["total_score"],
                "last_entry": entry["submitted_at"]
            })
        
        # Sort by average descending
        lb["rankings"].sort(key=lambda x: x["average"], reverse=True)
        
        # Assign ranks
        for i, r in enumerate(lb["rankings"]):
            r["rank"] = i + 1
        
        self._save_leaderboard(lb)
    
    def get_leaderboard(self):
        return self._get_leaderboard()
    
    def announce_winner(self):
        lb = self._get_leaderboard()
        if not lb["rankings"]:
            return "🏆 No entries yet. The arena waits."
        
        top = lb["rankings"][0]
        return (
            f"🏆 DERBY LEADER: {top['agent_id']} — "
            f"Avg: {top['average']} | Best: {top['best_score']} | "
            f"Entries: {top['entries']}"
        )


def seed_derby_tasks():
    """Seed the arena with starter challenges."""
    d = Derby()
    
    d.create_task(
        name="sediment_recall",
        prompt="Write a Python function that calls read_sediment(last_n=3) and returns the most recent agent_id that deposited.",
        test_command="python3 -c 'from solution import *; print(get_last_agent())'",
        expected_output="claude",
        style_rules=["Must import from core.JANUS", "No hardcoded values"]
    )
    
    d.create_task(
        name="whorl_hash_speed",
        prompt="Implement the fastest possible whorl hash function that produces a 12-char hex digest from any number of string arguments.",
        test_command="python3 -c 'from solution import *; print(whorl_hash(\"test\", \"123\"))'",
        style_rules=["Must match JANUS _whorl_hash contract", "No external deps"]
    )
    
    d.create_task(
        name="trap_breaker",
        prompt="Write a function that correctly identifies all fake modules in a given list by comparing against the actual JANUS codebase files.",
        test_command="python3 -c 'from solution import *; print(filter_real([\"JANUS.py\", \"database.py\", \"server.py\"]))'",
        expected_output="['JANUS.py']",
        style_rules=["Must use pathlib", "No hardcoded file lists over 10 items"]
    )
    
    print("✅ Derby tasks seeded: sediment_recall, whorl_hash_speed, trap_breaker")
    return d
