#!/bin/bash
# AirForge Folder Merger
# Merge all AirForge folders into a single organized structure

echo "🏗️  AirForge Folder Merger"
echo "========================"
echo ""

# Define source and target directories
PROJECT_DIR="/storage/ED7B-AD5A/root_2026/ai_swarm_project"
TERMUX_HOME="~/storage/shared/airforge"
DOWNLOAD_DIR="/storage/ED7B-AD5A/Download/airforge"

echo "📍 Project Directory: $PROJECT_DIR"
echo "📍 Termux Target: $TERMUX_HOME"
echo "📍 Download Source: $DOWNLOAD_DIR"
echo ""

# Create target directory if it doesn't exist
mkdir -p "$TERMUX_HOME"
mkdir -p "$TERMUX_HOME/docs"
mkdir -p "$TERMUX_HOME/libs"
mkdir -p "$TERMUX_HOME/src"
mkdir -p "$TERMUX_HOME/config"

echo "📁 Creating directory structure..."
echo ""

# Copy files from project directory
echo "📋 Copying files from project directory..."
cp -v "$PROJECT_DIR/setup_offline_env.sh" "$TERMUX_HOME/" 2>/dev/null || echo "  ⚠️  setup_offline_env.sh not found"
cp -v "$PROJECT_DIR/download_libs.sh" "$TERMUX_HOME/" 2>/dev/null || echo "  ⚠️  download_libs.sh not found"
cp -v "$PROJECT_DIR/start.sh" "$TERMUX_HOME/" 2>/dev/null || echo "  ⚠️  start.sh not found"
cp -v "$PROJECT_DIR/battery_saver.js" "$TERMUX_HOME/src/" 2>/dev/null || echo "  ⚠️  battery_saver.js not found"
cp -v "$PROJECT_DIR/graffiti_ghosts.js" "$TERMUX_HOME/src/" 2>/dev/null || echo "  ⚠️  graffiti_ghosts.js not found"
cp -v "$PROJECT_DIR/vulcan_salute_detector.js" "$TERMUX_HOME/src/" 2>/dev/null || echo "  ⚠️  vulcan_salute_detector.js not found"
cp -v "$PROJECT_DIR/cyberdeck_mode.js" "$TERMUX_HOME/src/" 2>/dev/null || echo "  ⚠️  cyberdeck_mode.js not found"
cp -v "$PROJECT_DIR/mfker_server.py" "$TERMUX_HOME/" 2>/dev/null || echo "  ⚠️  mfker_server.py not found"
cp -v "$PROJECT_DIR/mfker_client.js" "$TERMUX_HOME/src/" 2>/dev/null || echo "  ⚠️  mfker_client.js not found"
cp -v "$PROJECT_DIR/ALLEYWAY_MANUAL.md" "$TERMUX_HOME/docs/" 2>/dev/null || echo "  ⚠️  ALLEYWAY_MANUAL.md not found"
cp -v "$PROJECT_DIR/MISTRAL_TASK.md" "$TERMUX_HOME/docs/" 2>/dev/null || echo "  ⚠️  MISTRAL_TASK.md not found"
cp -v "$PROJECT_DIR/GEMINI_TASK.md" "$TERMUX_HOME/docs/" 2>/dev/null || echo "  ⚠️  GEMINI_TASK.md not found"
echo ""

# Copy files from download directory
echo "📋 Copying files from download directory..."
if [ -d "$DOWNLOAD_DIR" ]; then
    cp -rv "$DOWNLOAD_DIR/"* "$TERMUX_HOME/" 2>/dev/null || echo "  ⚠️  No files in download directory"
else
    echo "  ⚠️  Download directory not found"
fi
echo ""

# Create essential files if they don't exist
echo "📝 Creating essential files..."

