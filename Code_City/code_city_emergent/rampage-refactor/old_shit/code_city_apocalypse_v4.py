"""[ARCHIVED — syntax error fixed by wrapping]

#!/usr/bin/env python3
\"\"\"
CODE CITY APOCALYPSE v1 - Turns errors into visual chaos
Buildings = Files, Errors = Disasters, Bugs = Monsters
Enhanced with interactive UI and fixes.
\"\"\"
import json
import random
import math
import os
import sys
from datetime import datetime

class CodeCityApocalypse:
    def __init__(self):
        self.buildings = []  # Files as buildings
        self.disasters = []  # Errors as disasters
        self.monsters = []   # Bugs as monsters
        self.air_raids = []  # Syntax errors as air raids
        
    def scan_project(self, project_path="."):
        \"\"\"Scan project and create city layout\"\"\"
        self.buildings = []
        building_id = 0
        
        try:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith(('.py', '.ts', '.tsx', '.js')):
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                        except OSError:
                            continue  # Skip inaccessible files
                        
                        # Create building from file
                        building = {
                            'id': building_id,
                            'name': file,
                            'path': filepath,
                            'height': max(10, min(100, size // 1000)),  # Height based on file size
                            'width': random.randint(5, 15),
                            'depth': random.randint(5, 15),
                            'x': random.randint(0, 100),
                            'z': random.randint(0, 100),
                            'health': 100,
                            'type': self.get_file_type(file),
                            'color': self.get_file_color(file),
                            'windows': random.randint(5, 50),  # Lines of code
                            'occupants': random.randint(1, 10)  # Functions/classes
                        }
                        
                        # Check for errors in file
                        error_level = self.scan_file_for_errors(filepath)
                        if error_level > 0:
                            building['health'] = max(0, 100 - (error_level * 20))
                            self.trigger_disaster(building, error_level)
                        
                        self.buildings.append(building)
                        building_id += 1
        except Exception as e:
            print(f"Error scanning project: {e}")
        
        return self.generate_city_scene()
    
    def get_file_type(self, filename):
        \"\"\"Determine building type based on file\"\"\"
        if filename.endswith('.py'):
            return 'python_tower'
        elif filename.endswith('.tsx') or filename.endswith('.jsx'):
            return 'react_dome' 
        elif filename.endswith('.ts') or filename.endswith('.js'):
            return 'javascript_spire'
        else:
            return 'data_bunker'
    
    def get_file_color(self, filename):
        \"\"\"Get building color based on file type\"\"\"
        colors = {
            'python_tower': '#3572A5',  # Python blue
            'react_dome': '#61DAFB',    # React blue
            'javascript_spire': '#F7DF1E',  # JS yellow
            'data_bunker': '#4CAF50'    # Green
        }
        return colors.get(self.get_file_type(filename), '#666666')
    
    def scan_file_for_errors(self, filepath):
        \"\"\"Scan file for errors and return severity level\"\"\"
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            error_level = 0
            
            # Check for common error patterns
            error_patterns = [
                ('SyntaxError', 3),
                ('NameError', 2),
                ('TypeError', 2),
                ('IndexError', 2),
                ('TODO', 1),
                ('FIXME', 1),
                ('HACK', 1),
                ('XXX', 1)
            ]
            
            for pattern, severity in error_patterns:
                if pattern.lower() in content.lower():
                    error_level += severity
            
            # Check for long files (potential code smells)
            lines = content.split('\n')
            if len(lines) > 200:
                error_level += 1
            if len(lines) > 500:
                error_level += 2
            
            return min(5, error_level)  # Cap at 5
            
        except Exception:
            return 3  # File read error
    
    def trigger_disaster(self, building, severity):
        \"\"\"Trigger appropriate disaster based on error severity\"\"\"
        disasters = [
            self.create_fire,
            self.create_monster,
            self.create_air_raid,
            self.create_earthquake,
            self.create_lightning
        ]
        
        # Trigger multiple disasters for high severity
        for i in range(severity):
            disaster_func = random.choice(disasters)
            disaster_func(building)
    
    def create_fire(self, building):
        \"\"\"Create fire disaster for syntax errors\"\"\"
        fire = {
            'type': 'fire',
            'building_id': building['id'],
            'intensity': random.randint(1, 10),
            'position': {
                'x': building['x'] + random.randint(-5, 5),
                'y': random.randint(10, building['height']),
                'z': building['z'] + random.randint(-5, 5)
            },
            'particles': random.randint(10, 50)
        }
        self.disasters.append(fire)
    
    def create_monster(self, building):
        \"\"\"Create Rampage-style monster for logic errors\"\"\"
        monsters = ['gorilla', 'lizard', 'wolf', 'dinosaur']
        monster = {
            'type': 'monster',
            'species': random.choice(monsters),
            'building_id': building['id'],
            'position': {
                'x': building['x'],
                'y': 0,
                'z': building['z']
            },
            'scale': random.uniform(1.0, 3.0),
            'health': random.randint(50, 100),
            'damage': random.randint(1, 5)
        }
        self.monsters.append(monster)
    
    def create_air_raid(self, building):
        \"\"\"Create Red Baron air raid for runtime errors\"\"\"
        plane = {
            'type': 'air_raid',
            'pilot': 'red_baron',
            'building_id': building['id'],
            'position': {
                'x': random.randint(0, 100),
                'y': random.randint(30, 50),
                'z': random.randint(0, 100)
            },
            'velocity': {
                'x': random.uniform(-2, 2),
                'y': 0,
                'z': random.uniform(-2, 2)
            },
            'bombs': random.randint(1, 5)
        }
        self.air_raids.append(plane)
    
    def create_earthquake(self, building):
        \"\"\"Create earthquake for system crashes\"\"\"
        quake = {
            'type': 'earthquake',
            'epicenter': {
                'x': building['x'],
                'z': building['z']
            },
            'magnitude': random.uniform(3.0, 7.0),
            'duration': random.randint(3, 10)
        }
        self.disasters.append(quake)
    
    def create_lightning(self, building):
        \"\"\"Create lightning for electrical/performance issues\"\"\"
        lightning = {
            'type': 'lightning',
            'building_id': building['id'],
            'start': {
                'x': building['x'] + random.randint(-10, 10),
                'y': 50,
                'z': building['z'] + random.randint(-10, 10)
            },
            'end': {
                'x': building['x'],
                'y': 0,
                'z': building['z']
            },
            'bolts': random.randint(1, 3)
        }
        self.disasters.append(lightning)
    
    def generate_city_scene(self):
        \"\"\"Generate Three.js scene with all elements\"\"\"
        scene = {
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
        
        return scene
    
    def generate_threejs_html(self, scene_data):
        \"\"\"Generate HTML with Three.js visualization\"\"\"
        html_template = \"\"\"
<!DOCTYPE html>
<html>
<head>
    <title>CODE CITY APOCALYPSE</title>
    <style>
        body { 
            margin: 0; 
            background: linear-gradient(#1a1a2e, #16213e);
            color: white;
            font-family: 'Courier New', monospace;
            overflow: hidden;
        }
        #info {
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 5px;
            z-index: 100;
        }
        #city-stats {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 5px;
            z-index: 100;
        }
        #building-details {
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 5px;
            display: none;
            z-index: 100;
        }
        canvas { display: block; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="info">
        <h2>🏙️ CODE CITY APOCALYPSE</h2>
        <p>Files = Buildings | Errors = Disasters | Bugs = Monsters</p>
        <p>Click buildings for details. Use mouse to orbit/zoom.</p>
    </div>
    
    <div id="city-stats">
        <h3>City Status</h3>
        <p>🏢 Buildings: <span id="building-count">0</span></p>
        <p>🔥 Disasters: <span id="disaster-count">0</span></p>
        <p>👾 Monsters: <span id="monster-count">0</span></p>
        <p>✈️ Air Raids: <span id="air-raid-count">0</span></p>
    </div>

    <div id="building-details">
        <h3>Building Details</h3>
        <p id="details-content">Click a building to see info.</p>
    </div>

    <script>
        // SCENE DATA FROM PYTHON
        const cityData = {{SCENE_DATA}};
        
        // Initialize Three.js
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);
        
        // OrbitControls for interactivity
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 50);
        scene.add(directionalLight);
        
        // City ground
        const groundGeometry = new THREE.PlaneGeometry(200, 200);
        const groundMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x2d5a27,
            shininess: 30 
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);
        
        // Create buildings
        const buildings = [];
        cityData.city.buildings.forEach(buildingData => {
            const geometry = new THREE.BoxGeometry(
                buildingData.width, 
                buildingData.height, 
                buildingData.depth
            );
            
            const material = new THREE.MeshPhongMaterial({ 
                color: buildingData.color,
                transparent: true,
                opacity: 0.8
            });
            
            const building = new THREE.Mesh(geometry, material);
            building.position.set(buildingData.x, buildingData.height / 2, buildingData.z);
            building.userData = buildingData;
            
            // Add windows (code lines)
            for (let i = 0; i < buildingData.windows; i++) {
                const windowGeometry = new THREE.PlaneGeometry(0.5, 0.5);
                const windowMaterial = new THREE.MeshBasicMaterial({ 
                    color: 0xffff00,
                    transparent: true,
                    opacity: 0.7
                });
                const window = new THREE.Mesh(windowGeometry, windowMaterial);
                
                const floor = Math.floor(i / 5);
                const windowInFloor = i % 5;
                
                window.position.set(
                    (buildingData.width / 2) - 1,
                    (floor * 2) + 1,
                    (buildingData.depth / 2) - 1 - (windowInFloor * 1.5)
                );
                window.rotation.y = Math.PI / 2;
                
                building.add(window);
            }
            
            scene.add(building);
            buildings.push(building);
        });

"""