import logging

import os
import time
import re
import requests
from dotenv import load_dotenv

load_dotenv()

# Environment Variables from .env
BSM_TRIGGER = os.getenv("BSM_TRIGGER_TAG", "#bsm")
NEXUS_API_HOST = os.getenv("NEXUS_API_HOST", "127.0.0.1")
NEXUS_API_PORT = os.getenv("NEXUS_API_PORT", 8000)
NEXUS_COMMAND_URL = f"http://{NEXUS_API_HOST}:{NEXUS_API_PORT}/command"

class SyntaxCaptcoder:
    """
    Simulates Syntax Captcoder, monitoring input for the BSM tag and
    extracting code/scripting from 'Live Nat Coding' inputs.
    """
    def __init__(self, nexus_url: str):
        self.nexus_url = nexus_url
        self.is_monitoring = True
        logging.info(f"Captcoder monitoring active. Nexus URL: {nexus_url}")

    def _send_to_nexus(self, raw_input: str):
        """Sends raw input to the Multimodal Command Nexus API."""
        payload = {
            "raw_input": raw_input,
            "source_agent": "Syntax Captcoder"
        }
        try:
            # POST the raw command to the FastAPI backend (nexus_api.py)
            response = requests.post(self.nexus_url, json=payload)
            response.raise_for_status()
            result = response.json()
            logging.info(f"   [Nexus Response] Action: {result.get('action')}")
        except requests.exceptions.RequestException as e:
            logging.info(f"   [Nexus ERROR] Failed to connect to Nexus API: {e}")

    def simulate_live_nat_coding(self, input_text: str):
        """Simulates processing of voice/text input."""
        logging.info(f"\n[CAPTURING] Input: '{input_text.strip()}'")

        # 1. Check for BSM Trigger
        if BSM_TRIGGER in input_text.lower():
            logging.info(f"   [ACTION] BSM Trigger detected! Sending to Nexus for flow initiation.")
            self._send_to_nexus(input_text)
            return

        # 2. Extract Code Snippets (Simulated Live Nat Coding)
        # Pattern: Matches any content between double backticks (`) as a code suggestion
        code_snippets = re.findall(r"``([^`]+)``", input_text)
        
        if code_snippets:
            for snippet in code_snippets:
                cleaned_snippet = snippet.strip()
                logging.info(f"   [CODE EXTRACTED] Snippet: {cleaned_snippet}")
                
                # Send the clean code snippet as a Nat Command (e.g., JaneNat, apply this code)
                nat_command = f"JaneNat, apply code snippet: {cleaned_snippet}"
                self._send_to_nexus(nat_command)

        elif "janenat" in input_text.lower():
             # If no code but a direct JaneNat command, send the whole input to Nexus
            self._send_to_nexus(input_text)
        else:
            logging.info("   [ACTION] No BSM or Code/Nat Command detected. Input ignored.")


# --- PoC Test ---
if __name__ == "__main__":
    captcoder = SyntaxCaptcoder(NEXUS_COMMAND_URL)
    
    # Test 1: BSM Initiation
    captcoder.simulate_live_nat_coding("Okay, let's start the Blue Sky Meeting now #bsm")
    
    # Test 2: Live Nat Coding - Code Extraction
    captcoder.simulate_live_nat_coding(
        "I think the next step is to define the class for the new asset. Let's try ``class EquiLexAsset: pass``"
    )
    
    # Test 3: Direct JaneNat Command (should be routed by Multimodal Nexus)
    captcoder.simulate_live_nat_coding("JaneNat, generate the investor pitch deck.")
