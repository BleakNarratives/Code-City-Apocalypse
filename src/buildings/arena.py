# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/arena.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/arena.py

"""
The Arena - PvP Combat System
Where developers compete in code battles, algorithm races, and refactor duels.
Real-time 1v1 or team battles with ELO rankings and betting systems.
"""

import random
import time
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# ==================== COMBAT MODES ====================

class CombatMode(Enum):
    REFACTOR_RACE = "refactor_race"           # Who fixes code faster
    ALGORITHM_DUEL = "algorithm_duel"         # Implement algorithm better
    BUG_HUNT = "bug_hunt"                     # Find bugs first
    OPTIMIZATION_WAR = "optimization_war"     # Optimize performance
    DESIGN_BATTLE = "design_battle"           # Architecture showdown
    FREESTYLE = "freestyle"                   # Anything goes

class CombatResult(Enum):
    PLAYER1_WIN = "player1_win"
    PLAYER2_WIN = "player2_win"
    DRAW = "draw"
    FORFEIT = "forfeit"

# ==================== CHALLENGE TYPES ====================

@dataclass
class Challenge:
    """A specific combat challenge."""
    id: str
    mode: CombatMode
    title: str
    description: str
    difficulty: int  # 1-10
    time_limit: int  # seconds
    
    # The actual task
    buggy_code: str = ""
    test_cases: List[Dict] = field(default_factory=list)
    acceptance_criteria: str = ""
    
    # Scoring
    max_score: int = 100
    speed_bonus: int = 25
    quality_bonus: int = 25


# ==================== ARENA CHALLENGES ====================

ARENA_CHALLENGES = {
    "spaghetti_untangle": Challenge(
        id="spaghetti_untangle",
        mode=CombatMode.REFACTOR_RACE,
        title="The Spaghetti Untangler",
        description="Refactor this nested nightmare into readable code",
        difficulty=5,
        time_limit=300,
        buggy_code="""
def process(data):
    if data:
        if len(data) > 0:
            result = []
            for i in range(len(data)):
                if data[i]:
                    if isinstance(data[i], str):
                        if len(data[i]) > 0:
                            result.append(data[i].upper())
                        else:
                            result.append("")
                    else:
                        result.append(str(data[i]))
                else:
                    result.append("None")
            return result
    return []
""",
        acceptance_criteria="Max 3 levels of nesting, proper list comprehension"
    ),
    
    "magic_numbers": Challenge(
        id="magic_numbers",
        mode=CombatMode.REFACTOR_RACE,
        title="The Magic Number Massacre",
        description="Replace all magic numbers with named constants",
        difficulty=3,
        time_limit=180,
        buggy_code="""
def calculate_price(qty, is_member):
    if qty > 100:
        price = qty * 9.99 * 0.85
    elif qty > 50:
        price = qty * 9.99 * 0.90
    else:
        price = qty * 9.99
    
    if is_member:
        price = price * 0.95
    
    tax = price * 0.0825
    return price + tax
""",
        acceptance_criteria="No magic numbers, proper constants"
    ),
    
    "algorithm_race": Challenge(
        id="algorithm_race",
        mode=CombatMode.ALGORITHM_DUEL,
        title="Binary Search Sprint",
        description="Implement binary search faster and better",
        difficulty=6,
        time_limit=240,
        test_cases=[
            {"input": ([1,2,3,4,5], 3), "output": 2},
            {"input": ([1,2,3,4,5], 6), "output": -1},
            {"input": ([10,20,30,40,50], 30), "output": 2},
        ],
        acceptance_criteria="O(log n) complexity, handles edge cases"
    ),
    
    "bug_swarm": Challenge(
        id="bug_swarm",
        mode=CombatMode.BUG_HUNT,
        title="The Bug Swarm",
        description="Find and fix all 7 bugs hidden in this code",
        difficulty=7,
        time_limit=420,
        buggy_code="""
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def find_max(lst):
    max_val = lst[0]
    for i in range(len(lst)):
        if lst[i] > max_val:
            max_val = i
    return max_val

def reverse_string(s):
    return s[::-1]

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(result)
        return self.result
""",
        acceptance_criteria="All bugs fixed, code runs without errors"
    ),
    
    "performance_hell": Challenge(
        id="performance_hell",
        mode=CombatMode.OPTIMIZATION_WAR,
        title="Performance Hell",
        description="Optimize this O(n³) disaster",
        difficulty=8,
        time_limit=600,
        buggy_code="""
def find_duplicates(arr1, arr2, arr3):
    result = []
    for i in arr1:
        for j in arr2:
            for k in arr3:
                if i == j == k:
                    if i not in result:
                        result.append(i)
    return result
""",
        acceptance_criteria="Better than O(n²), uses proper data structures"
    )
}


