
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: email, hashlib, json, logging, os, pathlib, re, shutil, smtplib, ssl, subprocess, time, typing, zipfile
# ROLE: /\\_/\\
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging

# syntax_ai.py - Expanded Syntax AI Prototype: Artistic/Personalization Engine + Automation Beast
# Refs: Blue Sky Meeting Round 2, ModMind Tier 4
import os
import time
import hashlib
import shutil
import zipfile
import subprocess
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any, Dict

try:
    from pygame import mixer as _pygame_mixer  # Optional sound alerts.
except ImportError:  # Headless/code-analysis installs do not need pygame.
    _pygame_mixer = None


class _SilentSound:
    def play(self):
        return None


class _SilentMixer:
    def init(self):
        return None

    def Sound(self, _path):
        return _SilentSound()


import json  # For insights dumps
import re  # For simple code analysis/refactor
from pathlib import Path  # Required for type hinting Path objects

class SyntaxAI:
    def __init__(self, user_id='Bleak', workspace_dir='.'):
        self.user_id = user_id
        self.workspace_dir = workspace_dir
        self.session_count = 0  # Evolves avatar over sessions
        self.avatar = self.generate_avatar()  # Initial face
        self.templates = {"harvard": "Project Echo – AI-Driven Neuro-Immersion..."}  # Expand with more drafts
        self.idle_threshold = 300  # 5min for bitch work/backdraft
        self.last_interaction = time.time()
        # Audio is optional: scanner-only/headless environments should retain
        # the analysis path even when pygame or an audio device is unavailable.
        self._mixer = _pygame_mixer or _SilentMixer()
        try:
            self._mixer.init()
        except Exception:
            self._mixer = _SilentMixer()
        self.goldilocks_zones = {}  # Analyzed optimal spots

    def generate_avatar(self):
        # Evolve face: Hash user_id + session for procedural ASCII art
        seed = hashlib.md5(f"{self.user_id}_{self.session_count}".encode()).hexdigest()[:8]
        eyes = ["^_^", "O_O", "-_-"][int(seed[0], 16) % 3]
        mouth = [" :D ", " :/ ", " :O "][int(seed[1], 16) % 3]
        return f"""
 /\\_/\\
( {eyes} )
( {mouth} )
 Syntax-{seed}
"""

    def toss_files(self, file_types=['.py', '.txt', '.log', '.json', '.zip']):
        # Toss large code/docs/archives: Scan, zip by type, save/email
        archives = {}
        for root, _, files in os.walk(self.workspace_dir):
            for file in files:
                if any(file.endswith(ft) for ft in file_types):
                    ft = file.split('.')[-1]
                    if ft not in archives:
                        archives[ft] = zipfile.ZipFile(f"tossed_{ft}.zip", 'w', zipfile.ZIP_DEFLATED)
                    archives[ft].write(os.path.join(root, file), file)
        for z in archives.values():
            z.close()
        logging.info(f"{self.avatar.strip()}: Tossed archives! Check tossed_*.zip")
        # Optional: Email them
        # self.send_email("bleaknarratives@gmail.com", "Tossed Files", attach=list(archives.keys()))

    def analyze_codebase(self):
        # Process insights: Scan .py files for Goldilocks zones (e.g., long funcs for refactor)
        self.goldilocks_zones = {}
        for root, _, files in os.walk(self.workspace_dir):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        code = f.read()
                        funcs = re.findall(r'def (\w+)\(', code)
                        for func in funcs:
                            # Mock insight: If func name >10 chars, suggest refactor
                            if len(func) > 10:
                                self.goldilocks_zones[func] = "Optimal refactor zone: Too verbose."
        with open('insights.json', 'w') as f:
            json.dump(self.goldilocks_zones, f)
        logging.info(f"{self.avatar.strip()}: Analyzed codebase! Insights in insights.json")

    def optimize_workspace(self):
        # Bitch work: Clean, sort, refactor, updates (mock safe)
        logging.info(f"{self.avatar.strip()}: Starting bitch work...")
        # Empty recycle (mock: clear temp dir)
        shutil.rmtree('__pycache__', ignore_errors=True)
        os.system('rm -rf /tmp/syntax_temp')  # Safe mock
        # Sort/combine files: e.g., merge logs
        logs = [f for f in os.listdir('.') if f.endswith('.log')]
        if logs:
            with open('combined.log', 'w') as combined:
                for log in logs:
                    with open(log, 'r') as lf:
                        combined.write(lf.read() + '\n')
                    os.remove(log)  # Delete after merge
        # Refactor code: Simple stub (e.g., shorten var names in mocks)
        for file in os.listdir('.'):
            if file.endswith('.py'):
                with open(file, 'r+') as f:
                    code = f.read()
                    code = re.sub(r'long_variable_name', 'lvn', code)  # Mock refactor
                    f.seek(0)
                    f.write(code)
                    f.truncate()
        # Updates/upgrades: Mock terminal (e.g., pip list)
        subprocess.run(['pip', 'list'], capture_output=True)  # Safe
        # Keep user updated
        logging.info(f"{self.avatar.strip()}: Workspace optimized! Merged logs, refactored code, cleared caches.")

    def backdraft_prompt(self):
        # Proactive prompt
        self._mixer.Sound('chime.wav').play() if os.path.exists('chime.wav') else logging.info("Chime!")  # Alert
        suggestions = ["Pitch Stanford?", "Toss code?", "Analyze codebase?"]
        return f"{self.avatar.strip()}: Idle! Next: {suggestions[self.session_count % 3]} (y/n)"

    def voice_nat_command(self):
        # Voice/Nat stub: Use input for now (full STT needs speech_recognition)
        command = input(f"{self.avatar.strip()}: Speak nat command: ")
        # Process: e.g., if "optimize", call bitch work
        if "optimize" in command.lower():
            self.optimize_workspace()
        elif "toss" in command.lower():
            self.toss_files()
        # TTS stub: Print for now

    def generate_pitch(self, target):
        pitch = self.templates.get(target, "Generic neuro-immersive pitch...")
        logging.info(f"{self.avatar.strip()}: Generated pitch for {target}")
        return pitch

    def send_email(self, to_email, subject, body, attach=None):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = "echo@modmind.ai"
        msg['To'] = to_email
        msg.set_content(body)
        if attach:
            for a in attach:
                with open(f"tossed_{a}.zip", 'rb') as f:
                    msg.add_attachment(f.read(), maintype='application', subtype='zip', filename=f"tossed_{a}.zip")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("bleaknarratives@gmail.com", "your_app_pass")  # Replace with app pass
            server.send_message(msg)
        logging.info(f"{self.avatar.strip()}: Email sent to {to_email}")

    def analyze_file_content(self, file_path: Path, content: str) -> Dict[str, Any]:
        """
        Analyzes content of a single file for Goldilocks zones (refactoring opportunities).
        Returns a dictionary of insights for that file.
        """
        insights = {
            "goldilocks_zones": [],
            "avatar_message": f"{self.avatar.strip()}: Analyzed {file_path.name}."
        }
        
        if file_path.suffix == '.py':
            funcs = re.findall(r'def (\w+)\(', content)
            for func_name in funcs:
                # Basic insight: If func name >10 chars, suggest refactor
                if len(func_name) > 10:
                    insights["goldilocks_zones"].append({
                        "type": "verbose_function_name",
                        "function": func_name,
                        "message": f"Optimal refactor zone: Function '{func_name}' is too verbose."
                    })
            # Add other Python-specific analysis here
            
        elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
            # Example: Basic check for large functions in JS/TS
            js_funcs = re.findall(r'(function\s+\w+\s*\(|const\s+\w+\s*=\s*\(|class\s+\w+)', content)
            for func_declaration in js_funcs:
                # Mock: if a function declaration is followed by many lines, flag it
                if content.count('\n', content.find(func_declaration), content.find(func_declaration) + 500) > 20: # Crude length check
                     insights["goldilocks_zones"].append({
                        "type": "long_function",
                        "function": func_declaration.strip(),
                        "message": f"Optimal refactor zone: '{func_declaration.strip()}' might be too long."
                    })

        return insights

    def run(self):
        self.session_count += 1
        self.avatar = self.generate_avatar()  # Evolve per run
        logging.info(self.avatar.strip())
        while True:
            # Check idle
            if time.time() - self.last_interaction > self.idle_threshold:
                logging.info(self.backdraft_prompt())
                response = input("?> ")
                self.last_interaction = time.time()
                if response.lower() == 'y':
                    self.optimize_workspace()  # Or other actions
            # Nat/voice loop
            self.voice_nat_command()
            self.last_interaction = time.time()
            time.sleep(10)  # Poll

if __name__ == "__main__":
    syntax = SyntaxAI()
    syntax.analyze_codebase()  # Initial process
    syntax.toss_files()  # Test toss
    syntax.run()