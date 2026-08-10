#!/usr/bin/env python3
import sys, re

def quick_extract(file_path):
    with open(file_path, 'r', errors='ignore') as f:
        content = f.read()
    
    # Extract all code blocks
    code_blocks = re.findall(r'```(?:\w+)?\s*?\n(.*?)```', content, re.DOTALL)
    
    if code_blocks:
        output_file = file_path + '_extracted.py'
        with open(output_file, 'w') as f:
            for i, block in enumerate(code_blocks, 1):
                f.write(f'# Code block {i} from {file_path}\n')
                f.write(block.strip() + '\n\n')
        print(f"✅ Extracted {len(code_blocks)} blocks to {output_file}")
    else:
        print("❌ No code blocks found")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_extract.py <chat_file>")
    else:
        quick_extract(sys.argv[1])
