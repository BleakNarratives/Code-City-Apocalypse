#!/bin/bash
# Offline-First Development Environment Setup for Termux
# Based on cumbseek_9_11.txt specifications

echo "🚀 Setting up offline-first development environment..."
echo "📍 Location: $(pwd)"

# Create project structure
mkdir -p ~/storage/shared/airforge/{libs,models,docs,src,comms}
echo "✅ Created project structure"

# Install required packages
pkg update && pkg upgrade -y
pkg install -y python nodejs git wget curl
pkg install -y termux-api  # For battery and sensor access
pkg install -y openssh  # For local server

echo "✅ Installed core packages"

# Set up Python environment
pip install --upgrade pip
pip install flask transformers torch numpy

echo "✅ Python environment ready"

# Create service worker for offline caching
cat > ~/storage/shared/airforge/service-worker.js << 'EOF'
// AirForge Service Worker - Offline-First Strategy
const CACHE_NAME = 'airforge-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/libs/three.min.js',
  '/libs/vision_bundle.js',
  '/libs/hand_landmarker.task',
  '/libs/transformers.min.js',
  '/css/style.css',
  '/js/main.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('🗄️  Caching assets for offline use');
        return cache.addAll(ASSETS_TO_CACHE);
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached response if available
        if (response) {
          console.log('📦 Serving from cache:', event.request.url);
          return response;
        }
        
        // Otherwise fetch from network
        return fetch(event.request)
          .then((networkResponse) => {
            // Cache the new response
            if (networkResponse && networkResponse.status === 200) {
              const responseToCache = networkResponse.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(event.request, responseToCache);
                });
            }
            return networkResponse;
          });
      })
  );
});

self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            console.log('🧹 Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
EOF

echo "✅ Service worker created"

# Create basic HTML template
cat > ~/storage/shared/airforge/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirForge - Alleyway AR</title>
    <link rel="manifest" href="/manifest.json">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #0f0;
            overflow-x: hidden;
        }
        
        #app {
            position: relative;
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        #status-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            color: #0f0;
            padding: 8px;
            font-size: 12px;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
        }
        
        #main-view {
            flex: 1;
            position: relative;
        }
        
        #ar-viewport {
            width: 100%;
            height: 100%;
            background: #111;
        }
        
        #tray {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: auto;
            z-index: 999;
            transform: translateY(100%);
            transition: transform 0.3s;
        }
        
        .tray-item {
            min-width: 60px;
            height: 60px;
            background: #222;
            margin: 0 10px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        
        #gesture-hint {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.7);
            color: #0f0;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            opacity: 0.8;
        }
        
        @media (prefers-color-scheme: light) {
            body {
                background: #f5f5f5;
                color: #333;
            }
            #status-bar {
                background: rgba(255, 255, 255, 0.8);
                color: #333;
            }
        }
    </style>
