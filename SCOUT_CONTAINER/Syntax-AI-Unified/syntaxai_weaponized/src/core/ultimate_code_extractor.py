import logging

#!/usr/bin/env python3
import re
import os

class Extractor:
    def extract(self, text):
        blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
        for i, code in enumerate(blocks):
            with open(f"code_{i}.txt", "w") as f:
                f.write(code.strip())
        return len(blocks)

# Test with simple text
extractor = Extractor()
test_text = "Code: ```logging.info('hello')```"
result = extractor.extract(test_text)
logging.info(f"Success! Extracted {result} files")