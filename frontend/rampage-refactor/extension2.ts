import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let panel: vscode.WebviewPanel | undefined;

    const deployAgentCmd = vscode.commands.registerCommand('rampage.deployAgent', async () => {
        if (!panel) {
            panel = vscode.window.createWebviewPanel(
                'rampageView',
                'Rampage City',
                vscode.ViewColumn.Beside,
                { enableScripts: true }
            );
            panel.webview.html = getWebviewContent();
            panel.onDidDispose(() => panel = undefined);
        } else {
            panel.reveal();
        }

        // Spawn initial monster from diagnostics
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const diagnostics = vscode.languages.getDiagnostics(editor.document.uri);
            if (diagnostics.length > 0) {
                const firstError = diagnostics[0];
                panel.webview.postMessage({
                    type: 'SPAWN_MONSTER',
                    line: firstError.range.start.line + 1,
                    msg: firstError.message,
                    height: Math.max(20, firstError.message.length * 2),
                    color: '#ff4444'
                });
            }
        }
    });

    // Listen for new errors
    vscode.workspace.onDidChangeTextDocument(e => {
        if (panel) {
            const diagnostics = vscode.languages.getDiagnostics(e.document.uri);
            if (diagnostics.length > 0) {
                const firstError = diagnostics[0];
                panel.webview.postMessage({
                    type: 'SPAWN_MONSTER', 
                    line: firstError.range.start.line + 1,
                    msg: firstError.message,
                    height: Math.max(20, firstError.message.length * 2),
                    color: '#ff0000'
                });
            }
        }
    });

    context.subscriptions.push(deployAgentCmd);
}

function getWebviewContent(): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #000; }
        #hud { position: absolute; top: 10px; left: 10px; color: white; z-index: 100; }
        button { background: #ff4444; color: white; border: none; padding: 8px 16px; cursor: pointer; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.165.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="hud">
        <button onclick="deployAgent()">🚀 DEPLOY AGENT</button>
        <div id="status">Ready</div>
    </div>
    <div id="city"></div>
    
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x05050a);
        
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 100;
        
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('city').appendChild(renderer.domElement);
        
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        
        // Ground
        const ground = new THREE.Mesh(
            new THREE.PlaneGeometry(200, 200),
            new THREE.MeshStandardMaterial({ color: 0x111133 })
        );
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);
        
        // Lighting
        scene.add(new THREE.AmbientLight(0x404040));
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(50, 50, 50);
        scene.add(light);
        
        let monsters = [];
        let agentActive = false;
        
        // Message handling
        window.addEventListener('message', event => {
            const data = event.data;
            if (data.type === 'SPAWN_MONSTER') {
                spawnMonster(data);
            }
        });
        
        function spawnMonster(data) {
            const geometry = new THREE.ConeGeometry(5, data.height, 6);
            const material = new THREE.MeshStandardMaterial({ 
                color: data.color,
                emissive: data.color,
                emissiveIntensity: 0.3
            });
            
            const monster = new THREE.Mesh(geometry, material);
            monster.position.set(
                (Math.random() - 0.5) * 100,
                data.height / 2,
                (Math.random() - 0.5) * 100
            );
            monster.userData = { line: data.line, msg: data.msg };
            
            scene.add(monster);
            monsters.push(monster);
            
            document.getElementById('status').innerHTML = \`🐛 Bug at line \${data.line}: \${data.msg}\`;
        }
        
        function deployAgent() {
            if (agentActive || monsters.length === 0) return;
            
            agentActive = true;
            document.getElementById('status').innerHTML = '🤖 Agent deployed! Fixing bugs...';
            
            // Simulate AI fixing
            setTimeout(() => {
                if (monsters.length > 0) {
                    const monster = monsters.pop();
                    scene.remove(monster);
                    document.getElementById('status').innerHTML = \`✅ Fixed bug: \${monster.userData.msg}\`;
                }
                agentActive = false;
            }, 2000);
        }
        
        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            
            monsters.forEach(monster => {
                monster.rotation.y += 0.01;
                monster.position.y = (Math.sin(Date.now() * 0.001) * 5) + (monster.geometry.parameters.height / 2);
            });
            
            controls.update();
            renderer.render(scene, camera);
        }
        
        animate();
        
        // Handle resize
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>`;
}

export function deactivate() {}