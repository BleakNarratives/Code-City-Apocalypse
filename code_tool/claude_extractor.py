#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: re, subprocess
# ROLE: main function module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

import subprocess
import re

def main():
    print("🎯 CLAUDE EXTRACTOR")
    print("=" * 40)
    
    try:
        result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
        text = result.stdout
        
        if not text.strip():
            print("❌ Clipboard empty!")
            return
        
        # SIMPLE EXTRACTION - just grab everything between ```
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        blocks = [b.strip() for b in blocks if b.strip()]
        
        if not blocks:
            print("❌ No ``` code blocks found!")
            print("TEXT PREVIEW:")
            print(text[:300])
            return
        
        print(f"📦 Found {len(blocks)} code blocks!")
        
        for i, code in enumerate(blocks):
            filename = f"claude_block_{i+1}.txt"
            with open(filename, 'w') as f:
                f.write(code)
            print(f"💾 {filename}")
            print(f"First line: {code.split(chr(10))[0][:50]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
