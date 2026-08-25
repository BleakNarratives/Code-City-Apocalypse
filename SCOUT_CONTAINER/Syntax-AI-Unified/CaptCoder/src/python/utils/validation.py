"""
Syntax AI CaptCoder - Validation Utilities

Provides input validation, code validation, and security checks.

Author: Syntax AI Team
Version: 1.0.0
"""

import re
import ast
import logging
from typing import List, Dict, Any, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


class ValidationUtils:
    """
    Utility class for validation.
    
    Provides:
    - Input validation
    - Code validation
    - Security checks
    - Sanitization
    """
    
    # Maximum lengths
    MAX_INPUT_LENGTH = 10000
    MAX_CODE_LENGTH = 100000
    MAX_FILENAME_LENGTH = 255
    MAX_LINE_LENGTH = 1000
    
    # Dangerous patterns
    DANGEROUS_PATTERNS = [
        r'\beval\(',  # eval
        r'\nexec\(',  # exec
        r'\bcompile\(',  # compile
        r'\b__import__\(',  # __import__
        r'\bopen\(',  # file open (context depends)
        r'\bos\.system\(',  # os.system
        r'\bos\.popen\(',  # os.popen
        r'\bsubprocess\.call\(',  # subprocess.call
        r'\bsubprocess\.run\(',  # subprocess.run
        r'\bsubprocess\.Popen\(',  # subprocess.Popen
        r'\bgetattr\(',  # getattr (can be dangerous)
        r'\bsetattr\(',  # setattr (can be dangerous)
        r'\bdelattr\(',  # delattr (can be dangerous)
        r'\bbytes\(',  # bytes (can be used for exploits)
        r'\bbytearray\(',  # bytearray
        r'\bmemoryview\(',  # memoryview
    ]
    
    # Allowed characters for various contexts
    SAFE_FILENAME_CHARS = r'[^\x00-\x1f<>:"/\\|?*]'  # Characters NOT allowed in filenames
    SAFE_CODE_CHARS = None  # Code can contain almost anything
    
    @classmethod
    def validate_input(cls, text: str, context: str = "general") -> Tuple[bool, Optional[str]]:
        """
        Validate input text.
        
        Args:
            text: The text to validate
            context: The context for validation (general, filename, code, command)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if text is None:
            return False, "Input cannot be None"
        
        if not isinstance(text, str):
            return False, f"Input must be a string, got {type(text).__name__}"
        
        # Check length
        max_length = getattr(cls, f"MAX_{context.upper()}_LENGTH", cls.MAX_INPUT_LENGTH)
        if len(text) > max_length:
            return False, f"Input too long (max {max_length} characters)"
        
        # Context-specific validation
        if context == "filename":
            return cls.validate_filename(text)
        elif context == "code":
            return cls.validate_code(text)
        elif context == "command":
            return cls.validate_command(text)
        
        # General validation
        return True, None
    
    @classmethod
    def validate_filename(cls, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a filename.
        
        Args:
            filename: The filename to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename cannot be empty"
        
        if len(filename) > cls.MAX_FILENAME_LENGTH:
            return False, f"Filename too long (max {cls.MAX_FILENAME_LENGTH} characters)"
        
        # Check for invalid characters
        if re.search(cls.SAFE_FILENAME_CHARS, filename):
            invalid_chars = set(re.findall(cls.SAFE_FILENAME_CHARS, filename))
            return False, f"Filename contains invalid characters: {invalid_chars}"
        
        # Check for reserved names
        reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                         'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3']
        if filename.upper() in reserved_names:
            return False, f"Filename is a reserved name: {filename}"
        
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Filename cannot contain path separators or traversal"
        
        return True, None
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize a filename to make it safe.
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        sanitized = re.sub(cls.SAFE_FILENAME_CHARS, '_', filename)
        
        # Replace multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Truncate if too long
        if len(sanitized) > cls.MAX_FILENAME_LENGTH:
            # Try to preserve extension
            parts = sanitized.rsplit('.', 1)
            if len(parts) == 2 and len(parts[1]) < 10:
                ext = '.' + parts[1]
                name_part = parts[0][:cls.MAX_FILENAME_LENGTH - len(ext)]
                sanitized = name_part + ext
            else:
                sanitized = sanitized[:cls.MAX_FILENAME_LENGTH]
        
        # Ensure we have a valid filename
        if not sanitized:
            sanitized = 'unnamed'
        
        return sanitized
    
    @classmethod
    def validate_code(cls, code: str, check_syntax: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Validate code.
        
        Args:
            code: The code to validate
            check_syntax: Whether to check Python syntax (if applicable)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not code:
            return False, "Code cannot be empty"
        
        if len(code) > cls.MAX_CODE_LENGTH:
            return False, f"Code too long (max {cls.MAX_CODE_LENGTH} characters)"
        
        # Check for extremely long lines
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if len(line) > cls.MAX_LINE_LENGTH:
                return False, f"Line {i+1} is too long (max {cls.MAX_LINE_LENGTH} characters)"
        
        # Check for dangerous patterns
        dangerous = cls.check_for_dangerous_patterns(code)
        if dangerous:
            return False, f"Code contains potentially dangerous patterns: {dangerous}"
        
        # Optionally check Python syntax
        if check_syntax:
            try:
                ast.parse(code)
            except SyntaxError as e:
                return False, f"Syntax error: {e}"
            except Exception as e:
                # Not Python code, that's okay
                pass
        
        return True, None
    
    @classmethod
    def check_for_dangerous_patterns(cls, code: str) -> Optional[List[str]]:
        """
        Check code for potentially dangerous patterns.
        
        Args:
            code: The code to check
            
        Returns:
            List of dangerous patterns found, or None if safe
        """
        found_patterns = []
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                found_patterns.append(pattern)
        
        return found_patterns if found_patterns else None
    
    @classmethod
    def validate_command(cls, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a command.
        
        Args:
            command: The command to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not command:
            return False, "Command cannot be empty"
        
        if len(command) > cls.MAX_INPUT_LENGTH:
            return False, f"Command too long (max {cls.MAX_INPUT_LENGTH} characters)"
        
        # Check for command injection patterns
        dangerous_patterns = [
            r'[;&|`]',  # Command chaining
            r'\$\(',  # Command substitution
            r'\$\{',  # Command substitution
            r'\$EN',  # Environment variables
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                return False, f"Command contains dangerous pattern: {pattern}"
        
        return True, None
    
    @classmethod
    def sanitize_command(cls, command: str) -> str:
        """
        Sanitize a command to make it safe.
        
        Args:
            command: The command to sanitize
            
        Returns:
            Sanitized command
        """
        # Remove dangerous patterns
        sanitized = re.sub(r'[;&|`]', '', command)
        sanitized = re.sub(r'\$\(', '', sanitized)
        sanitized = re.sub(r'\$\{', '', sanitized)
        
        # Remove leading/trailing whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @classmethod
    def validate_path(cls, path: str, allow_absolute: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Validate a file path.
        
        Args:
            path: The path to validate
            allow_absolute: Whether to allow absolute paths
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not path:
            return False, "Path cannot be empty"
        
        # Check for path traversal
        if '..' in path:
            return False, "Path cannot contain '..' (path traversal)"
        
        # Check for null bytes
        if '\x00' in path:
            return False, "Path cannot contain null bytes"
        
        # Check if absolute paths are allowed
        if not allow_absolute and os.path.isabs(path):
            return False, "Absolute paths are not allowed"
        
        return True, None
    
    @classmethod
    def sanitize_path(cls, path: str) -> str:
        """
        Sanitize a file path.
        
        Args:
            path: The path to sanitize
            
        Returns:
            Sanitized path
        """
        import os
        
        # Remove null bytes
        sanitized = path.replace('\x00', '')
        
        # Normalize path
        sanitized = os.path.normpath(sanitized)
        
        # Remove path traversal
        sanitized = sanitized.replace('..', '')
        
        # Remove leading/trailing slashes
        sanitized = sanitized.strip('/\\')
        
        return sanitized
    
    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an email address.
        
        Args:
            email: The email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not email:
            return False, "Email cannot be empty"
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, None
    
    @classmethod
    def validate_url(cls, url: str, require_protocol: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Validate a URL.
        
        Args:
            url: The URL to validate
            require_protocol: Whether to require http:// or https://
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"
        
        pattern = r'^[a-zA-Z]+://[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})?(/[^\s]*)?$' if require_protocol else \
                 r'^[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})?(/[^\s]*)?$'
        
        if not re.match(pattern, url, re.IGNORECASE):
            return False, "Invalid URL format"
        
        return True, None


# Import os for path validation
import os
