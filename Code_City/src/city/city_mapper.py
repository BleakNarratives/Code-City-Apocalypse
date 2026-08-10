# File: /storage/emulated/0/code_city/src/city/city_mapper.py

"""
CityMapper - convert scanned files into 'building' objects for visualizer and simulator.

Building schema:
{
  'id': 'relative/path',
  'language': 'Python',
  'lines': 420,
  'height': 9,           # floors
  'width': 3,            # simplistic physical footprint
  'color': '#RRGGBB',
  'flaw_type': 'spaghetti' | 'legacy' | 'ui_clunky' | 'placeholder' | 'ok',
  'flaw_score': 0.0,     # higher => worse
  'last_modified': 1680000000.0
}
"""

import os
import json
import time
from datetime import datetime, timedelta

LANG_COLORS = {
    'Python': '#3572A5',
    'JavaScript': '#F0DB4F',
    'TypeScript': '#3178C6',
    'Java': '#b07219',
    'Kotlin': '#A97BFF',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Go': '#00ADD8',
    'C': '#555555',
    'C++': '#f34b7d',
    'Rust': '#dea584',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Shell': '#89e051',
    'Other': '#888888',
    'JSON': '#D0D0D0',
    'YAML': '#C3B0A3',
    'Markdown': '#222222'
}

def color_for_lang(lang):
    return LANG_COLORS.get(lang, LANG_COLORS['Other'])

def floors_from_lines(lines):
    # each 50 lines = 1 floor (tweakable)
    return max(1, lines // 50)

def footprint_from_complexity(metrics):
    # simple proxy: more long_funcs & deeper indents => wider footprint
    base = 1
    base += min(4, metrics.get('long_funcs', 0))
    base += min(3, metrics.get('deep_indents', 0))
    return base

def compute_flaw(metrics):
    """
    Simple heuristics to assign flaw type and score:
    spaghetti -> many deep indents, long functions, low comments
    placeholder -> many placeholders or TODOs
    legacy -> last modified older than 365 days and low todos but high size
    ui_clunky -> file mentions 'ui', 'layout', 'style' and has TODOs
    runtime_error -> many TODO + placeholders + zero tests (can't detect tests here)
    """
    score = 0.0
    # ingredients
    lines = metrics['lines']
    todos = metrics.get('todos', 0)
    placeholders = metrics.get('placeholders', 0)
    long_funcs = metrics.get('long_funcs', 0)
    deep_indents = metrics.get('deep_indents', 0)
    comments_ratio = metrics.get('comments_ratio', 0.0)
    age_days = (time.time() - metrics['last_modified']) / (60*60*24)

    # base score from mass
    score += min(1.0, lines / 1000.0) * 0.4
    score += min(1.0, long_funcs / 10.0) * 0.2
    score += min(1.0, deep_indents / 6.0) * 0.2
    score += min(1.0, todos / 10.0) * 0.2

    # placeholders bump
    score += min(1.0, placeholders / 5.0) * 0.4

    # adjust for comments (less comments -> worse score)
    score *= (1.0 + max(0.0, 0.5 - comments_ratio))

    # decide main flaw
    flaw = 'ok'
    if placeholders >= 2:
        flaw = 'placeholder'
    elif (deep_indents >= 3 or long_funcs >= 2) and comments_ratio < 0.15:
        flaw = 'spaghetti'
    elif 'ui' in os.path.basename(metrics['path']).lower() or 'layout' in metrics['path'].lower():
        if todos > 0:
            flaw = 'ui_clunky'
    elif age_days > 365 and lines > 200:
        flaw = 'legacy'
    elif todos > 5 and placeholders > 1:
        flaw = 'runtime_error'

    # clamp score
    flaw_score = max(0.0, min(1.0, score))
    return flaw, flaw_score

def map_file_to_building(metrics, repo_root):
    rel = os.path.relpath(metrics['path'], repo_root)
    language = metrics.get('language', 'Other')
    lines = metrics.get('lines', 0)
    floors = floors_from_lines(lines)
    footprint = footprint_from_complexity(metrics)
    color = color_for_lang(language)
    flaw, score = compute_flaw(metrics)
    building = {
        'id': rel,
        'path': metrics['path'],
        'language': language,
        'lines': lines,
        'height': floors,
        'width': footprint,
        'color': color,
        'flaw_type': flaw,
        'flaw_score': score,
        'last_modified': metrics.get('last_modified'),
    }
    return building

def build_city(file_metrics_list, repo_root):
    city = {
        'generated_at': time.time(),
        'repo_root': os.path.abspath(repo_root),
        'buildings': []
    }
    for m in file_metrics_list:
        b = map_file_to_building(m, repo_root)
        city['buildings'].append(b)
    # sort by height desc for panoramas
    city['buildings'].sort(key=lambda x: x['height'], reverse=True)
    return city

def save_city(city, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(city, f, indent=2)

if __name__ == '__main__':
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    import scanner.repo_scanner as rs
    files = rs.scan_repo(root)
    city = build_city(files, root)
    print(f"Mapped {len(city['buildings'])} buildings from {root}")
    print(json.dumps(city['buildings'][:10], indent=2))