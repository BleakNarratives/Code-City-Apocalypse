"""
Syntax AI CaptCoder - Livestream Service

Manages livestreaming for Blue Sky Meetings.
Supports multiple providers (restream.io, streamyard, custom).

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Environment Configuration
LIVESTREAM_PROVIDER = os.getenv("LIVESTREAM_PROVIDER", "restream.io")
LIVESTREAM_ENDPOINTS = os.getenv("LIVESTREAM_ENDPOINTS", "youtube,tiktok,instagram").split(",")
LIVESTREAM_API_KEY = os.getenv("LIVESTREAM_API_KEY", None)
RESTREAM_API_KEY = os.getenv("RESTREAM_API_KEY", None)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", None)

@dataclass
class LivestreamConfig:
    """Configuration for a livestream."""
    provider: str
    endpoints: List[str]
    title: str
    description: str
    quality: str = "1080p"
    fps: int = 30
    bitrate: int = 6000
    is_live: bool = False
    stream_url: Optional[str] = None
    recording: bool = False
    recording_path: Optional[str] = None


class LivestreamService:
    """
    Service for managing livestreams.
    
    Supports:
    - Multiple streaming providers
    - Multi-endpoint streaming
    - Recording
    - Session management
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        endpoints: Optional[List[str]] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the LivestreamService.
        
        Args:
            provider: Streaming provider (restream.io, streamyard, custom)
            endpoints: List of streaming endpoints
            api_key: API key for the provider
        """
        self.provider = provider or LIVESTREAM_PROVIDER
        self.endpoints = endpoints or LIVESTREAM_ENDPOINTS
        self.api_key = api_key or self._get_api_key()
        
        # State
        self.is_live = False
        self.is_recording = False
        self.current_stream: Optional[LivestreamConfig] = None
        self.session_id: Optional[str] = None
        self.start_time: Optional[datetime] = None
        
        # Statistics
        self.stats = {
            "sessions_started": 0,
            "sessions_ended": 0,
            "total_duration": 0,
            "errors": 0,
            "endpoints_streamed": 0
        }
        
        logger.info(f"LivestreamService initialized. Provider: {self.provider}")
    
    def _get_api_key(self) -> Optional[str]:
        """Get the API key for the current provider."""
        if self.provider == "restream.io":
            return RESTREAM_API_KEY
        elif self.provider == "youtube":
            return YOUTUBE_API_KEY
        return LIVESTREAM_API_KEY
    
    def start_stream(
        self,
        title: str = "Blue Sky Meeting",
        description: str = "Live coding session with Syntax AI CaptCoder",
        quality: str = "1080p",
        fps: int = 30,
        bitrate: int = 6000,
        record: bool = True
    ) -> bool:
        """
        Start a livestream.
        
        Args:
            title: Stream title
            description: Stream description
            quality: Video quality (720p, 1080p, 4k)
            fps: Frames per second
            bitrate: Bitrate in kbps
            record: Whether to record the stream
            
        Returns:
            True if successful, False otherwise
        """
        if self.is_live:
            logger.warning("Stream is already live")
            return False
        
        if not self.api_key and self.provider != "custom":
            logger.error(f"API key required for {self.provider}")
            return False
        
        try:
            self.session_id = f"stream_{int(time.time())}"
            self.start_time = datetime.now()
            
            # Create stream config
            self.current_stream = LivestreamConfig(
                provider=self.provider,
                endpoints=self.endpoints,
                title=title,
                description=description,
                quality=quality,
                fps=fps,
                bitrate=bitrate,
                is_live=True,
                recording=record
            )
            
            # Provider-specific startup
            if self.provider == "restream.io":
                success = self._start_restream()
            elif self.provider == "youtube":
                success = self._start_youtube()
            elif self.provider == "custom":
                success = self._start_custom()
            else:
                logger.error(f"Unsupported provider: {self.provider}")
                return False
            
            if success:
                self.is_live = True
                self.stats["sessions_started"] += 1
                self.stats["endpoints_streamed"] += len(self.endpoints)
                logger.info(f"Livestream started: {title} ({self.endpoints})")
            
            return success
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Failed to start stream: {e}")
            self.is_live = False
            self.current_stream = None
            return False
    
    def _start_restream(self) -> bool:
        """Start stream on restream.io."""
        try:
            # Restream API endpoints
            url = "https://api.restream.io/v1/channel"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Get channel info
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.current_stream.stream_url = data.get("streamKey")
                logger.info(f"Restream RTMP URL: {data.get('rtmpUrl')}")
                logger.info(f"Stream key: {self.current_stream.stream_url}")
                return True
            else:
                logger.error(f"Restream API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Restream startup failed: {e}")
            return False
    
    def _start_youtube(self) -> bool:
        """Start stream on YouTube Live."""
        try:
            # YouTube Live API
            url = "https://www.googleapis.com/youtube/v3/liveBroadcasts"
            
            params = {
                "part": "snippet,status",
                "key": self.api_key
            }
            
            payload = {
                "snippet": {
                    "title": self.current_stream.title,
                    "description": self.current_stream.description,
                    "scheduledStartTime": datetime.now().isoformat() + "Z"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
            
            response = requests.post(url, params=params, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.current_stream.stream_url = f"https://www.youtube.com/watch?v={data.get('id')}"
                logger.info(f"YouTube Live URL: {self.current_stream.stream_url}")
                return True
            else:
                logger.error(f"YouTube API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"YouTube startup failed: {e}")
            return False
    
    def _start_custom(self) -> bool:
        """Start custom stream (placeholder)."""
        # For custom providers, just log the configuration
        logger.info(f"Custom stream started with endpoints: {self.endpoints}")
        self.current_stream.stream_url = "custom://stream"
        return True
    
    def stop_stream(self) -> bool:
        """Stop the current livestream."""
        if not self.is_live:
            logger.warning("No active stream to stop")
            return False
        
        try:
            # Provider-specific shutdown
            if self.provider == "restream.io":
                success = self._stop_restream()
            elif self.provider == "youtube":
                success = self._stop_youtube()
            elif self.provider == "custom":
                success = self._stop_custom()
            else:
                success = True
            
            if success:
                # Calculate duration
                if self.start_time:
                    duration = (datetime.now() - self.start_time).total_seconds()
                    self.stats["total_duration"] += duration
                    self.stats["sessions_ended"] += 1
                
                self.is_live = False
                self.is_recording = False
                self.current_stream = None
                self.session_id = None
                self.start_time = None
                
                logger.info("Livestream stopped")
            
            return success
            
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Failed to stop stream: {e}")
            return False
    
    def _stop_restream(self) -> bool:
        """Stop stream on restream.io."""
        # For now, just return True
        # In a full implementation, this would call the Restream API
        logger.info("Restream stopped")
        return True
    
    def _stop_youtube(self) -> bool:
        """Stop stream on YouTube Live."""
        # For now, just return True
        # In a full implementation, this would call the YouTube API
        logger.info("YouTube Live stopped")
        return True
    
    def _stop_custom(self) -> bool:
        """Stop custom stream."""
        logger.info("Custom stream stopped")
        return True
    
    def start_recording(self, path: Optional[str] = None) -> bool:
        """Start recording the stream."""
        if self.is_recording:
            logger.warning("Recording is already in progress")
            return False
        
        try:
            self.is_recording = True
            self.current_stream.recording = True
            self.current_stream.recording_path = path or f"/storage/emulated/0/Recordings/{self.session_id}.mp4"
            
            logger.info(f"Recording started: {self.current_stream.recording_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.is_recording = False
            return False
    
    def stop_recording(self) -> bool:
        """Stop recording the stream."""
        if not self.is_recording:
            logger.warning("No active recording to stop")
            return False
        
        try:
            self.is_recording = False
            if self.current_stream:
                self.current_stream.recording = False
            
            logger.info("Recording stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current livestream status."""
        return {
            "is_live": self.is_live,
            "is_recording": self.is_recording,
            "provider": self.provider,
            "endpoints": self.endpoints,
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "current_stream": self.current_stream.to_dict() if self.current_stream else None,
            "stats": self.stats
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get livestream statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "sessions_started": 0,
            "sessions_ended": 0,
            "total_duration": 0,
            "errors": 0,
            "endpoints_streamed": 0
        }


