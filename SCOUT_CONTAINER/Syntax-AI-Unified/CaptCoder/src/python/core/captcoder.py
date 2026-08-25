"""
Syntax AI CaptCoder - Main CaptCoder Class

This module provides the core CaptCoder functionality, integrating:
- Real-time input monitoring for #BSM (Blue Sky Meeting) tags
- Code snippet extraction from backtick blocks and other formats
- JaneNat command routing to Nexus API
- Multi-modal input support (chat, voice, screen)
- TTS feedback capabilities

Integrated from:
- /RootBase/syntax_captcoder/syntax_captcoder.py
- /RootBase/Loosies/chat_code_capture.py
- /RootBase/Loosies/auto_code_extractor.py

Author: Syntax AI Team
Version: 1.0.0
"""

import logging
import os
import re
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

# Import from utils
from ..utils.file_utils import FileUtils
from ..utils.text_utils import TextUtils
from ..utils.validation import ValidationUtils

# Import from services
from ..services.nexus_client import NexusClient

# Environment Variables from .env
BSM_TRIGGER = os.getenv("BSM_TRIGGER_TAG", "#bsm")
NEXUS_API_HOST = os.getenv("NEXUS_API_HOST", "127.0.0.1")
NEXUS_API_PORT = int(os.getenv("NEXUS_API_PORT", 8000))
NEXUS_COMMAND_URL = f"http://{NEXUS_API_HOST}:{NEXUS_API_PORT}/command"

