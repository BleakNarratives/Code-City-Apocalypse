# 🤖 MISTRAL TASK INTEGRATION

**AirForge v2.0 - Mistral AI Integration Guide**

*Running large language models on a Motorola phone in an alleyway*

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

Mistral AI integration for AirForge provides offline-capable large language model functionality optimized for resource-constrained environments (i.e., homeless development on a Motorola phone).

### Key Features

- **Offline Inference**: Run models without internet
- **Battery-Aware**: Adaptive computation based on power
- **Memory Efficient**: Quantized models and caching
- **Gesture Controlled**: Full hand gesture interface
- **P2P Sync**: Share model outputs with nearby devices

### Architecture

```
User Gestures → MediaPipe → Mistral Model → Response → AR Display
                         ▲               ↓
                    Battery Monitor ← Cache System
```

---

## 📦 SETUP

### Prerequisites

```bash
# In Termux
pkg install python pip
pip install transformers torch sentencepiece
pip install mistralai  # When available
```

### Model Download

```bash
# Download quantized model
mkdir -p ~/storage/shared/airforge/models/mistral
cd ~/storage/shared/airforge/models/mistral

# Download from Hugging Face (when online)
# git lfs install
# git clone https://huggingface.co/mistralai/Mistral-7B-v0.1

# For offline use, download these files:
wget https://example.com/mistral-7b-gguf-q4_0.bin -O mistral-7b-q4_0.gguf
wget https://example.com/tokenizer.json
wget https://example.com/special_tokens_map.json
```

### Configuration

```json
// config.json
{
    "mistral": {
        "model_path": "models/mistral/mistral-7b-q4_0.gguf",
        "tokenizer_path": "models/mistral/tokenizer.json",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "battery_threshold": 20,
        "cache_size": 100,
        "offline_mode": true
    }
}
```

---

## 🤖 MODEL INTEGRATION

### Python Backend

```python
# mistral_server.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import os

class MistralEngine:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            config = json.load(f)
            self.config = config["mistral"]
        
        self.model = None
        self.tokenizer = None
        self.device = "cpu"  # No GPU on mobile
        self.loaded = False
    
    def load_model(self):
        """Load quantized model"""
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config["tokenizer_path"]
            )
            
            # Load quantized model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config["model_path"],
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True  # 8-bit quantization
            )
            
            self.loaded = True
            print("🤖 Mistral model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def generate(self, prompt, max_tokens=None):
        """Generate text from prompt"""
        if not self.loaded:
            if not self.load_model():
                return {"error": "Model failed to load"}
        
        # Check battery
        battery = self.get_battery_level()
        if battery < self.config["battery_threshold"]:
            max_tokens = min(max_tokens or self.config["max_tokens"], 128)
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generate with sampling
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens or self.config["max_tokens"],
                temperature=self.config["temperature"],
                top_p=self.config["top_p"],
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "prompt": prompt,
            "response": response,
            "tokens": len(outputs[0]),
            "battery": battery,
            "model": "mistral-7b"
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
// mistral_client.js
class MistralClient {
    constructor(baseURL = 'http://localhost:31338') {
        this.baseURL = baseURL;
        this.connected = false;
        this.modelLoaded = false;
    }
    
    async connect() {
        try {
            const response = await fetch(`${this.baseURL}/status`);
            const status = await response.json();
            this.connected = true;
            this.modelLoaded = status.model_loaded;
            return status;
        } catch (error) {
            console.log(`❌ Mistral connection failed: ${error.message}`);
            this.connected = false;
            return null;
        }
    }
    
    async generate(prompt, options = {}) {
        if (!this.connected) {
            await this.connect();
        }
        
        const payload = {
            prompt: prompt,
            max_tokens: options.max_tokens || 256,
            temperature: options.temperature || 0.7
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
        // Simple fallback when Mistral not available
        const responses = [
            `Based on "${prompt}", I'd suggest charging your phone and trying again. The walls are thin...`,
            `Offline mode: ${prompt} → Remember to use the Vulcan salute for Nova Accord! 🖖`,
            `Battery conservation mode: Short response to save power. ${prompt.substring(0, 50)}...`
        ];
        
        return {
            response: responses[Math.floor(Math.random() * responses.length)],
            offline: true,
            tokens: 10
        };
    }
}
```

---

## 💬 CHAT INTERFACE

### HTML Interface

```html
<div id="mistral-chat">
    <div id="chat-history" style="
        height: 300px;
        overflow-y: auto;
        background: #0a0a0a;
        color: #0f0;
        padding: 10px;
        font-family: monospace;
        border: 1px solid #0f0;
        border-radius: 5px;
    "></div>
    
    <div id="chat-input" style="
        display: flex;
        margin-top: 10px;
    ">
        <input type="text" id="mistral-prompt" 
               style="flex: 1; padding: 8px; background: #111; color: #0f0; border: 1px solid #0f0;"
               placeholder="Ask Mistral anything...">
        <button onclick="sendToMistral()" 
                style="padding: 8px 16px; background: #0f0; color: #000; border: none; margin-left: 5px;">
            SEND
        </button>
    </div>
