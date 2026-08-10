# FILE: /storage/emulated/0/code_tool/ultra_extractor.py
# RUN: cd /storage/emulated/0/code_tool && python3 ultra_extractor.py

import re
import os
import json
from pathlib import Path
from datetime import datetime

class UltraExtractor:
    def __init__(self):
        self.base_dir = Path("/storage/emulated/0/code_tool")
        self.projects_dir = self.base_dir / "organized_projects"
        self.projects_dir.mkdir(exist_ok=True)
    
    def extract_and_organize(self, text, project_name=None):
        """The extractor that actually organizes your code"""
        print("🧠 ULTRA EXTRACTOR - Cognitive Bypass Activated")
        
        if not project_name:
            project_name = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        project_path = self.projects_dir / project_name
        project_path.mkdir(exist_ok=True)
        
        # Extract code blocks
        blocks = re.findall(r'```(?:(\w+)\n)?(.*?)```', text, re.DOTALL)
        
        print(f"📦 Found {len(blocks)} code blocks")
        
        # Organize intelligently
        for i, (lang, code) in enumerate(blocks):
            file_info = self.analyze_code_block(code, lang, i, text)
            self.save_organized_file(project_path, file_info, code)
        
        # Generate project map
        self.generate_project_map(project_path, blocks)
        
        print(f"✅ Project organized: {project_path}")
        return project_path
    
    def analyze_code_block(self, code, lang, index, full_text):
        """Figure out what this code actually is"""
        code_lower = code.lower()
        
        # Auto-detect purpose
        if 'def test_' in code_lower or 'assert ' in code_lower:
            file_type = 'test'
            folder = 'tests'
            name = f"test_{index}.py"
        elif 'def ' in code_lower and 'import ' in code_lower:
            file_type = 'module' 
            folder = 'src'
            name = f"module_{index}.py"
        elif 'function ' in code_lower and 'console.log' in code_lower:
            file_type = 'javascript'
            folder = 'src'
            name = f"app_{index}.js"
        else:
            file_type = 'utility'
            folder = 'utils'
            name = f"util_{index}.py"
        
        return {
            'filename': name,
            'folder': folder,
            'type': file_type,
            'language': lang or 'auto'
        }
    
    def save_organized_file(self, project_path, file_info, code):
        """Save file in proper location"""
        folder_path = project_path / file_info['folder']
        folder_path.mkdir(exist_ok=True)
        
        file_path = folder_path / file_info['filename']
        with open(file_path, 'w') as f:
            f.write(code.strip())
        
        print(f"   📄 {file_info['folder']}/{file_info['filename']} ({file_info['type']})")
    
    def generate_project_map(self, project_path, blocks):
        """Create a map so you remember what everything is"""
        map_data