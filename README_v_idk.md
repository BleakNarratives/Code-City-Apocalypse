{
    # Primary Key: The immutable component identifier
    "EQI-CODEX-LINGUA-SOVEREIGN-4A82": {
        
        # --- I. Integrity Check (L-S-L-1: EQI/EQT) ---
        "integrity_source": "src.entities.mayor_strump_boss.py", 
        "time_code_helix": {
            # Base parameters for the KMS/EPH/DIR Braiding
            "strands": 3,
            "base_radius": 50, # qrsize // 2 + 50
            "phase_shift_deg": 120.0, # Ensures non-overlap
            # The exact, trusted perturbation factor (AI-Perturbation Anchor)
            "torsion_amplitude": 20.0,
            "torsion_frequency": 3.0 
        },
        
        # --- II. Consistency Check (L-S-L-2: SHS/Harmonics) ---
        "harmonic_overlay": {
            # The fundamental frequencies for the sin wave overlay
            "trusted_frequencies": [0.5, 1.0, 1.5],
            "wave_amplitude": 50.0,
            "alpha_variation_func": "100 * (1 + sin(i/50)) / 2" # Alpha mask function
        },

        # --- III. Deep Inspection Trigger (DLSI: Golden Spiral) ---
        "golden_spiral": {
            # Defines the exact, expected curvature for the spiral (Recurrence Relation)
            "a_base": 10.0,
            "b_curvature": 0.1, # Critical value; deviation triggers DLSI
            "theta_range_max": 6.2831853 # 2π (Trusted full revolution)
        },

        # --- IV. Metadata ---
        "qr_data_payload": "CODEX-LINGUA-SOVEREIGN",
        "whisper_text": "The braid remembers..."
    },
    
    # Example for another component
    "EQI-ARENA-PVP-A7F2-12B3": {
        # ... (similar structure for the Arena system)
    }
}
