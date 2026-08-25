import os
from pathlib import Path

# Root directory of the entire RootBase project
ROOT_DIR = Path("/storage/emulated/0/RootBase")

# Directories and files to explicitly exclude from monitoring and analysis
# These are glob patterns relative to ROOT_DIR
EXCLUSION_PATTERNS = [
    "molt_engine/**",
    "molt_v3_engine/**",
    "data/motherbrain/api/bus/**",
    "node_modules/**", # Common for many projects, often external
    ".git/**",         # Git internals
    "__pycache__/**",  # Python compiled files
    "*.pyc",           # Python compiled files
    "*.txt",           # General text files (can be refined later)
    "*.md",            # Markdown files
    "archive/**",      # User specified archive directory
    "tmp/**",          # Temporary files/directories
    "bin/**",          # Executables/scripts which may not need code analysis
    "nemo/**",         # Specific directory, assumed to be excluded based on context
    "ollama_models_too/**", # OLLAMA Models directory
    "swarm_intell_dupe", # Specific file, assumed to be excluded
    "structure_dump.txt", # Specific file, assumed to be excluded
]

# Paths to explicitly monitor. If empty, the entire ROOT_DIR (minus exclusions) is monitored.
MONITORED_PATHS = ["/storage/emulated/0/RootBase/data_scouts"]

# Reporting configuration
REPORTING_CONFIG = {
    "output_format": "json", # or "text", "markdown"
    "report_file": ROOT_DIR / "logs/truthsleuth_report.json"
}

# Thresholds and rules for code quality
CODE_QUALITY_RULES = {
    "max_line_length": 100,
    "max_function_complexity": 10, # Cyclomatic complexity
    "forbidden_patterns": [
        "eval(",
        "exec("
    ],
    "min_docstring_length": 20 # Minimum characters for a docstring
}