# ==================== PLAYER LOADOUT ====================

@dataclass
class Loadout:
    """Player's equipped abilities and buffs."""
    equipped_patterns: List[str] = field(default_factory=list)  # Frankencode IDs
    active_buffs: Dict[str, int] = field(default_factory=dict)  # buff -> duration
    
    # Abilities
    can_use_hints: bool = True
    can_see_tests: bool = True
    speed_multiplier: float = 1.0
    quality_bonus: int = 0


# ==================== ARENA MATCH ====================

@dataclass
class ArenaMatch:
    """A PvP match instance."""
    id: str
    challenge: Challenge
    player1_id: str
    player2_id: str
    player1_name: str
    player2_name: str
    
    # Loadouts
    player1_loadout: Loadout
    player2_loadout: Loadout
    
    # State
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    
    # Scoring
    player1_score: int = 0
    player2_score: int = 0
    player1_time: Optional[float] = None
    player2_time: Optional[float] = None
    player1_submission: Optional[str] = None
    player2_submission: Optional[str] = None
    
    # Spectators
    spectators: List[str] = field(default_factory=list)
    bets: Dict[str, Tuple[str, int]] = field(default_factory=dict)  # spectator_id -> (player_id, amount)
    
    result: Optional[CombatResult] = None
    winner_id: Optional[str] = None


# ==================== ELO RANKING ====================

class ELOSystem:
    """Calculate ELO ratings for competitive play."""
    
    def __init__(self, k_factor: int = 32):
        self.k_factor = k_factor
    
    def calculate_expected_score(self, rating_a: int, rating_b: int) -> float:
        """Calculate expected win probability."""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    def update_ratings(
        self,
        winner_rating: int,
        loser_rating: int,
        is_draw: bool = False
    ) -> Tuple[int, int]:
        """Update both players' ratings after match."""
        expected_winner = self.calculate_expected_score(winner_rating, loser_rating)
        expected_loser = 1 - expected_winner
        
        if is_draw:
            actual_winner = 0.5
            actual_loser = 0.5
        else:
            actual_winner = 1.0
            actual_loser = 0.0
        
        new_winner = winner_rating + self.k_factor * (actual_winner - expected_winner)
        new_loser = loser_rating + self.k_factor * (actual_loser - expected_loser)
        
        return int(new_winner), int(new_loser)


# ==================== ARENA SYSTEM ====================

