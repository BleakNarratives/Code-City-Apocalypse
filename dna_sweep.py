#!/usr/bin/env python3
"""
DNA Sweep — Code-City-Apocalypse

Tags every Python file with a [DNA_TAG] block matching RootBase convention.
Deterministic, idempotent, zero-overwrites.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional

# ── Configuration ───────────────────────────────────────────────────────

ORIGIN = "Crostini-Chromebook"
AUTHOR = "Buffy (Codebuff AI)"
SESSION = "2026-08-22 Bucket 08 DNA Sweep"

# Pillar mapping based on directory location
PILLAR_MAP = {
    "Code_City/src/entities": "codecity-entities",
    "Code_City/src/buildings": "codecity-buildings",
    "Code_City/src/core": "codecity-core",
    "Code_City/src/city": "codecity-city",
    "Code_City/src/scanner": "codecity-scanner",
    "Code_City/src/multiplayer": "codecity-multiplayer",
    "Code_City/src/integrations": "codecity-integrations",
    "Code_City/code_tool": "codecity-extraction",
    "Code_City/app": "codecity-app",
    "Code_City/data": "codecity-data",
    "Code_City/sigil_bn_0": "codecity-sigil",
    "Code_City_Unified": "codecity-unified",
    "code_tool": "codecity-extraction",
    "app": "codecity-app",
    "backend": "codecity-backend",
    "frontend": "codecity-frontend",
    "src": "codecity-src",
}

# Tier mapping based on file role
TIER_MAP = {
    "test_": (0, "Test"),
    "simple_test": (0, "Test"),
    "__init__": (1, "Package"),
    "cli": (2, "Interface"),
    "server": (2, "Interface"),
    "app": (2, "Interface"),
    "main": (2, "Interface"),
    "core": (3, "Core"),
    "engine": (3, "Core"),
    "scanner": (3, "Core"),
    "mapper": (3, "Core"),
    "orchestrator": (3, "Core"),
    "attack": (4, "Attack"),
    "red_team": (4, "Attack"),
    "defend": (5, "Defense"),
    "security": (5, "Defense"),
    "audit": (5, "Defense"),
    "widget": (6, "UI"),
    "visualiz": (6, "UI"),
    "demo": (6, "UI"),
    "html": (6, "UI"),
    "config": (7, "Config"),
    "util": (7, "Utility"),
    "helper": (7, "Utility"),
    "extract": (8, "Extraction"),
    "chat_export": (8, "Extraction"),
}


def infer_pillar(filepath: str) -> str:
    """Infer pillar from file path."""
    for pattern, pillar in PILLAR_MAP.items():
        if pattern in filepath:
            return pillar
    return "codecity-general"


def infer_tier(filepath: str, content: str) -> tuple:
    """Infer tier from filename and content."""
    name = Path(filepath).stem.lower()
    for pattern, tier_info in TIER_MAP.items():
        if pattern in name:
            return tier_info
    # Check content for clues
    if "class " in content and "def " in content:
        return (3, "Module")
    if "def " in content:
        return (2, "Script")
    return (1, "File")


def infer_deps(content: str) -> str:
    """Extract import dependencies from content."""
    deps = set()
    for match in re.finditer(r'^(?:import|from)\s+(\S+)', content, re.MULTILINE):
        mod = match.group(1).split('.')[0]
        if mod not in ('__future__',):
            deps.add(mod)
    return ", ".join(sorted(deps)) if deps else "stdlib"


def infer_role(filepath: str, content: str) -> str:
    """Infer the file's role from content."""
    # Check docstring
    doc_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
    if doc_match:
        first_line = doc_match.group(1).strip().split('\n')[0][:80]
        if first_line:
            return first_line

    # Check class/function names
    classes = re.findall(r'class\s+(\w+)', content)
    funcs = re.findall(r'def\s+(\w+)', content)

    if classes:
        return f"{classes[0]} class module"
    if funcs:
        return f"{funcs[0]} function module"
    return Path(filepath).stem.replace('_', ' ')


def generate_dna_tag(filepath: str, content: str) -> str:
    """Generate a DNA_TAG block for a file."""
    rel = str(Path(filepath))
    pillar = infer_pillar(rel)
    tier_num, tier_name = infer_tier(rel, content)
    deps = infer_deps(content)
    role = infer_role(rel, content)

    tag = f"""# [DNA_TAG]
# ORIGIN: {ORIGIN}
# PILLAR: {pillar}
# DEPS: {deps}
# ROLE: {role}
# AUTHOR: {AUTHOR}
# SESSION: {SESSION}
# TIER: {tier_name} ({tier_num})
# [/DNA_TAG]"""
    return tag


def needs_tag(content: str) -> bool:
    """Check if file already has a DNA_TAG."""
    return "[DNA_TAG]" not in content


def tag_file(filepath: Path) -> bool:
    """Tag a single file. Returns True if modified."""
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return False

    if not needs_tag(content):
        return False

    # Skip files that are too small (< 10 bytes)
    if len(content.strip()) < 10:
        return False

    tag = generate_dna_tag(str(filepath), content)

    # Insert after shebang or at start
    lines = content.split('\n')
    insert_at = 0

    if lines and lines[0].startswith('#!'):
        insert_at = 1
    elif lines and lines[0].startswith('#'):
        # Find end of comment block
        for i, line in enumerate(lines):
            if not line.startswith('#'):
                insert_at = i
                break
        else:
            insert_at = len(lines)

    lines.insert(insert_at, '')
    lines.insert(insert_at + 1, tag)
    lines.insert(insert_at + 2, '')

    new_content = '\n'.join(lines)
    filepath.write_text(new_content, encoding='utf-8')
    return True


def main():
    root = Path(__file__).parent
    py_files = sorted(
        f for f in root.rglob('*.py')
        if '__pycache__' not in str(f)
        and '.git' not in str(f)
        and f.name != 'dna_sweep.py'
        and f.name != 'fix_android_paths.py'
        and f.name != 'verify_paths.py'
    )

    print(f"DNA SWEEP — Code-City-Apocalypse")
    print(f"Files found: {len(py_files)}")
    print()

    tagged = 0
    skipped = 0
    errors = 0

    for f in py_files:
        try:
            if tag_file(f):
                tagged += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {f.relative_to(root)}: {e}")
            errors += 1

    print(f"Tagged: {tagged}")
    print(f"Skipped (already tagged or too small): {skipped}")
    print(f"Errors: {errors}")
    print(f"Total: {tagged + skipped + errors}")

    # Verify
    verify_count = sum(
        1 for f in root.rglob('*.py')
        if '__pycache__' not in str(f)
        and '.git' not in str(f)
        and f.name != 'dna_sweep.py'
        and '[DNA_TAG]' in f.read_text(encoding='utf-8', errors='replace')
    )
    print(f"\nVerification: {verify_count} files now have DNA_TAG")


if __name__ == "__main__":
    main()
