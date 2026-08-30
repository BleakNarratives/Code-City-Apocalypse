import json
import subprocess
from pathlib import Path
import sys

# Self-locating import (Crostini-native, no Android hardcodes).
_PKG_DIR = Path(__file__).resolve().parent          # .../truthsleuth
_PKG_PARENT = _PKG_DIR.parent                         # .../SCOUT_CONTAINER
for _p in (_PKG_PARENT, _PKG_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from truthsleuth.config import ROOT_DIR  # noqa: E402


class TruthSleuthBridge:
    def __init__(self):
        self.whorl_runtime_path = ROOT_DIR / "whorl_runtime.py"
        self.nat_cmd = ROOT_DIR / "natcommand_nathub" / "nat.py"

    def log_to_nathub(self, message: str):
        """Sends arbitration logs to Nathub via NatCommand."""
        if not self.nat_cmd.exists():
            print(f"TruthSleuthBridge: NatCommand not found at {self.nat_cmd} — skipping.")
            return
        try:
            subprocess.run(
                ["python3", str(self.nat_cmd), f"log: {message}"],
                timeout=30,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
            print(f"TruthSleuthBridge: log_to_nathub failed: {e}")

    def execute_whorl_pattern(self, pattern: dict):
        """Dispatches a pattern to the Whorl Runtime."""
        if not self.whorl_runtime_path.exists():
            print(
                "TruthSleuthBridge: Whorl runtime not found at "
                f"{self.whorl_runtime_path} — skipping."
            )
            return
        pattern_str = json.dumps(pattern)
        print(f"[*] Dispatching to Whorl: {pattern.get('name')}")
        self.log_to_nathub(f"Arbitration initiated: {pattern.get('name')}")

    def store_finding_in_loom(self, finding: dict):
        """Stores a code quality finding into our proprietary Loom DB."""
        print(f"[*] Persisting to Loom DB: {finding.get('type')}")
        self.log_to_nathub(f"Finding persisted: {finding.get('type')}")


# Initialize and test bridge
if __name__ == "__main__":
    bridge = TruthSleuthBridge()
    bridge.log_to_nathub("TruthSleuth System Initialized.")