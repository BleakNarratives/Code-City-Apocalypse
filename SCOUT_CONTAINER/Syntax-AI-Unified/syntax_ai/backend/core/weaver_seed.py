```python
# weaver_seed.py 
from sentence_transformers  import SentenceTransformer 
import chromadb 
from chromadb.config  import Settings 

class ConceptWeaver:
    """
    Finds  deep patterns  across law, code, philosophy.
    This  is your 'insider  knowledge bearing' system.
    """
    def  __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Tiny  model
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./weaver_db"
        ))
        self.collection = self.client.get_or_create_collection("concepts")
    
    def  weave_concept(self, text, domain, metadata=None):
        """Add  concept with  vector embedding"""
        embedding = self.encoder.encode(text).tolist()
        
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"domain": domain, **(metadata  or {})}],
            ids=[hashlib.sha256(text.encode()).hexdigest()[:16]]
        )
    
    def  find_bridges(self, query, n_results=5):
        """Find  conceptual bridges  across domains"""
        query_embedding = self.encoder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return  results
```