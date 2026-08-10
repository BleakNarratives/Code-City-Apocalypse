#!/usr/bin/env python3
"""
APOCALYPSE INTEGRATION - Connects code errors to visual disasters
"""
from code_city_apocalypse import CodeCityApocalypse
from smart_coder import SmartCoder
import traceback

class ApocalypseCoder:
    def __init__(self):
        self.coder = SmartCoder()
        self.city = CodeCityApocalypse()
        self.city.scan_project(".")
    
    def generate_with_apocalypse(self, description, language="python"):
        """Generate code with disaster visualization"""
        try:
            result = self.coder.generate_from_description(description, language)
            
            # Save files
            for filename, content in result["files"].items():
                with open(filename, 'w') as f:
                    f.write(content)
                print(f"📄 Created: {filename}")
            
            # Test the generated code for errors
            self.test_for_disasters(result)
            
            return result
            
        except Exception as e:
            # Trigger disaster on generation error
            error_type = type(e).__name__.lower()
            self.city.trigger_disaster(error_type, "generation", str(e))
            self.city.render_city()
            raise
    
    def test_for_disasters(self, result):
        """Test generated code and trigger disasters for errors"""
        for filename, content in result["files"].items():
            if filename.endswith('.py'):
                # Simple syntax check (in real use, would run the code)
                if 'error' in content.lower() or 'bug' in content.lower():
                    self.city.trigger_disaster("logic_error", filename, "Potential bug detected in generated code")
                
                # Check for common issues
                if 'import ' in content and 'not found' in content:
                    self.city.trigger_disaster("import_error", filename, "Missing import detected")
        
        self.city.render_city()
    
    def live_apocalypse_mode(self):
        """Live mode with continuous disaster monitoring"""
        print("🌋 LIVE APOCALYPSE MODE ACTIVATED!")
        print("Every error becomes a visual disaster!")
        
        import time
        while True:
            try:
                command = input("\n💬 Code Command: ").strip()
                if command.lower() in ['exit', 'quit']:
                    break
                
                if command.startswith('#python'):
                    self.generate_with_apocalypse(command.replace('#python', '').strip(), 'python')
                elif command.startswith('#react'):
                    self.generate_with_apocalypse(command.replace('#react', '').strip(), 'react')
                else:
                    print("❓ Use #python or #react commands")
                
                # Update city state
                self.city.update_city()
                self.city.render_city()
                
            except Exception as e:
                print(f"💥 Generation error: {e}")
                self.city.trigger_disaster("runtime_error", "live_mode", str(e))
                self.city.render_city()

def main():
    apocalypse_coder = ApocalypseCoder()
    apocalypse_coder.live_apocalypse_mode()

if __name__ == "__main__":
    main()