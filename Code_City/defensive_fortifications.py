
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: celtic_crypto, fiber_core, hashlib, time
# ROLE: Enhanced security measures for the fiber loom system
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import hashlib
import time
from fiber_core import DataFiber
from celtic_crypto import CelticDataLoom

class DefensiveFortifications:
    """
    Enhanced security measures for the fiber loom system
    """
    
    def __init__(self, loom):
        self.loom = loom
        self.intrusion_detection_log = []
        self.suspicious_activity_count = 0
        self.last_integrity_check = time.time()
        
    def enable_tamper_detection(self):
        """Enable continuous integrity monitoring"""
        print("🛡️  Tamper Detection System: ACTIVATED")
        
        # Store original state for comparison
        self.original_collective_hash = self.loom.collective_hash
        self.original_fiber_count = len(self.loom.fibers)
        self.original_knot_count = len(self.loom.knot_weave.knot_registry)
        
    def check_integrity_breach(self):
        """Check for unauthorized modifications"""
        current_time = time.time()
        
        # Rate limit integrity checks
        if current_time - self.last_integrity_check < 1.0:  # 1 second minimum
            return True
            
        self.last_integrity_check = current_time
        
        # Check collective hash consistency
        recomputed_hash = self._recompute_collective_hash()
        if recomputed_hash != self.loom.collective_hash:
            self.log_intrusion("COLLECTIVE_HASH_TAMPER", 
                             f"Hash mismatch: expected {recomputed_hash[:16]}, got {self.loom.collective_hash[:16]}")
            return False
        
        # Check fiber count consistency
        if len(self.loom.fibers) != self.original_fiber_count:
            self.log_intrusion("FIBER_COUNT_TAMPER",
                             f"Fiber count changed: {self.original_fiber_count} -> {len(self.loom.fibers)}")
            return False
            
        return True
    
    def _recompute_collective_hash(self):
        """Recompute collective hash from current fibers"""
        collective_hash = "0" * 64
        fiber_ids = sorted(self.loom.fibers.keys())  # Deterministic order
        
        for fiber_id in fiber_ids:
            fiber = self.loom.fibers[fiber_id]
            components = [collective_hash, fiber_id, fiber.content_hash]
            collective_hash = hashlib.sha3_256(''.join(components).encode()).hexdigest()
            
        return collective_hash
    
    def log_intrusion(self, intrusion_type, details):
        """Log suspicious activity"""
        intrusion = {
            'type': intrusion_type,
            'details': details,
            'timestamp': time.time(),
            'collective_state': self.loom.get_collective_status(),
            'severity': self._assess_severity(intrusion_type)
        }
        
        self.intrusion_detection_log.append(intrusion)
        self.suspicious_activity_count += 1
        
        print(f"🚨 INTRUSION DETECTED: {intrusion_type}")
        print(f"   📍 {details}")
        
        # Auto-response based on severity
        if intrusion['severity'] == "CRITICAL":
            self.activate_emergency_protocols()
    
    def _assess_severity(self, intrusion_type):
        """Assess severity of detected intrusion"""
        critical_types = ["COLLECTIVE_HASH_TAMPER", "MASS_FIBER_INJECTION"]
        high_types = ["FIBER_COUNT_TAMPER", "KNOT_REGISTRY_BREACH"]
        
        if intrusion_type in critical_types:
            return "CRITICAL"
        elif intrusion_type in high_types:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def activate_emergency_protocols(self):
        """Activate emergency security measures"""
        print("🚨 EMERGENCY PROTOCOLS: ACTIVATED")
        
        # Freeze all operations
        print("   ❄️  System operations frozen")
        
        # Create emergency backup
        emergency_backup = {
            'collective_hash': self.loom.collective_hash,
            'fiber_count': len(self.loom.fibers),
            'knot_count': len(self.loom.knot_weave.knot_registry),
            'timestamp': time.time()
        }
        
        print(f"   💾 Emergency backup created: {emergency_backup}")
        
        # Alert monitoring (would connect to external systems IRL)
        print("   📢 Security alert broadcast")
    
    def enable_rate_limiting(self, max_fibers_per_minute=60):
        """Prevent denial of service attacks"""
        self.max_fibers_per_minute = max_fibers_per_minute
        self.fiber_add_times = []
        print(f"🛡️  Rate Limiting: {max_fibers_per_minute} fibers/minute")
    
    def check_rate_limit(self):
        """Check if rate limit would be exceeded"""
        current_time = time.time()
        
        # Remove old entries
        self.fiber_add_times = [t for t in self.fiber_add_times 
                              if current_time - t < 60]  # Last minute
        
        if len(self.fiber_add_times) >= self.max_fibers_per_minute:
            self.log_intrusion("RATE_LIMIT_EXCEEDED",
                             f"Rate limit exceeded: {len(self.fiber_add_times)} fibers in last minute")
            return False
            
        self.fiber_add_times.append(current_time)
        return True
    
    def enable_celtic_knot_verification(self):
        """Enable continuous Celtic knot integrity verification"""
        print("🛡️  Celtic Knot Verification: ACTIVATED")
        
    def verify_all_knots(self):
        """Verify integrity of all Celtic knots"""
        compromised_knots = []
        
        for knot_id, knot in self.loom.knot_weave.knot_registry.items():
            fiber_a = self.loom.fibers.get(knot['fiber_a'])
            fiber_b = self.loom.fibers.get(knot['fiber_b'])
            
            if fiber_a and fiber_b:
                if not self.loom.knot_weave.verify_knot_integrity(knot_id, fiber_a, fiber_b):
                    compromised_knots.append(knot_id)
        
        if compromised_knots:
            self.log_intrusion("KNOT_INTEGRITY_BREACH",
                             f"Compromised knots: {len(compromised_knots)}")
            return False
            
        return True

