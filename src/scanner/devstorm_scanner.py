# File: devstorm_scanner.py (The ModMind Scanner Backend)

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: stdlib
# ROLE: Classifies a file into Industry, Commerce, or Residential Zone based on path and
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]


# --- ZONING CLASSIFIER (Blueprint for ModMind Agent Specialization) ---

CODE_ZONES = {
    "INDUSTRY": { # Backend Services, APIs, Databases, Core Logic
        "extensions": [".py", ".go", ".java", ".c", ".cpp", ".cs", ".php", ".sql"],
        "paths": ["/api/", "/service/", "/db/", "/models/", "/core/"]
    },
    "COMMERCE": { # Frontend, UI/UX, User-Facing Apps, Gaming Logic
        "extensions": [".js", ".ts", ".html", ".css", ".scss", ".vue", ".jsx", ".tsx"],
        "paths": ["/ui/", "/app/", "/components/", "/views/", "/public/"]
    },
    "RESIDENTIAL": { # Infrastructure, Config, Scripts, Documentation
        "extensions": [".yaml", ".json", ".xml", ".sh", ".md", ".toml", ".tf", ".env"],
        "paths": ["/config/", "/tests/", "/docs/", "/scripts/", "/infra/"]
    }
}

def classify_zone(file_path):
    """Classifies a file into Industry, Commerce, or Residential Zone based on path and extension."""
    
    file_path_lower = file_path.lower()
    
    # 1. Classify by Path (Higher Priority)
    for zone, criteria in CODE_ZONES.items():
        for path_segment in criteria["paths"]:
            if path_segment in file_path_lower:
                return zone
    
    # 2. Classify by Extension
    for zone, criteria in CODE_ZONES.items():
        for ext in criteria["extensions"]:
            if file_path_lower.endswith(ext):
                return zone
    
    # 3. Default 
    return "RESIDENTIAL" 

# --- END ZONING CLASSIFIER ---
# The rest of your Python scanner logic will go here (e.g., analyze_file function)