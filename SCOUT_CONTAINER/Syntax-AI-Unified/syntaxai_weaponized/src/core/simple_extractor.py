import logging

import re
from pathlib import Path
from datetime import datetime

class SimpleExtractor:
    def extract_from_text(self, text):
        logging.info('Extracting code...')
        project_name = f'project_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        project_path = Path('exports/extracted_projects') / project_name
        project_path.mkdir(parents=True, exist_ok=True)
        for i, code in enumerate(blocks):
            with open(project_path / f'code_{i}.py', 'w') as f:
                f.write(code.strip())
        logging.info(f'Saved {len(blocks)} files to {project_path}')
        return project_path
