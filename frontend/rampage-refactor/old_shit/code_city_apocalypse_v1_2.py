#!/usr/bin/env python3
"""
CODE CITY APOCALYPSE v1.2 - Optimized for big codebases, expanded features
No freezing, more tank: diff tracking, error fixes, modular growth.
"""
import json
import random
import os
import sys
import asyncio
import aiofiles
from datetime import datetime
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess  # For opening files in editor

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class CodeCityApocalypse:
    def __init__(self):
        self.buildings = []
        self.disasters = []
        self.monsters = []
        self.air_raids = []
        self.last_scan = {}
        self.max_files = 500  # Cap to prevent freeze
        self.file_limit = 1024 * 1024  # 1MB max per file
        
    async def scan_project(self, project_path="."):
        """Async scan with limits and progress"""
        print("Scanning project...")
        updated = False
        file_count = 0
        
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file_count >= self.max_files:
                    print(f"Hit file cap at {self.max_files}. Add pagination for more.")
                    break
                if file.endswith(('.py', '.ts', '.tsx', '.js')):
                    filepath = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(filepath)
                        size = os.path.getsize(filepath)
                        if size > self.file_limit:
                            print(f"Skipping large file: {filepath}")
                            continue
                        if filepath not in self.last_scan or self.last_scan[filepath] != mtime:
                            self.last_scan[filepath] = mtime
                            updated = True
                            await self.update_building(filepath, file)
                            file_count += 1
                            if file_count % 50 == 0:
                                print(f"Scanned {file_count} files...")
                    except OSError:
                        continue
        
        if updated:
            socketio.emit('update_scene', self.generate_city_scene())
        print(f"Scan complete: {file_count} files.")
        return self.generate_city_scene()
    
    async def update_building(self, filepath, filename):
        """Async update for a single building"""
        building = next((b for b in self.buildings if b['path'] == filepath), None)
        if not building:
            building = {
                'id': len(self.buildings),
                'name': filename,
                'path': filepath,
                'x': random.randint(0, 100),
                'z': random.randint(0, 100),
            }
            self.buildings.append(building)
        
        size = os.path.getsize(filepath)
        building.update({
            'height': max(10, min(100, size // 1000)),
            'width': random.randint(5, 15),
            'depth': random.randint(5, 15),
            'health': 100,
            'type': self.get_file_type(filename),
            'color': self.get_file_color(filename),
            'windows': random.randint(5, 50),
            'occupants': random.randint(1, 10)
        })
        
        error_level = await self.scan_file_for_errors(filepath)
        if error_level > 0:
            building['health'] = max(0, 100 - (error_level * 20))
            self.trigger_disaster(building, error_level)
    
    async def scan_file_for_errors(self, filepath):
        """Async file scan with size check"""
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = await f.read()
            
            error_level = 0
            patterns = [
                ('SyntaxError', 3), ('NameError', 2), ('TypeError', 2),
                ('IndexError', 2), ('TODO', 1), ('FIXME', 1), ('HACK', 1), ('XXX', 1)
            ]
            for pattern, severity in patterns:
                if pattern.lower() in content.lower():
                    error_level += severity
            
            lines = content.split('\n')
            if len(lines) > 200: error_level += 1
            if len(lines) > 500: error_level += 2
            
            return min(5, error_level)
        except Exception:
            return 3
    
    def trigger_disaster(self, building, severity):
        # Unchanged, but could add more types here for expansion
        disasters = [self.create_fire, self.create_monster, self.create_air_raid]
        for _ in range(severity):
            random.choice(disasters)(building)
    
    def create_fire(self, building):
        fire = {
            'type': 'fire', 'building_id': building['id'],
            'intensity': random.randint(1, 10),
            'position': {'x': building['x'] + random.randint(-5, 5), 'y': random.randint(10, building['height']), 'z': building['z'] + random.randint(-5, 5)},
            'particles': random.randint(10, 50)
        }
        self.disasters.append(fire)
    
    def create_monster(self, building):
        monster = {
            'type': 'monster', 'species': random.choice(['gorilla', 'lizard', 'wolf', 'dinosaur']),
            'building_id': building['id'],
            'position': {'x': building['x'], 'y': 0, 'z': building['z']},
            'scale': random.uniform(1.0, 3.0), 'health': random.randint(50, 100), 'damage': random.randint(1, 5)
        }
        self.monsters.append(monster)
    
    def create_air_raid(self, building):
        plane = {
            'type': 'air_raid', 'pilot': 'red_baron',
            'building_id': building['id'],
            'position': {'x': random.randint(0, 100), 'y': random.randint(30, 50), 'z': random.randint(0, 100)},
            'velocity': {'x': random.uniform(-2, 2), 'y': 0, 'z': random.uniform(-2, 2)},
            'bombs': random.randint(1, 5)
        }
        self.air_raids.append(plane)
    
    def generate_city_scene(self):
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_buildings': len(self.buildings),
                'total_disasters': len(self.disasters),
                'total_monsters': len(self.monsters),
                'total_air_raids': len(self.air_raids)
            },
            'city': {
                'buildings': self.buildings,
                'disasters': self.disasters,
                'monsters': self.monsters,
                'air_raids': self.air_raids
            }
        }
    
    def generate_html(self):
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Code City - Workflow Viz</title>
    <style>
        body { margin: 0; background: #f0f0f0; font-family: monospace; display: flex; }
        #sidebar { width: 300px; background: #333; color: white; padding: 10px; overflow-y: auto; }
        #viz { flex: 1; position: relative; }
        #stats { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 5px; color: white; }
        #mode-toggle, #focus-toggle { position: absolute; top: 10px; left: 10px; margin-bottom: 5px; }
        canvas { width: 100%; height: 100%; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <div id="sidebar">
        <h3>Files & Errors</h3>
        <ul id="file-list"></ul>
    </div>
    <div id="viz">
        <button id="mode-toggle">Toggle 2D/3D</button>
        <button id="focus-toggle">Focus Mode</button>
        <div id="stats">Loading...</div>
        <canvas id="canvas"></canvas>
    </div>
    <script>
        const socket = io();
        let scene, camera, renderer, buildings = [], mode = '3d', focused = false;
        
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas') });
        renderer.setSize(window.innerWidth - 300, window.innerHeight);
        
        scene.add(new THREE.AmbientLight(0x404040));
        const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshBasicMaterial({ color: 0x666666 }));
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);
        camera.position.set(50, 50, 50);
        
        socket.on('update_scene', (data) => {
            buildings.forEach(b => scene.remove(b));
            buildings = [];
            
            data.city.buildings.slice(0, 100).forEach(b => {  // Limit objects for perf
                const geom = mode === '3d' ? new THREE.BoxGeometry(b.width, b.height, b.depth) : new THREE.PlaneGeometry(b.width, b.height);
                const mat = new THREE.MeshBasicMaterial({ color: b.color });
                const mesh = new THREE.Mesh(geom, mat);
                mesh.position.set(b.x, mode === '3d' ? b.height / 2 : 0, b.z);
                mesh.userData = b;
                if (!focused) scene.add(mesh);
                buildings.push(mesh);
            });
            
            const list = document.getElementById('file-list');
            list.innerHTML = data.city.buildings.map(b => 
                `<li onclick="openFile('${b.path}')">${b.name} - Health: ${b.health}% 
                <button onclick="suggestFix('${b.path}', '${b.name}')">Fix</button></li>`
            ).join('');
            
            document.getElementById('stats').innerHTML = `Buildings: ${data.metadata.total_buildings} | Disasters: ${data.metadata.total_disasters}`;
        });
        
        function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
        animate();
        
        document.getElementById('mode-toggle').onclick = () => { mode = mode === '3d' ? '2d' : '3d'; socket.emit('request_update'); };
        document.getElementById('focus-toggle').onclick = () => { 
            focused = !focused; 
            buildings.forEach(b => focused ? scene.remove(b) : scene.add(b)); 
        };
        
        function openFile(path) { window.open(`file://${path}`); }
        function suggestFix(path, name) { alert(`Suggested fix for ${name}: Check for syntax errors in ${path}. Open in editor?`); }
    </script>
</body>
</html>
        """

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, apocalypse):
        self.apocalypse = apocalypse
        self.debounce_timer = None
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.py', '.ts', '.tsx', '.js')):
            if self.debounce_timer:
                self.debounce_timer.cancel()
            self.debounce_timer = asyncio.get_event_loop().call_later(1.0, lambda: asyncio.create_task(self.apocalypse.scan_project()))

apocalypse = CodeCityApocalypse()

@app.route('/')
def index():
    return render_template_string(apocalypse.generate_html())

@socketio.on('connect')
def handle_connect():
    emit('update_scene', apocalypse.generate_city_scene())

@socketio.on('request_update')
def handle_request():
    asyncio.create_task(apocalypse.scan_project())

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    asyncio.run(apocalypse.scan_project(path))
    
    observer = Observer()
    observer.schedule(FileChangeHandler(apocalypse), path, recursive=True)
    observer.start()
    
    print("Code City server running... Open http://localhost:5000")
    socketio.run(app, debug=True)
