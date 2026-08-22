# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/entities/mayor_strump_boss.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/entities/mayor_strump_boss.py

"""
Mayor Donetti Strump - The Corrupt Mayor Boss
A satirical raid boss who secretly loves spaghetti code and spawns chaos.
Multiplayer-ready with phase transitions and contextual taunts.
"""

import random
import time
from typing import List, Dict, Optional

class MayorStrump:
    """
    The antagonist of Code City. Loves spaghetti code, hates clean architecture.
    Gets progressively more unhinged as you refactor his beloved technical debt.
    """
    
    def __init__(self, codebase_size: int = 1000):
        self.name = "Mayor Donetti Strump"
        self.title = "The Developer-in-Chief"
        self.secret_lair = "Strump Tower of Technical Debt"
        
        # Boss stats (scale with codebase)
        self.max_health = max(500, codebase_size // 2)
        self.current_health = self.max_health
        self.phase = 1
        self.max_phases = 3
        
        # Attack patterns
        self.sabotage_cooldown = 0
        self.spawn_cooldown = 0
        self.rant_cooldown = 0
        
        # Stats tracking (for multiplayer)
        self.damage_taken_by_player = {}
        self.sabotages_deployed = 0
        self.monsters_spawned = 0
        self.rants_delivered = 0
        
        # Personality
        self.mood = "confident"  # confident -> angry -> desperate
        self.favorite_flaw = "spaghetti"
        
    # ==================== PHASE SYSTEM ====================
    
    def get_current_phase(self) -> int:
        """Determine boss phase based on remaining health."""
        health_percent = (self.current_health / self.max_health) * 100
        
        if health_percent > 66:
            return 1
        elif health_percent > 33:
            return 2
        else:
            return 3
    
    def check_phase_transition(self) -> bool:
        """Check if boss entered new phase, update accordingly."""
        new_phase = self.get_current_phase()
        if new_phase != self.phase:
            self.phase = new_phase
            self._phase_transition()
            return True
        return False
    
    def _phase_transition(self):
        """Handle phase transition effects."""
        if self.phase == 2:
            self.mood = "angry"
            print(f"\n💢 {self.name} is getting ANGRY!")
            print("🗣️ \"You're making my beautiful code look bad! Fake news!\"")
            self._spawn_emergency_monsters()
            
        elif self.phase == 3:
            self.mood = "desperate"
            print(f"\n😰 {self.name} is DESPERATE!")
            print("🗣️ \"This is the worst refactor in the history of refactors, maybe ever!\"")
            self._deploy_mega_sabotage()
    
    # ==================== ATTACK PATTERNS ====================
    
    def take_turn(self, city_buildings: List[Dict]) -> Dict:
        """Execute mayor's turn in combat. Returns action log."""
        self.sabotage_cooldown = max(0, self.sabotage_cooldown - 1)
        self.spawn_cooldown = max(0, self.spawn_cooldown - 1)
        self.rant_cooldown = max(0, self.rant_cooldown - 1)
        
        actions = []
        
        # Always rant if possible (flavor)
        if self.rant_cooldown == 0 and random.random() > 0.4:
            rant = self.deliver_rant()
            actions.append({"type": "rant", "text": rant})
            self.rant_cooldown = 2
        
        # Sabotage based on phase
        if self.sabotage_cooldown == 0:
            sabotage = self.deploy_sabotage(city_buildings)
            if sabotage:
                actions.append(sabotage)
                self.sabotage_cooldown = 3 if self.phase == 1 else 2
        
        # Spawn monsters
        if self.spawn_cooldown == 0:
            spawn = self.spawn_minions()
            if spawn:
                actions.append(spawn)
                self.spawn_cooldown = 4 if self.phase < 3 else 2
        
        return {"phase": self.phase, "health": self.current_health, "actions": actions}
    
    def deploy_sabotage(self, buildings: List[Dict]) -> Optional[Dict]:
        """Introduce new flaws to clean buildings."""
        clean_buildings = [b for b in buildings if b.get('flaw_type') == 'ok' and b.get('health', 100) > 50]
        
        if not clean_buildings:
            return None
        
        target = random.choice(clean_buildings)
        flaw_type = random.choice(['spaghetti', 'legacy', 'ui_clunky', 'placeholder'])
        
        # Apply sabotage
        target['flaw_type'] = f"strump_{flaw_type}"
        target['health'] = max(1, target['health'] - random.randint(10, 30))
        
        self.sabotages_deployed += 1
        
        taunt = random.choice([
            f"I'm introducing some TREMENDOUS {flaw_type} to {target['language']}!",
            f"Nobody writes {flaw_type} better than me. Nobody!",
            f"Your {target['language']} file needed more character. I fixed it!",
            f"That code was too clean. Sad! I made it great again!"
        ])
        
        return {
            "type": "sabotage",
            "target": target['id'],
            "flaw": flaw_type,
            "taunt": taunt
        }
    
    def spawn_minions(self) -> Optional[Dict]:
        """Spawn monsters based on current phase."""
        spawn_count = self.phase  # More monsters in later phases
        
        monster_types = {
            1: [("Spaghetti Imp", "spaghetti", 15)],
            2: [("Legacy Golem", "legacy", 20), ("UI Gremlin", "ui_clunky", 18)],
            3: [("Chaos Dragon", "runtime_error", 30), ("Debt Demon", "placeholder", 25)]
        }
        
        spawns = []
        available = monster_types.get(self.phase, monster_types[1])
        
        for _ in range(spawn_count):
            name, flaw, strength = random.choice(available)
            spawns.append({
                "name": name,
                "flaw_preference": flaw,
                "strength": strength
            })
        
        self.monsters_spawned += len(spawns)
        
        return {
            "type": "spawn",
            "monsters": spawns,
            "count": len(spawns)
        }
    
    # ==================== DIALOGUE SYSTEM ====================
    
    def deliver_rant(self) -> str:
        """Context-aware taunts based on phase and mood."""
        self.rants_delivered += 1
        
        rants_by_phase = {
            1: [
                "My code is YUGE! The best code! Everyone says so!",
                "I've written more lines of code than anyone. Believe me!",
                "This codebase is tremendous. Some say it's too good!",
                "Refactoring is for losers. Winners ship spaghetti!",
                "I know more about coding than the coders, okay?"
            ],
            2: [
                "You're being very unfair to my technical debt!",
                "The fake news media says my code has bugs. WRONG!",
                "Nobody sabotages their own codebase better than me!",
                "This is a witch hunt! My placeholders are perfect!",
                "I've had the best legacy code. People tell me all the time!"
            ],
            3: [
                "This is the worst refactor in history, possibly ever!",
                "You're making my beautiful spaghetti code look terrible!",
                "I'll build a firewall and make the users pay for it!",
                "My code is under audit! You can't look at it!",
                "I'm the best at technical debt. Nobody does it better!"
            ]
        }
        
        return random.choice(rants_by_phase.get(self.phase, rants_by_phase[1]))
    
    def taunt_player(self, player_name: str, action: str) -> str:
        """Generate personalized taunt based on player action."""
        taunts = {
            "refactor": [
                f"{player_name}? More like {player_name} the Loser!",
                f"Your refactor is weak, {player_name}. Very weak!",
                f"I've seen better refactors from interns, {player_name}!",
            ],
            "fix": [
                f"That wasn't even a real bug, {player_name}. Fake news!",
                f"You call that a fix? Sad!",
                f"My bugs have the best features, {player_name}!",
            ],
            "attack": [
                f"Is that all you got, {player_name}? Pathetic!",
                f"I've taken harder hits from code reviewers!",
                f"Your attacks are almost as weak as your commit messages!",
            ]
        }
        
        return random.choice(taunts.get(action, ["Nice try, loser!"]))
    
    # ==================== SPECIAL ABILITIES ====================
    
    def _spawn_emergency_monsters(self):
        """Phase 2 transition: spawn extra monsters."""
        print("🚨 Mayor Strump calls for BACKUP!")
        print("💀 3x Spaghetti Beasts materialize from technical debt!")
    
    def _deploy_mega_sabotage(self):
        """Phase 3 transition: massive sabotage wave."""
        print("⚠️ Mayor Strump deploys the ULTIMATE SABOTAGE!")
        print("💣 Random code files corrupted with placeholder bombs!")
    
    # ==================== DAMAGE & HEALTH ====================
    
    def take_damage(self, damage: int, player_name: str = "Anonymous"):
        """Apply damage to boss, track by player for multiplayer."""
        self.current_health = max(0, self.current_health - damage)
        
        # Track damage per player
        if player_name not in self.damage_taken_by_player:
            self.damage_taken_by_player[player_name] = 0
        self.damage_taken_by_player[player_name] += damage
        
        # Check for phase transition
        self.check_phase_transition()
        
        return {
            "remaining_health": self.current_health,
            "is_defeated": self.is_defeated(),
            "response": self.taunt_player(player_name, "attack")
        }
    
    def is_defeated(self) -> bool:
        """Check if boss is dead."""
        return self.current_health <= 0
    
    # ==================== LOOT & REWARDS ====================
    
    def drop_loot(self) -> Dict:
        """Generate rewards for defeating the mayor."""
        loot_table = {
            "epic": [
                "The Art of the Refactor (Design Pattern Book)",
                "Strump's Secret: How to NOT Write Code",
                "Golden Commit: +50% Refactor Speed",
                "Mayor's Hairpiece (Legendary Cosmetic)"
            ],
            "rare": [
                "Clean Code Manifesto",
                "Spaghetti Detector (Tool)",
                "Legacy Code Exorcism Kit",
                "UI Polish Spray"
            ],
            "common": [
                "Generic Linter",
                "Stack Overflow Bookmark",
                "Coffee Mug: 'I Survived Strump Tower'",
                "Rubber Duck (Debugging Aid)"
            ]
        }
        
        # Loot based on performance
        total_damage = sum(self.damage_taken_by_player.values())
        
        drops = []
        drops.append(random.choice(loot_table["epic"]))
        drops.append(random.choice(loot_table["rare"]))
        drops.append(random.choice(loot_table["common"]))
        
        return {
            "drops": drops,
            "bonus_xp": total_damage * 2,
            "achievement": "Made Code Great Again (But Actually)",
            "leaderboard": sorted(
                self.damage_taken_by_player.items(),
                key=lambda x: x[1],
                reverse=True
            )
        }
    
    # ==================== MULTIPLAYER HOOKS ====================
    
    def get_boss_state(self) -> Dict:
        """Return current boss state for network sync."""
        return {
            "name": self.name,
            "health": self.current_health,
            "max_health": self.max_health,
            "phase": self.phase,
            "mood": self.mood,
            "stats": {
                "sabotages": self.sabotages_deployed,
                "monsters_spawned": self.monsters_spawned,
                "rants": self.rants_delivered
            },
            "damage_by_player": self.damage_taken_by_player
        }
    
    def broadcast_action(self, action: Dict) -> str:
        """Format action for multiplayer broadcast."""
        msg = f"[BOSS] Mayor Strump: "
        
        if action["type"] == "rant":
            msg += f"🗣️ {action['text']}"
        elif action["type"] == "sabotage":
            msg += f"💣 Sabotaged {action['target']} with {action['flaw']}!"
        elif action["type"] == "spawn":
            msg += f"👹 Spawned {action['count']} monsters!"
        
        return msg


# ==================== DEMO FIGHT ====================

if __name__ == "__main__":
    print("🏙️ CODE CITY RAID: STRUMP TOWER")
    print("=" * 50)
    
    # Mock city buildings
    mock_buildings = [
        {"id": "main.py", "language": "Python", "flaw_type": "ok", "health": 100},
        {"id": "utils.js", "language": "JavaScript", "flaw_type": "spaghetti", "health": 80},
        {"id": "style.css", "language": "CSS", "flaw_type": "ui_clunky", "health": 60},
    ]
    
    # Initialize boss
    mayor = MayorStrump(codebase_size=2000)
    print(f"\n👔 {mayor.name} appears!")
    print(f"💪 Health: {mayor.current_health}/{mayor.max_health}")
    print(f"🏢 Location: {mayor.secret_lair}\n")
    
    # Simulate 10 turn raid
    for turn in range(1, 11):
        print(f"\n--- TURN {turn} ---")
        
        # Boss takes turn
        boss_action = mayor.take_turn(mock_buildings)
        print(f"Phase {boss_action['phase']} | Health: {boss_action['health']}")
        
        for action in boss_action['actions']:
            if action['type'] == 'rant':
                print(f"🗣️ Strump: \"{action['text']}\"")
            elif action['type'] == 'sabotage':
                print(f"💣 {action['taunt']}")
            elif action['type'] == 'spawn':
                print(f"👹 Spawned {action['count']} monsters!")
        
        # Player attacks (simulated)
        player_damage = random.randint(50, 100)
        result = mayor.take_damage(player_damage, "TestPlayer")
        print(f"⚔️ Player deals {player_damage} damage!")
        print(f"💬 Strump: \"{result['response']}\"")
        
        if result['is_defeated']:
            print("\n🎉 MAYOR STRUMP DEFEATED!")
            loot = mayor.drop_loot()
            print(f"\n💎 LOOT DROPS:")
            for item in loot['drops']:
                print(f"  - {item}")
            print(f"\n🏆 Bonus XP: {loot['bonus_xp']}")
            print(f"🥇 Achievement: {loot['achievement']}")
            break
        
        time.sleep(0.5)  # Dramatic pause