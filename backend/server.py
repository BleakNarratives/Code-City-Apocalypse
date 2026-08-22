#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: asyncio, datetime, json, logging, os, pathlib, typing, websockets
# ROLE: CODE CITY - Cross-Platform Backend Server
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

"""
CODE CITY - Cross-Platform Backend Server
A functional code city visualization system for Android and Windows
"""

import os
import json
import asyncio
import websockets
from pathlib import Path
from typing import Dict, List, Set
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server configuration
HOST = os.getenv('HOST', '0.0.0.0')  # Work on both Android and Windows
PORT = int(os.getenv('PORT', 8765))


class CodeCityScanner:
    """Scans codebases and generates city data"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.java', '.cpp', '.c', '.h', '.hpp',
            '.go', '.rs', '.rb', '.php', '.html', '.css'
        }
        self.max_file_size = 1024 * 1024  # 1MB - works on mobile
    
    def scan_codebase(self, root_path: str) -> Dict[str, any]:
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
            'root_path': str(root),
            'timestamp': datetime.now().isoformat()
        }
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned"""
        if not file_path.is_file():
            return False
        
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return False
        
        # Skip common directories that cause issues
        skip_dirs = {'node_modules', 'venv', '__pycache__', '.git', 'dist', 'build'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return False
        
        # Check extension
        if file_path.suffix.lower() not in self.supported_extensions:
            return False
        
        # Check file size (important for mobile)
        try:
            if file_path.stat().st_size > self.max_file_size:
                return False
        except:
            return False
        
        return True
    
    def _analyze_file(self, file_path: Path, root: Path) -> Dict[str, any]:
        """Analyze a single file and return building data"""
        try:
            stats = file_path.stat()
            
            # Read file content safely
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except:
                content = ""
            
            lines = content.count('\n') + 1 if content else 1
            size = stats.st_size
            complexity = self._calculate_complexity(file_path, content)
            
            # Calculate deterministic position based on filename
            file_hash = hash(str(file_path))
            x = (file_hash % 200) - 100
            z = ((file_hash >> 8) % 200) - 100
            
            # Calculate dimensions based on file characteristics
            height = max(10, min(150, lines // 2))
            width = max(8, min(30, size // 500))
            depth = max(8, min(30, complexity))
            
            # Color based on file type
            color = self._get_file_color(file_path)
            
            return {
                'id': str(file_path),
                'name': file_path.name,
                'path': str(file_path.relative_to(root)),
                'full_path': str(file_path),
                'type': file_path.suffix[1:] if file_path.suffix else 'file',
                'size': size,
                'lines': lines,
                'complexity': complexity,
                'health': 100,
                'position': {'x': x, 'y': 0, 'z': z},
                'dimensions': {
                    'width': width,
                    'height': height,
                    'depth': depth
                },
                'color': color
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
            content = file_path.read_text(encoding='utf-8')
            
            # Check syntax
            try:
                compile(content, str(file_path), 'exec')
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
                    
                # Simple unused variable detection
                if line.strip().startswith('def ') or line.strip().startswith('class '):
                    # Skip function/class definitions
                    continue
                    
                if '=' in line and not line.strip().startswith('#'):
                    # Very simple unused variable check
                    parts = line.split('=')
                    if len(parts) > 1:
                        var_name = parts[0].strip()
                        if var_name and not var_name.startswith('('):
                            # Check if variable is used later
                            remaining_content = '='.join(parts[1:])
                            if var_name not in remaining_content and content.count(var_name) == 1:
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
            content = file_path.read_text(encoding='utf-8')
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
        
        except Exception as e:
            logger.warning(f"Error checking JS bugs: {e}")
        
        return bugs
    
    def _create_monster(self, building: Dict, bug: Dict) -> Dict[str, any]:
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


class CodeCityServer:
    """WebSocket server for Code City"""
    
    def __init__(self):
        self.clients: Set = set()
        self.scanner = CodeCityScanner()
        self.current_city = None
        logger.info("🏙️ Code City Server initialized")
    
    async def handle_client(self, websocket):
        """Handle WebSocket client connections"""
        self.clients.add(websocket)
        logger.info(f"✅ Client connected. Total clients: {len(self.clients)}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                'type': 'connected',
                'message': 'Welcome to Code City!',
                'timestamp': datetime.now().isoformat()
            }))
            
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, message: str):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            action = data.get('action')
            
            logger.info(f"📨 Received action: {action}")
            
            if action == 'scan':
                await self.scan_codebase(websocket, data)
                
            elif action == 'rescan':
                await self.rescan_file(websocket, data)
                
            elif action == 'get_file_content':
                await self.get_file_content(websocket, data)
                
            elif action == 'deploy_agent':
                await self.deploy_agent(websocket, data)
                
            elif action == 'health':
                await websocket.send(json.dumps({
                    'type': 'health',
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat()
                }))
                
            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f'Unknown action: {action}'
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def scan_codebase(self, websocket, data: Dict):
        """Scan a codebase and return city data"""
        folder_path = data.get('path', os.getcwd())
        
        try:
            logger.info(f"🔍 Scanning codebase at: {folder_path}")
            
            # Send scanning status
            await websocket.send(json.dumps({
                'type': 'scanning',
                'message': 'Scanning codebase...',
                'path': folder_path
            }))
            
            # Perform scan
            city_data = self.scanner.scan_codebase(folder_path)
            self.current_city = city_data
            
            logger.info(f"✅ Scan complete: {len(city_data['buildings'])} files, {len(city_data['monsters'])} bugs")
            
            # Send city data
            await websocket.send(json.dumps({
                'type': 'city_data',
                'data': city_data,
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Scan error: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Scan failed: {str(e)}'
            }))
    
    async def rescan_file(self, websocket, data: Dict):
        """Re-scan a specific file to check if bug is fixed"""
        file_path = data.get('file_path')
        
        try:
            logger.info(f"🔄 Re-scanning file: {file_path}")
            
            # Re-scan just this file
            building = self.scanner._analyze_file(Path(file_path), Path(file_path).parent)
            
            if building:
                bugs = self.scanner._find_bugs(Path(file_path), building)
                building['bugs'] = bugs
            
            await websocket.send(json.dumps({
                'type': 'file_rescanned',
                'data': building,
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Re-scan failed: {str(e)}'
            }))
    
    async def get_file_content(self, websocket, data: Dict):
        """Get file content and line information"""
        file_path = data.get('file_path')
        line_number = data.get('line_number', 1)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Get context around the error line
            start = max(0, line_number - 5)
            end = min(len(lines), line_number + 5)
            
            context = {
                'file_path': file_path,
                'line_number': line_number,
                'lines': lines[start:end],
                'start_line': start + 1,
                'end_line': end + 1
            }
            
            await websocket.send(json.dumps({
                'type': 'file_content',
                'data': context
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Failed to read file: {str(e)}'
            }))
    
    async def deploy_agent(self, websocket, data: Dict):
        """Deploy an agent to target a monster"""
        monster_id = data.get('monster_id')
        
        logger.info(f"🤖 Agent deployed targeting monster: {monster_id}")
        
        # Create agent data
        agent = {
            'id': f'agent_{monster_id}_{datetime.now().timestamp()}',
            'target_monster_id': monster_id,
            'status': 'hunting',
            'position': {'x': 0, 'y': 10, 'z': 0}
        }
        
        await websocket.send(json.dumps({
            'type': 'agent_deployed',
            'data': agent
        }))
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )


async def main():
    """Start the server"""
    server = CodeCityServer()

    print("\n" + "="*60)
    print("🏙️ CODE CITY - Cross-Platform Backend Server")
    print("="*60)
    print(f"🚀 WebSocket server running on ws://{HOST}:{PORT}")
    print(f"📡 HTTP health check: http://{HOST}:{PORT}/health")
    print(f"🌐 Accessible from: http://localhost:{PORT}")
    print(f"📁 Ready to scan codebases!")
    print("="*60)
    print(f"Platform: {'Android' if 'com.termux' in os.getcwd() else 'Windows/Linux'}")
    print(f"Python: {os.sys.version}")
    print("="*60 + "\n")

    async with websockets.serve(server.handle_client, HOST, PORT):
        await asyncio.Future()  # Run forever
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"\n💥 Server error: {e}")