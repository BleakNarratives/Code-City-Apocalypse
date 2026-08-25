"""
Syntax AI CaptCoder - Python Package

Unified code intelligence and extraction system for the Syntax AI ecosystem.

This package provides:
- Real-time code monitoring during Blue Sky Meetings (#BSM)
- Autonomous code extraction from multiple sources
- Intelligent code optimization through the "Bitch Work" protocol
- Multi-language support (Python, TypeScript, JavaScript, Java, C++, SQL, etc.)
- Seamless integration with Nexus API, IDEal, DreamTable Sandbox, and Looking Glass

Version: 1.0.0
Author: Syntax AI Team
License: MIT
"""

from .core.captcoder import SyntaxCaptcoder
from .core.code_monitor import CodeMonitor
from .core.nexus_client import NexusClient
from .core.smart_coder import SmartCoder

from .extractors.code_extractor import CodeExtractor
from .extractors.chat_extractor import ChatExtractor
from .extractors.screen_extractor import ScreenExtractor

from .optimizers.code_optimizer import CodeOptimizer
from .optimizers.pattern_journal import PatternJournal

from .services.livestream import LivestreamService
from .services.sandbox import SandboxService
from .services.looking_glass import LookingGlassService

from .utils.file_utils import FileUtils
from .utils.text_utils import TextUtils
from .utils.validation import ValidationUtils

__version__ = "1.0.0"
__all__ = [
    # Core
    "SyntaxCaptcoder",
    "CodeMonitor",
    "NexusClient",
    "SmartCoder",
    # Extractors
    "CodeExtractor",
    "ChatExtractor",
    "ScreenExtractor",
    # Optimizers
    "CodeOptimizer",
    "PatternJournal",
    # Services
    "LivestreamService",
    "SandboxService",
    "LookingGlassService",
    # Utils
    "FileUtils",
    "TextUtils",
    "ValidationUtils",
]
