#!/usr/bin/env python3
"""
Fixed Chat Export Code Extractor v2
- Proper file extensions
- Language-specific folders
- Retroactive file fixing
"""

import re
import os
import hashlib
from pathlib import Path
from datetime import datetime

class ChatExportExtractor:
    def __init__(self, output_base="/home/bleaknarratives/Code-City-Apocalypse/code_tool/extracted_chat_code"):
        self.output_base = Path(output_base)
        self.output_base.mkdir(parents=True, exist_ok=True)
        
        # Proper extension mapping
        self.ext_map = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'tsx': 'tsx',
            'jsx': 'jsx',
            'html': 'html',
            'css': 'css',
            'bash': 'sh',
            'shell': 'sh',
            'sh': 'sh',
            'json': 'json',
            'yaml': 'yaml',
            'yml': 'yml',
            'sql': 'sql',
            'rust': 'rs',
            'go': 'go',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'markdown': 'md',
            'md': 'md',
            'xml': 'xml',
            'dockerfile': 'Dockerfile',
            'proto': 'proto',
            'toml': 'toml',
            'ini': 'ini',
            'env': 'env',
            'unknown': 'txt'
        }
        
        # Code block pattern
        self.code_pattern = r'```(\w+)?\s*\n(.*?)```'
    
    def extract_from_clipboard(self, content: str) -> dict:
        """Extract code blocks with proper language detection"""
        extracted = {}
        
        for match in re.finditer(self.code_pattern, content, re.DOTALL):
            lang = (match.group(1) or 'unknown').lower()
            code = match.group(2).strip()
            
            if not code:
                continue
            
            if lang not in extracted:
                extracted[lang] = []
            
            extracted[lang].append({
                'code': code,
                'hash': hashlib.sha256(code.encode()).hexdigest()[:8]
            })
        
        return extracted
    
    def save_code(self, lang: str, code_blocks: list):
        """Save code blocks with proper extensions and folders"""
        # Create language-specific folder
        lang_folder = self.output_base / lang
        lang_folder.mkdir(parents=True, exist_ok=True)
        
        # Get proper extension
        ext = self.ext_map.get(lang, 'txt')
        
        saved_files = []
        for i, block in enumerate(code_blocks):
            code = block['code']
            code_hash = block['hash']
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{lang}_{timestamp}_{code_hash}.{ext}"
            filepath = lang_folder / filename
            
            # Save file
            with open(filepath, 'w') as f:
                f.write(code)
            
            saved_files.append(str(filepath))
            print(f"✅ Saved: {filepath}")
        
        return saved_files
    
    def retroactive_fix(self):
        """Fix existing extracted files with wrong extensions"""
        print("🔧 Starting retroactive fix...")
        fixed_count = 0
        
        for file_path in self.output_base.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip if already has correct extension
            if file_path.suffix in [f".{ext}" for ext in self.ext_map.values()]:
                continue
            
            # Try to detect language from content
            try:
                content = file_path.read_text()
                detected_lang = self._detect_language(content)
                
                if detected_lang and detected_lang != 'unknown':
                    # Create proper folder and filename
                    lang_folder = self.output_base / detected_lang
                    lang_folder.mkdir(parents=True, exist_ok=True)
                    
                    ext = self.ext_map[detected_lang]
                    new_filename = file_path.stem + f".{ext}"
                    new_path = lang_folder / new_filename
                    
                    # Move and rename
                    file_path.rename(new_path)
                    fixed_count += 1
                    print(f"🔄 Fixed: {file_path.name} → {new_path}")
            
            except Exception as e:
                print(f"⚠️  Error fixing {file_path}: {e}")
        
        print(f"✅ Fixed {fixed_count} files")
    
    def _detect_language(self, content: str) -> str:
        """Detect language from code content"""
        # Simple heuristic detection
        if 'import ' in content and ('def ' in content or 'class ' in content):
            return 'python'
        elif 'function' in content or 'const ' in content or '=>' in content:
            return 'javascript'
        elif '<html' in content or '<div' in content:
            return 'html'
        elif 'SELECT ' in content or 'INSERT INTO' in content:
            return 'sql'
        elif '#!/bin/bash' in content or '#!/bin/sh' in content:
            return 'bash'
        else:
            return 'unknown'
    
    def process_clipboard(self):
        """Main processing function"""
        try:
            # Get clipboard content (Termux)
            import subprocess
            result = subprocess.run(['termux-clipboard-get'], 
                                  capture_output=True, text=True)
            content = result.stdout
            
            if not content:
                print("❌ Clipboard is empty")
                return
            
            # Extract code blocks
            extracted = self.extract_from_clipboard(content)
            
            if not extracted:
                print("❌ No code blocks found")
                return
            
            # Save all extracted code
            total_saved = 0
            for lang, blocks in extracted.items():
                saved = self.save_code(lang, blocks)
                total_saved += len(saved)
                print(f"📁 {lang}: {len(saved)} files")
            
            print(f"\n✅ Total: {total_saved} code blocks extracted")
        
        except Exception as e:
            print(f"💥 Error: {e}")

# CLI Interface
if __name__ == "__main__":
    import sys
    
    extractor = ChatExportExtractor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--fix':
            extractor.retroactive_fix()
        elif sys.argv[1] == '--help':
            print("""
Usage:
  python chat_export_extractor_v2.py          # Extract from clipboard
  python chat_export_extractor_v2.py --fix    # Fix existing files
  python chat_export_extractor_v2.py --help   # Show this help
            """)
        else:
            print("❌ Unknown command. Use --help")
    else:
        extractor.process_clipboard()