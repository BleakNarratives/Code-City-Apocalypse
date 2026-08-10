import logging

import os
import json
import time

class Swarm:
    def __init__(self):
        self.agents = {}
        
    def add_agent(self, name, role):
        self.agents[name] = {
            'role': role,
            'status': 'ready',
            'last_task': None
        }
        logging.info(f"Agent {name} added: {role}")
        
    def send_task(self, agent_name, task):
        task_file = f"tasks/{agent_name}_task.txt"
        with open(task_file, 'w') as f:
            f.write(task)
        logging.info(f"Task sent to {agent_name}")
        
    def check_complete(self, agent_name):
        result_file = f"comms/{agent_name}_result.txt"
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                result = f.read()
            os.remove(result_file)
            return result
        return None

# Quick start
swarm = Swarm()
swarm.add_agent("coder", "Write Python code")
swarm.add_agent("writer", "Write documentation")
swarm.add_agent("tester", "Test functionality")

logging.info("Swarm ready!")
logging.info("Run: python agent_coder.py")
logging.info("Run: python agent_writer.py")
logging.info("Run: python agent_tester.py")
