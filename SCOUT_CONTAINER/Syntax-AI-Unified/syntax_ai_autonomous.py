"""
FILENAME: syntax_ai_autonomous.py

Syntax AI - Autonomous Code Optimizer with Idle Detection
Part of the ModMind/EquiNex Universal Dashboard
Watches for user idle state and performs automated code maintenance

Project: Divine Gambit / ModMind MVP
Module: Syntax AI - "Bitch Work" Protocol + Autonomous Mode
"""

import os
import ast
import re
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class OptimizationResult:
    """Tracks what was optimized and why"""
    file_path: str
    optimization_type: str
    issues_found: List[str]
    fixes_applied: List[str]
    lines_changed: int
    timestamp: str
    confidence: float


class IdleDetector:
    """
    Detects when user is idle but present
    Monitors file modification times to determine activity
    """
    
    def __init__(self, project_root: str = ".", idle_threshold: int = 300):
        self.project_root = Path(project_root)
        self.idle_threshold = idle_threshold  # seconds
        self.last_activity = time.time()
        self.watching = False
        self.watch_thread = None
        
    def update_activity(self):
        """Mark that user activity was detected"""
        self.last_activity = time.time()
    
    def is_idle(self) -> bool:
        """Check if user has been idle long enough"""
        idle_time = time.time() - self.last_activity
        return idle_time >= self.idle_threshold
    
    def start_watching(self):
        """Start monitoring for file changes"""
        self.watching = True
        self.watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()
        logging.info(f"👁️  Idle detection started (threshold: {self.idle_threshold}s)")
    
    def stop_watching(self):
        """Stop monitoring"""
        self.watching = False
        if self.watch_thread:
            self.watch_thread.join(timeout=1)
    
    def _watch_loop(self):
        """Monitor file modifications in background"""
        last_check_times = {}
        
        while self.watching:
            try:
                # Check Python files for modifications
                for py_file in self.project_root.rglob('*.py'):
                    if any(x in str(py_file) for x in ['venv', '.venv', '__pycache__']):
                        continue
                    
                    try:
                        mtime = py_file.stat().st_mtime
                        
                        # If file was modified, mark activity
                        if py_file in last_check_times:
                            if mtime > last_check_times[py_file]:
                                self.update_activity()
                        
                        last_check_times[py_file] = mtime
                        
                    except (OSError, PermissionError):
                        continue
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logging.info(f"⚠️  Idle detector error: {e}")
                time.sleep(10)


