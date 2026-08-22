#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: datetime, json, logging, os, pathlib, random, re, time, typing
# ROLE: DIRECTORY TRAVERSAL ATTACK SIMULATOR
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]

"""
DIRECTORY TRAVERSAL ATTACK SIMULATOR
Simulates path traversal vulnerabilities in the Rampage Refactor system
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List
import logging
import random
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DirectoryTraversalAttack:
    """Simulates directory traversal attacks against the codebase scanner"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).absolute()
        self.vulnerabilities_found = []
        self.attack_log = []
        self.successful_exploits = []
        
        # Common traversal patterns
        self.traversal_patterns = [
            "../../../",
            "..%2F..%2F..%2F",
            "..%5C..%5C..%5C",
            "..%252f..%252f..%252f",
            "....//",
            "..%00/",
            "..%2e/",
            "..%252e/",
            "..%c0%af/",
            "..%c1%9c/",
            "..%e0%80%af/",
            "..%e0%81%9c/",
        ]
    
    def scan_for_vulnerabilities(self) -> List[Dict]:
        """Scan the target system for potential directory traversal vulnerabilities"""
        logger.info(f"🔍 Scanning {self.target_path} for directory traversal vulnerabilities...")
        
        vulnerabilities = []
        
        # Check 1: Look for file operations without path sanitization
        py_files = list(self.target_path.rglob('*.py'))
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for dangerous file operations
                dangerous_patterns = [
                    r'open\(',  # Direct file opening
                    r'Path\(',  # Pathlib usage
                    r'os\.path\.join\(',  # Path joining
                    r'file_path\s*=\s*request',  # Direct request assignment
                    r'os\.chdir\(',  # Directory changing
                    r'os\.listdir\(',  # Directory listing
                    r'os\.walk\(',  # Directory walking
                ]
                
                for pattern in dangerous_patterns:
                    if re.search(pattern, content):
                        vulnerability = {
                            'type': 'potential_traversal_vulnerability',
                            'file': str(py_file),
                            'pattern': pattern,
                            'severity': 'medium',
                            'description': f'Found {pattern} without apparent path sanitization'
                        }
                        vulnerabilities.append(vulnerability)
                        break
                        
            except Exception as e:
                logger.warning(f"Error scanning {py_file}: {e}")
        
        # Check 2: Look for WebSocket message handling without validation
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'websocket' in content.lower() and 'path' in content.lower():
                    if 'sanitize' not in content.lower() and 'validate' not in content.lower():
                        vulnerability = {
                            'type': 'websocket_path_vulnerability',
                            'file': str(py_file),
                            'severity': 'high',
                            'description': 'WebSocket handler processes paths without apparent validation'
                        }
                        vulnerabilities.append(vulnerability)
                        
            except Exception as e:
                logger.warning(f"Error scanning {py_file}: {e}")
        
        self.vulnerabilities_found = vulnerabilities
        logger.info(f"✅ Found {len(vulnerabilities)} potential vulnerabilities")
        
        return vulnerabilities
    
    def launch_attack(self, target_file: str = None) -> Dict:
        """Simulate launching a directory traversal attack"""
        logger.info("🚀 Launching directory traversal attack...")
        
        attack_results = {
            'attack_type': 'directory_traversal',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'vulnerabilities_exploited': [],
            'files_accessed': [],
            'sensitive_data_leaked': [],
            'attack_success': False
        }
        
        # If no specific target, pick a vulnerable file
        if not target_file and self.vulnerabilities_found:
            target_file = random.choice(self.vulnerabilities_found)['file']
        
        if target_file:
            logger.info(f"🎯 Targeting: {target_file}")
            
            # Simulate different traversal patterns
            for pattern in self.traversal_patterns[:5]:  # Try first 5 patterns
                attack_vector = f"{target_file}?path={pattern}etc/passwd"
                
                attack_attempt = {
                    'pattern': pattern,
                    'vector': attack_vector,
                    'timestamp': datetime.now().isoformat(),
                    'success': False
                }
                
                # Simulate 30% success rate for demonstration
                if random.random() < 0.3:
                    attack_attempt['success'] = True
                    attack_results['attack_success'] = True
                    
                    # Simulate accessing sensitive files
                    sensitive_files = [
                        '/etc/passwd',
                        '/etc/shadow',
                        '.env',
                        'config.json',
                        'secrets.txt',
                        'database.sqlite'
                    ]
                    
                    accessed_file = random.choice(sensitive_files)
                    attack_results['files_accessed'].append(accessed_file)
                    
                    # Simulate data leakage
                    if accessed_file == '/etc/passwd':
                        attack_results['sensitive_data_leaked'].append({
                            'file': accessed_file,
                            'data': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin',
                            'severity': 'critical'
                        })
                    elif accessed_file == '.env':
                        attack_results['sensitive_data_leaked'].append({
                            'file': accessed_file,
                            'data': 'API_KEY=sk-1234567890abcdef\nDB_PASSWORD=supersecret123',
                            'severity': 'critical'
                        })
                    
                    logger.info(f"⚠️  Successfully exploited with pattern: {pattern}")
                    logger.info(f"📁 Accessed sensitive file: {accessed_file}")
                    
                self.attack_log.append(attack_attempt)
        
        if attack_results['attack_success']:
            logger.warning("🔴 DIRECTORY TRAVERSAL ATTACK SUCCESSFUL!")
            logger.warning(f"📊 Leaked {len(attack_results['sensitive_data_leaked'])} sensitive files")
        else:
            logger.info("🟢 Directory traversal attack blocked")
        
        self.successful_exploits.append(attack_results)
        return attack_results
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'directory_traversal',
            'target': str(self.target_path),
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities_found': len(self.vulnerabilities_found),
            'vulnerabilities': self.vulnerabilities_found,
            'attack_attempts': len(self.attack_log),
            'successful_attacks': len(self.successful_exploits),
            'sensitive_data_leaked': len([item for attack in self.successful_exploits for item in attack.get('sensitive_data_leaked', [])]),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = [
            "✅ Implement path sanitization for all file operations",
            "✅ Use allowlists for valid file paths instead of denylists",
            "✅ Validate and sanitize all user input containing paths",
            "✅ Use absolute paths and resolve them before operations",
            "✅ Implement proper error handling that doesn't leak path information",
            "✅ Add WebSocket message validation for path-related operations",
            "✅ Use parameterized APIs instead of string concatenation for paths",
            "✅ Implement rate limiting on file access endpoints",
            "✅ Add security headers to prevent path manipulation",
            "✅ Conduct regular security audits and penetration testing"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"directory_traversal_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file


def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Directory Traversal Attack Simulator')
    parser.add_argument('target', help='Target directory to attack')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for vulnerabilities')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Target not found: {args.target}")
        return
    
    attack = DirectoryTraversalAttack(args.target)
    
    print("🔍 DIRECTORY TRAVERSAL ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for vulnerabilities
    vulnerabilities = attack.scan_for_vulnerabilities()
    
    if vulnerabilities:
        print(f"⚠️  Found {len(vulnerabilities)} potential vulnerabilities:")
        for vuln in vulnerabilities[:5]:  # Show first 5
            print(f"  • {vuln['description']} ({vuln['file']})")
        if len(vulnerabilities) > 5:
            print(f"  ... and {len(vulnerabilities) - 5} more")
    else:
        print("✅ No obvious vulnerabilities found")
    
    if not args.scan_only:
        print("\n🚀 Launching attack...")
        results = attack.launch_attack()
        
        if results['attack_success']:
            print("🔴 ATTACK SUCCESSFUL!")
            print(f"📁 Accessed {len(results['files_accessed'])} sensitive files")
            print(f"💀 Leaked {len(results['sensitive_data_leaked'])} sensitive data items")
        else:
            print("🟢 Attack blocked")
    
    # Save report
    report_file = args.report or f"directory_traversal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()