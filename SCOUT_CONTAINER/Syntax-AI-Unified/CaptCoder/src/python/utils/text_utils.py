"""
Syntax AI CaptCoder - Text Utilities

Provides text processing, code block extraction, and language detection.

Integrated from:
- /RootBase/Loosies/chat_code_capture.py
- /RootBase/Loosies/code_processor.py (Java - concepts ported to Python)

Author: Syntax AI Team
Version: 1.0.0
"""

import re
import logging
from typing import List, Dict, Optional, Tuple, Set

logger = logging.getLogger(__name__)


class TextUtils:
    """
    Utility class for text processing.
    
    Provides:
    - Code block extraction from text
    - Language detection from code
    - Text cleaning and normalization
    - Pattern matching
    """
    
    # Code block patterns
    CODE_BLOCK_PATTERNS = [
        # Triple backticks with optional language
        (r'```(\w*)\s*([\s\S]*?)```', 'fenced'),
        # Single backticks
        (r'`([^`]+)`', 'inline'),
        # Indented blocks (4 spaces or tab)
        (r'^(?:    |\t)(.+)$', 'indented'),
    ]
    
    # Language keywords for detection
    LANGUAGE_KEYWORDS = {
        'python': ['def ', 'import ', 'class ', 'print(', 'return ', 'if __name__', 'lambda ', 'self.'],
        'javascript': ['function ', 'const ', 'let ', 'var ', '=>', 'console.log', 'require(', 'export ', 'import '],
        'typescript': ['interface ', 'type ', 'any ', 'number ', 'string ', 'boolean ', 'void ', 'async '],
        'java': ['public ', 'private ', 'protected ', 'class ', 'void ', 'static ', 'new ', 'System.out.println'],
        'cpp': ['#include ', 'std::', 'cout <<', 'cin >>', 'namespace ', 'using namespace'],
        'csharp': ['using ', 'namespace ', 'class ', 'void ', 'public ', 'private '],
        'go': ['package ', 'import (', 'func ', 'var ', 'const ', 'type '],
        'rust': ['fn ', 'let ', 'mut ', 'const ', 'impl ', 'struct ', 'pub '],
        'ruby': ['def ', 'class ', 'end ', 'do ', 'if ', 'unless '],
        'php': ['<?php ', 'function ', 'class ', 'echo ', 'new ', '->'],
        'bash': ['#!/bin/bash', '#!/usr/bin/env bash', 'echo ', 'grep ', 'sed ', 'awk ', 'if [', 'for '],
        'sql': ['SELECT ', 'FROM ', 'WHERE ', 'INSERT INTO ', 'UPDATE ', 'DELETE FROM ', 'JOIN '],
        'html': ['<!DOCTYPE ', '<html', '<head', '<body', '<div', '<span', '<a href'],
        'css': ['{', '}', 'class ', 'id ', '@media ', 'display: ']
    }
    
    @classmethod
    def extract_code_blocks(cls, text: str) -> List[Dict[str, str]]:
        """
        Extract all code blocks from text.
        
        Args:
            text: The text to extract code from
            
        Returns:
            List of dictionaries with 'code' and 'type' (fenced, inline, indented)
        """
        blocks: List[Dict[str, str]] = []
        
        # Extract triple backtick blocks
        for match in re.finditer(r'```(\w*)\s*([\s\S]*?)```', text):
            language = match.group(1) or 'unknown'
            code = match.group(2).strip()
            if code:
                blocks.append({
                    'code': code,
                    'type': 'fenced',
                    'language': language
                })
        
        # Extract single backtick blocks
        for match in re.finditer(r'`([^`]+)`', text):
            code = match.group(1).strip()
            if code:
                blocks.append({
                    'code': code,
                    'type': 'inline',
                    'language': cls.detect_language(code)
                })
        
        # Extract indented blocks (requires multi-line processing)
        lines = text.split('\n')
        indented_block: List[str] = []
        in_block = False
        
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                if not in_block:
                    in_block = True
                    indented_block = []
                # Remove leading whitespace
                stripped_line = line.lstrip()
                if stripped_line:
                    indented_block.append(stripped_line)
            else:
                if in_block and indented_block:
                    code = '\n'.join(indented_block)
                    blocks.append({
                        'code': code,
                        'type': 'indented',
                        'language': cls.detect_language(code)
                    })
                    indented_block = []
                in_block = False
        
        # Handle case where text ends with indented block
        if in_block and indented_block:
            code = '\n'.join(indented_block)
            blocks.append({
                'code': code,
                'type': 'indented',
                'language': cls.detect_language(code)
            })
        
        return blocks
    
    @classmethod
    def extract_code_snippets(cls, text: str) -> List[str]:
        """
        Extract code snippets as simple strings.
        
        Args:
            text: The text to extract code from
            
        Returns:
            List of code snippets
        """
        blocks = cls.extract_code_blocks(text)
        return [block['code'] for block in blocks]
    
    @classmethod
    def detect_language(cls, code: str, hint: Optional[str] = None) -> str:
        """
        Detect the programming language from code content.
        
        Args:
            code: The code to analyze
            hint: Optional language hint (e.g., from fenced code block)
            
        Returns:
            Language name
        """
        # If hint is provided and valid, use it
        if hint and hint.lower() in cls.LANGUAGE_KEYWORDS:
            return hint.lower()
        
        # Score each language
        scores: Dict[str, int] = {}
        
        for language, keywords in cls.LANGUAGE_KEYWORDS.items():
            for keyword in keywords:
                # Case-insensitive search
                if re.search(keyword, code, re.IGNORECASE):
                    scores[language] = scores.get(language, 0) + 1
        
        # Return language with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        # Default to unknown
        return 'unknown'
    
    @classmethod
    def detect_tags(cls, text: str) -> List[Dict[str, str]]:
        """
        Detect special tags in text.
        
        Supports tags like:
        - #bsm (Blue Sky Meeting)
        - #task (Task)
        - #todo (To Do)
        - #python, #react, #fastapi (Language-specific)
        
        Args:
            text: The text to analyze
            
        Returns:
            List of tag dictionaries with 'tag', 'type', and 'description'
        """
        tags: List[Dict[str, str]] = []
        
        # Pattern for tags with optional description
        tag_pattern = r'(#(\w[\w-]*):?\s*(.*)?)$'
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            match = re.match(tag_pattern, line, re.IGNORECASE)
            if match:
                full_tag = match.group(1)
                tag_type = match.group(2).lower()
                description = (match.group(3) or '').strip()
                
                tags.append({
                    'tag': full_tag,
                    'type': tag_type,
                    'description': description if description else f"Tag: {full_tag}"
                })
            
            # Also check for inline tags
            inline_tags = re.findall(r'(#\w[\w-]*)', line)
            for tag in inline_tags:
                if tag not in [t['tag'] for t in tags]:
                    tags.append({
                        'tag': tag,
                        'type': tag[1:].lower(),
                        'description': f"Inline tag: {tag}"
                    })
        
        return tags
    
    @classmethod
    def clean_text(cls, text: str) -> str:
        """
        Clean text for processing.
        
        Removes:
        - Leading/trailing whitespace
        - Multiple consecutive newlines
        - Non-printable characters
        
        Args:
            text: The text to clean
            
        Returns:
            Cleaned text
        """
        # Remove non-printable characters (except newlines and tabs)
        cleaned = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
        
        # Normalize newlines
        cleaned = cleaned.replace('\r\n', '\n').replace('\r', '\n')
        
        # Collapse multiple newlines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
    
    @classmethod
    def normalize_code(cls, code: str, language: str = 'unknown') -> str:
        """
        Normalize code formatting.
        
        Args:
            code: The code to normalize
            language: The programming language
            
        Returns:
            Normalized code
        """
        # Clean the code
        code = cls.clean_text(code)
        
        # Language-specific normalization
        if language in ['python', 'javascript', 'typescript', 'java', 'cpp', 'csharp']:
            # Ensure proper indentation
            code = cls._normalize_indentation(code, language)
        
        # Remove trailing whitespace from each line
        lines = code.split('\n')
        lines = [line.rstrip() for line in lines]
        code = '\n'.join(lines)
        
        # Ensure file ends with newline
        if code and not code.endswith('\n'):
            code += '\n'
        
        return code
    
    @classmethod
    def _normalize_indentation(cls, code: str, language: str) -> str:
        """
        Normalize indentation for specific languages.
        
        Args:
            code: The code to normalize
            language: The programming language
            
        Returns:
            Code with normalized indentation
        """
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            if not line.strip():
                # Empty line - preserve or remove based on context
                normalized_lines.append('')
                continue
            
            # Count leading whitespace
            leading_spaces = len(line) - len(line.lstrip(' '))
            leading_tabs = len(line) - len(line.lstrip('\t'))
            
            # Convert tabs to spaces (4 spaces per tab for most languages)
            if leading_tabs > 0:
                if language in ['python', 'javascript', 'typescript']:
                    # Use 4 spaces per tab
                    indent = ' ' * (leading_tabs * 4)
                else:
                    # Use tabs as-is for other languages
                    indent = '\t' * leading_tabs
            elif leading_spaces > 0:
                if language in ['python']:
                    # Python uses 4 spaces
                    indent = ' ' * (leading_spaces // 4 * 4)
                else:
                    indent = ' ' * leading_spaces
            else:
                indent = ''
            
            # Preserve the actual content
            content = line[leading_spaces + leading_tabs:].rstrip()
            normalized_lines.append(indent + content)
        
        return '\n'.join(normalized_lines)
    
    @classmethod
    def extract_command(cls, text: str) -> Optional[str]:
        """
        Extract a command from text.
        
        Looks for patterns like:
        - "JaneNat, do something"
        - "Hey JaneNat, ..."
        - Direct commands
        
        Args:
            text: The text to extract command from
            
        Returns:
            Extracted command or None
        """
        # Pattern for JaneNat commands
        patterns = [
            r'JaneNat,\s*(.*)',
            r'Hey JaneNat,\s*(.*)',
            r'Ok JaneNat,\s*(.*)',
            r'JaneNat\s+(.*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                command = match.group(1).strip()
                if command:
                    return command
        
        return None
    
    @classmethod
    def extract_natural_language_command(cls, text: str) -> Optional[Dict[str, str]]:
        """
        Extract natural language command and intent.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with 'command', 'action', 'target' or None
        """
        text_lower = text.lower()
        
        # Intent patterns
        intents = {
            'create': ['create', 'make', 'build', 'generate', 'new'],
            'modify': ['modify', 'change', 'update', 'edit', 'fix'],
            'delete': ['delete', 'remove', 'erase', 'clear'],
            'read': ['read', 'show', 'display', 'view', 'list'],
            'search': ['search', 'find', 'look for', 'locate'],
            'run': ['run', 'execute', 'start', 'launch', 'test'],
            'stop': ['stop', 'quit', 'exit', 'end', 'terminate'],
            'help': ['help', '?', 'what can you do']
        }
        
        # Detect intent
        detected_intent = None
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_intent = intent
                    break
            if detected_intent:
                break
        
        if not detected_intent:
            return None
        
        # Extract target
        target = None
        for keyword in ['class', 'function', 'method', 'file', 'code', 'script', 'program', 'app']:
            if keyword in text_lower:
                target = keyword
                break
        
        # Remove intent keywords from text
        command_text = text
        for keyword in intents.get(detected_intent, []):
            command_text = re.sub(r'\b' + keyword + r'\b', '', command_text, flags=re.IGNORECASE)
        
        command_text = command_text.strip()
        if command_text.endswith('.'):
            command_text = command_text[:-1]
        
        return {
            'command': command_text,
            'action': detected_intent,
            'target': target,
            'original': text
        }
    
    @classmethod
    def generate_filename_from_text(cls, text: str, extension: str = 'py') -> str:
        """
        Generate a safe filename from text.
        
        Args:
            text: The text to use for filename
            extension: File extension (without dot)
            
        Returns:
            Safe filename
        """
        import datetime
        
        # Extract meaningful words
        words = re.findall(r'\b\w+\b', text)
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [w for w in words if w.lower() not in stop_words]
        
        # Capitalize and join
        if words:
            name = '_'.join(words[:5])  # Limit to first 5 words
        else:
            name = 'untitled'
        
        # Add timestamp for uniqueness
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        
        # Clean and sanitize
        name = re.sub(r'[^\w\-]', '', name)
        name = name[:50]  # Limit length
        
        return f"{name}_{timestamp}.{extension}"
    
    @classmethod
    def format_code_for_display(cls, code: str, language: str = 'unknown') -> str:
        """
        Format code for display in logs or UI.
        
        Args:
            code: The code to format
            language: The programming language
            
        Returns:
            Formatted code string
        """
        # Truncate long code
        if len(code) > 100:
            code = code[:100] + '...'
        
        # Add language indicator
        if language != 'unknown':
            return f"[{language}] {code}"
        
        return code