class CodeOptimizer:
    """
    Autonomous code optimization engine
    Scans Python files, identifies issues, applies fixes
    """
    
    def __init__(self, project_root: str = ".", log_file: str = "pattern_journal.json"):
        self.project_root = Path(project_root)
        self.log_file = log_file
        self.optimizations_performed = []
        
        self.rules = {
            "long_functions": 50,
            "missing_docstrings": True,
            "unused_imports": True,
            "print_statements": True,
            "inconsistent_naming": True,
            "magic_numbers": True,
            "no_type_hints": True
        }
        
    def scan_project(self, exclude_dirs: Optional[List[str]] = None) -> List[Path]:
        """Find all Python files in project"""
        if exclude_dirs is None:
            exclude_dirs = ['venv', '.venv', '__pycache__', '.git', 'node_modules']
        
        python_files = []
        for path in self.project_root.rglob('*.py'):
            if any(excluded in str(path) for excluded in exclude_dirs):
                continue
            python_files.append(path)
        
        self.log(f"Found {len(python_files)} Python files to scan")
        return python_files
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file for optimization opportunities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            issues = {
                "long_functions": [],
                "missing_docstrings": [],
                "unused_imports": [],
                "print_statements": [],
                "magic_numbers": [],
                "no_type_hints": []
            }
            
            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_length = node.end_lineno - node.lineno
                    if func_length > self.rules["long_functions"]:
                        issues["long_functions"].append({
                            "name": node.name,
                            "length": func_length,
                            "line": node.lineno
                        })
                    
                    # Check for missing docstrings
                    if self.rules["missing_docstrings"]:
                        if not ast.get_docstring(node):
                            issues["missing_docstrings"].append({
                                "name": node.name,
                                "line": node.lineno
                            })
                    
                    # Check for type hints
                    if self.rules["no_type_hints"]:
                        if not node.returns and node.name != "__init__":
                            issues["no_type_hints"].append({
                                "name": node.name,
                                "line": node.lineno,
                                "hint": "return type"
                            })
                
                # Check for print statements
                if self.rules["print_statements"]:
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'print':
                            issues["print_statements"].append({
                                "line": node.lineno
                            })
                
                # Check for magic numbers
                if self.rules["magic_numbers"]:
                    if isinstance(node, ast.Num) and not isinstance(node.n, bool):
                        if node.n not in [0, 1, -1, 2, 10, 100]:
                            issues["magic_numbers"].append({
                                "value": node.n,
                                "line": node.lineno
                            })
            
            return {
                "file_path": str(file_path),
                "issues": issues,
                "total_issues": sum(len(v) for v in issues.values()),
                "lines": len(content.split('\n'))
            }
            
        except SyntaxError as e:
            self.log(f"Syntax error in {file_path}: {e}", level="ERROR")
            return {"file_path": str(file_path), "error": str(e)}
        except Exception as e:
            self.log(f"Error analyzing {file_path}: {e}", level="ERROR")
            return {"file_path": str(file_path), "error": str(e)}
    
    def optimize_file(self, file_path: Path, analysis: Dict[str, Any]) -> OptimizationResult:
        """Apply automated optimizations to a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        modified_content = original_content
        fixes_applied = []
        issues_found = []
        
        # Fix 1: Replace print statements with logging
        if analysis["issues"]["print_statements"]:
            print_count = len(analysis["issues"]["print_statements"])
            issues_found.append(f"{print_count} print statements")
            
            if 'import logging' not in modified_content:
                modified_content = 'import logging\n\n' + modified_content
                fixes_applied.append("Added logging import")
            
            modified_content = re.sub(
                r'print\((.*?)\)',
                r'logging.info(\1)',
                modified_content
            )
            fixes_applied.append(f"Converted {print_count} prints to logging")
        
        # Fix 2: Flag missing docstrings
        if analysis["issues"]["missing_docstrings"]:
            missing_count = len(analysis["issues"]["missing_docstrings"])
            issues_found.append(f"{missing_count} missing docstrings")
            fixes_applied.append(f"Flagged {missing_count} functions for docstrings")
        
        # Fix 3: Flag magic numbers
        if analysis["issues"]["magic_numbers"]:
            magic_count = len(analysis["issues"]["magic_numbers"])
            issues_found.append(f"{magic_count} magic numbers")
            fixes_applied.append(f"Identified {magic_count} magic numbers for constants")
        
        # Calculate lines changed
        original_lines = original_content.split('\n')
        modified_lines = modified_content.split('\n')
        lines_changed = sum(1 for a, b in zip(original_lines, modified_lines) if a != b)
        
        # Only write if changes were made
        if modified_content != original_content:
            backup_path = file_path.with_suffix('.py.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            self.log(f"Optimized {file_path.name}: {len(fixes_applied)} fixes applied")
        
        result = OptimizationResult(
            file_path=str(file_path),
            optimization_type="automatic",
            issues_found=issues_found,
            fixes_applied=fixes_applied,
            lines_changed=lines_changed,
            timestamp=datetime.now().isoformat(),
            confidence=0.8
        )
        
        self.optimizations_performed.append(result)
        return result
    
    def run_bitch_work(self, auto_fix: bool = False) -> Dict[str, Any]:
        """Main autonomous optimization routine"""
        self.log("🤖 Syntax AI: Starting bitch work protocol...")
        
        start_time = time.time()
        files = self.scan_project()
        
        all_analyses = []
        all_optimizations = []
        
        for file_path in files:
            analysis = self.analyze_file(file_path)
            
            if "error" not in analysis and analysis["total_issues"] > 0:
                all_analyses.append(analysis)
                
                if auto_fix:
                    optimization = self.optimize_file(file_path, analysis)
                    all_optimizations.append(optimization)
        
        elapsed_time = time.time() - start_time
        
        summary = {
            "files_scanned": len(files),
            "files_with_issues": len(all_analyses),
            "files_optimized": len(all_optimizations),
            "total_issues_found": sum(a["total_issues"] for a in all_analyses),
            "total_fixes_applied": sum(len(o.fixes_applied) for o in all_optimizations),
            "elapsed_time": round(elapsed_time, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        self.log(f"✅ Bitch work complete: {summary['files_with_issues']} files analyzed")
        self.log_to_pattern_journal(summary, all_analyses, all_optimizations)
        
        return summary
    
    def generate_optimization_report(self) -> str:
        """Generate a human-readable report"""
        if not self.optimizations_performed:
            return "No optimizations performed yet."
        
        report = "# Syntax AI Optimization Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Total Optimizations: {len(self.optimizations_performed)}\n\n"
        
        for opt in self.optimizations_performed:
            report += f"## {Path(opt.file_path).name}\n"
            report += f"**Issues Found:** {', '.join(opt.issues_found)}\n"
            report += f"**Fixes Applied:** {', '.join(opt.fixes_applied)}\n"
            report += f"**Lines Changed:** {opt.lines_changed}\n"
            report += f"**Confidence:** {opt.confidence * 100:.0f}%\n\n"
        
        return report
    
    def log(self, message: str, level: str = "INFO"):
        """Simple console logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = {"INFO": "ℹ️", "ERROR": "❌", "WARNING": "⚠️", "DEBUG": "🔍"}.get(level, "📝")
        logging.info(f"{emoji} [{timestamp}] {message}")
    
    def log_to_pattern_journal(self, summary: Dict, analyses: List, optimizations: List):
        """Log optimization session to Pattern Journal"""
        try:
            entry = {
                "timestamp": time.time(),
                "timestamp_human": datetime.now().isoformat(),
                "level": "INFO",
                "module": "Syntax_AI_CodeOptimizer",
                "message": "Bitch work protocol completed",
                "data": {
                    "summary": summary,
                    "files_analyzed": len(analyses),
                    "optimizations": [asdict(opt) for opt in optimizations]
                }
            }
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
                
        except Exception as e:
            self.log(f"Failed to log to Pattern Journal: {e}", level="ERROR")


