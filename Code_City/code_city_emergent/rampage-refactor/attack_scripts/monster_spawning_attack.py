#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: datetime, json, logging, os, pathlib, random, typing
# ROLE: MONSTER SPAWNING ATTACK - RAMPAGE REFACTOR SPECIFIC
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]

"""
MONSTER SPAWNING ATTACK - RAMPAGE REFACTOR SPECIFIC
Simulates bug injection attacks that create "monsters" in the code city
"""

import os
import json
import random
from pathlib import Path
from typing import Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MonsterSpawningAttack:
    """Simulates bug injection attacks that create monsters in the Rampage Refactor code city"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).absolute()
        self.target_files = []
        self.spawn_log = []
        self.successful_spawns = []
        
        # Bug types that create different monsters
        self.bug_types = [
            {
                'type': 'syntax_error',
                'monster': 'gorilla',
                'description': 'Syntax errors that break compilation',
                'severity': 9,
                'color': '#ff0000',
                'examples': [
                    'def broken_function(\n    print("unclosed parenthesis")',
                    'if True\n    print("missing indentation")',
                    'return without_value',
                    'import non_existent_module_12345'
                ]
            },
            {
                'type': 'logic_error',
                'monster': 'lizard',
                'description': 'Logical errors that cause incorrect behavior',
                'severity': 7,
                'color': '#00ff00',
                'examples': [
                    'if x > 5 and x < 3:  # Impossible condition',
                    'while True:  # Infinite loop',
                    'return x + y - y  # Useless operation',
                    'if condition: return True\nelse: return True  # Redundant branch'
                ]
            },
            {
                'type': 'security_vulnerability',
                'monster': 'wolf',
                'description': 'Security vulnerabilities that can be exploited',
                'severity': 10,
                'color': '#0000ff',
                'examples': [
                    'password = request.GET["password"]  # No validation',
                    'exec(user_input)  # Code injection',
                    'pickle.load(open("data.pkl", "rb"))  # Unsafe deserialization',
                    'sql = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection'
                ]
            },
            {
                'type': 'performance_issue',
                'monster': 'dinosaur',
                'description': 'Performance bottlenecks and inefficiencies',
                'severity': 5,
                'color': '#ffff00',
                'examples': [
                    'for i in range(1000000):\n    for j in range(1000000):\n        pass  # Nested loops',
                    'data = [x for x in range(1000000) if x in [y for y in range(1000000)]]  # Inefficient',
                    'while True:\n    time.sleep(0.1)  # Busy waiting',
                    'def recursive_function():\n    recursive_function()  # No base case'
                ]
            },
            {
                'type': 'code_smell',
                'monster': 'rat',
                'description': 'Poor coding practices and anti-patterns',
                'severity': 3,
                'color': '#888888',
                'examples': [
                    'def do_everything():  # God function',
                    'a = b = c = d = e = f = g = h = i = j = 0  # Too many assignments',
                    'try:\n    risky_operation()\nexcept:\n    pass  # Silent exception',
                    'x = x if x else x  # Useless condition'
                ]
            },
            {
                'type': 'dead_code',
                'monster': 'ghost',
                'description': 'Unreachable or unused code',
                'severity': 2,
                'color': '#ffffff',
                'examples': [
                    'def unused_function():\n    pass  # Never called',
                    'if False:\n    print("This never runs")',
                    'x = 42  # Never used',
                    'try:\n    working_code()\nexcept ExceptionThatNeverHappens:\n    pass'
                ]
            }
        ]
    
    def scan_for_targets(self) -> List[Dict]:
        """Find files suitable for bug injection"""
        logger.info(f"🔍 Scanning {self.target_path} for bug injection targets...")
        
        targets = []
        
        # Find all code files
        code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp', '.go', '.rs', '.rb', '.php']
        
        for ext in code_extensions:
            files = list(self.target_path.rglob(f'*{ext}'))
            for file_path in files:
                try:
                    stats = file_path.stat()
                    if stats.st_size > 0 and stats.st_size < 512 * 1024:  # 512KB max
                        targets.append({
                            'file': str(file_path),
                            'size': stats.st_size,
                            'extension': ext,
                            'lines': len(file_path.read_text(encoding='utf-8', errors='ignore').split('\n'))
                        })
                except Exception as e:
                    logger.warning(f"Error scanning {file_path}: {e}")
        
        self.target_files = targets
        logger.info(f"✅ Found {len(targets)} potential bug injection targets")
        
        return targets
    
    def launch_spawning_attack(self, target_file: str = None) -> Dict:
        """Simulate monster spawning attack (bug injection)"""
        logger.info("🚀 Launching monster spawning attack...")
        
        attack_results = {
            'attack_type': 'monster_spawning',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'files_infected': [],
            'monsters_spawned': [],
            'spawn_success': False
        }
        
        # If no specific target, pick a random file
        if not target_file and self.target_files:
            target_file = random.choice(self.target_files)['file']
        
        if target_file:
            logger.info(f"🎯 Targeting: {target_file}")
            
            try:
                with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
                    original_content = f.read()
                
                # Determine number of bugs to inject (1-3 per file)
                num_bugs = random.randint(1, 3)
                logger.info(f"🐛 Injecting {num_bugs} bugs...")
                
                # Inject bugs and spawn monsters
                for i in range(num_bugs):
                    bug_type = random.choice(self.bug_types)
                    example = random.choice(bug_type['examples'])
                    
                    # Simulate injection (don't actually modify files for safety)
                    if random.random() < 0.85:  # 85% success rate
                        attack_results['spawn_success'] = True
                        attack_results['files_infected'].append(target_file)
                        
                        # Create monster data (compatible with Rampage Refactor format)
                        monster = {
                            'id': f"{target_file}_L{random.randint(1, 100)}_{bug_type['type']}",
                            'type': bug_type['type'],
                            'building_id': target_file,
                            'file_path': target_file,
                            'file_name': os.path.basename(target_file),
                            'position': {
                                'x': random.uniform(-50, 50),
                                'y': random.uniform(5, 50),
                                'z': random.uniform(-50, 50)
                            },
                            'severity': bug_type['severity'],
                            'message': f"{bug_type['description']}: {example[:50]}...",
                            'line': random.randint(1, 100),
                            'health': bug_type['severity'] * 10,
                            'color': bug_type['color'],
                            'monster_type': bug_type['monster']
                        }
                        
                        attack_results['monsters_spawned'].append(monster)
                        
                        logger.warning(f"⚠️  Spawned {bug_type['monster']} monster from {bug_type['type']}")
                        logger.warning(f"🐉 Monster ID: {monster['id']}")
                        logger.warning(f"📍 Position: ({monster['position']['x']:.1f}, {monster['position']['y']:.1f}, {monster['position']['z']:.1f})")
                        logger.warning(f"💀 Severity: {bug_type['severity']}/10")
                        
                        # Simulate the effects
                        if bug_type['severity'] >= 9:
                            logger.warning("🔥 CRITICAL BUG DETECTED!")
                        elif bug_type['severity'] >= 7:
                            logger.warning("⚠️  HIGH SEVERITY BUG!")
                        else:
                            logger.warning("🟡 MEDIUM SEVERITY BUG!")
                    else:
                        logger.info(f"🟢 Bug injection attempt {i+1} failed")
                        
            except Exception as e:
                logger.error(f"Spawning failed: {e}")
        
        if attack_results['spawn_success']:
            logger.warning("🔴 MONSTER SPAWNING ATTACK SUCCESSFUL!")
            logger.warning(f"🐉 Spawned {len(attack_results['monsters_spawned'])} monsters")
            logger.warning(f"💀 Infected {len(attack_results['files_infected'])} files")
        else:
            logger.info("🟢 Monster spawning attack blocked")
        
        self.successful_spawns.append(attack_results)
        return attack_results
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'monster_spawning',
            'target': str(self.target_path),
            'timestamp': datetime.now().isoformat(),
            'target_files_found': len(self.target_files),
            'target_files': self.target_files,
            'spawn_attempts': len(self.spawn_log),
            'successful_spawns': len(self.successful_spawns),
            'files_infected': len([item for attack in self.successful_spawns for item in attack.get('files_infected', [])]),
            'monsters_spawned': len([item for attack in self.successful_spawns for item in attack.get('monsters_spawned', [])]),
            'monster_details': [item for attack in self.successful_spawns for item in attack.get('monsters_spawned', [])],
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security and code quality recommendations"""
        recommendations = [
            "✅ Implement static code analysis (SonarQube, ESLint, Pylint)",
            "✅ Use automated testing with high coverage",
            "✅ Implement code review processes",
            "✅ Use type checking and linting tools",
            "✅ Implement continuous integration with quality gates",
            "✅ Use pre-commit hooks for code quality checks",
            "✅ Implement automated bug detection tools",
            "✅ Use code formatting tools consistently",
            "✅ Implement technical debt tracking",
            "✅ Conduct regular code audits and refactoring"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"monster_spawning_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file
    
    def generate_rampage_compatible_output(self) -> Dict:
        """Generate output compatible with Rampage Refactor monster format"""
        monsters = []
        buildings = []
        
        # Create building for each infected file
        for attack in self.successful_spawns:
            for file_path in attack.get('files_infected', []):
                if file_path not in [b['id'] for b in buildings]:
                    building = {
                        'id': file_path,
                        'name': os.path.basename(file_path),
                        'path': file_path,
                        'full_path': file_path,
                        'type': os.path.splitext(file_path)[1][1:],
                        'size': os.path.getsize(file_path),
                        'lines': len(open(file_path, 'r', encoding='utf-8', errors='ignore').read().split('\n')),
                        'complexity': random.randint(5, 50),
                        'health': max(0, 100 - len(attack.get('monsters_spawned', [])) * 5),
                        'position': {
                            'x': random.uniform(-100, 100),
                            'y': 0,
                            'z': random.uniform(-100, 100)
                        },
                        'dimensions': {
                            'width': random.uniform(8, 30),
                            'height': random.uniform(10, 150),
                            'depth': random.uniform(8, 30)
                        },
                        'color': self._get_file_color(file_path)
                    }
                    buildings.append(building)
            
            # Add all monsters
            monsters.extend(attack.get('monsters_spawned', []))
        
        return {
            'buildings': buildings,
            'monsters': monsters,
            'total_files': len(buildings),
            'total_errors': len(monsters),
            'root_path': str(self.target_path),
            'attack_source': 'monster_spawning_attack'
        }
    
    def _get_file_color(self, file_path: str) -> str:
        """Get building color based on file type"""
        ext = os.path.splitext(file_path)[1].lower()
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
        return colors.get(ext, '#6c757d')


def main():
    import sys
    import argparse
    import re
    
    parser = argparse.ArgumentParser(description='Monster Spawning Attack Simulator')
    parser.add_argument('target', help='Target directory to attack')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for targets')
    parser.add_argument('--rampage-output', action='store_true', help='Generate Rampage Refactor compatible output')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Target not found: {args.target}")
        return
    
    attack = MonsterSpawningAttack(args.target)
    
    print("🐉 MONSTER SPAWNING ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for targets
    targets = attack.scan_for_targets()
    
    if targets:
        print(f"🎯 Found {len(targets)} potential bug injection targets:")
        total_size = sum(t['size'] for t in targets)
        print(f"  • Total files: {len(targets)}")
        print(f"  • Total size: {total_size:,} bytes")
        print(f"  • Average file size: {total_size // len(targets):,} bytes")
        print(f"  • Available monster types: {', '.join(set(bt['monster'] for bt in attack.bug_types))}")
    else:
        print("✅ No suitable targets found")
    
    if not args.scan_only:
        print("\n🚀 Launching monster spawning attack...")
        results = attack.launch_spawning_attack()
        
        if results['spawn_success']:
            print("🔴 MONSTER SPAWNING ATTACK SUCCESSFUL!")
            print(f"🐉 Spawned {len(results['monsters_spawned'])} monsters:")
            
            # Show monster types
            monster_types = {}
            for monster in results['monsters_spawned']:
                m_type = monster.get('monster_type', 'unknown')
                monster_types[m_type] = monster_types.get(m_type, 0) + 1
            
            for m_type, count in monster_types.items():
                print(f"  • {count}x {m_type}")
            
            print(f"💀 Infected {len(results['files_infected'])} files")
        else:
            print("🟢 Monster spawning attack blocked")
        
        if args.rampage_output:
            print("\n🎮 Generating Rampage Refactor compatible output...")
            rampage_data = attack.generate_rampage_compatible_output()
            output_file = f"rampage_monsters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(rampage_data, f, indent=2)
            
            print(f"📄 Rampage output saved to: {output_file}")
            print(f"  • Buildings: {len(rampage_data['buildings'])}")
            print(f"  • Monsters: {len(rampage_data['monsters'])}")
    
    # Save report
    report_file = args.report or f"monster_spawning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()