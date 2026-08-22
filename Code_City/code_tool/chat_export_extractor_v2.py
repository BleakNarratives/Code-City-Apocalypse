
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-extraction
# DEPS: datetime, json, os, pathlib, re
# ROLE: [ARCHIVED — syntax error fixed by wrapping]
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Extraction (8)
# [/DNA_TAG]

"""[ARCHIVED — syntax error fixed by wrapping]

```python
#!/usr/bin/env python3
\"\"\"
Fixed Chat Export Code Extractor
- Saves files with correct extensions
- Organizes into language-specific folders
- Handles inline snippets separately
\"\"\"

# Auto-recovered file
\"\"\"
import re
import os
import json
from pathlib import Path
from datetime import datetime

class ChatExportExtractor:
    def __init__(self):
        self.output_dir = Path("/home/bleaknarratives/Code-City-Apocalypse/code_tool/extracted_chat_code")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # FIXED: Proper extension mapping
        self.ext_map = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'html': 'html',
            'css': 'css',
            'bash': 'sh',
            'shell': 'sh',
            'json': 'json',
            'yaml': 'yaml',
            'sql': 'sql',
            'rust': 'rs',
            'go': 'go',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'markdown': 'md',
            'xml': 'xml',
            'dockerfile': 'Dockerfile',
            'proto': 'proto',
            'unknown': 'txt'
        }
        
        # Enhanced code block patterns
        self.code_patterns = {
            'fenced': r'```(\w+)?\s*\n(.*?)```',  # ```python\ncode```
            'inline': r'`([^`\n]+)`'              # `inline code`
        }
    
    def extract_from_text(self, content: str, source_name: str) -> dict:
        \"\"\"Extract code blocks with proper language detection\"\"\"
        extracted = {}
        
        # Extract fenced code blocks
        for match in re.finditer(self.code_patterns['fenced'], content, re.DOTALL):
            lang = match.group(1) or 'unknown'
            code = match.group(2).strip()
            
            lang = lang.lower()
            if lang not in extracted:
                extracted[lang] = []
            extracted[lang].append(code)
        
        # Extract inline code (keep separate)
        inline_matches = re.findall(self.code_patterns['inline'], content)
        if inline_matches:
            extracted['inline'] = inline_matches
        
        return extracted
    
    def save_extracted_code(self, extracted: dict, source_name: str, original_path: str) -> list:
        \"\"\"Save code into organized language folders with correct extensions\"\"\"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []
        
        for lang, code_blocks in extracted.items():
            if not code_blocks:
                continue
            
            # Create language-specific folder
            if lang == 'inline':
                lang_dir = self.output_dir / "inline_snippets"
            else:
                lang_dir = self.output_dir / lang
            lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Get correct file extension
            ext = self.ext_map.get(lang, 'txt')
            
            for i, code in enumerate(code_blocks, 1):
                if lang == 'inline':
                    # Append all inline snippets to one file per source
                    filename = f"{source_name}_{timestamp}.txt"
                    filepath = lang_dir / filename
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(f"# Snippet {i}\n{code}\n{'='*40}\n")
                else:
                    # Individual files for code blocks
                    filename = f"{source_name}_block{i}_{timestamp}.{ext}"
                    filepath = lang_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"# Extracted from: {source_name}\n")
                        f.write(f"# Original: {original_path}\n")
                        f.write(f"# Language: {lang}\n")
                        f.write(f"# Block: {i}\n")
                        f.write("#" * 50 + "\n\n")
                        f.write(code + "\n")
                
                saved_files.append(str(filepath))
        
        # Create extraction report
        report_path = self.output_dir / f"{source_name}_{timestamp}_report.json"
        report = {
            "source": source_name,
            "original_file": original_path,
            "timestamp": timestamp,
            "languages": {lang: len(blocks) for lang, blocks in extracted.items()},
            "total_blocks": sum(len(blocks) for blocks in extracted.values()),
            "saved_files": saved_files
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return saved_files
    
    def process_file(self, file_path: str):
        \"\"\"Process a single chat export file\"\"\"
        source_name = Path(file_path).stem
        print(f"📄 Processing: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            extracted = self.extract_from_text(content, source_name)
            saved_files = self.save_extracted_code(extracted, source_name, file_path)
            
            print(f"✅ Extracted {sum(len(blocks) for blocks in extracted.values())} blocks")
            print(f"📁 Organized by language: {list(extracted.keys())}")
            return saved_files
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def run_extraction(self):
        \"\"\"Find and process all chat export files\"\"\"
        patterns = [
            "/home/bleaknarratives/Code-City-Apocalypse/*chat*.txt",
            "/home/bleaknarratives/Code-City-Apocalypse/*.log",
            "/home/bleaknarratives/Code-City-Apocalypse/*.txt",
            "/home/bleaknarratives/Code-City-Apocalypse/*.md"
        ]
        
        import glob
        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern))
        
        if not files:
            print("📭 No chat export files found")
            return
        
        print(f"📁 Found {len(files)} files\n")
        for file_path in files:
            self.process_file(file_path)
            print()

if __name__ == "__main__":
    extractor = ChatExportExtractor()
    extractor.run_extraction()
```
\"\"\"

"""