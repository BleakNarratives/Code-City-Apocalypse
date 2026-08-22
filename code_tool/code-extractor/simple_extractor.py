#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: json, os, shutil
# ROLE: simple extractor
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

import os
import shutil
import json

print("🚀 Starting Simple Code Extractor...")

# Just count files for now to test
try:
    with open("./logs/targeted_code_files.txt", "r") as f:
        files = [line.strip() for line in f if line.strip()]
    print(f"📁 Found {len(files)} files")
    print("First few files:")
    for i, file_path in enumerate(files[:5]):
        print(f"  {i+1}. {file_path}")
except Exception as e:
    print(f"❌ Error: {e}")