</div>

<script>
const mistralClient = new MistralClient();

async function sendToMistral() {
    const prompt = document.getElementById('mistral-prompt').value;
    if (!prompt.trim()) return;
    
    // Add user message
    addChatMessage('USER', prompt);
    document.getElementById('mistral-prompt').value = '';
    
    // Show typing indicator
    const typingId = addChatMessage('MISTRAL', '✧ Thinking...', true);
    
    // Generate response
    const result = await mistralClient.generate(prompt);
    
    // Update with response
    updateChatMessage(typingId, 'MISTRAL', result.response);
    
    // Add stats
    addChatMessage('SYSTEM', 
        `Tokens: ${result.tokens} | Battery: ${result.battery || 'N/A'}% | Model: ${result.model || 'Fallback'}`,
        true
    );
}

function addChatMessage(sender, message, system = false) {
    const id = 'msg-' + Date.now();
    const chatHistory = document.getElementById('chat-history');
    
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.style.marginBottom = '8px';
    messageDiv.style.padding = '6px';
    messageDiv.style.borderRadius = '4px';
    
    if (sender === 'USER') {
        messageDiv.style.background = 'rgba(0, 255, 0, 0.2)';
        messageDiv.style.borderLeft = '3px solid #0f0';
    } else if (sender === 'MISTRAL') {
        messageDiv.style.background = 'rgba(0, 0, 255, 0.2)';
        messageDiv.style.borderLeft = '3px solid #00f';
    } else {
        messageDiv.style.background = 'rgba(255, 255, 0, 0.1)';
        messageDiv.style.borderLeft = '3px solid #ff0';
        messageDiv.style.fontSize = '12px';
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
        if (sender === 'MISTRAL') {
            element.style.background = 'rgba(0, 0, 255, 0.2)';
            element.style.borderLeft = '3px solid #00f';
        }
    }
}

// Initialize
mistralClient.connect().then(status => {
    if (status) {
        addChatMessage('SYSTEM', `Mistral connected! Model: ${status.model || 'N/A'} | Battery: ${status.battery || 'N/A'}%`);
    } else {
        addChatMessage('SYSTEM', 'Mistral offline - using fallback mode');
    }
});
</script>
```

### Gesture Integration

```javascript
// Add to gesture detection
document.addEventListener('gestureDetected', (e) => {
    if (e.detail.gesture === 'double-tap') {
        // Open Mistral chat
        document.getElementById('mistral-chat').style.display = 
            document.getElementById('mistral-chat').style.display === 'none' ? 'block' : 'none';
    }
});
```

---

## 🔋 PERFORMANCE OPTIMIZATION

### Battery Management

```python
# In mistral_server.py
class BatteryMonitor:
    def __init__(self, threshold=20):
        self.threshold = threshold
        self.last_check = 0
        self.check_interval = 30  # seconds
    
    def should_reduce_quality(self):
        """Check if we should reduce model quality"""
        if time.time() - self.last_check < self.check_interval:
            return False
        
        self.last_check = time.time()
        battery = self.get_battery_level()
        
        if battery < 10:
            return 'critical'  # Max 64 tokens
        elif battery < self.threshold:
            return 'low'  # Max 128 tokens
        else:
            return 'normal'  # Full quality
    
    def adjust_parameters(self, battery_status):
        """Adjust model parameters based on battery"""
        if battery_status == 'critical':
            return {
                'max_tokens': 64,
                'temperature': 0.5,
                'top_p': 0.8
            }
        elif battery_status == 'low':
            return {
                'max_tokens': 128,
                'temperature': 0.6,
                'top_p': 0.85
            }
        else:
            return {
                'max_tokens': 256,
                'temperature': 0.7,
                'top_p': 0.9
            }
```

### Caching System

```python
# Add to mistral_server.py
class MistralCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, prompt):
        """Get cached response if available"""
        if prompt in self.cache:
            self.hits += 1
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
            'battery': self.get_battery_level()
        }
    
    def stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'size': len(self.cache),
            'hit_rate': self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }
