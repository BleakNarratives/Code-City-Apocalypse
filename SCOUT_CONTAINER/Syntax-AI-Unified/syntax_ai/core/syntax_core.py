import logging

"""
SYNTAX AI CORE - Robust version that works with any directory structure
"""

import os
import time
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SovereignDirective:
    action: str
    target: str
    confidence: float
    reasoning: str

class SyntaxAICore:
    """Robust Syntax AI core that adapts to any environment"""
    
    def __init__(self, project_root: str = ".", ecosystem_mode: bool = True):
        self.project_root = Path(project_root).absolute()
        self.ecosystem_mode = ecosystem_mode
        self.sovereign_directives = []
        self.is_running = False
        
        logging.info(f"🎯 Syntax AI initialized")
        logging.info(f"📁 Project root: {self.project_root}")
        logging.info(f"🌐 Ecosystem mode: {ecosystem_mode}")
    
    def scan_environment(self) -> Dict:
        """Scan the current environment and return what's available"""
        scan_result = {
            "project_root": str(self.project_root),
            "exists": self.project_root.exists(),
            "is_directory": self.project_root.is_dir() if self.project_root.exists() else False,
            "contents": [],
            "python_files": 0,
            "project_structure": {}
        }
        
        if self.project_root.exists() and self.project_root.is_dir():
            # List top-level contents
            scan_result["contents"] = [item.name for item in self.project_root.iterdir()]
            
            # Count Python files
            python_files = list(self.project_root.rglob("*.py"))
            scan_result["python_files"] = len(python_files)
            
            # Analyze project structure
            for item in self.project_root.iterdir():
                if item.is_dir():
                    item_files = list(item.rglob("*"))
                    scan_result["project_structure"][item.name] = {
                        "type": "directory",
                        "file_count": len(item_files),
                        "has_python": any(f.suffix == '.py' for f in item_files),
                        "has_requirements": (item / "requirements.txt").exists()
                    }
                else:
                    scan_result["project_structure"][item.name] = {
                        "type": "file",
                        "size": item.stat().st_size
                    }
        
        return scan_result
    
    def generate_bootstrap_directives(self, environment_scan: Dict) -> List[SovereignDirective]:
        """Generate initial directives based on environment scan"""
        directives = []
        
        if not environment_scan["exists"]:
            directives.append(SovereignDirective(
                action="create_directory",
                target=str(self.project_root),
                confidence=1.0,
                reasoning="Project root directory doesn't exist"
            ))
            return directives
        
        # If we have Python files but no requirements.txt
        if environment_scan["python_files"] > 0 and not (self.project_root / "requirements.txt").exists():
            directives.append(SovereignDirective(
                action="create_requirements",
                target=str(self.project_root / "requirements.txt"),
                confidence=0.9,
                reasoning="Python project detected but no requirements.txt found"
            ))
        
        # Check for potential project organization
        if environment_scan["python_files"] > 10 and not any("src" in name for name in environment_scan["project_structure"]):
            directives.append(SovereignDirective(
                action="organize_project",
                target=str(self.project_root / "src"),
                confidence=0.8,
                reasoning="Multiple Python files detected - suggest src/ structure"
            ))
        
        return directives
    
    def execute_directive(self, directive: SovereignDirective) -> bool:
        """Execute a single directive"""
        try:
            logging.info(f"🔧 Executing: {directive.action} -> {directive.target}")
            
            if directive.action == "create_directory":
                Path(directive.target).mkdir(parents=True, exist_ok=True)
                logging.info(f"✅ Created directory: {directive.target}")
                return True
                
            elif directive.action == "create_requirements":
                requirements_content = """# Project dependencies
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
python-multipart>=0.0.5
"""
                with open(directive.target, 'w') as f:
                    f.write(requirements_content)
                logging.info(f"✅ Created requirements.txt: {directive.target}")
                return True
                
            elif directive.action == "organize_project":
                src_dir = Path(directive.target)
                src_dir.mkdir(exist_ok=True)
                
                # Move Python files to src (just log for now - actual move would be more careful)
                py_files = list(self.project_root.glob("*.py"))
                logging.info(f"💡 Would move {len(py_files)} Python files to {src_dir}/")
                return True
                
            else:
                logging.info(f"⚠️ Unknown action: {directive.action}")
                return False
                
        except Exception as e:
            logging.info(f"❌ Failed to execute {directive.action}: {e}")
            return False
    
    def start_sovereign_operation(self) -> Dict:
        """Start autonomous operation"""
        logging.info("🚀 Starting Sovereign Operation")
        
        # First, scan the environment
        environment = self.scan_environment()
        logging.info(f"📊 Environment scan: {environment['python_files']} Python files, {len(environment['contents'])} items")
        
        # Generate bootstrap directives
        directives = self.generate_bootstrap_directives(environment)
        logging.info(f"🎯 Generated {len(directives)} bootstrap directives")
        
        # Execute high-confidence directives
        executed = 0
        for directive in directives:
            if directive.confidence > 0.7:
                if self.execute_directive(directive):
                    executed += 1
        
        # Start background monitoring if we have a valid environment
        if environment["exists"] and environment["is_directory"]:
            self.is_running = True
            monitor_thread = threading.Thread(target=self._background_monitor, daemon=True)
            monitor_thread.start()
            logging.info("🔍 Background monitoring started")
        
        return {
            "status": "operational" if self.is_running else "limited",
            "environment_scanned": True,
            "directives_generated": len(directives),
            "directives_executed": executed,
            "project_root": str(self.project_root)
        }
    
    def _background_monitor(self):
        """Background monitoring loop"""
        while self.is_running:
            try:
                # Simple heartbeat monitoring
                if self.project_root.exists():
                    python_files = list(self.project_root.rglob("*.py"))
                    if python_files:
                        # Basic health check - count files and check for modifications
                        logging.info(f"💓 Monitor: {len(python_files)} Python files active")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logging.info(f"⚠️ Monitor error: {e}")
                time.sleep(30)