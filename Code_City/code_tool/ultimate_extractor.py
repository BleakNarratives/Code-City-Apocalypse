#!/usr/bin/env python3
import re
import os

class Extractor:
    def extract(self, text):
        blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
        for i, code in enumerate(blocks):
            with open(f"code_{i}.txt", "w") as f:
                f.write(code.strip())
        return len(blocks)

# Simple test without escape hell
extractor = Extractor()
result = extractor.extract("Test print hello code")
print(f"Works! Ready for real extraction.")

# Real test with actual code blocks
test_text = """
Here is Python code:
```python
def hello():
    print("Hello world")
```
"""
result = extractor.extract(test_text)
print(f"Extracted {result} code blocks!")
