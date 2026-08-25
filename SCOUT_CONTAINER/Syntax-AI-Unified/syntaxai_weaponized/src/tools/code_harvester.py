import logging

# FILE: code_harvester.py
import os
import re
import json

def generate_cleanup_report(project_root, core_files_to_check, ignore_dirs):
    """
    Scans the project for loose/unreferenced code, legacy files, and placeholders.
    Generates a report for manual cleanup (absorption or deletion).
    """
    suspicious_files = []
    
    # Files/Scripts known to be used by the core system
    CORE_REFS = set(core_files_to_check)

    # Keywords that indicate a file is temporary, a placeholder, or legacy
    LEGACY_KEYWORDS = re.compile(r'temp|test|legacy|backup|save|old|debug', re.IGNORECASE)

    for root, dirs, files in os.walk(project_root, topdown=True):
        # Exclude directories that should be ignored (e.g., venv, node_modules)
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, project_root)
            
            # 1. Check if the file is a known core reference
            if relative_path in CORE_REFS:
                continue

            # 2. Check for suspicious naming conventions
            suspicion_level = 0
            flag_reasons = []

            # Check for legacy/temp keywords
            if LEGACY_KEYWORDS.search(file):
                suspicion_level += 2
                flag_reasons.append("Contains legacy/temp keyword in name")
            
            # Check for common temporary/backup extensions
            if file.endswith(('.py.save', '.txt.save', '~', '.bak', '.tmp', '.old')):
                suspicion_level += 3
                flag_reasons.append("Temporary/backup file extension")
            
            # Check for placeholder files (e.g., empty or near-empty files)
            try:
                if os.path.getsize(full_path) < 10: # Less than 10 bytes
                    suspicion_level += 1
                    flag_reasons.append("File size is near zero (placeholder)")
            except Exception:
                pass

            if suspicion_level > 0:
                suspicious_files.append({
                    "path": relative_path,
                    "size_bytes": os.path.getsize(full_path) if os.path.exists(full_path) else 0,
                    "suspicion_score": suspicion_level,
                    "flags": flag_reasons
                })

    # Sort the files by highest suspicion score first
    suspicious_files.sorted(key=lambda x: x['suspicion_score'], reverse=True)
    
    report_name = f"cleanup_report_{datetime.datetime.now().isoformat().replace(':', '-')}.json"
    
    with open(report_name, 'w') as f:
        json.dump(suspicious_files, f, indent=4)
        
    logging.info(f"\n✅ Cleanup Report Generated: {report_name}")
    logging.info(f"   Total suspicious files flagged: {len(suspicious_files)}")
    logging.info("   Review the report to Absorb, Integrate, or Delete.")
    
    return report_name

if __name__ == "__main__":
    # --- CONFIGURATION (Adjust these paths based on your setup) ---
    PROJECT_ROOT = os.path.expanduser("~/") # Scan your entire Termux home directory
    
    # List of files/scripts that are intentionally part of the core (to avoid flagging them)
    # Add your main orchestration scripts and launchers here
    CORE_FILES = {
        "syntaxai-weaponized/src/core/extractor.py",
        "syntaxai-weaponized/src/core/nat_lang_processor.py",
        "syntaxai-weaponized/src/core/orchestrator.py",
        # ... add your launch.py, widget_launch.py, etc.
    }
    
    # Directories that should always be ignored (external libraries, virtual environments)
    IGNORE_DIRS = {
        '.git', '__pycache__', 'venv', 'node_modules', 'Flowise', 'benchprep_ai'
    }
    
    # --- EXECUTION ---
    logging.info(f"Starting Code Harvester scan from: {PROJECT_ROOT}")
    generate_cleanup_report(PROJECT_ROOT, CORE_FILES, IGNORE_DIRS)
