# Author: BleakNarratives
# File: dna_engine.py
# Path: ~/Code_City_Unified/modmind_unified/src/dna_engine.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: ast, datetime, shutil, subprocess
# ROLE: Self-coding mutator. Reads file → prompts LLM → validates → overwrites.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

import ast
import subprocess
import shutil
from datetime import datetime

class DNAEngine:
    """Self-coding mutator. Reads file → prompts LLM → validates → overwrites."""

    def __init__(self, model="mistral"):
        self.model = model

    def _ollama_prompt(self, prompt):
        result = subprocess.run(
            ["ollama", "run", self.model, prompt],
            capture_output=True, text=True, timeout=120
        )
        return result.stdout.strip()

    def mutate(self, file_path, goal):
        with open(file_path, 'r') as f:
            original = f.read()

        # Backup before mutation
        backup = f"{file_path}.bak_{datetime.now().strftime('%H%M%S')}"
        shutil.copy(file_path, backup)
        print(f"[DNA] Backup → {backup}")

        prompt = (
            f"Rewrite the following Python code to add this feature: {goal}\n"
            f"Return ONLY the new Python code. No explanations. No markdown.\n\n"
            f"Original code:\n{original}"
        )

        print(f"[DNA] Prompting {self.model}...")
        new_code = self._ollama_prompt(prompt)

        try:
            ast.parse(new_code)
            with open(file_path, 'w') as f:
                f.write(new_code)
            print(f"[DNA] Mutation successful → {file_path}")
            return True
        except SyntaxError as e:
            print(f"[DNA] Syntax error in mutation — reverting. Error: {e}")
            shutil.copy(backup, file_path)
            return False
