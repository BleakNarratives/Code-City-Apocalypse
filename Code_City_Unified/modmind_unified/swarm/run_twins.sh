#!/usr/bin/env bash

cd ~/storage/shared/ai_swarm_project

echo "🧬 Starting Eden..."
python agent_eden.py &
eden_pid=$!

sleep 2

echo "⚡ Starting Jude..."
python agent_jude.py &
jude_pid=$!

sleep 2

echo "✅ Twins running! PIDs: $eden_pid, $jude_pid"
echo "Send tasks: echo 'Build something' > tasks/eden_task.txt"
echo "Press Enter to stop..."
read

kill $eden_pid $jude_pid 2>/dev/null
echo "Twins stopped"
