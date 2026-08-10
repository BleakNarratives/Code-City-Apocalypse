// Vulcan Salute Gesture Detector
// Based on cumbseek_9_11.txt specifications
// "Make a Star Trek Vulcan salute to unlock Nova Accord mode"

class VulcanSaluteDetector {
    constructor() {
        this.handLandmarker = null; // MediaPipe hand landmarker
        this.videoElement = null; // Video element for camera feed
        this.canvasElement = null; // Canvas for drawing landmarks
        this.canvasCtx = null; // Canvas context
        this.detectionActive = false; // Whether detection is active
        this.saluteDetected = false; // Whether Vulcan salute is currently detected
        this.lastSaluteTime = 0; // Timestamp of last detected salute
        this.saluteCooldown = 3000; // 3 second cooldown between detections
        
        // Vulcan salute parameters
        this.ringPinkyDistanceThreshold = 0.03; // Max distance between ring and pinky
        this.middleIndexDistanceThreshold = 0.03; // Max distance between middle and index
        this.thumbIndexDistanceThreshold = 0.1; // Min distance between thumb and index
        
        // Performance monitoring
        this.fps = 0;
        this.lastFrameTime = 0;
        this.frameCount = 0;
        
        // Initialize
        this.init();
    }
    
    async init() {
        console.log('🖖 VulcanSaluteDetector initializing...');
        
        // Create video and canvas elements
        this.createVideoElements();
        
        // Load MediaPipe hand landmarker
        await this.loadHandLandmarker();
        
        // Set up performance monitoring
        this.setupPerformanceMonitoring();
        
        console.log('🖖 VulcanSaluteDetector ready');
    }
    
    createVideoElements() {
        // Create video element
        this.videoElement = document.createElement('video');
        this.videoElement.id = 'vulcan-video';
        this.videoElement.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -1;
            opacity: 0.3;
            transform: scaleX(-1);
        `;
        this.videoElement.playsInline = true;
        this.videoElement.autoplay = true;
        
        // Create canvas for landmarks
        this.canvasElement = document.createElement('canvas');
        this.canvasElement.id = 'vulcan-canvas';
        this.canvasElement.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 100;
        `;
        
        // Add elements to body
        document.body.appendChild(this.videoElement);
        document.body.appendChild(this.canvasElement);
        
        // Get canvas context
        this.canvasCtx = this.canvasElement.getContext('2d');
    }
    
    async loadHandLandmarker() {
        try {
            // Load MediaPipe tasks vision
            const vision = await import('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js');
            
            // Create hand landmarker
            this.handLandmarker = await vision.HandLandmarker.createFromOptions(
                vision, {
                    baseOptions: {
                        modelAssetPath: 'libs/models/hand_landmarker.task',
                        delegate: 'CPU'
                    },
                    runningMode: 'VIDEO',
                    numHands: 2
                }
            );
            
            console.log('✅ Hand landmarker loaded');
            
            // Start camera
            await this.startCamera();
            
        } catch (error) {
            console.log(`❌ Failed to load hand landmarker: ${error.message}`);
            console.log('💡 Falling back to touch-based detection');
            
            // Set up touch-based fallback
            this.setupTouchDetection();
        }
    }
    