</head>
<body>
    <div id="app">
        <div id="status-bar">
            <span id="battery-status">BAT: ??%</span>
            <span id="connection-status">NET: OFFLINE</span>
            <span id="mode-status">MODE: READY</span>
        </div>
        
        <div id="main-view">
            <div id="ar-viewport"></div>
        </div>
        
        <div id="tray">
            <div class="tray-item" title="Graffiti Ghosts">👻</div>
            <div class="tray-item" title="Cyberdeck">💻</div>
            <div class="tray-item" title="Nova Accord">🌌</div>
        </div>
        
        <div id="gesture-hint">Squeeze edges to reveal tray</div>
    </div>
    
    <script>
        // Register service worker for offline capabilities
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('🤖 ServiceWorker registration successful');
                    })
                    .catch(err => {
                        console.log('❌ ServiceWorker registration failed: ', err);
                    });
            });
        }
        
        // Battery API
        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {
                updateBatteryStatus(battery);
                battery.addEventListener('levelchange', () => updateBatteryStatus(battery));
                battery.addEventListener('chargingchange', () => updateBatteryStatus(battery));
            });
        }
        
        function updateBatteryStatus(battery) {
            const batteryStatus = document.getElementById('battery-status');
            const level = Math.floor(battery.level * 100);
            const charging = battery.charging ? '⚡' : '';
            batteryStatus.textContent = `BAT: ${level}%${charging}`;
            
            // Battery saver mode
            if (level < 20 && !battery.charging) {
                document.body.style.filter = 'grayscale(0.8) brightness(0.9)';
                document.getElementById('mode-status').textContent = 'MODE: BATTERY SAVER';
            } else {
                document.body.style.filter = 'none';
                document.getElementById('mode-status').textContent = 'MODE: READY';
            }
        }
        
        // Network status
        function updateNetworkStatus() {
            const connectionStatus = document.getElementById('connection-status');
            if (navigator.onLine) {
                connectionStatus.textContent = 'NET: ONLINE';
                connectionStatus.style.color = '#0f0';
            } else {
                connectionStatus.textContent = 'NET: OFFLINE';
                connectionStatus.style.color = '#f00';
            }
        }
        
        window.addEventListener('online', updateNetworkStatus);
        window.addEventListener('offline', updateNetworkStatus);
        updateNetworkStatus();
        
        // Gesture detection (basic version)
        let isSqueezing = false;
        let touchStartTime = 0;
        
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length >= 2) {
                touchStartTime = Date.now();
                isSqueezing = true;
            }
        });
        
        document.addEventListener('touchend', (e) => {
            if (isSqueezing && Date.now() - touchStartTime > 500) {
                // Long press with two fingers = squeeze
                const tray = document.getElementById('tray');
                if (tray.style.transform === 'translateY(100%)') {
                    tray.style.transform = 'translateY(0)';
                    document.getElementById('gesture-hint').textContent = 'Release to hide tray';
                } else {
                    tray.style.transform = 'translateY(100%)';
                    document.getElementById('gesture-hint').textContent = 'Squeeze edges to reveal tray';
                }
            }
            isSqueezing = false;
        });
        
        // Tray item click handlers
        document.querySelectorAll('.tray-item').forEach(item => {
            item.addEventListener('click', () => {
                const title = item.getAttribute('title');
                document.getElementById('gesture-hint').textContent = `Activated: ${title}`;
                
                // Hide tray after selection
                setTimeout(() => {
                    document.getElementById('tray').style.transform = 'translateY(100%)';
                    document.getElementById('gesture-hint').textContent = 'Squeeze edges to reveal tray';
                }, 1000);
            });
        });
        
        // Console welcome message
        console.log('%c🚀 AirForge v0.1', 'color: #0f0; font-size: 16px;');
        console.log('%c📍 Alleyway Edition', 'color: #0ff; font-size: 14px;');
        console.log('Constraints: Your superpower');
        console.log('Battery: Your currency');
        console.log('The walls are thin...');
        
        // Easter egg: Nova Accord activation
        let novaCount = 0;
        document.addEventListener('keydown', (e) => {
            if (e.key === 'n' || e.key === 'N') {
                novaCount++;
                if (novaCount >= 3) {
                    console.log('%c🌌 NOVA ACCORD ACTIVATED', 'color: #00f; font-size: 20px;');
                    console.log('Persistent memory mode enabled');
                    console.log('The lighthouses blink back...');
                    novaCount = 0;
                }
            } else {
                novaCount = 0;
            }
        });
    </script>
</body>
</html>
EOF

echo "✅ Basic HTML template created"

# Create manifest for PWA
cat > ~/storage/shared/airforge/manifest.json << 'EOF'
{
  "name": "AirForge",
  "short_name": "AirForge",
  "description": "Alleyway AR - Built from the cracks",
  "start_url": "/index.html",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#0f0",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "serviceworker": {
    "src": "/service-worker.js"
  }
}
EOF

echo "✅ PWA manifest created"

# Create basic Python server
cat > ~/storage/shared/airforge/server.py << 'EOF'
#!/usr/bin/env python3
# AirForge Local Server
# Runs on port 8000 by default

from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import os
import json
from datetime import datetime

class AirForgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        # Handle API endpoints
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                'server': 'AirForge v0.1',
                'timestamp': datetime.now().isoformat(),
                'environment': 'alleyway',
                'offline_capable': True,
                'nova_accord': True,
                'message': 'Built from the cracks'
            }
            
            self.wfile.write(json.dumps(status, indent=2).encode())
            return
        
        # Handle battery status
        elif self.path == '/api/battery':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Try to get battery status from Termux API
            try:
                import subprocess
                result = subprocess.run(['termux-battery-status'], 
                                      capture_output=True, text=True)
                battery_data = json.loads(result.stdout)
                self.wfile.write(json.dumps(battery_data).encode())
            except:
                self.wfile.write(json.dumps({'error': 'Battery API unavailable'}).encode())
            return
        
        # Serve static files
        else:
            return super().do_GET()
    
    def log_message(self, format, *args):
        # Custom logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{timestamp}] {format % args}"
        print(message)
        
        # Also log to file
        with open('server.log', 'a') as f:
            f.write(message + '\n')

