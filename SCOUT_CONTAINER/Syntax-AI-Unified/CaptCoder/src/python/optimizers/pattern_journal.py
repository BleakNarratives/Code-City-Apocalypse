"""
Syntax AI CaptCoder - Pattern Journal

Logging and journaling system for optimization activities.
Tracks all optimizations, scans, and code quality metrics over time.

Integrated from:
- /RootBase/syntax_captcoder/pattern_journal.json (concept)

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class JournalEntry:
    """A single entry in the Pattern Journal."""
    timestamp: float
    timestamp_human: str
    level: str
    module: str
    message: str
    data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert datetime to string if needed
        if isinstance(result.get('timestamp_human'), datetime):
            result['timestamp_human'] = result['timestamp_human'].isoformat()
        return result


class PatternJournal:
    """
    Pattern Journal for tracking optimization activities.
    
    Provides:
    - JSON-based logging
    - Search and filter capabilities
    - Statistics and metrics
    - Export/import functionality
    
    The journal tracks:
    - Optimization runs
    - Issues found
    - Fixes applied
    - Performance metrics
    - Code quality trends
    """
    
    def __init__(self, journal_path: str = "pattern_journal.json"):
        """
        Initialize the PatternJournal.
        
        Args:
            journal_path: Path to the journal file
        """
        self.journal_path = Path(journal_path)
        self.entries: List[JournalEntry] = []
        self._is_loaded = False
        
        # Load existing entries
        self.load()
    
    def load(self) -> bool:
        """
        Load entries from the journal file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if self.journal_path.exists():
                with open(self.journal_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                entry_dict = json.loads(line)
                                entry = self._dict_to_entry(entry_dict)
                                self.entries.append(entry)
                            except json.JSONDecodeError:
                                # Skip invalid lines
                                continue
                
                self._is_loaded = True
                logger.info(f"Loaded {len(self.entries)} entries from Pattern Journal")
                return True
        except Exception as e:
            logger.error(f"Error loading Pattern Journal: {e}")
            return False
        
        self._is_loaded = True
        return True
    
    def _dict_to_entry(self, entry_dict: Dict[str, Any]) -> JournalEntry:
        """Convert dictionary to JournalEntry."""
        return JournalEntry(
            timestamp=entry_dict.get('timestamp', time.time()),
            timestamp_human=entry_dict.get('timestamp_human', datetime.now().isoformat()),
            level=entry_dict.get('level', 'INFO'),
            module=entry_dict.get('module', 'unknown'),
            message=entry_dict.get('message', ''),
            data=entry_dict.get('data'),
            tags=entry_dict.get('tags')
        )
    
    def _entry_to_dict(self, entry: JournalEntry) -> Dict[str, Any]:
        """Convert JournalEntry to dictionary."""
        return entry.to_dict()
    
    def log(
        self,
        message: str,
        module: str = "CodeOptimizer",
        level: str = "INFO",
        data: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> JournalEntry:
        """
        Log an entry to the Pattern Journal.
        
        Args:
            message: The message to log
            module: The module/source of the message
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            data: Additional data to include
            tags: Tags for categorization
            
        Returns:
            The created JournalEntry
        """
        now = datetime.now()
        entry = JournalEntry(
            timestamp=time.time(),
            timestamp_human=now.isoformat(),
            level=level,
            module=module,
            message=message,
            data=data,
            tags=tags
        )
        
        self.entries.append(entry)
        
        # Write to file
        try:
            with open(self.journal_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(self._entry_to_dict(entry)) + '\n')
        except Exception as e:
            logger.error(f"Error writing to Pattern Journal: {e}")
        
        return entry
    
    def log_optimization_run(
        self,
        summary: Dict[str, Any],
        analyses: List[Dict[str, Any]],
        optimizations: List[Dict[str, Any]]
    ) -> JournalEntry:
        """
        Log a complete optimization run.
        
        Args:
            summary: Summary statistics
            analyses: List of file analyses
            optimizations: List of optimizations applied
            
        Returns:
            The created JournalEntry
        """
        return self.log(
            message="Bitch work protocol completed",
            module="Syntax_AI_CodeOptimizer",
            level="INFO",
            data={
                "summary": summary,
                "files_analyzed": len(analyses),
                "optimizations": optimizations
            },
            tags=["optimization", "bitch-work", "scan"]
        )
    
    def log_code_issue(
        self,
        file_path: str,
        issue_type: str,
        details: Dict[str, Any],
        severity: str = "WARNING"
    ) -> JournalEntry:
        """
        Log a code issue found during analysis.
        
        Args:
            file_path: Path to the file with the issue
            issue_type: Type of issue (e.g., "long_function")
            details: Details about the issue
            severity: Severity level (INFO, WARNING, ERROR)
            
        Returns:
            The created JournalEntry
        """
        return self.log(
            message=f"Code issue found: {issue_type}",
            module="CodeAnalyzer",
            level=severity,
            data={
                "file": file_path,
                "issue_type": issue_type,
                "details": details
            },
            tags=["issue", issue_type, "code-quality"]
        )
    
    def log_fix_applied(
        self,
        file_path: str,
        fix_type: str,
        details: Dict[str, Any]
    ) -> JournalEntry:
        """
        Log a fix that was applied.
        
        Args:
            file_path: Path to the file that was fixed
            fix_type: Type of fix applied
            details: Details about the fix
            
        Returns:
            The created JournalEntry
        """
        return self.log(
            message=f"Fix applied: {fix_type}",
            module="CodeOptimizer",
            level="INFO",
            data={
                "file": file_path,
                "fix_type": fix_type,
                "details": details
            },
            tags=["fix", fix_type, "optimization"]
        )
    
    def log_bsm_session(
        self,
        action: str,
        details: Dict[str, Any]
    ) -> JournalEntry:
        """
        Log a Blue Sky Meeting session event.
        
        Args:
            action: Action (started, ended, code_extracted, etc.)
            details: Details about the event
            
        Returns:
            The created JournalEntry
        """
        return self.log(
            message=f"BSM session: {action}",
            module="BSM_Monitor",
            level="INFO",
            data={"action": action, **details},
            tags=["bsm", action]
        )
    
    def log_code_extraction(
        self,
        source: str,
        code: str,
        language: str = "unknown"
    ) -> JournalEntry:
        """
        Log a code extraction event.
        
        Args:
            source: Source of the extracted code
            code: The extracted code (truncated if long)
            language: Detected language
            
        Returns:
            The created JournalEntry
        """
        # Truncate code for logging
        code_preview = code[:100] + "..." if len(code) > 100 else code
        
        return self.log(
            message="Code extracted",
            module="CodeExtractor",
            level="INFO",
            data={
                "source": source,
                "language": language,
                "code_preview": code_preview,
                "code_length": len(code)
            },
            tags=["extraction", "code", language]
        )
    
    def search(
        self,
        module: Optional[str] = None,
        level: Optional[str] = None,
        tags: Optional[List[str]] = None,
        message: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[JournalEntry]:
        """
        Search journal entries.
        
        Args:
            module: Filter by module
            level: Filter by level
            tags: Filter by tags (all must match)
            message: Filter by message (substring)
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)
            
        Returns:
            List of matching entries
        """
        results = []
        
        for entry in self.entries:
            # Check module
            if module and entry.module != module:
                continue
            
            # Check level
            if level and entry.level != level:
                continue
            
            # Check tags
            if tags and entry.tags:
                if not all(tag in entry.tags for tag in tags):
                    continue
            elif tags:
                # No tags in entry but we're searching for tags
                continue
            
            # Check message
            if message and message.lower() not in entry.message.lower():
                continue
            
            # Check date range
            if start_date:
                try:
                    start = datetime.fromisoformat(start_date)
                    entry_time = datetime.fromisoformat(entry.timestamp_human)
                    if entry_time < start:
                        continue
                except:
                    pass
            
            if end_date:
                try:
                    end = datetime.fromisoformat(end_date)
                    entry_time = datetime.fromisoformat(entry.timestamp_human)
                    if entry_time > end:
                        continue
                except:
                    pass
            
            results.append(entry)
        
        return results
    
    def get_recent(self, count: int = 10) -> List[JournalEntry]:
        """
        Get most recent entries.
        
        Args:
            count: Number of entries to return
            
        Returns:
            List of recent entries
        """
        return self.entries[-count:] if count <= len(self.entries) else self.entries.copy()
    
    def get_by_date(self, date: str) -> List[JournalEntry]:
        """
        Get entries for a specific date.
        
        Args:
            date: Date in ISO format (YYYY-MM-DD)
            
        Returns:
            List of entries for that date
        """
        results = []
        for entry in self.entries:
            if entry.timestamp_human.startswith(date):
                results.append(entry)
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics from the journal.
        
        Returns:
            Dictionary with various statistics
        """
        stats: Dict[str, Any] = {
            "total_entries": len(self.entries),
            "by_level": {},
            "by_module": {},
            "by_tags": {},
            "timeline": {}
        }
        
        for entry in self.entries:
            # Count by level
            stats["by_level"][entry.level] = stats["by_level"].get(entry.level, 0) + 1
            
            # Count by module
            stats["by_module"][entry.module] = stats["by_module"].get(entry.module, 0) + 1
            
            # Count by tags
            if entry.tags:
                for tag in entry.tags:
                    stats["by_tags"][tag] = stats["by_tags"].get(tag, 0) + 1
            
            # Timeline by date
            date = entry.timestamp_human.split('T')[0]
            stats["timeline"][date] = stats["timeline"].get(date, 0) + 1
        
        return stats
    
    def get_code_quality_trends(self) -> Dict[str, Any]:
        """
        Get code quality trends from optimization entries.
        
        Returns:
            Dictionary with quality trend data
        """
        trends: Dict[str, Any] = {
            "issues_by_type": {},
            "fixes_by_type": {},
            "files_over_time": []
        }
        
        for entry in self.entries:
            if entry.module == "Syntax_AI_CodeOptimizer" and entry.data:
                data = entry.data
                if "summary" in data:
                    summary = data["summary"]
                    trends["files_over_time"].append({
                        "date": entry.timestamp_human.split('T')[0],
                        "files_scanned": summary.get("files_scanned", 0),
                        "files_with_issues": summary.get("files_with_issues", 0),
                        "total_issues": summary.get("total_issues_found", 0)
                    })
                
                if "optimizations" in data:
                    for opt in data["optimizations"]:
                        for fix in opt.get("fixes_applied", []):
                            trends["fixes_by_type"][fix] = trends["fixes_by_type"].get(fix, 0) + 1
        
        return trends
    
    def export_json(self, output_path: Optional[str] = None) -> bool:
        """
        Export the journal to a JSON file.
        
        Args:
            output_path: Path to export to (defaults to journal_path)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(output_path or self.journal_path)
            with open(path, 'w', encoding='utf-8') as f:
                for entry in self.entries:
                    f.write(json.dumps(self._entry_to_dict(entry)) + '\n')
            return True
        except Exception as e:
            logger.error(f"Error exporting Pattern Journal: {e}")
            return False
    
    def clear(self) -> None:
        """Clear all entries from memory and file."""
        self.entries = []
        try:
            with open(self.journal_path, 'w', encoding='utf-8') as f:
                pass  # Empty file
        except Exception as e:
            logger.error(f"Error clearing Pattern Journal: {e}")
    
    def rotate(self, max_size: int = 10000, max_files: int = 5) -> None:
        """
        Rotate journal files to prevent them from growing too large.
        
        Args:
            max_size: Maximum size in bytes before rotation
            max_files: Maximum number of rotated files to keep
        """
        try:
            if self.journal_path.exists():
                size = self.journal_path.stat().st_size
                if size > max_size:
                    # Rotate files
                    for i in range(max_files - 1, 0, -1):
                        old_path = self.journal_path.with_suffix(f".{i}")
                        new_path = self.journal_path.with_suffix(f".{i+1}")
                        if old_path.exists():
                            if i + 1 == max_files:
                                old_path.unlink()  # Delete oldest
                            else:
                                old_path.rename(new_path)
                    
                    # Rename current to .1
                    self.journal_path.rename(self.journal_path.with_suffix(".1"))
                    
                    # Reload entries (current file is now empty)
                    self.entries = []
                    self._is_loaded = False
                    self.load()
        except Exception as e:
            logger.error(f"Error rotating Pattern Journal: {e}")
    
    def __len__(self) -> int:
        """Return number of entries."""
        return len(self.entries)
    
    def __iter__(self):
        """Iterate over entries."""
        return iter(self.entries)
    
    def __getitem__(self, index: int) -> JournalEntry:
        """Get entry by index."""
        return self.entries[index]


def main():
    """Test Pattern Journal functionality."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pattern Journal - Manage optimization logs"
    )
    parser.add_argument(
        "--view",
        action="store_true",
        help="View recent entries"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics"
    )
    parser.add_argument(
        "--search",
        nargs="+",
        help="Search for entries"
    )
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="Rotate journal files"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all entries"
    )
    args = parser.parse_args()
    
    journal = PatternJournal()
    
    if args.view:
        entries = journal.get_recent(20)
        for entry in entries:
            print(f"[{entry.timestamp_human}] {entry.level:8} {entry.module}: {entry.message}")
    
    elif args.stats:
        stats = journal.get_statistics()
        print("Pattern Journal Statistics:")
        print(f"  Total entries: {stats['total_entries']}")
        print(f"  By level: {stats['by_level']}")
        print(f"  By module: {stats['by_module']}")
        print(f"  By tags: {stats['by_tags']}")
    
    elif args.search:
        results = journal.search(message=" ".join(args.search))
        print(f"Found {len(results)} matching entries:")
        for entry in results:
            print(f"  [{entry.timestamp_human}] {entry.module}: {entry.message}")
    
    elif args.rotate:
        journal.rotate()
        print("Journal rotated")
    
    elif args.clear:
        journal.clear()
        print("Journal cleared")
    else:
        # Default: show recent entries
        entries = journal.get_recent(10)
        print(f"Recent Pattern Journal entries ({len(journal)} total):")
        for entry in entries:
            print(f"  [{entry.timestamp_human}] {entry.level:8} {entry.module}: {entry.message}")


if __name__ == "__main__":
    main()
