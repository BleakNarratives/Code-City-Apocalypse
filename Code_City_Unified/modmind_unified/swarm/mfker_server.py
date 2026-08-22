
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, http, json, logging, os, platform, psutil, socketserver, sqlite3, subprocess, sys, threading, time
# ROLE: MFKER - Model Forge Kernel Execution Runtime
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

import logging

#!/usr/bin/env python3
"""
MFKER - Model Forge Kernel Execution Runtime
Based on cumbseek_9_11.txt specifications
Runs AI models directly on Android in Termux
"""

import http.server
import socketserver
import json
import os
import sys
import time
import threading
import sqlite3
from datetime import datetime
import subprocess
import platform
import psutil  # For system monitoring

# Check if we're running in Termux
TERMUX = os.path.exists('/data/data/com.termux/files/home')

class MFKERHandler(http.server.BaseHTTPRequestHandler):
    """Handle MFKER API requests"""
    
    models = {}
    cache_db = None
    performance_stats = {
        'requests': 0,
        'start_time': time.time(),
        'last_request': 0
    }
    
    def log_message(self, format, *args):
        """Custom logging that writes to both console and file"""
        msg = f"[{self.address_string()}] {format % args}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {msg}"
        logging.info(log_msg)
        
        # Log to file
        with open('mfker_server.log', 'a') as f:
            f.write(log_msg + '\n')
    
    def set_headers(self, content_type='application/json'):
        """Set common HTTP headers"""
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        self.performance_stats['requests'] += 1
        self.performance_stats['last_request'] = time.time()
        
        try:
            if self.path == '/status':
                self.handle_status()
            elif self.path == '/models':
                self.handle_models()
            elif self.path == '/stats':
                self.handle_stats()
            elif self.path == '/cache':
                self.handle_cache()
            elif self.path == '/battery':
                self.handle_battery()
            elif self.path == '/system':
                self.handle_system()
            else:
                self.handle_404()
        except Exception as e:
            self.handle_error(str(e))
    
    def do_POST(self):
        """Handle POST requests"""
        self.performance_stats['requests'] += 1
        self.performance_stats['last_request'] = time.time()
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            if self.path == '/inference':
                self.handle_inference(post_data)
            elif self.path == '/load_model':
                self.handle_load_model(post_data)
            elif self.path == '/unload_model':
                self.handle_unload_model(post_data)
            elif self.path == '/cache_result':
                self.handle_cache_result(post_data)
            elif self.path == '/clear_cache':
                self.handle_clear_cache(post_data)
            else:
                self.handle_404()
        except Exception as e:
            self.handle_error(str(e))
    
    def handle_status(self):
        """Return server status"""
        status = {
            'server': 'MFKER v1.0',
            'timestamp': datetime.now().isoformat(),
            'uptime': time.time() - self.performance_stats['start_time'],
            'requests': self.performance_stats['requests'],
            'models_loaded': list(self.models.keys()),
            'environment': 'termux' if TERMUX else 'unknown',
            'nova_accord': True,
            'battery_saver': True,
            'offline_capable': True
        }
        
        # Add battery info if available
        if TERMUX:
            status['battery'] = self.get_battery_info()
        
        self.set_headers()
        self.wfile.write(json.dumps(status, indent=2).encode())
    
    def handle_models(self):
        """Return available models"""
        available_models = [
            {
                'name': 'tiny-llama-1B',
                'type': 'text-generation',
                'size': '1B parameters',
                'offline': True,
                'battery_efficient': True,
                'description': 'Tiny language model for offline text generation'
            },
            {
                'name': 'distilbert-sentiment',
                'type': 'text-classification',
                'size': '66M parameters',
                'offline': True,
                'battery_efficient': True,
                'description': 'Lightweight sentiment analysis model'
            },
            {
                'name': 'gesture-predictor',
                'type': 'gesture-recognition',
                'size': 'Custom',
                'offline': True,
                'battery_efficient': True,
                'description': 'Hand gesture prediction for EquiNex'
            }
        ]
        
        loaded_models = []
        for model_name in self.models:
            model_info = self.models[model_name]
            loaded_models.append({
                'name': model_name,
                'type': model_info.get('type', 'unknown'),
                'loaded_at': model_info.get('loaded_at', 'unknown'),
                'size': model_info.get('size', 'unknown')
            })
        
        response = {
            'available': available_models,
            'loaded': loaded_models,
            'cache_enabled': True
        }
        
        self.set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def handle_inference(self, post_data):
        """Handle inference requests"""
        try:
            data = json.loads(post_data.decode())
            model_name = data.get('model', 'tiny-llama-1B')
            prompt = data.get('prompt', '')
            options = data.get('options', {})
            
            # Check if model is loaded
            if model_name not in self.models:
                response = {
                    'error': f'Model {model_name} not loaded',
                    'available_models': list(self.models.keys())
                }
                self.set_headers()
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Check cache first
            cached_result = self.get_cached_result(model_name, prompt)
            if cached_result:
                cached_result['cached'] = True
                cached_result['battery_saved'] = True
                self.set_headers()
                self.wfile.write(json.dumps(cached_result).encode())
                return
            
            # Run inference
            result = self.run_inference(model_name, prompt, options)
            
            # Cache the result
            self.cache_result(model_name, prompt, result)
            
            # Add performance info
            result['cached'] = False
            result['inference_time'] = 'simulated'  # Would be actual time in real impl
            
            self.set_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.handle_error(f'Inference error: {str(e)}')
    
    def run_inference(self, model_name, prompt, options):
        """Run inference on the specified model"""
        # This is a simulated inference - in a real implementation,
        # you would use the actual model
        
        if model_name == 'tiny-llama-1B':
            # Simulate text generation
            response_text = f"Based on your prompt '{prompt[:50]}...', here's a simulated response. "
            response_text += "This is running entirely offline on your device! "
            response_text += "The actual model would generate more coherent text, but this demonstrates "
            response_text += "the offline capability. Battery: "
            
            if TERMUX:
                battery = self.get_battery_info()
                response_text += f"{battery.get('level', 'unknown')}%"
            else:
                response_text += "unknown%"
            
            return {
                'model': model_name,
                'prompt': prompt,
                'response': response_text,
                'tokens': len(response_text.split()),
                'battery_efficient': True
            }
        
        elif model_name == 'distilbert-sentiment':
            # Simulate sentiment analysis
            sentiment = 'POSITIVE' if 'good' in prompt.lower() or 'great' in prompt.lower() else 'NEGATIVE'
            if '?' in prompt or 'how' in prompt.lower():
                sentiment = 'NEUTRAL'
            
            return {
                'model': model_name,
                'prompt': prompt,
                'sentiment': sentiment,
                'confidence': 0.85 + (0.15 * (len(prompt) / 100)),
                'battery_efficient': True
            }
        
        elif model_name == 'gesture-predictor':
            # Simulate gesture prediction
            gestures = ['PINCH', 'POINT', 'FIST', 'SWIPE_LEFT', 'SWIPE_RIGHT', 'VULCAN']
            predicted_gesture = gestures[len(prompt) % len(gestures)]
            
            return {
                'model': model_name,
                'prompt': prompt,
                'predicted_gesture': predicted_gesture,
                'confidence': 0.75 + (0.25 * (len(prompt) / 50)),
                'recommendation': 'Try the Vulcan salute to activate Nova Accord!'
            }
        
        else:
            return {
                'error': f'Unknown model: {model_name}',
                'available_models': list(self.models.keys())
            }
    
    def handle_load_model(self, post_data):
        """Load a model into memory"""
        try:
            data = json.loads(post_data.decode())
            model_name = data.get('model_name')
            
            if not model_name:
                self.handle_error('No model name specified')
                return
            
            # Simulate model loading
            if model_name in ['tiny-llama-1B', 'distilbert-sentiment', 'gesture-predictor']:
                self.models[model_name] = {
                    'loaded_at': datetime.now().isoformat(),
                    'type': 'text-generation' if model_name == 'tiny-llama-1B' else 'text-classification',
                    'size': '1B' if model_name == 'tiny-llama-1B' else '66M'
                }
                
                response = {
                    'status': f'Model {model_name} loaded successfully',
                    'model': model_name,
                    'loaded_at': self.models[model_name]['loaded_at'],
                    'battery_impact': 'low'
                }
                
                self.log_message(f'Loaded model: {model_name}')
            else:
                response = {
                    'status': 'error',
                    'error': f'Model {model_name} not available',
                    'available_models': ['tiny-llama-1B', 'distilbert-sentiment', 'gesture-predictor']
                }
            
            self.set_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.handle_error(f'Failed to load model: {str(e)}')
    
    def handle_unload_model(self, post_data):
        """Unload a model from memory"""
        try:
            data = json.loads(post_data.decode())
            model_name = data.get('model_name')
            
            if not model_name:
                self.handle_error('No model name specified')
                return
            
            if model_name in self.models:
                del self.models[model_name]
                response = {
                    'status': f'Model {model_name} unloaded successfully',
                    'memory_freed': True
                }
                self.log_message(f'Unloaded model: {model_name}')
            else:
                response = {
                    'status': 'error',
                    'error': f'Model {model_name} not loaded',
                    'loaded_models': list(self.models.keys())
                }
            
            self.set_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.handle_error(f'Failed to unload model: {str(e)}')
    
    def handle_stats(self):
        """Return performance statistics"""
        uptime = time.time() - self.performance_stats['start_time']
        
        stats = {
            'uptime_seconds': uptime,
            'uptime_human': self.seconds_to_human(uptime),
            'total_requests': self.performance_stats['requests'],
            'requests_per_minute': (self.performance_stats['requests'] / max(uptime, 1)) * 60,
            'models_loaded': len(self.models),
            'cache_size': self.get_cache_size(),
            'battery_efficient': True,
            'offline_capable': True
        }
        
        # Add system info
        if TERMUX:
            stats['system'] = self.get_system_info()
        
        self.set_headers()
        self.wfile.write(json.dumps(stats, indent=2).encode())
    
    def handle_cache(self):
        """Return cache information"""
        cache_info = {
            'enabled': True,
            'size': self.get_cache_size(),
            'entries': self.get_cache_entry_count(),
            'battery_saved': True,
            'offline_available': True
        }
        
        self.set_headers()
        self.wfile.write(json.dumps(cache_info, indent=2).encode())
    
    def handle_cache_result(self, post_data):
        """Manually cache a result"""
        try:
            data = json.loads(post_data.decode())
            model_name = data.get('model')
            prompt = data.get('prompt')
            result = data.get('result')
            
            if not all([model_name, prompt, result]):
                self.handle_error('Missing required fields: model, prompt, result')
                return
            
            success = self.cache_result(model_name, prompt, result)
            
            if success:
                response = {
                    'status': 'success',
                    'cached': True,
                    'battery_saved': True
                }
            else:
                response = {
                    'status': 'error',
                    'error': 'Failed to cache result'
                }
            
            self.set_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.handle_error(f'Cache error: {str(e)}')
    
    def handle_clear_cache(self, post_data):
        """Clear the cache"""
        try:
            data = json.loads(post_data.decode())
            confirm = data.get('confirm', False)
            
            if not confirm:
                response = {
                    'status': 'error',
                    'error': 'Clear cache requires confirmation (confirm=true)'
                }
                self.set_headers()
                self.wfile.write(json.dumps(response).encode())
                return
            
            success = self.clear_cache()
            
            if success:
                response = {
                    'status': 'success',
                    'cleared': True,
                    'previous_size': self.get_cache_size()
                }
            else:
                response = {
                    'status': 'error',
                    'error': 'Failed to clear cache'
                }
            
            self.set_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.handle_error(f'Clear cache error: {str(e)}')
    
    def handle_battery(self):
        """Return battery information"""
        if TERMUX:
            battery_info = self.get_battery_info()
            
            # Add battery saving tips
            battery_info['tips'] = []
            if battery_info.get('level', 100) < 20:
                battery_info['tips'].append('Connect charger soon')
                battery_info['tips'].append('Enable battery saver mode')
            
            self.set_headers()
            self.wfile.write(json.dumps(battery_info, indent=2).encode())
        else:
            self.handle_error('Battery API only available in Termux')
    
    def handle_system(self):
        """Return system information"""
        if TERMUX:
            system_info = self.get_system_info()
            self.set_headers()
            self.wfile.write(json.dumps(system_info, indent=2).encode())
        else:
            self.handle_error('System info only available in Termux')
    
    def handle_404(self):
        """Handle 404 Not Found"""
        response = {
            'error': 'Route not found',
            'available_routes': [
                'GET /status',
                'GET /models',
                'GET /stats',
                'GET /cache',
                'GET /battery',
                'GET /system',
                'POST /inference',
                'POST /load_model',
                'POST /unload_model',
                'POST /cache_result',
                'POST /clear_cache'
            ],
            'nova_accord': True,
            'message': 'The walls are thin...'
        }
        
        self.send_response(404)
        self.set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def handle_error(self, error_message):
        """Handle errors"""
        response = {
            'error': error_message,
            'timestamp': datetime.now().isoformat(),
            'nova_accord': True,
            'recovery_suggestion': 'Check server logs for details'
        }
        
        self.send_response(500)
        self.set_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())
        
        self.log_message(f'ERROR: {error_message}')
    
    # Cache management methods
    def init_cache(self):
        """Initialize the cache database"""
        try:
            self.cache_db = sqlite3.connect('mfker_cache.db')
            cursor = self.cache_db.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inference_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    result TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    battery_level INTEGER,
                    UNIQUE(model, prompt)
                )
            ''')
            
            self.cache_db.commit()
            return True
        except Exception as e:
            self.log_message(f'Cache init error: {str(e)}')
            return False
    
    def get_cached_result(self, model, prompt):
        """Get a cached result if available"""
        if not self.cache_db:
            self.init_cache()
        
        try:
            cursor = self.cache_db.cursor()
            cursor.execute(
                'SELECT result FROM inference_cache WHERE model = ? AND prompt = ?',
                (model, prompt)
            )
            
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            return None
        except Exception as e:
            self.log_message(f'Cache read error: {str(e)}')
            return None
    
    def cache_result(self, model, prompt, result):
        """Cache an inference result"""
        if not self.cache_db:
            self.init_cache()
        
        try:
            # Get current battery level
            battery_level = None
            if TERMUX:
                battery_info = self.get_battery_info()
                battery_level = battery_info.get('level')
            
            cursor = self.cache_db.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO inference_cache 
                   (model, prompt, result, battery_level) 
                   VALUES (?, ?, ?, ?)''',
                (model, prompt, json.dumps(result), battery_level)
            )
            
            self.cache_db.commit()
            return True
        except Exception as e:
            self.log_message(f'Cache write error: {str(e)}')
            return False
    
    def get_cache_size(self):
        """Get the size of the cache"""
        if not self.cache_db:
            self.init_cache()
        
        try:
            cursor = self.cache_db.cursor()
            cursor.execute('SELECT COUNT(*) FROM inference_cache')
            count = cursor.fetchone()[0]
            
            # Get database file size
            db_size = os.path.getsize('mfker_cache.db') if os.path.exists('mfker_cache.db') else 0
            
            return {
                'entries': count,
                'database_size_bytes': db_size,
                'database_size_human': self.bytes_to_human(db_size)
            }
        except Exception as e:
            self.log_message(f'Cache size error: {str(e)}')
            return {'entries': 0, 'database_size_bytes': 0, 'database_size_human': '0B'}
    
    def get_cache_entry_count(self):
        """Get the number of cached entries"""
        size_info = self.get_cache_size()
        return size_info['entries']
    
    def clear_cache(self):
        """Clear the cache"""
        if not self.cache_db:
            self.init_cache()
        
        try:
            cursor = self.cache_db.cursor()
            cursor.execute('DELETE FROM inference_cache')
            cursor.execute('VACUUM')  # Compact database
            self.cache_db.commit()
            return True
        except Exception as e:
            self.log_message(f'Cache clear error: {str(e)}')
            return False
    
    # Utility methods
    def get_battery_info(self):
        """Get battery information from Termux"""
        try:
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True, timeout=5)
            return json.loads(result.stdout)
        except Exception as e:
            self.log_message(f'Battery info error: {str(e)}')
            return {'level': 100, 'charging': False, 'error': str(e)}
    
    def get_system_info(self):
        """Get system information"""
        try:
            # Get CPU info
            cpu_count = os.cpu_count() or 1
            
            # Get memory info
            if TERMUX:
                try:
                    import psutil
                    memory = psutil.virtual_memory()
                    memory_info = {
                        'total': memory.total,
                        'available': memory.available,
                        'used': memory.used,
                        'percent': memory.percent
                    }
                except:
                    memory_info = {'total': 0, 'available': 0, 'used': 0, 'percent': 0}
            else:
                memory_info = {'total': 0, 'available': 0, 'used': 0, 'percent': 0}
            
            # Get storage info
            storage = os.statvfs('/')
            storage_info = {
                'total': storage.f_frsize * storage.f_blocks,
                'free': storage.f_frsize * storage.f_bfree,
                'used': storage.f_frsize * (storage.f_blocks - storage.f_bfree)
            }
            
            return {
                'platform': platform.system(),
                'cpu_cores': cpu_count,
                'memory': memory_info,
                'storage': storage_info,
                'python_version': platform.python_version(),
                'termux': TERMUX
            }
        except Exception as e:
            self.log_message(f'System info error: {str(e)}')
            return {'error': str(e)}
    
    def seconds_to_human(self, seconds):
        """Convert seconds to human-readable format"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        parts = []
        if days > 0:
            parts.append(f"{int(days)}d")
        if hours > 0:
            parts.append(f"{int(hours)}h")
        if minutes > 0:
            parts.append(f"{int(minutes)}m")
        if seconds > 0 or not parts:
            parts.append(f"{int(seconds)}s")
        
        return ' '.join(parts)
    
    def bytes_to_human(self, bytes_count):
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024.0:
                return f"{bytes_count:.1f}{unit}"
            bytes_count /= 1024.0
        return f"{bytes_count:.1f}PB"

def run_server(port=31337):
    """Run the MFKER server"""
    print("""
    ╔╦╗┌─┐╦═╗╔═╗╦═╗
     ║║├┤ ╠╦╝║╣ ╠╦╝
    ═╩╝└─┘╩╚═╚═╝╩╚═
    Model Forge Kernel Execution Runtime
    Port: {} | Environment: {}
    """.format(port, 'Termux' if TERMUX else 'Unknown'))
    
    # Initialize cache
    handler = MFKERHandler
    handler.init_cache()
    
    # Pre-load a model if specified
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
        logging.info(f"🤖 Pre-loading model: {model_name}")
        # In a real implementation, this would actually load the model
        handler.models[model_name] = {
            'loaded_at': datetime.now().isoformat(),
            'type': 'text-generation',
            'size': '1B'
        }
    
    # Start server
    with socketserver.TCPServer(("", port), handler) as httpd:
        logging.info(f"🌐 Server running on port {port}")
        logging.info(f"📱 Local access: http://localhost:{port}")
        logging.info(f"🔋 Battery API: {'Available' if TERMUX else 'Not available'}")
        logging.info(f"📦 Offline mode: Enabled")
        logging.info(f"🌌 Nova Accord: Active")
        logging.info("\n📋 Available endpoints:")
        logging.info("  GET  /status      - Server status")
        logging.info("  GET  /models      - Available models")
        logging.info("  GET  /stats       - Performance stats")
        logging.info("  GET  /cache       - Cache information")
        logging.info("  GET  /battery     - Battery status (Termux only)")
        logging.info("  GET  /system      - System information (Termux only)")
        logging.info("  POST /inference   - Run inference")
        logging.info("  POST /load_model  - Load a model")
        logging.info("  POST /unload_model - Unload a model")
        logging.info("\n💡 Press Ctrl+C to stop server")
        logging.info("📝 Logs: mfker_server.log")
        logging.info("🔋 Remember: The walls are thin...")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("\n⏹️  MFKER server stopped")
            logging.info("📋 Session stats:")
            logging.info(f"   Requests: {handler.performance_stats['requests']}")
            logging.info(f"   Uptime: {handler.seconds_to_human(time.time() - handler.performance_stats['start_time'])}")
            logging.info("💾 Cache preserved for next session")
            logging.info("🌌 Nova Accord state saved")

if __name__ == "__main__":
    # Check if we need to install dependencies
    if TERMUX:
        try:
            import psutil
        except ImportError:
            logging.info("📦 Installing required packages...")
            subprocess.run(['pip', 'install', 'psutil'], check=True)
    
    # Run server
    run_server()