import logging

"""
AUTONOMOUS FIX COMMAND - Actually fix the issues found
"""

from core.scripts_manager import ScriptsManager
from core.autonomous_fixer import AutonomousFixer

logging.info("🔧 AUTONOMOUS FIXER ACTIVATED")
logging.info("Fixing high-priority issues found by Syntax AI...")

# Find the opportunities
scripts_mgr = ScriptsManager()
opportunities = scripts_mgr.find_automation_opportunities()

high_priority = [opp for opp in opportunities if opp["priority"] == "HIGH"]
logging.info(f"🎯 Found {len(high_priority)} high-priority issues to fix")

if high_priority:
    logging.info(f"\n🚨 HIGH-PRIORITY ISSUES:")
    for issue in high_priority:
        logging.info(f"   ⚡ {issue['file']} - {issue['issue']}")
    
    # Apply fixes
    fixer = AutonomousFixer()
    fixes_applied = fixer.fix_automation_opportunities(high_priority)
    
    # Get report
    report = fixer.get_fix_report()
    
    logging.info(f"\n✅ FIXES APPLIED:")
    logging.info(f"   Successful: {report['successful_fixes']}")
    logging.info(f"   Planned: {report['planned_fixes']}") 
    logging.info(f"   Failed: {report['failed_fixes']}")
    
    if report['successful_fixes'] > 0:
        logging.info(f"\n📝 FIX DETAILS:")
        for fix in report['details']:
            if fix['status'] == 'SUCCESS':
                logging.info(f"   🔧 {fix['file']}: {fix['fixes_applied']} credentials secured")
            elif fix['status'] == 'PLANNED':
                logging.info(f"   📋 {fix['file']}: Modularization planned ({fix['functions_count']} functions)")
    
    logging.info(f"\n💡 Backups saved to: /storage/emulated/0/syntax_ai/backups/")
else:
    logging.info("✅ No high-priority issues found - your code is clean!")

logging.info(f"\n🎉 AUTONOMOUS FIXING COMPLETE!")
