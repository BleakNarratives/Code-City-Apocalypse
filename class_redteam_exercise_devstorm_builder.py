class RedTeamExercises:
    def penetration_test_city(self):
        attacks = {
            'brute_force': 'OrcArmySiege',
            'social_engineering': 'DoppelgangerInfiltration', 
            'zero_day': 'DragonAttack',
            'ddos': 'ZombieApocalypse',
            'phishing': 'SirenSongAttack'
        }
        
        for attack_type in self.team.arsenal:
            city_response = self.city.defenses.respond_to_attack(attack_type)
            self.analyze_defense_gaps(city_response)
