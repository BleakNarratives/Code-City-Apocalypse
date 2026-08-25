import time
import fnmatch
import os
from pathlib import Path
from typing import List, Callable, Dict

from truthsleuth.config import ROOT_DIR, EXCLUSION_PATTERNS, MONITORED_PATHS

# Store last modification times of monitored files
_file_timestamps: Dict[Path, float] = {}
_monitoring_active: bool = False

def _is_excluded(path: Path) -> bool:
    """Checks if a given path should be excluded based on EXCLUSION_PATTERNS."""
    try:
        relative_path = path.relative_to(ROOT_DIR)
    except ValueError:
        # Path is not within ROOT_DIR, so it's effectively excluded for relative pattern matching
        return True 
    for pattern in EXCLUSION_PATTERNS:
        if fnmatch.fnmatch(str(relative_path), pattern):
            return True
    return False

def get_all_monitored_files() -> List[Path]:
    """Returns a list of all files to be monitored, respecting inclusions and exclusions."""
    monitored_files = []
    # If MONITORED_PATHS is empty, monitor the entire ROOT_DIR
    search_paths = [ROOT_DIR] if not MONITORED_PATHS else [ROOT_DIR / p for p in MONITORED_PATHS]

    for base_path in search_paths:
        if not base_path.exists():
            print(f"Monitor: Warning: Monitored path does not exist: {base_path}")
            continue
        for file_path in base_path.rglob("*"):
            if file_path.is_file() and not _is_excluded(file_path):
                monitored_files.append(file_path)
    return monitored_files

def _initial_scan():
    """Performs an initial scan to populate file timestamps."""
    print("Monitor: Performing initial file system scan...")
    global _file_timestamps
    _file_timestamps = {}
    for file_path in get_all_monitored_files():
        try:
            _file_timestamps[file_path] = file_path.stat().st_mtime
        except FileNotFoundError:
            # File might have been deleted between get_all_monitored_files and stat() call
            continue
    print(f"Monitor: Initial scan complete. Tracking {len(_file_timestamps)} files.")

def scan_for_changes() -> List[Path]:
    """Scans the file system for new or modified files and returns a list of changed paths."""
    changed_files = []
    current_monitored_files = set(get_all_monitored_files())
    
    # Check for modified or new files
    for file_path in current_monitored_files:
        try:
            current_mtime = file_path.stat().st_mtime
            if file_path not in _file_timestamps or _file_timestamps[file_path] < current_mtime:
                changed_files.append(file_path)
                _file_timestamps[file_path] = current_mtime # Update timestamp
        except FileNotFoundError:
            # File might have been deleted since the current_monitored_files list was created
            # This case is handled implicitly as it won't be in _file_timestamps and won't be re-added if deleted.
            pass
            
    # Clean up _file_timestamps for deleted files (optional, but good for accuracy)
    # This finds files that were tracked but no longer exist
    deleted_files = [path for path in _file_timestamps if path not in current_monitored_files]
    for path in deleted_files:
        del _file_timestamps[path]

    return changed_files

def start_monitoring(interval_seconds: int, on_change_callback: Callable[[Path], None]):
    """
    Starts continuous file system monitoring.
    Args:
        interval_seconds: How often to scan for changes (in seconds).
        on_change_callback: A function to call with the Path of each changed file.
    """
    global _monitoring_active
    _monitoring_active = True
    _initial_scan() # Populate initial state

    print(f"Monitor: Starting continuous monitoring every {interval_seconds} seconds...")
    while _monitoring_active:
        changes = scan_for_changes()
        if changes:
            print(f"Monitor: Detected {len(changes)} changes.")
            for changed_file in changes:
                on_change_callback(changed_file)
        time.sleep(interval_seconds)
    print("Monitor: Monitoring stopped.")

def stop_monitoring():
    """Stops the continuous file system monitoring."""
    global _monitoring_active
    _monitoring_active = False
    print("Monitor: Signaling monitoring to stop.")
