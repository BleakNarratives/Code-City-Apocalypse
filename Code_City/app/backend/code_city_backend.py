#!/usr/bin/env python3
import os
import json
import ast
import asyncio
import websockets
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import threading

class CodebaseScanner:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).absolute()
        self.buildings = []
        self.monsters = []
        
    def scan_codebase(self):
        """Scan the actual file system and analyze code"""
        self.buildings = []
        self.monsters = []
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self._is_code_file(file_path):
                building = self._analyze_file(file_path)
                if building:
                    self.buildings.append(building)
                    
                    # Find errors and create monsters
                    errors = self._find_errors(file_path)
                    for error in errors:
                        monster = self._create_monster(building, error)
                        self.monsters.append(monster)
        
        return {
            'buildings': self.buildings,
            'monsters': self.monsters,
            'total_files': len(self.buildings),
            'total_errors': len(self.monsters)
        }
    
    def _is_code_file(self, file_path: Path) -> bool:
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.html', '.css', '.php', '.rb', '.go', '.rs'}
        return file_path.suffix.lower() in code_extensions
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a file and return building data"""
        try:
            stats = file_path.stat()
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Calculate metrics
            lines = content.count('\n')
            size = stats.st_size
            
            # Basic complexity analysis
            complexity = self._calculate_complexity(file_path, content)
            
            return {
                'id': str(file_path),
                'name': file_path.name,
                'path': str(file_path.relative_to(self.root_path)),
                'type': 'file',
                'size': size,
                'lines': lines,
                'complexity': complexity,
                'health': 100,
                'position': {
                    'x': hash(str(file_path)) % 1000,
                    'z': hash(str(file_path.parent)) % 1000
                },
                'dimensions': {
                    'width': max(10, min(50, lines // 10)),
                    'height': max(20, min(100, size // 100)),
                    'depth': max(10, min(30, complexity * 2))
                }
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _calculate_complexity(self, file_path: Path, content: str) -> int:
        """Calculate code complexity based on file type"""
        complexity = 1
        
        if file_path.suffix == '.py':
            # Python complexity: functions, classes, imports
            complexity += content.count('def ') * 2
            complexity += content.count('class ') * 3
            complexity += content.count('import ') * 1
            complexity += content.count('from ') * 1
            
        elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
            # JavaScript/TypeScript complexity
            complexity += content.count('function') * 2
            complexity += content.count('=>') * 1
            complexity += content.count('class ') * 3
            complexity += content.count('import ') * 1
            
        # Add basic line-based complexity
        complexity += min(20, content.count('\n') // 10)
        
        return max(1, complexity)
    
    def _find_errors(self, file_path: Path) -> List[Dict[str, Any]]:
        """Find actual code errors using linters"""
        errors = []
        
        try:
            if file_path.suffix == '.py':
                errors.extend(self._check_python_errors(file_path))
            elif file_path.suffix in ['.js', '.ts']:
                errors.extend(self._check_javascript_errors(file_path))
                
        except Exception as e:
            print(f"Error checking {file_path}: {e}")
            
        return errors
    
    def _check_python_errors(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check Python files for syntax and style errors"""
        errors = []
        
        try:
            # Syntax check
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    ast.parse(f.read())
                except SyntaxError as e:
                    errors.append({
                        'type': 'syntax_error',
                        'message': f"Syntax error: {e.msg}",
                        'line': e.lineno or 1,
                        'severity': 8
                    })
            
            # Basic style checks
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.rstrip()
                if len(line) > 100:
                    errors.append({
                        'type': 'line_too_long',
                        'message': f"Line {i} exceeds 100 characters",
                        'line': i,
                        'severity': 3
                    })
                if line.endswith(' '):
                    errors.append({
                        'type': 'trailing_whitespace',
                        'message': f"Trailing whitespace on line {i}",
                        'line': i,
                        'severity': 2
                    })
                    
        except Exception as e:
            print(f"Error in Python analysis: {e}")
            
        return errors
    
    def _check_javascript_errors(self, file_path: Path) -> List[Dict[str, Any]]:
        """Basic JavaScript error checking"""
        errors = []
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Look for common JS issues
        for i, line in enumerate(lines, 1):
            if 'console.log' in line and '//' not in line.split('console.log')[0]:
                errors.append({
                    'type': 'console_log',
                    'message': f"console.log left in code on line {i}",
                    'line': i,
                    'severity': 4
                })
            if '==' in line and '===' not in line and '!=' not in line:
                # Basic loose equality check
                if any(keyword in line for keyword in ['if', 'while', 'for', '&&', '||']):
                    errors.append({
                        'type': 'loose_equality',
                        'message': f"Use === instead of == on line {i}",
                        'line': i,
                        'severity': 5
                    })
                    
        return errors
    
    def _create_monster(self, building: Dict, error: Dict) -> Dict[str, Any]:
        """Create a monster from an error"""
        return {
            'id': f"{building['id']}_{error['type']}_{error['line']}",
            'type': error['type'],
            'building_id': building['id'],
            'position': {
                'x': building['position']['x'] + (hash(error['type']) % 20 - 10),
                'y': error['line'] * 2,
                'z': building['position']['z'] + (hash(error['message']) % 20 - 10)
            },
            'severity': error['severity'],
            'message': error['message'],
            'health': error['severity'] * 10
        }

