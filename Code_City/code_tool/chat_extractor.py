import os
import re
from datetime import datetime

# Create directories if they don't exist
os.makedirs("code", exist_ok=True)
os.makedirs("natural_language", exist_ok=True)
os.makedirs("tasks", exist_ok=True)

def parse_chat_log(chat_log):
    lines = chat_log.split("\n")
    code_blocks = []
    natural_language = []
    tasks = []
    current_code = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            if in_code_block:
                code_blocks.append("\n".join(current_code))
                current_code = []
            in_code_block = not in_code_block
        elif in_code_block:
            current_code.append(line)
        else:
            # Fixed regex - looks for dashes or TODO keywords
            if re.search(r"(-|\bTODO\b)", line, re.IGNORECASE):
                tasks.append(line)
            else:
                natural_language.append(line)

    return code_blocks, natural_language, tasks

def save_to_files(code_blocks, natural_language, tasks):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for i, code in enumerate(code_blocks):
        filename = f"code/code_block_{timestamp}_{i}.py"
        with open(filename, "w") as f:
            f.write(code)
        print(f"Saved code to {filename}")

    nl_filename = f"natural_language/chat_{timestamp}.txt"
    with open(nl_filename, "w") as f:
        f.write("\n".join(natural_language))
    print(f"Saved natural language to {nl_filename}")

    tasks_filename = f"tasks/tasks_{timestamp}.txt"
    with open(tasks_filename, "w") as f:
        f.write("\n".join(tasks))
    print(f"Saved tasks to {tasks_filename}")

# Test it
if __name__ == "__main__":
    test_chat = """
    Here's some natural language.
    ```python
    print("Hello, world!")
    ```
    Some more text.
    - TODO: Fix this thing
    - Another task
    """
    
    code_blocks, natural_language, tasks = parse_chat_log(test_chat)
    save_to_files(code_blocks, natural_language, tasks)
    print("Done!")