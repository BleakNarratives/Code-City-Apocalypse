import logging

#!/usr/bin/env python3
"""
SMART CODE EXTRACTOR v2.0
- Extracts code from conversations
- Analyzes context for proper placement
- Compiles into organized project structures
- Generates execution instructions
"""
import re
import os
import ast
import hashlib
import json
from pathlib import Path
from datetime import datetime

class SmartCodeExtractor:
    def __init__(self, base_export_path="/storage/emulated/0/syntaxai_weaponized/exports"):
        self.base_export_path = Path(base_export_path)
        self.code_blocks = []
        self.context_analyzer = ContextAnalyzer()
        self.project_organizer = ProjectOrganizer()
        
    def extract_complete_project(self, conversation_text, project_name=None):
        """
        Main extraction pipeline - turns conversation into working project
        """
        logging.info("🔍 SMART EXTRACTOR v2.0 - Analyzing conversation...")
        
        # Generate project name if not provided
        if not project_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project_name = f"project_{timestamp}"
        
        # Create project directory
        project_path = self.base_export_path / "extracted_projects" / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Extract code with context
        logging.info("📝 Extracting code blocks with context...")
        enhanced_blocks = self.extract_with_context(conversation_text)
        
        # Organize into project structure
        logging.info("🏗️  Organizing project structure...")
        project_structure = self.organize_into_project(enhanced_blocks)
        
        # Write files
        logging.info("💾 Writing project files...")
        self.write_project_files(project_structure, project_path)
        
        # Generate project metadata
        logging.info("📊 Generating project documentation...")
        self.generate_project_metadata(enhanced_blocks, project_path)
        
        logging.info(f"✅ Project extracted to: {project_path}")
        return project_path
    
    def extract_with_context(self, text):
        """Extract code with intelligent context analysis"""
        sections = self._split_conversation_sections(text)
        enhanced_blocks = []
        
        for i, section in enumerate(sections):
            context = self.context_analyzer.analyze_section(section, i)
            code_blocks = self._extract_code_blocks(section)
            
            for block in code_blocks:
                enhanced_block = self._enhance_block_with_context(block, context)
                enhanced_blocks.append(enhanced_block)
        
        return enhanced_blocks
    
    def _extract_code_blocks(self, text):
        """Extract code blocks from text with language detection"""
        code_blocks = []
        
        # Pattern for code blocks with language specification
        pattern = r'```(\w+)?\s*(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        for lang, code in matches:
            if not lang:
                lang = self._detect_language(code)
            
            code_blocks.append({
                'content': code.strip(),
                'language': lang.lower(),
                'raw_content': code
            })
        
        return code_blocks
    
    def _detect_language(self, code):
        """Detect programming language from code content"""
        code_lower = code.lower()
        
        if 'def ' in code_lower and 'import ' in code_lower:
            return 'python'
        elif 'function ' in code_lower and ('const ' in code_lower or 'let ' in code_lower):
            return 'javascript'
        elif '<?php' in code_lower or '$' in code_lower:
            return 'php'
        elif '<html' in code_lower or '<div' in code_lower:
            return 'html'
        elif '#!/bin/bash' in code_lower or 'sudo ' in code_lower:
            return 'bash'
        else:
            return 'unknown'
    
    def _enhance_block_with_context(self, code_block, context):
        """Add execution context and metadata to code block"""
        return {
            'code_id': self._generate_code_id(code_block['content']),
            'content': code_block['content'],
            'language': code_block['language'],
            'filename_suggestion': self._suggest_filename(code_block, context),
            'execution_context': context.get('purpose', 'utility'),
            'dependencies': self._detect_dependencies(code_block['content'], code_block['language']),
            'required_imports': self._extract_imports(code_block['content'], code_block['language']),
            'usage_instructions': context.get('instructions', ''),
            'tests_suggested': self._suggest_tests(code_block, context),
            'section_context': context.get('section_purpose', '')
        }
    
    def _suggest_filename(self, code_block, context):
        """Intelligently suggest filenames based on content and context"""
        language_extensions = {
            'python': '.py',
            'javascript': '.js',
            'bash': '.sh',
            'html': '.html',
            'css': '.css',
            'json': '.json',
            'php': '.php',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'ruby': '.rb',
            'go': '.go'
        }
        
        extension = language_extensions.get(code_block['language'], '.txt')
        
        # Use context to determine filename
        if 'main' in context.get('purpose', '').lower() or 'entry' in context.get('section_purpose', '').lower():
            return f"main{extension}"
        elif 'test' in context.get('purpose', '').lower():
            return f"test_{context.get('primary_function', 'module')}{extension}"
        elif 'config' in context.get('purpose', '').lower():
            return f"config{extension}"
        else:
            # Extract function/class name for filename
            primary_element = self._extract_primary_element(code_block['content'], code_block['language'])
            if primary_element:
                return f"{primary_element}{extension}"
            else:
                return f"module_{self._generate_code_id(code_block['content'])[:8]}{extension}"
    
    def _extract_primary_element(self, code, language):
        """Extract primary function/class name from code"""
        if language == 'python':
            # Look for function or class definitions
            func_match = re.search(r'def\s+(\w+)', code)
            class_match = re.search(r'class\s+(\w+)', code)
            return (func_match or class_match).group(1) if func_match or class_match else None
        elif language == 'javascript':
            func_match = re.search(r'function\s+(\w+)', code)
            return func_match.group(1) if func_match else None
        return None
    
    def organize_into_project(self, enhanced_blocks):
        """Organize code blocks into proper project structure"""
        return self.project_organizer.organize(enhanced_blocks)
    
    def write_project_files(self, project_structure, project_path):
        """Write organized project structure to files"""
        for file_path, content in project_structure.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def generate_project_metadata(self, enhanced_blocks, project_path):
        """Generate README, requirements, and execution instructions"""
        # Generate README.md
        readme_content = self._generate_readme(enhanced_blocks)
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Generate requirements.txt for Python projects
        python_blocks = [b for b in enhanced_blocks if b['language'] == 'python']
        if python_blocks:
            requirements = self._extract_python_requirements(python_blocks)
            with open(project_path / "requirements.txt", 'w') as f:
                f.write('\n'.join(requirements))
        
        # Generate execution instructions
        instructions = self._generate_execution_instructions(enhanced_blocks)
        with open(project_path / "RUN_INSTRUCTIONS.txt", 'w') as f:
            f.write(instructions)
    
    def _generate_code_id(self, content):
        """Generate unique ID for code block"""
        return hashlib.md5(content.encode()).hexdigest()[:16]

class ContextAnalyzer:
    def analyze_section(self, text, section_index):
        """Analyze text surrounding code for context"""
        return {
            'purpose': self._extract_purpose(text),
            'instructions': self._extract_instructions(text),
            'section_purpose': self._determine_section_role(text, section_index),
            'primary_function': self._extract_primary_function(text)
        }
    
    def _extract_purpose(self, text):
        text_lower = text.lower()
        purpose_indicators = {
            'test': 'testing',
            'main function': 'entry_point',
            'configuration': 'config',
            'utility function': 'utility',
            'api endpoint': 'web_service',
            'database': 'data_persistence',
            'script': 'script',
            'example': 'example'
        }
        
        for indicator, purpose in purpose_indicators.items():
            if indicator in text_lower:
                return purpose
        return 'utility'

# Additional classes would be in separate files...
