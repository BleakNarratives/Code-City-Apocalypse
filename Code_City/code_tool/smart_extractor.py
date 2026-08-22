#!/usr/bin/env python3
import subprocess
import re
from pathlib import Path
from datetime import datetime

def is_self_reference(text):
    self_refs = ["widget_extractor", "smart_extractor", "Extract_Code", "termux-clipboard-get"]
    return any(ref in text for ref in self_refs)

def main():
    print("🎯 SMART EXTRACTOR")
    print("=" * 40)
    
    try:
        result = subprocess.run(["termux-clipboard-get"], capture_output=True, text=True)
        text = result.stdout
        
        if not text.strip():
            print("❌ Clipboard empty!")
            return
        
        if is_self_reference(text):
            print("🤖 Detected widget commands - ignoring")
            print("💡 Copy an AI conversation instead")
            return
        
        # Look for code patterns
        if '```' not in text:
            print("❌ No code blocks (```) found!")
            return
        
        blocks = re.findall(r'```(?:\\w+)?\\\\s*([^`]*)```', text, re.DOTALL)
        blocks = [b.strip() for b in blocks if b.strip()]
        
        if not blocks:
            print("❌ Couldn't extract code from blocks")
            return
        
        print(f"📦 Found {len(blocks)} code blocks!")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = Path("/home/bleaknarratives/Code-City-Apocalypse/code_tool/extracted_projects") / f"project_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)
        
        for i, code in enumerate(blocks):
            filename = f"code_{i+1}.txt"
            filepath = project_dir / filename
            with open(filepath, 'w') as f:
                f.write(code)
            print(f"💾 {filename}")
        
        print(f"✅ Saved to: {project_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
