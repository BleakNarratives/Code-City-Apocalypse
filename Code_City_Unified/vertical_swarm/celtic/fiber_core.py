
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, hashlib, json
# ROLE: Classify content type for relationship weaving
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

import hashlib
import json
from datetime import datetime

class DataFiber:
    def __init__(self, raw_data, owner_id):
        self.raw_data = raw_data
        self.owner_id = owner_id
        self.fiber_id = hashlib.sha3_256(f"{raw_data}{owner_id}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        self.content_hash = hashlib.sha3_256(raw_data.encode()).hexdigest()
        self.timestamp = datetime.now().isoformat()
        
        # ADD THE MISSING METADATA
        self.metadata = {
            'owner_proof': hashlib.sha3_256(owner_id.encode()).hexdigest(),
            'content_hash': self.content_hash,
            'fiber_type': self._classify_content(),
            'size_vector': len(raw_data),
            'temporal_stamp': self.timestamp
        }
    
    def _classify_content(self):
        """Classify content type for relationship weaving"""
        data_lower = self.raw_data.lower()
        if any(word in data_lower for word in ['financial', 'money', 'bank', 'cash']):
            return "financial"
        elif any(word in data_lower for word in ['research', 'study', 'data', 'analysis']):
            return "research" 
        elif any(word in data_lower for word in ['dog', 'pet', 'animal', 'vet']):
            return "animal_care"
        elif any(word in data_lower for word in ['winter', 'cold', 'survival', 'shelter']):
            return "survival"
        elif any(word in data_lower for word in ['sock', 'clothing', 'mend']):
            return "personal_items"
        else:
            return "general"
    
    def to_dict(self):
        return {
            'fiber_id': self.fiber_id,
            'owner': self.owner_id,
            'content_preview': self.raw_data[:30] + '...',
            'integrity_hash': self.content_hash[:16] + '...',
            'fiber_type': self.metadata['fiber_type']
        }

# Quick test
if __name__ == "__main__":
    test = DataFiber("Bleak's secret project data", "bleak")
    print("🧪 Fiber Test:", json.dumps(test.to_dict(), indent=2))
    print("🔐 Metadata:", json.dumps(test.metadata, indent=2))
