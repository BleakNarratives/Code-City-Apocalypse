#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: fiber_core, json, loom_core, sys
# ROLE: FiberCLI class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

import sys
import json
from fiber_core import DataFiber
from loom_core import DataLoom

class FiberCLI:
    def __init__(self):
        self.loom = DataLoom()
        self.current_user = "bleak"
    
    def run(self):
        print("🌌 MOBILE FIBER LOOM CLI")
        print("Type 'help' for commands, 'exit' to quit\n")
        
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
                    print("❌ Unknown command. Type 'help' for options.")
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting Fiber Loom")
                break
            except Exception as e:
                print(f"💥 Error: {e}")
    
    def show_help(self):
        print("\n📋 AVAILABLE COMMANDS:")
        print("  status     - Show collective security status")
        print("  add        - Add new data fiber")
        print("  list       - List all fibers")
        print("  extract    - Extract a fiber by ID")  
        print("  visualize  - Show relationship map")
        print("  user       - Change current user")
        print("  help       - Show this help")
        print("  exit       - Exit the CLI")
    
    def show_status(self):
        status = self.loom.get_collective_status()
        print("\n📊 COLLECTIVE STATUS:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    def add_fiber(self):
        print("\n🎯 ADD NEW FIBER:")
        data = input("Enter data: ").strip()
        if data:
            fiber = DataFiber(data, self.current_user)
            self.loom.add_fiber(fiber)
            print(f"✅ Fiber added: {fiber.fiber_id[:8]}")
    
    def list_fibers(self):
        if not self.loom.fibers:
            print("\n📭 No fibers in loom")
            return
            
        print(f"\n📁 FIBERS ({len(self.loom.fibers)} total):")
        for fiber_id, fiber in self.loom.fibers.items():
            owner_indicator = " 👑" if fiber.owner_id == self.current_user else ""
            print(f"  {fiber_id[:8]} -> '{fiber.raw_data[:30]}...'{owner_indicator}")
    
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
                    print(f"✅ Extracted: {fiber.raw_data}")
                else:
                    print("❌ Extraction failed - check ownership")
            else:
                print("❌ Fiber not found")
    
    def change_user(self):
        new_user = input("Enter new username: ").strip()
        if new_user:
            self.current_user = new_user
            print(f"👤 Switched to user: {new_user}")

if __name__ == "__main__":
    cli = FiberCLI()
    cli.run()
