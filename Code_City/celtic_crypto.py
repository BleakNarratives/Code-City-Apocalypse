
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: hashlib, json, math
# ROLE: Implements Celtic knot-inspired cryptographic weaving
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import hashlib
import json
import math

class CelticKnotWeave:
    """
    Implements Celtic knot-inspired cryptographic weaving
    Each knot represents a multi-dimensional relationship binding
    """
    
    def __init__(self):
        self.knot_registry = {}
        print("🌀 Celtic Crypto Knot Weave Initialized")
    
    def create_knot(self, fiber_a, fiber_b, knot_type="standard"):
        """Create a cryptographic knot between two fibers"""
        
        # Generate knot signature based on both fibers' properties
        knot_seed = f"{fiber_a.fiber_id}{fiber_b.fiber_id}{fiber_a.metadata['content_hash'][:8]}{fiber_b.metadata['content_hash'][:8]}"
        
        knot_id = hashlib.sha3_256(knot_seed.encode()).hexdigest()[:12]
        
        knot = {
            'knot_id': knot_id,
            'fiber_a': fiber_a.fiber_id,
            'fiber_b': fiber_b.fiber_id, 
            'knot_type': knot_type,
            'complexity': self._calculate_knot_complexity(fiber_a, fiber_b),
            'interlocks': self._generate_interlocks(fiber_a, fiber_b),
            'integrity_hash': hashlib.sha3_256(knot_seed.encode()).hexdigest()
        }
        
        self.knot_registry[knot_id] = knot
        print(f"🔗 Celtic Knot {knot_id} woven between {fiber_a.fiber_id[:6]}↔{fiber_b.fiber_id[:6]}")
        
        return knot
    
    def _calculate_knot_complexity(self, fiber_a, fiber_b):
        """Calculate knot complexity based on fiber properties"""
        complexity = 0
        
        # Content length diversity
        length_diff = abs(len(fiber_a.raw_data) - len(fiber_b.raw_data))
        complexity += min(length_diff / 100, 1.0)
        
        # Type diversity bonus
        if fiber_a.metadata['fiber_type'] != fiber_b.metadata['fiber_type']:
            complexity += 0.5
        
        # Owner diversity bonus  
        if fiber_a.owner_id != fiber_b.owner_id:
            complexity += 0.3
            
        return round(min(complexity, 2.0), 2)
    
    def _generate_interlocks(self, fiber_a, fiber_b):
        """Generate interlocking cryptographic patterns"""
        interlocks = []
        
        # Create 3 interlock points (like knot crossings)
        for i in range(3):
            interlock_seed = f"{fiber_a.fiber_id}{fiber_b.fiber_id}{i}"
            interlock_hash = hashlib.sha3_256(interlock_seed.encode()).hexdigest()[:8]
            
            interlock = {
                'position': i,
                'hash': interlock_hash,
                'strength': (i + 1) * 0.3  # Increasing strength
            }
            interlocks.append(interlock)
            
        return interlocks
    
    def verify_knot_integrity(self, knot_id, fiber_a, fiber_b):
        """Verify a knot's integrity hasn't been compromised"""
        if knot_id not in self.knot_registry:
            return False
            
        knot = self.knot_registry[knot_id]
        
        # Recompute expected integrity hash
        knot_seed = f"{fiber_a.fiber_id}{fiber_b.fiber_id}{fiber_a.metadata['content_hash'][:8]}{fiber_b.metadata['content_hash'][:8]}"
        expected_hash = hashlib.sha3_256(knot_seed.encode()).hexdigest()
        
        return knot['integrity_hash'] == expected_hash
    
    def get_knot_web(self, fiber_id):
        """Get all knots connected to a specific fiber"""
        connected_knots = []
        
        for knot_id, knot in self.knot_registry.items():
            if knot['fiber_a'] == fiber_id or knot['fiber_b'] == fiber_id:
                connected_knots.append(knot)
                
        return connected_knots

