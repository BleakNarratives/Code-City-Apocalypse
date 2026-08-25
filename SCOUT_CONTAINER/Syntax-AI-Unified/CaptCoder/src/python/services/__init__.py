"""
Syntax AI CaptCoder - Services

This package provides service layer functionality for Syntax AI CaptCoder.
"""

from .nexus_api import app as nexus_app, main as nexus_main
from .nexus_api import get_stats as get_nexus_stats
from .livestream import LivestreamService, LivestreamConfig
from .livestream import get_livestream_service, main as livestream_main
from .sandbox import SandboxService, SandboxTest, SandboxResult
from .sandbox import get_sandbox_service, main as sandbox_main
from .looking_glass import LookingGlassService, VariableInfo, UIElement, LookingGlassPreview
from .looking_glass import get_looking_glass_service, main as looking_glass_main

# For backwards compatibility
NexusAPI = nexus_app

__all__ = [
    # Nexus API
    "nexus_app",
    "nexus_main",
    "get_nexus_stats",
    "NexusAPI",
    # Livestream
    "LivestreamService",
    "LivestreamConfig",
    "get_livestream_service",
    "livestream_main",
    # Sandbox
    "SandboxService",
    "SandboxTest",
    "SandboxResult",
    "get_sandbox_service",
    "sandbox_main",
    # Looking Glass
    "LookingGlassService",
    "VariableInfo",
    "UIElement",
    "LookingGlassPreview",
    "get_looking_glass_service",
    "looking_glass_main",
]
