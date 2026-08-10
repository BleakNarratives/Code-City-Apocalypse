import * as vscode from 'vscode';
import * as THREE from 'three';

export function activate(context: vscode.ExtensionContext) {
  let panel: vscode.WebviewPanel | undefined;

  const cmd = vscode.commands.registerCommand('rampage.deployAgent', async () => {
    if (!panel) {
      panel = vscode.window.createWebviewPanel(
        'rampageView',
        'Mayor’s City',
        vscode.ViewColumn.Beside,
        { enableScripts: true }
      );
      panel.webview.html = getWebviewContent();
      panel.onDidDispose(() => (panel = undefined));
    } else panel.reveal();

    // Mayor’s Tower - your active file
    const editor = vscode.window.activeTextEditor;
    if (editor) {
      const diag = await vscode.languages.getDiagnostics(editor.document.uri);
      if (diag.length > 0) {
        const err = diag[0];
        panel.webview.postMessage({
          type: 'SPAWN_MAYOR_TOWER',
          line: err.range.start.line + 1,
          msg: err.message,
          height: Math.max(50, err.source?.length || 100), // Taller mayor tower
          color: '#ffd700' // Gold for the mayor
        });
      }
    }
  });

  // Monster spawn on change
  vscode.workspace.onDidChangeTextDocument((e) => {
    if (panel) {
      const diag = vscode.languages.getDiagnostics(e.document.uri);
      if (diag.length > 0) {
        const first = diag[0];
        panel.webview.postMessage({
          type: 'SPAWN_MONSTER',
          line: first.range.start.line + 1,
          msg: first.message,
          height: Math.random() * 100 + 20,
          color: '#ff4444'
        });
      }
    }
  });

  context.subscriptions.push(cmd);
}

function getWebviewContent() {
  return `
    <!doctype html>
    <html>
    <head><style>body{margin:0;background:#0a0a0a;}canvas{width:100%;height:100vh;}</style></head>
    <body>
    <script type=module>
      import * as THREE from 'https://unpkg.com/three@0.165.0/build/three.module.js?module';
      import { OrbitControls } from 'https://unpkg.com/three@0.165.0/examples/jsm/controls/OrbitControls.js?module';

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x05050a);
      const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 150;
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);
      new OrbitControls(camera, renderer.domElement);

      // Ground
      const g = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshBasicMaterial({ color: 0x111122 }));
      g.rotation.x = -Math.PI / 2;
      scene.add(g);

      // Lights
      scene.add(new THREE.AmbientLight(0x404040));
      scene.add(new THREE.DirectionalLight(0xffffff, 0.5).position.set(1, 1, 1));

      const monsters = [];
      const mayorTower = null;

      window.addEventListener('message', (e) => {
        const data = e.data;
        if (data.type === 'SPAWN_MONSTER') {
          const m = new THREE.Mesh(
            new THREE.BoxGeometry(5, data.height, 5),
            new THREE.MeshBasicMaterial({ color: data.color, transparent: true, opacity: 0.8 })
          );
          m.position.y = data.height / 2 + 1;
          m.position.x = (data.line % 15) - 7;
          m.position.z = (data.line % 18) - 9;
          m.userData = { msg: data.msg };
          scene.add(m);
          monsters.push(m);
        } else if (data.type === 'SPAWN_MAYOR_TOWER') {
          if (mayorTower) scene.remove(mayorTower);
          const mt = new THREE.Mesh(
            new THREE.BoxGeometry(10, data.height, 10),
            new THREE.MeshBasicMaterial({ color: data.color, emissive: data.color, emissiveIntensity: 0.3 })
          );
          mt.position.y = data.height / 2 + 5;
          mt.position.x = 0;
          mt.position.z = 0;
          mt.userData = { msg: data.msg };
          scene.add(mt);
        } else if (data.type === 'FIX') {
          if (monsters.length) {
            const m = monsters.shift();
            m.material.color.set('#00ff44');
            m.scale.y = 1.5;
            m.userData = { fixed: true };
            setTimeout(() => scene.remove(m), 1000);
          }
        }
      });

      function animate() {
        requestAnimationFrame(animate);
        monsters.forEach((m) => {
          if (m.userData.fixed) return;
          m.rotation.y += 0.02;
          m.position.y += Math.sin(Date.now() * 0.001 + m.id) * 0.1;
        });
        renderer.render(scene, camera);
      }
      animate();

      // Deploy agent button
      const btn = document.createElement('button');
      btn.textContent = 'Mayor Deploy Agent';
      btn.style.cssText = 'position:absolute;top:10px;left:10px;color:white;background:#ffd700;padding:5px;border-radius:3px';
      btn.onclick = () => {
        window.parent.postMessage({ type: 'FIX', line: 1 }, '*');
        alert('Mayor sent agents! Fixing... (Copilot stub)');
      };
      document.body.appendChild(btn);
    </script>
    </body>
    </html>`;
}

export function deactivate() {}