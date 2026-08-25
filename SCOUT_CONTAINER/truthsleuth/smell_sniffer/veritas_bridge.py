import json
from pathlib import Path
from typing import List, Dict, Any

class VeritasBridge:
    """Bridge between TruthSleuth and the Veritas Entity Analyzer."""
    
    def __init__(self, rules_path: Path):
        self.rules_path = rules_path
        self.rules = self._load_rules()
        
    def _load_rules(self) -> Dict[str, Any]:
        with open(self.rules_path, "r") as f:
            return json.load(f).get("code_smell_rules", {})
            
    def analyze_code_content(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        issues = []
        for category, patterns in self.rules.items():
            for pattern in patterns:
                import re
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_no = content.count('\n', 0, match.start()) + 1
                    issues.append({
                        "file": file_path,
                        "line": line_no,
                        "type": category,
                        "message": f"Detected architectural smell pattern: {pattern}"
                    })
        return issues
