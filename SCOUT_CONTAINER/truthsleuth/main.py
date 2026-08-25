import time
import sys
import json
import threading
import subprocess
from pathlib import Path

# Add paths for local imports
sys.path.insert(0, "/storage/emulated/0/RootBase")
sys.path.insert(0, "/storage/emulated/0/RootBase/truthsleuth")

from truthsleuth.config import ROOT_DIR, EXCLUSION_PATTERNS, MONITORED_PATHS
from truthsleuth.monitor import start_monitoring, stop_monitoring, get_all_monitored_files
from truthsleuth.smell_sniffer.analysis import analyze_file
from truthsleuth.smell_sniffer.karma_oracle import TruthSleuthWildcard
from truthsleuth.reporter import generate_report
from truthsleuth.verify import verify_codebase_update, log_to_loom

# Agent Hierarchy:
# White Hat (TruthSleuth): Audits, reports, and monitors (Observation/Truth).
# Gray Hat (Molt Engines): Automated refactoring and logic improvement (Iteration/Growth).
# Brown Hat (Git/Persistence): Structural verification and immutable logging (Accountability/Persistence).

# Initialize tools
oracle = TruthSleuthWildcard()

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
            molt_cmd = [
                "python3", "/storage/emulated/0/RootBase/molt_v3_engine/molt_v3.py",
                f"Optimize code in {file_path}. Address issues: {[i['message'] for i in issues]}",
                "--headless", "--iters", "2"
            ]
            subprocess.run(molt_cmd)
            
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
