import subprocess
import os

def debug_clipboard():
    print("🔍 CLIPBOARD DEBUGGER")
    result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
    raw = result.stdout
    print(f"Length: {len(raw)}")
    print("First 200:", raw[:200])

debug_clipboard()
