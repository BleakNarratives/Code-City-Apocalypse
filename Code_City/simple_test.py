
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: hashlib, json
# ROLE: SimpleFiber class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Test (0)
# [/DNA_TAG]

print("🚀 Mobile Fiber Test Starting...")
import hashlib
import json

class SimpleFiber:
    def __init__(self, data):
        self.data = data
        self.fingerprint = hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def show(self):
        return f"Fiber: {self.fingerprint} -> {self.data[:20]}..."

# Test it
f1 = SimpleFiber("This is my first data fiber")
f2 = SimpleFiber("More important data here")
print(f1.show())
print(f2.show())
print("✅ Basic fiber system working!")
