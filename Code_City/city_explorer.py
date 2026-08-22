# FILE: /home/bleaknarratives/Code-City-Apocalypse/city_explorer.py  
# RUN: cd /home/bleaknarratives/Code-City-Apocalypse && python3 city_explorer.py

import os
from pathlib import Path

class CodeCity:
    def __init__(self, scan_path="/home/bleaknarratives/Code-City-Apocalypse"):
        self.scan_path = Path(scan_path)
        self.city = self.build_city()
    
    def build_city(self):
        """Scan file system and build city representation"""
        print("🏙️  Building Code City...")
        
        city = {
            'skyscrapers': [],    # Large code files (>10KB)
            'office_buildings': [], # Medium code files
            'houses': [],          # Small files
            'factories': [],       # Build/config files
            'parks': [],           # Documentation
            'construction': []     # Recent/modified files
        }
        
        for file_path in self.scan_path.rglob("*"):
            if file_path.is_file():
                building = self.analyze_building(file_path)
                if building:
                    city[building['type']].append(building)
        
        return city
    
    def analyze_building(self, file_path):
        """Determine what kind of building this file represents"""
        try:
            stats = file_path.stat()
            size = stats.st_size
            name = file_path.name
            ext = file_path.suffix
            
            # Skip non-code files for now (grey them out)
            if ext not in ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.json']:
                return None
            
            building = {
                'name': name,
                'path': str(file_path),
                'size': size,
                'height': min(size // 100, 50),  # Max 50 stories
                'last_modified': stats.st_mtime
            }
            
            # Determine building type
            if size > 10000:
                building['type'] = 'skyscrapers'
                building['color'] = 'blue'
            elif size > 1000:
                building['type'] = 'office_buildings' 
                building['color'] = 'green'
            elif 'test' in name or 'spec' in name:
                building['type'] = 'houses'
                building['color'] = 'yellow'
            elif 'config' in name or 'settings' in name:
                building['type'] = 'factories'
                building['color'] = 'red'
            else:
                building['type'] = 'houses'
                building['color'] = 'gray'
            
            return building
            
        except:
            return None
    
    def print_city_map(self):
        """Display the city layout"""
        print("\n" + "="*50)
        print("🏙️  CODE CITY LAYOUT")
        print("="*50)
        
        for building_type, buildings in self.city.items():
            if buildings:
                print(f"\n{building_type.upper().replace('_', ' ')}:")
                for building in buildings[:5]:  # Show first 5
                    print(f"  🏢 {building['name']} ({building['height']} stories)")
        
        total_buildings = sum(len(buildings) for buildings in self.city.values())
        print(f"\n📊 CITY STATS: {total_buildings} code buildings found")

# Build and display the city
city = CodeCity("/home/bleaknarratives/Code-City-Apocalypse/code_tool")  # Scan our workspace
city.print_city_map()