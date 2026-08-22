#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-frontend
# DEPS: datetime, json, os, random, sys
# ROLE: CODE CITY APOCALYPSE v1.4 - Static HTML version, no deps beyond standard lib
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
CODE CITY APOCALYPSE v1.4 - Static HTML version, no deps beyond standard lib
Quick viz for big codebases.
"""
import json
import random
import os
import sys
from datetime import datetime

class CodeCityApocalypse:
    def __init__(self):
        self.buildings = []
        self.disasters = []
        self.monsters = []
        self.air_raids = []
        
    def scan_project(self, project_path="."):
        """Scan project and create city"""
        print("Scanning project...")
        file_count = 0
        
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(('.py', '.ts', '.tsx', '.js')):
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        if size > 1024 * 1024:  # Skip >1MB
                            continue
                        building = {
                            'id': file_count,
                            'name': file,
                            'path': filepath,
                            'height': max(10, min(100, size // 1000)),
                            'width': random.randint(5, 15),
                            'depth': random.randint(5, 15),
                            'x': random.randint(0, 100),
                            'z': random.randint(0, 100),
                            'health': 100,
                            'type': self.get_file_type(file),
                            'color': self.get_file_color(file),
                            'windows': random.randint(5, 50),
                            'occupants': random.randint(1, 10)
                        }
                        
                        error_level = self.scan_file_for_errors(filepath)
                        if error_level > 0:
                            building['health'] = max(0, 100 - (error_level * 20))
                            self.trigger_disaster(building, error_level)
                        
                        self.buildings.append(building)
                        file_count += 1
                        if file_count >= 500:  # Cap
                            break
                    except OSError:
                        continue
            if file_count >= 500:
                break
        
        print(f"Scan complete: {file_count} files.")
        return self.generate_city_scene()
    
    def get_file_type(self, filename):
        if filename.endswith('.py'):
            return 'python_tower'
        elif filename.endswith('.tsx') or filename.endswith('.jsx'):
            return 'react_dome' 
        elif filename.endswith('.ts') or filename.endswith('.js'):
            return 'javascript_spire'
        else:
            return 'data_bunker'
    
    def get_file_color(self, filename):
        colors = {
            'python_tower': '#3572A5',
            'react_dome': '#61DAFB',
            'javascript_spire': '#F7DF1E',
            'data_bunker': '#4CAF50'
        }
        return colors.get(self.get_file_type(filename), '#666666')
    
    def scan_file_for_errors(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
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
    
    def generate_html(self, scene_data):
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code City Apocalypse</title>
    <style>
        body {{ margin: 0; background: #1a1a2e; color: white; font-family: monospace; }}
        #info {{ position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.8); padding: 10px; }}
        #stats {{ position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); padding: 10px; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="info">
        <h2>🏙️ CODE CITY APOCALYPSE</h2>
        <p>Buildings = Files | Disasters = Errors</p>
    </div>
    <div id="stats">
        <h3>Stats</h3>
        <p>Buildings: {scene_data['metadata']['total_buildings']}</p>
        <p>Disasters: {scene_data['metadata']['total_disasters']}</p>
    </div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        scene.add(new THREE.AmbientLight(0x404040));
        const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshBasicMaterial({{ color: 0x2d5a27 }}));
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);
        
        const cityData = {json.dumps(scene_data)};
        
        cityData.city.buildings.forEach(b => {{
            const geom = new THREE.BoxGeometry(b.width, b.height, b.depth);
            const mat = new THREE.MeshBasicMaterial({{ color: b.color }});
            const mesh = new THREE.Mesh(geom, mat);
            mesh.position.set(b.x, b.height / 2, b.z);
            scene.add(mesh);
        }});
        
        camera.position.set(50, 50, 50);
        camera.lookAt(0, 0, 0);
        
        function animate() {{
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
        """
        return html

def main():
    apocalypse = CodeCityApocalypse()
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    scene_data = apocalypse.scan_project(path)
    
    html_content = apocalypse.generate_html(scene_data)
    with open('code_city.html', 'w') as f:
        f.write(html_content)
    
    print("Viz generated. Open 'code_city.html' in your browser.")

if __name__ == "__main__":
    main()
