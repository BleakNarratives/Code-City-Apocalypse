"""
Syntax AI CaptCoder - Nexus API Server

FastAPI-based server for the Multimodal Command Nexus.
This is the central communication hub for all Syntax AI agents.

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Environment Configuration
NEXUS_PORT = int(os.getenv("NEXUS_API_PORT", 8000))
NEXUS_HOST = os.getenv("NEXUS_API_HOST", "0.0.0.0")
NEXUS_AUTH_ENABLED = os.getenv("NEXUS_AUTH_ENABLED", "False").lower() == "true"
NEXUS_API_KEY = os.getenv("NEXUS_API_KEY", None)
NEXUS_CORS_ORIGINS = os.getenv("NEXUS_CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:5173").split(",")

# ============================================================================
# MODELS
# ============================================================================

class CommandRequest(BaseModel):
    """Request body for command endpoint."""
    raw_input: str
    source_agent: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class CommandResponse(BaseModel):
    """Response from command endpoint."""
    status: str
    action: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str
    timestamp: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: str
    agents: Optional[List[Dict[str, Any]]] = None

@dataclass
class QueuedCommand:
    """Represents a queued command."""
    request_id: str
    command: CommandRequest
    timestamp: str
    retries: int = 0

# ============================================================================
# APPLICATION
# ============================================================================

app = FastAPI(
    title="Multimodal Command Nexus API",
    description="Central communication hub for Syntax AI agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=NEXUS_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory command queue
_command_queue: List[QueuedCommand] = []
_registered_agents: Dict[str, Dict[str, Any]] = {}

# Statistics
_stats = {
    "commands_received": 0,
    "commands_processed": 0,
    "agents_registered": 0,
    "errors": 0,
    "started_at": datetime.now().isoformat()
}


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/command", response_model=CommandResponse)
async def post_command(request: CommandRequest):
    """
    Receive a command from any Syntax AI agent.
    
    All agents communicate through this endpoint.
    Commands are queued and processed asynchronously.
    """
    request_id = f"cmd_{int(time.time() * 1000)}_{len(_command_queue)}"
    timestamp = datetime.now().isoformat()
    
    _stats["commands_received"] += 1
    
    # Create queued command
    queued = QueuedCommand(
        request_id=request_id,
        command=request,
        timestamp=timestamp
    )
    _command_queue.append(queued)
    
    logger.info(f"Command received from {request.source_agent}: {request.raw_input[:50]}...")
    
    # Process the command
    try:
        action, result = await process_command(request, request_id, timestamp)
        _stats["commands_processed"] += 1
        
        # Remove from queue
        _command_queue = [c for c in _command_queue if c.request_id != request_id]
        
        return CommandResponse(
            status="completed",
            action=action,
            result=result,
            request_id=request_id,
            timestamp=timestamp
        )
    except Exception as e:
        _stats["errors"] += 1
        logger.error(f"Error processing command {request_id}: {e}")
        return CommandResponse(
            status="error",
            action="error",
            error=str(e),
            request_id=request_id,
            timestamp=timestamp
        )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat(),
        agents=list(_registered_agents.values())
    )

@app.get("/queue")
async def get_queue():
    """Get current command queue status."""
    return JSONResponse(content={
        "queue_size": len(_command_queue),
        "commands": [{
            "request_id": c.request_id,
            "source_agent": c.command.source_agent,
            "raw_input": c.command.raw_input[:100],
            "timestamp": c.timestamp,
            "retries": c.retries
        } for c in _command_queue]
    })

@app.post("/agents/register")
async def register_agent(agent_info: Dict[str, Any]):
    """Register an agent with the Nexus."""
    agent_id = agent_info.get("name", f"agent_{len(_registered_agents)}")
    
    _registered_agents[agent_id] = {
        **agent_info,
        "registered_at": datetime.now().isoformat(),
        "last_seen": datetime.now().isoformat()
    }
    
    _stats["agents_registered"] += 1
    
    logger.info(f"Agent registered: {agent_id}")
    
    return JSONResponse(content={
        "status": "registered",
        "agent_id": agent_id,
        "timestamp": datetime.now().isoformat()
    })

@app.get("/agents")
async def list_agents():
    """List all registered agents."""
    return JSONResponse(content={
        "agents": list(_registered_agents.values()),
        "count": len(_registered_agents)
    })

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get information about a specific agent."""
    if agent_id not in _registered_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return JSONResponse(content=_registered_agents[agent_id])

@app.get("/stats")
async def get_stats():
    """Get Nexus API statistics."""
    return JSONResponse(content={
        **_stats,
        "queue_size": len(_command_queue),
        "registered_agents": len(_registered_agents)
    })


# ============================================================================
# COMMAND PROCESSING
# ============================================================================

