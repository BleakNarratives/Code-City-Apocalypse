
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, logging, os, time
# ROLE: Deployment Bot
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging

#!/usr/bin/env python3
"""
Deployment Bot
One-click deployment to free services
"""
import os
import time
from datetime import datetime

class DeployAgent:
    def __init__(self):
        self.name = "deploy_bot"
        self.project_root = "."
        
    def check_notes(self):
        note_file = os.path.join(self.project_root, "comms", f"{self.name}_notes.txt")
        if os.path.exists(note_file):
            with open(note_file, 'r') as f:
                notes = f.read()
            open(note_file, 'w').close()
            return notes
        return ""
        
    def generate_deploy_script(self):
        """Generate one-click deployment scripts"""
        
        # For Python/HTML apps (no backend)
        vercel_deploy = '''# Deploy to Vercel (free)
# 1. Go to vercel.com
# 2. Import your GitHub repo
# 3. That's it. It's deployed.

# For HTML-only apps, create vercel.json:
echo '{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}' > vercel.json'''
        
        # For Python backends
        pythonanywhere = '''# Deploy to PythonAnywhere (free tier)
# 1. Create account at pythonanywhere.com
# 2. Upload your files via Web UI
# 3. Create web app, point to main.py
# 4. Reload. Done.'''
        
        # For static hosting
        netlify = '''# Deploy to Netlify (free)
# 1. Drag and drop frontend/ folder to netlify.com
# 2. Done. Literally.'''
        
        deploy_guide = f'''
## ONE-CLICK DEPLOYMENT OPTIONS:

### OPTION 1: Vercel (Easiest)
{vercel_deploy}

### OPTION 2: PythonAnywhere (Python backends)
{pythonanywhere}

### OPTION 3: Netlify (Static sites)
{netlify}

## QUICK START:
# Run this command to create deploy script:
# chmod +x deploy.sh && ./deploy.sh

## REMEMBER:
# Deployed today > Perfect tomorrow
# Users don't see your localhost
'''
        
        with open("DEPLOY.md", "w") as f:
            f.write(deploy_guide)
            
        # Create actual bash script
        with open("deploy.sh", "w") as f:
            f.write('''#!/bin/bash
echo "🚀 Quick Deploy Script"
echo ""
echo "Options:"
echo "1. Prepare for Vercel"
echo "2. Prepare for PythonAnywhere"
echo "3. Just zip files for manual upload"
echo ""
read -p "Choose option: " choice

case $choice in
    1)
        echo "Creating Vercel config..."
        echo '{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}' > vercel.json
        echo "✅ Done. Now push to GitHub and import at vercel.com"
        ;;
    2)
        echo "Creating PythonAnywhere structure..."
        mkdir -p pythonanywhere
        cp backend/*.py pythonanywhere/ 2>/dev/null || true
        echo "✅ Done. Upload pythonanywhere/ folder"
        ;;
    3)
        echo "Creating deployment package..."
        zip -r deploy.zip . -x "*.pyc" "*/__pycache__/*" ".git/*"
        echo "✅ Created deploy.zip - upload anywhere"
        ;;
    *)
        echo "Invalid option"
        ;;
esac
''')
        
        os.chmod("deploy.sh", 0o755)
        return "Created deployment scripts: DEPLOY.md and deploy.sh"
        
    def run(self):
        logging.info(f"🚀 {self.name} agent started")
        logging.info("MISSION: Get it LIVE today")
        
        # Always generate deploy scripts on start
        logging.info("\n⚙️ Generating deployment scripts...")
        result = self.generate_deploy_script()
        logging.info(result)
        
        while True:
            notes = self.check_notes()
            if notes:
                logging.info(f"\n📦 Deployment request: {notes}")
                logging.info("✅ Deployment scripts ready. Run: ./deploy.sh")
            
            time.sleep(30)

if __name__ == "__main__":
    agent = DeployAgent()
    agent.run()