class Arena:
    """Main Arena building - manages all PvP combat."""
    
    def __init__(self):
        self.active_matches: Dict[str, ArenaMatch] = {}
        self.match_history: List[ArenaMatch] = []
        self.player_stats: Dict[str, Dict] = {}
        self.leaderboard: Dict[str, int] = {}  # player_id -> ELO
        self.elo_system = ELOSystem()
        
        self.match_count = 0
    
    # ==================== MATCHMAKING ====================
    
    def create_match(
        self,
        player1_id: str,
        player1_name: str,
        player2_id: str,
        player2_name: str,
        challenge_id: str,
        player1_loadout: Optional[Loadout] = None,
        player2_loadout: Optional[Loadout] = None
    ) -> ArenaMatch:
        """Create a new PvP match."""
        self.match_count += 1
        match_id = f"match_{self.match_count:04d}"
        
        challenge = ARENA_CHALLENGES.get(challenge_id)
        if not challenge:
            raise ValueError(f"Unknown challenge: {challenge_id}")
        
        match = ArenaMatch(
            id=match_id,
            challenge=challenge,
            player1_id=player1_id,
            player2_id=player2_id,
            player1_name=player1_name,
            player2_name=player2_name,
            player1_loadout=player1_loadout or Loadout(),
            player2_loadout=player2_loadout or Loadout()
        )
        
        self.active_matches[match_id] = match
        
        print(f"\n⚔️ ARENA MATCH CREATED: {match_id}")
        print(f"🥊 {player1_name} vs {player2_name}")
        print(f"🎯 Challenge: {challenge.title}")
        print(f"⏱️ Time Limit: {challenge.time_limit}s")
        
        return match
    
    def start_match(self, match_id: str) -> bool:
        """Begin the match timer."""
        match = self.active_matches.get(match_id)
        if not match:
            return False
        
        match.started_at = time.time()
        
        print(f"\n🔔 FIGHT!")
        print(f"⏳ {match.challenge.time_limit} seconds on the clock...")
        
        return True
    
    # ==================== SUBMISSIONS ====================
    
    def submit_solution(
        self,
        match_id: str,
        player_id: str,
        solution_code: str
    ) -> Dict:
        """Player submits their solution."""
        match = self.active_matches.get(match_id)
        if not match:
            return {"error": "Match not found"}
        
        if not match.started_at:
            return {"error": "Match not started"}
        
        submission_time = time.time() - match.started_at
        
        if submission_time > match.challenge.time_limit:
            return {"error": "Time expired"}
        
        # Record submission
        if player_id == match.player1_id:
            match.player1_submission = solution_code
            match.player1_time = submission_time
        elif player_id == match.player2_id:
            match.player2_submission = solution_code
            match.player2_time = submission_time
        else:
            return {"error": "Player not in match"}
        
        # Score the submission
        score = self._score_submission(match, player_id, solution_code, submission_time)
        
        if player_id == match.player1_id:
            match.player1_score = score
        else:
            match.player2_score = score
        
        print(f"✅ {match.player1_name if player_id == match.player1_id else match.player2_name} submitted!")
        print(f"⏱️ Time: {submission_time:.1f}s")
        print(f"🎯 Score: {score}/{match.challenge.max_score + match.challenge.speed_bonus + match.challenge.quality_bonus}")
        
        # Check if both submitted
        if match.player1_submission and match.player2_submission:
            self._end_match(match_id)
        
        return {
            "success": True,
            "score": score,
            "time": submission_time
        }
    
    def _score_submission(
        self,
        match: ArenaMatch,
        player_id: str,
        code: str,
        time_taken: float
    ) -> int:
        """Score a submission based on multiple factors."""
        score = 0
        
        # Base score (correctness - simulated for demo)
        base_score = random.randint(60, match.challenge.max_score)
        score += base_score
        
        # Speed bonus
        time_percent = time_taken / match.challenge.time_limit
        if time_percent < 0.5:
            speed_bonus = int(match.challenge.speed_bonus * (1 - time_percent))
            score += speed_bonus
        
        # Quality bonus (code analysis - simulated)
        quality_score = self._analyze_code_quality(code)
        score += int(match.challenge.quality_bonus * quality_score)
        
        # Loadout bonuses
        loadout = match.player1_loadout if player_id == match.player1_id else match.player2_loadout
        score += loadout.quality_bonus
        score = int(score * loadout.speed_multiplier)
        
        return score
    
    def _analyze_code_quality(self, code: str) -> float:
        """Simple code quality heuristic (0.0-1.0)."""
        # Check for good practices
        quality = 0.5  # baseline
        
        # Comments
        if '#' in code or '"""' in code:
            quality += 0.1
        
        # Proper indentation
        if '    ' in code:
            quality += 0.1
        
        # Named variables (not single letters, except in comprehensions)
        if any(len(word) > 2 for word in code.split() if word.isalpha()):
            quality += 0.1
        
        # Functions/classes defined
        if 'def ' in code or 'class ' in code:
            quality += 0.1
        
        # Not too long
        if len(code.splitlines()) < 50:
            quality += 0.1
        
        return min(1.0, quality)
    
    # ==================== MATCH RESOLUTION ====================
    
    def _end_match(self, match_id: str):
        """Finalize match and determine winner."""
        match = self.active_matches.get(match_id)
        if not match:
            return
        
        match.ended_at = time.time()
        
        # Determine winner
        if match.player1_score > match.player2_score:
            match.result = CombatResult.PLAYER1_WIN
            match.winner_id = match.player1_id
        elif match.player2_score > match.player1_score:
            match.result = CombatResult.PLAYER2_WIN
            match.winner_id = match.player2_id
        else:
            match.result = CombatResult.DRAW
        
        # Update ELO
        self._update_elo(match)
        
        # Update stats
        self._update_player_stats(match)
        
        # Resolve bets
        self._resolve_bets(match)
        
        # Move to history
        self.match_history.append(match)
        del self.active_matches[match_id]
        
        self._announce_winner(match)
    
    def _update_elo(self, match: ArenaMatch):
        """Update player ELO ratings."""
        p1_elo = self.leaderboard.get(match.player1_id, 1200)
        p2_elo = self.leaderboard.get(match.player2_id, 1200)
        
        if match.result == CombatResult.DRAW:
            new_p1, new_p2 = self.elo_system.update_ratings(p1_elo, p2_elo, is_draw=True)
        elif match.result == CombatResult.PLAYER1_WIN:
            new_p1, new_p2 = self.elo_system.update_ratings(p1_elo, p2_elo)
        else:
            new_p2, new_p1 = self.elo_system.update_ratings(p2_elo, p1_elo)
        
        self.leaderboard[match.player1_id] = new_p1
        self.leaderboard[match.player2_id] = new_p2
    
    def _update_player_stats(self, match: ArenaMatch):
        """Update player statistics."""
        for player_id in [match.player1_id, match.player2_id]:
            if player_id not in self.player_stats:
                self.player_stats[player_id] = {
                    "matches_played": 0,
                    "wins": 0,
                    "losses": 0,
                    "draws": 0,
                    "total_score": 0,
                    "avg_time": 0,
                    "fastest_win": None
                }
            
            stats = self.player_stats[player_id]
            stats["matches_played"] += 1
            
            if match.winner_id == player_id:
                stats["wins"] += 1
                submit_time = match.player1_time if player_id == match.player1_id else match.player2_time
                if stats["fastest_win"] is None or submit_time < stats["fastest_win"]:
                    stats["fastest_win"] = submit_time
            elif match.result == CombatResult.DRAW:
                stats["draws"] += 1
            else:
                stats["losses"] += 1
            
            score = match.player1_score if player_id == match.player1_id else match.player2_score
            stats["total_score"] += score
    
    # ==================== SPECTATORS & BETTING ====================
    
    def add_spectator(self, match_id: str, spectator_id: str) -> bool:
        """Add spectator to match."""
        match = self.active_matches.get(match_id)
        if not match:
            return False
        
        if spectator_id not in match.spectators:
            match.spectators.append(spectator_id)
        
        return True
    
    def place_bet(
        self,
        match_id: str,
        spectator_id: str,
        player_id: str,
        amount: int
    ) -> bool:
        """Spectator bets on a player."""
        match = self.active_matches.get(match_id)
        if not match or match.started_at:
            return False
        
        if player_id not in [match.player1_id, match.player2_id]:
            return False
        
        match.bets[spectator_id] = (player_id, amount)
        
        print(f"💰 Bet placed: {amount} coins on {match.player1_name if player_id == match.player1_id else match.player2_name}")
        
        return True
    
    def _resolve_bets(self, match: ArenaMatch):
        """Pay out winning bets."""
        if not match.bets or match.result == CombatResult.DRAW:
            return
        
        print("\n💸 RESOLVING BETS...")
        
        for spectator_id, (bet_player, amount) in match.bets.items():
            if bet_player == match.winner_id:
                payout = amount * 2
                print(f"  🎉 {spectator_id} wins {payout} coins!")
            else:
                print(f"  💀 {spectator_id} loses {amount} coins")
    
    # ==================== DISPLAY & QUERIES ====================
    
    def _announce_winner(self, match: ArenaMatch):
        """Dramatic match conclusion."""
        print("\n" + "="*60)
        print("🏆 MATCH COMPLETE!")
        print("="*60)
        
        print(f"\n🥊 {match.player1_name} vs {match.player2_name}")
        print(f"🎯 Challenge: {match.challenge.title}")
        
        print(f"\n📊 FINAL SCORES:")
        print(f"  {match.player1_name}: {match.player1_score} ({match.player1_time:.1f}s)")
        print(f"  {match.player2_name}: {match.player2_score} ({match.player2_time:.1f}s)")
        
        if match.result == CombatResult.DRAW:
            print(f"\n🤝 DRAW!")
        else:
            winner_name = match.player1_name if match.winner_id == match.player1_id else match.player2_name
            print(f"\n👑 WINNER: {winner_name}")
        
        print(f"\n📈 ELO CHANGES:")
        print(f"  {match.player1_name}: {self.leaderboard[match.player1_id]}")
        print(f"  {match.player2_name}: {self.leaderboard[match.player2_id]}")
        
        if match.spectators:
            print(f"\n👥 Spectators: {len(match.spectators)}")
    
    def show_leaderboard(self, top_n: int = 10):
        """Display top players by ELO."""
        print("\n🏆 ARENA LEADERBOARD")
        print("="*60)
        
        sorted_players = sorted(
            self.leaderboard.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        for rank, (player_id, elo) in enumerate(sorted_players, 1):
            stats = self.player_stats.get(player_id, {})
            wins = stats.get("wins", 0)
            losses = stats.get("losses", 0)
            
            print(f"#{rank}. {player_id}")
            print(f"     ELO: {elo} | W/L: {wins}/{losses}")
    
    def show_player_stats(self, player_id: str):
        """Display detailed player statistics."""
        stats = self.player_stats.get(player_id)
        if not stats:
            print(f"No stats found for {player_id}")
            return
        
        elo = self.leaderboard.get(player_id, 1200)
        
        print(f"\n📊 PLAYER STATS: {player_id}")
        print("="*60)
        print(f"ELO Rating: {elo}")
        print(f"Matches Played: {stats['matches_played']}")
        print(f"Record: {stats['wins']}W / {stats['losses']}L / {stats['draws']}D")
        
        if stats['matches_played'] > 0:
            win_rate = (stats['wins'] / stats['matches_played']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        
        if stats['fastest_win']:
            print(f"Fastest Win: {stats['fastest_win']:.1f}s")


# ==================== DEMO ====================

if __name__ == "__main__":
    print("🏟️ ARENA PVP SYSTEM DEMO")
    print("="*60)
    
    arena = Arena()
    
    # Create match
    print("\n--- CREATING MATCH ---")
    match = arena.create_match(
        player1_id="bleak_001",
        player1_name="BlekDev",
        player2_id="claude_001",
        player2_name="ClaudeAI",
        challenge_id="spaghetti_untangle"
    )
    
    # Add spectators
    arena.add_spectator(match.id, "grok_spec")
    arena.add_spectator(match.id, "deepseek_spec")
    
    # Place bets
    arena.place_bet(match.id, "grok_spec", "bleak_001", 100)
    arena.place_bet(match.id, "deepseek_spec", "claude_001", 150)
    
    # Start match
    print("\n--- STARTING MATCH ---")
    arena.start_match(match.id)
    
    # Simulate submissions
    time.sleep(1)
    
    print("\n--- PLAYERS SUBMIT SOLUTIONS ---")
    arena.submit_solution(
        match.id,
        "bleak_001",
        "def process(data): return [str(x).upper() if x else 'None' for x in data]"
    )
    
    time.sleep(0.5)
    
    arena.submit_solution(
        match.id,
        "claude_001",
        "def process(data): return [str(item).upper() if item else 'None' for item in (data or [])]"
    )
    
    # Show leaderboard
    print("\n--- LEADERBOARD ---")
    arena.show_leaderboard()
    
    print("\n🏁 Demo complete!")