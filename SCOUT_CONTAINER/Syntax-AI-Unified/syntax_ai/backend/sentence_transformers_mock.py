import logging

"""
Mock implementation of sentence_transformers for Termux compatibility
"""
import numpy as np
import time

class SentenceTransformer:
    def __init__(self, model_name=None):
        self.model_name = model_name or "mock-model"
        logging.info(f"🔧 Using Mock SentenceTransformer: {self.model_name}")
    
    def encode(self, texts, **kwargs):
        """Generate mock embeddings"""
        if isinstance(texts, str):
            texts = [texts]
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Generate consistent mock embeddings based on text content
        embeddings = []
        for text in texts:
            # Create deterministic-ish embedding based on text
            seed = hash(text) % 10000
            np.random.seed(seed)
            embedding = np.random.random(384).astype(np.float32)
            embeddings.append(embedding)
        
        if len(embeddings) == 1:
            return embeddings[0]
        return np.array(embeddings)
    
    def __call__(self, texts):
        return self.encode(texts)

# Mock functions
def util():
    class MockUtil:
        @staticmethod
        def pytorch_cos_sim(vec1, vec2):
            # Mock cosine similarity
            if isinstance(vec1, list) or (hasattr(vec1, 'ndim') and vec1.ndim > 1):
                return np.random.random((len(vec1), len(vec2)))
            return np.random.random()
    
    return MockUtil()

# Create mock module structure
import sys
from types import ModuleType

mock_module = ModuleType('sentence_transformers')
mock_module.SentenceTransformer = SentenceTransformer
mock_module.util = util

sys.modules['sentence_transformers'] = mock_module
