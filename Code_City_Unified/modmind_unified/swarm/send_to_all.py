import logging

import sys
import os

agents = [
    "psychology",
    "legal", 
    "security",
    "tech_guru",
    "marketing",
    "reviewer",
    "coder"
]

if len(sys.argv) < 2:
    logging.info("Usage: python send_to_all.py [your request]")
    logging.info("Example: python send_to_all.py 'Build AI swarm for psychology'")
    sys.exit(1)

task = " ".join(sys.argv[1:])

# Send to all agents
for agent in agents:
    task_file = f"tasks/{agent}_task.txt"
    with open(task_file, 'w') as f:
        f.write(task)
    
    logging.info(f"📨 Sent to {agent}: {task[:30]}...")

logging.info(f"\n✅ Task sent to {len(agents)} agents!")
logging.info("Check comms/*_result.txt for outputs")
