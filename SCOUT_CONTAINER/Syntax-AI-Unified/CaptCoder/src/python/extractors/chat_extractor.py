"""
Syntax AI CaptCoder - Chat Extractor

Extracts code from chat messages and interactive sessions.
Integrated from:
- /RootBase/Loosies/chat_code_capture.py
- /RootBase/Loosies/chat_code_capture_save.py

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import re
import sys
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field

from ..utils.file_utils import FileUtils
from ..utils.text_utils import TextUtils
from ..utils.validation import ValidationUtils

logger = logging.getLogger(__name__)


@dataclass
class ChatCodeBlock:
    """Represents a code block extracted from chat."""
    code: str
    language: str = "unknown"
    source: str = "chat"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class ChatExtractor:
    """
    Extracts code from chat messages.
    
    Features:
    - Interactive chat mode
    - Code block extraction (backticks, fenced blocks)
    - Language detection
    - File saving with safe filenames
    - TTS feedback (optional)
    - Session history
    """
    
    def __init__(
        self,
        output_dir: str = "generated_code",
        enable_tts: bool = True,
        max_history: int = 100
    ):
        """
        Initialize the ChatExtractor.
        
        Args:
            output_dir: Directory to save extracted code
            enable_tts: Enable text-to-speech feedback
            max_history: Maximum history size
        """
        self.file_utils = FileUtils()
        self.text_utils = TextUtils()
        self.validation = ValidationUtils()
        
        self.output_dir = Path(output_dir)
        self.enable_tts = enable_tts
        self.max_history = max_history
        
        # State
        self._session_history: List[str] = []
        self._extracted_blocks: List[ChatCodeBlock] = []
        
        # Callbacks
        self._code_extracted_callbacks: List[Callable] = []
        self._error_callbacks: List[Callable] = []
        
        # Statistics
        self.stats = {
            "sessions": 0,
            "messages_processed": 0,
            "code_blocks_extracted": 0,
            "files_saved": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"ChatExtractor initialized. Output: {self.output_dir}")
    
    def speak(self, text: str) -> None:
        """Speak text using TTS."""
        if not self.enable_tts:
            return
        
        try:
            # Clean text for shell
            clean_text = text.replace('"', '\\"').replace('$', '\\$').replace('`', "'")
            
            # Try espeak first
            try:
                subprocess.run(
                    ['espeak', '-s', '150', '-p', '50', clean_text],
                    capture_output=True,
                    timeout=10,
                    check=True
                )
            except:
                # Fallback to other methods
                try:
                    subprocess.run(
                        ['say', clean_text],
                        capture_output=True,
                        timeout=10
                    )
                except:
                    pass
            
            logger.info(f"🔊 TTS: {text}")
        except Exception as e:
            logger.warning(f"TTS Error: {e}")
    
    def extract_code_blocks(self, text: str) -> List[ChatCodeBlock]:
        """
        Extract all code blocks from chat text.
        
        Args:
            text: Chat text to extract from
            
        Returns:
            List of ChatCodeBlock objects
        """
        blocks: List[ChatCodeBlock] = []
        
        # Extract fenced code blocks (```python ... ```)
        fenced_pattern = r'```(\w*)\s*([\s\S]*?)```'
        for match in re.finditer(fenced_pattern, text):
            language = match.group(1) or "unknown"
            code = match.group(2).strip()
            if code:
                blocks.append(ChatCodeBlock(
                    code=code,
                    language=language,
                    source="chat",
                    metadata={"type": "fenced"}
                ))
        
        # Extract inline code blocks (`code`)
        inline_pattern = r'`([^`]+)`'
        for match in re.finditer(inline_pattern, text):
            code = match.group(1).strip()
            if code:
                # Detect language from content
                language = self.text_utils.detect_language(code)
                blocks.append(ChatCodeBlock(
                    code=code,
                    language=language,
                    source="chat",
                    metadata={"type": "inline"}
                ))
        
        return blocks
    
    def process_chat_message(self, message: str) -> List[ChatCodeBlock]:
        """
        Process a chat message and extract code.
        
        Args:
            message: Chat message to process
            
        Returns:
            List of extracted ChatCodeBlock objects
        """
        self.stats["messages_processed"] += 1
        
        # Add to history
        self._session_history.append(message)
        if len(self._session_history) > self.max_history:
            self._session_history = self._session_history[-self.max_history:]
        
        # Extract code blocks
        blocks = self.extract_code_blocks(message)
        
        for block in blocks:
            self._extracted_blocks.append(block)
            self.stats["code_blocks_extracted"] += 1
            self._notify_code_extracted(block)
        
        return blocks
    
    def save_code_blocks(
        self,
        blocks: List[ChatCodeBlock],
        context: str = ""
    ) -> List[str]:
        """
        Save code blocks to files.
        
        Args:
            blocks: List of code blocks to save
            context: Optional context for filename generation
            
        Returns:
            List of saved file paths
        """
        saved_files: List[str] = []
        
        for i, block in enumerate(blocks):
            filepath = self.save_code_block(block, context, i)
            if filepath:
                saved_files.append(filepath)
                self.stats["files_saved"] += 1
                self.speak(f"Saved {Path(filepath).name}")
        
        return saved_files
    
    def save_code_block(
        self,
        block: ChatCodeBlock,
        context: str = "",
        index: int = 0
    ) -> str:
        """
        Save a single code block to a file.
        
        Args:
            block: Code block to save
            context: Optional context for filename
            index: Index for naming
            
        Returns:
            Path to the saved file
        """
        try:
            # Generate filename
            if context:
                base_name = self.text_utils.generate_filename_from_text(context)
            else:
                base_name = self.text_utils.generate_filename_from_text(
                    block.code[:50],
                    block.language
                )
            
            # Ensure unique filename
            counter = 0
            filepath = self.output_dir / base_name
            while filepath.exists():
                counter += 1
                filepath = self.output_dir / f"{counter}_{base_name}"
            
            # Add header with metadata
            header = f"""# Extracted by Syntax AI ChatExtractor
