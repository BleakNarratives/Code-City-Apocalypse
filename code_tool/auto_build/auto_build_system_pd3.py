# In Pydroid3 terminal, you're in SHELL, not Python!
# Run Python explicitly:

python3 -c "
import os
base_dir = '/storage/emulated/0/Documents/auto_build_system'
os.makedirs(base_dir, exist_ok=True)

phase1_code = '''import time
import os
import subprocess
from datetime import datetime

def get_clipboard():
    try:
        result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ''

def save_to_file(content, filename):
    os.makedirs('/storage/emulated/0/Documents/auto_capture', exist_ok=True)
    filepath = f'/storage/emulated/0/Documents/auto_capture/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def main():
    print(\\\"🚗 RIDER STARTED\\\")
    last_content = \\\"\\\"
    while True:
        current_clip = get_clipboard()
        if current_clip and current_clip != last_content:
            print(\\\"📝 CAPTURED!\\\")
            last_content = current_clip
        time.sleep(5)

if __name__ == \\\"__main__\\\":
    main()
'''

with open(f'{base_dir}/conversation_rider.py', 'w') as f:
    f.write(phase1_code)

print(f'✅ SAVED: {base_dir}/conversation_rider.py')
"