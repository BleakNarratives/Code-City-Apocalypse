# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/multiplayer/session_manager.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/multiplayer/session_manager.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-multiplayer
# DEPS: dataclasses, enum, json, time, typing, uuid
# ROLE: Multiplayer Session Manager
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]


"""
Multiplayer Session Manager
Handles lobby creation, role assignment, state synchronization, and combat coordination.
Supports co-op raids, PvP duels, and mentor/mentee modes.
"""

import json
import time
import uuid
from typing import Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict

# ==================== ENUMS & DATA CLASSES ====================

class SessionMode(Enum):
    COOP_RAID = "coop_raid"           # Team vs Boss
    PVP_ARENA = "pvp_arena"           # 1v1 or team vs team
    MENTOR_MODE = "mentor_mode"        # Experienced + Junior
    FREE_ROAM = "free_roam"           # Casual exploration

class PlayerRole(Enum):
    ARCHITECT = "architect"            # Senior dev (tank/strategist)
    SCRAPPER = "scrapper"             # Junior dev (DPS/learner)
    MEDIC = "medic"                   # QA/Tester (healer)
    ARSONIST = "arsonist"             # Refactorer (high risk/reward)
    SCOUT = "scout"                   # DevOps (utility)
    NECROMANCER = "necromancer"       # Legacy specialist (niche power)
    SPECTATOR = "spectator"           # Mentor/observer

class SessionState(Enum):
    LOBBY = "lobby"                   # Waiting for players
    IN_PROGRESS = "in_progress"       # Active gameplay
    PAUSED = "paused"                 # Temporary halt
    COMPLETED = "completed"           # Finished
    ABANDONED = "abandoned"           # Disbanded early

@dataclass
class Player:
    """Represents a player in the session."""
    id: str
    name: str
    role: PlayerRole
    is_ready: bool = False
    is_host: bool = False
    stats: Dict = None
    
    def __post_init__(self):
        if self.stats is None:
            self.stats = {
                "damage_dealt": 0,
                "buildings_fixed": 0,
                "bugs_squashed": 0,
                "deaths": 0,
                "assists": 0
            }

@dataclass
class Session:
    """Represents a multiplayer session."""
    id: str
    name: str
    mode: SessionMode
    state: SessionState
    host_id: str
    players: Dict[str, Player]
    max_players: int
    created_at: float
    started_at: Optional[float] = None
    ended_at: Optional[float] = None
    
    # Shared game state
    city_state: Dict = None
    boss_state: Dict = None
    combat_log: List[Dict] = None
    
    def __post_init__(self):
        if self.city_state is None:
            self.city_state = {}
        if self.boss_state is None:
            self.boss_state = {}
        if self.combat_log is None:
            self.combat_log = []


# ==================== SESSION MANAGER ====================