async def process_command(
    request: CommandRequest,
    request_id: str,
    timestamp: str
) -> tuple[str, Dict[str, Any]]:
    """
    Process a command and return action + result.
    
    This is where the magic happens - commands are routed to appropriate handlers.
    """
    raw_input = request.raw_input
    source_agent = request.source_agent
    metadata = request.metadata or {}
    
    # Log the command
    logger.info(f"Processing command {request_id} from {source_agent}: {raw_input[:100]}...")
    
    # Extract intent and action
    action = metadata.get("action") or extract_action(raw_input)
    
    # Route based on action or content
    if action == "bsm_start" or "#bsm" in raw_input.lower():
        return handle_bsm_start(raw_input, source_agent, request_id)
    
    elif action == "bsm_end" or "#bsm-end" in raw_input.lower():
        return handle_bsm_end(raw_input, source_agent, request_id)
    
    elif action == "extract_code" or "extract" in raw_input.lower():
        return handle_extract_code(raw_input, source_agent, request_id)
    
    elif action == "generate_code" or raw_input.startswith("#python") or raw_input.startswith("#react") or raw_input.startswith("#fastapi"):
        return handle_generate_code(raw_input, source_agent, request_id)
    
    elif action == "optimize" or "bitch work" in raw_input.lower():
        return handle_optimize(raw_input, source_agent, request_id)
    
    elif "janenat" in raw_input.lower():
        return handle_janenat(raw_input, source_agent, request_id)
    
    else:
        # Default: echo back or route to appropriate handler
        return handle_generic(raw_input, source_agent, request_id)


def extract_action(raw_input: str) -> str:
    """Extract action from raw input."""
    import re
    
    # Check for explicit action in metadata
    # Check for hashtags
    match = re.search(r'^#(\w+)', raw_input)
    if match:
        return match.group(1)
    
    # Check for commands
    if "janenat" in raw_input.lower():
        return "janenat"
    
    if "#bsm" in raw_input.lower():
        return "bsm_start"
    
    if "#bsm-end" in raw_input.lower():
        return "bsm_end"
    
    return "generic"


def handle_bsm_start(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle Blue Sky Meeting start."""
    # Extract title if available
    title = raw_input.replace("#bsm", "").strip()
    if ":" in title:
        title = title.split(":")[0].strip()
    
    result = {
        "status": "bsm_started",
        "title": title or "Blue Sky Meeting",
        "session_id": request_id,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"BSM started: {title}")
    return "bsm_start", result


def handle_bsm_end(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle Blue Sky Meeting end."""
    result = {
        "status": "bsm_ended",
        "session_id": request_id,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info("BSM ended")
    return "bsm_end", result


def handle_extract_code(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle code extraction request."""
    from ..core.captcoder import SyntaxCaptcoder
    
    # Use CaptCoder to extract code
    captcoder = SyntaxCaptcoder()
    result = captcoder.simulate_live_nat_coding(raw_input)
    
    logger.info(f"Code extracted: {len(result.get('code_snippets', []))} snippets")
    
    return "code_extracted", {
        "snippets": result.get("code_snippets", []),
        "count": len(result.get("code_snippets", [])),
        "request_id": request_id
    }


def handle_generate_code(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle code generation request."""
    # Extract language and description
    if raw_input.startswith("#"):
        parts = raw_input[1:].split(" ", 1)
        language = parts[0] if parts else "python"
        description = parts[1] if len(parts) > 1 else ""
    else:
        language = "python"
        description = raw_input
    
    # For now, return a placeholder
    # In a full implementation, this would call SmartCoder
    result = {
        "language": language,
        "description": description,
        "code": f"# Generated {language} code for: {description}\n# Implement this in SmartCoder module",
        "status": "generated",
        "request_id": request_id
    }
    
    logger.info(f"Code generated for {language}: {description[:50]}...")
    return "code_generated", result


def handle_optimize(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle optimization request."""
    # For now, return placeholder
    # In a full implementation, this would call CodeOptimizer
    result = {
        "status": "optimization_queued",
        "raw_input": raw_input,
        "request_id": request_id,
        "message": "Run CodeOptimizer.run_bitch_work() for full optimization"
    }
    
    logger.info("Optimization requested")
    return "optimize", result


def handle_janenat(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle JaneNat command."""
    # Remove "JaneNat" prefix
    command = raw_input.replace("janenat", "").replace(",", "").strip()
    
    result = {
        "status": "command_routed",
        "command": command,
        "source_agent": source_agent,
        "request_id": request_id,
        "message": f"Command routed to appropriate handler: {command}"
    }
    
    logger.info(f"JaneNat command: {command}")
    return "command_routed", result


def handle_generic(raw_input: str, source_agent: str, request_id: str) -> tuple[str, Dict[str, Any]]:
    """Handle generic command."""
    result = {
        "status": "received",
        "raw_input": raw_input,
        "source_agent": source_agent,
        "request_id": request_id,
        "message": "Command received and queued for processing"
    }
    
    logger.info(f"Generic command from {source_agent}")
    return "queued", result


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the Nexus API server."""
    import uvicorn
    
    logger.info("🚀 Starting Multimodal Command Nexus API...")
    logger.info(f"   Host: {NEXUS_HOST}")
    logger.info(f"   Port: {NEXUS_PORT}")
    logger.info(f"   Auth enabled: {NEXUS_AUTH_ENABLED}")
    logger.info(f"   CORS origins: {NEXUS_CORS_ORIGINS}")
    
    uvicorn.run(
        app,
        host=NEXUS_HOST,
        port=NEXUS_PORT,
        log_level="info",
        reload=False
    )


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()
