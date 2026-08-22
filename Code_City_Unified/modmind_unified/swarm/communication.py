
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, json, logging, os, time
# ROLE: File-based communication system for agents
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging

"""
File-based communication system for agents
Simple, works on Termux, no external dependencies
"""
import os
import json
import time
from datetime import datetime

class SwarmComms:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.comms_dir = os.path.join(base_dir, "comms")
        self.tasks_dir = os.path.join(base_dir, "tasks")
        self.logs_dir = os.path.join(base_dir, "logs")
        
        # Create directories
        for d in [self.comms_dir, self.tasks_dir, self.logs_dir]:
            os.makedirs(d, exist_ok=True)
            
    def leave_note(self, to_agent, note, urgent=False):
        """Leave a note for an agent"""
        note_file = os.path.join(self.comms_dir, f"{to_agent}.notes")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        prefix = "🚨 URGENT: " if urgent else ""
        
        with open(note_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {prefix}{note}\n")
            
        # Also log it
        self.log_message(f"Note to {to_agent}: {note[:50]}...")
        
        return True
        
    def check_mailbox(self, agent_name):
        """Check and clear an agent's mailbox"""
        note_file = os.path.join(self.comms_dir, f"{agent_name}.notes")
        
        if not os.path.exists(note_file):
            return ""
            
        with open(note_file, 'r', encoding='utf-8') as f:
            notes = f.read()
            
        # Clear the file after reading
        open(note_file, 'w').close()
        
        return notes
        
    def create_task(self, task_data):
        """Create a task file"""
        task_id = f"task_{int(time.time())}"
        task_file = os.path.join(self.tasks_dir, f"{task_id}.json")
        
        task_data['id'] = task_id
        task_data['created'] = datetime.now().isoformat()
        task_data['status'] = 'pending'
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
            
        # Notify the assigned agent
        if 'assign_to' in task_data:
            self.leave_note(
                task_data['assign_to'], 
                f"New task assigned: {task_data.get('title', 'No title')}",
                urgent=True
            )
            
        return task_id
        
    def get_pending_tasks(self, agent_name=None):
        """Get pending tasks, optionally filtered by agent"""
        tasks = []
        
        for filename in os.listdir(self.tasks_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.tasks_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        task = json.load(f)
                        
                    if task['status'] == 'pending':
                        if agent_name is None or task.get('assign_to') == agent_name:
                            tasks.append(task)
                except:
                    continue
                    
        return tasks
        
    def complete_task(self, task_id, result=None):
        """Mark a task as complete"""
        task_file = os.path.join(self.tasks_dir, f"{task_id}.json")
        
        if not os.path.exists(task_file):
            return False
            
        with open(task_file, 'r', encoding='utf-8') as f:
            task = json.load(f)
            
        task['status'] = 'completed'
        task['completed'] = datetime.now().isoformat()
        if result:
            task['result'] = result
            
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=2, ensure_ascii=False)
            
        # Notify swarm
        self.log_message(f"Task completed: {task_id}")
        
        return True
        
    def log_message(self, message, level="INFO"):
        """Log a message to swarm log"""
        log_file = os.path.join(self.logs_dir, "swarm_comms.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
            
        logging.info(f"[{timestamp}] {message}")
        
    def broadcast(self, message):
        """Broadcast message to all agents"""
        # Get list of agents from existing note files
        for filename in os.listdir(self.comms_dir):
            if filename.endswith('.notes'):
                agent_name = filename.replace('.notes', '')
                self.leave_note(agent_name, f"📢 BROADCAST: {message}")
                
        self.log_message(f"Broadcast: {message}", "BROADCAST")

# Quick utility functions
def send_task(to_agent, task_title, task_details):
    """Quick function to send a task"""
    comms = SwarmComms()
    task_id = comms.create_task({
        'title': task_title,
        'description': task_details,
        'assign_to': to_agent
    })
    logging.info(f"✅ Task sent to {to_agent} (ID: {task_id})")
    return task_id

def check_my_tasks(agent_name):
    """Quick function for agents to check their tasks"""
    comms = SwarmComms()
    tasks = comms.get_pending_tasks(agent_name)
    
    if tasks:
        logging.info(f"📋 {len(tasks)} pending tasks:")
        for task in tasks:
            logging.info(f"  • {task['title']} (ID: {task['id']})")
    else:
        logging.info("✅ No pending tasks")
        
    return tasks
