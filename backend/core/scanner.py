#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: , ast, logging, os, pathlib, re, typing
# ROLE: Code Scanner - Analyzes codebases and detects bugs
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

"""
Code Scanner - Analyzes codebases and detects bugs
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any
import logging
from .CoreTenet_FCT import check_for_bloat

logger = logging.getLogger(__name__)


class CodebaseScanner:
    """Scans codebases and generates city data"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.html', '.css'
        }
        self.max_file_size = 1024 * 1024  # 1MB
    
    def scan_codebase(self, root_path: str) -> Dict[str, Any]:
        """Scan entire codebase and return city data"""
        root = Path(root_path).absolute()
        
        if not root.exists():
            raise ValueError(f"Path does not exist: {root_path}")
        
        buildings = []
        monsters = []
        
        # Walk through directory
        for file_path in root.rglob('*'):
            if not self._should_scan_file(file_path):
                continue
            
            try:
                building = self._analyze_file(file_path, root)
                if building:
                    buildings.append(building)
                    
                    # Find bugs in this file
                    bugs = self._find_bugs(file_path, building)
                    for bug in bugs:
                        monster = self._create_monster(building, bug)
                        monsters.append(monster)
            
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
                continue
        
        return {
            'buildings': buildings,
            'monsters': monsters,
            'total_files': len(buildings),
            'total_errors': len(monsters),
            'root_path': str(root)
        }
    
    def analyze_single_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file"""
        path = Path(file_path)
        building = self._analyze_file(path, path.parent)
        
        if building:
            bugs = self._find_bugs(path, building)
            building['bugs'] = bugs
        
        return building
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned"""
        if not file_path.is_file():
            return False
        
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return False
        
        # Skip node_modules, venv, etc.
        skip_dirs = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return False
        
        # Check extension
        if file_path.suffix.lower() not in self.supported_extensions:
            return False
        
        # Check file size
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except:
            return False
        
        return True
    
    def _analyze_file(self, file_path: Path, root: Path) -> Dict[str, Any]:
        """Analyze a single file and return building data"""
        try:
            stats = file_path.stat()
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode {file_path} with UTF-8, trying latin-1.")
                content = file_path.read_text(encoding='latin-1', errors='ignore')
            except (FileNotFoundError, IOError) as e:
                logger.error(f"Error reading file {file_path}: {e}")
                return None
            
            lines = content.count('\n') + 1
            size = stats.st_size
            complexity = self._calculate_complexity(file_path, content)
            
            # Calculate position (deterministic based on filename)
            file_hash = hash(str(file_path))
            x = (file_hash % 200) - 100
            z = ((file_hash >> 8) % 200) - 100
            
            # Calculate dimensions
            height = max(10, min(150, lines // 2))
            width = max(8, min(30, size // 500))
            depth = max(8, min(30, complexity))
            
            # Color based on file type
            color = self._get_file_color(file_path)
            
            
            # --- Bloat Analysis ---
            language = file_path.suffix[1:] if file_path.suffix else 'unknown'
            # For simplicity, using filename as template_type proxy, and empty lists for deps/services
            bloat_report = check_for_bloat(
                language=language,
                template_type=file_path.name,
                requested_dependencies=[], # Requires more advanced parsing to populate accurately
                required_external_services=[] # Requires more advanced parsing to populate accurately
            )

            return {
                'id': str(file_path),
                'name': file_path.name,
                'path': str(file_path.relative_to(root)),
                'full_path': str(file_path),
                'type': file_path.suffix[1:] if file_path.suffix else 'file',
                'size': size,
                'lines': lines,
                'complexity': complexity,
                'health': 100, # Base health, can be adjusted by bloat
                'position': {'x': x, 'y': 0, 'z': z},
                'dimensions': {
                    'width': width,
                    'height': height,
                    'depth': depth
                },
                'color': color,
                'bloat_report': bloat_report
            }
        
        except Exception as e:
            logger.warning(f"Error analyzing {file_path}: {e}")
            return None
    
    def _calculate_complexity(self, file_path: Path, content: str) -> int:
        """Calculate code complexity"""
        complexity = 1
        
        if file_path.suffix == '.py':
            complexity += content.count('def ') * 2
            complexity += content.count('class ') * 3
            complexity += content.count('if ') * 1
            complexity += content.count('for ') * 1
            complexity += content.count('while ') * 1
        
        elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
            complexity += content.count('function') * 2
            complexity += content.count('=>') * 1
            complexity += content.count('class ') * 3
            complexity += content.count('if ') * 1
            complexity += content.count('for ') * 1
        
        # Add base complexity from lines
        complexity += min(20, len(content.split('\n')) // 20)
        
        return max(1, min(50, complexity))
    
    def _get_file_color(self, file_path: Path) -> str:
        """Get color based on file type"""
        colors = {
            '.py': '#3776ab',      # Python blue
            '.js': '#f7df1e',      # JavaScript yellow
            '.ts': '#3178c6',      # TypeScript blue
            '.jsx': '#61dafb',     # React cyan
            '.tsx': '#61dafb',     # React cyan
            '.java': '#f89820',    # Java orange
            '.cpp': '#00599c',     # C++ blue
            '.c': '#a8b9cc',       # C gray
            '.go': '#00add8',      # Go cyan
            '.rs': '#ce422b',      # Rust red
            '.rb': '#cc342d',      # Ruby red
            '.php': '#777bb3',     # PHP purple
            '.html': '#e34c26',    # HTML orange
            '.css': '#1572b6'      # CSS blue
        }
        return colors.get(file_path.suffix, '#6c757d')
    
    def _find_bugs(self, file_path: Path, building: Dict) -> List[Dict]:
        """Find bugs in a file"""
        bugs = []
        
        try:
            if file_path.suffix == '.py':
                bugs.extend(self._check_python_bugs(file_path))
            elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                bugs.extend(self._check_javascript_bugs(file_path))
        except Exception as e:
            logger.warning(f"Error checking bugs in {file_path}: {e}")
        
        return bugs
    
    def _check_python_bugs(self, file_path: Path) -> List[Dict]:
        """Check Python files for bugs"""
        bugs = []
        
        try:
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode {file_path} with UTF-8 in _check_python_bugs, trying latin-1.")
                content = file_path.read_text(encoding='latin-1', errors='ignore')
            except (FileNotFoundError, IOError) as e:
                logger.error(f"Error reading file {file_path} in _check_python_bugs: {e}")
                return bugs # Return empty list if file cannot be read
            
            # Check syntax
            try:
                ast.parse(content)
            except SyntaxError as e:
                bugs.append({
                    'type': 'syntax_error',
                    'message': f'Syntax error: {e.msg}',
                    'line': e.lineno or 1,
                    'severity': 9
                })
            
            # Check for common issues
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Line too long
                if len(line) > 120:
                    bugs.append({
                        'type': 'line_too_long',
                        'message': f'Line exceeds 120 characters ({len(line)} chars)',
                        'line': i,
                        'severity': 3
                    })
                
                # Trailing whitespace
                if line.rstrip() != line and line.strip():
                    bugs.append({
                        'type': 'trailing_whitespace',
                        'message': 'Trailing whitespace',
                        'line': i,
                        'severity': 2
                    })
                
                # Unused variable (basic check)
                if re.match(r'^\s*[a-z_]\w*\s*=', line):
                    var_name = line.split('=')[0].strip()
                    if content.count(var_name) == 1:
                        bugs.append({
                            'type': 'unused_variable',
                            'message': f'Variable "{var_name}" may be unused',
                            'line': i,
                            'severity': 4
                        })
        
        except Exception as e:
            logger.warning(f"Error checking Python bugs: {e}")
        
        return bugs
    
    def _check_javascript_bugs(self, file_path: Path) -> List[Dict]:
        """Check JavaScript files for bugs"""
        bugs = []
        
        try:
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                logger.warning(f"Failed to decode {file_path} with UTF-8 in _check_javascript_bugs, trying latin-1.")
                content = file_path.read_text(encoding='latin-1', errors='ignore')
            except (FileNotFoundError, IOError) as e:
                logger.error(f"Error reading file {file_path} in _check_javascript_bugs: {e}")
                return bugs # Return empty list if file cannot be read
            
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # console.log left in code
                if 'console.log' in line and '//' not in line.split('console.log')[0]:
                    bugs.append({
                        'type': 'console_log',
                        'message': 'console.log() left in code',
                        'line': i,
                        'severity': 4
                    })
                
                # Loose equality
                if '==' in line and '===' not in line and '!=' not in line:
                    bugs.append({
                        'type': 'loose_equality',
                        'message': 'Use === instead of ==',
                        'line': i,
                        'severity': 5
                    })
                
                # Missing semicolon (basic check)
                if line.strip() and not line.strip().endswith((';', '{', '}', ',', ')', ']')):
                    if any(keyword in line for keyword in ['var ', 'let ', 'const ', 'return ']):
                        bugs.append({
                            'type': 'missing_semicolon',
                            'message': 'Missing semicolon',
                            'line': i,
                            'severity': 3
                        })
        
        except Exception as e:
            logger.warning(f"Error checking JS bugs: {e}")
        
        return bugs
    
    def _create_monster(self, building: Dict, bug: Dict) -> Dict[str, Any]:
        """Create monster from bug"""
        # Position near the building
        offset_x = (hash(bug['type']) % 20) - 10
        offset_z = (hash(bug['message']) % 20) - 10
        
        return {
            'id': f"{building['id']}_L{bug['line']}_{bug['type']}",
            'type': bug['type'],
            'building_id': building['id'],
            'file_path': building['full_path'],
            'file_name': building['name'],
            'position': {
                'x': building['position']['x'] + offset_x,
                'y': bug['line'] * 0.5,
                'z': building['position']['z'] + offset_z
            },
            'severity': bug['severity'],
            'message': bug['message'],
            'line': bug['line'],
            'health': bug['severity'] * 10,
            'color': self._get_monster_color(bug['type'])
        }
    
    def _get_monster_color(self, bug_type: str) -> str:
        """Get monster color based on bug type"""
        colors = {
            'syntax_error': '#ff0000',
            'line_too_long': '#4444ff',
            'trailing_whitespace': '#888888',
            'unused_variable': '#ff8800',
            'console_log': '#ffcc00',
            'loose_equality': '#aa00ff',
            'missing_semicolon': '#ff4444'
        }
        return colors.get(bug_type, '#ff4444')