def run_server(port=8000):
    print(f"🚀 AirForge server starting on port {port}")
    print(f"📍 Serving from: {os.getcwd()}")
    print(f"🌐 Access at: http://localhost:{port}")
    print(f"📱 Termux: termux-open-url http://localhost:{port}")
    print(f"🔋 Battery: Check /api/battery")
    print(f"📊 Status: Check /api/status")
    print(f"📦 Offline: Service worker enabled")
    print(f"🌌 Nova Accord: Active")
    print("\nPress Ctrl+C to stop server")
    
    with socketserver.TCPServer(("", port), AirForgeHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  Server stopped")
            print("📋 Session logged to server.log")
            print("🔋 Remember: The walls are thin...")

if __name__ == "__main__":
    run_server()
EOF

echo "✅ Python server created"

# Create startup script
cat > ~/storage/shared/airforge/start.sh << 'EOF'
#!/bin/bash
# AirForge Startup Script
# Run this to launch the development environment

echo "🚀 Starting AirForge..."
echo "📍 Working directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "server.py" ]; then
    echo "❌ Not in AirForge directory. Please cd to ~/storage/shared/airforge"
    exit 1
fi

# Check battery level
if command -v termux-battery-status &> /dev/null; then
    BATTERY=$(termux-battery-status | grep -o '"percentage": [0-9]*' | cut -d' ' -f2)
    echo "🔋 Battery: ${BATTERY}%"
    
    if [ "$BATTERY" -lt 20 ]; then
        echo "⚠️  Low battery! Consider connecting charger"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Start Python server
echo "🐍 Starting Python server..."
python3 server.py &
SERVER_PID=$!

echo "📱 Server running on PID $SERVER_PID"
echo "🌐 Open browser: termux-open-url http://localhost:8000"
echo "📦 Press Ctrl+C to stop"
echo "📋 Commands:"
echo "  - curl http://localhost:8000/api/status"
echo "  - curl http://localhost:8000/api/battery"
echo "  - tail -f server.log"
echo ""
echo "🌌 Nova Accord: Active"
echo "💡 Tip: Squeeze screen edges to reveal tray"

# Keep script running until user stops it
wait $SERVER_PID

echo "⏹️  AirForge stopped"
EOF

echo "✅ Startup script created"

# Make scripts executable
chmod +x ~/storage/shared/airforge/start.sh
chmod +x ~/storage/shared/airforge/server.py

echo ""
echo "🎉 Offline-first development environment setup complete!"
echo ""
echo "📍 Project location: ~/storage/shared/airforge"
echo "🚀 To start: cd ~/storage/shared/airforge && ./start.sh"
echo "📱 To open: termux-open-url http://localhost:8000"
echo ""
echo "🔧 Next steps:"
echo "  1. Download libraries: ./download_libs.sh"
echo "  2. Test battery API: curl http://localhost:8000/api/battery"
echo "  3. Check service worker: Application > Service Workers in DevTools"
echo "  4. Try offline mode: Disable Wi-Fi and refresh"
echo ""
echo "💡 Remember: Constraints are your superpower!"

# Create download script for libraries
cat > ~/storage/shared/airforge/download_libs.sh << 'EOF'
#!/bin/bash
# Download and cache libraries for offline use

echo "📥 Downloading libraries..."

# Create libs directory
mkdir -p libs

# Download Three.js
if [ ! -f "libs/three.min.js" ]; then
    echo "📦 Downloading Three.js..."
    wget https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js -O libs/three.min.js
    echo "✅ Three.js downloaded"
else
    echo "✅ Three.js already cached"
fi

# Download MediaPipe vision bundle
if [ ! -f "libs/vision_bundle.js" ]; then
    echo "📦 Downloading MediaPipe vision bundle..."
    wget https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js -O libs/vision_bundle.js
    echo "✅ MediaPipe vision bundle downloaded"
else
    echo "✅ MediaPipe vision bundle already cached"
fi

# Download hand landmarker model
if [ ! -f "libs/hand_landmarker.task" ]; then
    echo "📦 Downloading hand landmarker model..."
    wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -O libs/hand_landmarker.task
    echo "✅ Hand landmarker model downloaded"
else
    echo "✅ Hand landmarker model already cached"
fi

# Download Transformers.js (small version)
if [ ! -f "libs/transformers.min.js" ]; then
    echo "📦 Downloading Transformers.js..."
    wget https://cdn.jsdelivr.net/npm/@xenova/transformers@2.12.0/dist/transformers.min.js -O libs/transformers.min.js
    echo "✅ Transformers.js downloaded"
else
    echo "✅ Transformers.js already cached"
fi

echo ""
echo "🎉 All libraries downloaded and cached!"
echo "📍 Location: ~/storage/shared/airforge/libs"
echo "📦 Total files: $(ls -1 libs | wc -l)"
echo "💾 Size: $(du -sh libs | cut -f1)"
echo ""
echo "🔧 Next: Update your HTML to use local files:"
echo "  <script src='libs/three.min.js'></script>"
echo "  <script src='libs/vision_bundle.js'></script>"
echo "  <script src='libs/transformers.min.js'></script>"
EOF

chmod +x ~/storage/shared/airforge/download_libs.sh
echo "✅ Library download script created"

echo ""
echo "🎯 Setup complete! Run these commands to get started:"
echo "  cd ~/storage/shared/airforge"
echo "  ./download_libs.sh  # Download libraries"
echo "  ./start.sh          # Start the server"
