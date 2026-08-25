"""
Syntax AI CaptCoder - Code Extractor

Unified code extraction from files, directories, and various sources.
Integrates concepts from multiple sources:
- /RootBase/Loosies/auto_code_extractor.py
- /RootBase/Loosies/chat_code_capture.py
- /RootBase/syntax_captcoder/syntax_captcoder.py

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import re
import json
import time
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Callable, Union
from dataclasses import dataclass, field

from ..utils.file_utils import FileUtils
from ..utils.text_utils import TextUtils
from ..utils.validation import ValidationUtils

logger = logging.getLogger(__name__)


@dataclass
class ExtractedCode:
    """Represents a piece of extracted code."""
    content: str
    language: str = "unknown"
    source: str = "unknown"
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    """Result of a code extraction operation."""
    extracted: List[ExtractedCode]
    source: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    stats: Dict[str, Any] = field(default_factory=dict)


class CodeExtractor:
    """
    Unified code extractor that handles multiple sources.
    
    Extracts code from:
    - Files (monitored directories)
    - Chat messages
    - Screen content (via OCR)
    - Clipboard
    - Manual input
    
    Features:
    - Multiple file format support
    - Hash-based change detection
    - Event-based callbacks
    - Batch extraction
    """
    
    def __init__(
        self,
        watch_dirs: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
        code_extensions: Optional[Set[str]] = None,
        enable_watchdog: bool = True
    ):
        """
        Initialize the CodeExtractor.
        
        Args:
            watch_dirs: Directories to watch for new code files
            output_dir: Directory to save extracted code
            code_extensions: File extensions to monitor
            enable_watchdog: Use watchdog for real-time monitoring
        """
        self.file_utils = FileUtils()
        self.text_utils = TextUtils()
        self.validation = ValidationUtils()
        
        # Configuration
        self.watch_dirs = watch_dirs or self._get_default_watch_dirs()
        self.output_dir = output_dir or "/storage/emulated/0/auto_extracted_code"
        self.code_extensions = code_extensions or FileUtils.CODE_EXTENSIONS
        
        # State
        self._processed_files: Set[str] = set()
        self._file_hashes: Dict[str, str] = {}
        self._extracted_code: List[ExtractedCode] = []
        
        # Callbacks
        self._code_extracted_callbacks: List[Callable] = []
        self._file_processed_callbacks: List[Callable] = []
        self._error_callbacks: List[Callable] = []
        
        # Statistics
        self.stats = {
            "files_processed": 0,
            "code_snippets_extracted": 0,
            "errors": 0,
            "started_at": datetime.datetime.now().isoformat()
        }
        
        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"CodeExtractor initialized. Watching: {self.watch_dirs}")
    
    def _get_default_watch_dirs(self) -> List[str]:
        """Get default directories to watch."""
        default_dirs = [
            "/storage/emulated/0/Download",
            "/storage/emulated/0/Documents",
            "/storage/emulated/0/scripts"
        ]
        return [d for d in default_dirs if os.path.exists(d)]
    
    def extract_from_text(self, text: str, source: str = "chat") -> ExtractionResult:
        """
        Extract code blocks from text.
        
        Args:
            text: Text to extract code from
            source: Source identifier
            
        Returns:
            ExtractionResult with extracted code
        """
        code_blocks = self.text_utils.extract_code_blocks(text)
        
        extracted: List[ExtractedCode] = []
        
        for block in code_blocks:
            if not block.get("code") or not block["code"].strip():
                continue
            
            extracted_code = ExtractedCode(
                content=block["code"],
                language=block.get("language", "unknown"),
                source=source,
                timestamp=datetime.datetime.now().isoformat(),
                metadata={
                    "type": block.get("type", "unknown"),
                    "source": source
                }
            )
            extracted.append(extracted_code)
            self._extracted_code.append(extracted_code)
            self.stats["code_snippets_extracted"] += 1
            self._notify_code_extracted(extracted_code)
        
        return ExtractionResult(
            extracted=extracted,
            source=source,
            stats={"count": len(extracted)}
        )
    
    def extract_from_file(self, file_path: str) -> Optional[ExtractedCode]:
        """
        Extract code from a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            ExtractedCode or None if error
        """
        try:
            content = self.file_utils.read_file(file_path)
            if content is None:
                return None
            
            language = self.file_utils.detect_language(file_path)
            
            extracted = ExtractedCode(
                content=content,
                language=language,
                source="file",
                file_path=file_path,
                timestamp=datetime.datetime.now().isoformat(),
                metadata={
                    "file_path": file_path,
                    "file_size": self.file_utils.get_file_size(file_path),
                    "file_mod_time": self.file_utils.get_file_mod_time(file_path)
                }
            )
            
            self._extracted_code.append(extracted)
            self.stats["files_processed"] += 1
            self.stats["code_snippets_extracted"] += 1
            self._notify_code_extracted(extracted)
            
            return extracted
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error extracting from file {file_path}: {e}")
            self._notify_error(f"File extraction failed: {file_path}", e)
            return None
    
    def extract_from_directory(self, dir_path: str, recursive: bool = True) -> ExtractionResult:
        """
        Extract code from all files in a directory.
        
        Args:
            dir_path: Path to the directory
            recursive: Whether to search subdirectories
            
        Returns:
            ExtractionResult with all extracted code
        """
        files = self.file_utils.find_files(
            dir_path,
            extensions=self.code_extensions,
            recursive=recursive
        )
        
        extracted: List[ExtractedCode] = []
        
        for file_path in files:
            code = self.extract_from_file(file_path)
            if code:
                extracted.append(code)
        
        return ExtractionResult(
            extracted=extracted,
            source=dir_path,
            stats={
                "files_scanned": len(files),
                "files_extracted": len(extracted)
            }
        )
    
    def extract_from_all_watch_dirs(self) -> List[ExtractionResult]:
        """
        Extract code from all watched directories.
        
        Returns:
            List of ExtractionResult for each directory
        """
        results: List[ExtractionResult] = []
        
        for watch_dir in self.watch_dirs:
            if os.path.exists(watch_dir):
                result = self.extract_from_directory(watch_dir)
                results.append(result)
            else:
                logger.warning(f"Watch directory does not exist: {watch_dir}")
        
        return results
    
    def monitor_directory(self, dir_path: str) -> None:
        """
        Monitor a directory for new code files (non-blocking).
        
        Args:
            dir_path: Directory to monitor
        """
        if dir_path not in self.watch_dirs:
            self.watch_dirs.append(dir_path)
        
        # Scan existing files
        self._scan_directory(dir_path)
    
    def _scan_directory(self, dir_path: str) -> None:
        """Scan a directory for code files."""
        files = self.file_utils.find_files(
            dir_path,
            extensions=self.code_extensions,
            recursive=True
        )
        
        for file_path in files:
            file_id = self._get_file_id(file_path)
            if file_id not in self._processed_files:
                self._processed_files.add(file_id)
                self.extract_from_file(file_path)
    
    def _get_file_id(self, file_path: str) -> str:
        """Generate a unique ID for a file."""
        try:
            abs_path = os.path.abspath(file_path)
            file_hash = self.file_utils.get_file_hash(file_path)
            return f"{abs_path}:{file_hash}" if file_hash else abs_path
        except:
            return file_path
    
    def _notify_code_extracted(self, code: ExtractedCode) -> None:
        """Notify callbacks about extracted code."""
        for callback in self._code_extracted_callbacks:
            try:
                callback(code)
            except Exception as e:
                logger.error(f"Code extracted callback error: {e}")
    
    def _notify_file_processed(self, file_path: str) -> None:
        """Notify callbacks about processed file."""
        for callback in self._file_processed_callbacks:
            try:
                callback(file_path)
            except Exception as e:
                logger.error(f"File processed callback error: {e}")
    
    def _notify_error(self, message: str, error: Exception) -> None:
        """Notify callbacks about errors."""
        for callback in self._error_callbacks:
            try:
                callback(message, error)
            except Exception as e:
                logger.error(f"Error callback error: {e}")
    
    def save_extracted_code(
        self,
        code: ExtractedCode,
        output_dir: Optional[str] = None
    ) -> str:
        """
        Save extracted code to a file.
        
        Args:
            code: ExtractedCode to save
            output_dir: Directory to save to (defaults to self.output_dir)
            
        Returns:
            Path to the saved file
        """
        dir_path = output_dir or self.output_dir
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        ext = self.file_utils.detect_language(code.language)
        
        if code.file_path:
            # Use original filename if available
            filename = Path(code.file_path).name
        else:
            # Generate from code content
            filename = self.text_utils.generate_filename_from_text(
                code.content[:50],
                code.language
            )
        
        filepath = os.path.join(dir_path, f"{timestamp}_{filename}")
        
        # Add header with metadata
        header = f"""# Extracted by Syntax AI CaptCoder
