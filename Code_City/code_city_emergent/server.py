#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: asyncio, datetime, json, logging, os, pathlib, scanner, typing, websockets
# ROLE: Rampage Refactor - Backend Server
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

"""
Rampage Refactor - Backend Server
Scans codebases, detects bugs, manages WebSocket connections
"""

import os
import json
import asyncio
import websockets
from pathlib import Path
from typing import Dict, List, Set
from scanner import CodebaseScanner
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Server configuration
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8765))


class RampageServer:
    def __init__(self):
        self.clients: Set = set()
        self.scanner = CodebaseScanner()
        self.current_city = None
        logger.info("🦖 Rampage Refactor Server initialized")
    
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connections"""
        self.clients.add(websocket)
        logger.info(f"✅ Client connected. Total clients: {len(self.clients)}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                'type': 'connected',
                'message': 'Welcome to Rampage Refactor!',
                'timestamp': datetime.now().isoformat()
            }))
            
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, message: str):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            action = data.get('action')
            
            logger.info(f"📨 Received action: {action}")
            
            if action == 'scan':
                await self.scan_codebase(websocket, data)
            
            elif action == 'rescan':
                await self.rescan_file(websocket, data)
            
            elif action == 'get_file_content':
                await self.get_file_content(websocket, data)
            
            elif action == 'deploy_agent':
                await self.deploy_agent(websocket, data)
            
            elif action == 'health':
                await websocket.send(json.dumps({
                    'type': 'health',
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat()
                }))
            
            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': f'Unknown action: {action}'
                }))
        
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def scan_codebase(self, websocket, data: Dict):
        """Scan a codebase and return city data"""
        folder_path = data.get('path', os.getcwd())
        
        try:
            logger.info(f"🔍 Scanning codebase at: {folder_path}")
            
            # Send scanning status
            await websocket.send(json.dumps({
                'type': 'scanning',
                'message': 'Scanning codebase...',
                'path': folder_path
            }))
            
            # Perform scan
            city_data = self.scanner.scan_codebase(folder_path)
            self.current_city = city_data
            
            logger.info(f"✅ Scan complete: {len(city_data['buildings'])} files, {len(city_data['monsters'])} bugs")
            
            # Send city data
            await websocket.send(json.dumps({
                'type': 'city_data',
                'data': city_data,
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Scan error: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Scan failed: {str(e)}'
            }))
    
    async def rescan_file(self, websocket, data: Dict):
        """Re-scan a specific file to check if bug is fixed"""
        file_path = data.get('file_path')
        
        try:
            logger.info(f"🔄 Re-scanning file: {file_path}")
            
            # Re-scan just this file
            building = self.scanner.analyze_single_file(file_path)
            
            await websocket.send(json.dumps({
                'type': 'file_rescanned',
                'data': building,
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Re-scan failed: {str(e)}'
            }))
    
    async def get_file_content(self, websocket, data: Dict):
        """Get file content and line information"""
        file_path = data.get('file_path')
        line_number = data.get('line_number')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Get context around the error line
            start = max(0, line_number - 5)
            end = min(len(lines), line_number + 5)
            
            context = {
                'file_path': file_path,
                'line_number': line_number,
                'lines': lines[start:end],
                'start_line': start + 1,
                'end_line': end + 1
            }
            
            await websocket.send(json.dumps({
                'type': 'file_content',
                'data': context
            }))
            
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Failed to read file: {str(e)}'
            }))
    
    async def deploy_agent(self, websocket, data: Dict):
        """Deploy an agent to target a monster"""
        monster_id = data.get('monster_id')
        
        logger.info(f"🤖 Agent deployed targeting monster: {monster_id}")
        
        # Create agent data
        agent = {
            'id': f'agent_{monster_id}_{datetime.now().timestamp()}',
            'target_monster_id': monster_id,
            'status': 'hunting',
            'position': {'x': 0, 'y': 10, 'z': 0}
        }
        
        await websocket.send(json.dumps({
            'type': 'agent_deployed',
            'data': agent
        }))
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True
            )


async def main():
    """Start the server"""
    server = RampageServer()
    
    print("\n" + "="*50)
    print("🦖 RAMPAGE REFACTOR - Backend Server")
    print("="*50)
    print(f"🚀 WebSocket server running on ws://{HOST}:{PORT}")
    print(f"📡 HTTP health check: http://{HOST}:{PORT}/health")
    print(f"✨ Ready to scan codebases!")
    print("\nPress Ctrl+C to stop\n")
    print("="*50 + "\n")
    
    async with websockets.serve(server.handle_client, HOST, PORT):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
