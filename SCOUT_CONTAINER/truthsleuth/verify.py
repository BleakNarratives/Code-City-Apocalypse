import json
from pathlib import Path
import subprocess
import sys

# Self-locating import (Crostini-native, no Android hardcodes).
_PKG_DIR = Path(__file__).resolve().parent          # .../truthsleuth
_PKG_PARENT = _PKG_DIR.parent                         # .../SCOUT_CONTAINER
for _p in (_PKG_PARENT, _PKG_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from truthsleuth.config import ROOT_DIR  # noqa: E402

# Crostini-resolved relay log (was /storage/emulated/0/.../relay_log.jsonl).
LOOM_RELAY_LOG = ROOT_DIR / "logs" / "motherbrain_relay_log.jsonl"


def verify_codebase_update(file_path: Path):
    """
    Checks if a file has been updated by verifying current status via git.
    This links TruthSleuth's arbitration to the source of truth (Git).
    """
    print(f"[*] Verifying implementation for: {file_path}")
    result = subprocess.run(
        ["git", "status", "--porcelain", str(file_path)],
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(f"  -> Implementation verified (dirty/uncommitted): {result.stdout.strip()}")
        return True
    return False


def log_to_loom(finding: str, status: str):
    """
    Persistence layer for TruthSleuth findings via Loom DB.
    """
    log_entry = {"finding": finding, "status": status}
    print(f"[*] Persisting to Loom: {json.dumps(log_entry)}")

    try:
        LOOM_RELAY_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOOM_RELAY_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except OSError as e:
        print(f"[*] Loom persistence failed: {e}")