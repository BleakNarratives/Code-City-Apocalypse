import json
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from truthsleuth.config import REPORTING_CONFIG

def generate_report(issues: List[Dict[str, Any]]) -> Path:
    """Generates a report based on the identified issues and saves it to a file."""
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_issues": len(issues),
        "issues": issues,
        "summary": {
            "severity": {},
            "types": {}
        }
    }

    # Aggregate summary statistics
    for issue in issues:
        issue_type = issue.get("type", "unknown")
        # Assuming a default severity if not present in issue data
        issue_severity = issue.get("severity", "medium") 
        
        report_data["summary"]["types"][issue_type] = report_data["summary"]["types"].get(issue_type, 0) + 1
        report_data["summary"]["severity"][issue_severity] = report_data["summary"]["severity"].get(issue_severity, 0) + 1

    report_file_path = REPORTING_CONFIG["report_file"]
    report_file_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists

    try:
        with open(report_file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"Reporter: Report successfully generated at {report_file_path}")
        return report_file_path
    except Exception as e:
        print(f"Reporter: Error generating report: {e}")
        # Log or handle the error appropriately
        return Path("error_report.json") # Return a dummy path on error

def print_issue(issue: Dict[str, Any]):
    """Prints a single issue to the console (for quick feedback)."""
    print(f"[ISSUE] {issue.get("type", "N/A")} in {issue.get("file", "N/A")}:{issue.get("line", 0)} - {issue.get("message", "N/A")}")
