#!/bin/bash

cd ~/storage/shared/ai_swarm_project

echo "🧬⚡ LAUNCHING TWINS..."
echo ""

# Create all directories
mkdir -p eden/{blueprints,workbenches,orchestrations}
mkdir -p jude/{builds,executions,outputs}
mkdir -p dashboard desires

echo "1. Starting Eden (Architect)..."
termux-wake-lock
python agent_eden.py &
EDEN_PID=$!
echo "Eden PID: $EDEN_PID" > pids.txt

sleep 3

echo ""
echo "2. Starting Jude (Builder)..."
python agent_jude.py &
JUDE_PID=$!
echo "Jude PID: $JUDE_PID" >> pids.txt

sleep 3

echo ""
echo "3. Starting CLI Dashboard..."
python -c "
import time
import os
from datetime import datetime

while True:
    os.system('clear')
    print('🧠 SWARM DASHBOARD')
    print('='*40)
    print(f'Time: {datetime.now().strftime(\"%H:%M:%S\")}')
    print('')
    
    # Check agents
    agents = ['eden', 'jude', 'psychology', 'legal', 'security', 'tech_guru', 'marketing', 'reviewer', 'coder']
    print('AGENT STATUS:')
    for agent in agents:
        if os.path.exists(f'comms/{agent}_result.txt'):
            mtime = os.path.getmtime(f'comms/{agent}_result.txt')
            age = time.time() - mtime
            if age < 60:
                print(f'  {agent}: ✅ ACTIVE')
            else:
                print(f'  {agent}: ⚠️  IDLE')
        else:
            print(f'  {agent}: ❌ OFFLINE')
    
    print('')
    print('QUICK ACTIONS:')
    print('  1. Send task to Eden')
    print('  2. Check Jude builds')
    print('  3. View blueprints')
    print('  4. Exit')
    print('')
    
    try:
        choice = input('Choose [1-4]: ')
        if choice == '1':
            task = input('Task for Eden: ')
            with open('tasks/eden_task.txt', 'w') as f:
                f.write(task)
            print('Task sent to Eden!')
            time.sleep(2)
        elif choice == '2':
            if os.path.exists('jude/builds'):
                builds = os.listdir('jude/builds')
                print(f'Jude has {len(builds)} builds ready')
                for build in builds[:3]:
                    print(f'  • {build}')
            else:
                print('No builds yet')
            input('Press Enter...')
        elif choice == '3':
            if os.path.exists('eden/blueprints'):
                blueprints = os.listdir('eden/blueprints')
                print(f'Eden created {len(blueprints)} blueprints')
                for bp in blueprints[:3]:
                    print(f'  • {bp}')
            else:
                print('No blueprints yet')
            input('Press Enter...')
        elif choice == '4':
            print('Stopping...')
            with open('pids.txt', 'r') as f:
                for line in f:
                    pid = line.split()[-1]
                    os.system(f'kill {pid} 2>/dev/null')
            termux-wake-unlock
            exit()
    except KeyboardInterrupt:
        print('Stopping...')
        with open('pids.txt', 'r') as f:
            for line in f:
                pid = line.split()[-1]
                os.system(f'kill {pid} 2>/dev/null')
        termux-wake-unlock
        exit()
    
    time.sleep(5)
" &
DASH_PID=$!
echo "Dashboard PID: $DASH_PID" >> pids.txt

echo ""
echo "✅ TWINS LAUNCHED!"
echo ""
echo "Send task to Eden:"
echo "  echo 'Build AI SaaS' > tasks/eden_task.txt"
echo ""
echo "Check results in: comms/eden_result.txt"
echo ""
echo "Press Ctrl+C in this terminal to stop everything"
echo ""

# Keep script running
wait
