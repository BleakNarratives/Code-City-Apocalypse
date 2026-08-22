#!/usr/bin/env python3
"""
Path Migration VERIFICATION — Code-City-Apocalypse
Checks for remaining Android/Termux paths in executable code.
Platform-detection code (os.path.exists/com.termux checks) is expected and correct.
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.resolve()
ANDROID_BASE = "/storage/emulated/0"
TERMUX_HOME = "/data/data/com.termux"
TERMUX_SHEBANG = "#!/data/data/com.termux"

# Patterns that are LEGITIMATE in Python (platform detection)
LEGITIMATE_PATTERNS = [
    "'com.termux' in os.getcwd()",  # Platform detection
    "os.path.exists('/data/data/com.termux",  # Platform detection
]

issues = []
warnings = []

for ext in ("*.py", "*.sh", "*.yaml", "*.yml", "*.json"):
    for f in REPO_ROOT.rglob(ext):
        if "__pycache__" in str(f) or ".git" in str(f) or f.name == "fix_android_paths.py":
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except:
            continue

        lines = content.split('\n')
        file_issues = []

        for i, line in enumerate(lines, 1):
            # Skip empty/comment-only lines
            stripped = line.strip()
            if not stripped or stripped.startswith('#') and 'shebang' not in stripped.lower():
                # Check if it's a shebang line
                if not stripped.startswith('#!'):
                    continue

            # Check for Android paths
            if ANDROID_BASE in line:
                # Is this a legitimate platform detection?
                if any(p in line for p in LEGITIMATE_PATTERNS):
                    continue
                # Is this in a comment? (rough check)
                if stripped.startswith('#') or stripped.startswith('//'):
                    continue
                file_issues.append(f"  L{i}: {line.strip()[:100]}")

            # Check for Termux shebangs
            if stripped.startswith(TERMUX_SHEBANG):
                file_issues.append(f"  L{i} (shebang): {line.strip()}")

            # Check for Termux sys.path
            if f"sys.path" in line and TERMUX_HOME in line and "os.path.exists" not in line:
                file_issues.append(f"  L{i}: {line.strip()[:100]}")

        if file_issues:
            rel = f.relative_to(REPO_ROOT)
            issues.append((rel, file_issues))

# Report
if not issues:
    print("ALL CLEAR: No actionable Android/Termux paths remaining in executable code.")
    print("Platform detection code in server.py and mfker_server.py is correct.")
    sys.exit(0)
else:
    print(f"REMAINING ISSUES: {len(issues)} files\n")
    for path, file_issues in sorted(issues):
        print(f"  {path}:")
        for issue in file_issues:
            print(f"    {issue}")
        print()
    sys.exit(1)
