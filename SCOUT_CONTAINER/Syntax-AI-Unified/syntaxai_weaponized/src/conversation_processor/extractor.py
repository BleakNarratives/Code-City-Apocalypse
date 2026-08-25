# Save this as ~/syntaxai-weaponized/src/conversation_processor/extractor.py
import re
import json
from datetime import datetime
from pathlib import Path

class ConversationExtractor:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        
    def extract_components(self, raw_text):
        """Extract vibe/flow and code blocks from conversation"""
        # Clean vibe text
        vibe_text = re.sub(r'```.*?```', '', raw_text, flags=re.DOTALL)
        vibe_text = re.sub(r'`[^`]*`', '', vibe_text)
        vibe_text = re.sub(r'u0_a491@localhost.*?[\\$#]', '', vibe_text)
        vibe_text = re.sub(r'heredoc>.*', '', vibe_text)
        vibe_text = re.sub(r'\n\s*\n', '\n\n', vibe_text).strip()
        
        # Extract code blocks by language
        code_blocks = {}
        for lang in ['bash', 'python', 'json', 'yaml']:
            blocks = re.findall(rf'```{lang}\n(.*?)\n```', raw_text, re.DOTALL)
            if blocks:
                code_blocks[lang] = blocks
        
        return {
            'vibe_text': vibe_text,
            'code_blocks': code_blocks,
            'timestamp': datetime.now().isoformat(),
            'word_count': len(vibe_text.split()),
            'code_block_count': sum(len(blocks) for blocks in code_blocks.values())
        }
    
    def save_extraction(self, extracted_data, conversation_id=None):
        """Save extracted components to organized structure"""
        if not conversation_id:
            conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save vibe/flow
        vibe_path = self.project_root / "exports" / "vibe_flow" / f"{conversation_id}.txt"
        vibe_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(vibe_path, 'w', encoding='utf-8') as f:
            f.write(f"# Conversation Vibe/Flow: {conversation_id}\n")
            f.write(f"# Generated: {extracted_data['timestamp']}\n")
            f.write("="*50 + "\n\n")
            f.write(extracted_data['vibe_text'])
        
        # Save code blocks
        code_export = {}
        for lang, blocks in extracted_data['code_blocks'].items():
            lang_dir = self.project_root / "exports" / "code_blocks" / lang
            lang_dir.mkdir(parents=True, exist_ok=True)
            
            for i, block in enumerate(blocks):
                filename = f"{conversation_id}_{i+1}.{lang if lang != 'bash' else 'sh'}"
                filepath = lang_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(block)
                
                if lang not in code_export:
                    code_export[lang] = []
                code_export[lang].append(str(filepath))
        
        # Save metadata
        metadata = {
            'conversation_id': conversation_id,
            'extraction_time': extracted_data['timestamp'],
            'stats': {
                'vibe_word_count': extracted_data['word_count'],
                'code_blocks_total': extracted_data['code_block_count'],
                'code_blocks_by_lang': {lang: len(blocks) for lang, blocks in extracted_data['code_blocks'].items()}
            },
            'export_paths': {
                'vibe_flow': str(vibe_path),
                'code_blocks': code_export
            }
        }
        
        metadata_path = self.project_root / "data" / "processed" / f"{conversation_id}_metadata.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata