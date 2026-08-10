import logging

import os
import subprocess
import signal
import sys

logging.info("🚀 Launching Twins...")

# Change to project directory
os.chdir(os.path.expanduser("~/storage/shared/ai_swarm_project"))

# Create necessary directories
for d in ["eden/blueprints", "eden/workbenches", "eden/orchestrations", 
          "jude/builds", "jude/executions", "jude/outputs",
          "dashboard", "desires"]:
    os.makedirs(d, exist_ok=True)

# Start Eden
logging.info("🧬 Starting Eden...")
eden = subprocess.Popen([sys.executable, "agent_eden.py"], 
                       stdout=open("eden.log", "w"),
                       stderr=open("eden_err.log", "w"))

logging.info(f"Eden PID: {eden.pid}")

# Start Jude
logging.info("⚡ Starting Jude...")
jude = subprocess.Popen([sys.executable, "agent_jude.py"],
                       stdout=open("jude.log", "w"),
                       stderr=open("jude_err.log", "w"))

logging.info(f"Jude PID: {jude.pid}")

logging.info("\n✅ Twins are running!")
logging.info("📝 Eden log: tail -f eden.log")
logging.info("🔧 Jude log: tail -f jude.log")
logging.info("\n💡 Send tasks to Eden:")
logging.info('   echo "Build me an AI workbench" > tasks/eden_task.txt')
logging.info("\nPress Ctrl+C to stop...")

try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("\n🛑 Stopping twins...")
    eden.terminate()
    jude.terminate()
    eden.wait()
    jude.wait()
    logging.info("✅ Twins stopped")
