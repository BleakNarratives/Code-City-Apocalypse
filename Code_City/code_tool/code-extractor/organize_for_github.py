#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: os, re, shutil
# ROLE: categorize_file function module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

import os
import shutil
import re

source_dir = "./extracted_code"
target_dir = "./github_ready"

categories = {
    'agents': ['agent', 'twoie', 'wole'],
    'web': ['.html', '.css', '.js'],
    'frameworks': ['framework', 'modmind', 'knose'],
    'docs': ['.md', '.txt']
}

def categorize_file(filename):
    filename_lower = filename.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    return 'misc'

# Create category directories
for category in list(categories.keys()) + ['misc']:
    os.makedirs(os.path.join(target_dir, category), exist_ok=True)

# Organize files
for filename in os.listdir(source_dir):
    if filename == "extraction_report.json":
        continue
        
    file_path = os.path.join(source_dir, filename)
    if os.path.isfile(file_path):
        category = categorize_file(filename)
        dest_path = os.path.join(target_dir, category, filename)
        shutil.copy2(file_path, dest_path)
        print(f"📁 {filename} → {category}/")

print("\n🎉 Organization complete!")
