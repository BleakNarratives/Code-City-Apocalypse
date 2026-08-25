import logging

#!/usr/bin/env python3
"""
SMART EXTRACTOR LAUNCHER
Usage: python3 smart_extract_launch.py [conversation_file.txt] [project_name]
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from core.smart_extractor import SmartCodeExtractor

def main():
    if len(sys.argv) < 2:
        logging.info("Usage: python3 smart_extract_launch.py <conversation_file> [project_name]")
        return
    
    conversation_file = sys.argv[1]
    project_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(conversation_file):
        logging.info(f"Error: File {conversation_file} not found")
        return
    
    # Read conversation
    with open(conversation_file, 'r', encoding='utf-8') as f:
        conversation = f.read()
    
    # Extract project
    extractor = SmartCodeExtractor()
    project_path = extractor.extract_complete_project(conversation, project_name)
    
    logging.info(f"🎉 Project successfully extracted to: {project_path}")
    logging.info("📁 Project contains:")
    for item in project_path.iterdir():
        logging.info(f"   - {item.name}")

if __name__ == "__main__":
    main()
