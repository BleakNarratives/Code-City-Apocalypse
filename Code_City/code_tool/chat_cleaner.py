#!/usr/bin/env python3
import re
import os
import glob
from pathlib import Path

class ChatCleaner:
    def __init__(self):
        self.output_dir = "/home/bleaknarratives/Code-City-Apocalypse/code_tool/cleaned_chats"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # Patterns to identify and remove code blocks
        self.code_patterns = [
            r'```[\s\S]*?```',  # ```code blocks```
            r'`[^`]*`',         # `inline code`
            r'(\b(def|class|import|from|if|for|while|return)\b.*\n)+',  # Python code lines
            r'(<[^>]*>[\s\S]*?</[^>]*>)',  # HTML tags with content
            r'(\{[^}]*\})',     # JSON objects
            r'(\([^)]*\))',     # Function calls
        ]
        
        # Keep these contextual code mentions
        self.keep_patterns = [
            r'file.*\.py',
            r'function.*\(',
            r'we.*(need|should|will).*code',
            r'let.*(create|write).*script'
        ]
    
    def clean_chat_content(self, content):
        """Remove code blocks but keep contextual mentions"""
        original_content = content
        
        # First, remove all code blocks
        for pattern in self.code_patterns:
            content = re.sub(pattern, '', content)
        
        # Then restore contextual mentions that might have been removed
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Keep lines that discuss code but don't contain actual code blocks
            has_context = any(re.search(pattern, line, re.IGNORECASE) for pattern in self.keep_patterns)
            is_short = len(line) < 100
            has_no_brackets = not any(char in line for char in ['{', '}', '[', ']', '()`'])
            
            if has_context and is_short and has_no_brackets:
                cleaned_lines.append(line)
            elif not any(char in line for char in ['{', '}', '[', ']', '=`']):
                # Only keep non-code lines
                code_indicators = ['def ', 'class ', 'import ', 'from ', 'return ', ' = ', ' == ', ' != ']
                if not any(indicator in line for indicator in code_indicators):
                    cleaned_lines.append(line)
        
        # Remove duplicate empty lines
        cleaned_content = '\n'.join(cleaned_lines)
        cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
        
        return cleaned_content.strip()
    
    def find_chat_files(self):
        """Find potential chat log files"""
        chat_locations = [
            "/home/bleaknarratives/Code-City-Apocalypse/*.txt",
            "/home/bleaknarratives/Code-City-Apocalypse/*.txt", 
            "/home/bleaknarratives/Code-City-Apocalypse/*.log",
            "/home/bleaknarratives/Code-City-Apocalypse/scripts/*.txt"
        ]
        
        chat_files = []
        for location in chat_locations:
            chat_files.extend(glob.glob(location))
        
        return chat_files
    
    def clean_file(self, file_path):
        """Clean a single chat file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            cleaned = self.clean_chat_content(content)
            
            if cleaned:
                filename = Path(file_path).stem
                output_path = f"{self.output_dir}/{filename}_cleaned.txt"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"Cleaned chat from: {file_path}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(cleaned)
                
                return output_path
            return None
            
        except Exception as e:
            print(f"Error cleaning {file_path}: {e}")
            return None
    
    def clean_all_chats(self):
        """Clean all found chat files"""
        chat_files = self.find_chat_files()
        
        if not chat_files:
            print("📭 No chat files found in common locations")
            return
        
        print(f"📁 Found {len(chat_files)} potential chat files")
        
        cleaned_count = 0
        for file_path in chat_files:
            result = self.clean_file(file_path)
            if result:
                print(f"✅ Cleaned: {Path(file_path).name}")
                cleaned_count += 1
            else:
                print(f"❌ No content: {Path(file_path).name}")
        
        print(f"\n🎉 Cleaned {cleaned_count} chat files")
        print(f"📂 Output: {self.output_dir}/")

if __name__ == "__main__":
    cleaner = ChatCleaner()
    cleaner.clean_all_chats()
