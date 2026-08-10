import logging

import re
import os

def scan_for_hardcoded_secrets(file_path):
    """
    Scans a file for patterns that look like hardcoded secrets.
    """
    secret_patterns = [
        re.compile(r'["\'](api_key|password|secret|token)["\']\s*[:=]\s*["\']\w+["\']', re.IGNORECASE),
        re.compile(r'(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)\s*=\s*["\'].+["\']', re.IGNORECASE)
    ]
    
    issues = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            for pattern in secret_patterns:
                if pattern.search(line):
                    issues.append(f"Potential hardcoded secret found in {file_path} at line {line_num}: {line.strip()}")
    return issues

def scan_for_insecure_functions(file_path):
    """
    Scans a Python file for use of insecure functions like eval(), exec(), and pickle.
    """
    insecure_functions = ['eval', 'exec', 'pickle.load', 'pickle.loads']
    issues = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        for func in insecure_functions:
            if func in content:
                issues.append(f"Use of insecure function '{func}' found in {file_path}.")
    return issues

def scan_for_insecure_subprocess(file_path):
    """
    Scans a Python file for insecure use of subprocess with shell=True.
    """
    insecure_subprocess_pattern = re.compile(r'subprocess\.\w+\(.*shell=True.*\)', re.IGNORECASE)
    issues = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            if insecure_subprocess_pattern.search(line):
                issues.append(f"Potential insecure subprocess call with shell=True in {file_path} at line {line_num}: {line.strip()}")
    return issues

def run_security_scan(target_file):
    """
    Runs all security scans on a single file.
    """
    logging.info(f"--- Running security scan on {target_file} ---")
    all_issues = []
    
    if not os.path.exists(target_file):
        logging.info(f"Error: File not found at {target_file}")
        return

    all_issues.extend(scan_for_hardcoded_secrets(target_file))
    all_issues.extend(scan_for_insecure_functions(target_file))
    all_issues.extend(scan_for_insecure_subprocess(target_file))
    
    if all_issues:
        logging.info("Security issues found:")
        for issue in all_issues:
            logging.info(f"- {issue}")
    else:
        logging.info("No security issues found.")
    logging.info("--- Scan complete ---")


if __name__ == '__main__':
    # As an example, we'll make Agent 1 scan one of its own kind: agent5.
    # This is a good test case as agent5 is about implementation.
    test_file = 'agent5_implementation_framework.py'
    run_security_scan(test_file)

    # We can also create a dummy file with issues to test the scanner
    dummy_file_content = """
import subprocess
import pickle

password = "my_super_secret_password_123"

def vulnerable_function(data):
    # This is dangerous!
    eval(data)
    subprocess.run("echo 'hello'", shell=True)

class MyObject:
    pass

def deserialize_data(data):
    return pickle.loads(data)
"""
    dummy_file_path = 'vulnerable_test_file.py'
    with open(dummy_file_path, 'w') as f:
        f.write(dummy_file_content)
    
    run_security_scan(dummy_file_path)
    os.remove(dummy_file_path)

