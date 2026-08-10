# Save this as extractor.py
import sys

text = sys.stdin.read()
in_block = False
current_block = []

for line in text.split('\n'):
    if '```' in line:
        if in_block:
            print('=== CODE BLOCK ===')
            print('\n'.join(current_block))
            current_block = []
        in_block = not in_block
    elif in_block:
        current_block.append(line)