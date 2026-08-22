# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/blue_sky_obelisk.py
# Path: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/buildings/blue_sky_obelisk.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-buildings
# DEPS: dataclasses, enum, json, time, typing
# ROLE: Blue Sky Obelisk - The Strategy Hub
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]


"""
Blue Sky Obelisk - The Strategy Hub
A mystical planning space where teams pause combat to strategize, review data,
and make critical decisions about refactoring approaches.
"""

import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json

# ==================== MEETING TYPES ====================

class MeetingType(Enum):
    EMERGENCY_HUDDLE = "emergency_huddle"      # Quick tactical discussion
    STRATEGY_SESSION = "strategy_session"       # Deep planning
    RETROSPECTIVE = "retrospective"             # Post-raid review
    DESIGN_REVIEW = "design_review"            # Architecture planning
    STANDOFF = "standoff"                      # Temporary ceasefire to regroup

# ==================== DATA STRUCTURES ====================

@dataclass
class StrategyDecision:
    """A decision made during strategy sessions."""
    id: str
    decision_text: str
    proposed_by: str
    timestamp: float
    votes_for: Set[str] = field(default_factory=set)
    votes_against: Set[str] = field(default_factory=set)
    status: str = "pending"  # pending, approved, rejected, implemented


@dataclass
class ActionItem:
    """Tasks assigned during meetings."""
    id: str
    description: str
    assigned_to: str
    priority: int  # 1-5, 5 being critical
    created_at: float
    completed: bool = False
    target_building: Optional[str] = None


@dataclass
class InsightCard:
    """Data visualization cards displayed in the Obelisk."""
    id: str
    title: str
    card_type: str  # metric, chart, alert, recommendation
    data: Dict
    timestamp: float


@dataclass
class ObeliskMeeting:
    """A strategy meeting instance."""
    id: str
    meeting_type: MeetingType
    session_id: str
    participants: List[str]
    host_id: str
    
    started_at: float
    ended_at: Optional[float] = None
    
    # Meeting content
    agenda: List[str] = field(default_factory=list)
    decisions: List[StrategyDecision] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    
    # Data presented
    insight_cards: List[InsightCard] = field(default_factory=list)


# ==================== BLUE SKY OBELISK ====================

