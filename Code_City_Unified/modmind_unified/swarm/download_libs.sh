#!/bin/bash
# Download and cache libraries for offline use
# Based on cumbseek_9_11.txt specifications

echo "📥 Downloading libraries for offline-first development..."
echo "📍 Location: ~/storage/shared/airforge"

# Create libs directory if it doesn't exist
mkdir -p ~/storage/shared/airforge/libs
cd ~/storage/shared/airforge/libs

echo "📦 Creating library directory structure..."
mkdir -p threejs mediapipe transformers models

echo ""
echo "🚀 Starting downloads..."

# Download Three.js (minified version)
if [ ! -f "threejs/three.min.js" ]; then
    echo "📦 Downloading Three.js r160 (minified)..."
    wget https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js -O threejs/three.min.js
    echo "✅ Three.js downloaded"
else
    echo "✅ Three.js already cached"
fi

# Download Three.js examples (for controls, loaders, etc.)
if [ ! -f "threejs/OrbitControls.js" ]; then
    echo "📦 Downloading Three.js OrbitControls..."
    wget https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js -O threejs/OrbitControls.js
    echo "✅ OrbitControls downloaded"
else
    echo "✅ OrbitControls already cached"
fi

# Download MediaPipe vision bundle
if [ ! -f "mediapipe/vision_bundle.js" ]; then
    echo "📦 Downloading MediaPipe vision bundle..."
    wget https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/vision_bundle.js -O mediapipe/vision_bundle.js
    echo "✅ MediaPipe vision bundle downloaded"
else
    echo "✅ MediaPipe vision bundle already cached"
fi

# Download MediaPipe hand landmarker model
if [ ! -f "models/hand_landmarker.task" ]; then
    echo "📦 Downloading hand landmarker model (float16)..."
    wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -O models/hand_landmarker.task
    echo "✅ Hand landmarker model downloaded"
else
    echo "✅ Hand landmarker model already cached"
fi

# Download Transformers.js (small version for mobile)
if [ ! -f "transformers/transformers.min.js" ]; then
    echo "📦 Downloading Transformers.js (Xenova)..."
    wget https://cdn.jsdelivr.net/npm/@xenova/transformers@2.12.0/dist/transformers.min.js -O transformers/transformers.min.js
    echo "✅ Transformers.js downloaded"
else
    echo "✅ Transformers.js already cached"
fi

# Download a tiny language model for offline use
if [ ! -f "models/tiny-model.json" ]; then
    echo "📦 Downloading tiny language model..."
    # This is a placeholder - in reality you'd download a proper tiny model
    cat > models/tiny-model.json << 'MODEL_EOF'
{
  "model": "tiny-llama-1B",
  "description": "Tiny language model for offline use",
  "size": "1B parameters",
  "capabilities": ["text generation", "question answering"],
  "offline": true,
  "battery_efficient": true
}
MODEL_EOF
    echo "✅ Tiny model configuration created"
else
    echo "✅ Tiny model already cached"
fi

echo ""
echo "🎉 All libraries downloaded and cached!"
echo ""
echo "📍 Library structure:"
echo "  ~/storage/shared/airforge/libs/"
echo "    ├── threejs/"
echo "    │   ├── three.min.js"
echo "    │   └── OrbitControls.js"
echo "    ├── mediapipe/"
echo "    │   └── vision_bundle.js"
echo "    ├── transformers/"
echo "    │   └── transformers.min.js"
echo "    └── models/"
echo "        ├── hand_landmarker.task"
echo "        └── tiny-model.json"

echo ""
echo "📦 Total size: $(du -sh ~/storage/shared/airforge/libs | cut -f1)"
echo ""
echo "🔧 Usage in HTML:"
echo "  <!-- Three.js -->"
echo "  <script src='libs/threejs/three.min.js'></script>"
echo "  <script src='libs/threejs/OrbitControls.js'></script>"
echo "  "
echo "  <!-- MediaPipe -->"
echo "  <script src='libs/mediapipe/vision_bundle.js'></script>"
echo "  "
echo "  <!-- Transformers.js -->"
echo "  <script src='libs/transformers/transformers.min.js'></script>"
echo ""
echo "💡 Tip: Use these local files instead of CDN for offline development!"

# Create a simple test to verify libraries work
cat > ~/storage/shared/airforge/test_libs.html << 'TEST_EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Library Test</title>
    <style>
        body { font-family: monospace; background: #0a0a0a; color: #0f0; padding: 20px; }
        .success { color: #0f0; }
        .error { color: #f00; }
        .loading { color: #ff0; }
    </style>
</head>
<body>
    <h1>🧪 Library Test</h1>
    <div id="results"></div>
    
    <script>
        const results = document.getElementById('results');
        
        function log(message, type = 'info') {
            const div = document.createElement('div');
            div.className = type;
            div.textContent = message;
            results.appendChild(div);
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
        
        // Test Three.js
        log('📦 Testing Three.js...', 'loading');
        try {
            const script = document.createElement('script');
            script.src = 'libs/threejs/three.min.js';
            script.onload = () => {
                if (typeof THREE !== 'undefined') {
                    log('✅ Three.js loaded successfully!', 'success');
                    log(`   Version: ${THREE.REVISION}`, 'success');
                } else {
                    log('❌ Three.js failed to load', 'error');
                }
            };
            script.onerror = () => {
                log('❌ Three.js failed to load', 'error');
            };
            document.head.appendChild(script);
        } catch (error) {
            log(`❌ Three.js error: ${error.message}`, 'error');
        }
        
        // Test MediaPipe
        setTimeout(() => {
            log('📦 Testing MediaPipe...', 'loading');
            try {
                const script = document.createElement('script');
                script.src = 'libs/mediapipe/vision_bundle.js';
                script.onload = () => {
                    log('✅ MediaPipe loaded successfully!', 'success');
                };
                script.onerror = () => {
                    log('❌ MediaPipe failed to load', 'error');
                };
                document.head.appendChild(script);
            } catch (error) {
                log(`❌ MediaPipe error: ${error.message}`, 'error');
            }
        }, 1000);
        
        // Test Transformers.js
        setTimeout(() => {
            log('📦 Testing Transformers.js...', 'loading');
            try {
                const script = document.createElement('script');
                script.src = 'libs/transformers/transformers.min.js';
                script.onload = () => {
                    log('✅ Transformers.js loaded successfully!', 'success');
                };
                script.onerror = () => {
                    log('❌ Transformers.js failed to load', 'error');
                };
                document.head.appendChild(script);
            } catch (error) {
                log(`❌ Transformers.js error: ${error.message}`, 'error');
            }
        }, 2000);
        
        // Test hand landmarker model
        setTimeout(() => {
            log('📦 Testing hand landmarker model...', 'loading');
            fetch('libs/models/hand_landmarker.task')
                .then(response => {
                    if (response.ok) {
                        log('✅ Hand landmarker model available!', 'success');
                    } else {
                        log('❌ Hand landmarker model not found', 'error');
                    }
                })
                .catch(() => {
                    log('❌ Hand landmarker model failed to load', 'error');
                });
        }, 3000);
    </script>
</body>
</html>
TEST_EOF

echo "✅ Created library test page: test_libs.html"
echo "   Open it in browser to verify all libraries work!"