    async startCamera() {
        try {
            // Request camera access
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'user',
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                },
                audio: false
            });
            
            this.videoElement.srcObject = stream;
            
            // Wait for video to be ready
            await new Promise((resolve) => {
                this.videoElement.onloadedmetadata = resolve;
            });
            
            // Start detection loop
            this.startDetectionLoop();
            
            console.log('📹 Camera started');
            
        } catch (error) {
            console.log(`❌ Camera error: ${error.message}`);
            console.log('💡 Using touch-based detection instead');
            
            // Set up touch-based fallback
            this.setupTouchDetection();
        }
    }
    
    startDetectionLoop() {
        this.detectionActive = true;
        
        const detect = async () => {
            if (!this.detectionActive) return;
            
            // Update FPS counter
            this.updateFPS();
            
            // Process video frame
            if (this.videoElement.readyState >= 2) {
                await this.processFrame();
            }
            
            requestAnimationFrame(detect);
        };
        
        detect();
    }
    
    async processFrame() {
        // Set canvas size to match video
        this.canvasElement.width = this.videoElement.videoWidth;
        this.canvasElement.height = this.videoElement.videoHeight;
        
        // Clear canvas
        this.canvasCtx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
        
        // Detect hand landmarks
        const results = this.handLandmarker.detectForVideo(
            this.videoElement,
            performance.now()
        );
        
        // Process results
        if (results.landmarks) {
            this.drawLandmarks(results.landmarks);
            this.checkForVulcanSalute(results.landmarks);
        }
    }
    
    drawLandmarks(landmarks) {
        // Draw each hand's landmarks
        landmarks.forEach((hand, handIndex) => {
            // Draw palm
            this.canvasCtx.fillStyle = handIndex === 0 ? 'rgba(0, 255, 0, 0.3)' : 'rgba(0, 0, 255, 0.3)';
            
            // Draw landmarks
            hand.forEach((landmark, index) => {
                const x = landmark.x * this.canvasElement.width;
                const y = landmark.y * this.canvasElement.height;
                
                // Highlight key points
                if ([4, 8, 12, 16, 20].includes(index)) { // Thumb, index, middle, ring, pinky tips
                    this.canvasCtx.fillStyle = 'rgba(255, 0, 0, 0.8)';
                    this.canvasCtx.beginPath();
                    this.canvasCtx.arc(x, y, 6, 0, 2 * Math.PI);
                    this.canvasCtx.fill();
                } else {
                    this.canvasCtx.fillStyle = handIndex === 0 ? 'rgba(0, 255, 0, 0.6)' : 'rgba(0, 0, 255, 0.6)';
                    this.canvasCtx.beginPath();
                    this.canvasCtx.arc(x, y, 4, 0, 2 * Math.PI);
                    this.canvasCtx.fill();
                }
            });
            
            // Draw connections
            this.canvasCtx.strokeStyle = handIndex === 0 ? 'rgba(0, 255, 0, 0.5)' : 'rgba(0, 0, 255, 0.5)';
            this.canvasCtx.lineWidth = 2;
            
            // Palm connections
            const palmConnections = [
                [0, 1], [1, 2], [2, 3], [3, 4],  // Thumb
                [0, 5], [5, 6], [6, 7], [7, 8],  // Index
                [0, 9], [9, 10], [10, 11], [11, 12], // Middle
                [0, 13], [13, 14], [14, 15], [15, 16], // Ring
                [0, 17], [17, 18], [18, 19], [19, 20]  // Pinky
            ];
            
            palmConnections.forEach(([start, end]) => {
                const startLandmark = hand[start];
                const endLandmark = hand[end];
                
                this.canvasCtx.beginPath();
                this.canvasCtx.moveTo(startLandmark.x * this.canvasElement.width, startLandmark.y * this.canvasElement.height);
                this.canvasCtx.lineTo(endLandmark.x * this.canvasElement.width, endLandmark.y * this.canvasElement.height);
                this.canvasCtx.stroke();
            });
        });
    }
    
    checkForVulcanSalute(landmarks) {
        // Check each hand for Vulcan salute
        landmarks.forEach((hand, handIndex) => {
            if (hand.length >= 21) { // Make sure we have all landmarks
                const wrist = hand[0];
                const thumb = hand[4];
                const index = hand[8];
                const middle = hand[12];
                const ring = hand[16];
                const pinky = hand[20];
                
                // Calculate distances
                const ringPinkyDist = this.calculateDistance(ring, pinky);
                const middleIndexDist = this.calculateDistance(middle, index);
                const thumbIndexDist = this.calculateDistance(thumb, index);
                
                // Check Vulcan salute conditions
                const isVulcan = 
                    ringPinkyDist < this.ringPinkyDistanceThreshold &&
                    middleIndexDist < this.middleIndexDistanceThreshold &&
                    thumbIndexDist > this.thumbIndexDistanceThreshold;
                
                if (isVulcan) {
                    this.onVulcanSaluteDetected(handIndex);
                }
            }
        });
    }
    
    calculateDistance(landmark1, landmark2) {
        // Calculate Euclidean distance between two landmarks (normalized coordinates)
        const dx = landmark1.x - landmark2.x;
        const dy = landmark1.y - landmark2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    onVulcanSaluteDetected(handIndex) {
        const now = Date.now();
        
        // Check cooldown
        if (now - this.lastSaluteTime < this.saluteCooldown) {
            return; // Too soon since last detection
        }
        
        this.lastSaluteTime = now;
        this.saluteDetected = true;
        
        console.log(`🖖 Vulcan salute detected with ${handIndex === 0 ? 'left' : 'right'} hand!`);
        
        // Trigger Nova Accord activation
        this.triggerNovaAccord();
        
        // Visual feedback
        this.showVulcanEffect();
        
        // Haptic feedback
        if (navigator.vibrate) {
            // Morse code for "V" (dot dot dot dash)
            navigator.vibrate([100, 100, 100, 300]);
        }
        
        // Dispatch custom event
        const event = new CustomEvent('vulcanSaluteDetected', {
            detail: {
                hand: handIndex === 0 ? 'left' : 'right',
                timestamp: now
            }
        });
        document.dispatchEvent(event);
    }
    
    triggerNovaAccord() {
        // Activate Nova Accord mode
        console.log('🌌 NOVA ACCORD ACTIVATED');
        
        // Show activation message
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 255, 0.9);
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            font-family: monospace;
            font-size: 18px;
            z-index: 2000;
            animation: pulse 2s;
            box-shadow: 0 0 30px rgba(0, 0, 255, 0.7);
        `;
        message.textContent = '🌌 NOVA ACCORD ACTIVATED';
        
        document.body.appendChild(message);
        
        // Add pulse animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0%, 100% { transform: translate(-50%, -50%) scale(1); }
                50% { transform: translate(-50%, -50%) scale(1.1); }
            }
        `;
        document.head.appendChild(style);
        
        // Remove after animation
        setTimeout(() => {
            message.remove();
            style.remove();
        }, 2000);
        
        // Enable persistent memory mode
        if (window.airforgeBatterySaver) {
            window.airforgeBatterySaver.setMode('psychic');
        }
        
        // Save state for persistence
        this.saveNovaAccordState();
    }
    
    saveNovaAccordState() {
        try {
            const state = {
                novaAccordActive: true,
                activatedTimestamp: Date.now(),
                activationMethod: 'vulcan_salute',
                batteryLevel: this.getBatteryLevel()
            };
            
            localStorage.setItem('nova_accord_state', JSON.stringify(state));
            console.log('💾 Nova Accord state saved');
            
        } catch (error) {
            console.log(`❌ Failed to save Nova Accord state: ${error.message}`);
        }
    }
    
    getBatteryLevel() {
        if (window.airforgeBatterySaver && window.airforgeBatterySaver.battery) {
            return Math.floor(window.airforgeBatterySaver.battery.level * 100);
        }
        return 'unknown';
    }
    
    showVulcanEffect() {
        // Create Vulcan salute effect
        const effect = document.createElement('div');
        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(0, 0, 255, 0.8) 0%, rgba(0, 0, 255, 0) 70%);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 1999;
            animation: vulcanPulse 1.5s;
        `;
        
        document.body.appendChild(effect);
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes vulcanPulse {
                0% { transform: translate(-50%, -50%) scale(0.8); opacity: 1; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
                100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        // Remove after animation
        setTimeout(() => {
            effect.remove();
            style.remove();
        }, 1500);
    }
    
    setupTouchDetection() {
        console.log('👆 Setting up touch-based Vulcan salute detection');
        
        let touchSequence = [];
        const requiredSequence = ['thumb', 'index', 'middle', 'ring', 'pinky'];
        const timeout = 3000; // 3 seconds to complete sequence
        let sequenceTimer = null;
        
        document.addEventListener('touchstart', (e) => {
            // This is a simplified touch detection
            // In a real app, you'd use a more sophisticated approach
            
            if (e.touches.length === 1) {
                // Get touch position
                const touch = e.touches[0];
                const x = touch.clientX / window.innerWidth;
                const y = touch.clientY / window.innerHeight;
                
                // Determine which finger based on touch position
                // This is very simplified!
                let finger;
                
                if (x < 0.2) finger = 'thumb';
                else if (x < 0.4) finger = 'index';
                else if (x < 0.6) finger = 'middle';
                else if (x < 0.8) finger = 'ring';
                else finger = 'pinky';
                
                touchSequence.push(finger);
                
                // Reset timer
                if (sequenceTimer) clearTimeout(sequenceTimer);
                
                sequenceTimer = setTimeout(() => {
                    touchSequence = [];
                    console.log('⏱️  Touch sequence timed out');
                }, timeout);
                
                // Check if sequence matches Vulcan salute
                const sequenceStr = touchSequence.join(',');
                const requiredStr = requiredSequence.join(',');
                
                if (sequenceStr === requiredStr) {
                    console.log('🖖 Touch-based Vulcan salute detected!');
                    this.onVulcanSaluteDetected(0); // 0 for left hand
                    touchSequence = [];
                } else {
                    console.log(`👆 Sequence: ${sequenceStr}`);
                }
            }
        });
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
                
                // Log FPS every 5 seconds
                if (now - this.lastFrameTime >= 5000) {
                    console.log(`📊 FPS: ${this.fps}`);
                }
            }
            
            if (this.detectionActive) {
                requestAnimationFrame(monitor);
            }
        };
        
        monitor();
    }
    
    updateFPS() {
        this.frameCount++;
        const now = performance.now();
        const delta = now - this.lastFrameTime;
        
        if (delta >= 1000) {
            this.fps = Math.round((this.frameCount * 1000) / delta);
            this.frameCount = 0;
            this.lastFrameTime = now;
        }
    }
    
    getPerformanceStats() {
        return {
            fps: this.fps,
            detectionActive: this.detectionActive,
            saluteDetected: this.saluteDetected,
            lastSaluteTime: this.lastSaluteTime,
            cameraActive: this.videoElement && !this.videoElement.paused
        };
    }
    
    // Manual activation for testing
    manualActivate() {
        console.log('🔧 Manual Vulcan salute activation');
        this.onVulcanSaluteDetected(0);
    }
    
    // Clean up
    destroy() {
        console.log('🧹 Cleaning up VulcanSaluteDetector');
        
        this.detectionActive = false;
        
        // Stop camera
        if (this.videoElement && this.videoElement.srcObject) {
            const stream = this.videoElement.srcObject;
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            this.videoElement.srcObject = null;
        }
        
        // Remove elements
        if (this.videoElement) {
            this.videoElement.remove();
        }
        
        if (this.canvasElement) {
            this.canvasElement.remove();
        }
        
        // Clean up hand landmarker
        if (this.handLandmarker) {
            this.handLandmarker.close();
            this.handLandmarker = null;
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VulcanSaluteDetector;
}

// Auto-initialize if in browser
if (typeof window !== 'undefined') {
    // Check if already initialized
    if (!window.vulcanSaluteDetector) {
        // Initialize when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            window.vulcanSaluteDetector = new VulcanSaluteDetector();
            console.log('🖖 VulcanSaluteDetector auto-initialized');
            
            // Add manual activation for testing
            window.addEventListener('keydown', (e) => {
                if (e.key === 'v' || e.key === 'V') {
                    window.vulcanSaluteDetector.manualActivate();
                }
            });
        });
    }
}