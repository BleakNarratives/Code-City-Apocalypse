import json
import os
from datetime import datetime

# Path relative to the project root
STATE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/vertical_ai/state.json'))

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"decisions": [], "memories": [], "last_updated": None}
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"decisions": [], "memories": [], "last_updated": None}

def save_state(state):
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def add_decision(topic, decision_summary):
    state = load_state()
    state["decisions"].append({
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "summary": decision_summary
    })
    # Keep only last 10 for context window efficiency
    state["decisions"] = state["decisions"][-10:]
    save_state(state)

def get_recent_history():
    state = load_state()
    if not state["decisions"]:
        return "No previous boardroom history."
    
    history = ["--- PREVIOUS BOARDROOM DECISIONS ---"]
    for d in state["decisions"]:
        # Fix: ensure no literal newlines in the f-string in the source
        history.append(f"- [{d['timestamp'][:10]}] Topic: {d['topic']}\n  Result: {d['summary']}")
    return "\n".join(history)

if __name__ == "__main__":
    print(get_recent_history())
