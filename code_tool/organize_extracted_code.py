#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: glob, os, pathlib, re
# ROLE: Scans the OUTPUT_ROOT for extracted code files and moves them
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

# FILENAME: organize_extracted_code.py
# FILE PATH: /home/bleaknarratives/Code-City-Apocalypse/code_tool/organize_extracted_code.py

import os
import re
import glob
from pathlib import Path

# --- Configuration ---
# Must match the output directory in your ChatExportExtractor class
OUTPUT_ROOT = Path("/home/bleaknarratives/Code-City-Apocalypse/code_tool/extracted_chat_code")
# Regex to find the language and original file name from the saved file name
# e.g., 'conversation_log_test_python.txt' -> groups: ('conversation_log_test', 'python')
# This assumes your naming convention is {base_name}_{lang}.txt
FILENAME_PATTERN = re.compile(r'(.+)_(python|javascript|typescript|bash)\.txt$', re.IGNORECASE)
# ---------------------

def organize_files():
    """
    Scans the OUTPUT_ROOT for extracted code files and moves them
    into language-specific subfolders.
    """
    if not OUTPUT_ROOT.exists():
        print(f"🛑 Error: Output directory not found at {OUTPUT_ROOT}")
        return

    print(f"📂 Starting organization in: {OUTPUT_ROOT}")
    
    # Use glob to find all .txt files directly in the root directory
    files_to_organize = glob.glob(str(OUTPUT_ROOT / "*.txt"))
    
    # Counter for feedback
    files_moved_count = 0
    
    for file_path_str in files_to_organize:
        current_file = Path(file_path_str)
        
        # Skip this file if it's already in a subdirectory (i.e., it has been organized)
        if current_file.parent != OUTPUT_ROOT:
            continue
        
        match = FILENAME_PATTERN.search(current_file.name)
        
        if match:
            # base_name is the conversation_log_test part
            # lang is the python/javascript/etc part
            base_name, lang = match.groups()
            
            # Create the destination folder (e.g., /.../extracted_chat_code/python/)
            destination_folder = OUTPUT_ROOT / lang.lower()
            destination_folder.mkdir(parents=True, exist_ok=True)
            
            # Define the new path for the file
            new_path = destination_folder / current_file.name
            
            try:
                # Move the file
                current_file.rename(new_path)
                print(f"✅ Moved: '{current_file.name}' to '{lang.lower()}/'")
                files_moved_count += 1
            except Exception as e:
                print(f"⚠️ Failed to move {current_file.name}: {e}")
        else:
            print(f"⏭️ Skipped: '{current_file.name}' (Name did not match pattern)")

    print(f"\n✨ Organization complete. {files_moved_count} files moved.")

if __name__ == "__main__":
    organize_files()
