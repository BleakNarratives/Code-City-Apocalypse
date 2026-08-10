// Graffiti Ghosts - AR Text Persistence System
// Based on cumbseek_9_11.txt specifications
// "Text you spray in AR space with finger-gun gesture"

class GraffitiGhosts {
    constructor() {
        this.ghosts = []; // Array to store all graffiti ghosts
        this.currentGhost = null; // Currently selected ghost
        this.sprayMode = false; // Spray mode active
        this.viewMode = true; // View existing ghosts
        this.gpsAccuracy = 0; // GPS accuracy in meters
        this.lastPosition = null; // Last known GPS position
        this.landmarkDatabase = {}; // Visual landmarks for persistence
        this.p2pSyncInterval = null; // P2P sync interval
        this.p2pPeers = []; // Connected peers
        
        // Initialize
        this.init();
    }
    
    init() {
        console.log('👻 GraffitiGhosts initialized');
        
        // Load saved ghosts from localStorage
        this.loadGhosts();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Start GPS monitoring
        this.startGPS();
        
        // Start P2P sync (if available)
        this.startP2PSync();
        
        // Create UI
        this.createUI();
        
        console.log(`📊 Loaded ${this.ghosts.length} graffiti ghosts`);
    }
    
    setupEventListeners() {
        // Gesture detection for spray mode
        document.addEventListener('gestureDetected', (e) => {
            const gesture = e.detail.gesture;
            
            if (gesture === 'finger-gun') {
                this.toggleSprayMode();
            } else if (gesture === 'pinch' && this.sprayMode) {
                this.createGhost();
            } else if (gesture === 'swipe-left' && this.viewMode) {
                this.previousGhost();
            } else if (gesture === 'swipe-right' && this.viewMode) {
                this.nextGhost();
            }
        });
        
        // Voice commands
        window.addEventListener('voiceCommand', (e) => {
            const command = e.detail.command;
            
            if (command.includes('spray') || command.includes('ghost')) {
                this.toggleSprayMode();
            } else if (command.includes('save') || command.includes('persist')) {
                this.saveGhosts();
            }
        });
        
        // Device orientation for AR positioning
        window.addEventListener('deviceorientation', (e) => {
            if (this.sprayMode && this.currentGhost) {
                this.updateGhostPosition(e);
            }
        });
    }
    
