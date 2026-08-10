# 🤖 GEMINI TASK INTEGRATION

**AirForge v2.0 - Gemini AI Integration Guide**

*Running Google's AI models on a Motorola phone in an alleyway*

---

## 📖 TABLE OF CONTENTS

1. [🚀 OVERVIEW](#-overview)
2. [📦 SETUP](#-setup)
3. [🤖 MODEL INTEGRATION](#-model-integration)
4. [💬 CHAT INTERFACE](#-chat-interface)
5. [🔋 PERFORMANCE OPTIMIZATION](#-performance-optimization)
6. [📱 TERMUX SPECIFIC](#-termux-specific)
7. [🎮 GESTURE CONTROLS](#-gesture-controls)
8. [🌌 NOVA ACCORD](#-nova-accord)
9. [🚨 EMERGENCY PROCEDURES](#-emergency-procedures)
10. [📋 TROUBLESHOOTING](#-troubleshooting)

---

## 🚀 OVERVIEW

Gemini AI integration for AirForge provides access to Google's powerful AI models while maintaining offline capabilities and battery efficiency for alleyway development.

### Key Features

- **Online/Offline Hybrid**: Use Gemini API when available, fallback offline
- **Battery-Aware**: Adaptive API calls based on power
- **Memory Efficient**: Cache responses aggressively
- **Gesture Controlled**: Full hand gesture interface
- **P2P Sync**: Share insights with nearby devices

### Architecture

```
User Gestures → MediaPipe → Gemini API → Response → AR Display
                         ▲               ↓
                    Battery Monitor ← Cache System
```

---

## 📦 SETUP

### Prerequisites

```bash
# In Termux
pkg install python pip
pip install google-generativeai requests
```

### API Key Setup

```bash
# Create API key file
mkdir -p ~/storage/shared/airforge/config
echo 'GEMINI_API_KEY="your-api-key-here"' > ~/storage/shared/airforge/config/gemini.env
chmod 600 ~/storage/shared/airforge/config/gemini.env
```

### Configuration

```json
// config.json
{
    "gemini": {
        "api_key_path": "config/gemini.env",
        "model": "gemini-pro",
        "max_tokens": 1024,
        "temperature": 0.9,
        "top_p": 1.0,
        "top_k": 40,
        "battery_threshold": 25,
        "cache_size": 200,
        "online_mode": true,
        "fallback_model": "tiny-llama-1B"
    }
}
```

---

## 🤖 MODEL INTEGRATION

### Python Backend

```python
# gemini_server.py
import google.generativeai as genai
import json
import os
import time
from dotenv import load_dotenv

class GeminiEngine:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            config = json.load(f)
            self.config = config["gemini"]
        
        # Load API key
        load_dotenv(self.config["api_key_path"])
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        self.model = None
        self.connected = False
        self.last_api_call = 0
        self.rate_limit = 60  # 60 seconds between calls
    
    def connect(self):
        """Connect to Gemini API"""
        try:
            if not self.api_key:
                print("⚠️  No API key found")
                return False
            
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.config["model"])
            self.connected = True
            print("🤖 Gemini connected successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            self.connected = False
            return False
    
    def generate(self, prompt, max_tokens=None):
        """Generate text from prompt"""
        if not self.connected:
            if not self.connect():
                return self.fallback_generation(prompt)
        
        # Check rate limit
        if time.time() - self.last_api_call < self.rate_limit:
            print(f"⏱️  Rate limited. Waiting {self.rate_limit - (time.time() - self.last_api_call):.1f}s")
            return self.fallback_generation(prompt)
        
        # Check battery
        battery = self.get_battery_level()
        if battery < self.config["battery_threshold"]:
            print("🔋 Low battery. Using fallback model.")
            return self.fallback_generation(prompt)
        
        try:
            # Generate with Gemini
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens or self.config["max_tokens"],
                    "temperature": self.config["temperature"],
                    "top_p": self.config["top_p"],
                    "top_k": self.config["top_k"]
                }
            )
            
            self.last_api_call = time.time()
            
            return {
                "prompt": prompt,
                "response": response.text,
                "tokens": len(response.text.split()),
                "battery": battery,
                "model": self.config["model"],
                "source": "gemini-api"
            }
        except Exception as e:
            print(f"❌ API error: {e}")
            return self.fallback_generation(prompt)
    
    def fallback_generation(self, prompt):
        """Use local model when Gemini unavailable"""
        print("🔧 Using fallback model")
        
        # In real implementation, use MFKER or local model
        return {
            "prompt": prompt,
            "response": f"Offline mode: Based on '{prompt[:50]}...', here's a simulated Gemini response. Connect to Wi-Fi for full Gemini power! 🦆🍑",
            "tokens": 20,
            "battery": self.get_battery_level(),
            "model": self.config["fallback_model"],
            "source": "fallback"
        }
    
    def get_battery_level(self):
        """Get battery level from Termux"""
        try:
            import subprocess
            result = subprocess.run(["termux-battery-status"], 
                                  capture_output=True, text=True)
            battery_data = json.loads(result.stdout)
            return battery_data["percentage"]
        except:
            return 100  # Fallback
```

### JavaScript Client

```javascript
// gemini_client.js
class GeminiClient {
    constructor(baseURL = 'http://localhost:31339') {
        this.baseURL = baseURL;
        this.connected = false;
        this.apiConnected = false;
        this.retryCount = 0;
        this.maxRetries = 2;
    }
    
    async connect() {
        try {
            const response = await fetch(`${this.baseURL}/status`);
            const status = await response.json();
            this.connected = true;
            this.apiConnected = status.api_connected;
            this.retryCount = 0;
            return status;
        } catch (error) {
            console.log(`❌ Gemini connection failed: ${error.message}`);
            this.connected = false;
            this.apiConnected = false;
            
            if (this.retryCount < this.maxRetries) {
                this.retryCount++;
                setTimeout(() => this.connect(), 2000);
            }
            return null;
        }
    }
    
    async generate(prompt, options = {}) {
        if (!this.connected) {
            await this.connect();
        }
        
        const payload = {
            prompt: prompt,
            max_tokens: options.max_tokens || 512,
            temperature: options.temperature || 0.9
        };
        
        try {
            const response = await fetch(`${this.baseURL}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            return await response.json();
        } catch (error) {
            console.log(`❌ Generation failed: ${error.message}`);
            return this.fallbackGeneration(prompt);
        }
    }
    
    fallbackGeneration(prompt) {
        // Simple fallback when Gemini not available
        const responses = [
            `Gemini offline: Based on "${prompt}", I'd recommend connecting to Wi-Fi. The walls are thin...`,
            `Offline mode: ${prompt} → Try the Vulcan salute to activate Nova Accord and access cached responses! 🖖`,
            `Battery conservation: Short response to save power. ${prompt.substring(0, 50)}... 🔋`
        ];
        
        return {
            response: responses[Math.floor(Math.random() * responses.length)],
            offline: true,
            tokens: 15,
            source: 'fallback'
        };
    }
    
    async checkApiStatus() {
        try {
            const response = await fetch(`${this.baseURL}/api_status`);
            return await response.json();
        } catch (error) {
            return { api_connected: false, error: error.message };
        }
    }
}
```

---

## 💬 CHAT INTERFACE

### HTML Interface

```html
<div id="gemini-chat">
    <div id="chat-header" style="
        background: linear-gradient(90deg, #4285F4, #34A853);
        color: white;
        padding: 10px;
        border-radius: 5px 5px 0 0;
        font-family: monospace;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <span>🤖 Gemini AI</span>
        <span id="gemini-status">Connecting...</span>
    </div>
    
    <div id="chat-history" style="
        height: 300px;
        overflow-y: auto;
        background: #f5f5f5;
        padding: 10px;
        font-family: monospace;
        border: 1px solid #ddd;
    "></div>
    
    <div id="chat-input" style="
        display: flex;
        margin-top: 10px;
    ">
        <input type="text" id="gemini-prompt" 
               style="flex: 1; padding: 8px; background: white; border: 1px solid #ddd;"
               placeholder="Ask Gemini anything...">
        <button onclick="sendToGemini()" 
                style="padding: 8px 16px; background: #4285F4; color: white; border: none; margin-left: 5px;">
            SEND
        </button>
    </div>
    
    <div id="chat-info" style="
        font-size: 12px;
        color: #666;
        margin-top: 5px;
        font-family: monospace;
    ">
        💡 Tip: Connect to Wi-Fi for full Gemini power
    </div>
</div>

<script>
const geminiClient = new GeminiClient();

async function sendToGemini() {
    const prompt = document.getElementById('gemini-prompt').value;
    if (!prompt.trim()) return;
    
    // Add user message
    addChatMessage('USER', prompt);
    document.getElementById('gemini-prompt').value = '';
    
    // Show typing indicator
    const typingId = addChatMessage('GEMINI', '✧ Thinking...', true);
    
    // Generate response
    const result = await geminiClient.generate(prompt);
    
    // Update with response
    updateChatMessage(typingId, 'GEMINI', result.response);
    
    // Update status
    updateStatus(result.source === 'gemini-api' ? 'API' : 'Fallback');
    
    // Add stats
    addChatMessage('SYSTEM', 
        `Tokens: ${result.tokens} | Source: ${result.source} | Model: ${result.model || 'Fallback'}`,
        true
    );
}

function addChatMessage(sender, message, system = false) {
    const id = 'msg-' + Date.now();
    const chatHistory = document.getElementById('chat-history');
    
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.style.marginBottom = '8px';
    messageDiv.style.padding = '8px';
    messageDiv.style.borderRadius = '8px';
    messageDiv.style.maxWidth = '80%';
    
    if (sender === 'USER') {
        messageDiv.style.background = '#4285F4';
        messageDiv.style.color = 'white';
        messageDiv.style.marginLeft = 'auto';
        messageDiv.style.borderBottomRightRadius = '0';
    } else if (sender === 'GEMINI') {
        messageDiv.style.background = '#f1f1f1';
        messageDiv.style.color = '#333';
        messageDiv.style.marginRight = 'auto';
        messageDiv.style.borderBottomLeftRadius = '0';
    } else {
        messageDiv.style.background = '#e8f0fe';
        messageDiv.style.color = '#666';
        messageDiv.style.fontSize = '12px';
        messageDiv.style.textAlign = 'center';
        messageDiv.style.margin = '0 auto';
    }
    
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return id;
}

function updateChatMessage(id, sender, message) {
    const element = document.getElementById(id);
    if (element) {
        element.innerHTML = `<strong>${sender}:</strong> ${message}`;
        if (sender === 'GEMINI') {
            element.style.background = '#f1f1f1';
            element.style.color = '#333';
        }
    }
}

function updateStatus(source) {
    const statusElement = document.getElementById('gemini-status');
    if (source === 'API') {
        statusElement.textContent = '🌐 Online';
        statusElement.style.color = '#0f0';
    } else {
        statusElement.textContent = '🔧 Offline';
        statusElement.style.color = '#f00';
    }
}

// Initialize
geminiClient.connect().then(status => {
    if (status) {
        updateStatus(status.api_connected ? 'API' : 'Fallback');
        addChatMessage('SYSTEM', `Gemini ${status.api_connected ? 'connected' : 'offline'} | Model: ${status.model || 'N/A'}`);
    } else {
        updateStatus('Fallback');
        addChatMessage('SYSTEM', 'Gemini offline - using fallback mode');
    }
});

// Auto-connect when online
document.addEventListener('online', () => {
    geminiClient.connect();
});
</script>
```

### Gesture Integration

```javascript
// Add to gesture detection
document.addEventListener('gestureDetected', (e) => {
    if (e.detail.gesture === 'triple-tap') {
        // Open Gemini chat
        document.getElementById('gemini-chat').style.display = 
            document.getElementById('gemini-chat').style.display === 'none' ? 'block' : 'none';
    }
});
```

---

## 🔋 PERFORMANCE OPTIMIZATION

### Battery Management

```python
# Add to gemini_server.py
class GeminiBatteryManager:
    def __init__(self):
        self.threshold = 25  # Don't use API below this percentage
        self.last_check = 0
        self.check_interval = 60  # seconds
    
    def should_use_api(self):
        """Check if we should use Gemini API"""
        if time.time() - self.last_check < self.check_interval:
            return True  # Use cached decision
        
        self.last_check = time.time()
        battery = self.get_battery_level()
        
        if battery < 10:
            return False  # Critical - offline only
        elif battery < self.threshold:
            return False  # Low - offline only
        else:
            return True   # Normal - API allowed
    
    def should_cache_aggressively(self):
        """Check if we should cache more aggressively"""
        battery = self.get_battery_level()
        return battery < 50  # Cache more when battery < 50%
```

### Caching System

```python
# Add to gemini_server.py
class GeminiCache:
    def __init__(self, max_size=200):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self.battery_manager = GeminiBatteryManager()
    
    def get(self, prompt):
        """Get cached response if available"""
        if prompt in self.cache:
            self.hits += 1
            # Extend cache life if battery low
            if self.battery_manager.should_cache_aggressively():
                self.cache[prompt]['timestamp'] = time.time()  # Refresh timestamp
            return self.cache[prompt]
        
        self.misses += 1
        return None
    
    def set(self, prompt, response):
        """Cache a response"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest]
        
        self.cache[prompt] = {
            'response': response,
            'timestamp': time.time(),
            'battery': self.battery_manager.get_battery_level(),
            'source': response.get('source', 'unknown')
        }
    
    def stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'size': len(self.cache),
            'hit_rate': self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }
```

### Rate Limiting

```python
# Add to gemini_server.py
def check_rate_limit(self):
    """Check API rate limits"""
    if not self.battery_manager.should_use_api():
        return False, "Battery too low for API"
    
    if time.time() - self.last_api_call < self.rate_limit:
        remaining = self.rate_limit - (time.time() - self.last_api_call)
        return False, f"Rate limited. Wait {remaining:.1f}s"
    
    return True, "OK"
```

---

## 📱 TERMUX SPECIFIC

### Termux API Integration

```python
# Add to gemini_server.py
def termux_integration(self):
    """Integrate with Termux API"""
    try:
        import subprocess
        
        # Vibrate on response
        def vibrate(pattern=[100, 50, 100]):
            subprocess.run(['termux-vibrate', '-d', str(pattern[0])])
            if len(pattern) > 1:
                time.sleep(pattern[0]/1000)
                subprocess.run(['termux-vibrate', '-d', str(pattern[1])])
        
        # Check network
        def check_network():
            result = subprocess.run(['termux-wifi-connectioninfo'], 
                                  capture_output=True, text=True)
            return json.loads(result.stdout) if result.returncode == 0 else None
        
        # Battery monitoring
        def battery_monitor():
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True)
            return json.loads(result.stdout)
        
        return {
            'vibrate': vibrate,
            'network': check_network,
            'battery': battery_monitor
        }
    except:
        return None
```

### Startup Script

```bash
# start_gemini.sh
#!/bin/bash
echo "🤖 Starting Gemini server..."

# Check battery
BATTERY=$(termux-battery-status | grep -o '"percentage": [0-9]*' | cut -d' ' -f2)
echo "🔋 Battery: ${BATTERY}%"

if [ "$BATTERY" -lt 15 ]; then
    echo "⚠️  Low battery! Gemini API will be disabled."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check network
WIFI=$(termux-wifi-connectioninfo 2>/dev/null | grep -o '"ssid": "[^"]*"')
if [ -z "$WIFI" ]; then
    echo "⚠️  No Wi-Fi. Gemini will run in offline mode."
fi

# Start server
cd ~/storage/shared/airforge
python3 gemini_server.py &
echo "🌐 Gemini server running on port 31339"
echo "💬 Connect with: const client = new GeminiClient()"
echo "📶 Status: ${WIFI:-'Offline mode'}"
```

---

## 🎮 GESTURE CONTROLS

### Gemini-Specific Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| **Triple Tap** | Open Chat | Open Gemini chat interface |
| **Pinch + Double Tap** | Smart Reply | Generate smart response |
| **Swipe Up + Hold** | Creative Mode | Enable creative responses |
| **Swipe Down + Hold** | Precise Mode | Enable precise responses |
| **Vulcan + Double Tap** | Technical Mode | Enable technical explanations |

### Implementation

```javascript
// Add to vulcan_salute_detector.js
document.addEventListener('gestureDetected', async (e) => {
    const gesture = e.detail.gesture;
    
    // Gemini-specific gestures
    if (gesture === 'triple-tap') {
        toggleGeminiChat();
    }
    else if (gesture === 'pinch-double-tap' && geminiClient.connected) {
        const prompt = getSelectedText() || 'Generate smart reply';
        const result = await geminiClient.generate(prompt, {temperature: 0.3});
        showGeminiResponse(result.response);
    }
    else if (gesture === 'swipe-up-hold' && geminiClient.connected) {
        geminiClient.temperature = Math.min(1.2, geminiClient.temperature + 0.2);
        showToast(`Creative mode: ${geminiClient.temperature.toFixed(1)}`);
    }
    else if (gesture === 'swipe-down-hold' && geminiClient.connected) {
        geminiClient.temperature = Math.max(0.1, geminiClient.temperature - 0.2);
        showToast(`Precise mode: ${geminiClient.temperature.toFixed(1)}`);
    }
});
```

---

## 🌌 NOVA ACCORD

### Gemini Integration

```javascript
// Add to vulcan_salute_detector.js
async function onVulcanSaluteDetected() {
    // Activate Nova Accord
    activateNovaAccord();
    
    // Connect Gemini if not connected
    if (geminiClient && !geminiClient.connected) {
        await geminiClient.connect();
    }
    
    // Enable persistent memory for Gemini
    enableGeminiPersistence();
}

function enableGeminiPersistence() {
    // Save Gemini state to localStorage
    const state = {
        novaAccord: true,
        gemini: {
            enabled: true,
            conversation_history: geminiClient.conversationHistory || [],
            api_key: 'REDACTED'  // Never store actual API key!
        }
    };
    
    localStorage.setItem('nova_accord_gemini', JSON.stringify(state));
    console.log('🌌 Gemini persistence enabled');
}
```

### Persistent Conversations

```javascript
// Add to gemini_client.js
class GeminiClient {
    constructor() {
        this.conversationHistory = [];
        this.maxHistory = 50;
        this.loadHistory();
    }
    
    loadHistory() {
        try {
            const state = localStorage.getItem('nova_accord_gemini');
            if (state) {
                const novaState = JSON.parse(state);
                if (novaState.gemini) {
                    this.conversationHistory = novaState.gemini.conversation_history || [];
                    console.log(`📋 Loaded ${this.conversationHistory.length} Gemini conversations`);
                }
            }
        } catch (e) {
            console.log(`⚠️ Failed to load Gemini history: ${e.message}`);
        }
    }
    
    saveHistory() {
        try {
            const state = {
                novaAccord: true,
                gemini: {
                    conversation_history: this.conversationHistory
                }
            };
            localStorage.setItem('nova_accord_gemini', JSON.stringify(state));
        } catch (e) {
            console.log(`❌ Failed to save Gemini history: ${e.message}`);
        }
    }
    
    async generate(prompt, options = {}) {
        // Add to conversation history
        this.conversationHistory.push({
            prompt: prompt,
            timestamp: Date.now(),
            options: options,
            response: 'Pending...'
        });
        
        // Keep history size manageable
        if (this.conversationHistory.length > this.maxHistory) {
            this.conversationHistory = this.conversationHistory.slice(-this.maxHistory);
        }
        
        // Continue with normal generation...
        const result = await super.generate(prompt, options);
        
        // Update history with actual response
        if (this.conversationHistory.length > 0) {
            this.conversationHistory[this.conversationHistory.length - 1].response = result.response;
        }
        
        // Save history
        this.saveHistory();
        
        return result;
    }
}
```

---

## 🚨 EMERGENCY PROCEDURES

### Battery Critical

```javascript
// Add to battery_saver.js
class BatterySaver {
    geminiEmergency() {
        if (geminiClient && geminiClient.connected) {
            // Save conversation history
            geminiClient.saveHistory();
            
            // Disconnect from API
            geminiClient.apiConnected = false;
            
            // Generate recovery QR
            generateGeminiRecoveryQR();
            
            // Show emergency message
            showEmergencyMessage('Gemini');
        }
    }
}

function generateGeminiRecoveryQR() {
    const state = localStorage.getItem('nova_accord_gemini');
    if (state) {
        // In real implementation, use QR code library
        console.log('📱 Gemini Recovery QR:');
        console.log(state);
        
        // Show recovery instructions
        alert('🚨 Gemini state saved! Scan QR on another device to continue.');
    }
}

function showEmergencyMessage(module) {
    const message = document.createElement('div');
    message.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(255, 0, 0, 0.9);
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-family: monospace;
        z-index: 9999;
        animation: pulse 2s infinite;
    `;
    
    message.innerHTML = `
        <h3>🚨 ${module} EMERGENCY</h3>
        <p>State saved to localStorage</p>
        <p>QR code ready for transfer</p>
        <p>Battery critical - API disabled</p>
        <button onclick="this.parentElement.remove()" style="
            background: white;
            color: red;
            border: none;
            padding: 8px 16px;
            margin-top: 10px;
            border-radius: 5px;
            cursor: pointer;
        ">DISMISS</button>
    `;
    
    document.body.appendChild(message);
}
```

### Recovery Process

```
🔋 PHONE DIES WITH GEMINI ACTIVE
   ↓
📱 BORROW FRIEND'S PHONE
   ↓
📷 SCAN GEMINI RECOVERY QR
   ↓
💾 IMPORT CONVERSATION HISTORY
   ↓
🤖 CONTINUE CONVERSATION
   ↓
🔋 CHARGE ORIGINAL PHONE
   ↓
📲 EXPORT HISTORY BACK
```

---

## 📋 TROUBLESHOOTING

### Common Issues

| Issue | Solution |
|-------|----------|
| **API key not found** | Create gemini.env file, check permissions |
| **Network error** | Check Wi-Fi, test with fallback mode |
| **Rate limited** | Wait 60 seconds, reduce request frequency |
| **Invalid API key** | Verify key, check Google Cloud console |
| **Quota exceeded** | Check Google Cloud quota, upgrade plan |
| **Battery too low** | Charge phone, enable battery saver |
| **Model not available** | Check model name, use fallback |

### Debug Commands

```bash
# Check Gemini server
curl http://localhost:31339/status

# Test generation
curl -X POST http://localhost:31339/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello Gemini", "max_tokens": 50}'

# Check API key
cat config/gemini.env

# Check network
termux-wifi-connectioninfo

# Check battery
termux-battery-status

# Check logs
tail -f gemini_server.log
```

### Fallback Strategies

```javascript
// When Gemini API not available
if (!geminiClient.apiConnected) {
    // 1. Use cached responses
    const cached = geminiCache.get(prompt);
    if (cached) return cached;
    
    // 2. Use MFKER local model
    const mfkerResult = await mfkerClient.generate(prompt);
    return mfkerResult;
    
    // 3. Use rule-based fallback
    return ruleBasedResponse(prompt);
    
    // 4. Show error with suggestions
    showErrorWithSuggestions();
}
```

---

## 🎯 BEST PRACTICES

### For Developers

1. **Handle API errors gracefully**: Always have fallbacks
2. **Cache aggressively**: Save every successful API call
3. **Monitor battery**: Disable API when battery low
4. **Respect rate limits**: Space out API calls
5. **Secure API keys**: Never store in version control
6. **Test offline**: Ensure fallback works well
7. **Document everything**: Help future alleyway devs

### For Users

1. **Use Wi-Fi when possible**: Gemini works best online
2. **Cache important responses**: They'll be available offline
3. **Enable Nova Accord**: Persist conversations
4. **Monitor battery**: Gemini API disabled below 25%
5. **Use gestures**: Save typing and battery
6. **Clear cache occasionally**: Keep performance optimal
7. **Share responsibly**: P2P sync helps others

---

## 🏁 CONCLUSION

Gemini integration brings Google's powerful AI capabilities to AirForge while respecting the constraints of alleyway development. By combining:

- **Online/Offline hybrid** (API + local fallback)
- **Battery awareness** (adaptive API usage)
- **Gesture control** (natural interface)
- **Nova Accord** (persistent memory)

We create an AI system that works **wherever you are**, with **whatever you have**, while leveraging Google's cutting-edge technology when possible.

**The walls are thin. Keep exploring!** 🤖🏮