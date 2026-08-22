
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: logging, os, time
# ROLE: Auto-generated code
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

import logging

import time
import os

logging.info("🤖 Coder agent started - NOW FIXED")

while True:
    try:
        # Check for tasks
        task_file = "tasks/coder_task.txt"
        if os.path.exists(task_file):
            with open(task_file, 'r') as f:
                task = f.read()
            os.remove(task_file)
            
            logging.info(f"Task received (first 50 chars): {task[:50]}...")
            
            # Create directory if it doesn't exist
            os.makedirs("backend", exist_ok=True)
            os.makedirs("frontend", exist_ok=True)
            
            # Always write to a safe location
            filename = "backend/generated_code.py"
            code = f'''# Generated from task: {task[:100]}...

def main():
    """Auto-generated code"""
    logging.info("Code stub for complex request")
    # TODO: Implement based on requirements
    
if __name__ == "__main__":
    main()'''
            
            with open(filename, 'w') as f:
                f.write(code)
                
            # Send result
            with open("comms/coder_result.txt", 'w') as f:
                f.write(f"Created {filename}")
                
            logging.info(f"Created {filename}")
        
        time.sleep(3)
        
    except Exception as e:
        logging.info(f"Error: {e}")
        time.sleep(5)
