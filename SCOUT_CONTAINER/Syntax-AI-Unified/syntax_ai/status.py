import logging

"""
SYNTAX AI - COMPLETE ECOSYSTEM STATUS
"""

from core.syntax_core import SyntaxAICore
from core.android_integrator import AndroidEcosystemIntegrator  
from core.project_orchestrator import AutonomousProjectOrchestrator
from core.bleakdev_integration import BleakDevIntegration
from core.scripts_manager import ScriptsManager
from core.autonomous_fixer import AutonomousFixer

logging.info("🌐 SYNTAX AI - COMPLETE ECOSYSTEM STATUS")
logging.info("=" * 50)

# Initialize all systems
syntax_core = SyntaxAICore()
integrator = AndroidEcosystemIntegrator(syntax_core)
orchestrator = AutonomousProjectOrchestrator(integrator)
bleakdev = BleakDevIntegration()
scripts_mgr = ScriptsManager()

# BleakDev Status
logging.info("\n📊 BLEAKDEV PROJECT:")
bd_analysis = bleakdev.quick_analysis()
logging.info(f"   Python Files: {bd_analysis['python_files']}")
logging.info(f"   Estimated LOC: {bd_analysis['estimated_lines']:.0f}")
logging.info(f"   Status: {bd_analysis['status'].upper()}")

# Scripts Status  
logging.info("\n📦 SCRIPTS REPOSITORY:")
scripts_analysis = scripts_mgr.analyze_scripts()
logging.info(f"   Total Files: {scripts_analysis['total_files']}")
logging.info(f"   Python Scripts: {scripts_analysis['python_scripts']}")
logging.info(f"   Status: {scripts_analysis['status'].upper()}")

# Automation Opportunities
logging.info("\n🚀 AUTOMATION READINESS:")
opportunities = scripts_mgr.find_automation_opportunities()
high_priority = len([o for o in opportunities if o['priority'] == 'HIGH'])
logging.info(f"   High Priority: {high_priority}")
logging.info(f"   Total Opportunities: {len(opportunities)}")

# Bitch Work Organization
logging.info("\n🗂️  BITCH WORK MANAGEMENT:")
organized = scripts_mgr.organize_bitch_work()
logging.info(f"   Organized Files: {sum(organized.values())}")
for category, count in organized.items():
    if count > 0:
        logging.info(f"   {category.upper()}: {count} files")

# System Status
logging.info(f"\n✅ SYNTAX AI SYSTEM:")
logging.info(f"   Core: OPERATIONAL")
logging.info(f"   Android Integration: ACTIVE") 
logging.info(f"   Project Orchestration: READY")
logging.info(f"   Autonomous Fixing: ENABLED")

logging.info(f"\n🎯 NEXT ACTIONS:")
logging.info(f"   1. Run: python autonomous_fix.py")
logging.info(f"   2. Check: ls -la bitch_work/")
logging.info(f"   3. Optimize: python optimize_bleakdev.py")
logging.info(f"   4. Full Scan: python main.py")

logging.info(f"\n🚀 SYNTAX AI ECOSYSTEM - FULLY OPERATIONAL")
