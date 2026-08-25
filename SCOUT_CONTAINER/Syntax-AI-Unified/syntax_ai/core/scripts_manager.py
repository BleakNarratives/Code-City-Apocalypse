import logging

"""
SCRIPTS MANAGER - Handle that big ass scripts folder full of goodies
"""

from pathlib import Path
import shutil

class ScriptsManager:
    def __init__(self):
        self.scripts_path = Path("/storage/emulated/0/scripts")
        self.bitch_work_path = Path("/storage/emulated/0/syntax_ai/bitch_work")
        logging.info(f"🔧 Scripts Manager: {self.scripts_path} -> {self.bitch_work_path}")
    
    def analyze_scripts(self):
        """See what's in that scripts folder"""
        if not self.scripts_path.exists():
            return {"error": "Scripts folder not found"}
        
        scripts = list(self.scripts_path.rglob("*"))
        file_types = {}
        
        for script in scripts:
            if script.is_file():
                ext = script.suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_files": len(scripts),
            "file_types": file_types,
            "readme_files": len(list(self.scripts_path.rglob("*README*"))),
            "python_scripts": len(list(self.scripts_path.rglob("*.py"))),
            "shell_scripts": len(list(self.scripts_path.rglob("*.sh"))),
            "status": "goldmine" if len(scripts) > 100 else "moderate"
        }
    
    def organize_bitch_work(self):
        """Organize scripts into categorized bitch work folders"""
        self.bitch_work_path.mkdir(exist_ok=True)
        
        categories = {
            "automation": ["*.py", "*.sh", "*.bash"],
            "documentation": ["*.md", "*.txt", "README*"],
            "configs": ["*.json", "*.yaml", "*.yml", "*.config"],
            "assets": ["*.jpg", "*.png", "*.pdf", "*.zip"]
        }
        
        organized = {}
        
        for category, patterns in categories.items():
            category_path = self.bitch_work_path / category
            category_path.mkdir(exist_ok=True)
            
            organized[category] = 0
            for pattern in patterns:
                for file_path in self.scripts_path.rglob(pattern):
                    if file_path.is_file():
                        try:
                            shutil.copy2(file_path, category_path / file_path.name)
                            organized[category] += 1
                        except:
                            pass
        
        return organized
    
    def find_automation_opportunities(self):
        """Find scripts that could be automated by Syntax AI"""
        opportunities = []
        
        for py_file in self.scripts_path.rglob("*.py"):
            try:
                with open(py_file, 'r') as f:
                    content = f.read().lower()
                
                # Look for patterns that indicate automation potential
                if any(keyword in content for keyword in ['manual', 'todo', 'fixme', 'hardcoded', 'password']):
                    opportunities.append({
                        "file": str(py_file.name),
                        "issue": "Contains manual processes or hardcoded values",
                        "priority": "HIGH"
                    })
                
                # Look for repetitive patterns
                if content.count('def ') > 10:
                    opportunities.append({
                        "file": str(py_file.name),
                        "issue": "Multiple functions - could be modularized",
                        "priority": "MEDIUM"
                    })
                    
            except:
                pass
        
        return opportunities
