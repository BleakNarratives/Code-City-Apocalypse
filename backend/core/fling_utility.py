"""[ARCHIVED CHAT PASTE — historical artifact, not executable code]

import yaml
import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Setup logging for the utility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FlingUtility:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config: Dict = self._load_config()
        self.sd_card_root: Path = Path(os.path.expanduser(self.config.get("sd_card_root", "~/sd_card_root"))).resolve()
        
        # Ensure the base SD card root exists
        self.sd_card_root.mkdir(parents=True, exist_ok=True)
        logger.info(f"Fling utility initialized. SD Card Root: {self.sd_card_root}")

    def _load_config(self) -> Dict:
        \"\"\"Loads the Fling configuration from a YAML file.\"\"\"
        if not self.config_path.exists():
            logger.error(f"Config file not found: {self.config_path}")
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config file {self.config_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading config file {self.config_path}: {e}")
            raise

    def _resolve_source_path(self, path_str: str) -> Path:
        \"\"\"Expands user home directory and resolves the path.\"\"\"
        return Path(os.path.expanduser(path_str)).resolve()

    def fling_files(self, dry_run: bool = False) -> Dict:
        \"\"\"
        Scans source directories, matches files against patterns, and flings them to destinations.
        Returns a summary of actions taken.
        \"\"\"
        logger.info(f"Starting Fling operation (Dry Run: {dry_run})...")
        summary = {
            "total_scanned_files": 0,
            "total_flung_files": 0,
            "actions": []
        }

        source_dirs = [self._resolve_source_path(d) for d in self.config.get("source_directories", [])]
        mappings = self.config.get("mappings", [])

        for source_dir in source_dirs:
            if not source_dir.is_dir():
                logger.warning(f"Source directory not found, skipping: {source_dir}")
                continue

            logger.info(f"Scanning source directory: {source_dir}")
            for file_path in source_dir.rglob('*'):
                if not file_path.is_file():
                    continue
                
                summary["total_scanned_files"] += 1

                for mapping in mappings:
                    pattern = mapping.get("pattern")
                    destination_subdir = mapping.get("destination")
                    action = mapping.get("action", "move")
                    tag = mapping.get("tag", "N/A")
                    source_subdir_filter = mapping.get("source_subdir") # New filter for specific subdirs

                    if not pattern or not destination_subdir:
                        logger.warning(f"Skipping malformed mapping: {mapping}")
                        continue
                    
                    # Apply source_subdir filter if present
                    if source_subdir_filter:
                        # Convert glob pattern to regex for more flexible matching
                        # Ensure pattern matches full path relative to source_dir
                        relative_path_str = str(file_path.relative_to(source_dir))
                        if not Path(relative_path_str).match(source_subdir_filter + "/*") and 
                           not Path(relative_path_str).parent.match(source_subdir_filter):
                            continue # File is not in the specified source subdirectory pattern

                    # Check if file matches the pattern
                    if file_path.match(pattern):
                        dest_path_resolved = self.sd_card_root / destination_subdir / file_path.name
                        
                        logger.info(f"Match found: '{file_path}' -> '{dest_path_resolved}' (Tag: {tag})")

                        if not dry_run:
                            try:
                                dest_path_resolved.parent.mkdir(parents=True, exist_ok=True)
                                if action == "move":
                                    shutil.move(str(file_path), str(dest_path_resolved))
                                    logger.info(f"Moved: {file_path} to {dest_path_resolved}")
                                elif action == "copy":
                                    shutil.copy2(str(file_path), str(dest_path_resolved))
                                    logger.info(f"Copied: {file_path} to {dest_path_resolved}")
                                else:
                                    logger.warning(f"Unknown action '{action}' for {file_path}. Skipping.")
                                    continue # Skip to next file if action is unknown

                                summary["total_flung_files"] += 1
                                summary["actions"].append({
                                    "source": str(file_path),
                                    "destination": str(dest_path_resolved),
                                    "action": action,
                                    "tag": tag,
                                    "status": "success"
                                })
                                # If moved, we might not want to process it again for other mappings
                                if action == "move":
                                    break 

                            except Exception as e:
                                logger.error(f"Failed to fling {file_path} (Action: {action}): {e}")
                                summary["actions"].append({
                                    "source": str(file_path),
                                    "destination": str(dest_path_resolved),
                                    "action": action,
                                    "tag": tag,
                                    "status": f"failed: {e}"
                                })
                        else:
                            logger.info(f"DRY RUN: Would {action} '{file_path}' to '{dest_path_resolved}' (Tag: {tag})")
                            summary["actions"].append({
                                "source": str(file_path),
                                "destination": str(dest_path_resolved),
                                "action": action,
                                "tag": tag,
                                "status": "dry_run"
                            })
                            # In dry run, don't break, allow other mappings to show potential actions
                            # if action == "move":
                            #    break 
        logger.info("Fling operation complete.")
        return summary

if __name__ == "__main__":
    # Example usage (for testing fling_utility.py directly)
    config_file = Path(__file__).parent.parent / "config" / "fling_config.yaml"
    
    # Create some dummy files for testing
    dummy_source = Path(os.path.expanduser("~/fling_test_source"))
    dummy_source.mkdir(exist_ok=True, parents=True)
    (dummy_source / "report.pdf").touch()
    (dummy_source / "image.jpg").touch()
    (dummy_source / "project_reports").mkdir(exist_ok=True)
    (dummy_source / "project_reports" / "summary.md").touch()
    
    # Create a dummy log subdirectory
    (dummy_source / "some_app" / "logs").mkdir(exist_ok=True, parents=True)
    (dummy_source / "some_app" / "logs" / "app.log").touch()


    console = Console() # For rich output in example

    try:
        fling_util = FlingUtility(config_file)
        
        console.print(Panel("[bold yellow]Fling Utility - Dry Run[/bold yellow]", border_style="yellow"))
        dry_run_summary = fling_util.fling_files(dry_run=True)
        console.print(f"Total files scanned: {dry_run_summary['total_scanned_files']}")
        console.print(f"Total files to be flung (Dry Run): {dry_run_summary['total_flung_files']}")
        for action in dry_run_summary['actions']:
            console.print(f"  [cyan]DRY RUN:[/] {action['action']} '{action['source']}' to '{action['destination']}' (Tag: {action['tag']})")

        console.print(Panel("[bold green]Fling Utility - Executing[/bold green]", border_style="green"))
        # You would typically ask for confirmation before executing
        # input("Press Enter to execute the Fling operation...")
        # live_run_summary = fling_util.fling_files(dry_run=False)
        # console.print(f"Total files scanned: {live_run_summary['total_scanned_files']}")
        # console.print(f"Total files flung: {live_run_summary['total_flung_files']}")
        # for action in live_run_summary['actions']:
        #    console.print(f"  [green]FLUNG:[/] {action['action']} '{action['source']}' to '{action['destination']}' (Tag: {action['tag']}) - Status: {action['status']}")

    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Fling config file not found at {config_file}. Please create it.")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

"""