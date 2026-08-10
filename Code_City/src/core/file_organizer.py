# file_organizer.py - The Loosie Sorter

import os
import shutil
from collections import defaultdict

# The base path for all loose files and the target for organizing.
BASE_DIR = "/storage/emulated/0/root_2025"

class LoosieSorter: # <--- THIS CLASS NAME MUST BE HERE
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.loosies_path = os.path.join(BASE_DIR, 'loosies')
        self.known_targets = {
            '.py': 'scripts/python',
            '.sh': 'scripts/bash_shell',
            '.ts': 'scripts/typescript',
            '.tsx': 'frontend/src/components',
            '.js': 'scripts/javascript',
            '.json': 'configs',
            '.txt': 'documentation/notes',
            '.md': 'documentation/notes',
            '.log': 'documentation/logs',
            '.mp4': 'media/video',
            '.mp3': 'media/audio',
        }

    def sort_loosies(self):
        """Moves files from the 'loosies' folder into appropriate project structures."""
        if not os.path.exists(self.loosies_path):
            print(f"📁 Loosies path not found, creating: {self.loosies_path}")
            os.makedirs(self.loosies_path, exist_ok=True)
            return 0

        print(f"📦 Starting Loosie Sort in: {self.loosies_path}")
        moved_count = 0
        
        for filename in os.listdir(self.loosies_path):
            if filename in ['.', '..', '.git']:
                continue
                
            file_path = os.path.join(self.loosies_path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                target_folder_name = self.known_targets.get(ext, 'unknown_files')
                
                target_dir = os.path.join(BASE_DIR, target_folder_name)
                
                try:
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_dir, filename))
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")

        print(f"✅ Loosie Sort Complete. Moved {moved_count} files.")
        return moved_count
