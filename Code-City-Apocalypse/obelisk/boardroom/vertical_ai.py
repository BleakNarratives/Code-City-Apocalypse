#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: json, obelisk, sys
# ROLE: You are {persona}. Analyze: {docs}
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Code_City'))
from obelisk.lib.ai.gemini_wrapper import GeminiWrapper
import json

class VerticalAI:
    PERSONAS = {
        "CEO": "Strategic vision",
        "CFO": "Financial viability", 
        "CTO": "Technical feasibility",
        "CMO": "Market fit",
        "COO": "Operations"
    }
    
    def __init__(self):
        self.ai = GeminiWrapper()
    
    def analyze(self, documents, personas=None):
        if not personas:
            personas = list(self.PERSONAS.keys())
        results = {}
        for p in personas:
            print(f"  → {p} analyzing...")
            results[p] = self._analyze(documents, p)
        return results
    
    def _analyze(self, docs, persona):
        prompt = f"""You are {persona}. Analyze: {docs}
        
Return JSON: {{"insights": [], "concerns": [], "recommendations": []}}"""
        return self.ai.generate(prompt, 'json')

if __name__ == '__main__':
    vai = VerticalAI()
    result = vai.analyze(["Test doc"], ["CEO"])
    print(json.dumps(result, indent=2))
