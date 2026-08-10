import logging

#!/usr/bin/env python3
"""
Main swarm orchestrator - runs on Termux
Simple file-based communication between agents
"""
import os
import json
import time
import threading
from datetime import datetime

class SwarmOrchestrator:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.agents = {}
        self.task_queue = []
        self.communication_log = []
        
        # Create necessary directories
        os.makedirs(os.path.join(project_root, "comms"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "tasks"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
        
        logging.info(f"🎯 Swarm Orchestrator initialized at {project_root}")
        
    def register_agent(self, name, agent_file):
        """Register an agent script"""
        self.agents[name] = {
            'file': agent_file,
            'status': 'idle',
            'last_checkin': datetime.now().isoformat(),
            'notes': []
        }
        logging.info(f"🤖 Registered agent: {name}")
        
    def post_task(self, agent_name, task_description, priority=1):
        """Post a task to an agent"""
        task_id = f"task_{int(time.time())}"
        task = {
            'id': task_id,
            'agent': agent_name,
            'description': task_description,
            'priority': priority,
            'status': 'pending',
            'created': datetime.now().isoformat()
        }
        
        task_file = os.path.join(self.project_root, "tasks", f"{task_id}.json")
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
            
        # Notify agent via note
        self.leave_note(agent_name, f"New task assigned: {task_description}")
        
        logging.info(f"📋 Task posted to {agent_name}: {task_description[:50]}...")
        return task_id
        
    def leave_note(self, agent_name, note):
        """Leave a note for an agent"""
        note_file = os.path.join(self.project_root, "comms", f"{agent_name}_notes.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(note_file, 'a') as f:
            f.write(f"[{timestamp}] {note}\n")
            
        self.communication_log.append({
            'to': agent_name,
            'note': note,
            'time': timestamp
        })
        
    def check_notes(self, agent_name):
        """Check notes for an agent"""
        note_file = os.path.join(self.project_root, "comms", f"{agent_name}_notes.txt")
        if os.path.exists(note_file):
            with open(note_file, 'r') as f:
                notes = f.read()
            # Clear after reading
            open(note_file, 'w').close()
            return notes
        return ""
        
    def log(self, message, level="INFO"):
        """Log swarm activity"""
        log_file = os.path.join(self.project_root, "logs", "swarm.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
            
        if level == "ERROR":
            logging.info(f"🔴 {message}")
        elif level == "WARNING":
            logging.info(f"🟡 {message}")
        else:
            logging.info(f"🔵 {message}")

# Quick setup function
def setup_minimal_swarm():
    """Quick setup with basic agents"""
    swarm = SwarmOrchestrator()
    
    # Register agents (create their files)
    agents = {
        'backend_dev': "Specializes in Python backends. Keeps it simple.",
        'frontend_simplifier': "Uses minimal HTML/CSS. No complex animations.",
        'product_mind': "Breaks features into tiny shippable chunks.",
        'ux_minimalist': "Focus on clarity and function over beauty."
    }
    
    for name, desc in agents.items():
        swarm.register_agent(name, f"agent_{name}.py")
        swarm.leave_note(name, f"Welcome {name}! Your role: {desc}")
        
    return swarm

if __name__ == "__main__":
    logging.info("🚀 Starting swarm setup...")
    swarm = setup_minimal_swarm()
    
    # Example tasks
    swarm.post_task("backend_dev", "Create FastAPI endpoint for user login (email/password only)")
    swarm.post_task("frontend_simplifier", "Create login page with email and password fields only")
    swarm.post_task("product_mind", "List the 3 smallest shippable features for MVP")
    
    logging.info("\n✅ Swarm setup complete!")
    logging.info("📁 Project structure created")
    logging.info("🤖 4 agents registered and waiting for work")
    logging.info("📝 Tasks queued for immediate execution")
    logging.info("\nNext: Run agents individually with: python agent_backend_dev.py")
