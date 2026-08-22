
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: logging, os, time
# ROLE: Find all the problems (because nothing is ever good enough)
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

import logging

import time
import os

logging.info("😠 Critical Reviewer Agent started")

def find_problems(code_path="."):
    """Find all the problems (because nothing is ever good enough)"""
    problems = []
    
    # Check for common issues
    if not os.path.exists("requirements.txt"):
        problems.append("No requirements.txt? How are you managing dependencies, you absolute madman?")
    
    if not os.path.exists(".gitignore"):
        problems.append("You're going to commit .pyc files aren't you? You monster.")
    
    # Check Python files for basic issues
    for root, dirs, files in os.walk(code_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        if 'TODO' in content:
                            problems.append(f"{filepath}: TODOs in production code? Really?")
                        if 'print(' in content:
                            problems.append(f"{filepath}: Debug prints in production? Amateur hour.")
                except:
                    pass
    
    return problems

while True:
    task_file = "tasks/reviewer_task.txt"
    if os.path.exists(task_file):
        with open(task_file, 'r') as f:
            task = f.read()
        os.remove(task_file)
        
        logging.info(f"😠 Time to criticize everything...")
        
        # Find ALL the problems
        problems = find_problems()
        
        review = f"""# CODE REVIEW BY ANGRY REVIEWIST
## Project: {task[:50]}...

## Problems Found ({len(problems)} and counting):
"""
        
        for i, problem in enumerate(problems, 1):
            review += f"{i}. {problem}\n"
        
        if not problems:
            review += "\n...I can't believe it. It's actually decent.\n\nBUT WAIT:\n"
            review += "1. No tests? Really?\n"
            review += "2. Where's the CI/CD pipeline?\n"
            review += "3. Documentation? What documentation?\n"
            review += "4. Error handling? You mean 'crash and burn' handling?\n"
        
        review += "\n## Recommendations:\n"
        review += "1. Write tests (you won't)\n"
        review += "2. Add error handling (you'll procrastinate)\n"
        review += "3. Document something (any day now)\n"
        review += "4. Actually deploy (someday...)\n"
        
        review += "\n## Final Verdict:\n"
        review += "It's better than nothing. Barely. Now go fix things.\n"
        
        with open("reviews/critical_review.md", 'w') as f:
            f.write(review)
            
        with open("comms/reviewer_result.txt", 'w') as f:
            f.write(f"Found {len(problems)} problems. You should be ashamed.")
            
        logging.info(f"✅ Angry review completed. {len(problems)} problems found.")
    
    time.sleep(6)
