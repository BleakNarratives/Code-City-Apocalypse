import time
import sys
import json
import threading
import subprocess
from pathlib import Path

# Self-locating import: add the package parent to sys.path so
# `from truthsleuth.config import ...` works regardless of CWD (no more
# Android-era /storage/emulated hardcoded paths).
_PKG_DIR = Path(__file__).resolve().parent          # .../truthsleuth
_PKG_PARENT = _PKG_DIR.parent                         # .../SCOUT_CONTAINER
for _p in (_PKG_PARENT, _PKG_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from truthsleuth.config import (  # noqa: E402
    ROOT_DIR,
    MONITORED_PATHS,
    MOLT_ENGINE,
    MOLT_ENGINE_KIND,
)
from truthsleuth.monitor import (  # noqa: E402
    start_monitoring,
    stop_monitoring,
)
from truthsleuth.smell_sniffer.analysis import analyze_file  # noqa: E402
from truthsleuth.smell_sniffer.karma_oracle import TruthSleuthWildcard  # noqa: E402
from truthsleuth.reporter import generate_report  # noqa: E402
from truthsleuth.verify import verify_codebase_update, log_to_loom  # noqa: E402

# Agent Hierarchy:
# White Hat (TruthSleuth): Audits, reports, and monitors (Observation/Truth).
# Gray Hat (Molt Engines): Automated refactoring and logic improvement (Iteration/Growth).
# Brown Hat (Git/Persistence): Structural verification and immutable logging (Accountability/Persistence).

# Initialize tools
oracle = TruthSleuthWildcard()


def dispatch_molt(file_path: Path, issues) -> None:
    """Gray Hat: dispatch an optimization to the Molt engine.

    Resolves the engine path from config and adapts CLI args per engine kind.
    Fails soft — a missing/unavailable engine logs a warning and is skipped,
    never crashing the monitor loop.
    """
    if MOLT_ENGINE is None:
        print(
            "TruthSleuth [Gray Hat]: Molt engine not found — set "
            "TRUTHSLEUTH_MOLT_ENGINE or restore molt_v3_engine/. Skipping "
            "optimization."
        )
        return

    prompt = (
        f"Optimize code in {file_path}. "
        f"Address issues: {[i.get('message', '') for i in issues]}"
    )

    if MOLT_ENGINE_KIND == "molt_v3":
        cmd = ["python3", str(MOLT_ENGINE), prompt, "--headless", "--iters", "2"]
    else:
        # ox_package shim: positional prompt only (reads argv/stdin).
        cmd = ["python3", str(MOLT_ENGINE), prompt]

    try:
        subprocess.run(cmd, timeout=180)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
        print(f"TruthSleuth [Gray Hat]: Molt dispatch failed: {e}")


def run():
    print("TruthSleuth: Initializing Arbitration Loop...")

    def _on_file_change(file_path: Path):
        print(f"TruthSleuth [White Hat]: Analyzing {file_path.relative_to(ROOT_DIR)}...")
        issues = analyze_file(str(file_path))

        if issues:
            impact = oracle.calculate_impact(issues)
            oracle.karma_score -= impact

            # Recursive Optimization [Gray Hat]
            print(f"TruthSleuth [Gray Hat]: Dispatching improvement...")
            dispatch_molt(file_path, issues)

            # Structural Accountability [Brown Hat]
            is_verified = verify_codebase_update(file_path)
            status = "Verified" if is_verified else "Pending/Failed"
            log_to_loom(f"Optimization for {file_path.name}", status)

            generate_report(issues)
        else:
            print(f"TruthSleuth: {file_path.relative_to(ROOT_DIR)} structurally sound.")

    # Start monitor
    monitor_thread = threading.Thread(target=start_monitoring, args=(10, _on_file_change))
    monitor_thread.daemon = True
    monitor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_monitoring()
        monitor_thread.join()


if __name__ == "__main__":
    run()
