import logging

import os
import glob

logging.info("📊 Checking agent results...")
for file in glob.glob("comms/*_result.txt"):
    with open(file, 'r') as f:
        content = f.read()
    agent = os.path.basename(file).replace("_result.txt", "")
    logging.info(f"🤖 {agent}: {content}")
