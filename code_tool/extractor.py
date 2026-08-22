# Save this as extractor.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: sys
# ROLE: extractor
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

import sys

text = sys.stdin.read()
in_block = False
current_block = []

for line in text.split('\n'):
    if '```' in line:
        if in_block:
            print('=== CODE BLOCK ===')
            print('\n'.join(current_block))
            current_block = []
        in_block = not in_block
    elif in_block:
        current_block.append(line)