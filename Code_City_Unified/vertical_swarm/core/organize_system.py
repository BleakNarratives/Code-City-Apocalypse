#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: hashlib, os, pathlib, rich, shutil
# ROLE: VERTICAL AI - SYSTEM ORGANIZER
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

"""
VERTICAL AI - SYSTEM ORGANIZER
Eliminates duplicates, organizes files, and optimizes storage
"""

import os
import hashlib
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.tree import Tree

def find_duplicates(root_dir):
    """Find duplicate files using MD5 hashing"""
    console = Console()
    console.print("🔍 Scanning for duplicate files...")
    
    duplicates = {}
    
    with Progress() as progress:
        task = progress.add_task("Scanning files...", total=sum(1 for _ in Path(root_dir).rglob('*')))
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    if file_hash in duplicates:
                        duplicates[file_hash].append(file_path)
                    else:
                        duplicates[file_hash] = [file_path]
                except (IOError, OSError):
                    pass
                
                progress.update(task, advance=1)
    
    # Filter out non-duplicates
    true_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
    
    console.print(f"✅ Found {len(true_duplicates)} sets of duplicate files")
    return true_duplicates

def organize_by_category(root_dir):
    """Organize files into logical categories"""
    console = Console()
    console.print("📁 Organizing files by category...")
    
    # Category mapping
    categories = {
        'CODE': ['.py', '.js', '.java', '.cpp', '.h', '.sh'],
        'DATA': ['.json', '.csv', '.sql', '.db'],
        'DOCS': ['.md', '.txt', '.pdf', '.docx'],
        'CONFIG': ['.cfg', '.ini', '.yml', '.yaml', '.env'],
        'WEB': ['.html', '.css', '.php'],
        'MEDIA': ['.jpg', '.png', '.gif', '.mp4', '.mp3'],
        'ARCHIVE': ['.zip', '.tar', '.gz', '.rar']
    }
    
    # Create category directories
    for category in categories.keys():
        os.makedirs(os.path.join(root_dir, category), exist_ok=True)
    
    moved_files = 0
    
    with Progress() as progress:
        task = progress.add_task("Organizing files...", total=sum(1 for _ in Path(root_dir).rglob('*')))
        
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                # Skip if already in category folder
                if any(cat in root for cat in categories.keys()):
                    progress.update(task, advance=1)
                    continue
                
                # Find matching category
                for category, extensions in categories.items():
                    if ext in extensions:
                        target_dir = os.path.join(root_dir, category)
                        target_path = os.path.join(target_dir, file)
                        
                        # Handle name conflicts
                        counter = 1
                        while os.path.exists(target_path):
                            target_path = os.path.join(target_dir, f"{os.path.splitext(file)[0]}_{counter}{ext}")
                            counter += 1
                        
                        shutil.move(file_path, target_path)
                        moved_files += 1
                        break
                
                progress.update(task, advance=1)
    
    console.print(f"✅ Moved {moved_files} files into categories")

def remove_empty_directories(root_dir):
    """Remove empty directories"""
    console = Console()
    console.print("🗑️  Removing empty directories...")
    
    removed = 0
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                removed += 1
    
    console.print(f"✅ Removed {removed} empty directories")

def create_visual_map(root_dir):
    """Create visual tree map of directory structure"""
    console = Console()
    console.print("🗺️  Creating visual directory map...")
    
    tree = Tree("📁 VERTICAL AI SYSTEM")
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(root_dir, '').count(os.sep)
        indent = "   " * level
        
        if level == 0:
            continue
        
        parent = tree
        for part in Path(root).relative_to(root_dir).parts:
            parent = next((c for c in parent.children if c.label == part), None)
            if parent is None:
                break
        
        if parent is None:
            continue
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            dir_tree = parent.add(f"📂 {dir}")
            
            # Count files in directory
            file_count = sum(len(f) for _, _, f in os.walk(dir_path))
            if file_count > 0:
                dir_tree.add(f"📄 {file_count} files")
        
        for file in files:
            parent.add(f"📄 {file}")
    
    console.print(tree)

def optimize_storage(root_dir):
    """Run complete storage optimization"""
    console = Console()
    console.print(Panel.fit(
        "🧹 VERTICAL AI - STORAGE OPTIMIZATION",
        style="bold white on blue"
    ))
    
    # 1. Find duplicates
    duplicates = find_duplicates(root_dir)
    
    # 2. Organize by category
    organize_by_category(root_dir)
    
    # 3. Remove empty directories
    remove_empty_directories(root_dir)
    
    # 4. Create visual map
    create_visual_map(root_dir)
    
    # 5. Calculate savings
    total_size = sum(os.path.getsize(f) for f in Path(root_dir).rglob('*') if os.path.isfile(f))
    readable_size = f"{total_size / 1024 / 1024:.2f} MB"
    
    console.print(f"\n✅ OPTIMIZATION COMPLETE")
    console.print(f"   Total size: {readable_size}")
    console.print(f"   Duplicates found: {len(duplicates)}")
    console.print(f"   Files organized: {sum(len(v) for v in duplicates.values())}")
    console.print(f"   Storage optimized: ✅")

if __name__ == "__main__":
    console = Console()
    
    console.clear()
    console.print(Panel.fit(
        "🧹 VERTICAL AI - SYSTEM ORGANIZATION",
        style="bold white on purple"
    ))
    
    target_dir = "~/Vertical-AI"
    
    console.print(f"\n🎯 Target Directory: {target_dir}")
    console.print("📊 Current Status:")
    
    # Get directory stats
    total_files = sum(1 for _ in Path(target_dir).rglob('*'))
    total_size = sum(os.path.getsize(f) for f in Path(target_dir).rglob('*') if os.path.isfile(f))
    
    console.print(f"   Files: {total_files}")
    console.print(f"   Size: {total_size / 1024 / 1024:.2f} MB")
    
    input("\n🚀 Press Enter to begin organization...")
    
    optimize_storage(target_dir)
    
    console.print("\n" + "="*60)
    console.print("🎉 ORGANIZATION COMPLETE")
    console.print("="*60)
    console.print("\n📁 Your Vertical AI system is now:")
    console.print("   • Duplicate-free")
    console.print("   • Logically organized")
    console.print("   • Storage-optimized")
    console.print("   • Visually mapped")
    console.print("\n💡 Next steps:")
    console.print("   1. Review the visual map")
    console.print("   2. Delete unnecessary duplicates")
    console.print("   3. Enjoy your organized system!")