class AutonomousSyntaxAI:
    """
    Autonomous mode: watches for idle state and runs optimizations automatically
    """
    
    def __init__(self, project_root: str = ".", idle_threshold: int = 300):
        self.optimizer = CodeOptimizer(project_root)
        self.idle_detector = IdleDetector(project_root, idle_threshold)
        self.running = False
        self.last_optimization = 0
        self.optimization_cooldown = 600  # Don't optimize more than once per 10 minutes
        
    def start(self):
        """Start autonomous monitoring"""
        logging.info("🧠 Syntax AI - Autonomous Mode ACTIVATED")
        logging.info(f"   Idle threshold: {self.idle_detector.idle_threshold}s")
        logging.info(f"   Optimization cooldown: {self.optimization_cooldown}s")
        logging.info("   Monitoring for idle state...\n")
        
        self.running = True
        self.idle_detector.start_watching()
        
        try:
            while self.running:
                if self.idle_detector.is_idle():
                    # Check if enough time has passed since last optimization
                    time_since_last = time.time() - self.last_optimization
                    
                    if time_since_last >= self.optimization_cooldown:
                        logging.info("\n⏸️  User idle detected - starting autonomous optimization...")
                        
                        summary = self.optimizer.run_bitch_work(auto_fix=True)
                        
                        logging.info("\n📊 Autonomous Optimization Complete:")
                        logging.info(f"   Files scanned: {summary['files_scanned']}")
                        logging.info(f"   Issues found: {summary['total_issues_found']}")
                        logging.info(f"   Fixes applied: {summary['total_fixes_applied']}")
                        logging.info(f"   Time taken: {summary['elapsed_time']}s")
                        
                        # Generate report
                        report = self.optimizer.generate_optimization_report()
                        report_path = Path(f"syntax_ai_report_{int(time.time())}.md")
                        report_path.write_text(report)
                        logging.info(f"   Report: {report_path}\n")
                        
                        self.last_optimization = time.time()
                        
                        # Reset idle timer after optimization
                        self.idle_detector.update_activity()
                
                time.sleep(10)  # Check idle state every 10 seconds
                
        except KeyboardInterrupt:
            logging.info("\n🛑 Autonomous mode stopped by user")
            self.stop()
    
    def stop(self):
        """Stop autonomous monitoring"""
        self.running = False
        self.idle_detector.stop_watching()
        logging.info("✅ Syntax AI autonomous mode stopped")


def main():
    """Run Syntax AI with mode selection"""
    logging.info("🤖 Syntax AI - Autonomous Code Optimizer")
    logging.info("=" * 50)
    logging.info("\nSelect mode:")
    logging.info("  1) Manual scan (safe - no changes)")
    logging.info("  2) Manual optimize (with backups)")
    logging.info("  3) Autonomous mode (auto-optimize when idle)")
    logging.info()
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            # Manual scan only
            logging.info("\n📊 Running manual scan...")
            optimizer = CodeOptimizer(project_root=".")
            summary = optimizer.run_bitch_work(auto_fix=False)
            
            logging.info("\n" + "=" * 50)
            logging.info("📈 Summary:")
            logging.info(f"   Files scanned: {summary['files_scanned']}")
            logging.info(f"   Issues found: {summary['total_issues_found']}")
            logging.info(f"   Time taken: {summary['elapsed_time']}s")
            
            report = optimizer.generate_optimization_report()
            report_path = Path("syntax_ai_report.md")
            report_path.write_text(report)
            logging.info(f"\n📄 Report saved to: {report_path}")
            
        elif choice == "2":
            # Manual optimize
            logging.info("\n🔧 Running manual optimization...")
            logging.info("⚠️  This will modify files (backups created as .py.bak)")
            confirm = input("Continue? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                optimizer = CodeOptimizer(project_root=".")
                summary = optimizer.run_bitch_work(auto_fix=True)
                
                logging.info("\n" + "=" * 50)
                logging.info("📈 Summary:")
                logging.info(f"   Files optimized: {summary['files_optimized']}")
                logging.info(f"   Fixes applied: {summary['total_fixes_applied']}")
                logging.info(f"   Time taken: {summary['elapsed_time']}s")
                
                report = optimizer.generate_optimization_report()
                report_path = Path("syntax_ai_report.md")
                report_path.write_text(report)
                logging.info(f"\n📄 Report saved to: {report_path}")
            else:
                logging.info("❌ Cancelled")
                
        elif choice == "3":
            # Autonomous mode
            logging.info("\n🧠 Starting autonomous mode...")
            logging.info("   Press Ctrl+C to stop\n")
            
            autonomous = AutonomousSyntaxAI(project_root=".", idle_threshold=300)
            autonomous.start()
            
        else:
            logging.info("❌ Invalid choice")
            
    except KeyboardInterrupt:
        logging.info("\n\n🛑 Stopped by user")
    except Exception as e:
        logging.info(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()