class BlueSkyObelisk:
    """
    The central strategy hub where teams pause to think.
    Provides data visualization, voting systems, and collaborative planning.
    """
    
    def __init__(self):
        self.active_meetings: Dict[str, ObeliskMeeting] = {}
        self.meeting_history: List[ObeliskMeeting] = []
        self.global_decisions: List[StrategyDecision] = []
        self.pending_actions: List[ActionItem] = []
        
        self.meeting_count = 0
        self.decision_count = 0
        self.action_count = 0
    
    # ==================== MEETING MANAGEMENT ====================
    
    def start_meeting(
        self,
        session_id: str,
        host_id: str,
        participants: List[str],
        meeting_type: MeetingType,
        agenda: Optional[List[str]] = None
    ) -> ObeliskMeeting:
        """Initiate a strategy meeting."""
        self.meeting_count += 1
        meeting_id = f"meeting_{self.meeting_count:04d}"
        
        meeting = ObeliskMeeting(
            id=meeting_id,
            meeting_type=meeting_type,
            session_id=session_id,
            participants=participants,
            host_id=host_id,
            started_at=time.time(),
            agenda=agenda or []
        )
        
        self.active_meetings[meeting_id] = meeting
        
        print(f"\n🏛️ BLUE SKY MEETING INITIATED")
        print(f"📋 Type: {meeting_type.value}")
        print(f"👥 Participants: {', '.join(participants)}")
        print(f"⏱️ Time: Paused (Meeting in Progress)")
        
        if agenda:
            print(f"\n📌 AGENDA:")
            for i, item in enumerate(agenda, 1):
                print(f"  {i}. {item}")
        
        return meeting
    
    def end_meeting(self, meeting_id: str) -> bool:
        """Conclude meeting and implement decisions."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return False
        
        meeting.ended_at = time.time()
        duration = meeting.ended_at - meeting.started_at
        
        # Move to history
        self.meeting_history.append(meeting)
        del self.active_meetings[meeting_id]
        
        # Summarize
        self._print_meeting_summary(meeting, duration)
        
        print(f"\n⏱️ Combat Resumed")
        
        return True
    
    # ==================== DECISION MAKING ====================
    
    def propose_decision(
        self,
        meeting_id: str,
        proposer_id: str,
        decision_text: str
    ) -> Optional[StrategyDecision]:
        """Propose a strategic decision for vote."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return None
        
        self.decision_count += 1
        decision_id = f"decision_{self.decision_count:04d}"
        
        decision = StrategyDecision(
            id=decision_id,
            decision_text=decision_text,
            proposed_by=proposer_id,
            timestamp=time.time()
        )
        
        meeting.decisions.append(decision)
        
        print(f"\n📢 PROPOSAL: {decision_text}")
        print(f"   Proposed by: {proposer_id}")
        print(f"   Vote with /vote {decision_id} [for|against]")
        
        return decision
    
    def vote_on_decision(
        self,
        meeting_id: str,
        decision_id: str,
        voter_id: str,
        vote: bool  # True = for, False = against
    ) -> bool:
        """Cast vote on a decision."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return False
        
        # Find decision
        decision = None
        for d in meeting.decisions:
            if d.id == decision_id:
                decision = d
                break
        
        if not decision:
            return False
        
        # Remove from opposite set if exists
        if vote:
            decision.votes_for.add(voter_id)
            decision.votes_against.discard(voter_id)
        else:
            decision.votes_against.add(voter_id)
            decision.votes_for.discard(voter_id)
        
        # Check if decision reached majority
        total_participants = len(meeting.participants)
        majority = (total_participants // 2) + 1
        
        if len(decision.votes_for) >= majority:
            decision.status = "approved"
            print(f"✅ DECISION APPROVED: {decision.decision_text}")
            self.global_decisions.append(decision)
        elif len(decision.votes_against) >= majority:
            decision.status = "rejected"
            print(f"❌ DECISION REJECTED: {decision.decision_text}")
        
        return True
    
    # ==================== ACTION ITEMS ====================
    
    def create_action_item(
        self,
        meeting_id: str,
        description: str,
        assigned_to: str,
        priority: int = 3,
        target_building: Optional[str] = None
    ) -> Optional[ActionItem]:
        """Create a task from meeting discussion."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return None
        
        self.action_count += 1
        action_id = f"action_{self.action_count:04d}"
        
        action = ActionItem(
            id=action_id,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            created_at=time.time(),
            target_building=target_building
        )
        
        meeting.action_items.append(action)
        self.pending_actions.append(action)
        
        priority_emoji = "🔥" if priority >= 4 else "⚠️" if priority == 3 else "📝"
        print(f"{priority_emoji} ACTION ITEM: {description}")
        print(f"   Assigned to: {assigned_to}")
        if target_building:
            print(f"   Target: {target_building}")
        
        return action
    
    def complete_action_item(self, action_id: str) -> bool:
        """Mark action as completed."""
        for action in self.pending_actions:
            if action.id == action_id:
                action.completed = True
                self.pending_actions.remove(action)
                
                print(f"✅ Action Completed: {action.description}")
                return True
        
        return False
    
    # ==================== DATA VISUALIZATION ====================
    
    def add_insight_card(
        self,
        meeting_id: str,
        title: str,
        card_type: str,
        data: Dict
    ) -> Optional[InsightCard]:
        """Display data visualization during meeting."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return None
        
        card = InsightCard(
            id=f"card_{len(meeting.insight_cards) + 1}",
            title=title,
            card_type=card_type,
            data=data,
            timestamp=time.time()
        )
        
        meeting.insight_cards.append(card)
        
        self._display_insight_card(card)
        
        return card
    
    def _display_insight_card(self, card: InsightCard):
        """Render insight card to console."""
        print(f"\n📊 INSIGHT: {card.title}")
        print("─" * 60)
        
        if card.card_type == "metric":
            for key, value in card.data.items():
                print(f"  {key}: {value}")
        
        elif card.card_type == "alert":
            severity = card.data.get("severity", "info")
            message = card.data.get("message", "")
            emoji = "🚨" if severity == "critical" else "⚠️" if severity == "warning" else "ℹ️"
            print(f"  {emoji} {message}")
        
        elif card.card_type == "recommendation":
            print(f"  💡 {card.data.get('suggestion', '')}")
            if "reasoning" in card.data:
                print(f"     Reasoning: {card.data['reasoning']}")
        
        elif card.card_type == "chart":
            # ASCII bar chart
            items = card.data.get("items", [])
            max_val = max((item["value"] for item in items), default=1)
            
            for item in items:
                bar_length = int((item["value"] / max_val) * 40)
                bar = "█" * bar_length
                print(f"  {item['label']:20s} {bar} {item['value']}")
    
    # ==================== SPECIALIZED MEETINGS ====================
    
    def emergency_huddle(
        self,
        session_id: str,
        host_id: str,
        participants: List[str],
        crisis: str
    ) -> ObeliskMeeting:
        """Quick tactical meeting during critical moments."""
        meeting = self.start_meeting(
            session_id=session_id,
            host_id=host_id,
            participants=participants,
            meeting_type=MeetingType.EMERGENCY_HUDDLE,
            agenda=[
                f"Address Crisis: {crisis}",
                "Immediate tactical response",
                "Resource allocation"
            ]
        )
        
        # Auto-generate crisis insight
        self.add_insight_card(
            meeting.id,
            "CRISIS ALERT",
            "alert",
            {
                "severity": "critical",
                "message": crisis,
                "time_to_act": "NOW"
            }
        )
        
        return meeting
    
    def retrospective(
        self,
        session_id: str,
        host_id: str,
        participants: List[str],
        raid_stats: Dict
    ) -> ObeliskMeeting:
        """Post-raid review meeting."""
        meeting = self.start_meeting(
            session_id=session_id,
            host_id=host_id,
            participants=participants,
            meeting_type=MeetingType.RETROSPECTIVE,
            agenda=[
                "What went well?",
                "What could be improved?",
                "Action items for next raid"
            ]
        )
        
        # Display raid statistics
        self.add_insight_card(
            meeting.id,
            "Raid Performance",
            "metric",
            raid_stats
        )
        
        # Generate recommendations
        if raid_stats.get("deaths", 0) > 5:
            self.add_insight_card(
                meeting.id,
                "Recommendation",
                "recommendation",
                {
                    "suggestion": "Consider bringing a Medic next time",
                    "reasoning": "High death count indicates need for support"
                }
            )
        
        return meeting
    
    def design_review(
        self,
        session_id: str,
        host_id: str,
        participants: List[str],
        architecture_proposal: Dict
    ) -> ObeliskMeeting:
        """Review architectural changes."""
        meeting = self.start_meeting(
            session_id=session_id,
            host_id=host_id,
            participants=participants,
            meeting_type=MeetingType.DESIGN_REVIEW,
            agenda=[
                "Review proposed architecture",
                "Discuss trade-offs",
                "Vote on implementation approach"
            ]
        )
        
        # Display architecture proposal
        self.add_insight_card(
            meeting.id,
            "Architecture Proposal",
            "metric",
            architecture_proposal
        )
        
        return meeting
    
    # ==================== NOTES & LOGGING ====================
    
    def add_note(self, meeting_id: str, note: str, author: str) -> bool:
        """Add note to meeting log."""
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            return False
        
        timestamped_note = f"[{time.strftime('%H:%M:%S')}] {author}: {note}"
        meeting.notes.append(timestamped_note)
        
        return True
    
    # ==================== SUMMARY & EXPORT ====================
    
    def _print_meeting_summary(self, meeting: ObeliskMeeting, duration: float):
        """Print meeting summary."""
        print("\n" + "="*60)
        print("📋 MEETING SUMMARY")
        print("="*60)
        
        print(f"\nType: {meeting.meeting_type.value}")
        print(f"Duration: {duration:.0f} seconds")
        print(f"Participants: {len(meeting.participants)}")
        
        if meeting.decisions:
            print(f"\n📊 DECISIONS MADE: {len(meeting.decisions)}")
            for decision in meeting.decisions:
                status_emoji = "✅" if decision.status == "approved" else "❌" if decision.status == "rejected" else "⏳"
                print(f"  {status_emoji} {decision.decision_text}")
        
        if meeting.action_items:
            print(f"\n📝 ACTION ITEMS: {len(meeting.action_items)}")
            for action in meeting.action_items:
                priority_emoji = "🔥" if action.priority >= 4 else "⚠️" if action.priority == 3 else "📝"
                print(f"  {priority_emoji} {action.description} → {action.assigned_to}")
        
        if meeting.notes:
            print(f"\n💬 NOTES: {len(meeting.notes)} entries")
    
    def export_meeting_notes(self, meeting_id: str, filepath: str) -> bool:
        """Export meeting to JSON file."""
        # Check both active and history
        meeting = self.active_meetings.get(meeting_id)
        if not meeting:
            for m in self.meeting_history:
                if m.id == meeting_id:
                    meeting = m
                    break
        
        if not meeting:
            return False
        
        export_data = {
            "meeting_id": meeting.id,
            "type": meeting.meeting_type.value,
            "session_id": meeting.session_id,
            "participants": meeting.participants,
            "started_at": time.ctime(meeting.started_at),
            "ended_at": time.ctime(meeting.ended_at) if meeting.ended_at else None,
            "agenda": meeting.agenda,
            "decisions": [
                {
                    "text": d.decision_text,
                    "proposed_by": d.proposed_by,
                    "status": d.status,
                    "votes_for": len(d.votes_for),
                    "votes_against": len(d.votes_against)
                }
                for d in meeting.decisions
            ],
            "action_items": [
                {
                    "description": a.description,
                    "assigned_to": a.assigned_to,
                    "priority": a.priority,
                    "completed": a.completed
                }
                for a in meeting.action_items
            ],
            "notes": meeting.notes
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📄 Meeting notes exported to {filepath}")
        
        return True
    
    # ==================== QUERIES ====================
    
    def get_pending_actions_for_player(self, player_id: str) -> List[ActionItem]:
        """Get all pending tasks assigned to player."""
        return [a for a in self.pending_actions if a.assigned_to == player_id]
    
    def get_recent_decisions(self, count: int = 10) -> List[StrategyDecision]:
        """Get most recent approved decisions."""
        approved = [d for d in self.global_decisions if d.status == "approved"]
        return sorted(approved, key=lambda x: x.timestamp, reverse=True)[:count]


# ==================== DEMO ====================

if __name__ == "__main__":
    print("🏛️ BLUE SKY OBELISK DEMO")
    print("="*60)
    
    obelisk = BlueSkyObelisk()
    
    # Emergency huddle
    print("\n--- SCENARIO: Boss at 25% HP, Team Struggling ---")
    meeting = obelisk.emergency_huddle(
        session_id="raid_001",
        host_id="bleak_001",
        participants=["bleak_001", "claude_001", "grok_001"],
        crisis="Mayor Strump entered Phase 3, spawning chaos monsters rapidly"
    )
    
    time.sleep(1)
    
    # Propose decision
    print("\n--- STRATEGY DISCUSSION ---")
    decision = obelisk.propose_decision(
        meeting.id,
        "claude_001",
        "Focus all DPS on spaghetti zones to reduce monster spawns"
    )
    
    # Vote
    obelisk.vote_on_decision(meeting.id, decision.id, "bleak_001", True)
    obelisk.vote_on_decision(meeting.id, decision.id, "claude_001", True)
    obelisk.vote_on_decision(meeting.id, decision.id, "grok_001", True)
    
    # Create action items
    obelisk.create_action_item(
        meeting.id,
        "Refactor main.py spaghetti loops immediately",
        "bleak_001",
        priority=5,
        target_building="main.py"
    )
    
    obelisk.create_action_item(
        meeting.id,
        "Deploy medic to heal UI clunky buildings",
        "grok_001",
        priority=4
    )
    
    # Add notes
    obelisk.add_note(meeting.id, "Remember to save progress before next phase", "claude_001")
    
    # End meeting
    time.sleep(1)
    print("\n--- ENDING MEETING ---")
    obelisk.end_meeting(meeting.id)
    
    # Show pending actions
    print("\n--- PENDING ACTIONS ---")
    for action in obelisk.pending_actions:
        print(f"  {action.description} → {action.assigned_to}")
    
    print("\n🏁 Demo complete!")