class AIAgent:
    def __init__(self):
        self.agents = []
    
    def deploy_agent(self, target_monster: Dict, codebase: CodebaseScanner):
        """Deploy an AI agent to fix a specific error"""
        agent_id = f"agent_{len(self.agents)}_{target_monster['id']}"
        
        agent = {
            'id': agent_id,
            'target_monster_id': target_monster['id'],
            'position': {'x': 0, 'y': 10, 'z': 0},
            'status': 'deploying',
            'health': 100
        }
        
        self.agents.append(agent)
        
        # Start fixing in background
        threading.Thread(target=self._fix_error, args=(agent, target_monster, codebase)).start()
        
        return agent
    
    def _fix_error(self, agent: Dict, monster: Dict, codebase: CodebaseScanner):
        """Actually fix the error (simulated for now)"""
        try:
            # Simulate AI working
            import time
            time.sleep(2)
            
            # In reality, this would call OpenAI API, Claude, etc.
            # For now, we'll just "fix" by removing the monster
            agent['status'] = 'fixed'
            
            # Broadcast the fix
            asyncio.run(self._broadcast_fix(agent, monster))
            
        except Exception as e:
            print(f"Agent error: {e}")
            agent['status'] = 'failed'
    
    async def _broadcast_fix(self, agent: Dict, monster: Dict):
        """Broadcast that a fix was applied"""
        # This would send to the frontend via WebSockets
        pass

# WebSocket server for real-time updates
class CodeCityServer:
    def __init__(self, root_path: str):
        self.scanner = CodebaseScanner(root_path)
        self.agent_manager = AIAgent()
        self.clients = set()
    
    async def handle_client(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(websocket, data)
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, data):
        action = data.get('action')
        
        if action == 'scan':
            # Scan the actual codebase
            result = self.scanner.scan_codebase()
            await websocket.send(json.dumps({
                'type': 'city_data',
                'data': result
            }))
            
        elif action == 'deploy_agent':
            # Deploy AI agent to fix an error
            monster_id = data.get('monster_id')
            monster = next((m for m in self.scanner.monsters if m['id'] == monster_id), None)
            
            if monster:
                agent = self.agent_manager.deploy_agent(monster, self.scanner)
                await websocket.send(json.dumps({
                    'type': 'agent_deployed',
                    'data': agent
                }))

async def main():
    # Get the actual current directory or passed path
    root_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(f"🦖 Scanning codebase at: {root_path}")
    
    server = CodeCityServer(root_path)
    
    # Start WebSocket server
    start_server = websockets.serve(server.handle_client, "localhost", 8765)
    
    print("🚀 Code City Backend running on ws://localhost:8765")
    print("📁 Monitoring:", root_path)
    
    await start_server

if __name__ == "__main__":
    import sys
    asyncio.run(main())