# TTS Configuration
TTS_ENABLED = os.getenv("TTS_ENABLED", "True").lower() == "true"
TTS_ENGINE = os.getenv("TTS_ENGINE", "espeak")
TTS_SPEED = os.getenv("TTS_SPEED", "150")
TTS_PITCH = os.getenv("TTS_PITCH", "50")

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SyntaxCaptcoder:
    """
    Main CaptCoder class that monitors input for BSM tags, extracts code snippets,
    and routes commands to the Nexus API.
    
    This is the unified entry point for all Syntax AI CaptCoder operations.
    """
    
    def __init__(self, nexus_url: Optional[str] = None, enable_tts: Optional[bool] = None):
        """
        Initialize the SyntaxCaptcoder.
        
        Args:
            nexus_url: URL of the Nexus API (defaults to NEXUS_COMMAND_URL env var)
            enable_tts: Enable text-to-speech feedback (defaults to TTS_ENABLED env var)
        """
        self.nexus_url = nexus_url or NEXUS_COMMAND_URL
        self.is_monitoring = False
        self.enable_tts = enable_tts if enable_tts is not None else TTS_ENABLED
        self.nexus_client = NexusClient(self.nexus_url)
        self.file_utils = FileUtils()
        self.text_utils = TextUtils()
        self.validation = ValidationUtils()
        
        # Callbacks for event handling
        self._bsm_start_callbacks: List[Callable] = []
        self._bsm_end_callbacks: List[Callable] = []
        self._code_extracted_callbacks: List[Callable] = []
        self._command_routed_callbacks: List[Callable] = []
        
        # Statistics
        self.stats = {
            "bsm_sessions": 0,
            "code_snippets_extracted": 0,
            "commands_routed": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }
        
        logger.info(f"Captcoder initialized. Nexus URL: {self.nexus_url}")
        if self.enable_tts:
            self.speak("Syntax AI CaptCoder initialized and ready")
    
    def speak(self, text: str) -> None:
        """
        Speak text using TTS engine.
        
        Args:
            text: The text to speak
        """
        if not self.enable_tts:
            return
        
        try:
            clean_text = text.replace('"', '\\"').replace('$', '\\$')
            if TTS_ENGINE == "espeak":
                subprocess.run(
                    ['espeak', '-s', TTS_SPEED, '-p', TTS_PITCH, clean_text],
                    capture_output=True,
                    timeout=10
                )
            logger.info(f"🔊 TTS: {text}")
        except Exception as e:
            logger.warning(f"TTS Error: {e}")
    
    def _send_to_nexus(self, raw_input: str, source: str = "CaptCoder") -> Optional[Dict]:
        """
        Sends raw input to the Multimodal Command Nexus API.
        
        Args:
            raw_input: The input to send to Nexus
            source: The source agent name
            
        Returns:
            Response from Nexus API or None if failed
        """
        payload = {
            "raw_input": raw_input,
            "source_agent": source,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = self.nexus_client.post_command(payload)
            if response:
                logger.info(f"   [Nexus Response] Action: {response.get('action')}")
                self.stats["commands_routed"] += 1
                self._notify_command_routed(raw_input, response)
            return response
        except Exception as e:
            logger.error(f"   [Nexus ERROR] Failed to connect to Nexus API: {e}")
            self.stats["errors"] += 1
            return None
    
    def _notify_command_routed(self, command: str, response: Dict) -> None:
        """Notify all registered callbacks that a command was routed."""
        for callback in self._command_routed_callbacks:
            try:
                callback(command, response)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def simulate_live_nat_coding(self, input_text: str) -> Dict[str, Any]:
        """
        Simulates processing of voice/text input.
        
        This is the main entry point for processing user input.
        
        Args:
            input_text: The text input to process
            
        Returns:
            Dictionary containing processing results
        """
        result = {
            "input": input_text,
            "bsm_detected": False,
            "code_snippets": [],
            "commands_routed": [],
            "action": "none"
        }
        
        logger.info(f"\n[CAPTURING] Input: '{input_text.strip()}'")
        
        # 1. Check for BSM Trigger
        if BSM_TRIGGER in input_text.lower():
            logger.info(f"   [ACTION] BSM Trigger detected! Sending to Nexus for flow initiation.")
            self._send_to_nexus(input_text)
            result["bsm_detected"] = True
            result["action"] = "bsm_initiated"
            self.stats["bsm_sessions"] += 1
            self._notify_bsm_start(input_text)
            return result
        
        # Check for BSM End
        if "#bsm-end" in input_text.lower() or "end blue sky meeting" in input_text.lower():
            logger.info(f"   [ACTION] BSM End detected!")
            self._notify_bsm_end(input_text)
            result["action"] = "bsm_ended"
            return result
        
        # 2. Extract Code Snippets
        code_snippets = self._extract_code_snippets(input_text)
        
        if code_snippets:
            for snippet in code_snippets:
                cleaned_snippet = snippet.strip()
                logger.info(f"   [CODE EXTRACTED] Snippet: {cleaned_snippet[:50]}...")
                result["code_snippets"].append(cleaned_snippet)
                
                # Send the clean code snippet as a Nat Command
                nat_command = f"JaneNat, apply code snippet: {cleaned_snippet}"
                self._send_to_nexus(nat_command)
                result["commands_routed"].append(nat_command)
                self.stats["code_snippets_extracted"] += 1
                self._notify_code_extracted(cleaned_snippet)
        
        # 3. Check for JaneNat commands (no code but direct command)
        elif "janenat" in input_text.lower():
            self._send_to_nexus(input_text)
            result["commands_routed"].append(input_text)
            result["action"] = "command_routed"
        
        # 4. Check for language-specific commands
        elif self._is_language_command(input_text):
            self._process_language_command(input_text)
            result["action"] = "language_command"
        
        else:
            logger.info("   [ACTION] No BSM, Code, or Nat Command detected. Input ignored.")
            result["action"] = "ignored"
        
        return result
    
    def _extract_code_snippets(self, text: str) -> List[str]:
        """
        Extract code snippets from text.
        
        Supports multiple formats:
        - Backtick blocks: ```python ... ``` or ``` ... ```
        - Inline backticks: `code`
        - Indented blocks (4 spaces or tab)
        
        Args:
            text: The text to extract code from
            
        Returns:
            List of extracted code snippets
        """
        snippets = []
        
        # Pattern 1: Multi-line code blocks with triple backticks
        # Matches ```python ... ``` or ``` ... ```
        code_blocks = re.findall(r'```(?:\w*)?\s*([\s\S]*?)```', text)
        snippets.extend([block.strip() for block in code_blocks if block.strip()])
        
        # Pattern 2: Single-line inline code with single backticks
        inline_codes = re.findall(r'`([^`]+)`', text)
        snippets.extend([code.strip() for code in inline_codes if code.strip()])
        
        # Pattern 3: Indented code blocks (4 spaces or tab at start of line)
        # This matches Python-style indented code
        lines = text.split('\n')
        indented_block = []
        in_block = False
        
        for line in lines:
            if line.startswith('    ') or line.startswith('\t'):
                if not in_block:
                    in_block = True
                    indented_block = []
                indented_block.append(line)
            else:
                if in_block:
                    if indented_block:
                        snippets.append('\n'.join(indented_block).strip())
                    in_block = False
        
        # Handle case where text ends with indented block
        if in_block and indented_block:
            snippets.append('\n'.join(indented_block).strip())
        
        return snippets
    
    def _is_language_command(self, text: str) -> bool:
        """Check if text is a language-specific command like #python, #react, etc."""
        pattern = r'^#(\w+)\s+.*'
        return bool(re.match(pattern, text.strip()))
    
    def _process_language_command(self, text: str) -> None:
        """
        Process language-specific commands.
        
        Commands like:
        - #python create user class
        - #react build component
        - #fastapi create endpoint
        """
        match = re.match(r'^#(\w+)\s+(.*)', text.strip())
        if match:
            language = match.group(1).lower()
            command = match.group(2)
            
            logger.info(f"   [LANGUAGE COMMAND] Language: {language}, Command: {command}")
            
            # Route to appropriate handler
            if language == "python":
                self._handle_python_command(command)
            elif language == "react":
                self._handle_react_command(command)
            elif language == "fastapi":
                self._handle_fastapi_command(command)
            elif language == "form":
                self._handle_form_command(command)
            else:
                # Send to Nexus for generic handling
                self._send_to_nexus(f"#{language} {command}")
    
    def _handle_python_command(self, command: str) -> None:
        """Handle Python-specific commands."""
        # Send to SmartCoder for generation
        nat_command = f"JaneNat, generate Python code: {command}"
        self._send_to_nexus(nat_command)
    
    def _handle_react_command(self, command: str) -> None:
        """Handle React-specific commands."""
        nat_command = f"JaneNat, generate React component: {command}"
        self._send_to_nexus(nat_command)
    
    def _handle_fastapi_command(self, command: str) -> None:
        """Handle FastAPI-specific commands."""
        nat_command = f"JaneNat, generate FastAPI endpoint: {command}"
        self._send_to_nexus(nat_command)
    
    def _handle_form_command(self, command: str) -> None:
        """Handle Form-specific commands."""
        nat_command = f"JaneNat, generate form: {command}"
        self._send_to_nexus(nat_command)
    
    def _notify_bsm_start(self, input_text: str) -> None:
        """Notify all registered callbacks that BSM started."""
        for callback in self._bsm_start_callbacks:
            try:
                callback(input_text)
            except Exception as e:
                logger.error(f"BSM start callback error: {e}")
    
    def _notify_bsm_end(self, input_text: str) -> None:
        """Notify all registered callbacks that BSM ended."""
        for callback in self._bsm_end_callbacks:
            try:
                callback(input_text)
            except Exception as e:
                logger.error(f"BSM end callback error: {e}")
    
    def _notify_code_extracted(self, code_snippet: str) -> None:
        """Notify all registered callbacks that code was extracted."""
        for callback in self._code_extracted_callbacks:
            try:
                callback(code_snippet)
            except Exception as e:
                logger.error(f"Code extracted callback error: {e}")
    
    # Callback registration methods
    def on_bsm_start(self, callback: Callable[[str], None]) -> None:
        """Register a callback for BSM start events."""
        self._bsm_start_callbacks.append(callback)
    
    def on_bsm_end(self, callback: Callable[[str], None]) -> None:
        """Register a callback for BSM end events."""
        self._bsm_end_callbacks.append(callback)
    
    def on_code_extracted(self, callback: Callable[[str], None]) -> None:
        """Register a callback for code extraction events."""
        self._code_extracted_callbacks.append(callback)
    
    def on_command_routed(self, callback: Callable[[str, Dict], None]) -> None:
        """Register a callback for command routed events."""
        self._command_routed_callbacks.append(callback)
    
    def start_monitoring(self) -> None:
        """Start continuous monitoring mode."""
        self.is_monitoring = True
        logger.info("🎤 LIVE MONITORING ACTIVATED!")
        if self.enable_tts:
            self.speak("Live monitoring activated. Ready to capture code and commands.")
        logger.info("I'm now monitoring for BSM tags, code snippets, and JaneNat commands...")
        logger.info("Type 'exit' to quit\n")
    
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring mode."""
        self.is_monitoring = False
        logger.info("🛑 Monitoring stopped")
        if self.enable_tts:
            self.speak("Monitoring stopped")
    
    def run_interactive(self) -> None:
        """
        Run CaptCoder in interactive mode.
        
        Reads input from stdin and processes it in real-time.
        """
        self.start_monitoring()
        
        try:
            while self.is_monitoring:
                try:
                    input_text = input("📝 Input: ").strip()
                    
                    if input_text.lower() == 'exit':
                        self.speak("Exiting CaptCoder")
                        break
                    
                    if input_text:
                        self.simulate_live_nat_coding(input_text)
                        
                except KeyboardInterrupt:
                    self.speak("Monitoring interrupted")
                    break
                    
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
        finally:
            self.stop_monitoring()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "bsm_sessions": 0,
            "code_snippets_extracted": 0,
            "commands_routed": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }


# --- PoC Test ---
def main():
    """Run CaptCoder in test mode."""
    logger.info("🚀 Starting Syntax AI CaptCoder...")
    
    captcoder = SyntaxCaptcoder()
    
    # Test 1: BSM Initiation
    logger.info("\n" + "="*60)
    logger.info("TEST 1: BSM Initiation")
    logger.info("="*60)
    result1 = captcoder.simulate_live_nat_coding("Okay, let's start the Blue Sky Meeting now #bsm")
    logger.info(f"Result: {result1}")
    
    # Test 2: Live Nat Coding - Code Extraction
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Code Extraction")
    logger.info("="*60)
    result2 = captcoder.simulate_live_nat_coding(
        "I think the next step is to define the class for the new asset. Let's try ``class EquiLexAsset: pass``"
    )
    logger.info(f"Result: {result2}")
    
    # Test 3: Direct JaneNat Command
    logger.info("\n" + "="*60)
    logger.info("TEST 3: JaneNat Command")
    logger.info("="*60)
    result3 = captcoder.simulate_live_nat_coding("JaneNat, generate the investor pitch deck.")
    logger.info(f"Result: {result3}")
    
    # Test 4: Language-specific command
    logger.info("\n" + "="*60)
    logger.info("TEST 4: Language Command")
    logger.info("="*60)
    result4 = captcoder.simulate_live_nat_coding("#python create user authentication class")
    logger.info(f"Result: {result4}")
    
    # Test 5: Multi-line code block
    logger.info("\n" + "="*60)
    logger.info("TEST 5: Multi-line Code Block")
    logger.info("="*60)
    result5 = captcoder.simulate_live_nat_coding("""
Here's the implementation:

```python
def calculate_total/assets):
    total = 0
    for asset in assets:
        total += asset.value
    return total
```
    """)
    logger.info(f"Result: {result5}")
    
    # Print statistics
    logger.info("\n" + "="*60)
    logger.info("STATISTICS")
    logger.info("="*60)
    stats = captcoder.get_stats()
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")
    
    logger.info("\n✅ All tests completed!")


if __name__ == "__main__":
    import sys
    
    # Check for interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        captcoder = SyntaxCaptcoder()
        captcoder.run_interactive()
    else:
        main()
