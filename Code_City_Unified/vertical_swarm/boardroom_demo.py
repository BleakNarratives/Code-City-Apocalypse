#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, subprocess, sys
# ROLE: VERTICAL AI // DEMO READY
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: UI (6)
# [/DNA_TAG]

"""
VERTICAL AI // DEMO READY
One file. Eight voices. Your ideas. No bullshit.
"""

import subprocess
import sys
from datetime import datetime

PERSONAS = [
    {"name": "CEO", "color": "33", "role": "revenue & strategy"},
    {"name": "ADVERSARY", "color": "31", "role": "fatal flaws"},
    {"name": "ARCHITECT", "color": "34", "role": "technical feasibility"},
    {"name": "CMO", "color": "32", "role": "market positioning"},
    {"name": "THREAT", "color": "35", "role": "security risks"},
    {"name": "RAP GENIUS", "color": "33", "role": "street-level truth"},
    {"name": "PYTCH", "color": "35", "role": "weird connections"},
    {"name": "TWOIE", "color": "36", "role": "data & numbers"},
]

MODEL = "mistral:7b-instruct"  # change if you use a different model

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def call_model(prompt):
    """Single function to call Ollama."""
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=45
        )
        if result.returncode != 0:
            return f"[error: {result.stderr[:60]}]"
        return result.stdout.strip()
    except Exception as e:
        return f"[error: {str(e)[:60]}]"

def get_persona_response(persona, idea):
    """Build prompt and get response for one persona."""
    prompt = f"""You are {persona['name']}. Your job: {persona['role']}.

User idea: {idea}

Respond in ONE short sentence. Be direct. Be yourself."""
    return call_model(prompt)

def main():
    # Check if Ollama is responsive
    try:
        subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
    except:
        print(color("\n❌ Ollama not running. Start it with: ollama serve\n", "31"))
        sys.exit(1)
    
    print(color("\n" + "="*60, "36"))
    print(color("VERTICAL AI // BOARDROOM DEMO", "36"))
    print(color("="*60 + "\n", "36"))
    
    while True:
        try:
            idea = input(color("\n⚡ your idea: ", "33"))
            if not idea:
                continue
            
            print(color("\n" + "─"*60, "32"))
            
            for p in PERSONAS:
                print(f"\n{color(p['name'].ljust(12), p['color'])} ", end="", flush=True)
                response = get_persona_response(p, idea)
                print(response)
            
            print(color("\n" + "─"*60, "32"))
            
        except KeyboardInterrupt:
            print(color("\n\n👋 later.\n", "31"))
            sys.exit(0)

if __name__ == "__main__":
    main()