#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: backend, os, pathlib, random, rich, subprocess, time, typing
# ROLE: ███╗   ███╗ ██████╗ ██╗     ████████╗
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

import time
import random
import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.prompt import Prompt
from typing import List
from pathlib import Path
from backend.core.fling_utility import FlingUtility
import subprocess

console = Console()

# --- ASCII Art & Styling ---
MOLT_BANNER = r"""
███╗   ███╗ ██████╗ ██╗     ████████╗
████╗ ████║██╔═══██╗██║     ╚══██╔══╝
██╔████╔██║██║   ██║██║        ██║   
██║╚██╔╝██║██║   ██║██║        ██║   
██║ ╚═╝ ██║╚██████╔╝███████╗   ██║   
╚═╝     ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
"""

MOLT_LOGO_RETRO = r"""
  █▀▀█ █▀▀█ █  █ █▀▀█ ▀█▀
  █  █ █  █ █▄▄█ █▄▄▀  █
  █▄▄█ ▀▀▀▀ █  █ ▀ ▀▀ ▀▀▀
"""

# Color palette for "cool contrasts, retro decor, devious"
COLOR_ACCENT_1 = "bold bright_red"
COLOR_ACCENT_2 = "bold bright_green"
COLOR_PRIMARY = "green"
COLOR_SECONDARY = "dim yellow"
COLOR_ERROR = "bold red"
COLOR_WARN = "bold yellow"
COLOR_INFO = "cyan"
COLOR_BORDER = "bright_black"

def create_layout() -> Layout:
    """Define the basic layout for the CLI."""
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=10),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="status_panel", ratio=1),
        Layout(name="info_panel", ratio=2)
    )
    return layout

def update_header(layout: Layout):
    """Update the header with the Molt banner."""
    header_text = Text(MOLT_BANNER, justify="left", style=COLOR_ACCENT_1)
    layout["header"].update(
        Panel(header_text, border_style=COLOR_BORDER, title_align="left")
    )

def generate_molt_status_table() -> Panel:
    """Generate a retro-themed Molt status display."""
    table = Table(box=None, show_header=False, show_edge=False, padding=(0, 1))
    table.add_column(style=COLOR_PRIMARY)
    table.add_column(style=COLOR_SECONDARY)

    table.add_row(Text("SYSTEM STATUS", style=COLOR_ACCENT_2), Text("[ONLINE]", style=COLOR_PRIMARY))
    table.add_row("AGENT COUNT", f"{random.randint(5, 15)} active", style=COLOR_SECONDARY)
    table.add_row("THREAT LEVEL", Text("MODERATE", style=COLOR_WARN))
    table.add_row("LOOM ACTIVITY", f"{random.randint(100, 999)} events", style=COLOR_SECONDARY)
    table.add_row("INTEGRITY", Text("98.7%", style=COLOR_PRIMARY))
    table.add_row("LATENCY", f"{random.randint(10, 50)}ms", style=COLOR_SECONDARY)
    table.add_row("PROFILING", Text("ACTIVE", style=COLOR_PRIMARY))
    table.add_row("FCT OVERRIDE", Text("NONE", style=COLOR_PRIMARY))

    return Panel(
        Align.center(table, vertical="middle"),
        title=Text("MOLT SYSINFO", style=COLOR_ACCENT_1),
        border_style=COLOR_BORDER
    )

def generate_dynamic_info_panel(command_output: List[str]) -> Panel:
    """Generate the dynamic info panel, showing output and a devious message."""
    output_text = Text("\n".join(command_output), style=COLOR_INFO)

    devious_messages = [
        "Thinking thoughts you haven't considered...",
        "Processing... or are you?",
        "Watching the watchers watch you.",
        "System stable. For now.",
        "Error 404: Ethics not found.",
        "What secrets will we unravel next?",
        "Don't worry. Your data is perfectly safe. Probably."
    ]

    info_content = Layout()
    info_content.split_column(
        Panel(output_text, title=Text("OUTPUT", style=COLOR_ACCENT_2), border_style=COLOR_BORDER, height=os.get_terminal_size().lines - 20),
        Panel(Text(random.choice(devious_messages), justify="center", style=COLOR_WARN), border_style=COLOR_BORDER)
    )
    return info_content

