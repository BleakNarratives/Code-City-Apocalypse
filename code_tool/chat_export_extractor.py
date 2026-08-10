#!/usr/bin/env python3
# FILENAME: chat_export_extractor.py
# FILE PATH: /storage/emulated/0/scripts/chat_export_extractor.py

import re
import os
from pathlib import Path
import glob

class ChatExportExtractor:
    """
    Extracts code blocks of specific languages from a text string 
    (like a chat log) and saves them into separate files.
    """
    def __init__(self):
        # This is the directory where extracted code blocks will be saved
        # Must match the folder used by the organizer script
        self.output_dir = "/storage/emulated/0/extracted_chat_code"
        # Ensure the output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # Define regular expressions for different code block types
        # re.DOTALL ensures that '.' also matches newline characters.
        self.code_patterns = {
            'python': r'```python(.*?)```',
            'javascript': r'```javascript(.*?)```',
            'typescript': r'```typescript(.*?)```',
            'bash': r'```bash(.*?)```',
        }

    def extract_code_blocks(self, text):
        """Finds all code blocks matching the defined patterns."""
        extracted = {}
        for lang, pattern in self.code_patterns.items():
            # re.DOTALL is crucial for matching multi-line code blocks
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                extracted[lang] = matches
        return extracted

    def save_code_blocks(self, extracted, base_name):
        """Saves extracted blocks into files named {base_name}_{lang}.txt"""
        for lang, blocks in extracted.items():
            # Files are saved directly in the root output dir for the organizer script to find
            file_path = os.path.join(self.output_dir, f"{base_name}_{lang}.txt")
            with open(file_path, 'w') as f:
                for i, block in enumerate(blocks):
                    f.write(f"--- Code Block {i+1} ({lang}) ---\n")
                    f.write(block.strip())
                    f.write("\n\n")
            print(f"📦 Saved {len(blocks)} {lang} block(s) to: {file_path}")

if __name__ == "__main__":
    extractor = ChatExportExtractor()
    
    # Simple test text (replace this with your actual chat log input method later)
    sample_text = """
    Here's some Python code:
    ```python
    def hello():
        print("Hello, world!")
    ```

    And some TypeScript for the UI:
    ```typescript
    const VibeVault = () => {
        // AI driven input processing
        return <input type="text" placeholder="Enter your vibe-and-intent" />; 
    };
    ```
    And a Bash script:
    ```bash
    # Run the DAWG scheduler
    ./dawg_scheduler.sh start
    ```
    """
    
    # Base name for the output files
    output_base_name = "conversation_log_test" 
    
    extracted = extractor.extract_code_blocks(sample_text)
    extractor.save_code_blocks(extracted, output_base_name)
    print("\n✅ Extraction complete. Run the organizer script next.")

