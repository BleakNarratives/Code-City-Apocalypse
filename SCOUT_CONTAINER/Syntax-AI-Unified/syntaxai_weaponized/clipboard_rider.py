import logging

# Run this in Pydroid3 Python console (NOT terminal)
import os
import subprocess

# Create the file using pure Python - NO HEREDOC!
rider_code = '''import time
import os
import subprocess
import re
from datetime import datetime

def get_clipboard():
    try:
        result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ""

def main():
    logging.info("🚗 RIDER STARTED - Monitoring clipboard...")
    last = ""
    while True:
        current = get_clipboard()
        if current and current != last:
            logging.info(f"📝 Captured: {len(current)} chars")
            last = current
        time.sleep(3)

if __name__ == "__main__":
    main()
'''

# Save directly to file
with open("/storage/emulated/0/syntaxai-weaponized/clipboard_rider.py", "w") as f:
    f.write(rider_code)

logging.info("✅ File saved via Python!")