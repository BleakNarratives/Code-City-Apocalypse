"""
MODMIND HUB - Fixed Version (No ML Dependencies)
Uses your linguistic fingerprinting instead of sentence_transformers
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import hashlib
import re
from datetime import datetime

# Pydantic schemas
class WeaveKnowledgeRequest(BaseModel):
    content: str
    source: str
    importance: float = 0.5
    metadata: dict = {}

class QueryBridgeRequest(BaseModel):
    query: str
    min_similarity: float = 0.3

# Your linguistic fingerprinting (from ConceptWeaver)
def linguistic_fingerprint(text):
    """Create pattern signature without heavy ML"""
    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower)
    word_lengths = [len(w) for w in words]
    
    return {
        'word_count': len(words),
        'unique_words': len(set(words)),
        'avg_word_len': sum(word_lengths) / len(word_lengths) if word_lengths else 0,
        'contains_negation': any(neg in text_lower for neg in ['not', 'no', 'never']),
        'contains_action': any(act in text_lower for act in ['do', 'make', 'create', 'build']),
        'structure_hash': hashlib.md5(
            ''.join([str(l) for l in word_lengths[:10]]).encode()
        ).hexdigest()[:8]
    }

# Simple in-memory storage for demo
knowledge_fibers = []
concepts = []
bridges = []

app = FastAPI(
    title="ModMind Syntax Hub (Mobile Edition)",
    description="Zero-dependency AI knowledge system",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "ModMind Syntax Hub LIVE", 
        "status": "operational",
        "mode": "zero_dependency",
        "co-developers": ["Barkley", "Buttercup"]
    }

@app.post("/notary/weave")
async def weave_fiber(fiber_data: WeaveKnowledgeRequest):
    """Add knowledge fiber"""
    fiber_id = hashlib.sha256(
        f"{fiber_data.content}{datetime.now()}".encode()
    ).hexdigest()[:16]
    
    fiber = {
        'fiber_id': fiber_id,
        'content': fiber_data.content,
        'source': fiber_data.source,
        'importance': fiber_data.importance,
        'learned_at': datetime.now().isoformat()
    }
    
    knowledge_fibers.append(fiber)
    
    # Also add as concept for weaving
    concept_id = hashlib.sha256(fiber_data.content.encode()).hexdigest()[:16]
    concepts.append({
        'concept_id': concept_id,
        'content': fiber_data.content,
        'domain': fiber_data.source,
        'fingerprint': linguistic_fingerprint(fiber_data.content)
    })
    
    return {"status": "woven", "fiber_id": fiber_id}

@app.get("/notary/recall/{keyword}")
async def recall_memory(keyword: str):
    """Recall knowledge"""
    results = [f for f in knowledge_fibers if keyword.lower() in f['content'].lower()]
    return {"results": results}

@app.post("/weaver/find_bridges")
async def find_bridges(query_data: QueryBridgeRequest):
    """Find conceptual bridges using linguistic fingerprints"""
    query_fp = linguistic_fingerprint(query_data.query)
    
    matches = []
    for concept in concepts:
        similarity = 0.0
        fp = concept['fingerprint']
        
        # Simple similarity calculation
        if query_fp['word_count'] > 0 and fp['word_count'] > 0:
            wc_sim = 1 - abs(query_fp['word_count'] - fp['word_count']) / max(query_fp['word_count'], fp['word_count'])
            similarity += wc_sim * 0.3
        
        if query_fp['structure_hash'] == fp['structure_hash']:
            similarity += 0.4
            
        if query_fp['contains_action'] == fp['contains_action']:
            similarity += 0.15
            
        if query_fp['contains_negation'] == fp['contains_negation']:
            similarity += 0.15
            
        if similarity >= query_data.min_similarity:
            matches.append({
                'content': concept['content'],
                'domain': concept['domain'], 
                'similarity': similarity
            })
    
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    return {"matches": matches}

@app.post("/equilex/transform/{command}")
async def equilex_transform(command: str):
    """Semantic command transformation"""
    transform_map = {
        "blink_twice": "confirm_safety",
        "say_less": "terminate_command", 
        "retro_sanitization": "purge_metadata",
        "bead_rackwards": "reverse_sequence"
    }
    
    if command in transform_map:
        return {
            "input_symbol": command,
            "output_semantic": transform_map[command],
            "action": f"Execute: {transform_map[command]}()"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Unknown command: {command}")

@app.get("/system/status")
async def system_status():
    """Check system health"""
    return {
        "fibers_stored": len(knowledge_fibers),
        "concepts_woven": len(concepts), 
        "bridges_found": len(bridges),
        "environment": "termux_android",
        "canine_support": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
