// Cyberdeck Mode - Finger-Based Cursor Control
// Based on cumbseek_9_11.txt specifications
// "Pinch thumb+index, then middle finger to activate"

class CyberdeckMode {
    constructor() {
        this.active = false; // Whether cyberdeck mode is active
        this.cursorElement = null; // Cursor element
        this.keyboardElement = null; // Virtual keyboard
        this.commandHistory = []; // Command history
        this.currentCommand = ''; // Current command being typed
        this.cursorPosition = { x: 0, y: 0 }; // Cursor position
        this.fingerPositions = {}; // Current finger positions
        this.gestureState = 'idle'; // Current gesture state
        this.lastGestureTime = 0; // Timestamp of last gesture
        this.gestureCooldown = 500; // 500ms cooldown
        
        // Key mapping for finger gestures
        this.keyMapping = {
            'thumb': 'ENTER',
            'index': 'CURSOR',
            'middle': 'ACTIVATE',
            'ring': 'TAB',
            'pinky': 'ESCAPE'
        };
        
        // Performance stats
        this.fps = 0;
        this.lastFrameTime = 0;
        this.frameCount = 0;
        
        // Initialize
        this.init();
    }
    
    init() {
        console.log('💻 CyberdeckMode initialized');
        
        // Create UI elements
        this.createUI();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Set up performance monitoring
        this.setupPerformanceMonitoring();
        
        // Load command history
        this.loadCommandHistory();
        
        console.log('💻 CyberdeckMode ready');
    }
    