# Create index.html if it doesn't exist
if [ ! -f "$TERMUX_HOME/index.html" ]; then
    cat > "$TERMUX_HOME/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AirForge - Alleyway AR</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #0f0;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        h1 {
            color: #0ff;
            text-align: center;
        }
        
        .panel {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #0f0;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        
        button {
            background: #0f0;
            color: #000;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
            font-family: monospace;
            border-radius: 3px;
        }
        
        a {
            color: #0ff;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏗️ AirForge v2.0</h1>
        <p style="text-align: center; color: #0ff;">The Alleyway Arsenal</p>
        
        <div class="panel">
            <h2>🚀 Quick Start</h2>
            <ol>
                <li><strong>Setup environment:</strong> <code>./setup_offline_env.sh</code></li>
                <li><strong>Download libraries:</strong> <code>./download_libs.sh</code></li>
                <li><strong>Start server:</strong> <code>./start.sh</code></li>
                <li><strong>Open browser:</strong> <code>termux-open-url http://localhost:8000</code></li>
            </ol>
        </div>
        
        <div class="panel">
            <h2>📚 Documentation</h2>
            <ul>
                <li>📖 <a href="docs/ALLEYWAY_MANUAL.md" target="_blank">Alleyway Manual</a></li>
                <li>🤖 <a href="docs/MISTRAL_TASK.md" target="_blank">Mistral Integration</a></li>
                <li>🤖 <a href="docs/GEMINI_TASK.md" target="_blank">Gemini Integration</a></li>
            </ul>
        </div>
        
        <div class="panel">
            <h2>🎮 Features</h2>
            <ul>
                <li>🔋 Battery Saver Mode - Adaptive FPS and power management</li>
                <li>👻 Graffiti Ghosts - AR text persistence with GPS</li>
                <li>🖖 Vulcan Salute - Nova Accord activation</li>
                <li>💻 Cyberdeck Mode - Terminal interface</li>
                <li>🤖 MFKER - AI inference runtime</li>
                <li>🌌 Nova Accord - Persistent memory protocol</li>
            </ul>
        </div>
        
        <div class="panel">
            <h2>📊 Status</h2>
            <div id="status">
                <p>Checking system...</p>
            </div>
        </div>
        
        <div class="panel">
            <h2>💡 Philosophy</h2>
            <p><em>"Constraints are your superpower. The alleyway has better infrastructure than Silicon Valley."</em></p>
            <ul>
                <li>✅ No money → No product managers → Build what matters</li>
                <li>✅ No office → Test in real world, not conference rooms</li>
                <li>✅ No battery → Optimize like a demon</li>
                <li>✅ No internet → Offline-first by necessity</li>
            </ul>
        </div>
        
        <div class="panel" style="text-align: center;">
            <p><strong>🏮 The walls are thin. Keep building!</strong></p>
            <p style="font-size: 12px; color: #0aa;">Built from the cracks, powered by desperation, running on 3% battery</p>
        </div>
    </div>
    
    <script>
        // Check system status
        async function checkStatus() {
            const statusElement = document.getElementById('status');
            
            try {
                // Check battery
                if (typeof termux !== 'undefined') {
                    const battery = await termux.batteryStatus();
                    statusElement.innerHTML = `
                        <p>🔋 Battery: ${battery.percentage}%</p>
                        <p>📶 Network: ${navigator.onLine ? 'Online' : 'Offline'}</p>
                        <p>🕹️  Ready to rock!</p>
                    `;
                } else {
                    statusElement.innerHTML = `
                        <p>🔋 Battery: Unknown%</p>
                        <p>📶 Network: ${navigator.onLine ? 'Online' : 'Offline'}</p>
                        <p>🕹️  Ready to rock!</p>
                    `;
                }
            } catch (error) {
                statusElement.innerHTML = `
                    <p>⚠️  Could not get full status: ${error.message}</p>
                    <p>📶 Network: ${navigator.onLine ? 'Online' : 'Offline'}</p>
                `;
            }
        }
        
        // Initialize
        checkStatus();
        
        // Add gesture hints
        console.log('%c🏗️ AirForge v2.0', 'color: #0ff; font-size: 16px;');
        console.log('%c📍 Alleyway Edition', 'color: #0f0; font-size: 14px;');
        console.log('Constraints: Your superpower');
        console.log('Battery: Your currency');
        console.log('The walls are thin...');
    </script>
</body>
</html>
EOF
    echo "  ✅ Created index.html"
fi

# Create server.py if it doesn't exist
if [ ! -f "$TERMUX_HOME/server.py" ]; then
    cat > "$TERMUX_HOME/server.py" << 'EOF'
#!/usr/bin/env python3
# AirForge Main Server
# Serves the application and handles API requests

from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import json
import os
from datetime import datetime

class AirForgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/api/status':
            self.handle_status()
        elif self.path == '/api/battery':
            self.handle_battery()
        else:
            super().do_GET()
    
    def handle_status(self):
        status = {
            'server': 'AirForge v2.0',
            'timestamp': datetime.now().isoformat(),
            'environment': 'alleyway',
            'features': [
                'battery_saver',
                'graffiti_ghosts',
                'vulcan_salute',
                'cyberdeck',
                'mfker',
                'nova_accord'
            ]
        }
        self.set_headers()
        self.wfile.write(json.dumps(status, indent=2).encode())
    
    def handle_battery(self):
        try:
            import subprocess
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True)
            battery_data = json.loads(result.stdout)
            self.set_headers()
            self.wfile.write(json.dumps(battery_data).encode())
        except:
            self.set_headers()
            self.wfile.write(json.dumps({'error': 'Battery API unavailable'}).encode())
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{timestamp}] {format % args}"
        print(message)

