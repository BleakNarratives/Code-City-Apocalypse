
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: logging, random, sys
# ROLE: Fighter class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging
import random
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Fighter:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
    
    def attack(self, move):
        damage = random.randint(15, 25)
        logging.info(f"{self.name} uses {move}! -{damage} HP")
        return damage

def run_battle():
    logging.info("🤺 TERMINAL TITANS - BATTLE MODE")
    logging.info("Mikey vs Claude")
    logging.info("")
    
    mikey = Fighter("MIKEY")
    claude = Fighter("CLAUDE")
    
    moves = ["BASH SLAM", "PYTHON PUNCH", "GIT GRAB", "SPECIAL MOVE"]
    
    while mikey.hp > 0 and claude.hp > 0:
        # Player turn
        logging.info(f"Mikey HP: {mikey.hp} | Claude HP: {claude.hp}")
        logging.info("1. BASH SLAM  2. PYTHON PUNCH  3. GIT GRAB  4. SPECIAL")
        
        try:
            choice = input("Attack: ").strip()
            if choice in ["1", "2", "3", "4"]:
                damage = mikey.attack(moves[int(choice)-1])
                claude.hp -= damage
            else:
                logging.info("Invalid! You hesitate.")
                continue
        except (ValueError, IndexError):
            continue
        except KeyboardInterrupt:
            logging.info("\nBattle aborted.")
            return

        # Claude attacks back if alive
        if claude.hp > 0:
            damage = claude.attack(random.choice(moves))
            mikey.hp -= damage
        
        logging.info("")
    
    # Result
    if mikey.hp > 0:
        logging.info("🎉 YOU WIN! Claude defeated!")
        logging.info("Earned: Terminal XP +100")
    else:
        logging.info("💀 You lost. Game over.")

if __name__ == "__main__":
    run_battle()
