Now let me create the modern React Code City component with a beautiful UI:
Action: file_editor create /app/frontend/src/components/CodeCity.js --file-text "import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CodeCity = () => {
  const canvasRef = useRef(null);
  const [cityData, setCityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [customPath, setCustomPath] = useState('');
  const [showMenu, setShowMenu] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const cityRef = useRef(null);

  useEffect(() => {
    // Load current codebase on mount
    loadCurrentCodebase();
  }, []);

  useEffect(() => {
    if (cityData && canvasRef.current && !isPaused) {
      initializeCity(cityData);
    }
  }, [cityData, isPaused]);

  const loadCurrentCodebase = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/scan-current`);
      setCityData(response.data);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error loading codebase:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCustomCodebase = async () => {
    if (!customPath) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/scan-codebase`, {
        path: customPath,
        max_files: 500
      });
      setCityData(response.data);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error scanning codebase:', error);
      alert('Error scanning codebase. Make sure the path is valid and accessible.');
    } finally {
      setLoading(false);
    }
  };

  const initializeCity = (data) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    class City {
      constructor(buildings, stats) {
        this.buildings = buildings.map((b, i) => ({
          ...b,
          x: 100 + (i % 15) * 80 + Math.random() * 20,
          y: height - 150 - b.height * 10,
          originalY: height - 150 - b.height * 10,
          shake: 0,
          floatOffset: Math.random() * Math.PI * 2
        }));
        this.stats = stats;
        this.particles = [];
        this.time = 0;
        this.monsters = [];
      }

      spawnMonster() {
        this.monsters.push({
          x: Math.random() * width,
          y: 100 + Math.random() * 100,
          vx: (Math.random() - 0.5) * 2,
          vy: (Math.random() - 0.5) * 2,
          size: 15 + Math.random() * 10,
          color: '#ff0066',
          rotation: 0
        });
      }

      damageBuilding(building) {
        building.health = Math.max(0, building.health - 20);
        this.createExplosion(building.x + building.width * 5, building.y);
      }

      repairBuilding(building) {
        building.health = 100;
        building.flaw_score = 0.1;
        this.createSparkles(building.x + building.width * 5, building.y);
      }

      createExplosion(x, y) {
        for (let i = 0; i < 20; i++) {
          this.particles.push({
            x, y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6 - 2,
            life: 40,
            maxLife: 40,
            color: ['#ff0066', '#ff6600', '#ffff00'][Math.floor(Math.random() * 3)],
            size: 2 + Math.random() * 3
          });
        }
      }

      createSparkles(x, y) {
        for (let i = 0; i < 30; i++) {
          this.particles.push({
            x, y,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4 - 3,
            life: 50,
            maxLife: 50,
            color: ['#00ff41', '#00ffff', '#ffffff'][Math.floor(Math.random() * 3)],
            size: 1 + Math.random() * 2
          });
        }
      }

      draw() {
        // Beautiful gradient background
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, '#0a0e27');
        gradient.addColorStop(0.5, '#1a1f3a');
        gradient.addColorStop(1, '#0f1419');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);

        // Animated stars
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        for (let i = 0; i < 50; i++) {
          const x = (i * 137.5) % width;
          const y = (i * 73.2) % (height * 0.4);
          const twinkle = Math.sin(this.time * 0.01 + i) * 0.5 + 0.5;
          ctx.globalAlpha = twinkle * 0.8;
          ctx.fillRect(x, y, 2, 2);
        }
        ctx.globalAlpha = 1;

        // Ground with glow
        const groundGradient = ctx.createLinearGradient(0, height - 150, 0, height);
        groundGradient.addColorStop(0, 'rgba(0, 255, 65, 0.1)');
        groundGradient.addColorStop(1, 'rgba(0, 255, 65, 0.3)');
        ctx.fillStyle = groundGradient;
        ctx.fillRect(0, height - 150, width, 150);

        // Grid lines with glow effect
        ctx.strokeStyle = 'rgba(0, 255, 65, 0.15)';
        ctx.lineWidth = 1;
        for (let i = 0; i < width; i += 50) {
          ctx.beginPath();
          ctx.moveTo(i, height - 150);
          ctx.lineTo(i, height);
          ctx.stroke();
        }

        // Draw buildings with 3D effect
        this.buildings.forEach(building => {
          const floatY = Math.sin(this.time * 0.02 + building.floatOffset) * 2;
          building.shake = building.health < 100 ? Math.sin(this.time * 0.3) * 2 : 0;
          
          const bWidth = building.width * 10;
          const bHeight = building.height * 10;
          const x = building.x + building.shake;
          const y = building.y + floatY;

          // 3D shadow
          ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
          ctx.fillRect(x + 5, y + 5, bWidth, bHeight);

          // Building glow
          if (building.health > 50) {
            ctx.shadowBlur = 20;
            ctx.shadowColor = building.color;
          }

          // Main building
          ctx.fillStyle = building.color;
          ctx.fillRect(x, y, bWidth, bHeight);

          ctx.shadowBlur = 0;

          // Windows with depth
          const windowColor = building.health > 50 ? '#ffff00' : '#ff6600';
          ctx.fillStyle = windowColor;
          for (let wx = 5; wx < bWidth - 5; wx += 12) {
            for (let wy = 5; wy < bHeight - 5; wy += 15) {
              if (Math.random() > 0.2) {
                // Window glow
                ctx.shadowBlur = 5;
                ctx.shadowColor = windowColor;
                ctx.fillRect(x + wx, y + wy, 6, 8);
                ctx.shadowBlur = 0;
              }
            }
          }

          // Health bar with glassmorphism
          if (building.health < 100) {
            // Background
            ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
            ctx.fillRect(x - 2, y - 15, bWidth + 4, 8);
            
            // Health
            const healthColor = building.health > 50 ? '#00ff41' : '#ff6600';
            ctx.fillStyle = healthColor;
            ctx.fillRect(x, y - 13, bWidth * (building.health / 100), 4);
            
            // Border
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.lineWidth = 1;
            ctx.strokeRect(x - 2, y - 15, bWidth + 4, 8);
          }

          // Flaw indicator
          if (building.flaw_score > 0.5) {
            ctx.fillStyle = '#ff0066';
            ctx.font = '8px monospace';
            ctx.fillText(building.flaw_type.toUpperCase(), x, y - 20);
          }

          // Top edge highlight
          ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
          ctx.fillRect(x, y, bWidth, 2);
        });

        // Draw monsters with glow
        this.monsters.forEach(monster => {
          monster.rotation += 0.05;
          
          ctx.save();
          ctx.translate(monster.x, monster.y);
          ctx.rotate(monster.rotation);
          
          // Glow effect
          ctx.shadowBlur = 20;
          ctx.shadowColor = monster.color;
          
          // Body
          ctx.fillStyle = monster.color;
          ctx.beginPath();
          ctx.arc(0, 0, monster.size, 0, Math.PI * 2);
          ctx.fill();
          
          ctx.shadowBlur = 0;
          
          // Eyes
          ctx.fillStyle = '#ffff00';
          ctx.fillRect(-6, -4, 4, 4);
          ctx.fillRect(2, -4, 4, 4);
          
          // Teeth
          ctx.fillStyle = '#ffffff';
          for (let i = -monster.size; i < monster.size; i += 5) {
            ctx.fillRect(i, 2, 3, 4);
          }
          
          ctx.restore();
        });

        // Draw particles
        this.particles.forEach(particle => {
          const alpha = particle.life / particle.maxLife;
          ctx.globalAlpha = alpha;
          ctx.shadowBlur = 10;
          ctx.shadowColor = particle.color;
          ctx.fillStyle = particle.color;
          ctx.fillRect(particle.x - particle.size / 2, particle.y - particle.size / 2, particle.size, particle.size);
        });
        ctx.globalAlpha = 1;
        ctx.shadowBlur = 0;

        // Scan lines (subtle)
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        for (let i = 0; i < height; i += 3) {
          ctx.fillRect(0, i, width, 1);
        }
      }

      update() {
        this.time++;

        // Update monsters
        this.monsters.forEach(monster => {
          monster.x += monster.vx;
          monster.y += monster.vy;
          
          if (monster.x < 0 || monster.x > width) monster.vx *= -1;
          if (monster.y < 0 || monster.y > height - 150) monster.vy *= -1;
        });

        // Update particles
        this.particles = this.particles.filter(p => {
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.2;
          p.life--;
          return p.life > 0;
        });
      }

      animate() {
        this.update();
        this.draw();
      }
    }

    const city = new City(data.buildings, data.stats);
    cityRef.current = city;

    const animate = () => {
      if (!isPaused) {
        city.animate();
      }
      requestAnimationFrame(animate);
    };
    animate();
  };

  return (
    <div className=\"min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900\">
      {/* Menu Button */}
      <button
        onClick={() => setShowMenu(!showMenu)}
        className=\"fixed top-4 right-4 z-50 bg-black/40 backdrop-blur-md border border-green-500/30 text-green-400 px-6 py-3 rounded-lg hover:bg-green-500/20 transition-all duration-300 shadow-lg shadow-green-500/20\"
        data-testid=\"menu-button\"
      >
        ☰ Menu
      </button>

      {/* Menu Panel */}
      {showMenu && (
        <div className=\"fixed top-20 right-4 z-50 bg-black/60 backdrop-blur-xl border border-green-500/30 rounded-xl p-6 shadow-2xl shadow-green-500/20 w-80\"
             data-testid=\"menu-panel\">
          <h2 className=\"text-2xl font-bold text-green-400 mb-4 flex items-center gap-2\">
            🏙️ Code City Control
          </h2>
          
          {/* Stats */}
          {stats && (
            <div className=\"mb-6 space-y-2 text-sm\">
              <div className=\"flex justify-between text-cyan-400\">
                <span>Files:</span>
                <span className=\"font-bold text-yellow-400\">{stats.total_files}</span>
              </div>
              <div className=\"flex justify-between text-cyan-400\">
                <span>Lines:</span>
                <span className=\"font-bold text-yellow-400\">{stats.total_lines.toLocaleString()}</span>
              </div>
              <div className=\"flex justify-between text-cyan-400\">
                <span>Scan Time:</span>
                <span className=\"font-bold text-yellow-400\">{stats.scan_time?.toFixed(2)}s</span>
              </div>
            </div>
          )}

          {/* Controls */}
          <div className=\"space-y-3\">
            <button
              onClick={() => setIsPaused(!isPaused)}
              className=\"w-full bg-purple-500/20 border border-purple-400/50 text-purple-300 px-4 py-2 rounded-lg hover:bg-purple-500/40 transition-all\"
              data-testid=\"pause-button\"
            >
              {isPaused ? '▶️ Resume' : '⏸️ Pause'}
            </button>

            <button
              onClick={() => cityRef.current?.spawnMonster()}
              className=\"w-full bg-red-500/20 border border-red-400/50 text-red-300 px-4 py-2 rounded-lg hover:bg-red-500/40 transition-all\"
              data-testid=\"spawn-monster-button\"
            >
              👹 Spawn Monster
            </button>

            <button
              onClick={loadCurrentCodebase}
              className=\"w-full bg-blue-500/20 border border-blue-400/50 text-blue-300 px-4 py-2 rounded-lg hover:bg-blue-500/40 transition-all\"
              data-testid=\"refresh-button\"
            >
              🔄 Refresh
            </button>
          </div>

          {/* Custom Path */}
          <div className=\"mt-6 pt-6 border-t border-green-500/20\">
            <label className=\"block text-green-400 text-sm mb-2\">
              Scan Custom Path:
            </label>
            <input
              type=\"text\"
              value={customPath}
              onChange={(e) => setCustomPath(e.target.value)}
              placeholder=\"/path/to/your/code\"
              className=\"w-full bg-black/40 border border-green-500/30 text-green-300 px-3 py-2 rounded-lg mb-2 focus:outline-none focus:border-green-500\"
              data-testid=\"custom-path-input\"
            />
            <button
              onClick={loadCustomCodebase}
              disabled={!customPath || loading}
              className=\"w-full bg-green-500/20 border border-green-400/50 text-green-300 px-4 py-2 rounded-lg hover:bg-green-500/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed\"
              data-testid=\"scan-custom-button\"
            >
              🔍 Scan
            </button>
          </div>
        </div>
      )}

      {/* Main Canvas */}
      <div className=\"flex items-center justify-center min-h-screen p-8\">
        <div className=\"relative\">
          {loading && (
            <div className=\"absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm rounded-xl z-10\">
              <div className=\"text-green-400 text-xl font-mono\">
                Scanning codebase...
              </div>
            </div>
          )}
          
          <canvas
            ref={canvasRef}
            width={1400}
            height={800}
            className=\"border-2 border-green-500/30 rounded-xl shadow-2xl shadow-green-500/20\"
            data-testid=\"code-city-canvas\"
          />
          
          {/* Info Bar */}
          <div className=\"mt-4 bg-black/40 backdrop-blur-md border border-green-500/30 rounded-lg p-4 text-green-400 font-mono text-sm\">
            <div className=\"flex justify-between items-center\">
              <span>🎮 Code City Retro Visualization</span>
              {stats && <span>📂 {stats.scanned_path}</span>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeCity;
"
Observation: Create successful: /app/frontend/src/components/CodeCity.js