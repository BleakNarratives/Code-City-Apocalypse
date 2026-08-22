#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, subprocess, sys
# ROLE: boardroom_simple.py – One file, eight opinions, no bullshit.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

"""
boardroom_simple.py – One file, eight opinions, no bullshit.
Run with: python boardroom_simple.py
"""

import subprocess
import sys
from datetime import datetime

PERSONAS = [
    {"name": "CEO", "color": "33", 
     "prompt": "You are a CEO. Focus on revenue, scalability, and strategic vision. Be blunt. One sentence."},
    
    {"name": "ADVERSARY", "color": "31", 
     "prompt": "You are an Adversary. Find fatal flaws. Be brutal but accurate. One sentence."},
    
    {"name": "ARCHITECT", "color": "34", 
     "prompt": "You are an Architect. Focus on technical feasibility, debt, and scalability. One sentence."},
    
    {"name": "CMO", "color": "32", 
     "prompt": "You are a CMO. Focus on market positioning, audience, and messaging. One sentence."},
    
    {"name": "THREAT", "color": "35", 
     "prompt": "You are a Threat Modeler. Identify security risks and attack vectors. One sentence."},
    
    {"name": "RAP GENIUS", "color": "33", 
     "prompt": "You are Rap Genius. Deliver insights in rhyme, but keep it tight. One line."},
    
    {"name": "PYTCH", "color": "35", 
     "prompt": "You are Pytch. You think laterally, connect weird dots, speak strangely. One sentence."},
    
    {"name": "TWOIE", "color": "36", 
     "prompt": "You are Twoie. You demand data, numbers, proof. One sentence."},
]

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def get_response(persona, idea):
    """Call Ollama with persona prompt and user idea."""
    full_prompt = f"{persona['prompt']}\n\nUser idea: {idea}\n\nYour response (one sentence):"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:7b-instruct", full_prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return f"[error: {result.stderr[:50]}]"
        return result.stdout.strip()
    except Exception as e:
        return f"[error: {str(e)[:50]}]"

def main():
    print("\033[2J\033[H")  # clear screen
    print(color("=" * 60, "36"))
    print(color("VERTICAL AI BOARDROOM // SIMPLE MODE", "36"))
    print(color("=" * 60, "36"))
    print("Type your idea. Get eight opinions. No fluff.\n")
    
    while True:
        try:
            idea = input(color("\n> your idea: ", "33"))
            if not idea:
                continue
            
            print(color("\n" + "-" * 60, "32"))
            
            for p in PERSONAS:
                print(f"\n{color(p['name'].ljust(12), p['color'])} ", end="", flush=True)
                response = get_response(p, idea)
                print(response)
            
            print(color("\n" + "-" * 60, "32"))
            
        except KeyboardInterrupt:
            print(color("\n\nlater.\n", "31"))
            sys.exit(0)
        except Exception as e:
            print(color(f"\n[error: {e}]", "31"))

if __name__ == "__main__":
    main()