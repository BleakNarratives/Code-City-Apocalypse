#!/usr/bin/env python3
"""
Gemini API Wrapper - Pure REST (No grpcio)
"""
import requests
import json
import yaml
from pathlib import Path

class GeminiWrapper:
    def __init__(self, config_path=None):
        if config_path is None:
            # Default to a path relative to the current file's location
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        else:
            config_path = Path(config_path)

        config = yaml.safe_load(config_path.read_text())
        self.api_key = config['api_keys']['gemini']
        
        if not self.api_key:
            raise ValueError("No Gemini API key in config.yaml")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash-exp"
    
    def generate(self, prompt, response_format='text'):
        """Generate content via REST API"""
        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code != 200:
                raise Exception(f"API error {response.status_code}: {response.text}")
            
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            
            if response_format == 'json':
                try:
                    return json.loads(text)
                except:
                    return {"raw": text}
            
            return text
            
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")

if __name__ == '__main__':
    wrapper = GeminiWrapper()
    result = wrapper.generate("Say 'Code City is online'")
    print(result)