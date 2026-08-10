from pathlib import Path, PurePath
import json, hashlib, html

datafile = Path("Codeshitty.txt")
lines = [l.strip() for l in datafile.read_text().splitlines() if l.strip()]
entries = []
for i, l in enumerate(lines):
    name = l.split("|")[0].strip()
    h = int(hashlib.sha1(name.encode()).hexdigest()[:8], 16)
    entries.append({
        "id": f"b{i}",
        "name": name,
        "size": 100 + (h % 5000),
        "lines": 1 + (h % 400)
    })

html_city = json.dumps(entries)
template = Path("code_city_template.html").read_text()
Path("code_city_final.html").write_text(template.replace("%%CITY%%", html_city))
print("✅ Built code_city_final.html successfully!")