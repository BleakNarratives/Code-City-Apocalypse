#!/usr/bin/env python3
import sys
import os
import subprocess

# Add the modmind_unified/src directory to the Python path
modmind_src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modmind_unified', 'src')
sys.path.append(modmind_src_path)

# Add the tools directory to the Python path for qwen_cli
tools_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools')
sys.path.append(tools_path)

# Try to import modmind_architect, but make it optional for Qwen commands
try:
    from modmind_architect import modmind_architect
    MODMIND_AVAILABLE = True
except (ImportError, NameError):
    MODMIND_AVAILABLE = False
    print("Note: modmind_architect not available. Qwen commands will still work.")


def qwen_chat(prompt: str = None):
    """Launch Qwen CLI in chat mode."""
    from tools.qwen_cli.qwen_cli import qwen_chat as qwen_chat_fn
    return qwen_chat_fn(prompt, interactive=True)


def qwen_query(query: str):
    """Run a single query through Qwen CLI."""
    from tools.qwen_cli.qwen_cli import qwen_query as qwen_query_fn
    return qwen_query_fn(query)


def run_modmind_architect(task: str):
    """Run the modmind_architect if available."""
    if not MODMIND_AVAILABLE:
        print("Error: modmind_architect is not available.")
        print("The modmind_unified/src/modmind_architect.py file may need to be updated.")
        return 1
    
    try:
        from modmind_architect import SwarmController
        controller = SwarmController()
        result = controller.route_task(task)
        print(f"\nResult: {result}")
        return 0
    except Exception as e:
        print(f"Error running modmind_architect: {e}")
        return 1


def main():
    print("Welcome to Code City & Vertical AI Command Center")
    print("-----------------------------------------------")

    try:
        if len(sys.argv) > 1:
            command = sys.argv[1]
            args = sys.argv[2:]
            
            # Handle Qwen commands
            if command == "qwen_chat":
                prompt = " ".join(args) if args else None
                return qwen_chat(prompt)
            elif command == "qwen_query":
                if not args:
                    print("Usage: python -m code_city.modmind_cli qwen_query <prompt>")
                    return 1
                return qwen_query(" ".join(args))
            elif command == "qwen_mcp":
                cmd = ["qwen", "mcp"] + args
                result = subprocess.run(cmd, check=False)
                return result.returncode
            else:
                # Default: pass to modmind_architect
                task = " ".join(sys.argv[1:])
                return run_modmind_architect(task)
        else:
            task = input("What are we building today, Mike? ")
            return run_modmind_architect(task)
    except KeyboardInterrupt:
        print("\nExiting.")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
