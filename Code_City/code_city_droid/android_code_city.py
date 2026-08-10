#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import sys
import webbrowser
from pathlib import Path
import threading
import time

class CodebaseScanner:
    def __init__(self, root_path):
        self.root_path = Path(root_path).absolute()
        
    def scan_codebase(self):
        buildings = []
        monsters = []
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self._is_code_file(file_path):
                building = self._analyze_file(file_path)
                if building:
                    buildings.append(building)
                    
                    errors = self._find_errors(file_path)
                    for error in errors:
                        monster = self._create_monster(building, error)
                        monsters.append(monster)
        
        return {
            'buildings': buildings,
            'monsters': monsters,
            'total_files': len(buildings),
            'total_errors': len(monsters)
        }
    
    def _is_code_file(self, file_path):
        code_exts = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.md', '.txt', '.java', '.cpp', '.c'}
        return file_path.suffix.lower() in code_exts
    
    def _analyze_file(self, file_path):
        try:
            stats = file_path.stat()
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.count('\n')
            size = stats.st_size
            
            # Simple complexity calculation
            complexity = 1
            complexity += content.count('def ') * 2
            complexity += content.count('class ') * 3
            complexity += content.count('function') * 2
            complexity += min(20, lines // 10)
            
            return {
                'id': str(file_path),
                'name': file_path.name,
                'path': str(file_path.relative_to(self.root_path)),
                'lines': lines,
                'size': size,
                'complexity': complexity,
                'errors': 0,
                'position': {
                    'x': hash(str(file_path)) % 800 - 400,
                    'z': hash(str(file_path.parent)) % 800 - 400
                },
                'dimensions': {
                    'width': max(10, min(50, lines // 5)),
                    'height': max(20, min(120, size // 50)),
                    'depth': max(8, min(25, complexity))
                }
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _find_errors(self, file_path):
        errors = []
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.rstrip()
                
                # Python errors
                if file_path.suffix == '.py':
                    if 'print(' in line and '#' not in line.split('print(')[0]:
                        errors.append({
                            'type': 'debug_print',
                            'message': f"Debug print on line {i}",
                            'line': i,
                            'severity': 3
                        })
                    if 'TODO:' in line or 'FIXME:' in line:
                        errors.append({
                            'type': 'todo',
                            'message': f"TODO/FIXME on line {i}",
                            'line': i,
                            'severity': 2
                        })
                
                # General code issues
                if len(line) > 100:
                    errors.append({
                        'type': 'long_line',
                        'message': f"Line {i} too long ({len(line)} chars)",
                        'line': i,
                        'severity': 4
                    })
                if line.endswith(' '):
                    errors.append({
                        'type': 'trailing_whitespace', 
                        'message': f"Trailing whitespace line {i}",
                        'line': i,
                        'severity': 1
                    })
                    
        except Exception as e:
            print(f"Error checking {file_path}: {e}")
            
        return errors
    
    def _create_monster(self, building, error):
        return {
            'id': f"{building['id']}_{error['type']}_{error['line']}",
            'type': error['type'],
            'building_id': building['id'],
            'position': {
                'x': building['position']['x'] + (hash(error['type']) % 30 - 15),
                'y': error['line'] * 1.5,
                'z': building['position']['z'] + (hash(error['message']) % 30 - 15)
            },
            'severity': error['severity'],
            'message': error['message'],
            'health': error['severity'] * 10
        }

class CodeCityHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.scanner = CodebaseScanner(os.getcwd())
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/scan':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = self.scanner.scan_codebase()
            self.wfile.write(json.dumps(data).encode())
            return
            
        elif self.path == '/':
            self.path = '/code_city.html'
            
        return super().do_GET()

def start_server(port=8000):
    with socketserver.TCPServer(("", port), CodeCityHandler) as httpd:
        print(f"🚀 Code City Apocalypse running at: http://localhost:{port}")
        print("📁 Scanning:", os.getcwd())
        print("💥 Open the above URL in your browser!")
        httpd.serve_forever()

if __name__ == "__main__":
    # Try to open browser automatically
    try:
        webbrowser.open('http://localhost:8000')
    except:
        pass
        
    start_server()