// Battery Saver Mode for AirForge
// Based on cumbseek_9_11.txt specifications

class BatterySaver {
    constructor() {
        this.battery = null;
        this.mode = 'performance'; // 'performance' | 'balanced' | 'battery'
        this.fps = 60;
        this.cameraActive = true;
        this.lastHandDetection = Date.now();
        this.handDetectionTimeout = 2000; // 2 seconds
        this.performanceStats = {
            fpsHistory: [],
            batteryHistory: [],
            lastUpdate: Date.now()
        };
        
        // Initialize
        this.init();
    }
    
    init() {
        console.log('🔋 BatterySaver initialized');
        
        // Check for Battery API
        if ('getBattery' in navigator) {
            navigator.getBattery().then(battery => {
                this.battery = battery;
                this.updateBatteryStatus();
                
                // Set up event listeners
                battery.addEventListener('levelchange', () => this.updateBatteryStatus());
                battery.addEventListener('chargingchange', () => this.updateBatteryStatus());
                
                console.log('📊 Battery API available');
            });
        } else {
            console.log('⚠️ Battery API not available, using fallback mode');
            this.battery = {
                level: 1.0,
                charging: false
            };
        }
        
        // Set up performance monitoring
        this.setupPerformanceMonitoring();
        
        // Apply initial mode
        this.applyMode();
    }
    
    updateBatteryStatus() {
        if (!this.battery) return;
        
        const level = Math.floor(this.battery.level * 100);
        const charging = this.battery.charging;
        
        console.log(`🔋 Battery: ${level}% ${charging ? '(charging)' : ''}`);
        
        // Update performance stats
        this.performanceStats.batteryHistory.push({
            level: level,
            charging: charging,
            timestamp: Date.now()
        });
        
        // Keep only last 10 readings
        if (this.performanceStats.batteryHistory.length > 10) {
            this.performanceStats.batteryHistory.shift();
        }
        
        // Adapt mode based on battery level
        this.adaptMode();
    }
    
    adaptMode() {
        if (!this.battery) return;
        
        const level = this.battery.level * 100;
        const charging = this.battery.charging;
        
        let newMode;
        
        // Determine mode based on battery level and charging status
        if (charging) {
            newMode = 'performance';
        } else if (level < 20) {
            newMode = 'battery';
        } else if (level < 50) {
            newMode = 'balanced';
        } else {
            newMode = 'performance';
        }
        
        // Only change mode if it's different
        if (newMode !== this.mode) {
            console.log(`🔄 Switching from ${this.mode} to ${newMode} mode`);
            this.mode = newMode;
            this.applyMode();
        }
    }
    
    applyMode() {
        console.log(`⚡ Applying ${this.mode} mode settings`);
        
        switch (this.mode) {
            case 'battery':
                this.fps = 10;
                this.cameraActive = false;
                this.handDetectionTimeout = 5000; // 5 seconds
                this.applyBatterySaverStyles();
                break;
                
            case 'balanced':
                this.fps = 24;
                this.cameraActive = true;
                this.handDetectionTimeout = 3000; // 3 seconds
                this.applyBalancedStyles();
                break;
                
            case 'performance':
                this.fps = 60;
                this.cameraActive = true;
                this.handDetectionTimeout = 2000; // 2 seconds
                this.applyPerformanceStyles();
                break;
        }
        
        // Update UI
        this.updateUI();
        
        // Log the change
        console.log(`📊 Mode ${this.mode}: FPS=${this.fps}, Camera=${this.cameraActive}, Timeout=${this.handDetectionTimeout}ms`);
    }
    
    applyBatterySaverStyles() {
        // Apply visual indicators for battery saver mode
        document.body.style.filter = 'grayscale(0.8) brightness(0.9)';
        document.body.style.transition = 'filter 0.3s ease';
        
        // Add battery saver indicator
        let indicator = document.getElementById('battery-saver-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'battery-saver-indicator';
            indicator.style.position = 'fixed';
            indicator.style.top = '10px';
            indicator.style.right = '10px';
            indicator.style.background = 'rgba(0, 0, 0, 0.7)';
            indicator.style.color = '#f00';
            indicator.style.padding = '5px 10px';
            indicator.style.borderRadius = '5px';
            indicator.style.fontSize = '12px';
            indicator.style.zIndex = '1000';
            indicator.style.fontFamily = 'monospace';
            document.body.appendChild(indicator);
        }
        indicator.textContent = '🔋 BATTERY SAVER';
    }
    
    applyBalancedStyles() {
        // Remove grayscale but keep slight dimming
        document.body.style.filter = 'brightness(0.95)';
        
        // Update or create indicator
        let indicator = document.getElementById('battery-saver-indicator');
        if (indicator) {
            indicator.textContent = '⚡ BALANCED';
            indicator.style.color = '#ff0';
        }
    }
    
    applyPerformanceStyles() {
        // Remove all filters
        document.body.style.filter = 'none';
        
        // Update or create indicator
        let indicator = document.getElementById('battery-saver-indicator');
        if (indicator) {
            indicator.textContent = '🚀 PERFORMANCE';
            indicator.style.color = '#0f0';
        }
    }
    
