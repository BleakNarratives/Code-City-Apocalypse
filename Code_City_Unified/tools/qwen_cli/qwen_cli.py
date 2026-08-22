#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: os, subprocess, sys
# ROLE: Qwen CLI Integration for Code City Unified
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

"""
Qwen CLI Integration for Code City Unified

This module provides a wrapper around the Qwen Code CLI,
allowing it to be called from the modmind_cli command center.
"""
import subprocess
import sys
import os


def qwen_chat(prompt: str = None, interactive: bool = False, model: str = None):
    """
    Launch Qwen CLI in chat mode.
    
    Args:
        prompt: Optional initial prompt to send to Qwen
        interactive: If True, launch in interactive mode
        model: Optional model to use (e.g., 'qwen2.5-coder:1.5b')
    """
    cmd = ["qwen"]
    
    if model:
        cmd.extend(["-m", model])
    
    if interactive:
        if prompt:
            cmd.extend(["-i", prompt])
        else:
            # Launch in pure interactive mode
            cmd.append("-i",)
    else:
        if prompt:
            cmd.append(prompt)
        else:
            # Default: launch interactive Qwen CLI
            cmd.append("-i")
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: 'qwen' command not found. Please ensure Qwen Code CLI is installed.")
        return 1
    except KeyboardInterrupt:
        print("\nQwen chat interrupted.")
        return 0


def qwen_query(query: str, model: str = None):
    """
    Run a single query through Qwen CLI (non-interactive).
    
    Args:
        query: The query/prompt to send
        model: Optional model to use
    """
    cmd = ["qwen"]
    
    if model:
        cmd.extend(["-m", model])
    
    cmd.append(query)
    
    try:
        result = subprocess.run(cmd, capture_output=False, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: 'qwen' command not found.")
        return 1


def qwen_mcp(command: str = None):
    """
    Manage MCP servers through Qwen CLI.
    
    Args:
        command: Optional MCP subcommand
    """
    cmd = ["qwen", "mcp"]
    
    if command:
        cmd.append(command)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: 'qwen' command not found.")
        return 1


def main():
    """Main entry point for qwen_cli module."""
    if len(sys.argv) < 2:
        print("Qwen CLI Module")
        print("---------------")
        print("Usage: python -m tools.qwen_cli.qwen_cli <command> [args]")
        print("")
        print("Commands:")
        print("  chat [prompt]     - Launch Qwen in chat mode")
        print("  query <prompt>    - Run a single query")
        print("  mcp [command]     - Manage MCP servers")
        print("  help              - Show this help")
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "chat":
        prompt = " ".join(args) if args else None
        return qwen_chat(prompt, interactive=True)
    elif command == "query":
        if not args:
            print("Error: query requires a prompt")
            return 1
        return qwen_query(" ".join(args))
    elif command == "mcp":
        return qwen_mcp(args[0] if args else None)
    elif command == "help":
        return main()
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
