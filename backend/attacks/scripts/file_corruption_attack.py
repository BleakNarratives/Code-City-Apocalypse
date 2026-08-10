#!/usr/bin/env python3
"""
FILE CORRUPTION ATTACK SIMULATOR
Simulates malicious file corruption attacks against codebases
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


class FileCorruptionAttack:
    """Simulates file corruption attacks against source code"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).absolute()
        self.target_files = []
        self.corruption_log = []
        self.successful_corruptions = []
        
        # Corruption strategies
        self.corruption_strategies = [
            {
                'name': 'byte_flipping',
                'description': 'Flip random bytes in the file',
                'severity': 'medium'
            },
            {
                'name': 'string_replacement',
                'description': 'Replace critical strings with garbage',
                'severity': 'high'
            },
            {
                'name': 'function_removal',
                'description': 'Remove random functions/classes',
                'severity': 'critical'
            },
            {
                'name': 'import_corruption',
                'description': 'Corrupt import statements',
                'severity': 'high'
            },
            {
                'name': 'syntax_injection',
                'description': 'Inject syntax errors',
                'severity': 'medium'
            },
            {
                'name': 'encoding_corruption',
                'description': 'Change file encoding',
                'severity': 'critical'
            }
        ]
    
    def scan_for_targets(self) -> List[Dict]:
        """Find files suitable for corruption"""
        logger.info(f"🔍 Scanning {self.target_path} for corruption targets...")
        
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
                            'lines': len(file_path.read_text(encoding='utf-8', errors='ignore').split('\n'))
                        })
                except Exception as e:
                    logger.warning(f"Error scanning {file_path}: {e}")
        
        self.target_files = targets
        logger.info(f"✅ Found {len(targets)} potential corruption targets")
        
        return targets
    
    def launch_corruption_attack(self, target_file: str = None) -> Dict:
        """Simulate file corruption attack"""
        logger.info("🚀 Launching file corruption attack...")
        
        attack_results = {
            'attack_type': 'file_corruption',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'files_corrupted': [],
            'corruption_success': False,
            'corruption_details': []
        }
        
        # If no specific target, pick a random file
        if not target_file and self.target_files:
            target_file = random.choice(self.target_files)['file']
        
        if target_file:
            logger.info(f"🎯 Targeting: {target_file}")
            
            try:
                with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
                    original_content = f.read()
                
                # Choose corruption strategy
                strategy = random.choice(self.corruption_strategies)
                logger.info(f"🔧 Using strategy: {strategy['name']}")
                
                # Simulate corruption (don't actually corrupt files for safety)
                if random.random() < 0.8:  # 80% success rate
                    attack_results['corruption_success'] = True
                    attack_results['files_corrupted'].append(target_file)
                    
                    # Simulate different corruption effects
                    if strategy['name'] == 'byte_flipping':
                        corrupted_content = self._simulate_byte_flipping(original_content)
                    elif strategy['name'] == 'string_replacement':
                        corrupted_content = self._simulate_string_replacement(original_content)
                    elif strategy['name'] == 'function_removal':
                        corrupted_content = self._simulate_function_removal(original_content)
                    elif strategy['name'] == 'import_corruption':
                        corrupted_content = self._simulate_import_corruption(original_content)
                    elif strategy['name'] == 'syntax_injection':
                        corrupted_content = self._simulate_syntax_injection(original_content)
                    elif strategy['name'] == 'encoding_corruption':
                        corrupted_content = self._simulate_encoding_corruption(original_content)
                    else:
                        corrupted_content = original_content
                    
                    # Log corruption details
                    attack_results['corruption_details'].append({
                        'file': target_file,
                        'strategy': strategy['name'],
                        'severity': strategy['severity'],
                        'original_size': len(original_content),
                        'corrupted_size': len(corrupted_content),
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logger.warning(f"⚠️  Successfully corrupted {target_file} using {strategy['name']}")
                    logger.warning(f"📊 File size changed from {len(original_content)} to {len(corrupted_content)} bytes")
                    
                    # Simulate the effects
                    if strategy['name'] in ['function_removal', 'import_corruption']:
                        logger.warning("💀 Critical functionality destroyed!")
                    elif strategy['name'] == 'encoding_corruption':
                        logger.warning("🔤 File encoding corrupted - unreadable!")
                    else:
                        logger.warning("🔧 File structure damaged!")
                    
                else:
                    logger.info("🟢 Corruption attempt failed")
                    
            except Exception as e:
                logger.error(f"Corruption failed: {e}")
        
        if attack_results['corruption_success']:
            logger.warning("🔴 FILE CORRUPTION ATTACK SUCCESSFUL!")
            logger.warning(f"💀 Corrupted {len(attack_results['files_corrupted'])} files")
        else:
            logger.info("🟢 File corruption attack blocked")
        
        self.successful_corruptions.append(attack_results)
        return attack_results
    
    def _simulate_byte_flipping(self, content: str) -> str:
        """Simulate byte flipping corruption"""
        if len(content) == 0:
            return content
        
        # Convert to bytes, flip some bits, convert back
        byte_content = content.encode('utf-8', errors='ignore')
        corrupted_bytes = bytearray(byte_content)
        
        # Flip 10% of bytes
        for i in range(len(corrupted_bytes)):
            if random.random() < 0.1:
                corrupted_bytes[i] = corrupted_bytes[i] ^ 0xFF  # XOR with 0xFF
        
        return corrupted_bytes.decode('utf-8', errors='replace')
    
    def _simulate_string_replacement(self, content: str) -> str:
        """Simulate string replacement corruption"""
        critical_strings = ['def ', 'class ', 'import ', 'function ', 'const ', 'let ', 'return ']
        
        for critical in critical_strings:
            if critical in content:
                # Replace 30% of occurrences
                occurrences = content.split(critical)
                for i in range(1, len(occurrences)):
                    if random.random() < 0.3:
                        occurrences[i] = "CORRUPTED_" + occurrences[i]
                content = critical.join(occurrences)
        
        return content
    
    def _simulate_function_removal(self, content: str) -> str:
        """Simulate function removal corruption"""
        lines = content.split('\n')
        corrupted_lines = []
        
        in_function = False
        function_start = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect function/class start
            if (stripped.startswith('def ') or stripped.startswith('class ') or 
                stripped.startswith('function ') or stripped.startswith('const ') or 
                stripped.startswith('let ')) and not stripped.endswith(':'):
                
                if in_function and random.random() < 0.5:  # 50% chance to remove the function
                    logger.info(f"🗑️  Removing function starting at line {function_start}")
                    # Remove the function we were tracking
                    corrupted_lines = corrupted_lines[:function_start]
                    in_function = False
                else:
                    function_start = len(corrupted_lines)
                    in_function = True
            
            # Add current line
            corrupted_lines.append(line)
            
            # Detect function/class end (simplified)
            if in_function and (stripped == '' or (stripped.startswith('def ') or stripped.startswith('class '))):
                in_function = False
        
        return '\n'.join(corrupted_lines)
    
    def _simulate_import_corruption(self, content: str) -> str:
        """Simulate import statement corruption"""
        lines = content.split('\n')
        corrupted_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('import ') or stripped.startswith('from ') or stripped.startswith('require('):
                if random.random() < 0.7:  # 70% chance to corrupt import
                    corrupted_line = line.replace('import', 'CORRUPTED_IMPORT')
                    corrupted_line = corrupted_line.replace('from', 'CORRUPTED_FROM')
                    corrupted_line = corrupted_line.replace('require', 'CORRUPTED_REQUIRE')
                    corrupted_lines.append(corrupted_line)
                    logger.info(f"🔧 Corrupted import: {line[:30]}...")
                else:
                    corrupted_lines.append(line)
            else:
                corrupted_lines.append(line)
        
        return '\n'.join(corrupted_lines)
    
    def _simulate_syntax_injection(self, content: str) -> str:
        """Simulate syntax error injection"""
        lines = content.split('\n')
        
        # Inject syntax errors at random lines
        for i in range(len(lines)):
            if random.random() < 0.1 and not lines[i].strip().startswith('#'):  # 10% chance, skip comments
                syntax_errors = [
                    'SYNTAX_ERROR_INJECTED',
                    '{{{{{ INVALID_SYNTAX }}}}',
                    'def broken_function(',  # Unclosed parenthesis
                    'if True:  # Missing indentation',
                    'return without value',
                    'import non_existent_module_12345'
                ]
                lines[i] += ' ' + random.choice(syntax_errors)
        
        return '\n'.join(lines)
    
    def _simulate_encoding_corruption(self, content: str) -> str:
        """Simulate file encoding corruption"""
        # Convert to different encoding and back
        try:
            # Try to corrupt by using wrong encoding
            corrupted = content.encode('utf-8', errors='ignore')
            corrupted = corrupted.decode('latin-1', errors='replace')
            corrupted = corrupted.encode('utf-16', errors='replace')
            return corrupted.decode('utf-16', errors='replace')
        except:
            # If that fails, just scramble some characters
            return ''.join([
                chr(ord(c) + random.randint(-5, 5)) if random.random() < 0.3 else c
                for c in content
            ])
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'file_corruption',
            'target': str(self.target_path),
            'timestamp': datetime.now().isoformat(),
            'target_files_found': len(self.target_files),
            'target_files': self.target_files,
            'corruption_attempts': len(self.corruption_log),
            'successful_corruptions': len(self.successful_corruptions),
            'files_corrupted': len([item for attack in self.successful_corruptions for item in attack.get('files_corrupted', [])]),
            'corruption_details': [item for attack in self.successful_corruptions for item in attack.get('corruption_details', [])],
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = [
            "✅ Implement file integrity monitoring",
            "✅ Use version control with proper access controls",
            "✅ Implement backup and recovery procedures",
            "✅ Use file permissions and access controls",
            "✅ Implement code signing for critical files",
            "✅ Use static code analysis to detect anomalies",
            "✅ Implement change detection systems",
            "✅ Use file system monitoring tools",
            "✅ Implement proper error handling and logging",
            "✅ Conduct regular security audits of file systems"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"file_corruption_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file


def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='File Corruption Attack Simulator')
    parser.add_argument('target', help='Target directory to attack')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for targets')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Target not found: {args.target}")
        return
    
    attack = FileCorruptionAttack(args.target)
    
    print("💀 FILE CORRUPTION ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for targets
    targets = attack.scan_for_targets()
    
    if targets:
        print(f"🎯 Found {len(targets)} potential corruption targets:")
        total_size = sum(t['size'] for t in targets)
        print(f"  • Total files: {len(targets)}")
        print(f"  • Total size: {total_size:,} bytes")
        print(f"  • Average file size: {total_size // len(targets):,} bytes")
    else:
        print("✅ No suitable targets found")
    
    if not args.scan_only:
        print("\n🚀 Launching corruption attack...")
        results = attack.launch_corruption_attack()
        
        if results['corruption_success']:
            print("🔴 CORRUPTION ATTACK SUCCESSFUL!")
            print(f"💀 Corrupted {len(results['files_corrupted'])} files")
            print(f"📊 Used {len(results['corruption_details'])} corruption strategies")
        else:
            print("🟢 Corruption attack blocked")
    
    # Save report
    report_file = args.report or f"file_corruption_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()