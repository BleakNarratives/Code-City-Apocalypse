# ☣️ CodeSmellSniffer 

A lightweight, blistering fast static analysis engine designed to evaluate raw architecture logic, locate hidden anti-patterns, surface security anomalies, and map technical debt instantly. Perfect for pre-code review audits, automated QA validation pipelines, or freelance code assessments.

## 🚀 Execution & Options

Run the CLI utility passing your target file directly along with your targeted parameters:

python3 sniffer.py /path/to/target_file.py --intensity [light|medium|deep] --format [txt|json|yaml|toml|md]

### Parameters Breakdown

| Argument | Options | Description |
|---|---|---|
| path (Trailing positional) | *Any readable file path* | Location of target asset to scan |
| --intensity | light, medium, deep | Controls tolerance levels for nested blocks and method line-counts |
| --format | txt, json, yaml, toml, md | Explicit structure of output terminal print or file stream |

## 🧬 Checked Anti-Patterns
* **Silent Killers:** Catching generic catch-all except: blocks swallowing stack traces.
* **Arrow Complexity:** Locating heavily nested control loops that ruin readability.
* **Brain Functions:** Flags long methods exceeding clean structural line parameters.
* **Security Leaks:** Identifies hardcoded tokens or assignment strings storing explicit passwords.
* **Hoarder Tendencies:** Warns when dead-weight structural # TODO strings are piling up.

---
*Developed as an enterprise freelance optimization utility.*
