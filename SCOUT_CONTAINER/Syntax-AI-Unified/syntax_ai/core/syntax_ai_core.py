import logging

#!/usr/bin/env python3
import re
import subprocess
import os
import json
import tempfile
from pathlib import Path

logging.info("🤖 SYNTAX AI CORE - TEST VERSION")
logging.info("=" * 50)

# Simple test to prove it works
test_commands = [
    "echo 'Syntax AI is ALIVE!'",
    "mkdir -p /storage/emulated/0/syntax_test",
    "cd /storage/emulated/0/syntax_test && echo 'Test file' > test.txt",
    "ls -la /storage/emulated/0/syntax_test/"
]

logging.info("🚀 Executing test commands...")
for i, cmd in enumerate(test_commands):
    logging.info(f"Command {i+1}: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    logging.info(f"Output: {result.stdout}")
    if result.stderr:
        logging.info(f"Error: {result.stderr}")
    logging.info("-" * 30)

logging.info("🎉 SYNTAX AI TEST COMPLETE!")
logging.info("📁 Check: /storage/emulated/0/syntax_test/")
