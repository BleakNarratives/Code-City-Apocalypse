# src/core/smart_extractor.py
import re
import os
import ast
import hashlib
from pathlib import Path

class SmartCodeExtractor:
    def __init__(self):
        self.code_blocks = []
        self.context_analyzer = ContextAnalyzer()
    
    def extract_with_context(self, text):
        """Extract code with surrounding context intelligence"""
        sections = self.split_conversation_sections(text)
        
        for section in sections:
            # Analyze context before code blocks
            context = self.context_analyzer.analyze_surrounding_text(section)
            
            # Extract code blocks
            code_blocks = self.extract_code_blocks(section)
            
            for code_block in code_blocks:
                enhanced_block = self.enhance_with_context(code_block, context)
                self.code_blocks.append(enhanced_block)
        
        return self.compile_and_organize()
    
    def enhance_with_context(self, code_block, context):
        """Add execution context to code blocks"""
        return {
            'code': code_block['content'],
            'language': code_block['language'],
            'block_id': self.generate_block_id(code_block['content']),
            'filename_suggestion': self.suggest_filename(code_block, context),
            'execution_context': context.get('purpose', 'unknown'),
            'dependencies': self.detect_dependencies(code_block['content']),
            'required_imports': self.extract_imports(code_block['content']),
            'usage_instructions': context.get('instructions', ''),
            'tests_suggested': self.suggest_tests(code_block, context)
        }
    
    def suggest_filename(self, code_block, context):
        """Intelligently name files based on content and context"""
        language_extensions = {
            'python': '.py',
            'javascript': '.js', 
            'bash': '.sh',
            'html': '.html',
            'css': '.css',
            'json': '.json'
        }
        
        # Extract purpose from context
        purpose_keywords = self.extract_purpose_keywords(context)
        
        if purpose_keywords:
            base_name = purpose_keywords[0]  # Use first purpose keyword
        else:
            base_name = 'module'
        
        extension = language_extensions.get(code_block['language'], '.txt')
        return f"{base_name}{extension}"
    
    def compile_and_organize(self):
        """Organize extracted code into proper project structure"""
        project_structure = {}
        
        for block in self.code_blocks:
            # Determine file location based on context
            file_path = self.determine_file_path(block)
            
            # Add imports and dependencies
            full_content = self.assemble_complete_file(block)
            
            project_structure[file_path] = full_content
        
        return project_structure
    
    def determine_file_path(self, block):
        """Decide where in project structure code belongs"""
        if block['execution_context'] == 'main_script':
            return f"src/main{block['language_extension']}"
        elif 'test' in block['execution_context'].lower():
            return f"tests/test_{block['filename_suggestion']}"
        elif 'config' in block['execution_context'].lower():
            return f"config/{block['filename_suggestion']}"
        else:
            return f"src/modules/{block['filename_suggestion']}"

class ContextAnalyzer:
    def analyze_surrounding_text(self, text):
        """Extract execution context from conversation"""
        context = {
            'purpose': self.extract_purpose(text),
            'instructions': self.extract_instructions(text),
            'dependencies_mentioned': self.extract_mentioned_dependencies(text),
            'execution_environment': self.detect_environment(text)
        }
        return context
    
    def extract_purpose(self, text):
        purpose_indicators = {
            'this function': 'utility_function',
            'the main script': 'main_execution', 
            'test case': 'testing',
            'configuration': 'config_file',
            'api endpoint': 'web_service',
            'database': 'data_persistence'
        }
        
        for indicator, purpose in purpose_indicators.items():
            if indicator in text.lower():
                return purpose
        return 'general_utility'