# File: CoreTenet_FCT.py
# FCT = Foundational Constraint Trigger. Enforces Goldie Lock Zone adherence.

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-backend
# DEPS: stdlib
# ROLE: check_for_bloat function module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]


def check_for_bloat(language: str, template_type: str, requested_dependencies: list, required_external_services: list) -> dict:
    
    # --- 1. Define Standard Tenet Weights (The FCT's Priority System) ---
    # Weights prioritize MINIMALISM and STABILITY over maximal features.
    
    WEIGHT_DEPENDENCY = 5  # High weight: Every external dep adds heavy baggage.
    WEIGHT_COMPLEXITY = 10 # Highest weight: Accidental complexity is the root bloat.
    WEIGHT_EXTERNAL_CALLS = 8 # High weight: Every external call is a stability risk.

    # --- 2. Calculate Base Metrics ---
    
    # M1: Dependency Count (Simple count)
    M1_Score = len(requested_dependencies) * WEIGHT_DEPENDENCY
    
    # M2: Projected Cyclomatic Complexity (Calculated by Syntax VBS Engine based on template_type)
    # The VBS Engine must ensure the boilerplate has minimal decision paths (e.g., no excessive if/else/loops).
    # Goldie Lock Target: Complexity of 1-3. Score is punitive above 3.
    # Fallback: Use template_type length as proxy for complexity
    projected_complexity = len(template_type) 
    M2_Score = max(0, (projected_complexity - 3)) * WEIGHT_COMPLEXITY
    
    # M3: External Service Calls
    M3_Score = len(required_external_services) * WEIGHT_EXTERNAL_CALLS

    # --- 3. Calculate Total Bloat Score & Advisory Threshold ---
    
    TOTAL_BLOAT_SCORE = M1_Score + M2_Score + M3_Score
    
    ADVISORY_THRESHOLD = 25 # Set a low threshold to aggressively enforce minimalism.

    # --- 4. Trigger the FCT Advisory ---
    
    if TOTAL_BLOAT_SCORE >= ADVISORY_THRESHOLD:
        # FCT has been triggered! Force a context refresh (The Trespass Retrieval).
        # This will instantly surface the 'Goldie Lock' and 'Anti-Bloat' principles.
        
        advisory_message = f"ADVISORY: Proposed setup exceeds the Goldie Lock Bloat Score ({TOTAL_BLOAT_SCORE}/{ADVISORY_THRESHOLD})."
        
        # #advisory #FCT #GoldieLock
        return {
            "Triggered": True,
            "Score": TOTAL_BLOAT_SCORE,
            "Message": advisory_message,
            "Details": {
                "M1_Dependency_Count": len(requested_dependencies),
                "M2_Complexity_Score": projected_complexity,
                "M3_External_Calls": len(required_external_services)
            }
        }
    
    return {"Triggered": False, "Score": TOTAL_BLOAT_SCORE}