# Enhanced Loom with Celtic Knots
class CelticDataLoom:
    def __init__(self):
        self.fibers = {}
        self.knot_weave = CelticKnotWeave()
        self.collective_hash = "0" * 64
        print("🌌 CELTIC DATA LOOM - Enhanced with Cryptographic Knots")
    
    def add_fiber(self, fiber):
        """Add fiber with automatic Celtic knot weaving"""
        self.fibers[fiber.fiber_id] = fiber
        
        # Update collective security hash
        components = [self.collective_hash, fiber.fiber_id, fiber.content_hash]
        self.collective_hash = hashlib.sha3_256(''.join(components).encode()).hexdigest()
        
        print(f"🧵 Fiber {fiber.fiber_id[:8]} woven into collective")
        print(f"🔗 Collective Hash: {self.collective_hash[:16]}...")
        
        # Enhanced Celtic knot weaving
        self._celtic_auto_weave(fiber)
    
    def _celtic_auto_weave(self, new_fiber):
        """Create Celtic knots with existing fibers based on complex relationships"""
        knots_created = 0
        
        for existing_id, existing_fiber in self.fibers.items():
            if existing_id != new_fiber.fiber_id:
                # Only create knots between different fiber types for diversity
                if new_fiber.metadata['fiber_type'] != existing_fiber.metadata['fiber_type']:
                    knot = self.knot_weave.create_knot(new_fiber, existing_fiber, "cross-type")
                    knots_created += 1
                
                # Also knot fibers from different owners
                elif new_fiber.owner_id != existing_fiber.owner_id:
                    knot = self.knot_weave.create_knot(new_fiber, existing_fiber, "cross-owner") 
                    knots_created += 1
        
        if knots_created > 0:
            print(f"   🪢 Created {knots_created} Celtic knots")
    
    def extract_fiber(self, fiber_id, owner_id):
        """Extract fiber with Celtic knot verification"""
        if fiber_id not in self.fibers:
            print(f"❌ Fiber {fiber_id[:8]} not found")
            return None
            
        fiber = self.fibers[fiber_id]
        
        # Verify ownership via metadata proof
        expected_owner_hash = hashlib.sha3_256(owner_id.encode()).hexdigest()
        if fiber.metadata['owner_proof'] != expected_owner_hash:
            print(f"🚫 Ownership verification failed for {fiber_id[:8]}")
            return None
        
        # Verify Celtic knot integrity before extraction
        connected_knots = self.knot_weave.get_knot_web(fiber_id)
        valid_knots = 0
        
        for knot in connected_knots:
            other_fiber_id = knot['fiber_b'] if knot['fiber_a'] == fiber_id else knot['fiber_a']
            if other_fiber_id in self.fibers:
                other_fiber = self.fibers[other_fiber_id]
                if self.knot_weave.verify_knot_integrity(knot['knot_id'], fiber, other_fiber):
                    valid_knots += 1
        
        print(f"✅ Ownership verified - {valid_knots}/{len(connected_knots)} Celtic knots intact")
        print(f"📤 Extracting {fiber_id[:8]} from collective weave")
        
        return fiber
    
    def visualize_celtic_weave(self):
        """Enhanced visualization showing Celtic knots"""
        print("\n" + "="*60)
        print("🪢 CELTIC KNOT WEAVE VISUALIZATION")
        print("="*60)
        
        for fiber_id, fiber in self.fibers.items():
            print(f"🎯 {fiber_id[:8]} [{fiber.metadata['fiber_type']}] -> '{fiber.raw_data[:20]}...'")
            
            # Show Celtic knots
            knots = self.knot_weave.get_knot_web(fiber_id)
            for knot in knots[:4]:  # Show max 4 knots
                other = knot['fiber_b'] if knot['fiber_a'] == fiber_id else knot['fiber_a']
                knot_char = "🪢" if knot['knot_type'] == "cross-type" else "🔗"
                print(f"    {knot_char} {other[:8]} (complexity: {knot['complexity']})")
        
        status = self.get_collective_status()
        print(f"\n📊 Collective Security: {status['security_level']}")
        print(f"🔗 Integrity: {status['collective_integrity_hash'][:16]}...")
        print(f"🪢 Total Celtic Knots: {len(self.knot_weave.knot_registry)}")

    def get_collective_status(self):
        """Get enhanced status with Celtic knot metrics"""
        total_knots = len(self.knot_weave.knot_registry)
        avg_knots_per_fiber = total_knots / max(1, len(self.fibers))
        
        return {
            'total_fibers': len(self.fibers),
            'total_celtic_knots': total_knots,
            'knot_density': avg_knots_per_fiber,
            'collective_integrity_hash': self.collective_hash,
            'security_level': self._calculate_security_level(),
            'woven_density': len(self.knot_weave.knot_registry) / max(1, len(self.fibers))
        }
    
    def _calculate_security_level(self):
        """Enhanced security calculation with knot complexity"""
        fiber_count = len(self.fibers)
        knot_count = len(self.knot_weave.knot_registry)
        
        if fiber_count == 0:
            return "EMPTY"
        elif fiber_count == 1:
            return "VULNERABLE_SINGLETON"
        elif knot_count == 0:
            return "UNWOVEN_COLLECTIVE"
        elif knot_count / fiber_count >= 2.0:
            return "CELTIC_FORTIFIED"
        elif knot_count / fiber_count >= 1.0:
            return "STRONG_COLLECTIVE"
        else:
            return "EMERGING_COLLECTIVE"

# Demo the enhanced system
if __name__ == "__main__":
    print("🌌 CELTIC FIBER LOOM DEMO - Enhanced Security")
    print("=" * 60)
    
    from fiber_core import DataFiber
    
    # Create enhanced loom
    celtic_loom = CelticDataLoom()
    
    # Add diverse fibers
    fibers_data = [
        ("Project Odds financial projections 2024", "bleak"),
        ("Addiction research methodology - behavioral patterns", "bleak"), 
        ("Mobile fiber system architecture diagrams", "bleak"),
        ("Uncle Steve's sock mending patterns size 12", "steve"),
        ("Winter survival strategies - below freezing protocols", "bleak"),
        ("Dog care routines - vet appointments and feeding", "bleak"),
        ("Emergency contact information and shelters", "bleak")
    ]
    
    print("\n🎯 WEAVING FIBERS WITH CELTIC KNOTS:")
    for data, owner in fibers_data:
        fiber = DataFiber(data, owner)
        celtic_loom.add_fiber(fiber)
        print("")
    
    # Show enhanced status
    print("\n🏊 ENHANCED COLLECTIVE STATUS:")
    status = celtic_loom.get_collective_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Visualize Celtic weave
    celtic_loom.visualize_celtic_weave()
    
    # Demonstrate secure extraction
    print("\n📤 SECURE EXTRACTION WITH KNOT VERIFICATION:")
    test_fiber_id = list(celtic_loom.fibers.keys())[0]
    extracted = celtic_loom.extract_fiber(test_fiber_id, "bleak")
    
    if extracted:
        print(f"✅ Successfully extracted: {extracted.raw_data}")
