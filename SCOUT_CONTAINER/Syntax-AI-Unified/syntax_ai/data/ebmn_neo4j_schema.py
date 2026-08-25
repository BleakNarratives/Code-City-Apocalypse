# ebmn_neo4j_schema.py - EquiLex Braided Metadata Node (EBMN) Schema

EBMN_NODE_SCHEMA = {
    "label": "EBMN",
    "structural_vectors": ["yaw_vector", "pitch_vector"]
}

EBMN_RELATIONSHIPS = ["AUTH_VERIFIED", "BRAIDED_WITH", "DEPENDS_ON"]

def verify_integrity_vectors(node_data):
    """Checks the pitch (EQT) and yaw (SHS) vectors of a new node."""
    pitch = node_data.get('pitch_vector')
    yaw = node_data.get('yaw_vector')

    if pitch != 'NOMINAL':
        return False, f"Pitch Error: EQT Miss Detected ({pitch})"
    if yaw != 'NOMINAL':
        return False, f"Yaw Error: SHS Drift Detected ({yaw})"

    return True, "Vectors Nominal"

