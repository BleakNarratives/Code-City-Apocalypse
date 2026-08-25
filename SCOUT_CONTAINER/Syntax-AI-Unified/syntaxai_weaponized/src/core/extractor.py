# FILE: extractor.py
import re
import json
import datetime

def extract_code_and_vibe(conversation_text, file_name, file_path):
    """Extracts code blocks and the remaining natural language ('vibe') from conversation text."""
    
    header_comment = f"# FILE: {file_name}\n# FULL PATH: {file_path}\n\n"
    code_block_pattern = re.compile(r'```(?P<lang>\w+)?\s*(?P<code>.*?)\s*```', re.DOTALL)
    
    extracted_data = {
        "metadata": {
            "source_file_name": file_name,
            "source_file_path": file_path,
            "captured_timestamp": datetime.datetime.now().isoformat()
        },
        "code_blocks": {},
        "vibe_flow": conversation_text
    }
    
    code_blocks = {}
    vibe_with_placeholders = conversation_text
    
    for i, match in enumerate(code_block_pattern.finditer(conversation_text)):
        lang = match.group('lang') or 'text'
        code = match.group('code').strip()
        
        code_content = header_comment + code
        block_id = f"CODE_BLOCK_{i}"
        code_blocks[block_id] = {"language": lang.lower(), "content": code_content}
        
        vibe_with_placeholders = vibe_with_placeholders.replace(match.group(0), f"[{block_id} EXTRACTED {lang.upper()}]")

    vibe_flow = re.sub(r'\n\s*\n', '\n\n', vibe_with_placeholders).strip()
    
    extracted_data["code_blocks"] = code_blocks
    extracted_data["vibe_flow"] = vibe_flow
    
    return extracted_data