    updateUI() {
        // Update status bar if it exists
        const statusBar = document.getElementById('status-bar');
        if (statusBar) {
            const modeElement = document.getElementById('mode-status') || 
                statusBar.querySelector('span:last-child');
            
            if (modeElement) {
                modeElement.textContent = `MODE: ${this.mode.toUpperCase()}`;
            }
        }
        
        // Update console
        console.log(`📋 Current mode: ${this.mode.toUpperCase()}`);
    }
    
    setupPerformanceMonitoring() {
        // Monitor FPS
        let lastFrameTime = performance.now();
        let frameCount = 0;
        let fps = 0;
        
        const updateFPS = () => {
            const now = performance.now();
            const delta = now - lastFrameTime;
            
            frameCount++;
            
            if (delta >= 1000) {
                fps = Math.round((frameCount * 1000) / delta);
                this.performanceStats.fpsHistory.push(fps);
                
                // Keep only last 10 readings
                if (this.performanceStats.fpsHistory.length > 10) {
                    this.performanceStats.fpsHistory.shift();
                }
                
                frameCount = 0;
                lastFrameTime = now;
            }
            
            requestAnimationFrame(updateFPS);
        };
        
        updateFPS();
    }
    
    getPerformanceStats() {
        return {
            mode: this.mode,
            fps: this.fps,
            cameraActive: this.cameraActive,
            batteryLevel: this.battery ? Math.floor(this.battery.level * 100) : 'unknown',
            charging: this.battery ? this.battery.charging : false,
            fpsHistory: this.performanceStats.fpsHistory,
            batteryHistory: this.performanceStats.batteryHistory
        };
    }
    
    // Hand detection tracking
    handDetected() {
        this.lastHandDetection = Date.now();
        
        // If we're in battery mode and camera was off, turn it back on temporarily
        if (this.mode === 'battery' && !this.cameraActive) {
            console.log('👋 Hand detected, temporarily enabling camera');
            this.cameraActive = true;
            
            // Turn off camera again after timeout
            setTimeout(() => {
                if (Date.now() - this.lastHandDetection > this.handDetectionTimeout) {
                    console.log('📵 No hand activity, disabling camera');
                    this.cameraActive = false;
                }
            }, this.handDetectionTimeout);
        }
    }
    
    // Manual mode override
    setMode(mode) {
        if (['performance', 'balanced', 'battery'].includes(mode)) {
            this.mode = mode;
            this.applyMode();
        } else {
            console.log(`⚠️ Invalid mode: ${mode}`);
        }
    }
    
    // Emergency power save
    emergencyPowerSave() {
        console.log('🚨 EMERGENCY POWER SAVE ACTIVATED!');
        
        // Save current state
        this.saveState();
        
        // Switch to extreme battery mode
        this.fps = 5;
        this.cameraActive = false;
        this.handDetectionTimeout = 10000; // 10 seconds
        
        // Apply extreme visual indicators
        document.body.style.filter = 'grayscale(1) brightness(0.7)';
        
        // Show emergency indicator
        let indicator = document.getElementById('battery-saver-indicator');
        if (indicator) {
            indicator.textContent = '🚨 EMERGENCY POWER SAVE';
            indicator.style.color = '#f00';
            indicator.style.background = 'rgba(255, 0, 0, 0.3)';
        }
        
        // Vibrate SOS pattern
        if (navigator.vibrate) {
            navigator.vibrate([100, 30, 100, 30, 100, 200, 300, 30, 300, 30, 300, 200, 100, 30, 100, 30, 100]);
        }
        
        console.log('🔋 Saving every drop of battery...');
    }
    
    saveState() {
        // Save current application state to localStorage
        const state = {
            batterySaver: {
                mode: this.mode,
                fps: this.fps,
                cameraActive: this.cameraActive,
                timestamp: Date.now()
            },
            performanceStats: this.performanceStats
        };
        
        try {
            localStorage.setItem('airforge_battery_saver_state', JSON.stringify(state));
            console.log('💾 Battery saver state saved');
        } catch (error) {
            console.log(`❌ Failed to save state: ${error.message}`);
        }
    }
    
    loadState() {
        try {
            const savedState = localStorage.getItem('airforge_battery_saver_state');
            if (savedState) {
                const state = JSON.parse(savedState);
                console.log('📋 Loaded saved battery saver state');
                return state;
            }
        } catch (error) {
            console.log(`⚠️ Failed to load state: ${error.message}`);
        }
        return null;
    }
    
    // Clean up
    destroy() {
        console.log('🧹 Cleaning up BatterySaver');
        
        // Remove indicator
        const indicator = document.getElementById('battery-saver-indicator');
        if (indicator) {
            indicator.remove();
        }
        
        // Reset styles
        document.body.style.filter = 'none';
        
        // Remove event listeners if battery API was available
        if (this.battery) {
            this.battery.removeEventListener('levelchange', this.updateBatteryStatus);
            this.battery.removeEventListener('chargingchange', this.updateBatteryStatus);
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BatterySaver;
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
    // Check if already initialized
    if (!window.airforgeBatterySaver) {
        window.airforgeBatterySaver = new BatterySaver();
        console.log('🔋 BatterySaver auto-initialized');
    }
}