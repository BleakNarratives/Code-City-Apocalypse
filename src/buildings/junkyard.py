# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/junkyard.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/junkyard.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: dataclasses, enum, json, random, typing
# ROLE: Junkyard - The Frankencode Factory
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]


"""
Junkyard - The Frankencode Factory
Where deleted/deprecated code goes to be salvaged, combined, and resurrected.
Players can craft "Frankencode" patterns from scrap for unique abilities.
"""

import random
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ==================== SCRAP TYPES ====================

class ScrapRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class ScrapType(Enum):
    SPAGHETTI_LOOP = "spaghetti_loop"
    DEPRECATED_API = "deprecated_api"
    LEGACY_FUNCTION = "legacy_function"
    DEAD_CODE = "dead_code"
    PLACEHOLDER_STUB = "placeholder_stub"
    MAGIC_NUMBER = "magic_number"
    GOD_CLASS = "god_class"
    COPY_PASTE = "copy_paste"
    NESTED_HELL = "nested_hell"
    COMMENT_LIE = "comment_lie"

@dataclass
class CodeScrap:
    """A piece of salvaged code."""
    id: str
    name: str
    scrap_type: ScrapType
    rarity: ScrapRarity
    language: str
    lines_of_code: int
    source_file: str
    power_level: int  # Used in crafting calculations
    
    # Flavortext
    description: str = ""
    found_in: str = ""
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.scrap_type.value,
            "rarity": self.rarity.value,
            "language": self.language,
            "loc": self.lines_of_code,
            "source": self.source_file,
            "power": self.power_level,
            "description": self.description
        }


# ==================== FRANKENCODE PATTERNS ====================

@dataclass
class FrankencodePattern:
    """A crafted combination of scraps that grants abilities."""
    id: str
    name: str
    rarity: ScrapRarity
    components: List[str]  # Scrap IDs used
    ability: str
    power: int
    description: str
    
    def to_dict(self):
        return asdict(self)


# ==================== CRAFTING RECIPES ====================

RECIPES = {
    "spaghetti_detector": {
        "name": "Spaghetti Detector 3000",
        "components": [ScrapType.SPAGHETTI_LOOP, ScrapType.NESTED_HELL],
        "min_count": 3,
        "ability": "Instantly highlight all spaghetti code in codebase",
        "description": "Built from the worst offenders. It takes one to know one."
    },
    "legacy_translator": {
        "name": "Legacy Code Rosetta Stone",
        "components": [ScrapType.LEGACY_FUNCTION, ScrapType.COMMENT_LIE, ScrapType.DEPRECATED_API],
        "min_count": 5,
        "ability": "Auto-generate documentation for undocumented legacy code",
        "description": "Deciphers ancient mysteries by understanding their lies."
    },
    "placeholder_eliminator": {
        "name": "TODO Destroyer",
        "components": [ScrapType.PLACEHOLDER_STUB, ScrapType.DEAD_CODE],
        "min_count": 10,
        "ability": "Automatically implement all TODO/FIXME comments",
        "description": "Procrastination made manifest. Now it fights back."
    },
    "god_class_breaker": {
        "name": "SRP Enforcer",
        "components": [ScrapType.GOD_CLASS, ScrapType.COPY_PASTE],
        "min_count": 7,
        "ability": "Automatically split god classes into proper modules",
        "description": "Even gods can be shattered."
    },
    "magic_debugger": {
        "name": "The All-Seeing Eye",
        "components": [ScrapType.MAGIC_NUMBER, ScrapType.DEAD_CODE, ScrapType.COMMENT_LIE],
        "min_count": 15,
        "ability": "Reveals all hidden bugs and edge cases",
        "description": "Chaos recognizes chaos."
    }
}


# ==================== JUNKYARD SYSTEM ====================

