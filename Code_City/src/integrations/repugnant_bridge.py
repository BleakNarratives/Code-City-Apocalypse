# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/integrations/repugnant_bridge.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/integrations/repugnant_bridge.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-integrations
# DEPS: dataclasses, enum, json, statistics, time, typing
# ROLE: Repugnant Integration Bridge
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]


"""
Repugnant Integration Bridge
Connects Code City to Repugnant (human behavior monitor) for:
- Real-time emotional state tracking during boss fights
- Adaptive difficulty based on frustration levels
- Taunt effectiveness analysis for Mayor Strump
- Team dynamics monitoring
- Mentor/mentee relationship insights
"""

import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import statistics

# ==================== EMOTIONAL STATES ====================

class EmotionalState(Enum):
    CONFIDENT = "confident"
    FOCUSED = "focused"
    FRUSTRATED = "frustrated"
    TILTED = "tilted"          # Gaming term for angry/unfocused
    BURNT_OUT = "burnt_out"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    FLOW_STATE = "flow_state"  # In the zone

class TauntReaction(Enum):
    MOTIVATED = "motivated"     # Taunt made them try harder
    DEFENSIVE = "defensive"     # Got under their skin
    IGNORED = "ignored"         # Didn't care
    AMUSED = "amused"          # Thought it was funny
    RAGE_QUIT = "rage_quit"    # Too much

# ==================== DATA STRUCTURES ====================

@dataclass
class BehavioralSnapshot:
    """A moment in time capturing player behavior."""
    timestamp: float
    player_id: str
    session_id: str
    
    # Context
    game_phase: str
    boss_health_percent: float
    player_performance: str  # "winning", "struggling", "neutral"
    
    # Emotional indicators
    emotional_state: EmotionalState
    confidence_score: float  # 0.0-1.0
    frustration_level: float  # 0.0-1.0
    
    # Behavioral signals
    action_speed: float  # Commands per minute
    error_rate: float    # Mistakes per action
    chat_sentiment: float  # -1.0 (negative) to 1.0 (positive)
    
    # Reactions
    last_taunt: Optional[str] = None
    taunt_reaction: Optional[TauntReaction] = None


@dataclass
class PlayerProfile:
    """Long-term behavioral profile of a player."""
    player_id: str
    created_at: float
    
    # Personality traits
    tilt_threshold: float = 0.5  # How easily frustrated
    competitiveness: float = 0.5  # How much they care about winning
    learning_speed: float = 0.5   # How fast they improve
    social_preference: float = 0.5  # Solo vs team player
    
    # Historical data
    total_sessions: int = 0
    total_rage_quits: int = 0
    favorite_taunt: Optional[str] = None
    most_effective_taunt: Optional[str] = None
    
    # Patterns
    performance_trend: List[float] = field(default_factory=list)
    emotional_baseline: EmotionalState = EmotionalState.FOCUSED


@dataclass
class TauntEffectiveness:
    """Analysis of how well a taunt performs."""
    taunt_text: str
    times_used: int = 0
    
    reactions: Dict[TauntReaction, int] = field(default_factory=dict)
    avg_performance_change: float = 0.0  # Did they get better or worse after?
    
    # Demographics
    effective_on_juniors: bool = False
    effective_on_seniors: bool = False
    backfire_rate: float = 0.0  # Caused rage quits


# ==================== REPUGNANT BRIDGE ====================