# Language: {block.language}
# Source: {block.source}
# Extracted: {block.timestamp}

"""
            
            # Write file
            content = header + block.code
            self.file_utils.write_file(str(filepath), content)
            
            logger.info(f"💾 Saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error saving code block: {e}")
            self._notify_error(f"Save failed for block: {block.code[:50]}", e)
            return ""
    
    def generate_filename(self, base_name: str, extension: str = "py") -> str:
        """
        Generate a safe filename from base name.
        
        Args:
            base_name: Base name for the file
            extension: File extension
            
        Returns:
            Safe filename
        """
        # Clean and sanitize
        name = self.text_utils.generate_filename_from_text(base_name, extension)
        return self.validation.sanitize_filename(name)
    
    def run_interactive(self) -> None:
        """Run in interactive chat mode."""
        self.stats["sessions"] += 1
        logger.info("🎤 LIVE CHAT CAPTURE ACTIVATED!")
        self.speak("Chat code capture activated. Ready to extract code from your chat.")
        logger.info("I'm now reading your chat commands and generating code...")
        logger.info("Paste chat responses containing code blocks (use backticks)")
        logger.info("Type 'exit' to quit\n")
        
        try:
            while True:
                try:
                    user_input = input("📝 PASTE CHAT RESPONSE: ").strip()
                    
                    if user_input.lower() == 'exit':
                        self.speak("Exiting chat capture")
                        break
                    
                    if user_input:
                        # Process the input
                        blocks = self.process_chat_message(user_input)
                        
                        if blocks:
                            saved_files = self.save_code_blocks(blocks, user_input)
                            self.speak(f"Extracted {len(blocks)} code files")
                            logger.info(f"✅ Saved {len(saved_files)} files")
                        else:
                            logger.info("❌ No code blocks found")
                            self.speak("No code blocks found")
                        
                except KeyboardInterrupt:
                    self.speak("Chat capture interrupted")
                    logger.info("\n👋 Exiting...")
                    break
                    
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
        finally:
            logger.info("🛑 Chat capture stopped")
    
    def run_with_command(self, command: str) -> List[ChatCodeBlock]:
        """
        Process a single command and extract code.
        
        Args:
            command: Command/input to process
            
        Returns:
            List of extracted code blocks
        """
        return self.process_chat_message(command)
    
    def process_language_command(self, command: str, language: str) -> List[str]:
        """
        Process a language-specific command.
        
        Args:
            command: The command/description
            language: Target language
            
        Returns:
            List of saved file paths
        """
        # Extract code blocks from command
        blocks = self.extract_code_blocks(command)
        
        if blocks:
            return self.save_code_blocks(blocks, f"{language}_{command[:50]}")
        
        # If no code blocks, generate from description
        if language == "python":
            code = self._generate_python_code(command)
        elif language == "react":
            code = self._generate_react_code(command)
        elif language == "fastapi":
            code = self._generate_fastapi_code(command)
        else:
            code = self._generate_generic_code(command, language)
        
        if code:
            block = ChatCodeBlock(
                code=code,
                language=language,
                source="generated",
                metadata={"from_command": command}
            )
            return self.save_code_blocks([block], command)
        
        return []
    
    def _generate_python_code(self, description: str) -> str:
        """Generate Python code from description."""
        # Simple template-based generation
        class_name = self._description_to_class_name(description)
        
        return f"""# Auto-generated by Syntax AI ChatExtractor