```

### Memory Management

```python
# Add to mistral_server.py
def unload_model(self):
    """Unload model to free memory"""
    if self.model:
        del self.model
        self.model = None
        self.loaded = False
        
        # Force garbage collection
        import gc
        gc.collect()
        
        print("🗑️  Model unloaded to free memory")
        return True
    return False

def auto_unload(self):
    """Automatically unload when not in use"""
    if self.loaded and time.time() - self.last_use > 300:  # 5 minutes
        return self.unload_model()
    return False
```

---

## 📱 TERMUX SPECIFIC

### Termux API Integration

```python
# Add to mistral_server.py
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
        
        # Battery monitoring
        def battery_monitor():
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True)
            return json.loads(result.stdout)
        
        return {
            'vibrate': vibrate,
            'battery': battery_monitor
        }
    except:
        return None
```

### Startup Script

```bash
# start_mistral.sh
#!/bin/bash
echo "🤖 Starting Mistral server..."

# Check battery
BATTERY=$(termux-battery-status | grep -o '"percentage": [0-9]*' | cut -d' ' -f2)
echo "🔋 Battery: ${BATTERY}%"

if [ "$BATTERY" -lt 15 ]; then
    echo "⚠️  Low battery! Mistral may not perform well."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start server
cd ~/storage/shared/airforge
python3 mistral_server.py &
echo "🌐 Mistral server running on port 31338"
echo "💬 Connect with: const client = new MistralClient()"
```

---

## 🎮 GESTURE CONTROLS

### Mistral-Specific Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| **Double Tap** | Open Chat | Open Mistral chat interface |
| **Pinch + Hold** | Long Response | Generate longer response |
| **Swipe Up** | Increase Temp | Make responses more creative |
| **Swipe Down** | Decrease Temp | Make responses more focused |
| **Vulcan + Tap** | Technical Mode | Enable technical explanations |

### Implementation

```javascript
// Add to vulcan_salute_detector.js
document.addEventListener('gestureDetected', async (e) => {
    const gesture = e.detail.gesture;
    
    // Mistral-specific gestures
    if (gesture === 'double-tap') {
        toggleMistralChat();
    }
    else if (gesture === 'pinch-hold' && mistralClient.connected) {
        const prompt = getSelectedText() || 'Tell me a story';
        const result = await mistralClient.generate(prompt, {max_tokens: 512});
        showMistralResponse(result.response);
    }
    else if (gesture === 'swipe-up' && mistralClient.connected) {
        mistralClient.temperature = Math.min(1.0, mistralClient.temperature + 0.1);
        showToast(`Temperature: ${mistralClient.temperature.toFixed(1)}`);
    }
    else if (gesture === 'swipe-down' && mistralClient.connected) {
        mistralClient.temperature = Math.max(0.1, mistralClient.temperature - 0.1);
        showToast(`Temperature: ${mistralClient.temperature.toFixed(1)}`);
    }
});
```

---

## 🌌 NOVA ACCORD

### Mistral Integration

```javascript
// Add to vulcan_salute_detector.js
async function onVulcanSaluteDetected() {
    // Activate Nova Accord
    activateNovaAccord();
    
    // Load Mistral model if not loaded
    if (mistralClient && !mistralClient.modelLoaded) {
        await mistralClient.loadModel('mistral-7b');
    }
    
    // Enable persistent memory for Mistral
    enableMistralPersistence();
}

function enableMistralPersistence() {
    // Save Mistral state to localStorage
    const state = {
        novaAccord: true,
        mistral: {
            enabled: true,
            last_prompt: mistralClient.lastPrompt,
            conversation_history: mistralClient.history
        }
    };
    
    localStorage.setItem('nova_accord_mistral', JSON.stringify(state));
    console.log('🌌 Mistral persistence enabled');
}
```

### Persistent Conversations

```javascript
// Add to mistral_client.js
class MistralClient {
    constructor() {
        this.conversationHistory = [];
        this.maxHistory = 20;
        this.loadHistory();
    }
    
    loadHistory() {
        try {
            const state = localStorage.getItem('nova_accord_mistral');
            if (state) {
                const novaState = JSON.parse(state);
                if (novaState.mistral) {
                    this.conversationHistory = novaState.mistral.conversation_history || [];
                    console.log(`📋 Loaded ${this.conversationHistory.length} Mistral conversations`);
                }
            }
        } catch (e) {
            console.log(`⚠️ Failed to load Mistral history: ${e.message}`);
        }
    }
    
