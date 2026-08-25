import logging

"""
REAL ECOSYSTEM INTEGRATOR - Direct integration with your existing projects
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class RealEcosystemIntegrator:
    """Direct integration with your actual project structure"""
    
    def __init__(self, syntax_core):
        self.syntax = syntax_core
        self.ecosystem_manifest = self._load_ecosystem_manifest()
        self.active_connections = {}
        
    def _load_ecosystem_manifest(self) -> Dict:
        """Load from your actual project structure or create initial manifest"""
        manifest_path = Path(__file__).parent.parent / "config" / "ecosystem_manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        
        # Create initial manifest based on typical project structure
        base_path = Path("..")  # Root directory containing your projects
        manifest = {"projects": {}}
        
        # Auto-discover projects in parent directory
        for item in base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                manifest["projects"][item.name] = {
                    "path": str(item),
                    "type": self._infer_project_type(item),
                    "status": self._assess_project_status(item),
                    "tech_stack": self._detect_tech_stack(item),
                    "integration_points": self._discover_integration_points(item)
                }
        
        # Save the discovered manifest
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
            
        return manifest
    
    def _infer_project_type(self, project_path: Path) -> str:
        """Infer project type from structure and files"""
        if (project_path / "package.json").exists():
            return "frontend"
        elif (project_path / "requirements.txt").exists() or (project_path / "pyproject.toml").exists():
            return "backend"
        elif (project_path / "Dockerfile").exists():
            return "service"
        elif any(project_path.glob("*.md")):
            return "documentation"
        else:
            return "unknown"
    
    def _assess_project_status(self, project_path: Path) -> str:
        """Assess project status based on git and file activity"""
        try:
            # Check git status
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cr'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                return "active"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check for recent file modifications
        recent_files = list(project_path.rglob("*"))
        if recent_files:
            return "development"
        
        return "planning"
    
    def _detect_tech_stack(self, project_path: Path) -> List[str]:
        """Detect technologies used in the project"""
        tech_stack = []
        
        # Check for common tech stack indicators
        tech_indicators = {
            "python": ["requirements.txt", "pyproject.toml", "*.py"],
            "react": ["package.json", "src/", "public/"],
            "fastapi": ["main.py", "app.py", "fastapi"],
            "typescript": ["tsconfig.json", "*.ts", "*.tsx"],
            "docker": ["Dockerfile", "docker-compose.yml"],
            "postgres": ["postgres", "pg", "psycopg2"],
            "neo4j": ["neo4j", "cypher"],
            "llm": ["openai", "anthropic", "llama", "ollama"]
        }
        
        for tech, indicators in tech_indicators.items():
            for indicator in indicators:
                if indicator.endswith('/'):  # Directory
                    if (project_path / indicator).exists():
                        tech_stack.append(tech)
                        break
                else:  # File or pattern
                    if list(project_path.rglob(indicator)):
                        tech_stack.append(tech)
                        break
        
        return list(set(tech_stack))  # Remove duplicates
    
    def _discover_integration_points(self, project_path: Path) -> List[Dict]:
        """Scan actual code for API endpoints and integration points"""
        integration_points = []
        
        # Scan Python files for FastAPI routes
        for py_file in project_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find FastAPI route decorators
                routes = re.findall(r'@.*?\.(get|post|put|delete)\(["\']([^"\']+)["\']', content)
                for method, path in routes:
                    integration_points.append({
                        "file": str(py_file.relative_to(project_path)),
                        "method": method.upper(),
                        "path": path,
                        "service": project_path.name,
                        "type": "api_endpoint"
                    })
                
                # Find function definitions that could be integration points
                functions = re.findall(r'def\s+(\w+).*?:', content)
                for func in functions:
                    if any(keyword in func.lower() for keyword in ['api', 'route', 'endpoint', 'handler', 'integrate']):
                        integration_points.append({
                            "file": str(py_file.relative_to(project_path)),
                            "method": "FUNCTION",
                            "path": func,
                            "service": project_path.name,
                            "type": "integration_function"
                        })
                        
            except Exception as e:
                logging.info(f"⚠️ Error scanning {py_file}: {e}")
                continue
        
        return integration_points
    
    def connect_to_project(self, project_name: str) -> bool:
        """Establish real connection to a project"""
        if project_name not in self.ecosystem_manifest["projects"]:
            logging.info(f"❌ Project not found: {project_name}")
            return False
        
        project_info = self.ecosystem_manifest["projects"][project_name]
        project_path = Path(project_info["path"])
        
        if not project_path.exists():
            logging.info(f"❌ Project path doesn't exist: {project_path}")
            return False
        
        # Test connection by checking if we can read files
        try:
            test_files = list(project_path.rglob("*"))[:5]  # Check first 5 files
            if test_files:
                self.active_connections[project_name] = {
                    "path": project_path,
                    "status": "connected",
                    "integration_points": project_info["integration_points"],
                    "last_checked": str(datetime.now())
                }
                logging.info(f"✅ Connected to {project_name} - {len(test_files)} files accessible")
                return True
        except Exception as e:
            logging.info(f"❌ Connection failed to {project_name}: {e}")
        
        return False
    
    def scan_project_health(self, project_name: str) -> Dict:
        """Perform real health check on a project"""
        if project_name not in self.active_connections:
            if not self.connect_to_project(project_name):
                return {"status": "disconnected", "health_score": 0.0}
        
        project_path = self.active_connections[project_name]["path"]
        health_metrics = {}
        
        try:
            # Code metrics
            py_files = list(project_path.rglob("*.py"))
            js_files = list(project_path.rglob("*.js"))
            ts_files = list(project_path.rglob("*.ts"))
            total_files = len(py_files) + len(js_files) + len(ts_files)
            
            health_metrics["file_count"] = total_files
            health_metrics["code_health"] = min(total_files / 100, 1.0)  # Simple metric
            
            # Test coverage (if tests exist)
            test_files = list(project_path.rglob("*test*.py")) + list(project_path.rglob("*.test.*"))
            health_metrics["test_coverage"] = len(test_files) / max(len(py_files), 1)
            
            # Recent activity
            health_metrics["recent_activity"] = self._check_recent_activity(project_path)
            
            # Overall health score
            health_score = (
                health_metrics["code_health"] * 0.4 +
                health_metrics["test_coverage"] * 0.3 +
                health_metrics["recent_activity"] * 0.3
            )
            health_metrics["health_score"] = health_score
            
        except Exception as e:
            logging.info(f"❌ Health scan failed for {project_name}: {e}")
            health_metrics = {"status": "error", "health_score": 0.0}
        
        return health_metrics
    
    def _check_recent_activity(self, project_path: Path) -> float:
        """Check for recent file modifications (0.0 to 1.0)"""
        try:
            recent_files = []
            for file_path in project_path.rglob("*"):
                if file_path.is_file():
                    # Get modification time (days since modified)
                    mtime = file_path.stat().st_mtime
                    days_ago = (time.time() - mtime) / (24 * 3600)
                    if days_ago < 30:  # Files modified in last 30 days
                        recent_files.append(file_path)
            
            # Normalize to 0.0-1.0 scale
            activity_score = min(len(recent_files) / 10, 1.0)
            return activity_score
            
        except Exception:
            return 0.0