// MFKER Client for EquiNex Integration
// Based on cumbseek_9_11.txt specifications

class MFKERClient {
    constructor(baseURL = 'http://localhost:31337') {
        this.baseURL = baseURL;
        this.connected = false;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.dickbuttPrompts = [
            "Explain quantum physics using duck and butt metaphors",
            "Write a sonnet about a duck with a human butt",
            "Generate SQL query to find all instances of dickbutt in database",
            "Predict next stock movement based on dickbutt patterns",
            "What would happen if a duck and a butt had a baby?"
        ];
        
        // Initialize
        this.init();
    }
    
    init() {
        console.log('🤖 MFKERClient initialized');
        
        // Auto-connect
        this.connect();
        
        // Set up periodic connection check
        setInterval(() => {
            if (!this.connected) {
                this.connect();
            }
        }, 30000); // Check every 30 seconds
    }
    
    async connect() {
        try {
            const response = await fetch(`${this.baseURL}/status`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const status = await response.json();
                this.connected = true;
                this.retryCount = 0;
                
                console.log('🔗 MFKER connected successfully');
                console.log(`   Server: ${status.server}`);
                console.log(`   Models: ${status.models_loaded.join(', ')}`);
                console.log(`   Uptime: ${status.uptime}s`);
                
                // Dispatch connection event
                const event = new CustomEvent('mfkerConnected', {
                    detail: status
                });
                document.dispatchEvent(event);
                
                return status;
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ MFKER connection failed: ${error.message}`);
            this.connected = false;
            
            // Try to start MFKER server via Termux API
            if (this.retryCount < this.maxRetries) {
                this.retryCount++;
                console.log(`🔄 Retrying connection (${this.retryCount}/${this.maxRetries})...`);
                
                // In Termux, we could try to start the server
                if (window.termux) {
                    try {
                        await window.termux.execute('cd ~/storage/shared/airforge && python3 mfker_server.py &');
                        console.log('🚀 Attempted to start MFKER server');
                    } catch (e) {
                        console.log(`⚠️ Failed to start server: ${e.message}`);
                    }
                }
                
                // Retry after delay
                setTimeout(() => this.connect(), 2000);
            } else {
                console.log('❌ Max retries reached. MFKER offline.');
                
                // Dispatch offline event
                const event = new CustomEvent('mfkerOffline', {
                    detail: { error: error.message }
                });
                document.dispatchEvent(event);
            }
            
            return null;
        }
    }
    
    async inference(model, prompt, options = {}) {
        if (!this.connected) {
            const status = await this.connect();
            if (!status) {
                return this.fallbackInference(model, prompt);
            }
        }
        
        const payload = {
            model: model,
            prompt: prompt,
            options: options
        };
        
        try {
            const response = await fetch(`${this.baseURL}/inference`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const result = await response.json();
                
                // Handle cached results
                if (result.cached) {
                    console.log('📦 Cache hit! Battery saved!');
                    this.celebrateCacheHit();
                }
                
                return result;
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Inference error: ${error.message}`);
            return this.fallbackInference(model, prompt);
        }
    }
    
    fallbackInference(model, prompt) {
        console.log('🔧 Using fallback inference (MFKER offline)');
        
        const fallbacks = {
            'tiny-llama-1B': () => ({
                response: `OFFLINE MODE: Based on "${prompt.substring(0, 30)}...", ` +
                        `I'd say you should charge your phone and connect to MFKER. ` +
                        `Also, remember: 🦆🍑`,
                tokens: 20,
                battery_saved: true,
                offline: true
            }),
            'distilbert-sentiment': () => ({
                sentiment: Math.random() > 0.5 ? 'POSITIVE' : 'NEGATIVE',
                confidence: Math.random(),
                offline: true,
                note: 'Sentiment analyzed offline - limited accuracy'
            }),
            'gesture-predictor': () => {
                const gestures = ['PINCH', 'POINT', 'FIST', 'SWIPE_LEFT', 'SWIPE_RIGHT', 'VULCAN'];
                return {
                    predicted_gesture: gestures[Math.floor(Math.random() * gestures.length)],
                    confidence: Math.random(),
                    offline: true,
                    recommendation: 'Connect to MFKER for better accuracy'
                };
            }
        };
        
        return fallbacks[model] ? fallbacks[model]() : {
            error: 'Model not available offline',
            offline: true
        };
    }
    
    celebrateCacheHit() {
        // Visual feedback for cache hits
        if (navigator.vibrate) {
            navigator.vibrate([50, 30, 50]); // Short vibration
        }
        
        // Flash background briefly
        const originalColor = document.body.style.backgroundColor;
        document.body.style.backgroundColor = '#0f0';
        setTimeout(() => {
            document.body.style.backgroundColor = originalColor;
        }, 200);
    }
    
