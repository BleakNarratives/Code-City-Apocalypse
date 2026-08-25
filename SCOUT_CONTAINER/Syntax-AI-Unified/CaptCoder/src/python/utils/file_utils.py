"""
Syntax AI CaptCoder - File Utilities

Provides file operations, path utilities, and file type detection.

Integrated from:
- /RootBase/Loosies/auto_code_extractor.py
- /RootBase/Loosies/advanced_code_bundler.py

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import re
import json
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Union
import logging

logger = logging.getLogger(__name__)


class FileUtils:
    """
    Utility class for file operations.
    
    Provides:
    - Safe file reading/writing
    - Path manipulation
    - File type detection
    - File search and filtering
    - File hashing
    - Directory operations
    """
    
    # Code file extensions
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp',
        '.h', '.hpp', '.go', '.rust', '.rs', '.swift', '.kt', '.scala',
        '.rb', '.php', '.sh', '.bash', '.zsh', '.ps1', '.lua'
    }
    
    # Text file extensions
    TEXT_EXTENSIONS = {
        '.txt', '.md', '.rst', '.csv', '.json', '.xml', '.yaml',
        '.yml', '.toml', '.cfg', '.conf', '.ini', '.log'
    }
    
    # Markup/file extensions
    MARKUP_EXTENSIONS = {
        '.html', '.htm', '.xhtml', '.css', '.scss', '.sass', '.less'
    }
    
    # All supported extensions
    SUPPORTED_EXTENSIONS = CODE_EXTENSIONS | TEXT_EXTENSIONS | MARKUP_EXTENSIONS
    
    @classmethod
    def get_file_extension(cls, file_path: str) -> str:
        """Get the file extension from a path."""
        return Path(file_path).suffix.lower()
    
    @classmethod
    def is_code_file(cls, file_path: str) -> bool:
        """Check if a file is a code file."""
        ext = cls.get_file_extension(file_path)
        return ext in cls.CODE_EXTENSIONS
    
    @classmethod
    def is_text_file(cls, file_path: str) -> bool:
        """Check if a file is a text file."""
        ext = cls.get_file_extension(file_path)
        return ext in cls.TEXT_EXTENSIONS
    
    @classmethod
    def is_markup_file(cls, file_path: str) -> bool:
        """Check if a file is a markup file."""
        ext = cls.get_file_extension(file_path)
        return ext in cls.MARKUP_EXTENSIONS
    
    @classmethod
    def is_supported_file(cls, file_path: str) -> bool:
        """Check if a file has a supported extension."""
        ext = cls.get_file_extension(file_path)
        return ext in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def detect_language(cls, file_path: str) -> str:
        """
        Detect the programming language from file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Language name or 'unknown'
        """
        ext = cls.get_file_extension(file_path)
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.go': 'go',
            '.rust': 'rust',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.rb': 'ruby',
            '.php': 'php',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'bash',
            '.ps1': 'powershell',
            '.lua': 'lua',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml'
        }
        
        return language_map.get(ext, 'unknown')
    
    @classmethod
    def detect_language_from_content(cls, content: str) -> str:
        """
        Detect the programming language from file content.
        
        Args:
            content: The file content
            
        Returns:
            Language name or 'unknown'
        """
        # Language patterns
        language_patterns = [
            (r'\bdef\s+\w+', 'python'),
            (r'\bimport\s+\w+', 'python'),
            (r'\bclass\s+\w+', 'python'),
            (r'\bprint\(', 'python'),
            (r'\bfunction\s+\w+', 'javascript'),
            (r'\bconst\s+\w+', 'javascript'),
            (r'\blet\s+\w+', 'javascript'),
            (r'\bvar\s+\w+', 'javascript'),
            (r'\b=>\s*', 'javascript'),
            (r'\bconsole\.log\(', 'javascript'),
            (r'\bpublic\s+class\s+\w+', 'java'),
            (r'\bprivate\s+\w+', 'java'),
            (r'\bvoid\s+\w+', 'java'),
            (r'\bstatic\s+\w+', 'java'),
            (r'\bnew\s+\w+', 'java'),
            (r'\b# include\s+<', 'cpp'),
            (r'\bstd::\w+', 'cpp'),
            (r'\bcout\s*<<', 'cpp'),
            (r'\bcin\s*>>', 'cpp'),
            (r'\bnamespace\s+\w+', 'cpp'),
            (r'\bSELECT\s+', 'sql'),
            (r'\bFROM\s+', 'sql'),
            (r'\bWHERE\s+', 'sql'),
            (r'\bINSERT\s+INTO\s+', 'sql'),
            (r'\bUPDATE\s+', 'sql'),
            (r'\bDELETE\s+FROM\s+', 'sql'),
            (r'\b package\s+', 'go'),
            (r'\bimport\s+"', 'go'),
            (r'\bfunc\s+\w+', 'go'),
            (r'<\?php', 'php'),
            (r'\b<?\s*\$', 'php'),
            (r'#!/bin/bash', 'bash'),
            (r'#!/usr/bin/env\s+bash', 'bash'),
            (r'\becho\s+', 'bash'),
            (r'\bgrep\s+', 'bash'),
            (r'\bdef\s+\w+\(', 'ruby'),
            (r'\bclass\s+\w+\s*<', 'ruby'),
            (r'\bdo\s*\|', 'ruby'),
        ]
        
        # Check patterns
        scores: Dict[str, int] = {}
        for pattern, language in language_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                scores[language] = scores.get(language, 0) + 1
        
        # Return language with highest score
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return 'unknown'
    
    @classmethod
    def read_file(cls, file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        Read a file safely.
        
        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)
            
        Returns:
            File content or None if error
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
                return None
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    @classmethod
    def write_file(cls, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        Write to a file safely.
        
        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create parent directories if needed
            parent_dir = os.path.dirname(file_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False
    
    @classmethod
    def append_file(cls, file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """
        Append to a file safely.
        
        Args:
            file_path: Path to the file
            content: Content to append
            encoding: File encoding (default: utf-8)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error appending to file {file_path}: {e}")
            return False
    
    @classmethod
    def file_exists(cls, file_path: str) -> bool:
        """Check if a file exists."""
        return os.path.isfile(file_path)
    
    @classmethod
    def directory_exists(cls, dir_path: str) -> bool:
        """Check if a directory exists."""
        return os.path.isdir(dir_path)
    
    @classmethod
    def create_directory(cls, dir_path: str, exist_ok: bool = True) -> bool:
        """
        Create a directory.
        
        Args:
            dir_path: Path to the directory
            exist_ok: If True, don't raise error if directory exists
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(dir_path, exist_ok=exist_ok)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            return False
    
    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    @classmethod
    def delete_directory(cls, dir_path: str, recursive: bool = True) -> bool:
        """
        Delete a directory.
        
        Args:
            dir_path: Path to the directory
            recursive: If True, delete directory tree
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(dir_path):
                if recursive:
                    shutil.rmtree(dir_path)
                else:
                    os.rmdir(dir_path)
            return True
        except Exception as e:
            logger.error(f"Error deleting directory {dir_path}: {e}")
            return False
    
    @classmethod
    def copy_file(cls, src: str, dst: str) -> bool:
        """
        Copy a file.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            logger.error(f"Error copying file from {src} to {dst}: {e}")
            return False
    
    @classmethod
    def move_file(cls, src: str, dst: str) -> bool:
        """
        Move a file.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.move(src, dst)
            return True
        except Exception as e:
            logger.error(f"Error moving file from {src} to {dst}: {e}")
            return False
    
    @classmethod
    def get_file_hash(cls, file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """
        Generate a hash of a file.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm (md5, sha1, sha256)
            
        Returns:
            Hash string or None if error
        """
        try:
            hash_func = getattr(hashlib, algorithm.lower())()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        except Exception as e:
            logger.error(f"Error hashing file {file_path}: {e}")
            return None
    
    @classmethod
    def get_file_size(cls, file_path: str) -> Optional[int]:
        """
        Get the size of a file in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes or None if error
        """
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Error getting file size for {file_path}: {e}")
            return None
    
    @classmethod
    def get_file_mod_time(cls, file_path: str) -> Optional[float]:
        """
        Get the modification time of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Timestamp or None if error
        """
        try:
            return os.path.getmtime(file_path)
        except Exception as e:
            logger.error(f"Error getting file modification time for {file_path}: {e}")
            return None
    
    @classmethod
    def find_files(
        cls,
        base_dir: str,
        extensions: Optional[Set[str]] = None,
        exclude_dirs: Optional[Set[str]] = None,
        recursive: bool = True
    ) -> List[str]:
        """
        Find files in a directory matching criteria.
        
        Args:
            base_dir: Base directory to search
            extensions: Set of file extensions to match
            exclude_dirs: Set of directory names to exclude
            recursive: If True, search recursively
            
        Returns:
            List of matching file paths
        """
        if extensions is None:
            extensions = cls.SUPPORTED_EXTENSIONS
        
        if exclude_dirs is None:
            exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'dist', '.vscode'}
        
        matches: List[str] = []
        
        try:
            if recursive:
                for root, dirs, files in os.walk(base_dir):
                    # Filter out excluded directories
                    dirs[:] = [d for d in dirs if d not in exclude_dirs]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        ext = cls.get_file_extension(file_path)
                        if ext in extensions:
                            matches.append(file_path)
            else:
                for file in os.listdir(base_dir):
                    file_path = os.path.join(base_dir, file)
                    if os.path.isfile(file_path):
                        ext = cls.get_file_extension(file_path)
                        if ext in extensions:
                            matches.append(file_path)
        except Exception as e:
            logger.error(f"Error finding files in {base_dir}: {e}")
        
        return matches
    
    @classmethod
    def read_json(cls, file_path: str) -> Optional[Dict]:
        """
        Read a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Parsed JSON or None if error
        """
        try:
            content = cls.read_file(file_path)
            if content:
                return json.loads(content)
            return None
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return None
    
    @classmethod
    def write_json(cls, file_path: str, data: Dict, indent: int = 2) -> bool:
        """
        Write a JSON file.
        
        Args:
            file_path: Path to the JSON file
            data: Data to write
            indent: Indentation level (default: 2)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            return cls.write_file(file_path, content)
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False
    
    @classmethod
    def sanitize_filename(cls, name: str, max_length: int = 255) -> str:
        """
        Sanitize a string for use as a filename.
        
        Args:
            name: The string to sanitize
            max_length: Maximum filename length
            
        Returns:
            Sanitized filename
        """
        # Replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)
        
        # Replace multiple consecutive invalid characters
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing spaces and underscores
        sanitized = sanitized.strip('_ ')
        
        # Truncate if too long
        if len(sanitized) > max_length:
            # Try to preserve extension
            parts = sanitized.rsplit('.', 1)
            if len(parts) == 2 and len(parts[1]) < 10:
                ext = '.' + parts[1]
                name_part = parts[0][:max_length - len(ext)]
                sanitized = name_part + ext
            else:
                sanitized = sanitized[:max_length]
        
        # Ensure we have a valid filename
        if not sanitized or sanitized in ('.', '..'):
            sanitized = 'unnamed'
        
        return sanitized
    
    @classmethod
    def generate_temp_filename(cls, prefix: str = 'temp', extension: str = 'tmp') -> str:
        """
        Generate a temporary filename.
        
        Args:
            prefix: Filename prefix
            extension: File extension (without dot)
            
        Returns:
            Temporary filename with full path
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{prefix}_{timestamp}.{extension}"
        
        # Use system temp directory
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, filename)


