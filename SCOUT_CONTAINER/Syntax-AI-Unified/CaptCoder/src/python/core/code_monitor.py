"""
Syntax AI CaptCoder - Code Monitor

Real-time code monitoring service that watches for code changes
and triggers extraction/processing automatically.

Integrated from:
- /RootBase/Loosies/auto_code_extractor.py
- /RootBase/syntax_captcoder/syntax_captcoder.py

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import time
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..utils.file_utils import FileUtils

logger = logging.getLogger(__name__)


class CodeChangeHandler(FileSystemEventHandler):
    """File system event handler for code monitoring."""
    
    def __init__(self, monitor: 'CodeMonitor'):
        self.monitor = monitor
    
    def on_created(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event(event.src_path, "created")
    
    def on_modified(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event(event.src_path, "modified")
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event(event.src_path, "deleted")


class CodeMonitor:
    """
    Monitors directories for code file changes and triggers processing.
    
    Features:
    - Watch multiple directories for changes
    - Hash-based change detection (avoids duplicate processing)
    - Configurable file extensions
    - Callback-based event handling
    """
    
    def __init__(
        self,
        watch_dirs: Optional[List[str]] = None,
        code_extensions: Optional[Set[str]] = None,
        check_interval: int = 30
    ):
        """
        Initialize the CodeMonitor.
        
        Args:
            watch_dirs: Directories to watch for changes
            code_extensions: File extensions to monitor (default: .py, .js, .ts, etc.)
            check_interval: Interval in seconds for manual checks
        """
        self.file_utils = FileUtils()
        
        # Configuration
        self.watch_dirs = watch_dirs or self._get_default_watch_dirs()
        self.code_extensions = code_extensions or self._get_default_extensions()
        self.check_interval = check_interval
        
        # State
        self._processed_files: Set[str] = set()
        self._file_hashes: Dict[str, str] = {}
        self._is_running = False
        self._observer: Optional[Observer] = None
        
        # Callbacks
        self._file_created_callbacks: List[Callable] = []
        self._file_modified_callbacks: List[Callable] = []
        self._file_deleted_callbacks: List[Callable] = []
        self._code_detected_callbacks: List[Callable] = []
        
        # Statistics
        self.stats = {
            "files_created": 0,
            "files_modified": 0,
            "files_deleted": 0,
            "code_files_processed": 0,
            "errors": 0
        }
        
        logger.info(f"CodeMonitor initialized. Watching: {self.watch_dirs}")
    
    def _get_default_watch_dirs(self) -> List[str]:
        """Get default directories to watch."""
        default_dirs = [
            "/storage/emulated/0/Download",
            "/storage/emulated/0/Documents",
            "/storage/emulated/0/scripts"
        ]
        
        # Filter to only existing directories
        return [d for d in default_dirs if os.path.exists(d)]
    
    def _get_default_extensions(self) -> Set[str]:
        """Get default code file extensions."""
        return {
            '.py', '.txt', '.js', '.ts', '.tsx', '.jsx',
            '.html', '.css', '.json', '.xml', '.yaml', '.yml',
            '.java', '.cpp', '.c', '.h', '.hpp', '.sh', '.md'
        }
    
    def is_code_file(self, file_path: str) -> bool:
        """Check if a file is a code file based on extension."""
        ext = Path(file_path).suffix.lower()
        return ext in self.code_extensions
    
    def get_file_hash(self, file_path: str) -> Optional[str]:
        """Generate MD5 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Error hashing file {file_path}: {e}")
            return None
    
    def _handle_file_event(self, file_path: str, event_type: str) -> None:
        """Handle a file system event."""
        try:
            if not self.is_code_file(file_path):
                return
            
            file_id = self._get_file_id(file_path)
            
            if event_type == "created":
                self.stats["files_created"] += 1
                self._notify_file_created(file_path)
                self._process_code_file(file_path)
                
            elif event_type == "modified":
                # Check if file was actually modified (not just saved)
                current_hash = self.get_file_hash(file_path)
                if current_hash and current_hash != self._file_hashes.get(file_id):
                    self.stats["files_modified"] += 1
                    self._file_hashes[file_id] = current_hash
                    self._notify_file_modified(file_path)
                    self._process_code_file(file_path)
                
            elif event_type == "deleted":
                self.stats["files_deleted"] += 1
                self._notify_file_deleted(file_path)
                if file_id in self._file_hashes:
                    del self._file_hashes[file_id]
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error handling file event {event_type} for {file_path}: {e}")
    
    def _get_file_id(self, file_path: str) -> str:
        """Generate a unique ID for a file."""
        try:
            abs_path = os.path.abspath(file_path)
            file_hash = self.get_file_hash(file_path)
            return f"{abs_path}:{file_hash}" if file_hash else abs_path
        except:
            return file_path
    
    def _process_code_file(self, file_path: str) -> None:
        """Process a code file."""
        try:
            if not self.is_code_file(file_path):
                return
            
            self.stats["code_files_processed"] += 1
            self._notify_code_detected(file_path)
            
            logger.info(f"📥 Code file detected: {file_path}")
            
            # Here you would typically:
            # 1. Extract code from the file
            # 2. Send to Nexus API
            # 3. Trigger optimization
            # This is handled by callbacks
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error processing code file {file_path}: {e}")
    
    def _notify_file_created(self, file_path: str) -> None:
        """Notify callbacks about file creation."""
        for callback in self._file_created_callbacks:
            try:
                callback(file_path)
            except Exception as e:
                logger.error(f"File created callback error: {e}")
    
    def _notify_file_modified(self, file_path: str) -> None:
        """Notify callbacks about file modification."""
        for callback in self._file_modified_callbacks:
            try:
                callback(file_path)
            except Exception as e:
                logger.error(f"File modified callback error: {e}")
    
    def _notify_file_deleted(self, file_path: str) -> None:
        """Notify callbacks about file deletion."""
        for callback in self._file_deleted_callbacks:
            try:
                callback(file_path)
            except Exception as e:
                logger.error(f"File deleted callback error: {e}")
    
    def _notify_code_detected(self, file_path: str) -> None:
        """Notify callbacks about code detection."""
        for callback in self._code_detected_callbacks:
            try:
                callback(file_path)
            except Exception as e:
                logger.error(f"Code detected callback error: {e}")
    
    def add_watch_dir(self, dir_path: str) -> None:
        """Add a directory to watch."""
        if dir_path not in self.watch_dirs:
            self.watch_dirs.append(dir_path)
            logger.info(f"Added watch directory: {dir_path}")
    
    def remove_watch_dir(self, dir_path: str) -> None:
        """Remove a directory from watch."""
        if dir_path in self.watch_dirs:
            self.watch_dirs.remove(dir_path)
            logger.info(f"Removed watch directory: {dir_path}")
    
    def start(self, use_watchdog: bool = True) -> None:
        """
        Start monitoring for code changes.
        
        Args:
            use_watchdog: Use watchdog library for real-time monitoring
                        If False, uses manual polling
        """
        if self._is_running:
            logger.warning("CodeMonitor is already running")
            return
        
        self._is_running = True
        
        # Initialize file hashes for existing files
        self._scan_existing_files()
        
        if use_watchdog:
            try:
                import watchdog
                self._start_watchdog()
            except ImportError:
                logger.warning("watchdog not installed, falling back to polling")
                self._start_polling()
        else:
            self._start_polling()
        
        logger.info("👁️  CodeMonitor started")
    
    def _start_watchdog(self) -> None:
        """Start watchdog-based monitoring."""
        self._observer = Observer()
        
        for watch_dir in self.watch_dirs:
            if os.path.exists(watch_dir):
                self._observer.schedule(
                    CodeChangeHandler(self),
                    watch_dir,
                    recursive=True
                )
        
        self._observer.start()
        logger.info("Using watchdog for real-time file monitoring")
    
    def _start_polling(self) -> None:
        """Start polling-based monitoring."""
        logger.info(f"Using polling for file monitoring (interval: {self.check_interval}s)")
        
        def polling_loop():
            while self._is_running:
                try:
                    self._check_for_changes()
                    time.sleep(self.check_interval)
                except Exception as e:
                    logger.error(f"Error in polling loop: {e}")
                    time.sleep(5)  # Wait before retrying
        
        import threading
        self._polling_thread = threading.Thread(target=polling_loop, daemon=True)
        self._polling_thread.start()
    
    def _scan_existing_files(self) -> None:
        """Scan existing files in watch directories."""
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            
            for root, dirs, files in os.walk(watch_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.is_code_file(file_path):
                        file_id = self._get_file_id(file_path)
                        file_hash = self.get_file_hash(file_path)
                        if file_hash:
                            self._file_hashes[file_id] = file_hash
                            self._processed_files.add(file_id)
        
        logger.info(f"Scanned {len(self._file_hashes)} existing code files")
    
    def _check_for_changes(self) -> None:
        """Check for file changes using polling."""
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            
            for root, dirs, files in os.walk(watch_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.is_code_file(file_path):
                        continue
                    
                    file_id = self._get_file_id(file_path)
                    current_hash = self.get_file_hash(file_path)
                    
                    if file_id not in self._file_hashes:
                        # New file
                        self._file_hashes[file_id] = current_hash
                        self._handle_file_event(file_path, "created")
                    elif current_hash != self._file_hashes.get(file_id):
                        # Modified file
                        self._file_hashes[file_id] = current_hash
                        self._handle_file_event(file_path, "modified")
    
    def stop(self) -> None:
        """Stop monitoring."""
        if not self._is_running:
            return
        
        self._is_running = False
        
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None
        
        if hasattr(self, '_polling_thread'):
            self._polling_thread.join(timeout=5)
        
        logger.info("🛑 CodeMonitor stopped")
    
    # Callback registration
    def on_file_created(self, callback: Callable[[str], None]) -> None:
        """Register callback for file creation events."""
        self._file_created_callbacks.append(callback)
    
    def on_file_modified(self, callback: Callable[[str], None]) -> None:
        """Register callback for file modification events."""
        self._file_modified_callbacks.append(callback)
    
    def on_file_deleted(self, callback: Callable[[str], None]) -> None:
        """Register callback for file deletion events."""
        self._file_deleted_callbacks.append(callback)
    
    def on_code_detected(self, callback: Callable[[str], None]) -> None:
        """Register callback for code detection events."""
        self._code_detected_callbacks.append(callback)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "files_created": 0,
            "files_modified": 0,
            "files_deleted": 0,
            "code_files_processed": 0,
            "errors": 0
        }


def main():
    """Run CodeMonitor in standalone mode."""
    import argparse
    
    parser = argparse.ArgumentParser(description="CodeMonitor - Monitor directories for code changes")
    parser.add_argument("--dirs", nargs="+", help="Directories to watch")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds")
    parser.add_argument("--no-watchdog", action="store_true", help="Disable watchdog, use polling")
    args = parser.parse_args()
    
    watch_dirs = args.dirs if args.dirs else None
    
    monitor = CodeMonitor(
        watch_dirs=watch_dirs,
        check_interval=args.interval
    )
    
    # Add simple logging callback
    def log_code_detected(file_path: str):
        logger.info(f"Code detected: {file_path}")
    
    monitor.on_code_detected(log_code_detected)
    
    try:
        monitor.start(use_watchdog=not args.no_watchdog)
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        monitor.stop()
        logger.info("CodeMonitor stopped by user")


if __name__ == "__main__":
    main()