# Source: {code.source}
# Language: {code.language}
# Extracted: {code.timestamp}
# File: {code.file_path or 'N/A'}

"""
        
        content = header + code.content
        
        self.file_utils.write_file(filepath, content)
        logger.info(f"Saved extracted code: {filepath}")
        
        return filepath
    
    def auto_extract_and_save(self, dir_path: str) -> None:
        """
        Auto-extract code from directory and save to output.
        
        Args:
            dir_path: Directory to extract from
        """
        result = self.extract_from_directory(dir_path)
        
        for code in result.extracted:
            self.save_extracted_code(code)
    
    # Callback registration
    def on_code_extracted(self, callback: Callable[[ExtractedCode], None]) -> None:
        """Register callback for code extraction events."""
        self._code_extracted_callbacks.append(callback)
    
    def on_file_processed(self, callback: Callable[[str], None]) -> None:
        """Register callback for file processed events."""
        self._file_processed_callbacks.append(callback)
    
    def on_error(self, callback: Callable[[str, Exception], None]) -> None:
        """Register callback for errors."""
        self._error_callbacks.append(callback)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "files_processed": 0,
            "code_snippets_extracted": 0,
            "errors": 0,
            "started_at": datetime.datetime.now().isoformat()
        }
    
    def get_extracted_code(self) -> List[ExtractedCode]:
        """Get all extracted code."""
        return self._extracted_code.copy()
    
    def clear_extracted_code(self) -> None:
        """Clear all extracted code."""
        self._extracted_code = []


# Import datetime
import datetime


def main():
    """Test CodeExtractor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CodeExtractor - Extract code from various sources")
    parser.add_argument("--text", type=str, help="Extract code from text")
    parser.add_argument("--file", type=str, help="Extract code from file")
    parser.add_argument("--dir", type=str, help="Extract code from directory")
    parser.add_argument("--monitor", type=str, help="Monitor directory for changes")
    parser.add_argument("--save", action="store_true", help="Save extracted code to output directory")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()
    
    extractor = CodeExtractor()
    
    if args.text:
        result = extractor.extract_from_text(args.text)
        print(f"Extracted {len(result.extracted)} code blocks from text")
        for i, code in enumerate(result.extracted):
            print(f"\n--- Code Block {i+1} ({code.language}) ---")
            print(code.content[:200] + "..." if len(code.content) > 200 else code.content)
    
    elif args.file:
        code = extractor.extract_from_file(args.file)
        if code:
            print(f"Extracted code from {args.file}")
            print(f"Language: {code.language}")
            print(f"Content length: {len(code.content)} characters")
            if args.save:
                path = extractor.save_extracted_code(code)
                print(f"Saved to: {path}")
    
    elif args.dir:
        result = extractor.extract_from_directory(args.dir)
        print(f"Extracted {len(result.extracted)} code files from {args.dir}")
        if args.save:
            for code in result.extracted:
                extractor.save_extracted_code(code)
            print(f"All files saved to {extractor.output_dir}")
    
    elif args.monitor:
        extractor.monitor_directory(args.monitor)
        print(f"Monitoring directory: {args.monitor}")
    
    elif args.stats:
        print(json.dumps(extractor.get_stats(), indent=2))
    
    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    main()
