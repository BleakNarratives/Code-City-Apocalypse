import logging

# FILE: conversation_orchestrator.py
# FULL PATH: ~/syntaxai-weaponized/src/core/orchestrator.py

import os
import datetime
from src.core.extractor import extract_code_and_vibe # Assumes you save the extractor.py above
from src.core.nat_lang_processor import fractalize_blue_sky_output # Assumes you save the nat_lang_processor.py above

# --- Pytch Code Sorting Class Improvement ---
# Implements better, more structured sorting logic, anticipating Pytch's data needs.
class PytchSorter:
    """
    Enhanced sorting class to structure code and natural language data 
    for better IDE/dashboard presentation (ModMind/EquiNex).
    """
    def __init__(self, base_export_path="exports"):
        self.base_export_path = base_export_path
        os.makedirs(self.base_export_path, exist_ok=True)
        self.log = []

    def sort_and_save(self, extracted_data):
        """Processes extracted data and saves code and vibe to structured locations."""
        
        file_path = extracted_data["metadata"]["source_file_path"]
        timestamp = extracted_data["metadata"]["captured_timestamp"].replace(":", "-")
        
        # 1. Save Vibe Flow (Blue Sky Analysis)
        vibe_filename = f"vibe_{timestamp}.txt"
        vibe_dir = os.path.join(self.base_export_path, "vibe_flow")
        os.makedirs(vibe_dir, exist_ok=True)
        
        # Run Nat Lang Sep (Blue Sky Meetings) on the vibe text
        blue_sky_analysis = fractalize_blue_sky_output(extracted_data["vibe_flow"])
        
        # Save the structured analysis for Pytch to integrate
        analysis_filename = f"analysis_{timestamp}.json"
        analysis_dir = os.path.join(self.base_export_path, "blue_sky_analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        with open(os.path.join(analysis_dir, analysis_filename), 'w') as f:
            json.dump(blue_sky_analysis, f, indent=4)
        
        self.log.append(f"Saved Blue Sky Analysis: {analysis_filename}")

        # 2. Save Code Blocks
        code_count = 0
        for block_id, block_data in extracted_data["code_blocks"].items():
            lang = block_data["language"]
            content = block_data["content"]
            
            # Create language-specific directory for Pytch sorting
            code_dir = os.path.join(self.base_export_path, "code_blocks", lang)
            os.makedirs(code_dir, exist_ok=True)
            
            # Use block_id for unique filename
            code_filename = f"{block_id}_{lang}_{timestamp}.txt" 
            
            with open(os.path.join(code_dir, code_filename), 'w') as f:
                f.write(content)
            
            self.log.append(f"Saved Code Block ({lang}): {code_filename}")
            code_count += 1
            
        return {"code_blocks_saved": code_count, "analysis_saved": analysis_filename}


# --- Main Orchestration Function ---
def process_conversation_file(input_file_path):
    """Runs a file through the entire pipeline: extract, process, and sort."""
    
    # 1. Read input
    try:
        with open(input_file_path, 'r') as f:
            conversation_text = f.read()
    except FileNotFoundError:
        logging.info(f"ERROR: Input file not found at {input_file_path}")
        return None

    file_name = os.path.basename(input_file_path)

    # 2. Extract Code and Vibe (Simultaneously)
    logging.info("-> 1. Running simultaneous Code Extractor & Vibe Separation...")
    extracted_data = extract_code_and_vibe(conversation_text, file_name, input_file_path)
    logging.info(f"-> Found {len(extracted_data['code_blocks'])} code blocks.")
    
    # 3. Sort and Process Nat Lang (Blue Sky Fractalization)
    logging.info("-> 2. Running Pytch Sorter & Blue Sky Fractalization...")
    sorter = PytchSorter()
    results = sorter.sort_and_save(extracted_data)
    
    logging.info(f"\n✅ Processing Complete for {file_name}")
    logging.info(f"   Code Blocks Saved: {results['code_blocks_saved']}")
    logging.info(f"   Blue Sky Analysis Saved: {results['analysis_saved']}")

    return results

# Example of how the main launch.py would call this:
# if __name__ == "__main__":
#     # This is where the clipboard monitor output or manual file would be pointed
#     temp_capture_file = "/path/to/your/captured/conversation.txt"
#     process_conversation_file(temp_capture_file)
