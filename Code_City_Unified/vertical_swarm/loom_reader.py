
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: collections, datetime, json, os
# ROLE: Reads the last N lines of the Loom DB log and summarizes the Red Team's findings
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

import json
import os
from collections import Counter
from datetime import datetime

# Path relative to the project root
LOOM_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/loom_nat_db.json.log'))

def get_threat_assessment(limit=50):
    """
    Reads the last N lines of the Loom DB log and summarizes the Red Team's findings.
    Returns a string suitable for LLM context injection.
    """
    if not os.path.exists(LOOM_DB):
        return "Intelligence Briefing: No active Red Team operations detected. The system is untested."

    events = []
    try:
        with open(LOOM_DB, 'r') as f:
            # Read last N lines efficiently for large logs
            lines = f.readlines()[-limit:]
            for line in lines:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        return f"Intelligence Briefing Error: Unable to access Loom DB ({str(e)})."

    if not events:
        return "Intelligence Briefing: Red Team logs are empty."

    # Analyze the chaos
    total_events = len(events)
    actions = Counter(e.get('action', 'Unknown') for e in events)
    agents = Counter(e.get('agent_role', 'Unknown') for e in events)
    
    # Check for critical failures or successes
    survival_count = sum(1 for e in events if e.get('action') == 'RESULT' and 'survived' in e.get('details', '').lower())
    death_count = sum(1 for e in events if e.get('action') == 'RESULT' and 'died' in e.get('details', '').lower())
    recruitment_count = sum(1 for e in events if e.get('action') == 'RESULT' and 'recruited' in e.get('details', '').lower())
    
    # Construct the narrative
    briefing = [
        f"--- TOP SECRET THREAT ASSESSMENT ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---",
        f"Recent Activity: {total_events} events analyzed.",
        f"Active Agents: {', '.join([f'{k} ({v})' for k,v in agents.items()])}",
        f"Primary Vectors: {', '.join([f'{k} ({v})' for k,v in actions.items()])}",
        "",
        "CRITICAL OUTCOMES:",
        f"- Survival Rate: {survival_count} successes vs {death_count} failures.",
        f"- Recruitment/Compromise Events: {recruitment_count}",
        "",
        "RECENT LOG SNAPSHOTS:"
    ]
    
    # Add last 3 specific details for context
    for e in events[-3:]:
        briefing.append(f"- [{e.get('timestamp')}] {e.get('agent_role')}: {e.get('details')}")
        
    return "\n".join(briefing)

if __name__ == "__main__":
    print(get_threat_assessment())
