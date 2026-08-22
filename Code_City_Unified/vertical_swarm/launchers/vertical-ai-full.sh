#!/bin/bash

SWARM_DIR="$HOME/.ai_swarm"
mkdir -p "$SWARM_DIR"

clear
echo "Vertical AI Swarm | Session: $(date +%Y-%m-%d)"
echo "Status: $([ -f /proc/%d/oom_score_adj ] && echo "🟢 ACTIVE" || echo "🟡 LOW RAM") | RAM: $(free -h|head -2|tail -1|awk '{print $3"/"$2}')"
echo

echo "[1] Orchestrator (qwen2.5): Spawn threat + rap subagents. Status: READY"
echo "[2] Threat Modeler (deepseek): RAM risk HIGH on Android. Mitigation: swap required"
echo "[3] Rap Genius (llama3.2): 'Yo orchestrate the swarm, don't crash the phone—APPROVE'"
echo

echo "Votes: 2-1 APPROVE > launch real agents? y/n/q(uit)"
echo -n "> "
read choice

case $choice in
  y|Y)
    echo "🚀 Vertical AI Swarm ACTIVATING..."
    
    # Real Ollama agent swarm (your exact models)
    ollama run qwen2.5-coder:1.5b "Vertical AI boardroom: orchestrate threat modeler + rap genius subagents. Output execution plan." > "$SWARM_DIR/orchestrator.out" &
    ORCH_PID=$!
    
    ollama run deepseek-coder:latest "Threat modeling for Vertical AI swarm on Android Termux: RAM limits, process crashes, Android OOM killer risks. Mitigation plan." > "$SWARM_DIR/threat.out" &
    THREAT_PID=$!
    
    ollama run llama3.2:1b "Rap genius approves Vertical AI swarm launch: drop Eminem-style bars about AI agents collaborating without crashing mobile device." > "$SWARM_DIR/rap.out" &
    RAP_PID=$!
    
    # Live status
    echo "Agents spawning... PIDs: orch=$ORCH_PID threat=$THREAT_PID rap=$RAP_PID"
    
    # Wait for all agents
    wait $ORCH_PID $THREAT_PID $RAP_PID
    echo "✅ Swarm complete! Outputs:"
    ls -la "$SWARM_DIR"/*.out
    echo "View: cat ~/.ai_swarm/*.out"
    ;;
  n|N)
    echo "Swarm aborted. Edit agents above and rerun."
    ;;
  q|Q)
    echo "Vertical AI session ended."
    exit 0
    ;;
  *)
    echo "Invalid: y/n/q"
    ./vertical-ai-full.sh
    ;;
esac

echo
echo "Run 'cat ~/.ai_swarm/*.out' to read agent reports."
echo "Rerun: ./vertical-ai-full.sh"
