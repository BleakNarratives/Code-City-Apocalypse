Demo runner
Usage:
  termux $ python3 /storage/emulated/0/code_city/demo_city.py /path/to/your/repo

Outputs:
  - /storage/emulated/0/code_city/data/city.json
  - an ASCII 'panorama' printed to stdout (sorted by height)
"""

import os
import sys
import time
import json

REPO_ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT_JSON = '/storage/emulated/0/code_city/data/city.json'

# ensure local imports work when executed from top-level
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from scanner.repo_scanner import scan_repo
    from city.city_mapper import build_city, save_city
except Exception:
    # if launched from /storage..., assume structure is /storage/.../src present
    sys.path.insert(0, os.path.join('/storage/emulated/0/code_city', 'src'))
    from scanner.repo_scanner import scan_repo
    from city.city_mapper import build_city, save_city

def ascii_panorama(city):
    """
    Simple ASCII panorama: each building occupies a column whose height is 'height'.
    We show top N buildings with simple blocks scaled for terminal.
    """
    top = city['buildings'][:40]
    max_h = max((b['height'] for b in top), default=1)
    # scale heights to a terminal-friendly size
    rows = min(20, max_h)
    scale = max_h / rows if max_h > rows else 1.0

    # create grid
    grid = [[' ' for _ in top] for _ in range(rows)]
    for col, b in enumerate(top):
        ch = '#' if b['flaw_type'] != 'ok' else '|'
        h = int(b['height'] / max(1, scale))
        for r in range(rows - 1, rows - 1 - h, -1):
            if r >= 0:
                grid[r][col] = ch

    # render
    print("\nASCII PANORAMA (top files by height; '#' = flawed building, '|' = OK):\n")
    for r in grid:
        print(''.join(c + ' ' for c in r))
    # footer with file labels truncated
    print("\nLEGEND (file : height : flaw_type)")
    for b in top:
        label = b['id'][:40].ljust(40)
        print(f"{label}  | {b['height']:3d} floors | {b['flaw_type']} (score {b['flaw_score']:.2f})")

def main():
    repo = REPO_ROOT
    print(f"[{time.ctime()}] Scanning repo: {repo} ...")
    files = scan_repo(repo)
    print(f"Found {len(files)} source files, mapping to city...")
    city = build_city(files, repo)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    save_city(city, OUT_JSON)
    print(f"Saved city JSON -> {OUT_JSON}")
    ascii_panorama(city)

if __name__ == '__main__':
    main()