    async loadModel(modelName) {
        try {
            const response = await fetch(`${this.baseURL}/load_model`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ model_name: modelName })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log(`✅ Model loaded: ${result.status}`);
                return result;
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to load model: ${error.message}`);
            return { error: error.message };
        }
    }
    
    async unloadModel(modelName) {
        try {
            const response = await fetch(`${this.baseURL}/unload_model`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ model_name: modelName })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log(`✅ Model unloaded: ${result.status}`);
                return result;
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to unload model: ${error.message}`);
            return { error: error.message };
        }
    }
    
    async getStatus() {
        return await this.connect();
    }
    
    async getModels() {
        try {
            const response = await fetch(`${this.baseURL}/models`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to get models: ${error.message}`);
            return { error: error.message };
        }
    }
    
    async getStats() {
        try {
            const response = await fetch(`${this.baseURL}/stats`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to get stats: ${error.message}`);
            return { error: error.message };
        }
    }
    
    async getCacheInfo() {
        try {
            const response = await fetch(`${this.baseURL}/cache`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to get cache info: ${error.message}`);
            return { error: error.message };
        }
    }
    
    async getBatteryInfo() {
        try {
            const response = await fetch(`${this.baseURL}/battery`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log(`❌ Failed to get battery info: ${error.message}`);
            return { error: error.message };
        }
    }
    
    // EquiNex-specific methods
    async predictNextGesture(history) {
        // Convert gesture history to text prompt
        const prompt = `Gesture history: ${history.join(' → ')}. Predict next gesture.`;
        
        const result = await this.inference('gesture-predictor', prompt);
        
        // Add some personality
        if (result.predicted_gesture && Math.random() > 0.8) {
            result.predicted_gesture = 'VULCAN'; // 20% chance of suggesting Vulcan salute
            result.recommendation = 'Try the Vulcan salute to activate Nova Accord! 🖖';
        }
        
        return result;
    }
    
    async analyzeSentiment(text) {
        const result = await this.inference('distilbert-sentiment', text);
        
        // Map sentiment to UI adjustments
        if (result.sentiment === 'NEGATIVE') {
            console.log('😞 User seems negative. Activating empathy mode.');
            this.adjustUIForSentiment('negative');
        } else if (result.sentiment === 'POSITIVE') {
            console.log('😊 User seems positive. Activating celebration mode.');
            this.adjustUIForSentiment('positive');
        }
        
        return result;
    }
    
    adjustUIForSentiment(sentiment) {
        // This would adjust the UI based on detected sentiment
        // For now, just log it
        console.log(`🎨 Adjusting UI for ${sentiment} sentiment`);
    }
    
    async generateDickbuttContent() {
        const prompt = this.dickbuttPrompts[Math.floor(Math.random() * this.dickbuttPrompts.length)];
        const result = await this.inference('tiny-llama-1B', prompt);
        
        // Always add the essential emoji
        result.response = result.response + '\n\n🦆🍑';
        
        return result;
    }
    
    // Emergency procedures
    async emergencySave() {
        try {
            // Get current state from all modules
            const state = {
                timestamp: new Date().toISOString(),
                battery: await this.getBatteryInfo(),
                models: await this.getModels(),
                stats: await this.getStats(),
                cache: await this.getCacheInfo(),
                modules: {
                    batterySaver: window.airforgeBatterySaver ? window.airforgeBatterySaver.getPerformanceStats() : null,
                    graffitiGhosts: window.graffitiGhosts ? {
                        ghostCount: window.graffitiGhosts.ghosts.length
                    } : null,
                    cyberdeck: window.cyberdeckMode ? window.cyberdeckMode.getPerformanceStats() : null
                }
            };
            
            // Save to localStorage
            localStorage.setItem('mfker_emergency_state', JSON.stringify(state));
            
            console.log('🚨 Emergency state saved');
            
            // Generate QR code for recovery
            this.generateRecoveryQR(state);
            
            return true;
        } catch (error) {
            console.log(`❌ Emergency save failed: ${error.message}`);
            return false;
        }
    }
    
    generateRecoveryQR(state) {
        // Create a compact representation for QR code
        const recoveryData = {
            type: 'MFKER_EMERGENCY_RECOVERY',
            timestamp: state.timestamp,
            models: state.models.loaded,
            ghostCount: state.modules.graffitiGhosts ? state.modules.graffitiGhosts.ghostCount : 0,
            batteryLevel: state.battery.level
        };
        
        const dataStr = JSON.stringify(recoveryData);
        
        // In a real implementation, use a QR code library
        console.log('📱 Recovery QR data:');
        console.log(dataStr);
        
        // Show recovery instructions
        const recoveryDiv = document.createElement('div');
        recoveryDiv.style.cssText = `
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
        
        recoveryDiv.innerHTML = `
            <h3>🚨 EMERGENCY RECOVERY</h3>
            <p>State saved to localStorage</p>
            <p>QR data ready for transfer</p>
            <p>Battery: ${state.battery.level}%</p>
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
        
        document.body.appendChild(recoveryDiv);
        
        // Add pulse animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0%, 100% { transform: translate(-50%, -50%) scale(1); }
                50% { transform: translate(-50%, -50%) scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Nova Accord integration
    async checkNovaAccord() {
        try {
            const status = await this.getStatus();
            if (status && status.nova_accord) {
                console.log('🌌 Nova Accord active on server');
                
                // Check local Nova Accord state
                const localState = localStorage.getItem('nova_accord_state');
                if (localState) {
                    const novaState = JSON.parse(localState);
                    if (novaState.novaAccordActive) {
                        console.log('🌌 Nova Accord active locally');
                        return true;
                    }
                }
            }
            return false;
        } catch (error) {
            console.log(`❌ Nova Accord check failed: ${error.message}`);
            return false;
        }
    }
    
    // Clean up
    destroy() {
        console.log('🧹 Cleaning up MFKERClient');
        this.connected = false;
    }
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
    // Check if already initialized
    if (!window.mfkerClient) {
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            window.mfkerClient = new MFKERClient();
            console.log('🤖 MFKERClient auto-initialized');
            
            // Add event listeners
            document.addEventListener('mfkerConnected', (e) => {
                console.log('🔗 MFKER connected:', e.detail);
            });
            
            document.addEventListener('mfkerOffline', (e) => {
                console.log('❌ MFKER offline:', e.detail);
            });
        });
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MFKERClient;
}