# Add to_dict method to LivestreamConfig
LivestreamConfig.to_dict = lambda self: self.__dict__.copy()


# Singleton instance
_livestream_service: Optional[LivestreamService] = None


def get_livestream_service() -> LivestreamService:
    """Get the singleton LivestreamService instance."""
    global _livestream_service
    if _livestream_service is None:
        _livestream_service = LivestreamService()
    return _livestream_service


def main():
    """Test LivestreamService."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LivestreamService - Test streaming functionality")
    parser.add_argument("--start", action="store_true", help="Start stream")
    parser.add_argument("--stop", action="store_true", help="Stop stream")
    parser.add_argument("--record", action="store_true", help="Start recording")
    parser.add_argument("--stop-record", action="store_true", help="Stop recording")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()
    
    service = get_livestream_service()
    
    if args.start:
        success = service.start_stream(
            title="Syntax AI CaptCoder Test",
            description="Testing livestream functionality"
        )
        if success:
            print("✅ Stream started")
            print(json.dumps(service.get_status(), indent=2))
        else:
            print("❌ Failed to start stream")
    
    elif args.stop:
        success = service.stop_stream()
        if success:
            print("✅ Stream stopped")
        else:
            print("❌ Failed to stop stream")
    
    elif args.record:
        success = service.start_recording()
        if success:
            print("✅ Recording started")
        else:
            print("❌ Failed to start recording")
    
    elif args.stop_record:
        success = service.stop_recording()
        if success:
            print("✅ Recording stopped")
        else:
            print("❌ Failed to stop recording")
    
    elif args.status:
        print(json.dumps(service.get_status(), indent=2))
    
    else:
        # Show current status
        print(json.dumps(service.get_status(), indent=2))


if __name__ == "__main__":
    main()
