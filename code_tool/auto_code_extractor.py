#!/usr/bin/env python3
import os
import time
import json
from pathlib import Path
import hashlib

class AutoCodeExtractor:
    def __init__(self):
        self.watch_dirs = [
            "/home/bleaknarratives/Code-City-Apocalypse",
            "/home/bleaknarratives/Code-City-Apocalypse", 
            "/home/bleaknarratives/Code-City-Apocalypse/scripts"
        ]
        self.processed_files = set()
        self.code_extensions = {'.py', '.txt', '.js', '.html', '.css', '.md', '.json', '.xml', '.yaml', '.yml'}
        self.output_dir = "/home/bleaknarratives/Code-City-Apocalypse/code_tool/auto_extracted_code"
        
        # Create output structure
        Path(f"{self.output_dir}/code").mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/logs").mkdir(parents=True, exist_ok=True)
        
        self.load_processed_files()
    
    def load_processed_files(self):
        """Load already processed files to avoid duplicates"""
        log_file = f"{self.output_dir}/logs/processed_files.json"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.processed_files = set(json.load(f))
    
    def save_processed_files(self):
        """Save processed files list"""
        log_file = f"{self.output_dir}/logs/processed_files.json"
        with open(log_file, 'w') as f:
            json.dump(list(self.processed_files), f)
    
    def get_file_hash(self, file_path):
        """Generate file hash to detect changes"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def is_code_file(self, file_path):
        """Check if file is a code file"""
        ext = Path(file_path).suffix.lower()
        return ext in self.code_extensions
    
    def extract_new_files(self):
        """Find and extract new code files"""
        new_files = []
        
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
                
            for root, dirs, files in os.walk(watch_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    if self.is_code_file(file_path):
                        file_hash = self.get_file_hash(file_path)
                        file_id = f"{file_path}:{file_hash}"
                        
                        if file_id not in self.processed_files:
                            new_files.append(file_path)
                            self.processed_files.add(file_id)
        
        return new_files
    
    def copy_code_file(self, file_path):
        """Copy code file to organized structure"""
        try:
            filename = Path(file_path).name
            timestamp = int(time.time())
            dest_path = f"{self.output_dir}/code/{timestamp}_{filename}"
            
            # Handle duplicate names
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                dest_path = f"{self.output_dir}/code/{timestamp}_{name}_{counter}{ext}"
                counter += 1
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as src:
                content = src.read()
            
            with open(dest_path, 'w', encoding='utf-8') as dest:
                dest.write(f"# Source: {file_path}\n")
                dest.write(f"# Extracted: {time.ctime()}\n")
                dest.write("#" * 50 + "\n\n")
                dest.write(content)
            
            return dest_path
        except Exception as e:
            print(f"Error copying {file_path}: {e}")
            return None
    
    def run(self):
        """Main monitoring loop"""
        print("🤖 Auto Code Extractor Started...")
        print(f"📁 Watching: {', '.join(self.watch_dirs)}")
        print(f"📂 Output: {self.output_dir}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                new_files = self.extract_new_files()
                
                if new_files:
                    print(f"📥 Found {len(new_files)} new code files")
                    
                    for file_path in new_files:
                        dest_path = self.copy_code_file(file_path)
                        if dest_path:
                            print(f"✅ Extracted: {Path(file_path).name}")
                    
                    self.save_processed_files()
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Auto Code Extractor Stopped")
            self.save_processed_files()

if __name__ == "__main__":
    extractor = AutoCodeExtractor()
    extractor.run()