# Import tempfile for generate_temp_filename
import datetime
import tempfile


class PathUtils:
    """Path manipulation utilities."""
    
    @classmethod
    def get_absolute_path(cls, path: str) -> str:
        """Get absolute path."""
        return os.path.abspath(path)
    
    @classmethod
    def get_relative_path(cls, path: str, relative_to: str = None) -> str:
        """Get path relative to another path."""
        if relative_to is None:
            relative_to = os.getcwd()
        return os.path.relpath(path, relative_to)
    
    @classmethod
    def join_paths(cls, *paths: str) -> str:
        """Join multiple path components."""
        return os.path.join(*paths)
    
    @classmethod
    def get_directory(cls, file_path: str) -> str:
        """Get directory from file path."""
        return os.path.dirname(file_path)
    
    @classmethod
    def get_filename(cls, file_path: str) -> str:
        """Get filename from file path."""
        return os.path.basename(file_path)
    
    @classmethod
    def get_filename_without_extension(cls, file_path: str) -> str:
        """Get filename without extension."""
        filename = cls.get_filename(file_path)
        return os.path.splitext(filename)[0]
    
    @classmethod
    def get_extension(cls, file_path: str) -> str:
        """Get file extension."""
        return os.path.splitext(file_path)[1]
    
    @classmethod
    def normalize_path(cls, path: str) -> str:
        """Normalize a path."""
        return os.path.normpath(path)
    
    @classmethod
    def is_subpath(cls, path: str, parent: str) -> bool:
        """Check if path is a subpath of parent."""
        path = cls.get_absolute_path(path)
        parent = cls.get_absolute_path(parent)
        return path.startswith(parent + os.sep) or path == parent
