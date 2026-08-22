# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/core/attack_orchestrator.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: stdlib
# ROLE: Create monsters based on code flaws
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]


class AttackOrchestrator:
    def __init__(self):
        self.mayor = MayorStrump()
        self.attackers = self.spawn_attackers()
    
    def spawn_attackers(self):
        """Create monsters based on code flaws"""
        return [
            Monster("Flying Spaghetti Beast", 20, "spaghetti", "multiply"),
            Soldier("Legacy Marine", 15, "legacy", "grenade"),
            Tank("UI Crusher", 30, "ui_clunky", 50),
            Plane("Syntax Bomber", 25, "runtime_error", 60)
        ]
    
    def simulate_attack_wave(self, code_buildings):
        """Run attacks on flawed code buildings"""
        print("🚨 CODE CITY IS UNDER ATTACK!")
        
        # Mayor creates new flaws
        new_flaw = self.mayor.secretly_sabotage(code_buildings)
        if new_flaw:
            print(f"💥 Mayor Strump created: {new_flaw}")
        
        # Attackers target flawed buildings
        for attacker in self.attackers:
            flawed_buildings = [b for b in code_buildings if b['flaw_type'] == attacker.target_preference]
            if flawed_buildings:
                target = random.choice(flawed_buildings)
                attacker.attack(target)