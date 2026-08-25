import logging

"""
SYNTAX AI - NOW WITH SCRIPTS BITCH WORK MANAGEMENT
"""

import sys
from pathlib import Path

logging.info("🚀 SYNTAX AI - SCRIPTS INTEGRATION ACTIVATED")
logging.info("📱 Running from /storage/emulated/0/syntax_ai")

try:
    from core.syntax_core import SyntaxAICore
    from core.android_integrator import AndroidEcosystemIntegrator
    from core.project_orchestrator import AutonomousProjectOrchestrator
    from core.bleakdev_integration import BleakDevIntegration
    from core.scripts_manager import ScriptsManager
    
    logging.info("✅ All core modules loaded!")
    
    # Initialize systems
    syntax_core = SyntaxAICore()
    integrator = AndroidEcosystemIntegrator(syntax_core)
    orchestrator = AutonomousProjectOrchestrator(integrator)
    bleakdev = BleakDevIntegration()
    scripts_mgr = ScriptsManager()
    
    # Get ecosystem status
    status = orchestrator.get_ecosystem_status()
    
    logging.info(f"\n📊 ECOSYSTEM STATUS:")
    logging.info(f"   Projects found: {status['total_projects']}")
    
    for project in status['projects_found']:
        logging.info(f"   🗂️  {project['name']} - {project['files']} files")
    
    # ANALYZE THAT SCRIPTS FOLDER
    logging.info(f"\n🎯 ANALYZING SCRIPTS FOLDER (156 files)...")
    scripts_analysis = scripts_mgr.analyze_scripts()
    
    if "error" not in scripts_analysis:
        logging.info(f"📦 SCRIPTS FOLDER ANALYSIS:")
        logging.info(f"   Total files: {scripts_analysis['total_files']}")
        logging.info(f"   Python scripts: {scripts_analysis['python_scripts']}")
        logging.info(f"   Shell scripts: {scripts_analysis['shell_scripts']}") 
        logging.info(f"   README files: {scripts_analysis['readme_files']}")
        logging.info(f"   Status: {scripts_analysis['status'].upper()}")
        
        # Show file types
        logging.info(f"   File types: {', '.join([f'{k}: {v}' for k, v in scripts_analysis['file_types'].items()][:5])}")
    
    # FIND AUTOMATION OPPORTUNITIES
    logging.info(f"\n🔍 LOOKING FOR AUTOMATION OPPORTUNITIES...")
    opportunities = scripts_mgr.find_automation_opportunities()
    
    if opportunities:
        logging.info(f"🚀 FOUND {len(opportunities)} AUTOMATION OPPORTUNITIES:")
        for opp in opportunities[:3]:  # Show top 3
            logging.info(f"   ⚡ {opp['file']} - {opp['issue']} [{opp['priority']}]")
    
    # ORGANIZE BITCH WORK
    logging.info(f"\n🗂️  ORGANIZING SCRIPTS INTO BITCH WORK FOLDERS...")
    organized = scripts_mgr.organize_bitch_work()
    
    logging.info(f"✅ ORGANIZED {sum(organized.values())} FILES:")
    for category, count in organized.items():
        if count > 0:
            logging.info(f"   📁 {category}: {count} files")
    
    logging.info(f"\n✅ SYNTAX AI ACTIVE - SCRIPTS MANAGEMENT READY")
    logging.info(f"💡 Commands:")
    logging.info(f"   python -c \"from core.scripts_manager import ScriptsManager; s = ScriptsManager(); logging.info(s.analyze_scripts())\"")
    logging.info(f"   python -c \"from core.scripts_manager import ScriptsManager; s = ScriptsManager(); logging.info(s.find_automation_opportunities())\"")
    
except Exception as e:
    logging.info(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
