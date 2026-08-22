# File: code_city_attackers.py
# Path: /src/entities/code_city_attackers.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: random
# ROLE: Base class for all entities in Code City.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Attack (4)
# [/DNA_TAG]


import random

class CodeEntity:
    """Base class for all entities in Code City."""
    def __init__(self, name, strength, target_preference):
        self.name = name
        self.strength = strength
        self.target_preference = target_preference  # e.g., 'spaghetti', 'legacy', 'ui_clunky'

    def attack(self, building):
        """Simulate attack on a code building."""
        damage = random.randint(1, self.strength)
        print(f"{self.name} attacks {building['language']} building ({building['flaw_type']}) for {damage} damage!")
        building['health'] -= damage
        if building['health'] <= 0:
            print(f"Building destroyed! Refactor recommendation: Eliminate {building['flaw_type']} in lines {building['lines']}.")
        return building

class Monster(CodeEntity):
    """Monster class for natural/alien threats."""
    def __init__(self, name, strength, target_preference, special_ability):
        super().__init__(name, strength, target_preference)
        self.special_ability = special_ability  # e.g., 'multiply', 'corrupt'

    def use_ability(self, buildings):
        """Special monster ability."""
        if self.special_ability == 'multiply':
            print(f"{self.name} multiplies, spawning more monsters in spaghetti zones!")
            # Could return new Monster instances here for expansion
        elif self.special_ability == 'corrupt':
            for building in buildings:
                if random.random() > 0.5:
                    building['flaw_type'] = 'corrupted_' + building['flaw_type']
                    print(f"{self.name} corrupts {building['language']} building!")

class Soldier(CodeEntity):
    """Soldier class for army invasions."""
    def __init__(self, name, strength, target_preference, weapon):
        super().__init__(name, strength, target_preference)
        self.weapon = weapon  # e.g., 'rifle', 'grenade'

    def attack(self, building):
        super().attack(building)
        if self.weapon == 'grenade':
            extra_damage = random.randint(1, 5)
            print(f"Grenade bonus: {extra_damage} extra damage to adjacent floors!")
            building['health'] -= extra_damage

class Tank(CodeEntity):
    """Tank class for heavy vehicle assaults."""
    def __init__(self, name, strength, target_preference, armor):
        super().__init__(name, strength, target_preference)
        self.armor = armor

    def attack(self, building):
        super().attack(building)
        if building['height'] > 10:  # Tall buildings (large code mass)
            print(f"{self.name} rams base, collapsing {random.randint(1, 3)} floors!")

class Plane(CodeEntity):
    """Plane class for aerial strikes."""
    def __init__(self, name, strength, target_preference, speed):
        super().__init__(name, strength, target_preference)
        self.speed = speed

    def attack(self, building):
        super().attack(building)
        if self.speed > 50:
            print(f"{self.name} strafes from above, targeting UI flaws in {building['flaw_type']}!")

# Example usage (for demo - remove or expand for full integration)
if __name__ == "__main__":
    # Sample building: dict representing a code building
    sample_building = {
        'language': 'Python',
        'flaw_type': 'spaghetti',
        'height': 15,  # Code mass
        'lines': '50-65',  # Floors/lines
        'health': 100,
        'color': 'blue'  # Language-specific
    }

    # Instantiate attackers
    monster = Monster("Spaghetti Beast", 20, "spaghetti", "multiply")
    soldier = Soldier("Code Marine", 15, "legacy", "grenade")
    tank = Tank("Bug Crusher Tank", 30, "ui_clunky", 50)
    plane = Plane("Syntax Bomber", 25, "runtime_error", 60)

    # Simulate attacks
    monster.attack(sample_building)
    monster.use_ability([sample_building])
    soldier.attack(sample_building)
    tank.attack(sample_building)
    plane.attack(sample_building)