#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: datetime, json, logging, os, pathlib, random, typing
# ROLE: BUILDING DESTRUCTION ATTACK - RAMPAGE REFACTOR SPECIFIC
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]

"""
BUILDING DESTRUCTION ATTACK - RAMPAGE REFACTOR SPECIFIC
Simulates file deletion attacks that destroy "buildings" in the code city
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


class BuildingDestructionAttack:
    """Simulates file deletion attacks that destroy buildings in the Rampage Refactor code city"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).absolute()
        self.target_files = []
        self.destruction_log = []
        self.successful_destructions = []
        
        # Destruction strategies
        self.destruction_strategies = [
            {
                'name': 'complete_deletion',
                'description': 'Permanently delete the file',
                'severity': 'critical',
                'recoverable': False
            },
            {
                'name': 'content_wipe',
                'description': 'Empty file contents but keep the file',
                'severity': 'high',
                'recoverable': True
            },
            {
                'name': 'rename_obfuscation',
                'description': 'Rename file to obscure name',
                'severity': 'medium',
                'recoverable': True
            },
            {
                'name': 'permission_denial',
                'description': 'Change file permissions to deny access',
                'severity': 'medium',
                'recoverable': True
            },
            {
                'name': 'move_to_hidden',
                'description': 'Move file to hidden directory',
                'severity': 'low',
                'recoverable': True
            }
        ]
    
    def scan_for_targets(self) -> List[Dict]:
        """Find files suitable for destruction"""
        logger.info(f"🔍 Scanning {self.target_path} for destruction targets...")
        
        targets = []
        
        # Find all code files
        code_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp', '.go', '.rs', '.rb', '.php']
        
        for ext in code_extensions:
            files = list(self.target_path.rglob(f'*{ext}'))
            for file_path in files:
                try:
                    stats = file_path.stat()
                    if stats.st_size > 0 and stats.st_size < 1024 * 1024:  # 1MB max
                        targets.append({
                            'file': str(file_path),
                            'size': stats.st_size,
                            'extension': ext,
                            'lines': len(file_path.read_text(encoding='utf-8', errors='ignore').split('\n')),
                            'importance': self._calculate_importance(file_path)
                        })
                except Exception as e:
                    logger.warning(f"Error scanning {file_path}: {e}")
        
        self.target_files = targets
        logger.info(f"✅ Found {len(targets)} potential destruction targets")
        
        return targets
    
    def _calculate_importance(self, file_path: Path) -> int:
        """Calculate file importance based on name and content"""
        importance = 1
        
        # Check filename
        filename = file_path.name.lower()
        if any(keyword in filename for keyword in ['main', 'app', 'core', 'engine', 'server', 'config']):
            importance += 2
        
        # Check file content
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Count critical elements
            if file_path.suffix == '.py':
                importance += content.count('def ') * 0.5
                importance += content.count('class ') * 1.0
                importance += content.count('import ') * 0.2
            
            # Check for main functions
            if 'def main(' in content or 'if __name__ == "__main__"' in content:
                importance += 3
                
        except Exception as e:
            logger.warning(f"Error analyzing {file_path}: {e}")
        
        return min(10, max(1, importance))
    
    def launch_destruction_attack(self, target_file: str = None) -> Dict:
        """Simulate building destruction attack (file deletion)"""
        logger.info("🚀 Launching building destruction attack...")
        
        attack_results = {
            'attack_type': 'building_destruction',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'files_destroyed': [],
            'destruction_success': False,
            'destruction_details': [],
            'recoverable_files': [],
            'permanent_loss': []
        }
        
        # If no specific target, pick a high-importance file
        if not target_file and self.target_files:
            # Sort by importance and pick top candidate
            sorted_targets = sorted(self.target_files, key=lambda x: x['importance'], reverse=True)
            target_file = sorted_targets[0]['file']
        
        if target_file:
            logger.info(f"🎯 Targeting: {target_file}")
            
            try:
                file_info = next((f for f in self.target_files if f['file'] == target_file), None)
                if file_info:
                    logger.info(f"📊 Target importance: {file_info['importance']}/10")
                    logger.info(f"📊 Target size: {file_info['size']:,} bytes")
                    logger.info(f"📊 Target lines: {file_info['lines']} lines")
                
                # Choose destruction strategy based on importance
                if file_info and file_info['importance'] >= 8:
                    strategy = next(s for s in self.destruction_strategies if s['name'] == 'complete_deletion')
                elif file_info and file_info['importance'] >= 5:
                    strategy = random.choice([
                        s for s in self.destruction_strategies 
                        if s['name'] in ['complete_deletion', 'content_wipe', 'rename_obfuscation']
                    ])
                else:
                    strategy = random.choice(self.destruction_strategies)
                
                logger.info(f"🔧 Using strategy: {strategy['name']} ({strategy['severity']} severity)")
                
                # Simulate destruction (don't actually delete files for safety)
                if random.random() < 0.9:  # 90% success rate
                    attack_results['destruction_success'] = True
                    attack_results['files_destroyed'].append(target_file)
                    
                    # Simulate different destruction effects
                    if strategy['name'] == 'complete_deletion':
                        destruction_result = f"File {target_file} permanently deleted"
                        attack_results['permanent_loss'].append(target_file)
                    elif strategy['name'] == 'content_wipe':
                        destruction_result = f"File {target_file} contents wiped (empty file)"
                        attack_results['recoverable_files'].append(target_file)
                    elif strategy['name'] == 'rename_obfuscation':
                        new_name = f".hidden_{os.path.basename(target_file)}.bak"
                        destruction_result = f"File {target_file} renamed to {new_name}"
                        attack_results['recoverable_files'].append(target_file)
                    elif strategy['name'] == 'permission_denial':
                        destruction_result = f"File {target_file} permissions set to 000 (no access)"
                        attack_results['recoverable_files'].append(target_file)
                    elif strategy['name'] == 'move_to_hidden':
                        destruction_result = f"File {target_file} moved to hidden directory"
                        attack_results['recoverable_files'].append(target_file)
                    else:
                        destruction_result = f"File {target_file} destroyed using {strategy['name']}"
                    
                    # Log destruction details
                    attack_results['destruction_details'].append({
                        'file': target_file,
                        'strategy': strategy['name'],
                        'severity': strategy['severity'],
                        'importance': file_info['importance'] if file_info else 1,
                        'result': destruction_result,
                        'recoverable': strategy['recoverable'],
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logger.warning(f"⚠️  Successfully destroyed {target_file}")
                    logger.warning(f"💀 {destruction_result}")
                    
                    # Simulate the effects
                    if strategy['name'] == 'complete_deletion':
                        logger.warning("🔥 CRITICAL FILE LOSS - IRRECOVERABLE!")
                    elif not strategy['recoverable']:
                        logger.warning("💀 PERMANENT DATA LOSS!")
                    else:
                        logger.warning("🟡 FILE DAMAGED - POTENTIALLY RECOVERABLE")
                    
                else:
                    logger.info("🟢 Destruction attempt failed")
                    
            except Exception as e:
                logger.error(f"Destruction failed: {e}")
        
        if attack_results['destruction_success']:
            logger.warning("🔴 BUILDING DESTRUCTION ATTACK SUCCESSFUL!")
            logger.warning(f"💀 Destroyed {len(attack_results['files_destroyed'])} files")
            if attack_results['permanent_loss']:
                logger.warning(f"🔥 {len(attack_results['permanent_loss'])} files permanently lost!")
            if attack_results['recoverable_files']:
                logger.warning(f"🟡 {len(attack_results['recoverable_files'])} files potentially recoverable")
        else:
            logger.info("🟢 Building destruction attack blocked")
        
        self.successful_destructions.append(attack_results)
        return attack_results
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'building_destruction',
            'target': str(self.target_path),
            'timestamp': datetime.now().isoformat(),
            'target_files_found': len(self.target_files),
            'target_files': self.target_files,
            'destruction_attempts': len(self.destruction_log),
            'successful_destructions': len(self.successful_destructions),
            'files_destroyed': len([item for attack in self.successful_destructions for item in attack.get('files_destroyed', [])]),
            'permanent_loss': len([item for attack in self.successful_destructions for item in attack.get('permanent_loss', [])]),
            'recoverable_files': len([item for attack in self.successful_destructions for item in attack.get('recoverable_files', [])]),
            'destruction_details': [item for attack in self.successful_destructions for item in attack.get('destruction_details', [])],
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security and backup recommendations"""
        recommendations = [
            "✅ Implement regular automated backups",
            "✅ Use version control with remote repositories",
            "✅ Implement file system monitoring and alerts",
            "✅ Use proper file permissions and access controls",
            "✅ Implement change detection and anomaly detection",
            "✅ Use immutable infrastructure patterns",
            "✅ Implement disaster recovery procedures",
            "✅ Use file integrity monitoring tools",
            "✅ Implement proper error handling and logging",
            "✅ Conduct regular security audits and penetration testing"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"building_destruction_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file
    
    def generate_rampage_compatible_output(self) -> Dict:
        """Generate output compatible with Rampage Refactor showing destroyed buildings"""
        destroyed_buildings = []
        surviving_buildings = []
        monsters = []  # Destruction can leave behind "ghost" monsters
        
        # Process all files
        for attack in self.successful_destructions:
            for file_path in attack.get('files_destroyed', []):
                # Check if file was permanently destroyed
                if file_path in attack.get('permanent_loss', []):
                    # Create a "destroyed" building marker
                    destroyed_buildings.append({
                        'id': file_path,
                        'name': os.path.basename(file_path),
                        'path': file_path,
                        'full_path': file_path,
                        'type': os.path.splitext(file_path)[1][1:],
                        'destroyed': True,
                        'destruction_type': next(
                            (d['strategy'] for d in attack['destruction_details'] if d['file'] == file_path),
                            'unknown'
                        ),
                        'position': {
                            'x': random.uniform(-100, 100),
                            'y': 0,
                            'z': random.uniform(-100, 100)
                        },
                        'color': '#000000',  # Black for destroyed
                        'ghost_monster': {
                            'id': f"ghost_{file_path}",
                            'type': 'ghost_building',
                            'building_id': file_path,
                            'position': {
                                'x': random.uniform(-100, 100),
                                'y': 5,
                                'z': random.uniform(-100, 100)
                            },
                            'severity': 10,
                            'message': f"Building destroyed: {os.path.basename(file_path)}",
                            'health': 100,
                            'color': '#888888'
                        }
                    })
                else:
                    # File is damaged but recoverable
                    surviving_buildings.append({
                        'id': file_path,
                        'name': os.path.basename(file_path),
                        'path': file_path,
                        'full_path': file_path,
                        'type': os.path.splitext(file_path)[1][1:],
                        'damaged': True,
                        'health': random.randint(10, 50),
                        'position': {
                            'x': random.uniform(-100, 100),
                            'y': 0,
                            'z': random.uniform(-100, 100)
                        },
                        'dimensions': {
                            'width': random.uniform(4, 15),  # Smaller due to damage
                            'height': random.uniform(5, 50),  # Smaller due to damage
                            'depth': random.uniform(4, 15)   # Smaller due to damage
                        },
                        'color': self._get_file_color(file_path)
                    })
        
        # Add ghost monsters for destroyed buildings
        for building in destroyed_buildings:
            if 'ghost_monster' in building:
                monsters.append(building['ghost_monster'])
        
        return {
            'buildings': surviving_buildings,
            'destroyed_buildings': destroyed_buildings,
            'monsters': monsters,
            'total_files': len(surviving_buildings),
            'total_destroyed': len(destroyed_buildings),
            'total_errors': len(monsters),
            'root_path': str(self.target_path),
            'attack_source': 'building_destruction_attack'
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
    
    parser = argparse.ArgumentParser(description='Building Destruction Attack Simulator')
    parser.add_argument('target', help='Target directory to attack')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for targets')
    parser.add_argument('--rampage-output', action='store_true', help='Generate Rampage Refactor compatible output')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Target not found: {args.target}")
        return
    
    attack = BuildingDestructionAttack(args.target)
    
    print("🏚️ BUILDING DESTRUCTION ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for targets
    targets = attack.scan_for_targets()
    
    if targets:
        print(f"🎯 Found {len(targets)} potential destruction targets:")
        total_size = sum(t['size'] for t in targets)
        avg_importance = sum(t['importance'] for t in targets) / len(targets)
        print(f"  • Total files: {len(targets)}")
        print(f"  • Total size: {total_size:,} bytes")
        print(f"  • Average importance: {avg_importance:.1f}/10")
        print(f"  • High-importance files (≥8/10): {sum(1 for t in targets if t['importance'] >= 8)}")
    else:
        print("✅ No suitable targets found")
    
    if not args.scan_only:
        print("\n🚀 Launching building destruction attack...")
        results = attack.launch_destruction_attack()
        
        if results['destruction_success']:
            print("🔴 DESTRUCTION ATTACK SUCCESSFUL!")
            print(f"💀 Destroyed {len(results['files_destroyed'])} files:")
            
            # Show destruction summary
            if results['permanent_loss']:
                print(f"  • 🔥 {len(results['permanent_loss'])} files permanently lost")
            if results['recoverable_files']:
                print(f"  • 🟡 {len(results['recoverable_files'])} files potentially recoverable")
            
            # Show most severe destruction
            if results['destruction_details']:
                most_severe = max(results['destruction_details'], key=lambda x: x['importance'])
                print(f"\n💀 Most severe destruction:")
                print(f"  • File: {os.path.basename(most_severe['file'])}")
                print(f"  • Importance: {most_severe['importance']}/10")
                print(f"  • Strategy: {most_severe['strategy']}")
                print(f"  • Result: {most_severe['result']}")
        else:
            print("🟢 Building destruction attack blocked")
        
        if args.rampage_output:
            print("\n🎮 Generating Rampage Refactor compatible output...")
            rampage_data = attack.generate_rampage_compatible_output()
            output_file = f"rampage_destruction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(rampage_data, f, indent=2)
            
            print(f"📄 Rampage output saved to: {output_file}")
            print(f"  • Surviving buildings: {len(rampage_data['buildings'])}")
            print(f"  • Destroyed buildings: {len(rampage_data['destroyed_buildings'])}")
            print(f"  • Ghost monsters: {len(rampage_data['monsters'])}")
    
    # Save report
    report_file = args.report or f"building_destruction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()