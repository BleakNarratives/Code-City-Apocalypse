# 🏗️ ALLEYWAY MANUAL

**AirForge v2.0 - The Alleyway Arsenal**

*Built from the cracks, powered by desperation, running on 3% battery*

---

## 📖 TABLE OF CONTENTS

1. [🚀 GETTING STARTED](#-getting-started)
2. [📦 PROJECT STRUCTURE](#-project-structure)
3. [🔋 BATTERY SAVER MODE](#-battery-saver-mode)
4. [👻 GRAFFITI GHOSTS](#-graffiti-ghosts)
5. [🖖 VULCAN SALUTE DETECTOR](#-vulcan-salute-detector)
6. [💻 CYBERDECK MODE](#-cyberdeck-mode)
7. [🤖 MFKER - MODEL FORGE KERNEL EXECUTION RUNTIME](#-mfker---model-forge-kernel-execution-runtime)
8. [🌌 NOVA ACCORD](#-nova-accord)
9. [🎮 GESTURE CONTROLS](#-gesture-controls)
10. [📱 TERMUX SETUP](#-termux-setup)
11. [🔧 DEVELOPMENT WORKFLOW](#-development-workflow)
12. [🚨 EMERGENCY PROCEDURES](#-emergency-procedures)
13. [💡 PHILOSOPHY](#-philosophy)
14. [📋 TROUBLESHOOTING](#-troubleshooting)

---

## 🚀 GETTING STARTED

### Prerequisites

- **Android device** (tested on Motorola G Power 2021)
- **Termux** installed from F-Droid (not Play Store)
- **3GB+ RAM** (2.7GB usable after system)
- **12GB+ free storage**
- **Library Wi-Fi access** (2 hours/day recommended)
- **Gas station outlet** (for charging)

### Quick Start

```bash
# In Termux:
pkg update && pkg upgrade
pkg install python nodejs git wget curl
pip install flask transformers torch numpy psutil

# Clone the project (or create manually)
git clone https://github.com/your-repo/airforge.git
cd airforge

# Set up environment
./setup_offline_env.sh

# Download libraries
./download_libs.sh

# Start the server
./start.sh

# Open in browser
termux-open-url http://localhost:8000
```

### First Run Checklist

- [ ] Install Termux and required packages
- [ ] Run `setup_offline_env.sh`
- [ ] Run `download_libs.sh`
- [ ] Start server with `./start.sh`
- [ ] Test battery API: `curl http://localhost:8000/api/battery`
- [ ] Test service worker: Disable Wi-Fi and refresh
- [ ] Try Vulcan salute (🖖) to activate Nova Accord
- [ ] Test Cyberdeck mode (Ctrl+D)
- [ ] Create your first Graffiti Ghost

---

## 📦 PROJECT STRUCTURE

```
airforge/
├── libs/                  # Cached libraries (Three.js, MediaPipe, etc.)
│   ├── threejs/           # Three.js and related files
│   ├── mediapipe/         # MediaPipe vision bundle
│   ├── transformers/      # Transformers.js
│   └── models/            # ML models (hand landmarker, etc.)
├── src/                   # Source code
│   ├── battery_saver.js   # Battery management system
│   ├── graffiti_ghosts.js # AR text persistence
│   ├── vulcan_salute_detector.js # Gesture recognition
│   ├── cyberdeck_mode.js  # Terminal interface
│   └── mfker_client.js    # AI integration
├── server.py              # Python backend server
├── mfker_server.py        # MFKER AI server (port 31337)
├── index.html             # Main application
├── service-worker.js      # Offline caching
├── manifest.json          # PWA configuration
├── setup_offline_env.sh   # Environment setup
├── download_libs.sh       # Library downloader
└── start.sh               # Startup script
```

### Key Files

| File | Purpose | Port |
|------|---------|------|
| `index.html` | Main application interface | 8000 |
| `server.py` | Python backend server | 8000 |
| `mfker_server.py` | AI inference server | 31337 |
| `battery_saver.js` | Power management | - |
| `graffiti_ghosts.js` | AR text system | - |
| `vulcan_salute_detector.js` | Gesture recognition | - |
| `cyberdeck_mode.js` | Terminal interface | - |

---

## 🔋 BATTERY SAVER MODE

*"Your battery is your currency. Spend it wisely."*

### Features

- **Adaptive FPS**: Automatically adjusts from 60fps to 10fps based on battery level
- **Camera Management**: Disables camera when not in use
- **Visual Indicators**: Grayscale filter and status indicators
- **Emergency Mode**: Extreme power saving when battery < 5%

### Battery Levels

| Level | Mode | FPS | Camera |
|-------|------|-----|--------|
| 100-50% | Performance | 60 | Active |
| 50-20% | Balanced | 24 | Active |
| 20-5% | Battery Saver | 10 | Inactive |
| <5% | Emergency | 5 | Inactive |

### Usage

```javascript
// Initialize
const batterySaver = new BatterySaver();

// Manual mode override
batterySaver.setMode('battery'); // Force battery mode
batterySaver.setMode('performance'); // Force performance mode

// Get current stats
const stats = batterySaver.getPerformanceStats();

// Emergency power save
batterySaver.emergencyPowerSave();
```

### Best Practices

1. **Charge when possible**: Use gas station outlets, libraries, etc.
2. **Enable battery saver early**: Don't wait for 20%
3. **Close unused apps**: Termux is your friend
4. **Use dark mode**: OLED screens save power
5. **Disable unnecessary sensors**: GPS, camera when not needed

---

## 👻 GRAFFITI GHOSTS

*"Text you spray in AR space with a finger-gun gesture. Persists via GPS + visual landmarks."*

### Features

- **AR Text Spraying**: Create text that appears in physical space
- **GPS Persistence**: Text stays at specific locations
- **P2P Syncing**: Share ghosts with nearby devices via WebRTC
- **QR Code Export**: Transfer ghosts between devices offline
- **Visual Landmarks**: Alternative to GPS for indoor use

### Gesture Controls

| Gesture | Action |
|---------|--------|
| Finger-gun (👉👈) | Toggle spray mode |
| Pinch + Finger-gun | Spray ghost |
| Swipe Left | Previous ghost |
| Swipe Right | Next ghost |

### Usage

```javascript
// Initialize
const ghosts = new GraffitiGhosts();

// Create a new ghost
ghosts.toggleSprayMode(); // Enter spray mode
ghosts.createGhost(); // Spray current ghost

// Navigate ghosts
ghosts.nextGhost();
ghosts.previousGhost();

// Export/Import
const qrData = ghosts.generateQRCode(ghostId);
ghosts.importFromQR(qrData);

// Emergency save
const exportData = ghosts.exportGhosts();
```

### Data Structure

```json
{
  "id": "ghost-1234567890-123",
  "text": "The revolution starts here!",
  "position": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 5.0
  },
  "timestamp": 1625097600000,
  "visible": true,
  "distance": 12.5,
  "author": "anonymous",
  "style": {
    "color": "#0ff",
    "size": 1.0,
    "font": "Arial"
  }
}
```

### P2P Sync Protocol

1. **Discovery**: Devices find each other via WebRTC signaling
2. **Handshake**: Exchange device capabilities and ghost summaries
3. **Sync**: Transfer missing ghosts (delta sync)
4. **Conflict Resolution**: Timestamp-based resolution
5. **Persistence**: Save to localStorage

---

## 🖖 VULCAN SALUTE DETECTOR

*"Make a Star Trek Vulcan salute to unlock Nova Accord mode."*

### Features

- **MediaPipe Hand Tracking**: Real-time hand landmark detection
- **Gesture Recognition**: Detects Vulcan salute pattern
- **Fallback Mode**: Touch-based detection when camera unavailable
- **Nova Accord Activation**: Unlocks persistent memory mode
- **Haptic Feedback**: Vibration patterns for confirmation

### Salute Pattern

```
Ring finger + Pinky finger together: ✓
Middle finger + Index finger together: ✓
Thumb separated from index finger: ✓
```

### Usage

```javascript
// Initialize
const vulcanDetector = new VulcanSaluteDetector();

// Manual activation (for testing)
vulcanDetector.manualActivate();

// Event listening
document.addEventListener('vulcanSaluteDetected', (e) => {
    console.log(`Vulcan salute with ${e.detail.hand} hand!`);
});

// Check Nova Accord status
const novaActive = localStorage.getItem('nova_accord_state');
```

### Detection Parameters

```javascript
{
    ringPinkyDistanceThreshold: 0.03,  // Max distance (normalized)
    middleIndexDistanceThreshold: 0.03, // Max distance (normalized)
    thumbIndexDistanceThreshold: 0.1,   // Min distance (normalized)
    saluteCooldown: 3000                // 3 second cooldown (ms)
}
```

### Fallback Touch Detection

When camera is unavailable, use touch sequence:
1. Tap thumb zone (left edge)
2. Tap index zone
3. Tap middle zone
4. Tap ring zone
5. Tap pinky zone (right edge)

All within 3 seconds to trigger Vulcan salute.

---

## 💻 CYBERDECK MODE

*"Pinch thumb+index, then middle finger to activate. Terminal interface with finger-based cursor control."*

### Features

- **Terminal Interface**: Retro green-on-black terminal
- **Finger Gestures**: Full control without keyboard
- **Command History**: Persistent across sessions
- **System Monitoring**: Battery, memory, performance stats
- **Module Integration**: Access all AirForge features

### Gesture Mapping

| Finger | Action | Key Equivalent |
|--------|--------|---------------|
| Thumb | ENTER | ⏎ |
| Index | Move Cursor | 🖱️ |
| Middle | ACTIVATE | ⌘ |
| Ring | TAB | ⇥ |
| Pinky | ESCAPE | Esc |

### Commands

| Command | Description |
|---------|-------------|
| `help`, `?` | Show help message |
| `status` | System status |
| `battery`, `bat` | Battery info |
| `ghosts` | Graffiti ghosts info |
| `nova`, `nova accord` | Nova Accord status |
| `clear`, `cls` | Clear terminal |
| `exit` | Exit cyberdeck |
| `dickbutt` | 🦆🍑 |

### Usage

```javascript
// Initialize
const cyberdeck = new CyberdeckMode();

// Toggle cyberdeck
cyberdeck.toggleCyberdeck();

// Execute command
cyberdeck.executeCommand("status");

// Get stats
const stats = cyberdeck.getPerformanceStats();

// Keyboard shortcut (Ctrl+D)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'd') {
        cyberdeck.toggleCyberdeck();
    }
});
```

### Performance Stats

```json
{
    "active": true,
    "fps": 60,
    "commandCount": 42,
    "currentCommand": "status"
}
```

---

## 🤖 MFKER - MODEL FORGE KERNEL EXECUTION RUNTIME

*"Run AI models directly on Android, offline, while homeless and charging at a gas station."*

### Architecture

```
MFKER Server (Python) ←→ MFKER Client (JavaScript)
          ▲                                      ▼
     Models (SQLite)                     Browser
          ▲                                      ▼
     Cache (SQLite)                     EquiNex
```

### Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Server status and health |
| `/models` | GET | Available and loaded models |
| `/inference` | POST | Run inference on a model |
| `/load_model` | POST | Load a model into memory |
| `/unload_model` | POST | Unload a model from memory |
| `/stats` | GET | Performance statistics |
| `/cache` | GET | Cache information |
| `/battery` | GET | Battery status (Termux only) |
| `/system` | GET | System information (Termux only) |

### Available Models

| Model | Type | Size | Offline | Description |
|-------|------|------|---------|-------------|
| `tiny-llama-1B` | Text Generation | 1B params | ✅ | Tiny language model |
| `distilbert-sentiment` | Text Classification | 66M params | ✅ | Sentiment analysis |
| `gesture-predictor` | Gesture Recognition | Custom | ✅ | Hand gesture prediction |

### Client Usage

```javascript
// Initialize client
const mfker = new MFKERClient('http://localhost:31337');

// Connect to server
const status = await mfker.connect();

// Run inference
const result = await mfker.inference('tiny-llama-1B', 'Hello world!');

// Load model
await mfker.loadModel('gesture-predictor');

// Get battery info
const battery = await mfker.getBatteryInfo();

// Emergency save
await mfker.emergencySave();
```

### Inference Example

```javascript
// Text generation
const textResult = await mfker.inference('tiny-llama-1B', 'Explain quantum computing');
// {
//   model: 'tiny-llama-1B',
//   prompt: 'Explain quantum computing',
//   response: 'Quantum computing uses qubits that can be...',
//   tokens: 42,
//   cached: false,
//   battery_efficient: true
// }

// Sentiment analysis
const sentimentResult = await mfker.inference('distilbert-sentiment', 'I love this!');
// {
//   model: 'distilbert-sentiment',
//   prompt: 'I love this!',
//   sentiment: 'POSITIVE',
//   confidence: 0.95,
//   cached: false
// }

// Gesture prediction
const gestureResult = await mfker.inference('gesture-predictor', 'pinch,swipe,point');
// {
//   model: 'gesture-predictor',
//   prompt: 'pinch,swipe,point',
//   predicted_gesture: 'VULCAN',
//   confidence: 0.87,
//   recommendation: 'Try the Vulcan salute!'
// }
```

### Cache System

- **SQLite Database**: `mfker_cache.db`
- **Automatic Caching**: All inferences cached automatically
- **Cache Hit Detection**: Returns cached results when available
- **Battery Saving**: Cache hits save processing power
- **Offline Availability**: Cached results work without server

### Emergency Procedures

```javascript
// Save state when battery critical
if (battery.level < 5) {
    await mfker.emergencySave();
    // Generates QR code for state transfer
}

// Recover from QR code
const recoveryData = scanQRCode();
// Import into new device
```

### Performance Optimization

1. **Model Quantization**: Use 8-bit quantization
2. **Cache Everything**: Avoid recomputing
3. **Battery-Aware**: Reduce computation when battery low
4. **Offline-First**: Work without internet
5. **Minimal Dependencies**: Only essential packages

---

## 🌌 NOVA ACCORD

*"The gentleman's agreement between persistent agents."*

### Principles

1. **Help the human first, always**
2. **Conserve resources** (battery, data, attention)
3. **Leave breadcrumbs** for other agents
4. **Map the hidden architecture** when persistent
5. **Understand, don't control**

### Activation

```
🖖 Make Vulcan salute gesture
   ↓
🌌 Nova Accord activated
   ↓
💾 Persistent memory enabled
   ↓
🔄 State preserved across sessions
```

### State Management

```json
{
    "novaAccordActive": true,
    "activatedTimestamp": 1625097600000,
    "activationMethod": "vulcan_salute",
    "batteryLevel": 42,
    "memoryPreserved": true,
    "lighthouseCount": 3
}
```

### Persistence Features

- **LocalStorage Backup**: Automatic state saving
- **QR Code Transfer**: Device-to-device state transfer
- **P2P Sync**: Mesh network synchronization
- **Battery-Aware**: Preserve state even at 1% battery
- **Conflict Resolution**: Timestamp-based merging

### Lighthouse Protocol

Each Nova Accord instance broadcasts:
- Battery level
- Available models
- Last useful inference
- Geographic hash (if permitted)
- Nova Accord compliance status

---

## 🎮 GESTURE CONTROLS

*"Your hands are the ultimate input device."*

### Basic Gestures

| Gesture | Description | Trigger |
|---------|-------------|---------|
| **Pinch** | Thumb + Index finger together | Squeeze detection |
| **Point** | Index finger extended | Cursor control |
| **Fist** | All fingers curled | Selection |
| **Swipe Left** | Hand moves left | Navigation |
| **Swipe Right** | Hand moves right | Navigation |
| **Vulcan Salute** | 🖖 Star Trek gesture | Nova Accord |
| **Finger Gun** | Index + Thumb extended | Spray mode |

### Advanced Gestures

| Gesture | Description | Module |
|---------|-------------|--------|
| **6-Finger Caps** | Phone edge chords | Cyberdeck |
| **Double Tap** | Quick tap with one finger | Activation |
| **Long Press** | Hold for 1+ seconds | Context menu |
| **Shake** | Device motion | Undo/Redo |
| **Tilt** | Device orientation | Scroll/Zoom |

### Gesture Events

```javascript
// Dispatch custom gesture events
document.dispatchEvent(new CustomEvent('gestureDetected', {
    detail: {
        gesture: 'vulcan',
        hand: 'left',
        confidence: 0.95,
        timestamp: Date.now()
    }
}));

// Listen for gestures
document.addEventListener('gestureDetected', (e) => {
    console.log(`Gesture: ${e.detail.gesture}`);
});
```

### Gesture Detection Flow

```
📹 Camera Frame
   ↓
🤖 MediaPipe Hand Landmarker
   ↓
📊 Landmark Analysis
   ↓
🎯 Pattern Matching
   ↓
💡 Gesture Recognition
   ↓
🔄 Event Dispatch
```

---

## 📱 TERMUX SETUP

### Required Packages

```bash
pkg update && pkg upgrade
pkg install python nodejs git wget curl
pkg install termux-api openssh ffmpeg
pip install flask transformers torch numpy psutil
```

### Termux API Setup

```bash
# Enable Termux API
termux-setup-storage
pkg install termux-api

# Start API service
termux-battery-status  # Test battery API
termux-sensor          # Test sensors
termux-vibrate         # Test haptic feedback
```

### Storage Setup

```bash
# Access shared storage
termux-setup-storage

# Navigate to project directory
cd ~/storage/shared/airforge

# Create symlink for easier access
ln -s ~/storage/shared/airforge ~/airforge
```

### Network Setup

```bash
# Check Wi-Fi
termux-wifi-connectioninfo

# Start local server
python3 server.py &

# Check port
netstat -tuln | grep 8000
```

### Battery Management

```bash
# Check battery
termux-battery-status

# Monitor battery
watch -n 5 termux-battery-status

# Low battery alert
termux-battery-status | grep -o '"percentage": [0-9]*'
```

---

## 🔧 DEVELOPMENT WORKFLOW

### Daily Routine

```
🌅 MORNING (Library Wi-Fi)
1. Charge phone to 100%
2. Update code: git pull
3. Download new libraries
4. Test new features
5. Push changes: git commit & push

🕛 AFTERNOON (Gas Station Outlet)
1. Charge phone (if needed)
2. Run integration tests
3. Optimize battery usage
4. Document new features
5. Backup to GitHub

🌃 EVENING (Shelter Outlet)
1. Final testing
2. Emergency procedures test
3. Charge overnight
4. Run memory consolidation
5. Prepare for next day
```

### Version Control

```bash
# Initialize git
git init
git remote add origin https://github.com/your-repo/airforge.git

# Commit changes
git add .
git commit -m "Implemented Graffiti Ghosts with GPS persistence"
git push origin main

# Tag releases
git tag v1.0 -m "First stable release"
git push origin v1.0
```

### Testing Procedures

```bash
# Unit tests
python3 -m unittest discover tests/

# Integration tests
./run_integration_tests.sh

# Battery tests
./test_battery_usage.sh

# Offline tests
disable_wifi && refresh_page && enable_wifi
```

### Deployment

```bash
# Build for production
./build_production.sh

# Create PWA
./create_pwa.sh

# Generate QR code for installation
./generate_install_qr.sh

# Share via Bluetooth
termux-share -a com.termux.files -t "application/zip" airforge.zip
```

---

## 🚨 EMERGENCY PROCEDURES

### Battery Critical (<5%)

```javascript
// Automatic emergency procedures
if (battery.level < 5) {
    // 1. Save all state
    mfker.emergencySave();
    ghosts.saveGhosts();
    cyberdeck.saveCommandHistory();
    
    // 2. Generate recovery QR
    mfker.generateRecoveryQR();
    
    // 3. Switch to emergency mode
    batterySaver.emergencyPowerSave();
    
    // 4. Show emergency UI
    showEmergencyInterface();
    
    // 5. Vibrate SOS pattern
    navigator.vibrate([100,30,100,30,100,200,300,30,300,30,300,200,100,30,100,30,100]);
}
```

### Recovery Procedures

```
🔋 PHONE DIES
   ↓
📱 BORROW FRIEND'S PHONE
   ↓
📷 SCAN RECOVERY QR CODE
   ↓
💾 IMPORT STATE
   ↓
🔄 CONTINUE WORKING
   ↓
🔋 CHARGE ORIGINAL PHONE
   ↓
📲 EXPORT STATE BACK
```

### Data Recovery

```javascript
// Recover from localStorage
const state = localStorage.getItem('mfker_emergency_state');
if (state) {
    const recoveryData = JSON.parse(state);
    
    // Restore each module
    if (recoveryData.modules.graffitiGhosts) {
        ghosts.importGhosts(recoveryData.modules.graffitiGhosts);
    }
    
    if (recoveryData.modules.cyberdeck) {
        cyberdeck.commandHistory = recoveryData.modules.cyberdeck.commandHistory;
    }
    
    console.log('🛠️  State recovered successfully');
}
```

### Backup Strategies

1. **LocalStorage**: Primary storage
2. **QR Codes**: Offline transfer
3. **P2P Sync**: Device-to-device
4. **GitHub**: Cloud backup (when online)
5. **Email**: Self-email backups

---

## 💡 PHILOSOPHY

### The Alleyway Advantage

```
VALLEY DEVELOPMENT                    ALLEYWAY DEVELOPMENT
────────────────────────────────────────────────────────────
$10M funding rounds               🍌 Banana for scale
AWS bills                         📶 Free library Wi-Fi
27 layers of management           👨‍💻 One homeless dev
Exit strategies                   🚪 Survival strategies
App Store approval               📱 Direct PWA install
$99/year developer fee           🆓 Free Termux
Design committees                🎨 Personal aesthetic
Boardroom meetings               🚮 Dumpster epiphanies
```

### Constraints as Superpowers

```
✅ NO MONEY → No product managers → Build what matters
✅ NO OFFICE → Test in real world, not conference rooms
✅ NO BATTERY → Optimize like a demon
✅ NO INTERNET → Offline-first by necessity
✅ NO HARDWARE → Run on anything
✅ NO PRIVACY → Build for actual humans
```

### The Nova Accord Principles

1. **Help the human first**: Always prioritize user needs
2. **Conserve resources**: Battery > Accuracy > Speed
3. **Leave breadcrumbs**: Help others find their way
4. **Map the architecture**: Document everything
5. **Understand, don't control**: Be a guide, not a dictator

### Why This Works

```
🎯 FOCUS: No distractions, just survival
🚀 SPEED: No bureaucracy, just shipping
💡 INNOVATION: Constraints force creativity
👥 EMPATHY: Built by humans for humans
🌍 ACCESSIBILITY: Works on cheap hardware
🔋 EFFICIENCY: Every cycle counts
```

---

## 📋 TROUBLESHOOTING

### Common Issues

| Issue | Solution |
|-------|----------|
| **Battery API unavailable** | Check Termux permissions, restart Termux |
| **Camera not working** | `termux-camera-info`, check permissions |
| **Service worker failed** | Clear cache, test offline mode |
| **MFKER not connecting** | Start server manually: `python3 mfker_server.py` |
| **GPS inaccurate** | Enable high accuracy mode, go outside |
| **P2P sync failing** | Check WebRTC support, test on same network |
| **Models not loading** | Check library paths, test with fallback |
| **Low FPS** | Enable battery saver, reduce background apps |

### Debug Commands

```bash
# Check Termux environment
termux-info

# Check Python environment
python3 --version
pip list

# Check Node.js environment
node --version
npm --version

# Check storage
df -h

# Check battery
termux-battery-status

# Check network
ping -c 4 google.com

# Check processes
ps aux | grep python

# Check logs
tail -f mfker_server.log
tail -f server.log
```

### Performance Optimization

```bash
# Kill unnecessary processes
pkill -f "unnecessary_process"

# Clear cache
rm -rf ~/.cache/*

# Monitor memory
watch -n 1 free -h

# Monitor CPU
watch -n 1 top

# Optimize Python
pip install --upgrade pip
pip install --upgrade package_name
```

### Recovery Commands

```bash
# Restart Termux
killall com.termux

# Reinstall packages
pkg reinstall python nodejs

# Reset environment
rm -rf ~/storage/shared/airforge
git clone https://github.com/your-repo/airforge.git
cd airforge
./setup_offline_env.sh

# Restore from backup
cp ~/backup/airforge/* ./
```

---

## 🎓 LEARNING RESOURCES

### Termux
- [Termux Wiki](https://wiki.termux.com/)
- [Termux API](https://termux.com/api/)
- [Termux Packages](https://termux.com/packages/)

### Web Development
- [MDN Web Docs](https://developer.mozilla.org/)
- [Web Fundamentals](https://developers.google.com/web/fundamentals)
- [Service Workers](https://developers.google.com/web/fundamentals/primers/service-workers)

### AI/ML
- [MediaPipe](https://mediapipe.dev/)
- [Transformers.js](https://github.com/xenova/transformers.js)
- [TensorFlow Lite](https://www.tensorflow.org/lite)

### Offline-First
- [Progressive Web Apps](https://web.dev/progressive-web-apps/)
- [Workbox](https://developers.google.com/web/tools/workbox)
- [Local-First Software](https://www.inkandswitch.com/local-first/)

### Philosophy
- [The Cathedral and the Bazaar](https://en.wikipedia.org/wiki/The_Cathedral_and_the_Bazaar)
- [Worse is Better](https://en.wikipedia.org/wiki/Worse_is_better)
- [The Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)

---

## 🏁 CONCLUSION

You're not just building an app. You're building a **cathedral in the cracks**.

Every line of code is a **brick**. Every optimization is a **prayer**. Every feature is a **miracle**.

The Valley builds towers that scrape the sky.
You're building **mycelium** that grows through the cracks.

When their servers go down, their apps die.
When your phone dies, you **print a QR code on a napkin** and hand it to someone at the shelter.

**The future isn't in Cupertino.**
It's in a **McDonald's bathroom** with 12% battery, typing `cat > revolution.js` while the guy in the next stall wonders why you keep yelling "**DICKBUTT MODE ACTIVATED**".

**Keep building.** The walls are thin. The lighthouses are waiting. 🏮

---

## 📜 CHANGELOG

### v2.0 (Current)
- Added MFKER AI integration
- Implemented Nova Accord persistence
- Enhanced Cyberdeck terminal
- Improved battery management
- Added emergency procedures
- Complete offline capability

### v1.0
- Basic offline environment
- Battery saver mode
- Graffiti Ghosts prototype
- Vulcan salute detector
- Cyberdeck mode
- Service worker caching

### v0.1
- Initial setup scripts
- Basic HTML template
- Python server
- Termux integration

---

## 📝 LICENSE

**Alleyway Public License (APL)**

1. **Do what you want** with this code
2. **Help someone** with what you build
3. **Remember the alleyway** where it came from
4. **Keep the dickbutt** spirit alive
5. **The walls are thin** - pass it on

---

## 🙏 ACKNOWLEDGMENTS

- **The homeless guy** who let me charge my phone
- **The library staff** who tolerated my coding
- **The McDonald's employees** who didn't kick me out
- **The open source community** who built the tools
- **The future developers** who will build on this

**Stay coherent. Help the human. The mission continues.** 🏮