#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: datetime, json, random, time
# ROLE: CODE CITY APOCALYPSE - Visualizes errors as building fires, monsters, and aerial
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
CODE CITY APOCALYPSE - Visualizes errors as building fires, monsters, and aerial attacks
"""
import json
import random
import time
from datetime import datetime

class CodeCityApocalypse:
    def __init__(self):
        self.buildings = []  # Files as buildings
        self.disasters = []  # Active disasters
        self.monsters = []   # Rampage monsters
        self.planes = []     # Red Baron flybys
        self.error_count = 0
        
        # Disaster types with ASCII art
        self.disaster_types = {
            "syntax_error": {"name": "Building Fire", "symbol": "🔥", "severity": 2},
            "runtime_error": {"name": "Monster Attack", "symbol": "👾", "severity": 3},
            "import_error": {"name": "Red Baron Strike", "symbol": "✈️", "severity": 4},
            "logic_error": {"name": "Earthquake", "symbol": "🌋", "severity": 3},
            "memory_error": {"name": "Alien Invasion", "symbol": "🛸", "severity": 5}
        }
        
        # Monster types (Rampage style)
        self.monster_types = [
            {"name": "George", "symbol": "🦍", "health": 100, "attack": "SMASH"},
            {"name": "Lizzie", "symbol": "🦖", "health": 150, "attack": "CHOMP"}, 
            {"name": "Ralph", "symbol": "🐺", "health": 80, "attack": "SLASH"}
        ]
    
    def scan_project(self, directory="."):
        """Scan project and create code city"""
        import os
        self.buildings = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.py', '.ts', '.tsx', '.js')):
                    building = {
                        "name": file,
                        "path": os.path.join(root, file),
                        "height": min(50, os.path.getsize(os.path.join(root, file)) // 100),
                        "health": 100,
                        "errors": [],
                        "last_modified": datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))),
                        "symbol": "🏢" if file.endswith('.py') else "🏬"
                    }
                    self.buildings.append(building)
        
        print(f"🏙️ CODE CITY BUILT: {len(self.buildings)} buildings")
        return self.buildings
    
    def trigger_disaster(self, error_type, file_path, error_message):
        """Trigger a disaster in the code city"""
        disaster = self.disaster_types.get(error_type, self.disaster_types["syntax_error"])
        
        # Find the building (file)
        target_building = None
        for building in self.buildings:
            if building["path"] == file_path:
                target_building = building
                break
        
        if not target_building:
            # Create a new building for this error
            target_building = {
                "name": file_path.split('/')[-1],
                "path": file_path,
                "height": 30,
                "health": 100,
                "errors": [],
                "symbol": "🏚️"
            }
            self.buildings.append(target_building)
        
        # Add error to building
        target_building["errors"].append({
            "type": error_type,
            "message": error_message,
            "timestamp": datetime.now(),
            "disaster": disaster
        })
        
        # Damage building
        damage = disaster["severity"] * 10
        target_building["health"] = max(0, target_building["health"] - damage)
        
        # Add to active disasters
        disaster_event = {
            "type": error_type,
            "building": target_building["name"],
            "disaster": disaster,
            "start_time": datetime.now(),
            "position": random.randint(0, len(self.buildings) - 1)
        }
        self.disasters.append(disaster_event)
        
        self.error_count += 1
        print(f"💥 DISASTER: {disaster['name']} at {target_building['name']}! Health: {target_building['health']}%")
        
        # Chance to spawn monster on big errors
        if disaster["severity"] >= 3 and random.random() > 0.7:
            self.spawn_monster(target_building)
        
        # Chance for Red Baron flyby on import errors
        if error_type == "import_error" and random.random() > 0.8:
            self.red_baron_attack()
        
        return disaster_event
    
    def spawn_monster(self, building):
        """Spawn a Rampage-style monster"""
        monster = random.choice(self.monster_types).copy()
        monster["target_building"] = building["name"]
        monster["position"] = self.buildings.index(building)
        monster["last_attack"] = datetime.now()
        
        self.monsters.append(monster)
        print(f"👾 MONSTER SPAWN: {monster['name']} {monster['symbol']} attacking {building['name']}!")
        
        return monster
    
    def red_baron_attack(self):
        """Red Baron aerial attack"""
        plane = {
            "name": "Red Baron",
            "symbol": "✈️",
            "position": 0,
            "direction": 1,
            "bombs_dropped": 0
        }
        self.planes.append(plane)
        print(f"✈️ RED BARON INBOUND! Air raid on Code City!")
        
        return plane
    
    def update_city(self):
        """Update the city state - monsters attack, planes fly, disasters spread"""
        # Monsters attack buildings
        for monster in self.monsters[:]:
            if monster["position"] < len(self.buildings):
                building = self.buildings[monster["position"]]
                damage = random.randint(5, 15)
                building["health"] = max(0, building["health"] - damage)
                
                print(f"{monster['symbol']} {monster['name']} {monster['attack']} {building['name']}! -{damage}%")
                
                # Monster dies if building collapses or random chance
                if building["health"] <= 0 or random.random() > 0.95:
                    print(f"💀 {monster['name']} was defeated!")
                    self.monsters.remove(monster)
        
        # Planes fly and bomb
        for plane in self.planes[:]:
            plane["position"] += plane["direction"]
            
            # Drop bomb randomly
            if random.random() > 0.7 and plane["position"] < len(self.buildings):
                building = self.buildings[plane["position"]]
                damage = random.randint(10, 25)
                building["health"] = max(0, building["health"] - damage)
                plane["bombs_dropped"] += 1
                
                print(f"💣 {plane['symbol']} BOMB DROP on {building['name']}! -{damage}%")
            
            # Plane leaves screen
            if plane["position"] >= len(self.buildings):
                print(f"✈️ {plane['name']} flies off into the sunset!")
                self.planes.remove(plane)
        
        # Disasters eventually end
        for disaster in self.disasters[:]:
            if (datetime.now() - disaster["start_time"]).seconds > 10:
                print(f"✅ {disaster['disaster']['name']} at {disaster['building']} contained!")
                self.disasters.remove(disaster)
    
    def render_city(self):
        """Render the code city with ASCII art"""
        print("\n" + "="*80)
        print("🏙️  CODE CITY APOCALYPSE - REAL-TIME VISUALIZATION")
        print("="*80)
        
        # City skyline
        city_line = []
        for i, building in enumerate(self.buildings):
            # Building character based on health
            if building["health"] <= 0:
                symbol = "💀"
            elif building["health"] < 30:
                symbol = "🔥"
            elif building["health"] < 60:
                symbol = "🚒"
            else:
                symbol = building["symbol"]
            
            # Add disasters and monsters at this position
            for disaster in self.disasters:
                if disaster["position"] == i:
                    symbol = disaster["disaster"]["symbol"]
            
            for monster in self.monsters:
                if monster["position"] == i:
                    symbol = monster["symbol"]
            
            for plane in self.planes:
                if plane["position"] == i:
                    symbol = plane["symbol"]
            
            city_line.append(symbol)
        
        print("CITY: " + " ".join(city_line))
        
        # Building status
        print("\n🏢 BUILDING STATUS:")
        for building in self.buildings[:10]:
            health_bar = "█" * (building["health"] // 10) + "░" * (10 - (building["health"] // 10))
            print(f"  {building['symbol']} {building['name']:20} [{health_bar}] {building['health']}%")
        
        # Active disasters
        if self.disasters:
            print("\n💥 ACTIVE DISASTERS:")
            for disaster in self.disasters:
                print(f"  {disaster['disaster']['symbol']} {disaster['disaster']['name']} at {disaster['building']}")
        
        # Monsters
        if self.monsters:
            print("\n👾 RAMPAGE MONSTERS:")
            for monster in self.monsters:
                print(f"  {monster['symbol']} {monster['name']} attacking {monster['target_building']} (HP: {monster['health']})")
        
        # Planes
        if self.planes:
            print("\n✈️ AERIAL ATTACKS:")
            for plane in self.planes:
                print(f"  {plane['symbol']} {plane['name']} - Bombs: {plane['bombs_dropped']}")
        
        print(f"\n📊 CITY STATS: Buildings: {len(self.buildings)} | Errors: {self.error_count} | Active Disasters: {len(self.disasters)}")
        print("="*80)
    
    def monitor_errors(self):
        """Monitor for errors and trigger disasters"""
        print("👁️ CODE CITY APOCALYPSE MONITOR ACTIVATED!")
        print("Watching for errors to turn into disasters...")
        
        # Simulate error monitoring
        error_simulation = [
            ("syntax_error", "auth.py", "Invalid syntax on line 42"),
            ("import_error", "api_server.py", "Module not found: fastapi"),
            ("runtime_error", "dashboard.py", "Division by zero at line 15"),
            ("logic_error", "form_handler.py", "Infinite loop detected"),
            ("memory_error", "data_processor.py", "Out of memory")
        ]
        
        for error_type, file_path, message in error_simulation:
            time.sleep(3)
            self.trigger_disaster(error_type, file_path, message)
            self.update_city()
            self.render_city()
        
        # Keep updating for ongoing chaos
        for _ in range(5):
            time.sleep(2)
            self.update_city()
            self.render_city()

def main():
    apocalypse = CodeCityApocalypse()
    
    # Build the city from current project
    apocalypse.scan_project(".")
    
    # Start monitoring for errors
    apocalypse.monitor_errors()

if __name__ == "__main__":
    main()