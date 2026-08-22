
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: stdlib
# ROLE: MayorNPC class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

class MayorNPC:
    def summon_monsters(self):
        print("Mayor: 'Let's summon some code flaws to attack the city!'")
        for _ in range(5):
            monster = Monster(
                name="MemoryLeakDragon",
                health=100,
                damage=20,
                description="A dragon that leaks memory and crashes the city."
            )
            city.add_monster(monster)
        print("Mayor: 'The city is under attack! Time to defend!'")

    def spawn_tanks(self):
        print("Mayor: 'Spawning tanks to defend the city!'")
        for _ in range(3):
            tank = Tank(
                name="DebuggerTank",
                health=200,
                damage=50,
                description="A tank that uses debuggers to fight code flaws."
            )
            city.add_unit(tank)
        print("Mayor: 'The tanks are ready! Let's defend the city!'")