#!/data/data/com.termux/files/usr/bin/python3
import os
import json
from pathlib import Path

class ModMindDashboard:
    def __init__(self):
        self.projects_dir = Path.home() / "modmind-projects"
        self.projects_dir.mkdir(exist_ok=True)
    
    def show_menu(self):
        while True:
            os.system('clear')
            print("🛠️  ModMind Dashboard")
            print("1. New Project from FOSS")
            print("2. List Projects")
            print("3. Code Analysis")
            print("4. Blue Sky Session")
            print("5. Exit")
            
            choice = input("Choice: ")
            
            if choice == "1":
                self.new_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.code_analysis()
            elif choice == "4":
                self.blue_sky_session()
            elif choice == "5":
                break
    
    def new_project(self):
        print("Available FOSS bases:")
        bases = {
            "1": "Eclipse Theia",
            "2": "Code-Server", 
            "3": "Custom Git"
        }
        for k, v in bases.items():
            print(f"{k}. {v}")
        
        base = input("Select base: ")
        # Trigger the setup script
        os.system("bash modmind-setup.sh")
    
    def code_analysis(self):
        project = input("Project name: ")
        path = self.projects_dir / project
        
        if path.exists():
            print(f"🔍 Analyzing {project}...")
            # Simple code quality check
            os.system(f"find {path} -name '*.js' -o -name '*.ts' -o -name '*.py' | head -10 | xargs wc -l")
            print("\n📊 Basic metrics complete")
        input("Press Enter to continue...")
    
    def blue_sky_session(self):
        print("💭 Blue Sky Thinking Session")
        print("What's one small improvement you can make today?")
        idea = input("Idea: ")
        print(f"✨ Great! Now break it down:")
        print("1. What's the smallest testable piece?")
        print("2. What existing code can you build on?")
        print("3. What's your first 15-minute task?")
        input("\nPress Enter when ready to start...")

if __name__ == "__main__":
    dashboard = ModMindDashboard()
    dashboard.show_menu()