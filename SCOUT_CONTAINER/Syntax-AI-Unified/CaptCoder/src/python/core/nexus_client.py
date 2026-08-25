"""
Syntax AI CaptCoder - Nexus API Client

Client for communicating with the Multimodal Command Nexus API.
This is the central communication hub for all Syntax AI agents.

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
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

# Environment Configuration
NEXUS_API_HOST = os.getenv("NEXUS_API_HOST", "127.0.0.1")
NEXUS_API_PORT = int(os.getenv("NEXUS_API_PORT", 8000))
NEXUS_API_KEY = os.getenv("NEXUS_API_KEY", None)
NEXUS_HTTPS = os.getenv("NEXUS_HTTPS", "False").lower() == "true"

@dataclass
class NexusResponse:
    """Represents a response from the Nexus API."""
    status: str
    action: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: Optional[str] = None
    request_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NexusClient:
    """
    Client for the Multimodal Command Nexus API.
    
    Handles:
    - POST commands to /command endpoint
    - Agent registration
    - Command routing
    - Response handling
    - Retry logic
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize the NexusClient.
        
        Args:
            base_url: Base URL of Nexus API
            api_key: API key for authentication
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        self.api_key = api_key or NEXUS_API_KEY
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Build base URL
        protocol = "https" if NEXUS_HTTPS or (base_url and base_url.startswith("https://")) else "http"
        host = NEXUS_API_HOST
        port = NEXUS_API_PORT
        
        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            self.base_url = f"{protocol}://{host}:{port}" if port != 80 else f"{protocol}://{host}"
        
        # Endpoints
        self.command_url = f"{self.base_url}/command"
        self.health_url = f"{self.base_url}/health"
        self.agents_url = f"{self.base_url}/agents"
        self.register_url = f"{self.base_url}/agents/register"
        
        # Session
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "SyntaxCaptCoder/1.0.0"
        })
        
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Statistics
        self.stats = {
            "requests_sent": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "retries": 0,
            "last_request_time": None,
            "last_response_time": None
        }
        
        logger.info(f"NexusClient initialized. Base URL: {self.base_url}")
    
    def _make_request(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: int = 10
    ) -> Optional[Dict]:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: Request URL
            data: Form data
            json_data: JSON data
            params: URL parameters
            timeout: Request timeout in seconds
            
        Returns:
            Response as dictionary or None if failed
        """
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            attempt += 1
            
            try:
                start_time = time.time()
                
                response = self.session.request(
                    method=method,
                    url=url,
                    data=data,
                    json=json_data,
                    params=params,
                    timeout=timeout
                )
                
                self.stats["last_response_time"] = time.time() - start_time
                self.stats["requests_sent"] += 1
                
                if response.status_code >= 200 and response.status_code < 300:
                    self.stats["requests_successful"] += 1
                    
                    try:
                        return response.json()
                    except ValueError:
                        return {"status": "success", "message": response.text}
                
                elif response.status_code == 401:
                    logger.error("Nexus API authentication failed")
                    return None
                
                elif response.status_code >= 500:
                    last_error = f"Server error: {response.status_code}"
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay * attempt)
                        self.stats["retries"] += 1
                        continue
                
                else:
                    last_error = f"HTTP error: {response.status_code}"
                    return None
                    
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * attempt)
                    self.stats["retries"] += 1
                    continue
                else:
                    self.stats["requests_failed"] += 1
                    logger.error(f"Nexus API request failed after {attempt} attempts: {last_error}")
                    return None
        
        self.stats["requests_failed"] += 1
        return None
    
    def post_command(self, payload: Dict[str, Any]) -> Optional[NexusResponse]:
        """
        POST a command to the Nexus API.
        
        Args:
            payload: Command payload to send
            
        Returns:
            NexusResponse object or None if failed
        """
        self.stats["last_request_time"] = datetime.now().isoformat()
        
        # Add metadata
        payload_with_meta = {
            **payload,
            "timestamp": datetime.now().isoformat(),
            "source_type": "CaptCoder",
            "version": "1.0.0"
        }
        
        logger.debug(f"Sending command to Nexus: {payload_with_meta}")
        
        response = self._make_request(
            method="POST",
            url=self.command_url,
            json_data=payload_with_meta
        )
        
        if response:
            logger.debug(f"Nexus response: {response}")
            return NexusResponse(
                status=response.get("status", "success"),
                action=response.get("action", "unknown"),
                data=response.get("data"),
                message=response.get("message"),
                timestamp=response.get("timestamp"),
                request_id=response.get("request_id")
            )
        
        return None
    
    def register_agent(self, agent_info: Dict[str, Any]) -> Optional[Dict]:
        """
        Register this agent with the Nexus API.
        
        Args:
            agent_info: Information about the agent to register
            
        Returns:
            Registration response or None if failed
        """
        default_info = {
            "name": "SyntaxCaptCoder",
            "version": "1.0.0",
            "type": "code_extractor",
            "capabilities": [
                "code_extraction",
                "bsm_monitoring",
                "code_optimization",
                "code_generation"
            ],
            "description": "Unified code intelligence and extraction system"
        }
        
        payload = {**default_info, **agent_info}
        
        return self._make_request(
            method="POST",
            url=self.register_url,
            json_data=payload
        )
    
    def get_health(self) -> Optional[Dict]:
        """
        Check Nexus API health.
        
        Returns:
            Health status or None if failed
        """
        return self._make_request(
            method="GET",
            url=self.health_url
        )
    
    def list_agents(self) -> Optional[List[Dict]]:
        """
        List all registered agents.
        
        Returns:
            List of agent info or None if failed
        """
        response = self._make_request(
            method="GET",
            url=self.agents_url
        )
        
        if response and "agents" in response:
            return response["agents"]
        
        return None
    
    def is_available(self) -> bool:
        """
        Check if Nexus API is available.
        
        Returns:
            True if API is responsive, False otherwise
        """
        try:
            health = self.get_health()
            return health is not None and health.get("status") == "healthy"
        except:
            return False
    
    def wait_for_available(self, timeout: int = 30, interval: float = 1.0) -> bool:
        """
        Wait for Nexus API to become available.
        
        Args:
            timeout: Maximum time to wait in seconds
            interval: Time between checks in seconds
            
        Returns:
            True if API became available, False if timeout reached
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_available():
                return True
            time.sleep(interval)
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset client statistics."""
        self.stats = {
            "requests_sent": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "retries": 0,
            "last_request_time": None,
            "last_response_time": None
        }


# Singleton instance
_nexus_client: Optional[NexusClient] = None


def get_nexus_client() -> NexusClient:
    """Get the singleton NexusClient instance."""
    global _nexus_client
    if _nexus_client is None:
        _nexus_client = NexusClient()
    return _nexus_client


def main():
    """Test NexusClient functionality."""
    import argparse
    
    parser = argparse.ArgumentParser(description="NexusClient - Test Nexus API connection")
    parser.add_argument("--test-command", action="store_true", help="Test posting a command")
    parser.add_argument("--check-health", action="store_true", help="Check API health")
    parser.add_argument("--list-agents", action="store_true", help="List registered agents")
    args = parser.parse_args()
    
    client = NexusClient()
    
    if args.check_health:
        health = client.get_health()
        if health:
            logger.info(f"Nexus API Health: {health}")
        else:
            logger.error("Failed to check Nexus API health")
    
    if args.list_agents:
        agents = client.list_agents()
        if agents:
            logger.info(f"Registered Agents: {len(agents)}")
            for agent in agents:
                logger.info(f"  - {agent.get('name')} v{agent.get('version')}")
        else:
            logger.error("Failed to list agents")
    
    if args.test_command:
        payload = {
            "raw_input": "test command from NexusClient",
            "source_agent": "NexusClient-Test"
        }
        response = client.post_command(payload)
        if response:
            logger.info(f"Command Response: {response.to_dict()}")
        else:
            logger.error("Failed to post command")
    
    # Default: check health
    if not any([args.test_command, args.check_health, args.list_agents]):
        health = client.get_health()
        if health:
            logger.info(f"Nexus API is healthy: {health}")
        else:
            logger.warning("Nexus API is not responding")


if __name__ == "__main__":
    main()
