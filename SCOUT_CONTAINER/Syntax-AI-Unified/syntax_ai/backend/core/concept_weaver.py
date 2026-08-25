import logging

# concept_weaver.py - The Cross-Domain Pattern Detector

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import hashlib

class ConceptWeaver:
    """Finds deep patterns across law, code, philosophy."""
    def __init__(self, db_path="./weaver_db"):
        # Use a tiny model for mobile efficiency
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2') 
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=db_path
        ))
        self.collection = self.client.get_or_create_collection("concepts")
    
    def weave_concept(self, text, domain, metadata=None):
        """Add concept with vector embedding"""
        embedding = self.encoder.encode(text).tolist()
        
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"domain": domain, **(metadata or {})}],
            ids=[hashlib.sha256(text.encode()).hexdigest()[:16]]
        )
    
    def find_bridges(self, query, n_results=5):
        """Find conceptual bridges across domains"""
        query_embedding = self.encoder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

# Example Test Run (Add this to the end of the file to test)
if __name__ == '__main__':
    weaver = ConceptWeaver()
    
    # [span_0](start_span)Add concepts[span_0](end_span)
    weaver.weave_concept("The fundamental right to challenge unlawful detention.", "Law")
    weaver.weave_concept("An operation where the order of operands matters (A*B != B*A).", "Code/Crypto")
    weaver.weave_concept("The love of fate; accepting all that happens.", "Stoicism")
    
    logging.info("Concepts added.")
    
    # [span_1](start_span)Query for the conceptual bridge[span_1](end_span)
    query = "What is the structural similarity between sovereignty and non-commutative operations?"
    bridges = weaver.find_bridges(query, n_results=3)
    
    logging.info(f"\nQuery: {query}")
    for doc in bridges['documents'][0]:
        logging.info(f"  - Found Bridge: {doc}")
