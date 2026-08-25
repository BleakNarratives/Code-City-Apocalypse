"""
Syntax AI CaptCoder - Screen Extractor

Extracts code from screen content using OCR.
For Android/Termux environments.

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import re
import json
import time
import base64
import logging
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from PIL import Image, ImageGrab

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    pytesseract = None

from ..utils.file_utils import FileUtils
from ..utils.text_utils import TextUtils
from ..utils.validation import ValidationUtils

logger = logging.getLogger(__name__)


@dataclass
class ScreenCapture:
    """Represents a screen capture."""
    image: Optional[Image.Image] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    region: Optional[Tuple[int, int, int, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedScreenCode:
    """Represents code extracted from screen."""
    code: str
    language: str = "unknown"
    source: str = "screen"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class ScreenExtractor:
    """
    Extracts code from screen content using OCR.
    
    Features:
    - Screenshot capture
    - OCR-based text extraction
    - Code block detection
    - Region-based capture
    - Monitoring mode
    """
    
    def __init__(
        self,
        output_dir: str = "screen_extracted",
        ocr_lang: str = "eng",
        min_confidence: int = 60
    ):
        """
        Initialize the ScreenExtractor.
        
        Args:
            output_dir: Directory to save extracted code
            ocr_lang: Language for OCR (default: eng)
            min_confidence: Minimum confidence level for OCR results
        """
        self.file_utils = FileUtils()
        self.text_utils = TextUtils()
        self.validation = ValidationUtils()
        
        self.output_dir = Path(output_dir)
        self.ocr_lang = ocr_lang
        self.min_confidence = min_confidence
        
        # State
        self._captures: List[ScreenCapture] = []
        self._extracted_code: List[ExtractedScreenCode] = []
        
        # Callbacks
        self._code_extracted_callbacks: List[Callable] = []
        self._capture_callbacks: List[Callable] = []
        self._error_callbacks: List[Callable] = []
        
        # Statistics
        self.stats = {
            "captures_taken": 0,
            "code_extracted": 0,
            "files_saved": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not OCR_AVAILABLE:
            logger.warning("OCR not available. Install pytesseract and Tesseract OCR.")
        
        logger.info(f"ScreenExtractor initialized. Output: {self.output_dir}")
    
    def capture_screen(
        self,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Optional[ScreenCapture]:
        """
        Capture the screen or a region.
        
        Args:
            region: Optional (x1, y1, x2, y2) region to capture
            
        Returns:
            ScreenCapture or None if error
        """
        if not OCR_AVAILABLE:
            logger.error("OCR not available. Cannot capture screen.")
            return None
        
        try:
            if region:
                # Capture specific region
                x1, y1, x2, y2 = region
                image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            else:
                # Capture entire screen
                image = ImageGrab.grab()
            
            capture = ScreenCapture(
                image=image,
                region=region,
                metadata={
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode
                }
            )
            
            self._captures.append(capture)
            self.stats["captures_taken"] += 1
            self._notify_capture(capture)
            
            return capture
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error capturing screen: {e}")
            self._notify_error("Screen capture failed", e)
            return None
    
    def capture_screenshot(self, path: Optional[str] = None) -> Optional[str]:
        """
        Capture a screenshot and save it.
        
        Args:
            path: Optional path to save (defaults to timestamp-based path)
            
        Returns:
            Path to saved screenshot or None if error
        """
        capture = self.capture_screen()
        
        if capture and capture.image:
            if path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                path = self.output_dir / f"screenshot_{timestamp}.png"
            else:
                path = Path(path)
            
            capture.image.save(str(path))
            logger.info(f"Screenshot saved: {path}")
            return str(path)
        
        return None
    
    def extract_text_from_image(
        self,
        image: Image.Image,
        lang: Optional[str] = None
    ) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            image: PIL Image to extract text from
            lang: OCR language (defaults to self.ocr_lang)
            
        Returns:
            Extracted text
        """
        if not OCR_AVAILABLE:
            return ""
        
        try:
            ocr_lang = lang or self.ocr_lang
            text = pytesseract.image_to_string(image, lang=ocr_lang)
            return text
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return ""
    
    def extract_code_from_capture(
        self,
        capture: ScreenCapture
    ) -> List[ExtractedScreenCode]:
        """
        Extract code from a screen capture.
        
        Args:
            capture: ScreenCapture to extract from
            
        Returns:
            List of ExtractedScreenCode
        """
        if capture.image is None:
            return []
        
        # Extract text from image
        text = self.extract_text_from_image(capture.image)
        
        if not text or not text.strip():
            return []
        
        # Extract code blocks from text
        code_blocks = self.text_utils.extract_code_blocks(text)
        
        extracted: List[ExtractedScreenCode] = []
        
        for block in code_blocks:
            if not block.get("code") or not block["code"].strip():
                continue
            
            screen_code = ExtractedScreenCode(
                code=block["code"],
                language=block.get("language", "unknown"),
                source="screen",
                timestamp=capture.timestamp,
                metadata={
                    "type": block.get("type", "unknown"),
                    "from_capture": capture.timestamp,
                    "region": capture.region
                }
            )
            extracted.append(screen_code)
            self._extracted_code.append(screen_code)
            self.stats["code_extracted"] += 1
            self._notify_code_extracted(screen_code)
        
        return extracted
    
    def capture_and_extract(
        self,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> List[ExtractedScreenCode]:
        """
        Capture screen and extract code.
        
        Args:
            region: Optional region to capture
            
        Returns:
            List of extracted code
        """
        capture = self.capture_screen(region)
        
        if capture:
            return self.extract_code_from_capture(capture)
        
        return []
    
    def save_extracted_code(
        self,
        code: ExtractedScreenCode,
        output_dir: Optional[str] = None
    ) -> str:
        """
        Save extracted screen code to a file.
        
        Args:
            code: ExtractedScreenCode to save
            output_dir: Directory to save to
            
        Returns:
            Path to saved file
        """
        dir_path = Path(output_dir) if output_dir else self.output_dir
        dir_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            
            if code.language and code.language != "unknown":
                ext = self.file_utils.detect_language(code.language)
            else:
                ext = ".py"  # default
            
            filename = f"screen_code_{timestamp}{ext}"
            filepath = dir_path / filename
            
            # Add header with metadata
            header = f"""# Extracted by Syntax AI ScreenExtractor
# Language: {code.language}
# Source: {code.source}
# Extracted: {code.timestamp}
# Region: {code.metadata.get('region', 'fullscreen')}

"""
            
            content = header + code.code
            self.file_utils.write_file(str(filepath), content)
            
            self.stats["files_saved"] += 1
            logger.info(f"Saved screen code: {filepath}")
            
            return str(filepath)
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error saving screen code: {e}")
            self._notify_error(f"Save failed for code: {code.code[:50]}", e)
            return ""
    
    def run_monitoring(
        self,
        interval: float = 5.0,
        region: Optional[Tuple[int, int, int, int]] = None,
        max_captures: int = 100
    ) -> None:
        """
        Run in monitoring mode, capturing screen periodically.
        
        Args:
            interval: Seconds between captures
            region: Optional region to monitor
            max_captures: Maximum captures to keep
        """
        import time
        
        logger.info(f"Starting screen monitoring (interval: {interval}s)")
        
        try:
            capture_count = 0
            
            while True:
                # Capture and extract
                codes = self.capture_and_extract(region)
                
                if codes:
                    for code in codes:
                        self.save_extracted_code(code)
                        logger.info(f"Extracted {len(codes)} code blocks from screen")
                
                capture_count += 1
                
                # Clean up old captures
                if capture_count > max_captures:
                    self._captures = self._captures[-max_captures:]
                
                # Wait for next interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Screen monitoring stopped by user")
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error in monitoring: {e}")
    
    def extract_from_screenshot_file(
        self,
        image_path: str,
        lang: Optional[str] = None
    ) -> List[ExtractedScreenCode]:
        """
        Extract code from a screenshot image file.
        
        Args:
            image_path: Path to the image file
            lang: OCR language
            
        Returns:
            List of extracted code
        """
        try:
            image = Image.open(image_path)
            capture = ScreenCapture(
                image=image,
                metadata={"source_file": image_path}
            )
            return self.extract_code_from_capture(capture)
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error extracting from screenshot file: {e}")
            return []
    
    def extract_from_base64_image(
        self,
        image_data: str,
        lang: Optional[str] = None
    ) -> List[ExtractedScreenCode]:
        """
        Extract code from a base64-encoded image.
        
        Args:
            image_data: Base64-encoded image data
            lang: OCR language
            
        Returns:
            List of extracted code
        """
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            capture = ScreenCapture(image=image)
            return self.extract_code_from_capture(capture)
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Error extracting from base64 image: {e}")
            return []
    
    def _notify_code_extracted(self, code: ExtractedScreenCode) -> None:
        """Notify callbacks about extracted code."""
        for callback in self._code_extracted_callbacks:
            try:
                callback(code)
            except Exception as e:
                logger.error(f"Code extracted callback error: {e}")
    
    def _notify_capture(self, capture: ScreenCapture) -> None:
        """Notify callbacks about captures."""
        for callback in self._capture_callbacks:
            try:
                callback(capture)
            except Exception as e:
                logger.error(f"Capture callback error: {e}")
    
    def _notify_error(self, message: str, error: Exception) -> None:
        """Notify callbacks about errors."""
        for callback in self._error_callbacks:
            try:
                callback(message, error)
            except Exception as e:
                logger.error(f"Error callback error: {e}")
    
    # Callback registration
    def on_code_extracted(self, callback: Callable[[ExtractedScreenCode], None]) -> None:
        """Register callback for code extraction events."""
        self._code_extracted_callbacks.append(callback)
    
    def on_capture(self, callback: Callable[[ScreenCapture], None]) -> None:
        """Register callback for capture events."""
        self._capture_callbacks.append(callback)
    
    def on_error(self, callback: Callable[[str, Exception], None]) -> None:
        """Register callback for errors."""
        self._error_callbacks.append(callback)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "captures_taken": 0,
            "code_extracted": 0,
            "files_saved": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat()
        }