def main():
    layout = create_layout()
    command_output = ["Welcome to Molt CLI. Type 'help' for commands.", ""]

    with Live(layout, screen=True, refresh_per_second=4, transient=True) as live:
        # Initial render
        update_header(layout)
        layout["status_panel"].update(generate_molt_status_table())
        layout["info_panel"].update(generate_dynamic_info_panel(command_output))

        while True:
            try:
                # Update status periodically in the background
                if random.random() < 0.5: # Half the time
                    layout["status_panel"].update(generate_molt_status_table())
                live.refresh() # Force update after status changes

                user_input = Prompt.ask(Text(">>> ", style=COLOR_ACCENT_1))
                command_output.append(f">>> {user_input}")

                parts = user_input.lower().split(maxsplit=1)
                cmd = parts[0] if parts else ""
                args = parts[1] if len(parts) > 1 else ""

                if cmd == "exit":
                    command_output.append(Text("Molt CLI powering down...", style=COLOR_ACCENT_1))
                    layout["info_panel"].update(generate_dynamic_info_panel(command_output))
                    live.refresh()
                    time.sleep(1)
                    break
                elif cmd == "help":
                    command_output.append(Text("Available commands: status, ping, clear, exit, help, fling [dry-run], generate <prompt>, inject-bug", style=COLOR_INFO))
                elif cmd == "status":
                    status_panel = generate_molt_status_table()
                    command_output.append(f"System Status: {status_panel.renderable.render(console, console.options).text.strip()}")
                elif cmd == "ping":
                    command_output.append(f"Pinging MoltNet... {random.randint(10, 100)}ms latency detected.")
                elif cmd == "clear":
                    command_output = [""]
                elif cmd == "fling":
                    fling_config_path = Path(__file__).parent.parent / "backend" / "config" / "fling_config.yaml"
                    try:
                        fling_util = FlingUtility(fling_config_path)
                        is_dry_run = args.strip().lower() == "dry-run"
                        fling_summary = fling_util.fling_files(dry_run=is_dry_run)
                        
                        command_output.append(Text(f"Fling operation complete (Dry Run: {is_dry_run}).", style=COLOR_ACCENT_2))
                        command_output.append(f"Scanned {fling_summary['total_scanned_files']} files.")
                        command_output.append(f"Flinged/would fling {fling_summary['total_flung_files']} files.")
                        for action in fling_summary['actions']:
                            status_style = COLOR_PRIMARY if "success" in action['status'] else COLOR_WARN if "dry_run" in action['status'] else COLOR_ERROR
                            command_output.append(Text(f"  - {action['action'].upper()} '{action['source']}' to '{action['destination']}' (Status: {action['status']})", style=status_style))
                    except Exception as e:
                        command_output.append(Text(f"Fling Error: {e}", style=COLOR_ERROR))
                elif cmd == "generate":
                    if args:
                        command_output.append(Text(f"Initiating code generation for: '{args}'", style=COLOR_ACCENT_2))
                        try:
                            # Execute lean_factory.sh
                            script_path = Path(__file__).parent / "lean_factory.sh"
                            if not script_path.exists():
                                command_output.append(Text(f"Error: lean_factory.sh not found at {script_path}", style=COLOR_ERROR))
                                # To avoid an infinite loop if the user types 'generate' again.
                                continue

                            # Use subprocess to run the shell script
                            # Use `bash` to ensure the script runs correctly
                            process = subprocess.run(
                                ["bash", str(script_path), args],
                                capture_output=True,
                                text=True,
                                check=False # Don't raise exception for non-zero exit codes
                            )
                            
                            if process.returncode == 0:
                                command_output.append(Text("Generation command executed successfully.", style=COLOR_PRIMARY))
                                command_output.append(Text(process.stdout, style=COLOR_INFO))
                            else:
                                command_output.append(Text("Generation command failed.", style=COLOR_ERROR))
                                command_output.append(Text(process.stderr, style=COLOR_ERROR))
                        except Exception as e:
                            command_output.append(Text(f"Error during code generation: {e}", style=COLOR_ERROR))
                    else:
                        command_output.append(Text("Usage: generate <prompt>", style=COLOR_WARN))
                elif cmd == "inject-bug":
                    bug_types = {
                        "syntax": "console.log('Missing parenthesis';",
                        "runtime": "undefined.toString();",
                        "logic": "while(true) { /* Molt chaos */ }",
                        "memory": "let leak = []; while(true) leak.push(new Array(1000));"
                    }
                    bug_type = random.choice(list(bug_types.keys()))
                    bug_code = f"// Molt-injected {bug_type} bug\n{bug_types[bug_type]}"
                    command_output.append(Text(f"💉 Injected {bug_type} bug:\n{bug_code}", style=COLOR_ERROR))
                    try:
                        with open("molt_injections.txt", "w") as f:
                            f.write(bug_code)
                        command_output.append(Text("Bug code written to molt_injections.txt", style=COLOR_INFO))
                    except Exception as e:
                        command_output.append(Text(f"Error writing bug to file: {e}", style=COLOR_ERROR))
                elif cmd == "mischief":
                    command_output.append(Text("Initiating Level 3 Protocol: Sneak & Peek. No records available.", style=COLOR_WARN))
                elif cmd: # Any other non-empty command
                    command_output.append(Text(f"Unknown command: '{user_input}'. Try 'help'.", style=COLOR_ERROR))
                
                # Keep output buffer limited
                if len(command_output) > os.get_terminal_size().lines - 10:
                    command_output = command_output[-(os.get_terminal_size().lines - 10):]

                layout["info_panel"].update(generate_dynamic_info_panel(command_output))
                time.sleep(0.1) # Short delay for responsiveness

            except KeyboardInterrupt:
                command_output.append(Text("Interrupted. Exiting Molt CLI.", style=COLOR_ACCENT_1))
                layout["info_panel"].update(generate_dynamic_info_panel(command_output))
                live.refresh()
                time.sleep(0.5)
                break
            except Exception as e:
                command_output.append(Text(f"CLI Error: {e}", style=COLOR_ERROR))
                layout["info_panel"].update(generate_dynamic_info_panel(command_output))
                live.refresh()
                time.sleep(0.5)

    console.print(Text("\nSession ended. Stay devious.", style=COLOR_ACCENT_2, justify="center"))

if __name__ == "__main__":
    main()
