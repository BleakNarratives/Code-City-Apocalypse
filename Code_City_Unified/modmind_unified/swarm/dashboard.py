import logging

"""
🎛️ REAL-TIME SWARM DASHBOARD
Live monitoring of all agents, workbenches, and deployments
"""
import os
import json
import time
from datetime import datetime

class SwarmDashboard:
    def __init__(self):
        self.agents = [
            "eden", "jude", "psychology", "legal", "security",
            "tech_guru", "marketing", "reviewer", "coder"
        ]
        
        self.projects_dir = "projects"
        self.comms_dir = "comms"
        
        # Create dashboard directory
        os.makedirs("dashboard", exist_ok=True)
        
    def get_agent_status(self, agent_name):
        """Check if agent is running"""
        # Check if agent has recent activity
        result_file = f"{self.comms_dir}/{agent_name}_result.txt"
        if os.path.exists(result_file):
            mtime = os.path.getmtime(result_file)
            age = time.time() - mtime
            
            if age < 60:  # Active in last minute
                with open(result_file, 'r') as f:
                    last_result = f.read()[:100]
                return {
                    "status": "active",
                    "last_activity": datetime.fromtimestamp(mtime).strftime("%H:%M:%S"),
                    "last_result": last_result
                }
        
        # Check if agent file exists
        agent_file = f"agent_{agent_name}.py"
        if os.path.exists(agent_file):
            return {"status": "ready", "last_activity": "waiting"}
        else:
            return {"status": "offline", "last_activity": "never"}
            
    def get_eden_blueprints(self):
        """Get all blueprints from Eden"""
        blueprints = []
        blueprints_dir = "eden/blueprints"
        
        if os.path.exists(blueprints_dir):
            for file in os.listdir(blueprints_dir):
                if file.endswith(".json"):
                    filepath = os.path.join(blueprints_dir, file)
                    with open(filepath, 'r') as f:
                        blueprint = json.load(f)
                    blueprints.append({
                        "id": blueprint.get("id", "unknown"),
                        "name": blueprint.get("name", "Unnamed"),
                        "created": blueprint.get("created_at", "unknown"),
                        "components": len(blueprint.get("components", [])),
                        "status": "designed"
                    })
                    
        return blueprints
        
    def get_jude_builds(self):
        """Get all builds from Jude"""
        builds = []
        builds_dir = "jude/builds"
        
        if os.path.exists(builds_dir):
            for build in os.listdir(builds_dir):
                build_path = os.path.join(builds_dir, build)
                if os.path.isdir(build_path):
                    manifest_file = os.path.join(build_path, "deploy_manifest.json")
                    if os.path.exists(manifest_file):
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                        builds.append({
                            "id": manifest.get("build_id", build),
                            "blueprint": manifest.get("blueprint", "unknown"),
                            "components": manifest.get("components_built", 0),
                            "deployment_ready": manifest.get("deployment_ready", False),
                            "deploy_time": manifest.get("estimated_deploy_time", "unknown")
                        })
                        
        return builds
        
    def get_active_workbenches(self):
        """Get active workbenches"""
        workbenches = []
        workbench_dir = "eden/workbenches"
        
        if os.path.exists(workbench_dir):
            for workbench in os.listdir(workbench_dir):
                workbench_path = os.path.join(workbench_dir, workbench)
                if os.path.isdir(workbench_path):
                    config_file = os.path.join(workbench_path, "config.json")
                    if os.path.exists(config_file):
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                        workbenches.append({
                            "id": config.get("workbench_id", workbench),
                            "blueprint": config.get("for_blueprint", "unknown"),
                            "components": config.get("components_ready", 0),
                            "status": config.get("status", "unknown"),
                            "agents": config.get("agents_assigned", [])
                        })
                        
        return workbenches
        
    def generate_dashboard(self):
        """Generate HTML dashboard"""
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>🧠 SWARM DASHBOARD</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f23;
            color: #00ff00;
            padding: 20px;
            overflow-x: hidden;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { 
            text-align: center; 
            margin-bottom: 30px;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
        }
        .grid { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(0, 30, 0, 0.7);
            border: 1px solid #00ff00;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
        }
        .card h3 { 
            color: #00ff00;
            margin-bottom: 15px;
            border-bottom: 1px solid #00aa00;
            padding-bottom: 5px;
        }
        .status-active { color: #00ff00; }
        .status-ready { color: #ffff00; }
        .status-offline { color: #ff4444; }
        .agent-list { list-style: none; }
        .agent-list li { 
            padding: 8px;
            margin: 5px 0;
            background: rgba(0, 20, 0, 0.5);
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
        }
        .count { 
            font-size: 2.5em;
            text-align: center;
            margin: 10px 0;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }
        .subtitle { 
            text-align: center;
            color: #00aa00;
            margin-bottom: 20px;
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .deploy-btn {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            width: 100%;
        }
        .deploy-btn:hover {
            background: #00cc00;
            box-shadow: 0 0 15px #00ff00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 SWARM DASHBOARD</h1>
            <p class="subtitle">Real-time monitoring of Eden, Jude, and all specialized agents</p>
            <p>Last updated: <span id="updateTime">''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</span></p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🎯 AGENT STATUS</h3>
                <ul class="agent-list" id="agentStatus">
                    <!-- Filled by JavaScript -->
                </ul>
            </div>
            
            <div class="card">
                <h3>🧬 EDEN'S BLUEPRINTS</h3>
                <div class="count" id="blueprintCount">0</div>
                <div id="blueprintList">
                    <!-- Filled by JavaScript -->
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ JUDE'S BUILDS</h3>
                <div class="count" id="buildCount">0</div>
                <div id="buildList">
                    <!-- Filled by JavaScript -->
                </div>
            </div>
            
            <div class="card">
                <h3>🔧 ACTIVE WORKBENCHES</h3>
                <div class="count" id="workbenchCount">0</div>
                <div id="workbenchList">
                    <!-- Filled by JavaScript -->
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🚀 QUICK ACTIONS</h3>
            <button class="deploy-btn" onclick="deployLatest()">DEPLOY LATEST BUILD</button>
            <button class="deploy-btn" onclick="createSaaS()">CREATE NEW SAAS PROJECT</button>
            <button class="deploy-btn" onclick="createAIOrchestrator()">CREATE AI ORCHESTRATOR</button>
            <button class="deploy-btn" onclick="createWorkbench()">CREATE WORKBENCH SAAS</button>
        </div>
        
        <div class="card">
            <h3>📊 SYSTEM METRICS</h3>
            <p>Agents Online: <span id="onlineCount">0</span></p>
            <p>Total Components Built: <span id="componentCount">0</span></p>
            <p>Deployments Ready: <span id="deployReady">0</span></p>
            <p>Estimated Monthly Revenue (if deployed): <span id="revenueEstimate">$0</span></p>
        </div>
    </div>
    
    <script>
        function loadDashboard() {
            fetch('/dashboard_data')
                .then(response => response.json())
                .then(data => {
                    // Update agent status
                    const agentList = document.getElementById('agentStatus');
                    agentList.innerHTML = '';
                    let onlineCount = 0;
                    
                    for (const [agent, info] of Object.entries(data.agents)) {
                        const statusClass = 'status-' + info.status;
                        agentList.innerHTML += `
                            <li>
                                <strong>${agent}</strong>
                                <span class="${statusClass}">${info.status.toUpperCase()}</span>
                            </li>
                        `;
                        if (info.status === 'active') onlineCount++;
                    }
                    
                    // Update blueprint count
                    document.getElementById('blueprintCount').textContent = data.blueprints.length;
                    const blueprintList = document.getElementById('blueprintList');
                    blueprintList.innerHTML = '';
                    data.blueprints.slice(0, 3).forEach(bp => {
                        blueprintList.innerHTML += `<p>${bp.name}</p>`;
                    });
                    
                    // Update build count
                    document.getElementById('buildCount').textContent = data.builds.length;
                    const buildList = document.getElementById('buildList');
                    buildList.innerHTML = '';
                    data.builds.slice(0, 3).forEach(build => {
                        buildList.innerHTML += `<p>${build.id}</p>`;
                    });
                    
                    // Update workbench count
                    document.getElementById('workbenchCount').textContent = data.workbenches.length;
                    
                    // Update metrics
                    document.getElementById('onlineCount').textContent = onlineCount;
                    document.getElementById('componentCount').textContent = data.builds.reduce((sum, b) => sum + (b.components || 0), 0);
                    document.getElementById('deployReady').textContent = data.builds.filter(b => b.deployment_ready).length;
                    document.getElementById('revenueEstimate').textContent = '$' + (data.builds.length * 1000).toLocaleString();
                    
                    // Update time
                    document.getElementById('updateTime').textContent = new Date().toLocaleString();
                });
        }
        
        function deployLatest() {
            fetch('/deploy_latest')
                .then(response => response.json())
                .then(data => {
                    alert('Deployment initiated: ' + data.message);
                });
        }
        
        function createSaaS() {
            fetch('/create_saas')
                .then(response => response.json())
                .then(data => {
                    alert('SaaS project created: ' + data.message);
                    loadDashboard();
                });
        }
        
        function createAIOrchestrator() {
            fetch('/create_ai_orchestrator')
                .then(response => response.json())
                .then(data => {
                    alert('AI Orchestrator created: ' + data.message);
                    loadDashboard();
                });
        }
        
        function createWorkbench() {
            fetch('/create_workbench')
                .then(response => response.json())
                .then(data => {
                    alert('Workbench SaaS created: ' + data.message);
                    loadDashboard();
                });
        }
        
        // Initial load
        loadDashboard();
        
        // Refresh every 5 seconds
        setInterval(loadDashboard, 5000);
    </script>
</body>
</html>'''
        
        return html
        
    def generate_data_endpoint(self):
        """Generate JSON data for dashboard"""
        agents = {}
        for agent in self.agents:
            agents[agent] = self.get_agent_status(agent)
            
        data = {
            "agents": agents,
            "blueprints": self.get_eden_blueprints(),
            "builds": self.get_jude_builds(),
            "workbenches": self.get_active_workbenches(),
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(data)
        
    def run_web_dashboard(self):
        """Run dashboard as web server"""
        from fastapi import FastAPI
        import uvicorn
        
        app = FastAPI(title="Swarm Dashboard")
        
        @app.get("/")
        async def root():
            return {"message": "Swarm Dashboard API"}
            
        @app.get("/dashboard")
        async def dashboard():
            html = self.generate_dashboard()
            from fastapi.responses import HTMLResponse
            return HTMLResponse(content=html)
            
        @app.get("/dashboard_data")
        async def dashboard_data():
            data = self.generate_data_endpoint()
            import json
            return json.loads(data)
            
        @app.get("/deploy_latest")
        async def deploy_latest():
            # Find latest build
            builds_dir = "jude/builds"
            if os.path.exists(builds_dir):
                builds = sorted(os.listdir(builds_dir))
                if builds:
                    latest = os.path.join(builds_dir, builds[-1], "deploy.sh")
                    if os.path.exists(latest):
                        import subprocess
                        result = subprocess.run(["bash", latest], capture_output=True, text=True)
                        return {"message": f"Deployment initiated for {builds[-1]}", "output": result.stdout}
            
            return {"message": "No builds found"}
            
        @app.get("/create_saas")
        async def create_saas():
            with open("tasks/eden_task.txt", 'w') as f:
                f.write("Create a full-stack SaaS platform for AI agent management with autonomous deployment")
            return {"message": "SaaS project requested from Eden"}
            
        @app.get("/create_ai_orchestrator")
        async def create_ai_orchestrator():
            with open("tasks/eden_task.txt", 'w') as f:
                f.write("Create an AI orchestrator that can manage 100+ specialized agents with zero configuration")
            return {"message": "AI Orchestrator requested from Eden"}
            
        @app.get("/create_workbench")
        async def create_workbench():
            with open("tasks/eden_task.txt", 'w') as f:
                f.write("Create an intelligent development workbench that auto-generates code, tests, and deploys")
            return {"message": "Workbench SaaS requested from Eden"}
            
        logging.info("🚀 Starting Swarm Dashboard on http://localhost:8000")
        logging.info("📊 Open browser to: http://localhost:8000/dashboard")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    def run_cli_dashboard(self):
        """Run dashboard in CLI mode (for Termux)"""
        import curses
        
        def main(stdscr):
            curses.curs_set(0)
            stdscr.nodelay(1)
            stdscr.timeout(1000)
            
            while True:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Header
                stdscr.addstr(0, 0, "🧠 SWARM DASHBOARD", curses.A_BOLD)
                stdscr.addstr(1, 0, "=" * width)
                
                # Agents status
                stdscr.addstr(3, 0, "AGENTS:")
                row = 4
                for agent in self.agents[:9]:  # Limit for screen
                    status = self.get_agent_status(agent)
                    color = curses.color_pair(2 if status["status"] == "active" else 1)
                    stdscr.addstr(row, 2, f"{agent:15} [{status['status']:^7}]", color)
                    row += 1
                
                # Blueprints
                blueprints = self.get_eden_blueprints()
                stdscr.addstr(row + 1, 0, f"EDEN'S BLUEPRINTS: {len(blueprints)}")
                
                # Builds
                builds = self.get_jude_builds()
                stdscr.addstr(row + 2, 0, f"JUDE'S BUILDS: {len(builds)}")
                
                # Workbenches
                workbenches = self.get_active_workbenches()
                stdscr.addstr(row + 3, 0, f"ACTIVE WORKBENCHES: {len(workbenches)}")
                
                # Instructions
                stdscr.addstr(height - 2, 0, "Q: Quit | R: Refresh | D: Deploy latest")
                
                stdscr.refresh()
                
                # Check for input
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('r') or key == ord('R'):
                    continue
                elif key == ord('d') or key == ord('D'):
                    # Find and deploy latest build
                    pass
                    
        curses.wrapper(main)

if __name__ == "__main__":
    dashboard = SwarmDashboard()
    
    # Check if we can run web dashboard
    try:
        import fastapi
        dashboard.run_web_dashboard()
    except ImportError:
        logging.info("📟 FastAPI not available, running CLI dashboard...")
        try:
            dashboard.run_cli_dashboard()
        except:
            logging.info("📊 Dashboard data:")
            logging.info(f"Agents: {len(dashboard.agents)}")
            logging.info(f"Blueprints: {len(dashboard.get_eden_blueprints())}")
            logging.info(f"Builds: {len(dashboard.get_jude_builds())}")
            logging.info(f"Workbenches: {len(dashboard.get_active_workbenches())}")