    createUI() {
        // Create spray mode indicator
        this.sprayIndicator = document.createElement('div');
        this.sprayIndicator.id = 'graffiti-spray-indicator';
        this.sprayIndicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: #0f0;
            padding: 10px 20px;
            border-radius: 25px;
            font-family: monospace;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 1000;
            pointer-events: none;
        `;
        this.sprayIndicator.textContent = '👻 SPRAY MODE ACTIVE';
        document.body.appendChild(this.sprayIndicator);
        
        // Create ghost counter
        this.ghostCounter = document.createElement('div');
        this.ghostCounter.id = 'graffiti-ghost-counter';
        this.ghostCounter.style.cssText = `
            position: fixed;
            top: 50px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: #0f0;
            padding: 5px 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            z-index: 999;
        `;
        this.updateGhostCounter();
        document.body.appendChild(this.ghostCounter);
    }
    
    updateGhostCounter() {
        this.ghostCounter.textContent = `👻 ${this.ghosts.length}`;
    }
    
    startGPS() {
        if ('geolocation' in navigator) {
            console.log('📍 GPS available');
            
            // Request high accuracy GPS
            const gpsOptions = {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            };
            
            // Watch position
            this.gpsWatchId = navigator.geolocation.watchPosition(
                (position) => this.handleGPSPosition(position),
                (error) => this.handleGPSError(error),
                gpsOptions
            );
        } else {
            console.log('⚠️ GPS not available, using fallback positioning');
            // Fallback to visual landmarks only
        }
    }
    
    handleGPSPosition(position) {
        this.lastPosition = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: position.timestamp
        };
        
        this.gpsAccuracy = position.coords.accuracy;
        
        console.log(`📍 GPS: ${position.coords.latitude.toFixed(6)}, ${position.coords.longitude.toFixed(6)}`);
        console.log(`🎯 Accuracy: ${position.coords.accuracy.toFixed(1)} meters`);
        
        // Update ghosts that are near this location
        this.updateNearbyGhosts();
    }
    
    handleGPSError(error) {
        console.log(`❌ GPS error: ${error.message}`);
        
        switch(error.code) {
            case error.PERMISSION_DENIED:
                console.log('🚫 GPS permission denied');
                break;
            case error.POSITION_UNAVAILABLE:
                console.log('📡 GPS position unavailable');
                break;
            case error.TIMEOUT:
                console.log('⏱️ GPS timeout');
                break;
        }
    }
    
    updateNearbyGhosts() {
        if (!this.lastPosition) return;
        
        const maxDistance = 50; // 50 meters
        
        this.ghosts.forEach(ghost => {
            if (ghost.position && ghost.position.latitude && ghost.position.longitude) {
                const distance = this.calculateDistance(
                    this.lastPosition.latitude, 
                    this.lastPosition.longitude,
                    ghost.position.latitude,
                    ghost.position.longitude
                );
                
                if (distance <= maxDistance) {
                    ghost.visible = true;
                    ghost.distance = distance;
                    console.log(`👻 Ghost "${ghost.text.substring(0, 20)}..." nearby (${distance.toFixed(1)}m)`);
                } else {
                    ghost.visible = false;
                }
            }
        });
        
        // Update UI to show nearby ghosts
        this.updateVisibleGhosts();
    }
    
    calculateDistance(lat1, lon1, lat2, lon2) {
        // Haversine formula for distance between two GPS coordinates
        const R = 6371000; // Earth radius in meters
        const φ1 = lat1 * Math.PI / 180;
        const φ2 = lat2 * Math.PI / 180;
        const Δφ = (lat2 - lat1) * Math.PI / 180;
        const Δλ = (lon2 - lon1) * Math.PI / 180;
        
        const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
                  Math.cos(φ1) * Math.cos(φ2) *
                  Math.sin(Δλ/2) * Math.sin(Δλ/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        
        return R * c; // Distance in meters
    }
    
    startP2PSync() {
        // Check for WebRTC or other P2P capabilities
        if ('RTCPeerConnection' in window || 'webkitRTCPeerConnection' in window) {
            console.log('🔗 P2P capabilities detected');
            
            // Set up periodic sync
            this.p2pSyncInterval = setInterval(() => {
                this.syncWithPeers();
            }, 30000); // Sync every 30 seconds
            
            // Set up WebRTC data channel for direct device communication
            this.setupWebRTC();
        } else {
            console.log('⚠️ P2P not available, using QR code sync instead');
        }
    }
    
    setupWebRTC() {
        // This would be a more complete WebRTC implementation
        // For now, we'll just set up the basic structure
        
        this.webrtc = {
            peerConnections: {},
            dataChannels: {},
            signalingServer: null
        };
        
        console.log('🌐 WebRTC ready for peer connections');
    }
    
    syncWithPeers() {
        if (this.p2pPeers.length === 0) {
            return; // No peers to sync with
        }
        
        console.log(`🔄 Syncing with ${this.p2pPeers.length} peers...`);
        
        // Create a summary of our ghosts for sync
        const ghostSummary = this.ghosts.map(ghost => ({
            id: ghost.id,
            position: ghost.position,
            timestamp: ghost.timestamp,
            textLength: ghost.text.length
        }));
        
        // In a real implementation, we would:
        // 1. Compare ghost IDs with peers
        // 2. Request missing ghosts
        // 3. Send our unique ghosts
        // 4. Resolve conflicts
        
        console.log(`📋 Sharing ${ghostSummary.length} ghost summaries`);
        
        // For demo purposes, just log what we would sync
        this.p2pPeers.forEach(peer => {
            console.log(`🔗 Would sync with peer ${peer.id}`);
        });
    }
    
    toggleSprayMode() {
        this.sprayMode = !this.sprayMode;
        this.viewMode = !this.sprayMode;
        
        if (this.sprayMode) {
            console.log('🎨 Spray mode ACTIVATED');
            this.sprayIndicator.style.opacity = '1';
            this.sprayIndicator.style.background = 'rgba(0, 255, 0, 0.3)';
            
            // Create a new ghost
            this.createNewGhost();
            
            // Vibrate for feedback
            if (navigator.vibrate) {
                navigator.vibrate([50, 30, 50]);
            }
        } else {
            console.log('👁️ View mode ACTIVATED');
            this.sprayIndicator.style.opacity = '0';
            
            // Save the current ghost if it has content
            if (this.currentGhost && this.currentGhost.text.trim()) {
                this.saveCurrentGhost();
            }
            
            // Show all nearby ghosts
            this.updateVisibleGhosts();
        }
    }
    
    createNewGhost() {
        this.currentGhost = {
            id: this.generateGhostId(),
            text: '',
            position: this.lastPosition ? {
                latitude: this.lastPosition.latitude,
                longitude: this.lastPosition.longitude,
                accuracy: this.lastPosition.accuracy
            } : null,
            timestamp: Date.now(),
            visible: true,
            landmark: null, // Visual landmark reference
            author: 'anonymous',
            style: {
                color: this.getRandomColor(),
                size: 1.0,
                font: 'Arial'
            }
        };
        
        console.log(`👻 Created new ghost ${this.currentGhost.id}`);
    }
    
    createGhost() {
        if (!this.sprayMode || !this.currentGhost) {
            return;
        }
        
        // In a real implementation, this would be triggered by
        // a specific gesture (like finger-gun + pinch)
        
        console.log('🎨 Spraying graffiti ghost...');
        
        // Add to ghosts array
        this.ghosts.push(this.currentGhost);
        this.updateGhostCounter();
        
        // Create a new ghost for next spray
        this.createNewGhost();
        
        // Save to localStorage
        this.saveGhosts();
        
        // Sync with peers
        this.syncWithPeers();
        
        // Visual feedback
        this.showSprayEffect();
    }
    
    showSprayEffect() {
        // Create spray effect animation
        const effect = document.createElement('div');
        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(0,255,0,0.8) 0%, rgba(0,255,0,0) 70%);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 2000;
            animation: spray 1s ease-out;
        `;
        
        document.body.appendChild(effect);
        
        // Remove after animation
        setTimeout(() => {
            effect.remove();
        }, 1000);
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spray {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    saveCurrentGhost() {
        if (!this.currentGhost || !this.currentGhost.text.trim()) {
            return;
        }
        
        // Add to ghosts array if not already there
        if (!this.ghosts.some(g => g.id === this.currentGhost.id)) {
            this.ghosts.push(this.currentGhost);
            this.updateGhostCounter();
        }
        
        // Save to localStorage
        this.saveGhosts();
        
        console.log(`💾 Saved ghost ${this.currentGhost.id}`);
    }
    
    saveGhosts() {
        try {
            const ghostsToSave = this.ghosts.map(ghost => ({
                id: ghost.id,
                text: ghost.text,
                position: ghost.position,
                timestamp: ghost.timestamp,
                landmark: ghost.landmark,
                author: ghost.author,
                style: ghost.style
            }));
            
            localStorage.setItem('graffiti_ghosts', JSON.stringify(ghostsToSave));
            console.log(`💾 Saved ${ghostsToSave.length} ghosts to localStorage`);
            
            return true;
        } catch (error) {
            console.log(`❌ Failed to save ghosts: ${error.message}`);
            return false;
        }
    }
    
    loadGhosts() {
        try {
            const savedGhosts = localStorage.getItem('graffiti_ghosts');
            
            if (savedGhosts) {
                this.ghosts = JSON.parse(savedGhosts);
                console.log(`📋 Loaded ${this.ghosts.length} ghosts from localStorage`);
                
                // Update visible status based on current position
                if (this.lastPosition) {
                    this.updateNearbyGhosts();
                }
                
                return true;
            }
        } catch (error) {
            console.log(`⚠️ Failed to load ghosts: ${error.message}`);
        }
        
        return false;
    }
    
    updateVisibleGhosts() {
        // In a real implementation, this would update the AR view
        // to show/hide ghosts based on their visible property
        
        const visibleGhosts = this.ghosts.filter(g => g.visible);
        console.log(`👁️ ${visibleGhosts.length} ghosts visible nearby`);
        
        // For demo, just log them
        visibleGhosts.forEach(ghost => {
            const distance = ghost.distance ? ghost.distance.toFixed(1) + 'm' : 'unknown';
            console.log(`  - "${ghost.text.substring(0, 30)}..." (${distance})`);
        });
    }
    
    nextGhost() {
        if (this.ghosts.length === 0) return;
        
        const visibleGhosts = this.ghosts.filter(g => g.visible);
        if (visibleGhosts.length === 0) return;
        
        const currentIndex = visibleGhosts.findIndex(g => g.id === (this.currentGhost?.id));
        const nextIndex = (currentIndex + 1) % visibleGhosts.length;
        
        this.currentGhost = visibleGhosts[nextIndex];
        console.log(`👉 Selected ghost: "${this.currentGhost.text.substring(0, 30)}..."`);
        
        // In real implementation, center camera on this ghost
    }
    
    previousGhost() {
        if (this.ghosts.length === 0) return;
        
        const visibleGhosts = this.ghosts.filter(g => g.visible);
        if (visibleGhosts.length === 0) return;
        
        const currentIndex = visibleGhosts.findIndex(g => g.id === (this.currentGhost?.id));
        const prevIndex = (currentIndex - 1 + visibleGhosts.length) % visibleGhosts.length;
        
        this.currentGhost = visibleGhosts[prevIndex];
        console.log(`👈 Selected ghost: "${this.currentGhost.text.substring(0, 30)}..."`);
        
        // In real implementation, center camera on this ghost
    }
    
    generateGhostId() {
        return 'ghost-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
    }
    
    getRandomColor() {
        const colors = [
            '#0ff', '#f0f', '#ff0', '#0f0', '#f00', '#00f',
            '#ff69b4', '#00ffff', '#ffa500', '#8a2be2'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    updateGhostPosition(orientation) {
        if (!this.currentGhost || !this.sprayMode) return;
        
        // Update ghost position based on device orientation
        // This would position the ghost in 3D space relative to the user
        
        this.currentGhost.orientation = {
            alpha: orientation.alpha, // Z-axis rotation [0,360]
            beta: orientation.beta,   // X-axis rotation [-180,180]
            gamma: orientation.gamma  // Y-axis rotation [-90,90]
        };
        
        // In a real AR implementation, this would update the 3D position
        console.log(`📍 Updated ghost position: α=${orientation.alpha.toFixed(1)}°, β=${orientation.beta.toFixed(1)}°, γ=${orientation.gamma.toFixed(1)}°`);
    }
    
    // QR code generation for sharing ghosts
    generateQRCode(ghostId) {
        const ghost = this.ghosts.find(g => g.id === ghostId);
        if (!ghost) return null;
        
        // Create a shareable representation
        const ghostData = {
            id: ghost.id,
            text: ghost.text,
            position: ghost.position,
            timestamp: ghost.timestamp,
            style: ghost.style
        };
        
        const dataStr = JSON.stringify(ghostData);
        
        // In a real implementation, use a QR code library
        console.log(`📱 QR data for ghost ${ghostId}:`);
        console.log(dataStr);
        
        return dataStr;
    }
    
    // Import ghost from QR code
    importFromQR(qrData) {
        try {
            const ghostData = JSON.parse(qrData);
            
            // Check if we already have this ghost
            if (this.ghosts.some(g => g.id === ghostData.id)) {
                console.log(`⚠️ Ghost ${ghostData.id} already exists`);
                return false;
            }
            
            // Add the ghost
            this.ghosts.push({
                ...ghostData,
                visible: true, // Assume it's visible since we just imported it
                landmark: null
            });
            
            this.updateGhostCounter();
            this.saveGhosts();
            
            console.log(`📥 Imported ghost ${ghostData.id}`);
            return true;
        } catch (error) {
            console.log(`❌ Failed to import ghost: ${error.message}`);
            return false;
        }
    }
    
    // Clean up
    destroy() {
        console.log('🧹 Cleaning up GraffitiGhosts');
        
        // Stop GPS
        if (this.gpsWatchId) {
            navigator.geolocation.clearWatch(this.gpsWatchId);
        }
        
        // Stop P2P sync
        if (this.p2pSyncInterval) {
            clearInterval(this.p2pSyncInterval);
        }
        
        // Remove UI elements
        if (this.sprayIndicator) {
            this.sprayIndicator.remove();
        }
        
        if (this.ghostCounter) {
            this.ghostCounter.remove();
        }
    }
    
    // Export ghosts for backup
    exportGhosts() {
        const exportData = {
            format: 'AirForge Graffiti Ghosts v1.0',
            timestamp: Date.now(),
            ghosts: this.ghosts,
            metadata: {
                count: this.ghosts.length,
                location: this.lastPosition ? 
                    `${this.lastPosition.latitude.toFixed(6)}, ${this.lastPosition.longitude.toFixed(6)}` : 'unknown'
            }
        };
        
        return JSON.stringify(exportData, null, 2);
    }
    
    // Import ghosts from backup
    importGhosts(importData) {
        try {
            const data = JSON.parse(importData);
            
            if (data.format !== 'AirForge Graffiti Ghosts v1.0') {
                console.log('⚠️ Invalid import format');
                return false;
            }
            
            // Merge ghosts (avoid duplicates)
            const newGhosts = data.ghosts.filter(newGhost => 
                !this.ghosts.some(existingGhost => existingGhost.id === newGhost.id)
            );
            
            if (newGhosts.length > 0) {
                this.ghosts.push(...newGhosts);
                this.updateGhostCounter();
                this.saveGhosts();
                console.log(`📥 Imported ${newGhosts.length} new ghosts`);
                return true;
            } else {
                console.log('ℹ️ No new ghosts to import');
                return true;
            }
        } catch (error) {
            console.log(`❌ Import failed: ${error.message}`);
            return false;
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GraffitiGhosts;
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
    // Check if already initialized
    if (!window.graffitiGhosts) {
        window.graffitiGhosts = new GraffitiGhosts();
        console.log('👻 GraffitiGhosts auto-initialized');
    }
}