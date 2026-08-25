import logging

#!/usr/bin/env python3
import sys
import json
from fiber_core import DataFiber
from loom_core import DataLoom

class FiberCLI:
    def __init__(self):
        self.loom = DataLoom()
        self.current_user = "bleak"
    
    def run(self):
        logging.info("🌌 MOBILE FIBER LOOM CLI")
        logging.info("Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                cmd = input(f"fiber[{self.current_user}]> ").strip().lower()
                
                if cmd in ['exit', 'quit']:
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'status':
                    self.show_status()
                elif cmd == 'add':
                    self.add_fiber()
                elif cmd == 'list':
                    self.list_fibers()
                elif cmd == 'extract':
                    self.extract_fiber()
                elif cmd == 'visualize':
                    self.loom.visualize_weave()
                elif cmd == 'user':
                    self.change_user()
                elif cmd == '':
                    continue
                else:
                    logging.info("❌ Unknown command. Type 'help' for options.")
                    
            except KeyboardInterrupt:
                logging.info("\n👋 Exiting Fiber Loom")
                break
            except Exception as e:
                logging.info(f"💥 Error: {e}")
    
    def show_help(self):
        logging.info("\n📋 AVAILABLE COMMANDS:")
        logging.info("  status     - Show collective security status")
        logging.info("  add        - Add new data fiber")
        logging.info("  list       - List all fibers")
        logging.info("  extract    - Extract a fiber by ID")  
        logging.info("  visualize  - Show relationship map")
        logging.info("  user       - Change current user")
        logging.info("  help       - Show this help")
        logging.info("  exit       - Exit the CLI")
    
    def show_status(self):
        status = self.loom.get_collective_status()
        logging.info("\n📊 COLLECTIVE STATUS:")
        for key, value in status.items():
            logging.info(f"  {key}: {value}")
    
    def add_fiber(self):
        logging.info("\n🎯 ADD NEW FIBER:")
        data = input("Enter data: ").strip()
        if data:
            fiber = DataFiber(data, self.current_user)
            self.loom.add_fiber(fiber)
            logging.info(f"✅ Fiber added: {fiber.fiber_id[:8]}")
    
    def list_fibers(self):
        if not self.loom.fibers:
            logging.info("\n📭 No fibers in loom")
            return
            
        logging.info(f"\n📁 FIBERS ({len(self.loom.fibers)} total):")
        for fiber_id, fiber in self.loom.fibers.items():
            owner_indicator = " 👑" if fiber.owner_id == self.current_user else ""
            logging.info(f"  {fiber_id[:8]} -> '{fiber.raw_data[:30]}...'{owner_indicator}")
    
    def extract_fiber(self):
        fiber_id = input("Enter fiber ID to extract: ").strip()
        if fiber_id:
            # Find full ID if partial was entered
            full_id = None
            for fid in self.loom.fibers.keys():
                if fid.startswith(fiber_id):
                    full_id = fid
                    break
            
            if full_id:
                fiber = self.loom.extract_fiber(full_id, self.current_user)
                if fiber:
                    logging.info(f"✅ Extracted: {fiber.raw_data}")
                else:
                    logging.info("❌ Extraction failed - check ownership")
            else:
                logging.info("❌ Fiber not found")
    
    def change_user(self):
        new_user = input("Enter new username: ").strip()
        if new_user:
            self.current_user = new_user
            logging.info(f"👤 Switched to user: {new_user}")

if __name__ == "__main__":
    cli = FiberCLI()
    cli.run()