class RepugnantBridge:
    """
    Bridge between Code City and Repugnant behavioral monitor.
    Tracks player psychology, adapts game difficulty, optimizes taunts.
    """
    
    def __init__(self):
        self.behavioral_snapshots: List[BehavioralSnapshot] = []
        self.player_profiles: Dict[str, PlayerProfile] = {}
        self.taunt_effectiveness: Dict[str, TauntEffectiveness] = {}
        
        self.tracking_enabled = False
        
        # Thresholds for intervention
        self.frustration_warning_threshold = 0.7
        self.frustration_critical_threshold = 0.9
        self.burnout_session_count = 5
    
    # ==================== REAL-TIME TRACKING ====================
    
    def capture_snapshot(
        self,
        player_id: str,
        session_id: str,
        game_context: Dict,
        behavioral_signals: Dict
    ) -> BehavioralSnapshot:
        """Capture a behavioral snapshot."""
        # Ensure player profile exists
        if player_id not in self.player_profiles:
            self._create_player_profile(player_id)
        
        # Parse emotional state from signals
        emotional_state = self._infer_emotional_state(behavioral_signals)
        confidence = behavioral_signals.get("confidence_score", 0.5)
        frustration = behavioral_signals.get("frustration_level", 0.0)
        
        snapshot = BehavioralSnapshot(
            timestamp=time.time(),
            player_id=player_id,
            session_id=session_id,
            game_phase=game_context.get("phase", "unknown"),
            boss_health_percent=game_context.get("boss_health", 100.0),
            player_performance=game_context.get("performance", "neutral"),
            emotional_state=emotional_state,
            confidence_score=confidence,
            frustration_level=frustration,
            action_speed=behavioral_signals.get("action_speed", 0.0),
            error_rate=behavioral_signals.get("error_rate", 0.0),
            chat_sentiment=behavioral_signals.get("chat_sentiment", 0.0)
        )
        
        self.behavioral_snapshots.append(snapshot)
        
        # Check for intervention triggers
        self._check_intervention_triggers(snapshot)
        
        return snapshot
    
    def _infer_emotional_state(self, signals: Dict) -> EmotionalState:
        """Infer emotional state from behavioral signals."""
        frustration = signals.get("frustration_level", 0.0)
        confidence = signals.get("confidence_score", 0.5)
        action_speed = signals.get("action_speed", 0.0)
        error_rate = signals.get("error_rate", 0.0)
        
        # High frustration states
        if frustration > 0.8 and error_rate > 0.5:
            return EmotionalState.TILTED
        elif frustration > 0.6:
            return EmotionalState.FRUSTRATED
        
        # Low engagement
        elif confidence < 0.3 and action_speed < 0.3:
            return EmotionalState.BURNT_OUT
        
        # Positive states
        elif confidence > 0.7 and error_rate < 0.2:
            if action_speed > 0.8:
                return EmotionalState.FLOW_STATE
            else:
                return EmotionalState.CONFIDENT
        
        elif action_speed > 0.7:
            return EmotionalState.EXCITED
        
        # Default
        return EmotionalState.FOCUSED
    
    def _check_intervention_triggers(self, snapshot: BehavioralSnapshot):
        """Check if intervention is needed."""
        if snapshot.frustration_level >= self.frustration_critical_threshold:
            print(f"\n🚨 CRITICAL: {snapshot.player_id} showing extreme frustration!")
            print("   Recommendation: Reduce boss difficulty or suggest break")
            self._trigger_intervention(snapshot.player_id, "frustration_critical")
        
        elif snapshot.frustration_level >= self.frustration_warning_threshold:
            print(f"\n⚠️ WARNING: {snapshot.player_id} frustration rising")
            print("   Recommendation: Mayor Strump should ease up on taunts")
            self._trigger_intervention(snapshot.player_id, "frustration_warning")
        
        elif snapshot.emotional_state == EmotionalState.BURNT_OUT:
            print(f"\n😴 BURNOUT DETECTED: {snapshot.player_id}")
            print("   Recommendation: Suggest break or change activity")
    
    def _trigger_intervention(self, player_id: str, intervention_type: str):
        """Take adaptive action based on player state."""
        # This would send signals back to game systems
        pass
    
    # ==================== TAUNT ANALYSIS ====================
    
    def record_taunt(
        self,
        player_id: str,
        taunt_text: str,
        context: Dict
    ):
        """Record a taunt being delivered to player."""
        # Find most recent snapshot
        recent = self._get_recent_snapshot(player_id)
        if recent:
            recent.last_taunt = taunt_text
    
    def record_taunt_reaction(
        self,
        player_id: str,
        reaction: TauntReaction,
        performance_before: float,
        performance_after: float
    ):
        """Record how player reacted to taunt."""
        recent = self._get_recent_snapshot(player_id)
        if not recent or not recent.last_taunt:
            return
        
        recent.taunt_reaction = reaction
        
        # Update taunt effectiveness
        taunt_text = recent.last_taunt
        if taunt_text not in self.taunt_effectiveness:
            self.taunt_effectiveness[taunt_text] = TauntEffectiveness(
                taunt_text=taunt_text
            )
        
        effectiveness = self.taunt_effectiveness[taunt_text]
        effectiveness.times_used += 1
        
        # Track reaction
        if reaction not in effectiveness.reactions:
            effectiveness.reactions[reaction] = 0
        effectiveness.reactions[reaction] += 1
        
        # Track performance change
        perf_change = performance_after - performance_before
        effectiveness.avg_performance_change = (
            (effectiveness.avg_performance_change * (effectiveness.times_used - 1) + perf_change)
            / effectiveness.times_used
        )
        
        # Track backfires
        if reaction == TauntReaction.RAGE_QUIT:
            effectiveness.backfire_rate = (
                effectiveness.reactions[TauntReaction.RAGE_QUIT] / effectiveness.times_used
            )
            
            # Update player profile
            profile = self.player_profiles.get(player_id)
            if profile:
                profile.total_rage_quits += 1
        
        # Update favorite taunt for this player
        self._update_player_taunt_preferences(player_id, taunt_text, reaction)
    
    def _update_player_taunt_preferences(
        self,
        player_id: str,
        taunt: str,
        reaction: TauntReaction
    ):
        """Update which taunts work best on this player."""
        profile = self.player_profiles.get(player_id)
        if not profile:
            return
        
        # If taunt motivated them, it's effective
        if reaction == TauntReaction.MOTIVATED:
            profile.most_effective_taunt = taunt
        
        # Track most common taunt
        # (simplified - in production would track frequency)
        profile.favorite_taunt = taunt
    
    def get_optimal_taunt_for_player(
        self,
        player_id: str,
        current_state: EmotionalState
    ) -> Optional[str]:
        """Recommend best taunt for player's current state."""
        profile = self.player_profiles.get(player_id)
        if not profile:
            return None
        
        # If player is tilted, ease up
        if current_state in [EmotionalState.TILTED, EmotionalState.BURNT_OUT]:
            return None  # Signal: don't taunt right now
        
        # If player is confident, use their most effective taunt
        if current_state == EmotionalState.CONFIDENT:
            return profile.most_effective_taunt
        
        # For other states, use general effective taunts
        best_taunts = sorted(
            self.taunt_effectiveness.values(),
            key=lambda t: (
                t.reactions.get(TauntReaction.MOTIVATED, 0) - 
                t.reactions.get(TauntReaction.RAGE_QUIT, 0)
            ),
            reverse=True
        )
        
        return best_taunts[0].taunt_text if best_taunts else None
    
    # ==================== PLAYER PROFILING ====================
    
    def _create_player_profile(self, player_id: str) -> PlayerProfile:
        """Initialize new player profile."""
        profile = PlayerProfile(
            player_id=player_id,
            created_at=time.time()
        )
        
        self.player_profiles[player_id] = profile
        
        return profile
    
    def update_player_profile(
        self,
        player_id: str,
        session_summary: Dict
    ):
        """Update profile after session ends."""
        profile = self.player_profiles.get(player_id)
        if not profile:
            return
        
        profile.total_sessions += 1
        
        # Update performance trend
        performance_score = session_summary.get("performance_score", 0.5)
        profile.performance_trend.append(performance_score)
        
        # Keep only last 10 sessions
        if len(profile.performance_trend) > 10:
            profile.performance_trend.pop(0)
        
        # Calculate learning speed
        if len(profile.performance_trend) >= 3:
            trend = statistics.mean(profile.performance_trend[-3:]) - statistics.mean(profile.performance_trend[:3])
            profile.learning_speed = max(0.0, min(1.0, 0.5 + trend))
    
    def _get_recent_snapshot(self, player_id: str) -> Optional[BehavioralSnapshot]:
        """Get most recent snapshot for player."""
        player_snapshots = [s for s in self.behavioral_snapshots if s.player_id == player_id]
        return player_snapshots[-1] if player_snapshots else None
    
    # ==================== ADAPTIVE DIFFICULTY ====================
    
    def recommend_difficulty_adjustment(
        self,
        session_id: str,
        current_difficulty: float
    ) -> float:
        """Recommend difficulty adjustment based on player states."""
        # Get all recent snapshots for this session
        recent_snapshots = [
            s for s in self.behavioral_snapshots[-50:]
            if s.session_id == session_id
        ]
        
        if not recent_snapshots:
            return current_difficulty
        
        # Calculate average frustration
        avg_frustration = statistics.mean(
            s.frustration_level for s in recent_snapshots
        )
        
        # Count emotional states
        state_counts = {}
        for snapshot in recent_snapshots:
            state = snapshot.emotional_state
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # Adjust difficulty
        adjustment = 0.0
        
        # Too frustrated → easier
        if avg_frustration > 0.7:
            adjustment = -0.2
            print("📉 Recommending difficulty DECREASE (high frustration)")
        
        # Too easy/bored → harder
        elif avg_frustration < 0.2 and state_counts.get(EmotionalState.BURNT_OUT, 0) > 5:
            adjustment = 0.1
            print("📈 Recommending difficulty INCREASE (players bored)")
        
        # Flow state → perfect, don't change
        elif state_counts.get(EmotionalState.FLOW_STATE, 0) > 10:
            print("✅ Perfect difficulty (players in flow state)")
        
        new_difficulty = max(0.1, min(1.0, current_difficulty + adjustment))
        
        return new_difficulty
    
    # ==================== TEAM DYNAMICS ====================
    
    def analyze_team_dynamics(
        self,
        session_id: str,
        player_ids: List[str]
    ) -> Dict:
        """Analyze how well team is working together."""
        snapshots = [
            s for s in self.behavioral_snapshots[-100:]
            if s.session_id == session_id and s.player_id in player_ids
        ]
        
        if not snapshots:
            return {}
        
        # Group by player
        by_player = {}
        for snapshot in snapshots:
            if snapshot.player_id not in by_player:
                by_player[snapshot.player_id] = []
            by_player[snapshot.player_id].append(snapshot)
        
        # Calculate team cohesion indicators
        frustration_spread = statistics.stdev([
            statistics.mean(s.frustration_level for s in snaps)
            for snaps in by_player.values()
        ])
        
        # Low spread = team is feeling similar (good)
        # High spread = some frustrated, some not (bad)
        cohesion_score = 1.0 - min(1.0, frustration_spread)
        
        return {
            "cohesion_score": cohesion_score,
            "avg_frustration": statistics.mean(s.frustration_level for s in snapshots),
            "players_tilted": sum(
                1 for snaps in by_player.values()
                if statistics.mean(s.frustration_level for s in snaps) > 0.7
            ),
            "recommendation": (
                "Team cohesion good" if cohesion_score > 0.7
                else "Consider team meeting at Obelisk"
            )
        }
    
    # ==================== MENTOR/MENTEE INSIGHTS ====================
    
    def analyze_mentor_relationship(
        self,
        mentor_id: str,
        mentee_id: str,
        session_id: str
    ) -> Dict:
        """Analyze effectiveness of mentor/mentee pairing."""
        mentee_snapshots = [
            s for s in self.behavioral_snapshots[-50:]
            if s.player_id == mentee_id and s.session_id == session_id
        ]
        
        if not mentee_snapshots:
            return {}
        
        # Check if mentee improving
        if len(mentee_snapshots) >= 10:
            early_performance = statistics.mean(
                s.confidence_score for s in mentee_snapshots[:5]
            )
            late_performance = statistics.mean(
                s.confidence_score for s in mentee_snapshots[-5:]
            )
            
            improvement = late_performance - early_performance
            
            return {
                "mentee_improving": improvement > 0.1,
                "improvement_rate": improvement,
                "mentee_frustration": statistics.mean(s.frustration_level for s in mentee_snapshots),
                "recommendation": (
                    "Mentorship working well" if improvement > 0.1
                    else "Mentee may need different approach"
                )
            }
        
        return {"status": "Not enough data yet"}
    
    # ==================== EXPORTS & REPORTS ====================
    
    def generate_player_report(self, player_id: str) -> Dict:
        """Generate comprehensive behavioral report."""
        profile = self.player_profiles.get(player_id)
        if not profile:
            return {}
        
        player_snapshots = [
            s for s in self.behavioral_snapshots
            if s.player_id == player_id
        ]
        
        if not player_snapshots:
            return {"profile": profile}
        
        return {
            "player_id": player_id,
            "total_sessions": profile.total_sessions,
            "total_snapshots": len(player_snapshots),
            "avg_frustration": statistics.mean(s.frustration_level for s in player_snapshots),
            "rage_quit_rate": profile.total_rage_quits / max(1, profile.total_sessions),
            "most_common_state": max(
                set(s.emotional_state for s in player_snapshots),
                key=lambda state: sum(1 for s in player_snapshots if s.emotional_state == state)
            ).value,
            "most_effective_taunt": profile.most_effective_taunt,
            "learning_trend": "improving" if profile.learning_speed > 0.6 else "stable",
            "personality": {
                "tilt_threshold": profile.tilt_threshold,
                "competitiveness": profile.competitiveness,
                "social_preference": profile.social_preference
            }
        }
    
    def export_taunt_effectiveness_report(self, filepath: str):
        """Export taunt analysis to JSON."""
        report = {
            "taunts": [
                {
                    "text": t.taunt_text,
                    "times_used": t.times_used,
                    "reactions": {k.value: v for k, v in t.reactions.items()},
                    "avg_performance_change": t.avg_performance_change,
                    "backfire_rate": t.backfire_rate
                }
                for t in sorted(
                    self.taunt_effectiveness.values(),
                    key=lambda x: x.times_used,
                    reverse=True
                )
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Taunt effectiveness report exported to {filepath}")


# ==================== DEMO ====================

if __name__ == "__main__":
    print("💀 REPUGNANT INTEGRATION DEMO")
    print("="*60)
    
    bridge = RepugnantBridge()
    bridge.tracking_enabled = True
    
    # Simulate player session
    print("\n--- SIMULATING PLAYER SESSION ---")
    
    player_id = "bleak_001"
    session_id = "raid_001"
    
    # Early game - confident
    snapshot1 = bridge.capture_snapshot(
        player_id=player_id,
        session_id=session_id,
        game_context={
            "phase": "raid_active",
            "boss_health": 100.0,
            "performance": "winning"
        },
        behavioral_signals={
            "confidence_score": 0.8,
            "frustration_level": 0.2,
            "action_speed": 0.7,
            "error_rate": 0.1,
            "chat_sentiment": 0.5
        }
    )
    
    print(f"State: {snapshot1.emotional_state.value}")
    
    # Record taunt
    time.sleep(1)
    taunt = "Your code is almost as messy as your commit history!"
    bridge.record_taunt(player_id, taunt, {})
    
    # Mid game - getting frustrated
    snapshot2 = bridge.capture_snapshot(
        player_id=player_id,
        session_id=session_id,
        game_context={
            "phase": "raid_active",
            "boss_health": 60.0,
            "performance": "struggling"
        },
        behavioral_signals={
            "confidence_score": 0.5,
            "frustration_level": 0.6,
            "action_speed": 0.9,
            "error_rate": 0.4,
            "chat_sentiment": -0.3
        }
    )
    
    print(f"State: {snapshot2.emotional_state.value}")
    
    # Record reaction to taunt
    bridge.record_taunt_reaction(
        player_id,
        TauntReaction.DEFENSIVE,
        performance_before=0.7,
        performance_after=0.5
    )
    
    # Late game - tilted
    snapshot3 = bridge.capture_snapshot(
        player_id=player_id,
        session_id=session_id,
        game_context={
            "phase": "raid_active",
            "boss_health": 30.0,
            "performance": "struggling"
        },
        behavioral_signals={
            "confidence_score": 0.3,
            "frustration_level": 0.85,
            "action_speed": 1.2,
            "error_rate": 0.7,
            "chat_sentiment": -0.8
        }
    )
    
    print(f"State: {snapshot3.emotional_state.value}")
    
    # Get difficulty recommendation
    print("\n--- DIFFICULTY ANALYSIS ---")
    new_diff = bridge.recommend_difficulty_adjustment(session_id, 0.7)
    print(f"Recommended difficulty: {new_diff}")
    
    # Get optimal taunt
    print("\n--- TAUNT OPTIMIZATION ---")
    optimal = bridge.get_optimal_taunt_for_player(player_id, snapshot3.emotional_state)
    print(f"Optimal taunt: {optimal or 'NONE (player too tilted)'}")
    
    # Generate report
    print("\n--- PLAYER REPORT ---")
    report = bridge.generate_player_report(player_id)
    print(json.dumps(report, indent=2))
    
    print("\n🏁 Demo complete!")