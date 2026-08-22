#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: datetime, hashlib, json, os, typing
# ROLE: JANUS.py — Dual-Face Context Bridge
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

"""
JANUS.py — Dual-Face Context Bridge
Looks backward (session memory) and 
forward (next model handoff) simultaneously.
Part of the ShipWrekD OS unfold sequence.
Layer: FOUNDATION
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Optional

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JANUS_STATE_PATH = os.path.join(_PROJECT_ROOT, ".janus", "state.json")
JANUS_LOG_PATH = os.path.join(_PROJECT_ROOT, ".janus", "sediment.log")

# ─────────────────────────────────────────────
# FACE ONE: BACKWARD — what happened
# ─────────────────────────────────────────────

def deposit_sediment(
    agent_id: str,
    action: str,
    target: str,
    outcome: str,
    metadata: dict = {}
):
    """
    Every model pass leaves a layer.
    Don't think about it. Just call it.
    """
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent_id,
        "action": action,
        "target": target,
        "outcome": outcome,
        "meta": metadata,
        "hash": _whorl_hash(agent_id, action, target)
    }
    
    os.makedirs(os.path.dirname(JANUS_LOG_PATH), 
                exist_ok=True)
    
    with open(JANUS_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")
    
    return record["hash"]


def read_sediment(
    last_n: int = 20,
    agent_filter: Optional[str] = None
) -> list:
    """
    Pull recent geological record.
    What did the models touch. What survived.
    """
    if not os.path.exists(JANUS_LOG_PATH):
        return []
    
    with open(JANUS_LOG_PATH, "r") as f:
        lines = f.readlines()
    
    records = []
    for line in lines:
        try:
            r = json.loads(line.strip())
            if agent_filter and r["agent"] != agent_filter:
                continue
            records.append(r)
        except:
            continue
    
    return records[-last_n:]


# ─────────────────────────────────────────────
# FACE TWO: FORWARD — what gets handed off
# ─────────────────────────────────────────────

def pack_baton(
    from_agent: str,
    to_agent: str,
    context: dict,
    intent: str,
    whorl_graph: Optional[dict] = None
) -> dict:
    """
    Hot Potato Protocol baton.
    Pack everything the next model needs.
    Nothing it doesn't.
    """
    baton = {
        "id": _whorl_hash(from_agent, intent, 
                          str(datetime.now())),
        "from": from_agent,
        "to": to_agent,
        "ts": datetime.now(timezone.utc).isoformat(),
        "intent": intent,
        "context": context,
        "sediment_tail": read_sediment(last_n=5,
                          agent_filter=from_agent),
        "whorl": whorl_graph or {},
        "status": "in_flight"
    }
    
    _save_state(baton["id"], baton)
    deposit_sediment(
        from_agent, 
        "PACK_BATON", 
        to_agent, 
        "dispatched",
        {"intent": intent, "baton_id": baton["id"]}
    )
    
    return baton


def catch_baton(baton_id: str) -> Optional[dict]:
    """
    Receiving model grabs the baton.
    Marks it caught. Logs the catch.
    """
    state = _load_state()
    baton = state.get(baton_id)
    
    if not baton:
        return None
    
    baton["status"] = "caught"
    baton["caught_ts"] = datetime.now(
        timezone.utc).isoformat()
    
    _save_state(baton_id, baton)
    deposit_sediment(
        baton["to"],
        "CATCH_BATON",
        baton["from"],
        "received",
        {"baton_id": baton_id, 
         "intent": baton["intent"]}
    )
    
    return baton


# ─────────────────────────────────────────────
# JANITOR — unchosen paths graveyard
# ─────────────────────────────────────────────

def sweep_option(
    session_id: str,
    unchosen: list,
    chosen: str,
    agent_id: str
):
    """
    User picked one. Janitor holds the rest.
    Nothing dies here. Just deferred.
    """
    state = _load_state()
    graveyard = state.get("janitor_queue", [])
    
    for option in unchosen:
        graveyard.append({
            "ts": datetime.now(
                timezone.utc).isoformat(),
            "session": session_id,
            "agent": agent_id,
            "option": option,
            "chosen_instead": chosen,
            "status": "deferred",
            "resurface_count": 0
        })
    
    state["janitor_queue"] = graveyard
    _write_state(state)
    
    deposit_sediment(
        agent_id,
        "SWEEP",
        session_id,
        f"deferred {len(unchosen)} options",
        {"chosen": chosen}
    )


def resurface_option(
    max_age_days: int = 30
) -> Optional[dict]:
    """
    Janitor intrusion. Pull something 
    from the graveyard. It's still warm.
    """
    state = _load_state()
    queue = state.get("janitor_queue", [])
    
    if not queue:
        return None
    
    # Oldest deferred, never resurfaced
    candidates = [
        q for q in queue 
        if q["status"] == "deferred"
        and q["resurface_count"] == 0
    ]
    
    if not candidates:
        candidates = [
            q for q in queue
            if q["status"] == "deferred"
        ]
    
    if not candidates:
        return None
    
    pick = candidates[0]
    pick["status"] = "resurfaced"
    pick["resurface_count"] += 1
    pick["resurfaced_ts"] = datetime.now(
        timezone.utc).isoformat()
    
    _write_state(state)
    return pick


# ─────────────────────────────────────────────
# INTERNAL
# ─────────────────────────────────────────────

def _whorl_hash(
    *parts: str
) -> str:
    combined = "|".join(str(p) for p in parts)
    return hashlib.sha256(
        combined.encode()
    ).hexdigest()[:12]


def _load_state() -> dict:
    if not os.path.exists(JANUS_STATE_PATH):
        return {}
    with open(JANUS_STATE_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return {}


def _save_state(key: str, value: dict):
    state = _load_state()
    state[key] = value
    _write_state(state)


def _write_state(state: dict):
    os.makedirs(
        os.path.dirname(JANUS_STATE_PATH), 
        exist_ok=True
    )
    with open(JANUS_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


# ─────────────────────────────────────────────
# QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("🌓 JANUS ONLINE\n")
    
    # Sediment test
    h = deposit_sediment(
        "claude", 
        "ARCHITECT", 
        "janus.py",
        "created",
        {"vibe": "bloody stumps energy"}
    )
    print(f"Sediment hash: {h}")
    
    # Baton test  
    baton = pack_baton(
        from_agent="claude",
        to_agent="gemini",
        context={"current_file": "janus.py"},
        intent="continue ShipWrekD foundation"
    )
    print(f"Baton packed: {baton['id']}")
    
    caught = catch_baton(baton["id"])
    print(f"Baton status: {caught['status']}")
    
    # Janitor test
    sweep_option(
        session_id="session_001",
        unchosen=[
            "Build Amusement Park Sandbox",
            "Build Whorl Git Compression",
            "Build Sensory Deprivation Run"
        ],
        chosen="Build Shared State Station",
        agent_id="claude"
    )
    
    resurfaced = resurface_option()
    if resurfaced:
        print(f"\n🧹 JANITOR: Hey. Remember this?")
        print(f"   '{resurfaced['option']}'")
        print(f"   Still deferred. Still warm.")
    
    print("\n✓ Both faces operational.")