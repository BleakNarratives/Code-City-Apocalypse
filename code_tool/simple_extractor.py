
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: re, subprocess
# ROLE: extract_code function module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

import subprocess
import re

def extract_code():
    print("🔍 SIMPLE CODE EXTRACTOR")
    print("=" * 40)
    
    try:
        result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
        clipboard_content = result.stdout
        
        if not clipboard_content.strip():
            print("❌ Clipboard is empty!")
            return
            
        print(f"📋 Clipboard size: {len(clipboard_content)} characters")
        
        code_blocks = re.findall(r'```(.*?)```', clipboard_content, re.DOTALL)
        
        if not code_blocks:
            print("❌ No code blocks found")
            return
            
        print(f"🎯 Found {len(code_blocks)} code block(s)!")
        
        for i, block in enumerate(code_blocks):
            code = block.strip()
            if code.startswith('python'):
                code = code[6:].strip()
                
            filename = f"extracted_code_{i+1}.py"
            with open(filename, 'w') as f:
                f.write(code)
                
            print(f"💾 Saved: {filename}")
            
        print("✅ Extraction complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    extract_code()
