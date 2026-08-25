import logging

# api/main.py - The ModMind Hub (Architect Blueprint Core)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import sys

# --- GUARANTEED IMPORT FIX (Force Change Directory) ---
try:
    # 1. Calculate the project root path (e.g., /.../syntax_main/backend)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_file_dir, ".."))
    
    # 2. CRUCIAL STEP: Add the root to the system path AND change the CWD.
    sys.path.insert(0, project_root)
    os.chdir(project_root)
    
    # 3. Perform the standard, simple imports (now guaranteed to work)
    from core.syntax_notary import SyntaxNotary
    from core.concept_weaver import ConceptWeaver
    
except Exception as e:
    logging.info(f"FATAL: Module loading failed. Double-check file names and directory structure. Error: {e}")
    sys.exit(1)
# -------------------------------------------------------------------------

# --- Pydantic Schemas for API Endpoints ---
class WeaveKnowledgeRequest(BaseModel):
    content: str
    source: str
    importance: float = 0.5
    metadata: dict = {}

class SynthesizeRequest(BaseModel):
    fiber_ids: list[str]
    insight: str

class QueryBridgeRequest(BaseModel):
    query: str
    min_similarity: float = 0.3


# --- APP INITIALIZATION ---
app = FastAPI(
    title="ModMind Syntax Hub (EquiNex)", 
    version="1.0.0",
    description="The unified service layer for Notary and Weaver Seeds."
)

# Initialize the Seeds (The persistent brain components)
# The relative paths for the DBs now correctly start from the project root thanks to os.chdir()
notary = SyntaxNotary(db_path="./storage/syntax_memory.db")
weaver = ConceptWeaver(db_path="./storage/weaver_memory.db")


# --- ENDPOINTS: SEED A (SYNTAX NOTARY) ---

@app.post("/notary/weave", tags=["Notary (Memory)"])
def weave_fiber(fiber_data: WeaveKnowledgeRequest):
    """Adds a new knowledge fiber to Syntax's immutable journal."""
    fiber_id = notary.weave_knowledge(
        fiber_data.content, 
        fiber_data.source, 
        fiber_data.importance, 
        fiber_data.metadata
    )
    return {"status": "success", "fiber_id": fiber_id, "message": "Knowledge fiber woven and notarized."}

@app.post("/notary/synthesize", tags=["Notary (Memory)"])
def create_synthesis(data: SynthesizeRequest):
    """Syntax creates a new insight by connecting existing fibers."""
    try:
        new_fiber_id = notary.synthesize(data.fiber_ids, data.insight)
        return {"status": "success", "fiber_id": new_fiber_id, "message": "New synthesis notarized."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {e}")

@app.get("/notary/recall", tags=["Notary (Memory)"])
def recall_memory(keyword: str):
    """Recalls knowledge fibers based on a keyword query."""
    results = notary.recall(keyword)
    return {"status": "success", "results": results}


# --- ENDPOINTS: SEED B (CONCEPT WEAVER) ---

@app.post("/weaver/add_concept", tags=["Weaver (Pattern)"])
def weave_concept(concept_data: WeaveKnowledgeRequest):
    """Adds a concept to the Weaver DB and automatically checks for bridges."""
    concept_id = weaver.weave_concept(
        concept_data.content, 
        concept_data.source, 
        concept_data.metadata
    )
    return {"status": "success", "concept_id": concept_id, "message": "Concept woven and bridge detection initiated."}

@app.post("/weaver/find_bridges", tags=["Weaver (Pattern)"])
def find_bridges(query_data: QueryBridgeRequest):
    """Uses linguistic fingerprinting to find conceptual bridges relevant to the query."""
    matches = weaver.find_bridges(query_data.query, query_data.min_similarity)
    return {"status": "success", "query": query_data.query, "matches": matches}

@app.get("/weaver/domain_bridges", tags=["Weaver (Pattern)"])
def get_domain_bridges(domain_a: str, domain_b: str):
    """Retrieves discovered bridges between two specific domains (e.g., law and code)."""
    bridges = weaver.get_domain_bridges(domain_a, domain_b)
    return {"status": "success", "domain_a": domain_a, "domain_b": domain_b, "bridges": bridges}


# --- MODMIND / EQUILLEX INTEGRATION LAYER ---

@app.post("/equilex/transform_command", tags=["EquiLex (Semantic)"])
def equilex_transform(command: str):
    """
    Translates a user-defined symbolic command (Nova.Forge.Loom schema) 
    into a structured machine semantic, acting as the identity verification layer.
    """
    transform_map = {
        "blink_twice": "confirm_safety",
        "say_less": "terminate_command",
        "retro_sanitization": "purge_metadata",
        "bead_rackwards": "reverse_sequence"
    }

    if command in transform_map:
        return {
            "status": "Transformed",
            "input_symbol": command,
            "output_semantic": transform_map[command],
            "action_required": f"Execute internal function: {transform_map[command]}()"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Symbol '{command}' not defined in EquiLex schema.")
