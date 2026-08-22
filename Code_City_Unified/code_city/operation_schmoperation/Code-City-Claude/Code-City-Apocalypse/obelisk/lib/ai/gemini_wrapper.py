#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: google, json,, pathlib
# ROLE: GeminiWrapper class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

import google.generativeai as genai
import json, yaml
from pathlib import Path

class GeminiWrapper:
    def __init__(self, config_path="shared/config/config.yaml"):
        config = yaml.safe_load(Path(config_path).read_text())
        api_key = config['api_keys']['gemini']
        if not api_key:
            raise ValueError("No API key in config.yaml")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate(self, prompt, response_format='text'):
        response = self.model.generate_content(prompt)
        if response_format == 'json':
            try:
                return json.loads(response.text)
            except:
                return {"raw": response.text}
        return response.text
