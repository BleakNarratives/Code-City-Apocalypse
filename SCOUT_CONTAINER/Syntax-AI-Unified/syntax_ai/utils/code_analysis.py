"""
REAL CODE ANALYSIS - Actual analysis of your codebase
"""

import ast
import re
from pathlib import Path
from typing import List, Dict

class CodeAnalyzer:
    """Performs real analysis on your actual codebase"""
    
    @staticmethod
    def analyze_python_file(file_path: Path) -> Dict:
        """Perform real AST analysis on a Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                "file": str(file_path),
                "functions": [],
                "classes": [],
                "imports": [],
                "issues": [],
                "complexity": 0
            }
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        analysis["imports"].append(f"{module}.{alias.name}")
            
            # Analyze functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": len(node.args.args),
                        "calls": CodeAnalyzer._extract_function_calls(node)
                    })
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
            
            # Check for common issues
            analysis["issues"] = CodeAnalyzer._check_code_issues(content, file_path)
            analysis["complexity"] = len(analysis["functions"]) + len(analysis["classes"])
            
            return analysis
            
        except Exception as e:
            return {"file": str(file_path), "error": str(e)}
    
    @staticmethod
    def _extract_function_calls(node) -> List[str]:
        """Extract function calls from an AST node"""
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)
        return calls
    
    @staticmethod
    def _check_code_issues(content: str, file_path: Path) -> List[str]:
        """Check for common code issues"""
        issues = []
        
        # Security issues
        if "eval(" in content:
            issues.append("Use of eval() - security risk")
        if "exec(" in content:
            issues.append("Use of exec() - security risk")
        
        # Code quality issues
        if len(content.split('\n')) > 500:
            issues.append("File is too long - consider splitting")
        
        # TODO patterns
        if "TODO:" in content or "FIXME:" in content:
            issues.append("Contains TODO/FIXME comments")
        
        return issues
    
    @staticmethod
    def analyze_project(project_path: Path) -> Dict:
        """Analyze an entire project"""
        analysis = {
            "project": str(project_path),
            "files_analyzed": 0,
            "total_functions": 0,
            "total_classes": 0,
            "issues_found": 0,
            "file_analyses": []
        }
        
        python_files = list(project_path.rglob("*.py"))
        
        for py_file in python_files:
            if any(exclude in str(py_file) for exclude in ['venv', '.venv', '__pycache__']):
                continue
                
            file_analysis = CodeAnalyzer.analyze_python_file(py_file)
            analysis["file_analyses"].append(file_analysis)
            analysis["files_analyzed"] += 1
            analysis["total_functions"] += len(file_analysis.get("functions", []))
            analysis["total_classes"] += len(file_analysis.get("classes", []))
            analysis["issues_found"] += len(file_analysis.get("issues", []))
        
        return analysis