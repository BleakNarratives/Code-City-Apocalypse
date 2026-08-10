#!/usr/bin/env python3
import subprocess
import re
from pathlib import Path
from datetime import datetime

def extract_code(text):
    # MULTIPLE extraction methods
    methods = [
        r'```(?:\w+)?\s*([^`]*)```',  # Method 1
        r'```(.*?)```',               # Method 2  
        r'``(.*?)``',                 # Method 3
    ]
    
    for pattern in methods:
        blocks = re.findall(pattern, text, re.DOTALL)
        blocks = [b.strip() for b in blocks if b.strip()]
        if blocks:
            return blocks
    return []

def main():
    print("🎯 WORKING EXTRACTOR")
    print("=" * 40)
    
    try:
        result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
        text = result.stdout
        
        if not text.strip():
            print("❌ Clipboard empty! Copy AI conversation first.")
            return
        
        print(f"📋 Found: {len(text)} characters")
        
        blocks = extract_code(text)
        
        if not blocks:
            print("❌ STILL NO CODE FOUND!")
            print("Debug: Showing first 200 chars of clipboard:")
            print(text[:200])
            return
        
        print(f"📦 FOUND {len(blocks)} CODE BLOCKS!")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = Path("/storage/emulated/0/code_tool/extracted_projects") / f"project_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        for i, code in enumerate(blocks):
            filename = f"code_{i+1}.txt"
            filepath = project_dir / filename
            with open(filepath, 'w') as f:
                f.write("EXTRACTED CODE:\n" + "="*40 + "\n")
                f.write(code)
            print(f"💾 {filename}")
        
        print(f"✅ SAVED TO: {project_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