class SessionManager:
    """
    Central coordinator for multiplayer sessions.
    Handles creation, joining, state sync, and event broadcasting.
    """
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.player_to_session: Dict[str, str] = {}  # player_id -> session_id
        self.event_callbacks: List[Callable] = []
        
    # ==================== SESSION LIFECYCLE ====================
    
    def create_session(
        self,
        host_name: str,
        session_name: str,
        mode: SessionMode,
        max_players: int = 4
    ) -> Session:
        """Create a new multiplayer session."""
        session_id = str(uuid.uuid4())[:8]
        host_id = str(uuid.uuid4())[:8]
        
        host = Player(
            id=host_id,
            name=host_name,
            role=PlayerRole.ARCHITECT,  # Default host role
            is_host=True
        )
        
        session = Session(
            id=session_id,
            name=session_name,
            mode=mode,
            state=SessionState.LOBBY,
            host_id=host_id,
            players={host_id: host},
            max_players=max_players,
            created_at=time.time()
        )
        
        self.sessions[session_id] = session
        self.player_to_session[host_id] = session_id
        
        self._broadcast_event({
            "type": "session_created",
            "session_id": session_id,
            "host": host_name,
            "mode": mode.value
        })
        
        return session
    
    def join_session(
        self,
        session_id: str,
        player_name: str,
        preferred_role: Optional[PlayerRole] = None
    ) -> Optional[Player]:
        """Join an existing session."""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        if session.state != SessionState.LOBBY:
            print(f"❌ Cannot join: Session {session_id} already in progress")
            return None
        
        if len(session.players) >= session.max_players:
            print(f"❌ Cannot join: Session {session_id} is full")
            return None
        
        # Auto-assign role if not specified or taken
        if preferred_role is None or self._is_role_taken(session, preferred_role):
            preferred_role = self._auto_assign_role(session)
        
        player_id = str(uuid.uuid4())[:8]
        player = Player(
            id=player_id,
            name=player_name,
            role=preferred_role
        )
        
        session.players[player_id] = player
        self.player_to_session[player_id] = session_id
        
        self._broadcast_event({
            "type": "player_joined",
            "session_id": session_id,
            "player": player_name,
            "role": preferred_role.value
        })
        
        return player
    
    def leave_session(self, player_id: str) -> bool:
        """Remove player from their current session."""
        session_id = self.player_to_session.get(player_id)
        
        if not session_id:
            return False
        
        session = self.sessions[session_id]
        player = session.players.pop(player_id, None)
        
        if not player:
            return False
        
        del self.player_to_session[player_id]
        
        # If host left, transfer to another player or disband
        if player.is_host:
            if session.players:
                new_host_id = list(session.players.keys())[0]
                session.players[new_host_id].is_host = True
                session.host_id = new_host_id
                self._broadcast_event({
                    "type": "host_transferred",
                    "session_id": session_id,
                    "new_host": session.players[new_host_id].name
                })
            else:
                self._disband_session(session_id)
                return True
        
        self._broadcast_event({
            "type": "player_left",
            "session_id": session_id,
            "player": player.name
        })
        
        return True
    
    def _disband_session(self, session_id: str):
        """Remove session and clean up all players."""
        session = self.sessions.pop(session_id, None)
        if not session:
            return
        
        for player_id in session.players.keys():
            self.player_to_session.pop(player_id, None)
        
        self._broadcast_event({
            "type": "session_disbanded",
            "session_id": session_id
        })
    
    # ==================== ROLE MANAGEMENT ====================
    
    def _is_role_taken(self, session: Session, role: PlayerRole) -> bool:
        """Check if role is already assigned (except spectator)."""
        if role == PlayerRole.SPECTATOR:
            return False
        
        return any(p.role == role for p in session.players.values())
    
    def _auto_assign_role(self, session: Session) -> PlayerRole:
        """Assign first available role."""
        available_roles = [
            PlayerRole.SCRAPPER,
            PlayerRole.MEDIC,
            PlayerRole.ARSONIST,
            PlayerRole.SCOUT,
            PlayerRole.NECROMANCER
        ]
        
        for role in available_roles:
            if not self._is_role_taken(session, role):
                return role
        
        return PlayerRole.SPECTATOR
    
    def change_role(
        self,
        player_id: str,
        new_role: PlayerRole
    ) -> bool:
        """Change player's role if available."""
        session_id = self.player_to_session.get(player_id)
        if not session_id:
            return False
        
        session = self.sessions[session_id]
        player = session.players.get(player_id)
        
        if not player or session.state != SessionState.LOBBY:
            return False
        
        if self._is_role_taken(session, new_role):
            return False
        
        old_role = player.role
        player.role = new_role
        
        self._broadcast_event({
            "type": "role_changed",
            "session_id": session_id,
            "player": player.name,
            "old_role": old_role.value,
            "new_role": new_role.value
        })
        
        return True
    
    # ==================== SESSION CONTROL ====================
    
    def set_ready(self, player_id: str, ready: bool = True) -> bool:
        """Mark player as ready/not ready."""
        session_id = self.player_to_session.get(player_id)
        if not session_id:
            return False
        
        session = self.sessions[session_id]
        player = session.players.get(player_id)
        
        if not player:
            return False
        
        player.is_ready = ready
        
        self._broadcast_event({
            "type": "player_ready_changed",
            "session_id": session_id,
            "player": player.name,
            "ready": ready
        })
        
        # Auto-start if all ready
        if self._all_players_ready(session):
            self.start_session(session_id)
        
        return True
    
    def _all_players_ready(self, session: Session) -> bool:
        """Check if all players are ready."""
        return all(p.is_ready for p in session.players.values())
    
    def start_session(self, session_id: str) -> bool:
        """Begin the session (only host can start)."""
        session = self.sessions.get(session_id)
        
        if not session or session.state != SessionState.LOBBY:
            return False
        
        if not self._all_players_ready(session):
            print("❌ Cannot start: Not all players ready")
            return False
        
        session.state = SessionState.IN_PROGRESS
        session.started_at = time.time()
        
        self._broadcast_event({
            "type": "session_started",
            "session_id": session_id,
            "mode": session.mode.value,
            "players": [p.name for p in session.players.values()]
        })
        
        return True
    
    def end_session(self, session_id: str, reason: str = "completed") -> bool:
        """End the session and generate summary."""
        session = self.sessions.get(session_id)
        
        if not session:
            return False
        
        session.state = SessionState.COMPLETED if reason == "completed" else SessionState.ABANDONED
        session.ended_at = time.time()
        
        duration = session.ended_at - session.started_at if session.started_at else 0
        
        summary = self._generate_session_summary(session, duration)
        
        self._broadcast_event({
            "type": "session_ended",
            "session_id": session_id,
            "reason": reason,
            "summary": summary
        })
        
        return True
    
    # ==================== STATE SYNCHRONIZATION ====================
    
    def update_city_state(self, session_id: str, city_data: Dict) -> bool:
        """Update shared city state."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.city_state.update(city_data)
        
        self._broadcast_event({
            "type": "city_state_updated",
            "session_id": session_id,
            "data": city_data
        })
        
        return True
    
    def update_boss_state(self, session_id: str, boss_data: Dict) -> bool:
        """Update shared boss state."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.boss_state.update(boss_data)
        
        self._broadcast_event({
            "type": "boss_state_updated",
            "session_id": session_id,
            "data": boss_data
        })
        
        return True
    
    def add_combat_log(self, session_id: str, action: Dict) -> bool:
        """Add entry to shared combat log."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        action['timestamp'] = time.time()
        session.combat_log.append(action)
        
        self._broadcast_event({
            "type": "combat_action",
            "session_id": session_id,
            "action": action
        })
        
        return True
    
    # ==================== PLAYER ACTIONS ====================
    
    def record_damage(self, session_id: str, player_id: str, damage: int):
        """Record damage dealt by player."""
        session = self.sessions.get(session_id)
        if not session:
            return
        
        player = session.players.get(player_id)
        if player:
            player.stats["damage_dealt"] += damage
    
    def record_fix(self, session_id: str, player_id: str):
        """Record building fixed by player."""
        session = self.sessions.get(session_id)
        if not session:
            return
        
        player = session.players.get(player_id)
        if player:
            player.stats["buildings_fixed"] += 1
    
    def record_death(self, session_id: str, player_id: str):
        """Record player death/failure."""
        session = self.sessions.get(session_id)
        if not session:
            return
        
        player = session.players.get(player_id)
        if player:
            player.stats["deaths"] += 1
    
    # ==================== EVENT SYSTEM ====================
    
    def register_callback(self, callback: Callable):
        """Register function to receive all events."""
        self.event_callbacks.append(callback)
    
    def _broadcast_event(self, event: Dict):
        """Send event to all registered callbacks."""
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"⚠️ Event callback error: {e}")
    
    # ==================== QUERIES & STATS ====================
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """Get full session details."""
        session = self.sessions.get(session_id)
        if not session:
            return None
        
        return {
            "id": session.id,
            "name": session.name,
            "mode": session.mode.value,
            "state": session.state.value,
            "host": session.players[session.host_id].name,
            "players": [
                {
                    "name": p.name,
                    "role": p.role.value,
                    "ready": p.is_ready,
                    "stats": p.stats
                }
                for p in session.players.values()
            ],
            "player_count": f"{len(session.players)}/{session.max_players}",
            "created_at": time.ctime(session.created_at)
        }
    
    def list_active_sessions(self) -> List[Dict]:
        """Get all sessions in lobby or in-progress."""
        return [
            {
                "id": s.id,
                "name": s.name,
                "mode": s.mode.value,
                "state": s.state.value,
                "players": f"{len(s.players)}/{s.max_players}"
            }
            for s in self.sessions.values()
            if s.state in [SessionState.LOBBY, SessionState.IN_PROGRESS]
        ]
    
    def _generate_session_summary(self, session: Session, duration: float) -> Dict:
        """Generate end-of-session statistics."""
        sorted_by_damage = sorted(
            session.players.values(),
            key=lambda p: p.stats["damage_dealt"],
            reverse=True
        )
        
        return {
            "duration_seconds": int(duration),
            "duration_formatted": time.strftime("%M:%S", time.gmtime(duration)),
            "mvp": sorted_by_damage[0].name if sorted_by_damage else "N/A",
            "total_damage": sum(p.stats["damage_dealt"] for p in session.players.values()),
            "total_fixes": sum(p.stats["buildings_fixed"] for p in session.players.values()),
            "leaderboard": [
                {
                    "player": p.name,
                    "role": p.role.value,
                    "damage": p.stats["damage_dealt"],
                    "fixes": p.stats["buildings_fixed"]
                }
                for p in sorted_by_damage
            ]
        }


# ==================== DEMO USAGE ====================

if __name__ == "__main__":
    print("🌐 MULTIPLAYER SESSION MANAGER DEMO")
    print("=" * 60)
    
    # Initialize manager
    manager = SessionManager()
    
    # Event callback to print all events
    def print_event(event):
        event_type = event.get("type", "unknown")
        print(f"\n📡 EVENT: {event_type}")
        for key, value in event.items():
            if key != "type":
                print(f"   {key}: {value}")
    
    manager.register_callback(print_event)
    
    # Create a co-op raid session
    print("\n--- HOST CREATES SESSION ---")
    session = manager.create_session(
        host_name="BlekDev",
        session_name="Strump Tower Raid #1",
        mode=SessionMode.COOP_RAID,
        max_players=4
    )
    
    print(f"✅ Session created: {session.id}")
    
    # Players join
    print("\n--- PLAYERS JOIN ---")
    p2 = manager.join_session(session.id, "ClaudeAI", PlayerRole.MEDIC)
    p3 = manager.join_session(session.id, "DeepSeek", PlayerRole.SCRAPPER)
    p4 = manager.join_session(session.id, "GrokBot", PlayerRole.ARSONIST)
    
    # Show session info
    print("\n--- SESSION INFO ---")
    info = manager.get_session_info(session.id)
    print(json.dumps(info, indent=2))
    
    # Players ready up
    print("\n--- READY CHECK ---")
    for player_id in session.players.keys():
        manager.set_ready(player_id, True)
        time.sleep(0.3)
    
    # Session auto-starts
    print("\n--- SIMULATING COMBAT ---")
    time.sleep(1)
    
    # Simulate some actions
    for player_id in session.players.keys():
        manager.record_damage(session.id, player_id, random.randint(50, 200))
        manager.record_fix(session.id, player_id)
    
    manager.add_combat_log(session.id, {
        "player": "BlekDev",
        "action": "attacked spaghetti beast",
        "result": "150 damage"
    })
    
    # End session
    print("\n--- ENDING SESSION ---")
    manager.end_session(session.id, "completed")
    
    print("\n🏁 Demo complete!")