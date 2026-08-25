import logging

"""
DIAGNOSTIC SCRIPT - Android internal storage version
"""

import os
from pathlib import Path

def diagnose_android_structure():
    logging.info("📱 ANDROID STORAGE DIAGNOSIS")
    
    # Common Android storage paths
    possible_roots = [
        "/storage/emulated/0",  # Primary internal storage
        "/sdcard",              # Common symlink
        "/storage/sdcard0",     # Alternative
        "/data/data/com.termux/files/home/storage/shared",  # Termux shared storage
        "."                     # Current directory
    ]
    
    actual_root = None
    for root in possible_roots:
        test_path = Path(root)
        if test_path.exists():
            actual_root = test_path
            logging.info(f"✅ Found storage root: {root}")
            break
    
    if not actual_root:
        logging.info("❌ No storage root found!")
        return None
    
    # Check for syntax_ai in this root
    syntax_ai_path = actual_root / "syntax_ai"
    if syntax_ai_path.exists():
        logging.info(f"✅ Found syntax_ai: {syntax_ai_path}")
    else:
        logging.info(f"❌ syntax_ai not found at: {syntax_ai_path}")
        logging.info("💡 Creating syntax_ai directory structure...")
        syntax_ai_path.mkdir(exist_ok=True)
    
    # Look for your projects
    target_projects = ["ModMind", "EquiNex", "EquiLex", "ChAImeleon", "IDEal", "ShipWrekD_OS"]
    found_projects = {}
    
    logging.info(f"\n🔍 Looking for projects in {actual_root}:")
    for project in target_projects:
        project_path = actual_root / project
        if project_path.exists():
            files = list(project_path.rglob("*"))
            found_projects[project] = str(project_path)
            logging.info(f"✅ {project}: {len(files)} files at {project_path}")
        else:
            found_projects[project] = None
            logging.info(f"❌ {project}: NOT FOUND")
    
    # List everything in the root to see what's actually there
    logging.info(f"\n📂 Everything in {actual_root}:")
    for item in actual_root.iterdir():
        if item.is_dir():
            item_files = list(item.rglob("*"))
            logging.info(f"   📁 {item.name}/ ({len(item_files)} items)")
        else:
            logging.info(f"   📄 {item.name}")
    
    return actual_root, syntax_ai_path, found_projects

if __name__ == "__main__":
    result = diagnose_android_structure()
    if result:
        root, syntax_path, projects = result
        logging.info(f"\n💾 Android storage root: {root}")
        logging.info(f"💾 Syntax AI path: {syntax_path}")
        logging.info(f"💾 Found {len([p for p in projects.values() if p])} projects")