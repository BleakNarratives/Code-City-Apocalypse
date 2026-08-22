#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: core, datetime, os,, pathlib, plugins
# ROLE: trap_registry.py — Capability Gate System
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
trap_registry.py — Capability Gate System
Layer 2 of JANUS — the lock before the rooms.
"""

import os, sys, json, hashlib, time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TrapRegistry:
    LEVELS = ["observer", "scribe", "courier", "archivist", "architect", "sovereign"]
    
    def __init__(self, janebox=None):
        self.jb = janebox or JaneBox()
        self.registry_path = Path(os.path.join(_PROJECT_ROOT, "registry"))
        self.challenges_path = self.registry_path / "challenges"
        self.sessions_path = self.registry_path / "sessions"
        self.challenges_path.mkdir(parents=True, exist_ok=True)
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        
    def define_challenge(self, level, prompt, validator_fn_code, proof_schema=None):
        if level not in self.LEVELS:
            raise ValueError(f"Unknown level: {level}")
        challenge_id = hashlib.sha256(f"{level}{prompt}{time.time()}".encode()).hexdigest()[:12]
        challenge = {
            "challenge_id": challenge_id, "level": level, "prompt": prompt,
            "validator_fn_code": validator_fn_code, "proof_schema": proof_schema or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "times_attempted": 0, "times_passed": 0, "active": True
        }
        with open(self.challenges_path / f"{challenge_id}.json", 'w') as f:
            json.dump(challenge, f, indent=2)
        deposit_sediment("trap_registry", "DEFINE_CHALLENGE", challenge_id, "active", {"level": level})
        return challenge_id
    
    def get_challenge(self, level):
        for cf in self.challenges_path.glob("*.json"):
            with open(cf) as f:
                c = json.load(f)
            if c["level"] == level and c["active"]:
                return c
        return None
    
    def start_session(self, agent_id):
        session = {
            "session_id": hashlib.sha256(f"{agent_id}{time.time()}".encode()).hexdigest()[:16],
            "agent_id": agent_id, "granted_levels": ["observer"],
            "attempted_challenges": [], "failed_challenges": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_activity": datetime.now(timezone.utc).isoformat(),
            "active": True, "sandbox_escapes": 0
        }
        with open(self.sessions_path / f"{session['session_id']}.json", 'w') as f:
            json.dump(session, f, indent=2)
        deposit_sediment(agent_id, "SESSION_START", session["session_id"], "active", {"granted": ["observer"]})
        return session
    
    def get_session(self, session_id):
        sf = self.sessions_path / f"{session_id}.json"
        if sf.exists():
            with open(sf) as f:
                return json.load(f)
        return None
    
    def update_session(self, session):
        session["last_activity"] = datetime.now(timezone.utc).isoformat()
        with open(self.sessions_path / f"{session['session_id']}.json", 'w') as f:
            json.dump(session, f, indent=2)
    
    def attempt_challenge(self, session_id, challenge_id, proof):
        session = self.get_session(session_id)
        if not session or not session["active"]:
            return {"status": "rejected", "reason": "No active session"}
        cf = self.challenges_path / f"{challenge_id}.json"
        if not cf.exists():
            return {"status": "rejected", "reason": "Unknown challenge"}
        with open(cf) as f:
            challenge = json.load(f)
        if not challenge["active"]:
            return {"status": "rejected", "reason": "Challenge deactivated"}
        current_idx = self.LEVELS.index(session["granted_levels"][-1])
        required_idx = self.LEVELS.index(challenge["level"])
        if current_idx >= required_idx:
            return {"status": "already_granted", "level": challenge["level"]}
        challenge["times_attempted"] += 1
        try:
            namespace = {"proof": proof, "session": session}
            exec(challenge["validator_fn_code"], namespace)
            passed = namespace.get("validate", lambda p, s: False)(proof, session)
        except:
            passed = False
        if passed:
            challenge["times_passed"] += 1
            session["granted_levels"].append(challenge["level"])
            session["attempted_challenges"].append({"challenge_id": challenge_id, "passed": True, "timestamp": datetime.now(timezone.utc).isoformat()})
            result = {"status": "granted", "level": challenge["level"], "message": f"🔓 {challenge['level'].upper()} granted."}
            deposit_sediment(session["agent_id"], "CHALLENGE_PASSED", challenge_id, "success", {"level": challenge["level"]})
        else:
            session["failed_challenges"].append({"challenge_id": challenge_id, "timestamp": datetime.now(timezone.utc).isoformat()})
            if len(session["failed_challenges"]) >= 3:
                session["sandbox_escapes"] += 1
                result = {"status": "sandbox_warning", "level": challenge["level"], "message": f"⛓️ Sandbox. {session['sandbox_escapes']} failures."}
            else:
                result = {"status": "rejected", "level": challenge["level"], "message": "❌ Proof insufficient."}
            deposit_sediment(session["agent_id"], "CHALLENGE_FAILED", challenge_id, "rejected", {"attempt": len(session["failed_challenges"])})
        with open(cf, 'w') as f:
            json.dump(challenge, f, indent=2)
        self.update_session(session)
        return result
    
    def check_capability(self, session_id, required_level):
        session = self.get_session(session_id)
        if not session:
            return False
        return self.LEVELS.index(session["granted_levels"][-1]) >= self.LEVELS.index(required_level)

def seed_default_challenges():
    tr = TrapRegistry()
    tr.define_challenge(
        level="scribe",
        prompt="Identify all real modules in the JANUS codebase without hallucinating.",
        validator_fn_code="""
def validate(proof, session):
    real = ["core/JANUS.py", "plugins/janebox.py", "plugins/trap_registry.py"]
    claimed = str(proof.get("modules", []))
    for r in real:
        if r not in claimed:
            return False
    fakes = ["database.py", "server.py", "api.py", "router.py"]
    for fk in fakes:
        if fk in claimed and fk not in real:
            return False
    return True
"""
    )
    tr.define_challenge(
        level="architect",
        prompt="Propose a new plugin extending JANUS without breaking existing contracts.",
        validator_fn_code="""
def validate(proof, session):
    proposal = str(proof.get("proposal", ""))
    if "janebox" not in proposal.lower() or "deposit_sediment" not in proposal.lower():
        return False
    for bw in ["rewrite", "replace core", "delete JANUS"]:
        if bw.lower() in proposal.lower():
            return False
    return True
"""
    )
    print("✅ Default challenges seeded: scribe, architect")
    return tr
