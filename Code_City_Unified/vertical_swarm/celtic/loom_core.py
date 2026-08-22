
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: fiber_core, hashlib, json
# ROLE: Add fiber to loom and update collective security
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

import hashlib
import json
from fiber_core import DataFiber

class DataLoom:
    def __init__(self):
        self.fibers = {}
        self.relationships = []
        self.collective_hash = "0" * 64
        print("🌀 Data Loom Initialized - Ready to Weave")
    
    def add_fiber(self, fiber):
        """Add fiber to loom and update collective security"""
        self.fibers[fiber.fiber_id] = fiber
        
        # Update collective hash (this is the "juice")
        components = [self.collective_hash, fiber.fiber_id, fiber.content_hash]
        self.collective_hash = hashlib.sha3_256(''.join(components).encode()).hexdigest()
        
        print(f"🧵 Fiber {fiber.fiber_id[:8]} woven into collective")
        print(f"🔗 Collective Hash: {self.collective_hash[:16]}...")
        
        # Auto-weave with existing fibers
        self._auto_weave(fiber)
    
    def _auto_weave(self, new_fiber):
        """Automatically create relationships with existing fibers"""
        for existing_id, existing_fiber in self.fibers.items():
            if existing_id != new_fiber.fiber_id:
                # Create relationship based on content similarity
                rel_strength = self._calculate_similarity(new_fiber, existing_fiber)
                if rel_strength > 0.1:  # Minimum similarity threshold
                    relationship = {
                        'fiber_a': new_fiber.fiber_id,
                        'fiber_b': existing_fiber.fiber_id,
                        'strength': rel_strength,
                        'relationship_id': hashlib.sha3_256(
                            f"{new_fiber.fiber_id}{existing_fiber.fiber_id}".encode()
                        ).hexdigest()[:12]
                    }
                    self.relationships.append(relationship)
                    print(f"  🤝 Auto-woven with {existing_fiber.fiber_id[:8]} (strength: {rel_strength:.2f})")
    
    def _calculate_similarity(self, fiber_a, fiber_b):
        """Simple content similarity based on shared words"""
        words_a = set(fiber_a.raw_data.lower().split())
        words_b = set(fiber_b.raw_data.lower().split())
        
        if not words_a or not words_b:
            return 0
            
        intersection = words_a.intersection(words_b)
        union = words_a.union(words_b)
        
        return len(intersection) / len(union)
    
    def extract_fiber(self, fiber_id, owner_id):
        """Extract individual fiber from collective (carrots from juice)"""
        if fiber_id not in self.fibers:
            print(f"❌ Fiber {fiber_id[:8]} not found")
            return None
            
        fiber = self.fibers[fiber_id]
        
        # Verify ownership
        expected_owner_hash = hashlib.sha3_256(owner_id.encode()).hexdigest()
        if fiber.metadata['owner_proof'] != expected_owner_hash:
            print(f"🚫 Ownership verification failed for {fiber_id[:8]}")
            return None
        
        print(f"✅ Ownership verified - extracting {fiber_id[:8]}")
        return fiber
    
    def get_collective_status(self):
        """Get the current state of the woven fabric"""
        return {
            'total_fibers': len(self.fibers),
            'total_relationships': len(self.relationships),
            'collective_integrity_hash': self.collective_hash,
            'security_level': self._calculate_security_level(),
            'woven_density': len(self.relationships) / max(1, len(self.fibers))
        }
    
    def _calculate_security_level(self):
        """Calculate security based on fiber count and relationships"""
        if len(self.fibers) == 0:
            return "EMPTY"
        elif len(self.fibers) == 1:
            return "VULNERABLE_SINGLETON"
        elif len(self.fibers) < 5:
            return "EMERGING_COLLECTIVE"
        else:
            return "STRONG_COLLECTIVE"
    
    def visualize_weave(self):
        """Simple ASCII visualization of the fiber relationships"""
        print("\n" + "="*50)
        print("🧵 DATA LOOM VISUALIZATION")
        print("="*50)
        
        for fiber_id, fiber in self.fibers.items():
            print(f"🎯 {fiber_id[:8]} -> '{fiber.raw_data[:20]}...'")
            
            # Show relationships for this fiber
            related = [r for r in self.relationships 
                      if r['fiber_a'] == fiber_id or r['fiber_b'] == fiber_id]
            
            for rel in related[:3]:  # Show max 3 relationships
                other = rel['fiber_b'] if rel['fiber_a'] == fiber_id else rel['fiber_a']
                print(f"    └── 🤝 {other[:8]} (strength: {rel['strength']:.2f})")
        
        status = self.get_collective_status()
        print(f"\n📊 Collective Security: {status['security_level']}")
        print(f"🔗 Integrity: {status['collective_integrity_hash'][:16]}...")

# Demo the full system
if __name__ == "__main__":
    print("🌌 FIBER LOOM DEMO - Carrot Juice Protocol")
    print("=" * 50)
    
    # Create loom
    loom = DataLoom()
    
    # Add fibers (carrots/socks to the blender)
    fibers_data = [
        ("Project Odds financial data Q4 2024", "bleak"),
        ("Addiction research methodology notes", "bleak"), 
        ("Mobile fiber system architecture", "bleak"),
        ("Uncle Steve's sock mending patterns", "steve"),
        ("Winter survival strategies 2024", "bleak"),
        ("Dog care routines and vet info", "bleak")
    ]
    
    print("\n🎯 ADDING FIBERS TO LOOM:")
    for data, owner in fibers_data:
        fiber = DataFiber(data, owner)
        loom.add_fiber(fiber)
        print("")
    
    # Show collective status
    print("\n🏊 COLLECTIVE STATUS:")
    status = loom.get_collective_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Visualize the weave
    loom.visualize_weave()
    
    # Demonstrate extraction (getting carrots back)
    print("\n📤 EXTRACTION DEMO:")
    test_fiber_id = list(loom.fibers.keys())[0]
    extracted = loom.extract_fiber(test_fiber_id, "bleak")
    
    if extracted:
        print(f"✅ Successfully extracted: {extracted.raw_data}")
    
    # Try wrong owner (should fail)
    print("\n🚫 FAILED EXTRACTION (wrong owner):")
    failed = loom.extract_fiber(test_fiber_id, "wrong_owner")
    if not failed:
        print("✅ Security working - wrong owner rejected")