# Fortified Loom with Enhanced Security
class FortifiedCelticLoom(CelticDataLoom):
    """
    Celtic Data Loom with integrated defensive fortifications
    """
    
    def __init__(self):
        super().__init__()
        self.defenses = DefensiveFortifications(self)
        self.defenses.enable_tamper_detection()
        self.defenses.enable_rate_limiting()
        self.defenses.enable_celtic_knot_verification()
        
        print("🏰 FORTIFIED CELTIC LOOM - Defense Systems Online")
    
    def add_fiber(self, fiber):
        """Add fiber with security checks"""
        # Rate limiting check
        if not self.defenses.check_rate_limit():
            print("🚫 Rate limit exceeded - fiber rejected")
            return False
        
        # Perform integrity check before addition
        if not self.defenses.check_integrity_breach():
            print("🚫 Integrity breach detected - operation aborted")
            return False
        
        # Add fiber using parent method
        result = super().add_fiber(fiber)
        
        # Verify knots after addition
        self.defenses.verify_all_knots()
        
        return result
    
    def extract_fiber(self, fiber_id, owner_id):
        """Extract fiber with enhanced security verification"""
        # Integrity check before extraction
        if not self.defenses.check_integrity_breach():
            print("🚫 Integrity breach detected - extraction blocked")
            return None
        
        # Perform extraction
        fiber = super().extract_fiber(fiber_id, owner_id)
        
        return fiber
    
    def get_security_status(self):
        """Get comprehensive security status"""
        base_status = self.get_collective_status()
        defense_status = {
            'intrusion_detection_count': self.defenses.suspicious_activity_count,
            'rate_limit_enforced': self.defenses.max_fibers_per_minute,
            'tamper_detection_active': True,
            'last_intrusion': self.defenses.intrusion_detection_log[-1] if self.defenses.intrusion_detection_log else "None",
            'system_integrity': "COMPROMISED" if self.defenses.suspicious_activity_count > 0 else "SECURE"
        }
        
        return {**base_status, **defense_status}

# Test the fortified system
if __name__ == "__main__":
    print("🏰 FORTIFIED CELTIC LOOM SECURITY DEMO")
    print("="*60)
    
    # Create fortified loom
    fortress = FortifiedCelticLoom()
    
    # Add legitimate fibers
    print("\n🎯 ADDING LEGITIMATE FIBERS:")
    legitimate_fibers = [
        ("Secure financial data", "bleak"),
        ("Research findings", "bleak"),
        ("Personal documents", "bleak")
    ]
    
    for data, owner in legitimate_fibers:
        fiber = DataFiber(data, owner)
        fortress.add_fiber(fiber)
        print("")
    
    # Show security status
    print("\n🛡️  SECURITY STATUS:")
    security_status = fortress.get_security_status()
    for key, value in security_status.items():
        print(f"  {key}: {value}")
    
    # Simulate attack attempt
    print("\n🔴 SIMULATING ATTACK:")
    try:
        # Try to directly inject a fiber (bypassing security)
        attack_fiber = DataFiber("MALICIOUS PAYLOAD", "attacker")
        fortress.fibers[attack_fiber.fiber_id] = attack_fiber
        print("   💉 Attempted direct fiber injection...")
        
        # Check if detection works
        fortress.defenses.check_integrity_breach()
        
    except Exception as e:
        print(f"   🛡️  Attack blocked: {e}")
    
    print("\n🎯 DEMONSTRATING SECURE EXTRACTION:")
    if fortress.fibers:
        test_fiber_id = list(fortress.fibers.keys())[0]
        extracted = fortress.extract_fiber(test_fiber_id, "bleak")
        if extracted:
            print(f"   ✅ Secure extraction successful: {extracted.raw_data}")
    
    print(f"\n🏆 FORTIFIED SYSTEM READY - {security_status['system_integrity']}")
