
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: glob, logging, os
# ROLE: check results
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: File (1)
# [/DNA_TAG]

import logging

import os
import glob

logging.info("📊 Checking agent results...")
for file in glob.glob("comms/*_result.txt"):
    with open(file, 'r') as f:
        content = f.read()
    agent = os.path.basename(file).replace("_result.txt", "")
    logging.info(f"🤖 {agent}: {content}")
