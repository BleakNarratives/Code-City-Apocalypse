#!/usr/bin/env python3
"""
Phase 2 – Loom Daemon
Continuously syncs peer state, monitors integrity, and runs self-tests.
"""

import json, time, hashlib, threading, os, sys
from datetime import datetime
from pathlib import Path
from fiber_core import DataFiber
from celtic_crypto import CelticDataLoom
from red_team_attacks import RedTeamAttacker   # optional if file exists

PEER_FILE = "/home/bleaknarratives/Code-City-Apocalypse/peerlist.json"
SYNC_INTERVAL = 60          # seconds between sync attempts
INTEGRITY_CHECK_INTERVAL = 180
REDTEAM_INTERVAL = 600      # optional self-test every 10 min

class LoomDaemon:
    def __init__(self):
        self.loom = CelticDataLoom()
        self.last_sync = None
        self.running = True
        self.peers = self._load_peers()
        print(f"🛰️  Loom Daemon initialized ({len(self.peers)} peers)")

    def _load_peers(self):
        if os.path.exists(PEER_FILE):
            try:
                with open(PEER_FILE) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Peerlist load error: {e}")
        return []

    def sync_peers(self):
        """Fake peer sync until network layer implemented"""
        print(f"[{datetime.now().isoformat()}] 🔄 Syncing peers...")
        if not self.peers:
            print("   No peers found.  (Add IPs to peerlist.json)")
            return
        # compute local state hash
        state = json.dumps(self.loom.get_collective_status(), sort_keys=True)
        state_hash = hashlib.sha3_256(state.encode()).hexdigest()[:16]
        print(f"   Local collective hash → {state_hash}")
        # simulate exchange
        for peer in self.peers:
            print(f"   ↔ Pinged {peer}")
        self.last_sync = datetime.now()

    def integrity_check(self):
        print(f"[{datetime.now().isoformat()}] 🧩 Running integrity check…")
        status = self.loom.get_collective_status()
        print(f"   Fibers:{status['total_fibers']}  Knots:{status['total_celtic_knots']}")
        print(f"   Security:{status['security_level']}  Hash:{status['collective_integrity_hash'][:16]}...")

    def self_test(self):
        if 'RedTeamAttacker' in globals():
            print(f"[{datetime.now().isoformat()}] 🛡️ Launching self-defense test…")
            attacker = RedTeamAttacker(self.loom)
            results = attacker.run_all_attacks()
            print(f"   Red-team cycle complete, success={results['successful_attacks']}")
        else:
            print("   🔸 Red-team module not present – skipped.")

    def loop(self):
        print("🚀 Loom Daemon running — Ctrl +C to stop\n")
        t0 = time.time()
        while self.running:
            now = time.time()
            if now - t0 >= SYNC_INTERVAL:
                self.sync_peers();  t0 = now
            if int(now) % INTEGRITY_CHECK_INTERVAL == 0:
                self.integrity_check()
            if int(now) % REDTEAM_INTERVAL == 0:
                self.self_test()
            time.sleep(5)

if __name__ == "__main__":
    try:
        daemon = LoomDaemon()
        daemon.loop()
    except KeyboardInterrupt:
        print("\n🛑 Daemon stopped by user.")
