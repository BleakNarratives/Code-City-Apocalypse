#/bin/bash /storage/emulated/0/scripts/setup_frontend.sh
echo '🤖 SMART EXTRACTOR'
cd /storage/emulated/0/syntaxai_weaponized/
python3 -c "from src.core.simple_extractor import SimpleExtractor; SimpleExtractor().extract_from_text(open('test_conversation.txt').read())"
echo '✅ Done!'
