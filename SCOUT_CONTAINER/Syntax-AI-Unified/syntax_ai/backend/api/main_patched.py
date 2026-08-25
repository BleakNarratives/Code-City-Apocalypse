import logging

"""
Patched version of ModMind API with mock dependencies
"""
import sys
import os

# Add mock support before any other imports
try:
    import sentence_transformers
    logging.info("✅ Using real sentence-transformers")
except ImportError:
    logging.info("🔧 Loading mock sentence-transformers")
    # Import the mock implementation
    import sentence_transformers_mock
    from sentence_transformers_mock import SentenceTransformer
    sys.modules['sentence_transformers'] = sentence_transformers_mock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np

app = FastAPI(
    title="ModMind Syntax Hub",
    description="AI-powered code analysis and syntax validation",
    version="1.0.0"
)

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

class AnalysisResponse(BaseModel):
    issues: List[str]
    complexity: str
    suggestions: List[str]
    embeddings: Optional[List[float]] = None
    status: str

# Initialize the model (mock or real)
try:
    # Try to use real model
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logging.info("🚀 Real sentence transformer loaded")
except:
    # Fallback to mock
    from sentence_transformers_mock import SentenceTransformer
    model = SentenceTransformer('mock-all-MiniLM-L6-v2')
    logging.info("🎭 Mock sentence transformer loaded")

def analyze_code_syntax(code: str, language: str = "python"):
    """Analyze code syntax and provide feedback"""
    issues = []
    suggestions = []
    
    # Basic syntax checks
    lines = code.strip().split('\n')
    
    if len(lines) > 50:
        issues.append("Code might be too long - consider breaking into smaller functions")
        suggestions.append("Refactor into smaller, focused functions")
    
    if any(len(line) > 100 for line in lines):
        issues.append("Some lines are very long")
        suggestions.append("Keep lines under 100 characters for readability")
    
    if "TODO" in code or "FIXME" in code:
        issues.append("Found TODO/FIXME comments")
        suggestions.append("Address pending tasks before deployment")
    
    # Mock complexity analysis
    complexity = "low"
    if len(lines) > 30:
        complexity = "medium"
    if len(lines) > 100:
        complexity = "high"
    
    return issues, suggestions, complexity

@app.get("/")
async def root():
    return {
        "message": "ModMind Syntax Hub API",
        "status": "running", 
        "mode": "mock" if "mock" in str(type(model)).lower() else "real",
        "endpoints": ["/analyze", "/health", "/docs"]
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: CodeRequest):
    """Analyze code and provide AI-powered feedback"""
    try:
        # Generate embeddings
        embeddings = model.encode(request.code)
        
        # Analyze syntax
        issues, suggestions, complexity = analyze_code_syntax(
            request.code, request.language
        )
        
        return AnalysisResponse(
            issues=issues,
            complexity=complexity,
            suggestions=suggestions,
            embeddings=embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings,
            status="analysis_complete"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": "mock" if "mock" in str(type(model)).lower() else "real"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
