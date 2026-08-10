class MayorNPC:
    def debug_session(self):
        print("Mayor: 'Let's start a debugging session! I'll fix this code with logic that makes no sense!'")
        for building in city.buildings:
            if building.flaw_type != "ok":
                print(f"Mayor: 'Fixing {building.name}...'")
                building.flaw_type = "ok"
                print("Mayor: 'Fixed! Now it's 100% broken in a different way!'")
        print("Mayor: 'Debugging complete! The city is now more broken than before!'")
