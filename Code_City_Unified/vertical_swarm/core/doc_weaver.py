# doc_weaver.py - The 5tr8d0p3 Documentation Weaver for NotebookLM

import os

def create_5tr8d0p3(file_path):
    """Reads a Python file and generates a structured documentation file."""
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
    except Exception as e:
        return f"Error reading file: {e}"

    doc_content = []
    
    # 1. HEADER (The Head - Optimization/Outcome)
    doc_content.append(f"==================================================")
    doc_content.append(f"5TR8D0P3 DOCUMENTATION FILE")
    doc_content.append(f"SOURCE FILE: {os.path.basename(file_path)}")
    doc_content.append(f"FULL PATH: {file_path}")
    doc_content.append(f"==================================================")

    # 2. INTENT & PURPOSE (The Feet - Intent/Purpose)
    doc_content.append("\n[INTENT AND PURPOSE (THE FEET)]")
    
    # Extract file-level docstring or initial comments for intent
    for line in content:
        line = line.strip()
        if line.startswith('#'):
            doc_content.append(line.replace('# ', ''))
        elif line.startswith('"""') or line.startswith("'''"):
            break
        
    doc_content.append("\n[FUNCTIONAL BREAKDOWN]")
    
    # 3. FUNCTION/CLASS ANALYSIS (The Body)
    for i, line in enumerate(content):
        line = line.strip()
        if line.startswith('class ') or line.startswith('def '):
            for j in range(i + 1, min(i + 15, len(content))):
                sub_line = content[j].strip()
                if sub_line.startswith('"""') or sub_line.startswith("'''") or sub_line.startswith('#'):
                    doc_content.append(f"\n--- {line}")
                    while j < len(content):
                        current = content[j].strip()
                        doc_content.append(current.replace('#', '').strip())
                        j += 1
                        if current.endswith('"""') or current.endswith("'''"):
                            break
                    break
    
    # Write the output file
    output_path = file_path + ".5tr8d0p3.txt"
    try:
        with open(output_path, 'w') as out_f:
            out_f.write("\n".join(doc_content))
        return output_path
    except Exception as e:
        return f"Error writing file: {e}"

def weave_code_city_docs(base_dir):
    """Recursively finds all Python files and generates documentation for them."""
    print(f"\n🚀 Weaving 5tr8d0p3 Docs from: {base_dir}")
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py') and not file == os.path.basename(__file__):
                full_path = os.path.join(root, file)
                print(f"-> Processing {file}...")
                result_path = create_5tr8d0p3(full_path)
                print(f"  ✅ Saved to: {result_path}")
                
    print("\n✅ Documentation Weaving Complete. Upload the generated files (ending in .5tr8d0p3.txt) to NotebookLM.")

if __name__ == "__main__":
    # Start the scan from the Code City root
    weave_code_city_docs('/storage/emulated/0/root_2025/code_city')
    
