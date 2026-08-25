"""
AUTONOMOUS FIXER - Actually fix the issues Syntax AI found
"""

from pathlib import Path
import re
import shutil
from datetime import datetime

class AutonomousFixer:
    def __init__(self):
        self.fix_log = []
        self.backup_dir = Path("/storage/emulated/0/syntax_ai/backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def backup_file(self, file_path):
        """Create backup before fixing"""
        backup_path = self.backup_dir / f"{file_path.name}.backup_{datetime.now().strftime('%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def fix_hardcoded_credentials(self, file_path):
        """Replace hardcoded passwords with environment variables"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Pattern for hardcoded credentials
            patterns = [
                (r'(\w+)\s*=\s*["\']([^"\']*password[^"\']*)["\']', r'\1 = os.getenv("\1", "REDACTED_FOR_SECURITY")'),
                (r'(\w+)\s*=\s*["\']([^"\']*key[^"\']*)["\']', r'\1 = os.getenv("\1", "REDACTED_FOR_SECURITY")'),
                (r'(\w+)\s*=\s*["\']([^"\']*secret[^"\']*)["\']', r'\1 = os.getenv("\1", "REDACTED_FOR_SECURITY")')
            ]
            
            original_content = content
            fixes_applied = 0
            
            for pattern, replacement in patterns:
                content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
                fixes_applied += count
            
            if fixes_applied > 0:
                # Add import if needed
                if 'import os' not in content and fixes_applied > 0:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            lines.insert(i, 'import os')
                            break
                    else:
                        lines.insert(0, 'import os')
                    content = '\n'.join(lines)
                
                # Create backup and write fix
                backup_path = self.backup_file(file_path)
                with open(file_path, 'w') as f:
                    f.write(content)
                
                self.fix_log.append({
                    "file": str(file_path),
                    "fix": "hardcoded_credentials",
                    "fixes_applied": fixes_applied,
                    "backup": str(backup_path),
                    "status": "SUCCESS"
                })
                return fixes_applied
            
        except Exception as e:
            self.fix_log.append({
                "file": str(file_path),
                "fix": "hardcoded_credentials", 
                "error": str(e),
                "status": "FAILED"
            })
        
        return 0
    
    def modularize_large_file(self, file_path, max_functions=10):
        """Break large files into modules"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Count function definitions
            function_count = len(re.findall(r'^def\s+\w+', content, re.MULTILINE))
            
            if function_count > max_functions:
                # Create module directory
                module_dir = file_path.parent / f"{file_path.stem}_modules"
                module_dir.mkdir(exist_ok=True)
                
                # For now, just create a stub module structure
                init_file = module_dir / "__init__.py"
                init_file.write_text(f"# Auto-generated modules for {file_path.name}\n")
                
                self.fix_log.append({
                    "file": str(file_path),
                    "fix": "modularization",
                    "functions_count": function_count,
                    "module_created": str(module_dir),
                    "status": "PLANNED"
                })
                return 1
            
        except Exception as e:
            self.fix_log.append({
                "file": str(file_path),
                "fix": "modularization",
                "error": str(e),
                "status": "FAILED"
            })
        
        return 0
    
    def fix_automation_opportunities(self, opportunities):
        """Fix the high-priority automation opportunities found earlier"""
        total_fixes = 0
        
        for opportunity in opportunities:
            if opportunity["priority"] == "HIGH":
                file_path = Path("/storage/emulated/0/scripts") / opportunity["file"]
                if file_path.exists():
                    if "hardcoded" in opportunity["issue"].lower():
                        fixes = self.fix_hardcoded_credentials(file_path)
                        total_fixes += fixes
                    elif "modularized" in opportunity["issue"].lower():
                        fixes = self.modularize_large_file(file_path)
                        total_fixes += fixes
        
        return total_fixes
    
    def get_fix_report(self):
        """Generate a report of all fixes applied"""
        return {
            "total_fixes": len(self.fix_log),
            "successful_fixes": len([f for f in self.fix_log if f["status"] == "SUCCESS"]),
            "planned_fixes": len([f for f in self.fix_log if f["status"] == "PLANNED"]),
            "failed_fixes": len([f for f in self.fix_log if f["status"] == "FAILED"]),
            "details": self.fix_log
        }