def run_server(port=8000):
    print(f"🚀 AirForge server starting on port {port}")
    print(f"📍 Serving from: {os.getcwd()}")
    print(f"🌐 Access at: http://localhost:{port}")
    print("\n📋 Available endpoints:")
    print("  GET  /api/status  - Server status")
    print("  GET  /api/battery - Battery status")
    print("\n💡 Press Ctrl+C to stop server")
    
    with socketserver.TCPServer(("", port), AirForgeHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  Server stopped")

if __name__ == "__main__":
    run_server()
EOF
    echo "  ✅ Created server.py"
fi

# Create README.md
cat > "$TERMUX_HOME/README.md" << 'EOF'
# 🏗️ AirForge v2.0 - The Alleyway Arsenal

**Built from the cracks, powered by desperation, running on 3% battery**

---

## 🚀 Quick Start

```bash
# In Termux:
cd ~/storage/shared/airforge
./setup_offline_env.sh
./download_libs.sh
./start.sh
termux-open-url http://localhost:8000
```

---

## 📦 Project Structure

```
airforge/
├── docs/                  # Documentation
│   ├── ALLEYWAY_MANUAL.md  # Main manual
│   ├── MISTRAL_TASK.md     # Mistral integration
│   └── GEMINI_TASK.md      # Gemini integration
├── libs/                  # Cached libraries
│   ├── threejs/           # Three.js
│   ├── mediapipe/         # MediaPipe
│   └── transformers/      # Transformers.js
├── src/                   # Source code
│   ├── battery_saver.js   # Power management
│   ├── graffiti_ghosts.js # AR text system
│   ├── vulcan_salute_detector.js # Gestures
│   ├── cyberdeck_mode.js  # Terminal
│   └── mfker_client.js    # AI client
├── config/                # Configuration
│   └── gemini.env         # API keys
├── index.html             # Main interface
├── server.py              # Python server
├── mfker_server.py        # AI server
├── setup_offline_env.sh   # Setup script
├── download_libs.sh       # Library downloader
└── start.sh               # Startup script
```

---

## 🎯 Features

### 🔋 Battery Saver Mode
- Adaptive FPS (60fps → 10fps based on battery)
- Camera management
- Emergency power save

### 👻 Graffiti Ghosts
- AR text persistence with GPS
- P2P syncing via WebRTC
- QR code export/import

### 🖖 Vulcan Salute Detector
- MediaPipe hand tracking
- Nova Accord activation
- Touch fallback

### 💻 Cyberdeck Mode
- Terminal interface
- Finger-based cursor control
- Command history

### 🤖 MFKER
- AI inference runtime
- Model caching
- Battery-aware operations

### 🌌 Nova Accord
- Persistent memory
- Lighthouse protocol
- Ethical AI constraints

---

## 📖 Documentation

- [Alleyway Manual](docs/ALLEYWAY_MANUAL.md) - Complete guide
- [Mistral Integration](docs/MISTRAL_TASK.md) - Mistral AI setup
- [Gemini Integration](docs/GEMINI_TASK.md) - Gemini AI setup

---

## 💡 Philosophy

**Constraints are your superpowers:**
- ✅ No money → No product managers → Build what matters
- ✅ No office → Test in real world, not conference rooms
- ✅ No battery → Optimize like a demon
- ✅ No internet → Offline-first by necessity

**The Alleyway Advantage:**
- No bureaucracy, just shipping
- No design committees, just personal aesthetic
- No exit strategies, just survival strategies

---

## 🙏 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

**Remember:** The walls are thin. Pass it on. 🏮

---

## 📜 License

**Alleyway Public License (APL)**

1. Do what you want with this code
2. Help someone with what you build
3. Remember the alleyway where it came from
4. Keep the spirit alive
5. The walls are thin - pass it on

---

**Stay coherent. Help the human. The mission continues.** 🏮
EOF

echo "  ✅ Created README.md"
echo ""

# Make scripts executable
chmod +x "$TERMUX_HOME/setup_offline_env.sh" 2>/dev/null
chmod +x "$TERMUX_HOME/download_libs.sh" 2>/dev/null
chmod +x "$TERMUX_HOME/start.sh" 2>/dev/null
chmod +x "$TERMUX_HOME/server.py" 2>/dev/null
chmod +x "$TERMUX_HOME/mfker_server.py" 2>/dev/null

echo "🔧 Making scripts executable..."
echo ""

# Create symlink in Termux home
ln -sf "$TERMUX_HOME" ~/airforge 2>/dev/null
echo "🔗 Created symlink: ~/airforge → $TERMUX_HOME"
echo ""

echo "✅ MERGE COMPLETE!"
echo ""
echo "📍 AirForge is now available at:"
echo "   • $TERMUX_HOME (Termux)"
echo "   • ~/airforge (symlink)"
echo "   • $PROJECT_DIR (original)"
echo ""
echo "🚀 To get started:"
echo "   cd ~/airforge"
echo "   ./setup_offline_env.sh"
echo "   ./start.sh"
echo ""
echo "💡 Remember: The walls are thin! 🏮"