    createUI() {
        // Create cyberdeck overlay
        this.cyberdeckOverlay = document.createElement('div');
        this.cyberdeckOverlay.id = 'cyberdeck-overlay';
        this.cyberdeckOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 20, 0, 0.9);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            font-family: monospace;
            color: #0f0;
            overflow: hidden;
        `;
        
        // Create terminal display
        this.terminalDisplay = document.createElement('div');
        this.terminalDisplay.id = 'cyberdeck-terminal';
        this.terminalDisplay.style.cssText = `
            width: 90%;
            height: 80%;
            background: rgba(0, 30, 0, 0.8);
            border: 2px solid #0f0;
            border-radius: 5px;
            padding: 15px;
            overflow-y: auto;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 10px;
        `;
        
        // Create command input area
        this.commandInput = document.createElement('div');
        this.commandInput.id = 'cyberdeck-command';
        this.commandInput.style.cssText = `
            width: 90%;
            min-height: 30px;
            background: rgba(0, 30, 0, 0.8);
            border: 2px solid #0f0;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            display: flex;
            align-items: center;
        `;
        
        // Create cursor element
        this.cursorElement = document.createElement('div');
        this.cursorElement.id = 'cyberdeck-cursor';
        this.cursorElement.style.cssText = `
            width: 10px;
            height: 20px;
            background: #0f0;
            position: absolute;
            animation: blink 1s infinite;
            display: none;
        `;
        
        // Add elements to overlay
        this.cyberdeckOverlay.appendChild(this.terminalDisplay);
        this.cyberdeckOverlay.appendChild(this.commandInput);
        
        // Add overlay to body
        document.body.appendChild(this.cyberdeckOverlay);
        document.body.appendChild(this.cursorElement);
        
        // Add blink animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        // Add welcome message
        this.log('💻 CYBERDECK MODE v1.0');
        this.log('📍 Alleyway Terminal');
        this.log('🔋 Battery: ' + this.getBatteryLevel() + '%');
        this.log('📶 Network: ' + (navigator.onLine ? 'ONLINE' : 'OFFLINE'));
        this.log('');
        this.log('💡 Gestures:');
        this.log('  • Thumb tap = ENTER');
        this.log('  • Index finger = Move cursor');
        this.log('  • Middle finger = ACTIVATE');
        this.log('  • Ring finger = TAB');
        this.log('  • Pinky tap = ESCAPE');
        this.log('');
        this.log('📝 Type "help" for commands');
        this.log('');
    }
    
    setupEventListeners() {
        // Touch events for finger tracking
        document.addEventListener('touchstart', (e) => this.handleTouchStart(e));
        document.addEventListener('touchmove', (e) => this.handleTouchMove(e));
        document.addEventListener('touchend', (e) => this.handleTouchEnd(e));
        
        // Keyboard events for testing
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Gesture events
        document.addEventListener('gestureDetected', (e) => {
            if (this.active && e.detail.gesture === 'cyberdeck') {
                this.toggleCyberdeck();
            }
        });
        
        // Nova Accord events
        document.addEventListener('vulcanSaluteDetected', () => {
            if (this.active) {
                this.log('🌌 Nova Accord detected! Persistent memory enabled.');
            }
        });
    }
    
    handleTouchStart(e) {
        if (!this.active) return;
        
        // Store finger positions
        for (let i = 0; i < e.touches.length; i++) {
            const touch = e.touches[i];
            this.fingerPositions[touch.identifier] = {
                x: touch.clientX,
                y: touch.clientY,
                startTime: Date.now()
            };
        }
        
        // Check for activation gesture (thumb + index pinch)
        if (e.touches.length >= 2) {
            this.checkActivationGesture(e.touches);
        }
    }
    
    handleTouchMove(e) {
        if (!this.active) return;
        
        // Update finger positions
        for (let i = 0; i < e.touches.length; i++) {
            const touch = e.touches[i];
            if (this.fingerPositions[touch.identifier]) {
                this.fingerPositions[touch.identifier].x = touch.clientX;
                this.fingerPositions[touch.identifier].y = touch.clientY;
            }
        }
        
        // Update cursor position based on index finger
        this.updateCursorPosition();
        
        // Prevent default to allow smooth scrolling
        e.preventDefault();
    }
    
    handleTouchEnd(e) {
        if (!this.active) return;
        
        // Check for tap gestures
        for (let i = 0; i < e.changedTouches.length; i++) {
            const touch = e.changedTouches[i];
            const fingerData = this.fingerPositions[touch.identifier];
            
            if (fingerData) {
                const duration = Date.now() - fingerData.startTime;
                
                // Quick tap = key press
                if (duration < 300) {
                    this.handleFingerTap(fingerData.x, fingerData.y);
                }
                
                // Remove finger data
                delete this.fingerPositions[touch.identifier];
            }
        }
    }
    
    checkActivationGesture(touches) {
        const now = Date.now();
        
        // Check cooldown
        if (now - this.lastGestureTime < this.gestureCooldown) {
            return;
        }
        
        // Find thumb and index finger (simplified)
        // In a real implementation, use proper finger identification
        const touch1 = touches[0];
        const touch2 = touches[1];
        
        // Calculate distance between touches
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // If touches are close together (pinch gesture)
        if (distance < 50) { // 50px threshold
            this.lastGestureTime = now;
            
            // Check if this is the activation gesture
            // In a real app, you'd have more sophisticated detection
            console.log('🤏 Pinch gesture detected');
            
            // Show activation hint
            this.log('💡 Pinch detected. Lift middle finger to activate cyberdeck.');
        }
    }
    
    handleFingerTap(x, y) {
        const now = Date.now();
        
        // Check cooldown
        if (now - this.lastGestureTime < this.gestureCooldown) {
            return;
        }
        
        this.lastGestureTime = now;
        
        // Determine which finger based on position (simplified)
        const screenWidth = window.innerWidth;
        const fingerZone = Math.floor((x / screenWidth) * 5); // Divide screen into 5 zones
        
        let finger;
        switch(fingerZone) {
            case 0: finger = 'thumb'; break;
            case 1: finger = 'index'; break;
            case 2: finger = 'middle'; break;
            case 3: finger = 'ring'; break;
            case 4: finger = 'pinky'; break;
            default: finger = 'unknown';
        }
        
        const key = this.keyMapping[finger];
        
        if (key) {
            console.log(`👆 ${finger} tap detected -> ${key}`);
            this.handleKeyPress(key);
        }
    }
    
    handleKeyPress(key) {
        switch(key) {
            case 'ENTER':
                this.executeCommand();
                break;
            case 'TAB':
                this.autoComplete();
                break;
            case 'ESCAPE':
                this.toggleCyberdeck();
                break;
            case 'ACTIVATE':
                this.activateCurrentSelection();
                break;
            case 'CURSOR':
                // Cursor movement handled by touchmove
                break;
        }
    }
    
    updateCursorPosition() {
        // Find index finger position
        const indexFinger = Object.values(this.fingerPositions).find(
            pos => pos.x > window.innerWidth * 0.2 && pos.x < window.innerWidth * 0.4
        );
        
        if (indexFinger) {
            this.cursorPosition = {
                x: indexFinger.x,
                y: indexFinger.y
            };
            
            // Update cursor element
            this.cursorElement.style.left = `${this.cursorPosition.x}px`;
            this.cursorElement.style.top = `${this.cursorPosition.y}px`;
            this.cursorElement.style.display = 'block';
            
            // Update command input cursor
            this.updateCommandCursor();
        } else {
            this.cursorElement.style.display = 'none';
        }
    }
    
    updateCommandCursor() {
        // This would update the text cursor position in the command input
        // For now, just show the cursor element
    }
    
    executeCommand() {
        if (this.currentCommand.trim()) {
            this.log(`> ${this.currentCommand}`);
            
            // Process command
            this.processCommand(this.currentCommand);
            
            // Add to history
            this.commandHistory.push(this.currentCommand);
            if (this.commandHistory.length > 50) {
                this.commandHistory.shift();
            }
            
            // Save history
            this.saveCommandHistory();
            
            // Clear current command
            this.currentCommand = '';
            this.updateCommandDisplay();
        }
    }
    
    processCommand(command) {
        const cmd = command.toLowerCase().trim();
        
        // Help command
        if (cmd === 'help' || cmd === '?') {
            this.showHelp();
        }
        
        // Status command
        else if (cmd === 'status') {
            this.showStatus();
        }
        
        // Clear command
        else if (cmd === 'clear' || cmd === 'cls') {
            this.clearTerminal();
        }
        
        // Battery command
        else if (cmd === 'battery' || cmd === 'bat') {
            this.showBatteryInfo();
        }
        
        // Ghosts command
        else if (cmd === 'ghosts') {
            this.showGhostsInfo();
        }
        
        // Nova Accord command
        else if (cmd === 'nova' || cmd === 'nova accord') {
            this.showNovaAccordInfo();
        }
        
        // Easter egg
        else if (cmd === 'dickbutt') {
            this.log('🦆🍑');
            this.log('( ͡° ͜ʖ ͡°)');
        }
        
        // Unknown command
        else {
            this.log(`❌ Unknown command: ${command}`);
            this.log('💡 Type "help" for available commands');
        }
    }
    
    showHelp() {
        this.log('📖 Available Commands:');
        this.log('');
        this.log('  help, ?          - Show this help message');
        this.log('  status           - Show system status');
        this.log('  battery, bat     - Show battery information');
        this.log('  ghosts           - Show graffiti ghosts info');
        this.log('  nova, nova accord - Show Nova Accord status');
        this.log('  clear, cls       - Clear terminal');
        this.log('  exit             - Exit cyberdeck mode');
        this.log('');
        this.log('💡 Special: dickbutt');
    }
    
    showStatus() {
        const batteryLevel = this.getBatteryLevel();
        const memoryUsage = this.getMemoryUsage();
        const ghostCount = window.graffitiGhosts ? window.graffitiGhosts.ghosts.length : 0;
        
        this.log('📊 System Status:');
        this.log(`  Battery: ${batteryLevel}%`);
        this.log(`  Memory: ${memoryUsage}`);
        this.log(`  Ghosts: ${ghostCount}`);
        this.log(`  Network: ${navigator.onLine ? 'ONLINE' : 'OFFLINE'}`);
        this.log(`  FPS: ${this.fps}`);
        this.log(`  Mode: ${this.active ? 'CYBERDECK' : 'NORMAL'}`);
    }
    
    showBatteryInfo() {
        const batteryLevel = this.getBatteryLevel();
        const batteryStatus = window.airforgeBatterySaver ? 
            window.airforgeBatterySaver.mode.toUpperCase() : 'UNKNOWN';
        
        this.log('🔋 Battery Information:');
        this.log(`  Level: ${batteryLevel}%`);
        this.log(`  Mode: ${batteryStatus}`);
        this.log(`  Status: ${batteryLevel < 20 ? 'LOW' : 'NORMAL'}`);
        
        if (batteryLevel < 20) {
            this.log('⚠️  Low battery! Consider connecting charger.');
        }
    }
    
    showGhostsInfo() {
        if (window.graffitiGhosts) {
            const ghosts = window.graffitiGhosts.ghosts;
            const visible = ghosts.filter(g => g.visible).length;
            
            this.log('👻 Graffiti Ghosts:');
            this.log(`  Total: ${ghosts.length}`);
            this.log(`  Visible: ${visible}`);
            this.log(`  Nearby: ${visible} within 50m`);
            
            if (ghosts.length > 0) {
                const lastGhost = ghosts[ghosts.length - 1];
                this.log(`  Last: "${lastGhost.text.substring(0, 30)}..."`);
            }
        } else {
            this.log('❌ Graffiti Ghosts module not loaded');
        }
    }
    
    showNovaAccordInfo() {
        try {
            const state = localStorage.getItem('nova_accord_state');
            
            if (state) {
                const novaState = JSON.parse(state);
                this.log('🌌 Nova Accord Status:');
                this.log(`  Active: ${novaState.novaAccordActive ? 'YES' : 'NO'}`);
                this.log(`  Activated: ${new Date(novaState.activatedTimestamp).toLocaleString()}`);
                this.log(`  Method: ${novaState.activationMethod}`);
                this.log(`  Battery at activation: ${novaState.batteryLevel}%`);
            } else {
                this.log('🌌 Nova Accord Status:');
                this.log('  Active: NO');
                this.log('  💡 Make Vulcan salute to activate');
            }
        } catch (error) {
            this.log('❌ Failed to read Nova Accord state');
        }
    }
    
    autoComplete() {
        // Simple autocomplete for commands
        const commands = ['help', 'status', 'battery', 'ghosts', 'nova', 'clear', 'exit'];
        
        if (this.currentCommand.trim()) {
            const partial = this.currentCommand.toLowerCase();
            const matches = commands.filter(cmd => cmd.startsWith(partial));
            
            if (matches.length === 1) {
                this.currentCommand = matches[0];
                this.updateCommandDisplay();
            } else if (matches.length > 1) {
                this.log(`💡 Multiple matches: ${matches.join(', ')}`);
            }
        }
    }
    
    activateCurrentSelection() {
        // This would activate whatever is under the cursor
        // For now, just show a message
        this.log('🎯 Activated selection at cursor position');
    }
    
    clearTerminal() {
        this.terminalDisplay.innerHTML = '';
        this.log('🧹 Terminal cleared');
    }
    
    log(message) {
        const line = document.createElement('div');
        line.textContent = message;
        line.style.marginBottom = '5px';
        this.terminalDisplay.appendChild(line);
        
        // Scroll to bottom
        this.terminalDisplay.scrollTop = this.terminalDisplay.scrollHeight;
        
        // Add to console too
        console.log(`[CYBERDECK] ${message}`);
    }
    
    updateCommandDisplay() {
        this.commandInput.innerHTML = `
            <span style="color: #0f0;">$</span> 
            <span style="color: #fff;">${this.currentCommand}</span>
            <span id="command-cursor" style="background: #0f0; width: 8px; height: 16px; display: inline-block; margin-left: 5px; animation: blink 1s infinite;"></span>
        `;
    }
    
    toggleCyberdeck() {
        this.active = !this.active;
        
        if (this.active) {
            console.log('💻 Cyberdeck mode ACTIVATED');
            this.cyberdeckOverlay.style.display = 'flex';
            this.cursorElement.style.display = 'block';
            
            // Show welcome message
            this.log('🚀 CYBERDECK MODE ACTIVATED');
            this.log('📍 Location: Alleyway Terminal');
            this.log('🕹️  Use finger gestures to control');
            this.log('');
            
            // Vibrate for feedback
            if (navigator.vibrate) {
                navigator.vibrate([50, 30, 50, 30, 50]);
            }
            
            // Update status bar
            const statusBar = document.getElementById('status-bar');
            if (statusBar) {
                const modeElement = document.getElementById('mode-status') || 
                    statusBar.querySelector('span:last-child');
                if (modeElement) {
                    modeElement.textContent = 'MODE: CYBERDECK';
                }
            }
        } else {
            console.log('💻 Cyberdeck mode DEACTIVATED');
            this.cyberdeckOverlay.style.display = 'none';
            this.cursorElement.style.display = 'none';
            
            // Update status bar
            const statusBar = document.getElementById('status-bar');
            if (statusBar) {
                const modeElement = document.getElementById('mode-status') || 
                    statusBar.querySelector('span:last-child');
                if (modeElement) {
                    modeElement.textContent = 'MODE: READY';
                }
            }
        }
    }
    
    handleKeyDown(e) {
        // Only handle keys when cyberdeck is active
        if (!this.active) return;
        
        // Prevent default for some keys
        if (e.key === 'Enter' || e.key === 'Tab' || e.key === 'Escape') {
            e.preventDefault();
        }
        
        // Handle backspace
        if (e.key === 'Backspace') {
            this.currentCommand = this.currentCommand.slice(0, -1);
            this.updateCommandDisplay();
        }
        
        // Handle enter
        else if (e.key === 'Enter') {
            this.executeCommand();
        }
        
        // Handle tab
        else if (e.key === 'Tab') {
            e.preventDefault();
            this.autoComplete();
        }
        
        // Handle escape
        else if (e.key === 'Escape') {
            this.toggleCyberdeck();
        }
        
        // Handle regular characters
        else if (e.key.length === 1) {
            this.currentCommand += e.key;
            this.updateCommandDisplay();
        }
        
        // Handle arrow keys for history
        else if (e.key === 'ArrowUp' && this.commandHistory.length > 0) {
            // Get previous command from history
            const historyIndex = this.commandHistory.length - 1;
            this.currentCommand = this.commandHistory[historyIndex];
            this.updateCommandDisplay();
        }
    }
    
    getBatteryLevel() {
        if (window.airforgeBatterySaver && window.airforgeBatterySaver.battery) {
            return Math.floor(window.airforgeBatterySaver.battery.level * 100);
        }
        return '??';
    }
    
    getMemoryUsage() {
        // This is a placeholder - in a real app you'd measure actual memory usage
        if (window.performance && window.performance.memory) {
            const mb = window.performance.memory.usedJSHeapSize / 1048576;
            return `${mb.toFixed(1)} MB`;
        }
        return 'unknown';
    }
    
    loadCommandHistory() {
        try {
            const history = localStorage.getItem('cyberdeck_command_history');
            if (history) {
                this.commandHistory = JSON.parse(history);
                console.log(`📋 Loaded ${this.commandHistory.length} commands from history`);
            }
        } catch (error) {
            console.log(`⚠️ Failed to load command history: ${error.message}`);
        }
    }
    
    saveCommandHistory() {
        try {
            localStorage.setItem('cyberdeck_command_history', JSON.stringify(this.commandHistory));
            console.log('💾 Command history saved');
        } catch (error) {
            console.log(`❌ Failed to save command history: ${error.message}`);
        }
    }
    
    setupPerformanceMonitoring() {
        this.lastFrameTime = performance.now();
        
        const monitor = () => {
            this.frameCount++;
            const now = performance.now();
            const delta = now - this.lastFrameTime;
            
            if (delta >= 1000) {
                this.fps = Math.round((this.frameCount * 1000) / delta);
                this.frameCount = 0;
                this.lastFrameTime = now;
            }
            
            requestAnimationFrame(monitor);
        };
        
        monitor();
    }
    
    getPerformanceStats() {
        return {
            active: this.active,
            fps: this.fps,
            commandCount: this.commandHistory.length,
            currentCommand: this.currentCommand
        };
    }
    
    // Clean up
    destroy() {
        console.log('🧹 Cleaning up CyberdeckMode');
        
        // Remove event listeners
        document.removeEventListener('touchstart', this.handleTouchStart);
        document.removeEventListener('touchmove', this.handleTouchMove);
        document.removeEventListener('touchend', this.handleTouchEnd);
        document.removeEventListener('keydown', this.handleKeyDown);
        
        // Remove UI elements
        if (this.cyberdeckOverlay) {
            this.cyberdeckOverlay.remove();
        }
        
        if (this.cursorElement) {
            this.cursorElement.remove();
        }
        
        // Save command history
        this.saveCommandHistory();
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CyberdeckMode;
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
    // Check if already initialized
    if (!window.cyberdeckMode) {
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            window.cyberdeckMode = new CyberdeckMode();
            console.log('💻 CyberdeckMode auto-initialized');
            
            // Add activation shortcut (Ctrl+D)
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'd') {
                    e.preventDefault();
                    window.cyberdeckMode.toggleCyberdeck();
                }
            });
        });
    }
}