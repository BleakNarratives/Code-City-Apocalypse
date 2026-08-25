# Save this as ~/syntaxai_main/setup.py
import os
import subprocess

def create_project_structure():
    """Create proper GitHub-ready project structure"""
    project_root = os.path.expanduser("~/syntax_ai_main")
    
    directories = [
        "src",
        "src/conversation_processor", 
        "src/clipboard_monitor",
        "src/build_orchestrator",
        "tests",
        "automations",
        "extracted_code",
        "docs",
        "scripts",
        "data/raw_conversations",
        "data/processed",
        "exports/vibe_flow",
        "exports/code_blocks"
    ]
    
    for directory in directories:
        os.makedirs(f"{project_root}/{directory}", exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # Create __init__.py files
    for init_dir in ["src", "src/conversation_processor", "src/clipboard_monitor", "src/build_orchestrator"]:
        with open(f"{project_root}/{init_dir}/__init__.py", "w") as f:
            f.write('"""SyntaxAI Auto-conversation to code"""\n')
    
    print(f"✅ Project structure created at: {project_root}")
    return project_root

if __name__ == "__main__":
    create_project_structure()