# Description: {description}

class {class_name}:
    '''{description}'''
    
    def __init__(self):
        self.description = "{description}"
        self.status = "generated"
    
    def execute(self):
        '''Execute the main functionality'''
        import logging
        logging.info(f"Executing: {{self.description}}")
        return {{"status": "success", "task": self.description}}


def main():
    processor = {class_name}()
    result = processor.execute()
    logging.info(result)


if __name__ == "__main__":
    main()
"""
    
    def _generate_react_code(self, description: str) -> str:
        """Generate React code from description."""
        component_name = self._description_to_component_name(description)
        
        return f"""// Auto-generated by Syntax AI ChatExtractor
// Description: {description}

import React from 'react';

const {component_name}: React.FC = () => {{
    return (
        <div className="{component_name.lower()}">
            <h3>{description}</h3>
            <p>This component was automatically generated.</p>
            <div className="content">
                {/* Add your component logic here */}
            </div>
        </div>
    );
}};

export default {component_name};
"""
    
    def _generate_fastapi_code(self, description: str) -> str:
        """Generate FastAPI code from description."""
        endpoint_name = description.lower().replace(" ", "_")
        
        return f"""# Auto-generated by Syntax AI ChatExtractor
# Description: {description}

from fastapi import FastAPI

app = FastAPI(title="Auto-Generated API")

@app.get("/{endpoint_name}")
async def {endpoint_name.replace("-", "_")}():
    '''{description}'''
    return {{
        "message": "{description}",
        "status": "implemented",
        "timestamp": "{datetime.now().isoformat()}"
    }}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    
    def _generate_generic_code(self, description: str, language: str) -> str:
        """Generate generic code from description."""
        return f"// Auto-generated code for: {description}\n// Language: {language}\n// Implement this in your {language} project"
    
    def _description_to_class_name(self, description: str) -> str:
        """Convert description to class name."""
        words = re.findall(r'\b\w+\b', description)
        return ''.join(word.capitalize() for word in words) or "AutoGenerated"
    
    def _description_to_component_name(self, description: str) -> str:
        """Convert description to component name."""
        words = re.findall(r'\b\w+\b', description)
        return ''.join(word.capitalize() for word in words) or "AutoComponent"
    
    def _notify_code_extracted(self, block: ChatCodeBlock) -> None:
        """Notify callbacks about extracted code."""
        for callback in self._code_extracted_callbacks:
            try:
                callback(block)
            except Exception as e:
                logger.error(f"Code extracted callback error: {e}")
    
    def _notify_error(self, message: str, error: Exception) -> None:
        """Notify callbacks about errors."""
        for callback in self._error_callbacks:
            try:
                callback(message, error)
            except Exception as e:
                logger.error(f"Error callback error: {e}")
    
    # Callback registration
    def on_code_extracted(self, callback: Callable[[ChatCodeBlock], None]) -> None:
        """Register callback for code extraction events."""
        self._code_extracted_callbacks.append(callback)
    
    def on_error(self, callback: Callable[[str, Exception], None]) -> None:
        """Register callback for errors."""
        self._error_callbacks.append(callback)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "sessions": 0,
            "messages_processed": 0,
            "code_blocks_extracted": 0,
            "files_saved": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }


# Import datetime
import datetime


def main():
    """Run ChatExtractor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ChatExtractor - Extract code from chat messages"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive chat mode"
    )
    parser.add_argument(
        "--command",
        type=str,
        help="Process a single command"
    )
    parser.add_argument(
        "--language",
        type=str,
        help="Target language for code generation"
    )
    parser.add_argument(
        "--output-dir",
        default="generated_code",
        help="Output directory for saved code"
    )
    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="Disable text-to-speech"
    )
    args = parser.parse_args()
    
    extractor = ChatExtractor(
        output_dir=args.output_dir,
        enable_tts=not args.no_tts
    )
    
    if args.interactive:
        extractor.run_interactive()
    
    elif args.command:
        if args.language:
            # Generate code for specific language
            files = extractor.process_language_command(args.command, args.language)
            if files:
                logger.info(f"✅ Generated and saved {len(files)} files")
                for f in files:
                    logger.info(f"  - {f}")
            else:
                logger.info("❌ Failed to generate code")
        else:
            # Extract code from command
            blocks = extractor.process_chat_message(args.command)
            if blocks:
                files = extractor.save_code_blocks(blocks, args.command)
                logger.info(f"✅ Extracted and saved {len(files)} code blocks")
                for f in files:
                    logger.info(f"  - {f}")
            else:
                logger.info("❌ No code blocks found in command")
    
    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    main()
