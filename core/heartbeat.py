#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: datetime, os,, subprocess
# ROLE: HEARTBEAT — poor man's cron
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

"""
HEARTBEAT — poor man's cron
Runs scheduled jobs without crond.
Auto-discovers JANUS.py relative to this file.
"""
import os, sys, time
import subprocess
from datetime import datetime

# ── Dynamic path: find JANUS.py relative to this heartbeat file ──
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_JANUS_PATH = os.path.join(_PROJECT_ROOT, "core", "JANUS.py")

JOBS = [
    {
        "name": "janitor_resurface",
        "interval_seconds": 3600,
        "cmd": ["python3", _JANUS_PATH, "--resurface"]
    }
]

def run_job(job):
    print(f"[{datetime.now().isoformat()}] Running: {job['name']}")
    try:
        subprocess.run(job["cmd"], timeout=30)
    except Exception as e:
        print(f"  ✗ {job['name']} failed: {e}")

def main():
    print("💓 HEARTBEAT online")
    timers = {job["name"]: 0 for job in JOBS}
    
    while True:
        now = time.time()
        for job in JOBS:
            if now - timers[job["name"]] >= job["interval_seconds"]:
                run_job(job)
                timers[job["name"]] = now
        time.sleep(60)

if __name__ == "__main__":
    main()
