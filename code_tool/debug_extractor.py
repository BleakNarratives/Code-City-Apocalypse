
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: os, subprocess
# ROLE: debug_clipboard function module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

import subprocess
import os

def debug_clipboard():
    print("🔍 CLIPBOARD DEBUGGER")
    result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
    raw = result.stdout
    print(f"Length: {len(raw)}")
    print("First 200:", raw[:200])

debug_clipboard()