    saveHistory() {
        try {
            const state = {
                novaAccord: true,
                mistral: {
                    conversation_history: this.conversationHistory
                }
            };
            localStorage.setItem('nova_accord_mistral', JSON.stringify(state));
        } catch (e) {
            console.log(`❌ Failed to save Mistral history: ${e.message}`);
        }
    }
    
    async generate(prompt, options = {}) {
        // Add to conversation history
        this.conversationHistory.push({
            prompt: prompt,
            timestamp: Date.now(),
            options: options
        });
        
        // Keep history size manageable
        if (this.conversationHistory.length > this.maxHistory) {
            this.conversationHistory = this.conversationHistory.slice(-this.maxHistory);
        }
        
        // Save history
        this.saveHistory();
        
        // Continue with normal generation...
    }
}
```

---

## 🚨 EMERGENCY PROCEDURES

### Battery Critical

```javascript
// Add to battery_saver.js
class BatterySaver {
    mistralEmergency() {
        if (mistralClient && mistralClient.connected) {
            // Save conversation history
            mistralClient.saveHistory();
            
            // Unload model
            fetch('http://localhost:31338/unload_model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ confirm: true })
            });
            
            // Generate recovery QR
            generateMistralRecoveryQR();
        }
    }
}

function generateMistralRecoveryQR() {
    const state = localStorage.getItem('nova_accord_mistral');
    if (state) {
        // In real implementation, use QR code library
        console.log('📱 Mistral Recovery QR:');
        console.log(state);
        
        // Show recovery instructions
        alert('🚨 Mistral state saved! Scan QR on another device to continue.');
    }
}
```

### Recovery Process

```
🔋 PHONE DIES WITH MISTRAL ACTIVE
   ↓
📱 BORROW FRIEND'S PHONE
   ↓
📷 SCAN MISTRAL RECOVERY QR
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
| **Model fails to load** | Check file paths, ensure quantized model, restart Termux |
| **Out of memory** | Reduce max_tokens, unload model when not in use, close other apps |
| **Slow response** | Enable battery saver, reduce temperature, use shorter prompts |
| **Connection refused** | Start server: `python3 mistral_server.py`, check port 31338 |
| **Tokenizer error** | Verify tokenizer files, check JSON format, reinstall packages |
| **Battery drain** | Enable battery saver, reduce max_tokens, unload model frequently |

### Debug Commands

```bash
# Check Mistral server
curl http://localhost:31338/status

# Test generation
curl -X POST http://localhost:31338/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello Mistral", "max_tokens": 50}'

# Check battery
termux-battery-status

# Monitor memory
watch -n 1 free -h

# Check logs
tail -f mistral_server.log
```

### Fallback Strategies

```javascript
// When Mistral not available
if (!mistralClient.connected) {
    // 1. Use cached responses
    const cached = mistralCache.get(prompt);
    if (cached) return cached;
    
    // 2. Use smaller local model
    const localResult = await localModel.generate(prompt);
    
    // 3. Use rule-based fallback
    return ruleBasedResponse(prompt);
    
    // 4. Show error with suggestions
    showErrorWithSuggestions();
}
```

---

## 🎯 BEST PRACTICES

### For Developers

1. **Test on low battery**: Ensure graceful degradation
2. **Cache aggressively**: Save every successful response
3. **Monitor performance**: Track FPS, memory, battery
4. **Use quantization**: 8-bit models save memory
5. **Unload when idle**: Free memory after 5 minutes
6. **Fallback gracefully**: Always have a backup plan
7. **Document everything**: Help future alleyway devs

### For Users

1. **Charge when possible**: Mistral works best above 20%
2. **Use short prompts**: Save battery and get faster responses
3. **Cache important responses**: They'll be available offline
4. **Enable Nova Accord**: Persist conversations across sessions
5. **Use gestures**: Save typing and battery
6. **Clear cache occasionally**: Keep performance optimal
7. **Share responsibly**: P2P sync helps others

---

## 🏁 CONCLUSION

Mistral integration brings powerful AI capabilities to AirForge while respecting the constraints of alleyway development. By combining:

- **Offline capability** (quantized models)
- **Battery awareness** (adaptive quality)
- **Gesture control** (natural interface)
- **Nova Accord** (persistent memory)

We create an AI system that works **wherever you are**, with **whatever you have**.

**The walls are thin. Keep asking questions!** 🤖🏮