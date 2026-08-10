import requests
import os
from UnifiedCodeCity.engine.contracts import SynthesisProvider

class HuggingFaceSynthesisProvider(SynthesisProvider):
    def __init__(self):
        self.api_key = os.environ.get("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/facebook/musicgen-small" # Example lightweight model
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def synthesize(self, prompt: str, hive_state: dict) -> bytes:
        """Queries HF Inference API with prompt and Hive constraints."""
        # TODO: Construct prompt incorporating hive_state (key, tempo)
        payload = {"inputs": f"{prompt}, {hive_state.get('key')} major, {hive_state.get('tempo')} BPM"}
        
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Synthesis failed: {response.text}")
            
        return response.content
