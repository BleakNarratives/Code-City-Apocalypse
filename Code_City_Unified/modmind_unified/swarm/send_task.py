import logging

import sys
import os

if len(sys.argv) < 3:
    logging.info("Usage: python send_task.py [agent] [task]")
    logging.info("Agents: coder, writer, tester")
    sys.exit(1)

agent = sys.argv[1]
task = " ".join(sys.argv[2:])

task_file = f"tasks/{agent}_task.txt"
with open(task_file, 'w') as f:
    f.write(task)
    
logging.info(f"Task sent to {agent}: {task}")
logging.info(f"Check comms/{agent}_result.txt for output")
