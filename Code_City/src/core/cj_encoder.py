# cj_encoder.py - The Carrot Juice Protocol (CJP) Encoder for Celtic Data Loom

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-core
# DEPS: hashlib, json
# ROLE: Implements the Carrot Juice Protocol for topological data integrity.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]


import hashlib
import json

class CJPEncoder:
    """
    Implements the Carrot Juice Protocol for topological data integrity.
    It generates the unique Pitch and Yaw vectors that define non-linear data
    relationships (Knot Work) and enforces the Collective Juice Hash.
    """

    def __init__(self, integrity_salt="EquiNex_OSF_v3"):
        self.salt = integrity_salt
        self.PITCH_VECTOR = "10101" # Defines data ownership and vertical lineage
        self.YAW_VECTOR = "01010"   # Defines data relationship and horizontal lineage

    def generate_pitch_yaw(self, fiber_data: str) -> dict:
        """Generates the unique Pitch and Yaw cryptographic vectors."""
        # Calculate a primary hash of the data (the 'Raw Juice')
        raw_juice = hashlib.sha256(fiber_data.encode() + self.salt.encode()).hexdigest()

        # Pitch is derived from the first part of the hash, XORed with the vector
        pitch_hash = hashlib.sha256((raw_juice[:32] + self.PITCH_VECTOR).encode()).hexdigest()
        
        # Yaw is derived from the second part, XORed with the vector
        yaw_hash = hashlib.sha256((raw_juice[32:] + self.YAW_VECTOR).encode()).hexdigest()
        
        return {
            "pitch": pitch_hash,
            "yaw": yaw_hash,
            "raw_juice": raw_juice 
        }

    def generate_collective_juice(self, pitch_hashes: list, yaw_hashes: list) -> str:
        """Creates the Collective Juice Hash (the BFT Integrity Check)."""
        combined_data = "".join(sorted(pitch_hashes + yaw_hashes)) + self.salt
        return hashlib.sha256(combined_data.encode()).hexdigest()
        
    def cj_encode(self, data: dict) -> dict:
        """Wrapper to apply the CJP to a Fiber unit and embed the vectors."""
        data_string = json.dumps(data, sort_keys=True)
        vectors = self.generate_pitch_yaw(data_string)
        
        data['CJP_VECTORS'] = vectors
        return data
