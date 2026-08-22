#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: core, datetime, dotenv, httpx, os,
# ROLE: janebox.py — Shared State Station. Raw httpx. Upsert-capable.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""janebox.py — Shared State Station. Raw httpx. Upsert-capable."""

import os, sys, hashlib
from datetime import datetime, timezone

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

import httpx
from core.JANUS import deposit_sediment

class JaneBox:
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        if not self.url or not self.key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY required in .env")
        self.base = f"{self.url}/rest/v1"
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def _whorl_hash(self, *parts) -> str:
        return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:12]

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def write(self, whorl_key, payload, agent_id, session_id):
        """Write or update a whorl. Uses upsert: POST with merge-duplicates."""
        data = {
            "session_id": session_id,
            "agent_id": agent_id,
            "whorl_key": whorl_key,
            "payload": payload,
            "status": "active",
            "updated_at": self._now()
        }
        r = httpx.post(
            f"{self.base}/janebox_state",
            headers={
                **self.headers,
                "Prefer": "resolution=merge-duplicates,return=representation"
            },
            json=data
        )
        # If merge-duplicates not supported, fall back to check+PATCH
        if r.status_code == 409:
            existing = self.read(whorl_key)
            if existing:
                r = httpx.patch(
                    f"{self.base}/janebox_state",
                    headers={**self.headers, "Prefer": "return=representation"},
                    params={"whorl_key": f"eq.{whorl_key}"},
                    json={"payload": payload, "agent_id": agent_id,
                          "session_id": session_id, "updated_at": self._now()}
                )
        r.raise_for_status()
        deposit_sediment(agent_id, "WRITE", whorl_key, "success", {"session": session_id})
        result = r.json()
        return result[0] if isinstance(result, list) else result

    def read(self, whorl_key):
        r = httpx.get(
            f"{self.base}/janebox_state",
            headers=self.headers,
            params={"whorl_key": f"eq.{whorl_key}", "status": "eq.active",
                    "order": "updated_at.desc", "limit": "1"}
        )
        r.raise_for_status()
        data = r.json()
        return data[0] if data else None

    def list_session(self, session_id):
        r = httpx.get(
            f"{self.base}/janebox_state",
            headers=self.headers,
            params={"session_id": f"eq.{session_id}", "status": "eq.active"}
        )
        r.raise_for_status()
        return r.json() or []

    def hand_off(self, from_agent, to_agent, whorl_key):
        if not self.read(whorl_key):
            raise ValueError(f"No active record for: {whorl_key}")
        r = httpx.patch(
            f"{self.base}/janebox_state",
            headers={**self.headers, "Prefer": "return=representation"},
            params={"whorl_key": f"eq.{whorl_key}", "status": "eq.active"},
            json={"agent_id": to_agent, "updated_at": self._now()}
        )
        r.raise_for_status()
        deposit_sediment(from_agent, "HAND_OFF", to_agent, "success", {"whorl_key": whorl_key})

    def delete(self, whorl_key):
        r = httpx.patch(
            f"{self.base}/janebox_state",
            headers={**self.headers, "Prefer": "return=representation"},
            params={"whorl_key": f"eq.{whorl_key}"},
            json={"status": "retired", "updated_at": self._now()}
        )
        r.raise_for_status()
        deposit_sediment("janebox", "DELETE", whorl_key, "retired", {})

    def health_check(self) -> bool:
        try:
            r = httpx.get(f"{self.base}/janebox_state", headers=self.headers, params={"limit": "1"})
            return r.status_code == 200
        except:
            return False
