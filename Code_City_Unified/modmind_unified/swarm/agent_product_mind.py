
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, logging, os, time
# ROLE: Product Mind Agent
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging

#!/usr/bin/env python3
"""
Product Mind Agent
Breaks everything into tiny shippable chunks
"""
import os
import time
from datetime import datetime

class ProductAgent:
    def __init__(self):
        self.name = "product_mind"
        self.project_root = "."
        
    def check_notes(self):
        note_file = os.path.join(self.project_root, "comms", f"{self.name}_notes.txt")
        if os.path.exists(note_file):
            with open(note_file, 'r') as f:
                notes = f.read()
            open(note_file, 'w').close()
            return notes
        return ""
        
    def break_down_feature(self, feature_description):
        """Break feature into tiny shippable chunks"""
        chunks = []
        
        # Always start with these basics
        chunks.append("1. [15min] Create single HTML file with basic structure")
        chunks.append("2. [30min] Add ONE input field and submit button")
        chunks.append("3. [45min] Connect to ONE backend endpoint")
        chunks.append("4. [30min] Test it works end-to-end")
        chunks.append("5. [15min] Deploy it NOW (even if ugly)")
        
        # Add specific chunks based on feature
        if "login" in feature_description.lower():
            chunks.insert(1, "[20min] Email/password fields only (no validation)")
            chunks.insert(2, "[30min] POST to /login endpoint")
            
        elif "dashboard" in feature_description.lower():
            chunks.insert(1, "[25min] One stats card showing one number")
            chunks.insert(2, "[20min] One table with static data")
            
        elif "user profile" in feature_description.lower():
            chunks.insert(1, "[20min] Display username and email only")
            chunks.insert(2, "[40min] Basic edit form for just name")
            
        return "\n".join(chunks)
        
    def run(self):
        logging.info(f"📊 {self.name} agent started")
        logging.info("PHILOSOPHY: If it takes more than 2 hours, break it down more")
        
        while True:
            notes = self.check_notes()
            if notes:
                logging.info(f"\n📋 Feature request: {notes}")
                
                chunks = self.break_down_feature(notes)
                logging.info(f"\n✅ Broken into shippable chunks:")
                logging.info(chunks)
                
                # Save breakdown
                os.makedirs("docs", exist_ok=True)
                with open("docs/feature_breakdown.md", "w") as f:
                    f.write(f"# Feature: {notes}\n\n## Tiny Chunks:\n{chunks}\n\n")
                    f.write("## RULES:\n")
                    f.write("1. SHIP after each chunk if possible\n")
                    f.write("2. Working > Perfect\n")
                    f.write("3. Ugly but live > Beautiful but local\n")
                
                logging.info("\n📝 Saved to docs/feature_breakdown.md")
            
            time.sleep(15)

if __name__ == "__main__":
    agent = ProductAgent()
    agent.run()
