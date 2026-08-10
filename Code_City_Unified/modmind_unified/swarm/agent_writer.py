import logging

import time
import os

logging.info("📝 Writer agent started")

while True:
    task_file = "tasks/writer_task.txt"
    if os.path.exists(task_file):
        with open(task_file, 'r') as f:
            task = f.read()
        os.remove(task_file)
        
        logging.info(f"Writing: {task}")
        
        # Create documentation
        doc = f"# {task}\n\n## Purpose\nThis does something useful.\n\n## How to use\n1. Run it\n2. Use it\n\n## Notes\nMade with ❤️ by the swarm"
        
        filename = f"docs/{task.replace(' ', '_')}.md"
        with open(filename, 'w') as f:
            f.write(doc)
            
        with open("comms/writer_result.txt", 'w') as f:
            f.write(f"Documented: {filename}")
            
        logging.info(f"Documented: {filename}")
    
    time.sleep(5)
