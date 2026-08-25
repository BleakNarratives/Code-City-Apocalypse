"""
Syntax AI CaptCoder - Code Optimizer

Autonomous code optimization engine implementing the "Bitch Work" protocol.
Scans Python files, identifies issues, and applies fixes automatically.

Integrated from:
- /RootBase/syntax_captcoder/syntax_ai_code_optimizer_core.py

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import ast
import re
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Union
from dataclasses import dataclass, asdict

from ..utils.file_utils import FileUtils
from ..utils.text_utils import TextUtils

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Tracks what was optimized and why."""
    file_path: str
    optimization_type: str
    issues_found: List[str]
    fixes_applied: List[str]
    lines_changed: int
    timestamp: str
    confidence: float  # 0-1 score
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScanResult:
    """Result of scanning a file for issues."""
    file_path: str
    issues: Dict[str, List[Dict[str, Any]]]
    total_issues: int
    lines: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'file_path': self.file_path,
            'issues': self.issues,
            'total_issues': self.total_issues,
            'lines': self.lines
        }


class CodeOptimizer:
    """
    Autonomous code optimization engine.
    
    Implements the "Bitch Work" protocol:
    - Scans entire project for optimization opportunities
    - Identifies issues (long functions, missing docstrings, etc.)
    - Optionally applies automated fixes
    - Logs everything to Pattern Journal
    
    Features:
    - AST-based code analysis
    - Multiple optimization rules
    - Configurable thresholds
    - Backup creation before modifications
    - Pattern Journal integration
    """
    
    def __init__(
        self,
        project_root: Union[str, Path] = ".",
        log_file: str = "pattern_journal.json",
        auto_fix: bool = False,
        exclude_dirs: Optional[List[str]] = None,
        rules: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the CodeOptimizer.
        
        Args:
            project_root: Root directory of the project to scan
            log_file: Path to the Pattern Journal log file
            auto_fix: Whether to automatically apply fixes
            exclude_dirs: Directories to exclude from scanning
            rules: Custom optimization rules
        """
        self.project_root = Path(project_root)
        self.log_file = log_file
        self.auto_fix = auto_fix
        self.file_utils = FileUtils()
        self.text_utils = TextUtils()
        
        # Default exclude directories
        self.exclude_dirs = set(exclude_dirs or [
            'venv', '.venv', '__pycache__', '.git', 
            'node_modules', 'dist', '.vscode', '.idea', 'build'
        ])
        
        # Optimization rules with defaults
        self.rules = {
            "long_functions": 50,  # Max lines per function
            "missing_docstrings": True,
            "unused_imports": True,
            "print_statements": True,  # Convert to logging
            "inconsistent_naming": True,
            "magic_numbers": True,
            "no_type_hints": True,
            "trailing_whitespace": True,
            "mixed_tabs_spaces": True,
            "missing_newline": True
        }
        
        if rules:
            self.rules.update(rules)
        
        # State
        self.optimizations_performed: List[OptimizationResult] = []
        self.scan_results: List[ScanResult] = []
        
        # Statistics
        self.stats = {
            "files_scanned": 0,
            "files_with_issues": 0,
            "files_optimized": 0,
            "total_issues_found": 0,
            "total_fixes_applied": 0,
            "elapsed_time": 0.0,
            "started_at": None
        }
        
        logger.info(f"CodeOptimizer initialized for: {self.project_root}")
    
    def scan_project(self, exclude_dirs: Optional[List[str]] = None) -> List[Path]:
        """
        Find all Python files in the project.
        
        Args:
            exclude_dirs: Additional directories to exclude
            
        Returns:
            List of Path objects for Python files
        """
        exclude = self.exclude_dirs.union(set(exclude_dirs or []))
        python_files: List[Path] = []
        
        for path in self.project_root.rglob('*.py'):
            # Skip excluded directories
            if any(excluded in str(path) for excluded in exclude):
                continue
            python_files.append(path)
        
        logger.info(f"Found {len(python_files)} Python files to scan")
        self.stats["files_scanned"] = len(python_files)
        return python_files
    
    def analyze_file(self, file_path: Path) -> ScanResult:
        """
        Analyze a single Python file for optimization opportunities.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            ScanResult with issues found
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            issues: Dict[str, List[Dict[str, Any]]] = {
                "long_functions": [],
                "missing_docstrings": [],
                "unused_imports": [],
                "print_statements": [],
                "magic_numbers": [],
                "no_type_hints": [],
                "trailing_whitespace": [],
                "mixed_tabs_spaces": [],
                "missing_newline": []
            }
            
            # Check for long functions
            if self.rules["long_functions"]:
                self._check_long_functions(tree, issues)
            
            # Check for missing docstrings
            if self.rules["missing_docstrings"]:
                self._check_missing_docstrings(tree, issues)
            
            # Check for unused imports (requires more complex analysis)
            if self.rules["unused_imports"]:
                self._check_imports(tree, content, issues)
            
            # Check for print statements
            if self.rules["print_statements"]:
                self._check_print_statements(tree, issues)
            
            # Check for magic numbers
            if self.rules["magic_numbers"]:
                self._check_magic_numbers(tree, issues)
            
            # Check for type hints
            if self.rules["no_type_hints"]:
                self._check_type_hints(tree, issues)
            
            # Check for trailing whitespace
            if self.rules["trailing_whitespace"]:
                self._check_trailing_whitespace(content, issues)
            
            # Check for mixed tabs and spaces
            if self.rules["mixed_tabs_spaces"]:
                self._check_mixed_indentation(content, issues)
            
            # Check for missing newline at end of file
            if self.rules["missing_newline"]:
                self._check_missing_newline(content, issues, str(file_path))
            
            total_issues = sum(len(v) for v in issues.values())
            
            return ScanResult(
                file_path=str(file_path),
                issues=issues,
                total_issues=total_issues,
                lines=len(content.split('\n'))
            )
            
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            return ScanResult(
                file_path=str(file_path),
                issues={"syntax_error": [{"error": str(e), "line": e.lineno}]},
                total_issues=1,
                lines=0
            )
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return ScanResult(
                file_path=str(file_path),
                issues={"error": [{"error": str(e)}]},
                total_issues=1,
                lines=0
            )
    
    def _check_long_functions(self, tree: ast.AST, issues: Dict[str, List]) -> None:
        """Check for functions that are too long."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_length = node.end_lineno - node.lineno
                if func_length > self.rules["long_functions"]:
                    issues["long_functions"].append({
                        "name": node.name,
                        "length": func_length,
                        "line": node.lineno,
                        "suggestion": f"Refactor function to be under {self.rules['long_functions']} lines"
                    })
    
    def _check_missing_docstrings(self, tree: ast.AST, issues: Dict[str, List]) -> None:
        """Check for missing docstrings."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    issues["missing_docstrings"].append({
                        "name": node.name,
                        "type": type(node).__name__,
                        "line": node.lineno,
                        "suggestion": "Add docstring"
                    })
    
    def _check_imports(self, tree: ast.AST, content: str, issues: Dict[str, List]) -> None:
        """Check for unused imports."""
        # Collect all imports
        imports: List[Dict[str, Any]] = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        'name': alias.name,
                        'asname': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        'name': alias.name,
                        'module': node.module,
                        'asname': alias.asname,
                        'line': node.lineno
                    })
        
        # Check if imports are used (simple check)
        for imp in imports:
            name = imp.get('asname') or imp.get('name').split('.')[-1]
            if name not in content:
                # Could be a false positive, but flag it
                issues["unused_imports"].append({
                    "import": imp.get('name', imp.get('module', 'unknown')),
                    "line": imp['line'],
                    "suggestion": "Remove unused import"
                })
    
    def _check_print_statements(self, tree: ast.AST, issues: Dict[str, List]) -> None:
        """Check for print statements."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == 'print':
                    issues["print_statements"].append({
                        "line": node.lineno,
                        "suggestion": "Convert to logging"
                    })
    
    def _check_magic_numbers(self, tree: ast.AST, issues: Dict[str, List]) -> None:
        """Check for magic numbers (hardcoded numeric literals)."""
        # Common safe numbers
        safe_numbers = {0, 1, -1, 2, 10, 100, 1000}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in safe_numbers:
                    issues["magic_numbers"].append({
                        "value": node.value,
                        "line": node.lineno,
                        "suggestion": "Define as named constant"
                    })
            elif isinstance(node, ast.Num) and not isinstance(node.n, bool):
                if node.n not in safe_numbers:
                    issues["magic_numbers"].append({
                        "value": node.n,
                        "line": node.lineno,
                        "suggestion": "Define as named constant"
                    })
    
    def _check_type_hints(self, tree: ast.AST, issues: Dict[str, List]) -> None:
        """Check for missing type hints."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check return type hint
                if not node.returns and node.name != "__init__":
                    issues["no_type_hints"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "type": "return",
                        "suggestion": "Add return type hint"
                    })
                
                # Check parameter type hints
                for arg in node.args.args:
                    if not arg.annotation and arg.arg != 'self':
                        issues["no_type_hints"].append({
                            "name": node.name,
                            "parameter": arg.arg,
                            "line": node.lineno,
                            "type": "parameter",
                            "suggestion": f"Add type hint for parameter '{arg.arg}'"
                        })
    
    def _check_trailing_whitespace(self, content: str, issues: Dict[str, List]) -> None:
        """Check for trailing whitespace on lines."""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                issues["trailing_whitespace"].append({
                    "line": i,
                    "suggestion": "Remove trailing whitespace"
                })
    
    def _check_mixed_indentation(self, content: str, issues: Dict[str, List]) -> None:
        """Check for mixed tabs and spaces."""
        lines = content.split('\n')
        has_tabs = False
        has_spaces = False
        
        for i, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if not stripped:
                continue
            
            leading = line[:len(line) - len(stripped)]
            if '\t' in leading:
                has_tabs = True
            if ' ' in leading:
                has_spaces = True
            
            if has_tabs and has_spaces:
                issues["mixed_tabs_spaces"].append({
                    "line": i,
                    "suggestion": "Use consistent indentation (spaces or tabs)"
                })
                break
    
    def _check_missing_newline(self, content: str, issues: Dict[str, List], file_path: str) -> None:
        """Check for missing newline at end of file."""
        if content and not content.endswith('\n'):
            issues["missing_newline"].append({
                "file": file_path,
                "suggestion": "Add newline at end of file"
            })
    
    def generate_docstring(self, func_name: str, func_node: ast.FunctionDef) -> str:
        """
        Generate a basic docstring for a function.
        
        Args:
            func_name: Name of the function
            func_node: AST node for the function
            
        Returns:
            Generated docstring
        """
        # Extract parameters
        params = [arg.arg for arg in func_node.args.args]
        
        # Basic template
        docstring = f'"""\n{func_name.replace("_", " ").title()}\n\n'
        
        if params:
            docstring += "Args:\n"
            for param in params:
                if param != 'self':
                    docstring += f"    {param}: Description needed\n"
        
        docstring += "\n"
        docstring += "Returns:\n"
        docstring += "    Description needed\n"
        docstring += '"""'
        
        return docstring
    
    def optimize_file(self, file_path: Path, analysis: ScanResult) -> OptimizationResult:
        """
        Apply automated optimizations to a file.
        
        Args:
            file_path: Path to the file to optimize
            analysis: ScanResult from analyze_file
            
        Returns:
            OptimizationResult with fixes applied
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        modified_content = original_content
        fixes_applied: List[str] = []
        issues_found: List[str] = []
        
        # Fix 1: Replace print statements with logging
        if analysis.issues.get("print_statements"):
            print_count = len(analysis.issues["print_statements"])
            issues_found.append(f"{print_count} print statements")
            
            # Add logging import if not present
            if 'import logging' not in modified_content:
                modified_content = 'import logging\n\n' + modified_content
                fixes_applied.append("Added logging import")
            
            # Replace print with logging
            modified_content = re.sub(
                r'print\((.*?)\)',
                r'logging.info(\1)',
                modified_content
            )
            fixes_applied.append(f"Converted {print_count} prints to logging.info()")
        
        # Fix 2: Add missing newline at end of file
        if analysis.issues.get("missing_newline"):
            if not modified_content.endswith('\n'):
                modified_content += '\n'
                fixes_applied.append("Added newline at end of file")
        
        # Fix 3: Remove trailing whitespace
        if analysis.issues.get("trailing_whitespace"):
            lines = modified_content.split('\n')
            modified_content = '\n'.join(line.rstrip() for line in lines)
            fixes_applied.append("Removed trailing whitespace")
        
        # Calculate lines changed
        original_lines = original_content.split('\n')
        modified_lines = modified_content.split('\n')
        lines_changed = sum(1 for a, b in zip(original_lines, modified_lines) if a != b)
        
        # Only write if changes were made
        if modified_content != original_content:
            # Create backup
            backup_path = file_path.with_suffix('.py.bak')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write optimized version
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            logger.info(f"Optimized {file_path.name}: {len(fixes_applied)} fixes applied")
        
        result = OptimizationResult(
            file_path=str(file_path),
            optimization_type="automatic",
            issues_found=issues_found,
            fixes_applied=fixes_applied,
            lines_changed=lines_changed,
            timestamp=datetime.now().isoformat(),
            confidence=0.8  # High confidence for simple fixes
        )
        
        self.optimizations_performed.append(result)
        return result
    
    def run_bitch_work(self, auto_fix: Optional[bool] = None) -> Dict[str, Any]:
        """
        Main autonomous optimization routine.
        
        Scans all files, identifies issues, optionally applies fixes.
        
        Args:
            auto_fix: Override the instance auto_fix setting
            
        Returns:
            Summary of optimization run
        """
        use_auto_fix = auto_fix if auto_fix is not None else self.auto_fix
        
        logger.info("🤖 Syntax AI: Starting bitch work protocol...")
        
        start_time = time.time()
        self.stats["started_at"] = datetime.now().isoformat()
        
        files = self.scan_project()
        
        all_analyses: List[ScanResult] = []
        all_optimizations: List[OptimizationResult] = []
        
        for file_path in files:
            analysis = self.analyze_file(file_path)
            
            if "error" not in analysis.issues and analysis.total_issues > 0:
                all_analyses.append(analysis)
                self.scan_results.append(analysis)
                
                if use_auto_fix:
                    optimization = self.optimize_file(file_path, analysis)
                    all_optimizations.append(optimization)
        
        elapsed_time = time.time() - start_time
        
        # Update statistics
        self.stats.update({
            "files_with_issues": len(all_analyses),
            "files_optimized": len(all_optimizations),
            "total_issues_found": sum(a.total_issues for a in all_analyses),
            "total_fixes_applied": sum(len(o.fixes_applied) for o in all_optimizations),
            "elapsed_time": round(elapsed_time, 2)
        })
        
        logger.info(f"✅ Bitch work complete: {self.stats['files_with_issues']} files need attention")
        
        # Log to Pattern Journal
        summary = self.stats.copy()
        self.log_to_pattern_journal(summary, all_analyses, all_optimizations)
        
        return summary
    
    def generate_optimization_report(self) -> str:
        """
        Generate a human-readable report of optimizations.
        
        Returns:
            Markdown-formatted report
        """
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
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Simple console logging."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji_map = {"INFO": "ℹ️", "ERROR": "❌", "WARNING": "⚠️", "DEBUG": "🔍"}
        emoji = emoji_map.get(level, "📝")
        logging.log(getattr(logging, level, logging.INFO), f"{emoji} [{timestamp}] {message}")
    
    def log_to_pattern_journal(
        self,
        summary: Dict,
        analyses: List[ScanResult],
        optimizations: List[OptimizationResult]
    ) -> None:
        """
        Log optimization session to Pattern Journal.
        
        Args:
            summary: Summary statistics
            analyses: List of scan results
            optimizations: List of optimization results
        """
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
                    "optimizations": [opt.to_dict() for opt in optimizations]
                }
            }
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
                
        except Exception as e:
            self.log(f"Failed to log to Pattern Journal: {e}", level="ERROR")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "files_scanned": 0,
            "files_with_issues": 0,
            "files_optimized": 0,
            "total_issues_found": 0,
            "total_fixes_applied": 0,
            "elapsed_time": 0.0,
            "started_at": None
        }


def main():
    """Run Syntax AI Code Optimizer."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Syntax AI - Code Optimizer (Bitch Work Protocol)"
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Run analysis only, no fixes"
    )
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="Apply automated fixes"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate optimization report"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory to scan"
    )
    args = parser.parse_args()
    
    logger.info("🤖 Syntax AI - Code Optimizer")
    logger.info("=" * 50)
    
    optimizer = CodeOptimizer(
        project_root=args.project_root,
        auto_fix=args.auto_fix
    )
    
    # Run analysis or optimization
    if args.scan_only:
        logger.info("\n📊 Running code analysis...")
        summary = optimizer.run_bitch_work(auto_fix=False)
    else:
        logger.info("\n🔧 Running bitch work protocol...")
        summary = optimizer.run_bitch_work(auto_fix=args.auto_fix)
    
    logger.info("\n" + "=" * 50)
    logger.info("📈 Summary:")
    logger.info(f"   Files scanned: {summary['files_scanned']}")
    logger.info(f"   Issues found: {summary['total_issues_found']}")
    logger.info(f"   Files optimized: {summary['files_optimized']}")
    logger.info(f"   Fixes applied: {summary['total_fixes_applied']}")
    logger.info(f"   Time taken: {summary['elapsed_time']}s")
    
    # Generate report if requested
    if args.report:
        report = optimizer.generate_optimization_report()
        report_path = Path("syntax_ai_report.md")
        report_path.write_text(report)
        logger.info(f"\n📄 Report saved to: {report_path}")
    
    # Ask for confirmation before auto-fixing (if not already done)
    if summary['files_with_issues'] > 0 and not args.auto_fix and not args.scan_only:
        logger.info("\n⚠️  Found issues that can be auto-fixed.")
        logger.info("   Run with --auto-fix to apply automated optimizations.")
        logger.info("   (Backups will be created as .py.bak)")


if __name__ == "__main__":
    main()
