# File: /storage/emulated/0/code_city/src/entities/mayor_trump.py

class MayorTrump:
    def __init__(self):
        self.catchphrases = [
            "This codebase is tremendous, the best codebase!",
            "Fake news media says our app has bugs. Wrong!",
            "We're going to build a firewall and make the hackers pay for it!"
        ]
        self.secret_lair = "Trump Tower of Technical Debt"
    
    def secretly_sabotage(self, codebase):
        """The mayor creates spaghetti code and vulnerabilities"""
        if random.random() < 0.3:  # 30% chance of sabotage
            print("🗽 Mayor Trump: 'I alone can fix this code! (by making it worse)'")
            # Introduce random flaws
            flaw_type = random.choice(['spaghetti', 'legacy', 'ui_clunky'])
            return f"mayor_sabotage_{flaw_type}"
        return None