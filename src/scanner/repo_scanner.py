# File: /home/bleaknarratives/Code-City-Apocalypse/Code_City/src/scanner/repo_scanner.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: os, re, time
# ROLE: RepoScanner - scan a directory and extract per-file metrics used to build City o
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]


"""
RepoScanner - scan a directory and extract per-file metrics used to build City objects.

Output: a list of file-maps:
{
  'path': '/.../file.py',
  'language': 'Python',
  'lines': 420,
  'last_modified': 1690000000.0,
  'todos': 3,
  'placeholders': 1,
  'long_funcs': 2,
  'deep_indents': 4,
  'comments_ratio': 0.12
}
"""

import os
import time
import re

EXT_LANG = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.kts': 'Kotlin',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'C/C++',
    '.html': 'HTML',
    '.css': 'CSS',
    '.rs': 'Rust',
    '.swift': 'Swift',
    '.sh': 'Shell',
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.md': 'Markdown'
}

TODO_RX = re.compile(r'\b(TODO|FIXME|XXX|HACK)\b', re.IGNORECASE)
PLACEHOLDER_RX = re.compile(r'\b(TBD|PLACEHOLDER|IMPLEMENT_ME|pass\b|raise NotImplementedError)\b', re.IGNORECASE)
FUNC_DEF_RX = re.compile(r'^\s*(def |function |\bfunc\b|\bclass\b)', re.IGNORECASE)
INDENT_RX = re.compile(r'^(?P<indent>\s+)')

def detect_language(path):
    _, ext = os.path.splitext(path)
    return EXT_LANG.get(ext.lower(), 'Other')

def analyze_file(path):
    metrics = {
        'path': path,
        'language': detect_language(path),
        'lines': 0,
        'last_modified': os.path.getmtime(path),
        'todos': 0,
        'placeholders': 0,
        'long_funcs': 0,
        'deep_indents': 0,
        'comments': 0,
    }

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().splitlines()
    except Exception as e:
        # unreadable file: skip but record minimal info
        metrics['lines'] = 0
        return metrics

    metrics['lines'] = len(content)
    cur_func_len = 0
    in_func = False
    max_indent_depth = 0

    for ln in content:
        if ln.strip().startswith(('#', '//', '/*', '*')):  # crude comment detection
            metrics['comments'] += 1
        if TODO_RX.search(ln):
            metrics['todos'] += 1
        if PLACEHOLDER_RX.search(ln):
            metrics['placeholders'] += 1

        # detect function boundaries (coarse)
        if FUNC_DEF_RX.search(ln):
            if in_func and cur_func_len > 200:
                metrics['long_funcs'] += 1
            in_func = True
            cur_func_len = 0
        if in_func:
            cur_func_len += 1
            if cur_func_len > 1000:
                # prevent runaway counters
                cur_func_len = 1000

        m = INDENT_RX.match(ln)
        if m:
            depth = len(m.group('indent')) // 4
            if depth > max_indent_depth:
                max_indent_depth = depth

    # finalize last function
    if in_func and cur_func_len > 200:
        metrics['long_funcs'] += 1

    metrics['deep_indents'] = max_indent_depth
    metrics['comments_ratio'] = metrics['comments'] / metrics['lines'] if metrics['lines'] else 0.0
    return metrics

def scan_repo(root_path, include_exts=None):
    """
    Walk repo and return list of analyzed files.
    include_exts: optional set of lowercase extensions to include (e.g. {'.py','.js'})
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # skip common big folders
        skip_dirs = {'node_modules', '.git', '__pycache__', 'venv', 'build', 'dist'}
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fname in filenames:
            full = os.path.join(dirpath, fname)
            _, ext = os.path.splitext(fname)
            if include_exts and ext.lower() not in include_exts:
                continue
            # small safety: only scan reasonable sized text files
            try:
                if os.path.getsize(full) > 5 * 1024 * 1024:  # 5MB
                    continue
            except OSError:
                continue
            metrics = analyze_file(full)
            files.append(metrics)
    return files

if __name__ == '__main__':
    import sys, json
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    res = scan_repo(root)
    print(json.dumps(res, indent=2))