# For PIL imports
from PIL import Image as PILImage


def main():
    """Test ScreenExtractor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ScreenExtractor - Extract code from screen"
    )
    parser.add_argument(
        "--capture",
        action="store_true",
        help="Capture screen and extract code"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Run in monitoring mode"
    )
    parser.add_argument(
        "--screenshot",
        type=str,
        help="Extract code from screenshot file"
    )
    parser.add_argument(
        "--region",
        type=int,
        nargs=4,
        metavar=("X1", "Y1", "X2", "Y2"),
        help="Region to capture (x1 y1 x2 y2)"
    )
    parser.add_argument(
        "--lang",
        default="eng",
        help="OCR language"
    )
    parser.add_argument(
        "--output-dir",
        default="screen_extracted",
        help="Output directory"
    )
    args = parser.parse_args()
    
    extractor = ScreenExtractor(
        output_dir=args.output_dir,
        ocr_lang=args.lang
    )
    
    if args.capture:
        codes = extractor.capture_and_extract(
            region=tuple(args.region) if args.region else None
        )
        
        if codes:
            for code in codes:
                filepath = extractor.save_extracted_code(code)
                logger.info(f"Extracted and saved: {filepath}")
        else:
            logger.info("No code found in screen capture")
    
    elif args.monitor:
        extractor.run_monitoring()
    
    elif args.screenshot:
        codes = extractor.extract_from_screenshot_file(args.screenshot)
        
        if codes:
            for code in codes:
                filepath = extractor.save_extracted_code(code)
                logger.info(f"Extracted and saved: {filepath}")
        else:
            logger.info("No code found in screenshot")
    
    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    if not OCR_AVAILABLE:
        print("Error: OCR not available. Install with:")
        print("  pip install pytesseract pillow")
        print("  sudo apt install tesseract-ocr")
        print("  sudo apt install libtesseract-dev")
    else:
        main()
