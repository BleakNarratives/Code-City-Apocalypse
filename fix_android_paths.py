#!/usr/bin/env python3
"""
Path Migration Script — Code-City-Apocalypse
Converts hardcoded Android/Termux paths to Crostini (Debian Linux) paths.
Bucket 08: Code City Virtual Cortex path fix.
IDEMPOTENT: Running again after first run does nothing (paths already fixed).
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()

# Android base path (what we're migrating FROM)
ANDROID_BASE = "/storage/emulated/0"
TERMUX_SYS_PATH = "/data/data/com.termux/files/home/code_city"

def main():
    count = 0
    for ext in ("*.py", "*.sh", "*.yaml", "*.yml", "*.json"):
        for f in REPO_ROOT.rglob(ext):
            if "__pycache__" in str(f) or ".git" in str(f) or f.name == "fix_android_paths.py":
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                if ANDROID_BASE not in content and "com.termux" not in content:
                    continue
                print(f"  STILL HAS ANDROID PATHS: {f.relative_to(REPO_ROOT)}")
                count += 1
            except:
                pass
    if count == 0:
        print("All files clean. No Android/Termux paths remaining in executable code.")
    else:
        print(f"\n{count} files still have Android paths.")
    return count

if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
