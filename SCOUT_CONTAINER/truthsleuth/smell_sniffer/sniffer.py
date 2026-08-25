#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
from typing import Dict, Any, List

class CodeSmellSniffer:
    def __init__(self, target_path: str, intensity: str):
        self.target_path = target_path
        self.intensity = intensity
        self.metrics = {
            "file_name": os.path.basename(target_path),
            "lines_of_code": 0,
            "smells_detected": [],
            "severity_score": "Clean"
        }
        # Threshold adjustments based on depth intensity
        self.thresholds = {
            "light": {"max_len": 50, "max_nest": 4, "max_args": 5},
            "medium": {"max_len": 30, "max_nest": 3, "max_args": 4},
            "deep": {"max_len": 15, "max_nest": 2, "max_args": 3}
        }[intensity]

    def sniff(self) -> Dict[str, Any]:
        if not os.path.exists(self.target_path):
            print(f"[-] Error: File {self.target_path} not found.", file=sys.stderr)
            sys.exit(1)

        with open(self.target_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        self.metrics["lines_of_code"] = len(lines)
        self._analyze_lines(lines)
        self._analyze_raw_content("".join(lines))
        
        # Rate total carnage
        smell_count = len(self.metrics["smells_detected"])
        if smell_count == 0: self.metrics["severity_score"] = " Pristine"
        elif smell_count < 3: self.metrics["severity_score"] = " Low (Minor Odor)"
        elif smell_count < 6: self.metrics["severity_score"] = "☠️ Medium (Stinky)"
        else: self.metrics["severity_score"] = "☣️ Critical (Biohazard)"

        return self.metrics

    def _analyze_lines(self, lines: List[str]):
        current_func = None
        func_lines = 0
        indent_pattern = re.compile(r'^(?P<spaces>\s*)')

        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # 1. Detect Bare Excepts
            if "except:" in stripped or "except Exception:" in stripped:
                self.metrics["smells_detected"].append({
                    "line": idx, "type": "Silent Killer", "desc": "Bare or generic exception handling masking internal crashes."
                })

            # 2. Hardcoded Secrets (Naive regex for SaaS speed)
            if re.search(r'(password|passwd|secret|api_key|token|passwd)\s*=\s*[\'"][^\'"]+[\'"]', line, re.IGNORECASE):
                self.metrics["smells_detected"].append({
                    "line": idx, "type": "Security Leak", "desc": "Potential plaintext credential or API token hardcoded."
                })

            # 3. Arrow Anti-pattern (Deep Nesting)
            match = indent_pattern.match(line)
            if match and stripped:
                spaces = len(match.group('spaces'))
                tabs = line.count('\t')
                nest_level = (spaces // 4) + tabs
                if nest_level > self.thresholds["max_nest"]:
                    self.metrics["smells_detected"].append({
                        "line": idx, "type": "Arrow Complexity", "desc": f"Nesting depth tracking at level {nest_level}. Code refactoring required."
                    })

            # 4. Function Bloat Tracking
            if stripped.startswith("def ") or stripped.startswith("async def "):
                if current_func: # check previous function size before resetting
                    if func_lines > self.thresholds["max_len"]:
                        self.metrics["smells_detected"].append({
                            "line": idx - func_lines, "type": "Brain Function", "desc": f"Function '{current_func}' spans {func_lines} lines (Max allowed: {self.thresholds['max_len']})."
                        })
                # Check arguments count
                arg_match = re.search(r'\((.*?)\)', stripped)
                if arg_match:
                    args_count = len([a for a in arg_match.group(1).split(',') if a.strip()])
                    if args_count > self.thresholds["max_args"]:
                        func_name = stripped.split('(')[0].replace('def ', '').strip()
                        self.metrics["smells_detected"].append({
                            "line": idx, "type": "Long Parameter List", "desc": f"Function '{func_name}' accepts {args_count} positional parameters."
                        })
                current_func = stripped.split('(')[0].split(' ')[1]
                func_lines = 0
            elif current_func and stripped:
                func_lines += 1

    def _analyze_raw_content(self, content: str):
        # 5. Todo accumulation / Technical Debt
        todos = len(re.findall(r'#\s*(TODO|FIXME)', content, re.IGNORECASE))
        if todos > 4:
            self.metrics["smells_detected"].append({
                "line": "Global", "type": "Hoarder Tendencies", "desc": f"Found {todos} pending TODO/FIXME comments rotting in code."
            })

class OutputFormatter:
    @staticmethod
    def to_txt(data: Dict) -> str:
        out = f"=== SMELL SNIFFER REPORT: {data['file_name']} ===\n"
        out += f"Total Lines: {data['lines_of_code']}\n"
        out += f"Status: {data['severity_score']}\n"
        out += "="*40 + "\n"
        for issue in data['smells_detected']:
            out += f"[{issue['type']}] Line {issue['line']}: {issue['desc']}\n"
        return out

    @staticmethod
    def to_json(data: Dict) -> str:
        return json.dumps(data, indent=2)

    @staticmethod
    def to_yaml(data: Dict) -> str:
        out = f"report:\n  file: \"{data['file_name']}\"\n  loc: {data['lines_of_code']}\n  score: \"{data['severity_score']}\"\n  issues:\n"
        for issue in data['smells_detected']:
            out += f"    - line: {issue['line']}\n      type: \"{issue['type']}\"\n      desc: \"{issue['desc']}\"\n"
        return out

    @staticmethod
    def to_toml(data: Dict) -> str:
        out = f'[report]\nfile = "{data["file_name"]}"\nloc = {data["lines_of_code"]}\nscore = "{data["severity_score"]}"\n\n'
        for idx, issue in enumerate(data['smells_detected']):
            out += f'[[issues]]\nline = "{issue["line"]}"\ntype = "{issue["type"]}"\ndesc = "{issue["desc"]}"\n\n'
        return out

    @staticmethod
    def to_md(data: Dict) -> str:
        out = f"# Code Smell Audit: `{data['file_name']}`\n\n"
        out += f"- **Total Line Count:** {data['lines_of_code']}\n"
        out += f"- **System Health:** {data['severity_score']}\n\n"
        out += "## Detected Violations\n\n"
        if not data['smells_detected']:
            out += "*No code odors detected. Codebase is pristine.*\n"
        else:
            out += "| Line | Violation Type | Description |\n|---|---|---|\n"
            for issue in data['smells_detected']:
                out += f"| {issue['line']} | **{issue['type']}** | {issue['desc']} |\n"
        return out

def main():
    parser = argparse.ArgumentParser(description="CodeSmellSniffer - Static Architecture Evaluator")
    parser.add_argument("path", help="Path to target source file to scan")
    parser.add_argument("--intensity", choices=["light", "medium", "deep"], default="medium", help="Scan granularity threshold")
    parser.add_argument("--format", choices=["txt", "json", "yaml", "toml", "md"], default="txt", help="Rendered output structure")
    
    args = parser.parse_args()
    
    sniffer = CodeSmellSniffer(args.path, args.intensity)
    results = sniffer.sniff()
    
    formatter = getattr(OutputFormatter, f"to_{args.format}")
    print(formatter(results))

if __name__ == "__main__":
    main()
