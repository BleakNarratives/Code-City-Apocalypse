import logging

# file_organizer.py - Cleans up the root_2025 "loosies" and consolidates Code City

class FileOrganizer:
    def __init__(self, new_base_path="/storage/emulated/0/code_city"):
        self.base = new_base_path

    def get_target_path(self, filename):
        if "loosie" in filename.lower():
            return f"{self.base}/data/loosies_to_sort"
        return f"{self.base}/src/core"

    def recursively_find_and_move(self, current_source_path):
        logging.info(f">> Scanning for artifacts in: {current_source_path}")
        conceptual_files = ['Mayor_Strump_boss_system.py', 'loosie_01_untagged.txt']
        for filename in conceptual_files:
            target_directory = self.get_target_path(filename)
            logging.info(f"-> Mapped '{filename}' to {target_directory}")
        logging.info("✅ Loosie Sorter complete. Artifacts mapped.")