class Junkyard:
    """
    The Junkyard building where players salvage and craft.
    Tracks global scrap inventory and crafted patterns.
    """
    
    def __init__(self):
        self.scrap_inventory: Dict[str, CodeScrap] = {}
        self.crafted_patterns: Dict[str, FrankencodePattern] = {}
        self.scrap_count_by_type: Dict[ScrapType, int] = {t: 0 for t in ScrapType}
        self.total_scraps_collected = 0
        self.total_patterns_crafted = 0
        
    # ==================== SCRAP COLLECTION ====================
    
    def collect_scrap(
        self,
        scrap_type: ScrapType,
        language: str,
        source_file: str,
        lines: int
    ) -> CodeScrap:
        """Generate scrap from deleted/refactored code."""
        scrap_id = f"scrap_{self.total_scraps_collected + 1:04d}"
        
        # Determine rarity based on scrap type and LOC
        rarity = self._calculate_rarity(scrap_type, lines)
        power = self._calculate_power(rarity, lines)
        
        # Generate flavortext
        name = self._generate_scrap_name(scrap_type, language)
        description = self._generate_scrap_description(scrap_type, source_file)
        
        scrap = CodeScrap(
            id=scrap_id,
            name=name,
            scrap_type=scrap_type,
            rarity=rarity,
            language=language,
            lines_of_code=lines,
            source_file=source_file,
            power_level=power,
            description=description,
            found_in=f"Deleted from {source_file}"
        )
        
        self.scrap_inventory[scrap_id] = scrap
        self.scrap_count_by_type[scrap_type] += 1
        self.total_scraps_collected += 1
        
        print(f"✨ Collected: {name} ({rarity.value.upper()})")
        
        return scrap
    
    def _calculate_rarity(self, scrap_type: ScrapType, lines: int) -> ScrapRarity:
        """Determine rarity based on type and size."""
        base_rarity = {
            ScrapType.DEAD_CODE: ScrapRarity.COMMON,
            ScrapType.PLACEHOLDER_STUB: ScrapRarity.COMMON,
            ScrapType.MAGIC_NUMBER: ScrapRarity.UNCOMMON,
            ScrapType.COPY_PASTE: ScrapRarity.UNCOMMON,
            ScrapType.SPAGHETTI_LOOP: ScrapRarity.RARE,
            ScrapType.NESTED_HELL: ScrapRarity.RARE,
            ScrapType.COMMENT_LIE: ScrapRarity.RARE,
            ScrapType.LEGACY_FUNCTION: ScrapRarity.EPIC,
            ScrapType.DEPRECATED_API: ScrapRarity.EPIC,
            ScrapType.GOD_CLASS: ScrapRarity.LEGENDARY
        }
        
        rarity = base_rarity.get(scrap_type, ScrapRarity.COMMON)
        
        # Upgrade rarity for massive chunks of bad code
        if lines > 500:
            rarity_order = list(ScrapRarity)
            current_index = rarity_order.index(rarity)
            if current_index < len(rarity_order) - 1:
                rarity = rarity_order[current_index + 1]
        
        return rarity
    
    def _calculate_power(self, rarity: ScrapRarity, lines: int) -> int:
        """Calculate power level for crafting."""
        rarity_multiplier = {
            ScrapRarity.COMMON: 1,
            ScrapRarity.UNCOMMON: 2,
            ScrapRarity.RARE: 5,
            ScrapRarity.EPIC: 10,
            ScrapRarity.LEGENDARY: 20
        }
        
        base_power = rarity_multiplier[rarity]
        size_bonus = min(lines // 50, 10)
        
        return base_power + size_bonus
    
    def _generate_scrap_name(self, scrap_type: ScrapType, language: str) -> str:
        """Generate humorous scrap names."""
        names = {
            ScrapType.SPAGHETTI_LOOP: [
                f"Tangled {language} Mess",
                f"The Eternal Loop of {language}",
                f"Spaghetti Monster Fragment"
            ],
            ScrapType.DEPRECATED_API: [
                f"Ancient {language} Ritual",
                f"Forbidden {language} Incantation",
                f"The Old Way (Don't Use This)"
            ],
            ScrapType.LEGACY_FUNCTION: [
                f"Grandfather's {language} Code",
                f"Pre-Historic {language} Artifact",
                f"Before Time Began..."
            ],
            ScrapType.DEAD_CODE: [
                f"Zombie {language} Fragment",
                f"The Unreachable Code",
                f"Dead on Arrival"
            ],
            ScrapType.PLACEHOLDER_STUB: [
                f"TODO: Fix This Later",
                f"Future {language} Problem",
                f"Procrastinator's Delight"
            ],
            ScrapType.MAGIC_NUMBER: [
                "42 (But Why?)",
                "The Mysterious Constant",
                f"Unexplained {language} Value"
            ],
            ScrapType.GOD_CLASS: [
                f"The {language} Omnipotent",
                "Does Everything, Badly",
                f"All-Powerful {language} Monolith"
            ],
            ScrapType.COPY_PASTE: [
                "Ctrl+C, Ctrl+V Special",
                "The Duplicator",
                f"Repeated {language} Shame"
            ],
            ScrapType.NESTED_HELL: [
                "Seven Layers Deep",
                f"{language} Matryoshka Doll",
                "The Indentation Nightmare"
            ],
            ScrapType.COMMENT_LIE: [
                "Says One Thing, Does Another",
                "The Misleading Comment",
                "Trust Issues Incarnate"
            ]
        }
        
        return random.choice(names.get(scrap_type, [f"{language} Scrap"]))
    
    def _generate_scrap_description(self, scrap_type: ScrapType, source: str) -> str:
        """Generate scrap descriptions."""
        descriptions = {
            ScrapType.SPAGHETTI_LOOP: f"A twisted mess from {source}. Nobody knows what it does anymore.",
            ScrapType.DEPRECATED_API: f"This was cutting-edge in 2005. Now it's a museum piece.",
            ScrapType.LEGACY_FUNCTION: f"Written by someone who no longer works here. Or anywhere.",
            ScrapType.DEAD_CODE: f"Code that will never execute. Ever. Why is it still here?",
            ScrapType.PLACEHOLDER_STUB: f"TODO: Implement this. (Added 5 years ago)",
            ScrapType.MAGIC_NUMBER: f"What does this number mean? Only God and the original dev know.",
            ScrapType.GOD_CLASS: f"This class does EVERYTHING. Including making coffee.",
            ScrapType.COPY_PASTE: f"Someone copied this 47 times instead of writing a function.",
            ScrapType.NESTED_HELL: f"If statements nested deeper than Inception.",
            ScrapType.COMMENT_LIE: f"The comment says 'fast'. The code says 'O(n³)'."
        }
        
        return descriptions.get(scrap_type, f"Salvaged from {source}")
    
    # ==================== CRAFTING SYSTEM ====================
    
    def can_craft(self, recipe_name: str) -> bool:
        """Check if player has enough scraps for recipe."""
        recipe = RECIPES.get(recipe_name)
        if not recipe:
            return False
        
        required_types = recipe["components"]
        required_count = recipe["min_count"]
        
        # Count available scraps of required types
        available = sum(
            1 for scrap in self.scrap_inventory.values()
            if scrap.scrap_type in required_types
        )
        
        return available >= required_count
    
    def craft_pattern(self, recipe_name: str) -> Optional[FrankencodePattern]:
        """Craft a Frankencode pattern from scraps."""
        if not self.can_craft(recipe_name):
            print(f"❌ Not enough scraps for {recipe_name}")
            return None
        
        recipe = RECIPES[recipe_name]
        
        # Find and consume required scraps
        required_types = recipe["components"]
        required_count = recipe["min_count"]
        
        consumed_scraps = []
        for scrap in list(self.scrap_inventory.values()):
            if scrap.scrap_type in required_types and len(consumed_scraps) < required_count:
                consumed_scraps.append(scrap.id)
        
        # Remove consumed scraps
        total_power = 0
        for scrap_id in consumed_scraps:
            scrap = self.scrap_inventory.pop(scrap_id)
            self.scrap_count_by_type[scrap.scrap_type] -= 1
            total_power += scrap.power_level
        
        # Determine pattern rarity based on total power
        pattern_rarity = self._determine_pattern_rarity(total_power)
        
        # Create pattern
        pattern_id = f"pattern_{self.total_patterns_crafted + 1:04d}"
        pattern = FrankencodePattern(
            id=pattern_id,
            name=recipe["name"],
            rarity=pattern_rarity,
            components=consumed_scraps,
            ability=recipe["ability"],
            power=total_power,
            description=recipe["description"]
        )
        
        self.crafted_patterns[pattern_id] = pattern
        self.total_patterns_crafted += 1
        
        print(f"\n🔧 CRAFTED: {pattern.name}")
        print(f"   Rarity: {pattern_rarity.value.upper()}")
        print(f"   Power: {total_power}")
        print(f"   Ability: {pattern.ability}")
        
        return pattern
    
    def _determine_pattern_rarity(self, power: int) -> ScrapRarity:
        """Determine crafted pattern rarity from power level."""
        if power >= 150:
            return ScrapRarity.LEGENDARY
        elif power >= 80:
            return ScrapRarity.EPIC
        elif power >= 40:
            return ScrapRarity.RARE
        elif power >= 15:
            return ScrapRarity.UNCOMMON
        else:
            return ScrapRarity.COMMON
    
    # ==================== VIEWING & STATS ====================
    
    def show_inventory(self):
        """Display scrap inventory."""
        print("\n📦 JUNKYARD INVENTORY")
        print("=" * 60)
        print(f"Total Scraps: {len(self.scrap_inventory)}")
        print(f"Patterns Crafted: {len(self.crafted_patterns)}\n")
        
        print("Scraps by Type:")
        for scrap_type, count in self.scrap_count_by_type.items():
            if count > 0:
                print(f"  {scrap_type.value}: {count}")
    
    def show_patterns(self):
        """Display crafted patterns."""
        print("\n🛠️ CRAFTED PATTERNS")
        print("=" * 60)
        
        if not self.crafted_patterns:
            print("No patterns crafted yet. Visit the Junkyard!")
            return
        
        for pattern in self.crafted_patterns.values():
            print(f"\n{pattern.name} ({pattern.rarity.value.upper()})")
            print(f"  Power: {pattern.power}")
            print(f"  Ability: {pattern.ability}")
            print(f"  Components Used: {len(pattern.components)}")
    
    def show_recipes(self):
        """Display available crafting recipes."""
        print("\n📜 CRAFTING RECIPES")
        print("=" * 60)
        
        for recipe_name, recipe in RECIPES.items():
            can_make = "✅" if self.can_craft(recipe_name) else "❌"
            print(f"\n{can_make} {recipe['name']}")
            print(f"  Required: {recipe['min_count']}x from {len(recipe['components'])} types")
            print(f"  Ability: {recipe['ability']}")


# ==================== DEMO ====================

if __name__ == "__main__":
    print("🏗️ JUNKYARD FRANKENCODE SYSTEM DEMO")
    print("=" * 60)
    
    junkyard = Junkyard()
    
    # Simulate collecting scraps from refactoring
    print("\n--- COLLECTING SCRAPS ---")
    
    scraps_to_collect = [
        (ScrapType.SPAGHETTI_LOOP, "Python", "old_main.py", 150),
        (ScrapType.NESTED_HELL, "Python", "old_main.py", 200),
        (ScrapType.SPAGHETTI_LOOP, "JavaScript", "legacy.js", 80),
        (ScrapType.NESTED_HELL, "JavaScript", "utils.js", 120),
        (ScrapType.DEAD_CODE, "Python", "unused.py", 50),
        (ScrapType.PLACEHOLDER_STUB, "Python", "todo.py", 30),
    ]
    
    for scrap_type, lang, source, lines in scraps_to_collect:
        junkyard.collect_scrap(scrap_type, lang, source, lines)
        time.sleep(0.3)
    
    # Show inventory
    junkyard.show_inventory()
    
    # Show recipes
    junkyard.show_recipes()
    
    # Try crafting
    print("\n--- CRAFTING PATTERN ---")
    pattern = junkyard.craft_pattern("spaghetti_detector")
    
    # Show updated inventory
    junkyard.show_inventory()
    junkyard.show_patterns()
    
    print("\n🏁 Demo complete!")