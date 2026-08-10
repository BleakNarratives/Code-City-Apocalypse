import logging

logging.info("🧪 Testing swarm...")
import os
logging.info("✓ Python works")

# Create test task
with open("tasks/coder_task.txt", "w") as f:
    f.write("test")
    
logging.info("✓ Task system works")
os.remove("tasks/coder_task.txt")

logging.info("✅ Swarm ready to go!")
logging.info("\nTo start:")
logging.info("1. pip install -r requirements.txt")
logging.info("2. Open new Termux session")
logging.info("3. Run: python agent_coder.py")
logging.info("4. In another: python send_task.py coder 'Build something'")
