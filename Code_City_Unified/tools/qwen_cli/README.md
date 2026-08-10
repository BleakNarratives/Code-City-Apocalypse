# Qwen CLI for Code City Unified

> Integration layer for Qwen Code CLI within the Code City command center.

## Overview

This toolkit provides seamless integration between the Qwen Code CLI and the Code City Unified multi-agent orchestration system. It enables interactive AI-assisted development, single-query operations, and MCP server management through a unified command interface.

## Installation

### Prerequisites

- **Termux** (Android) or compatible Linux environment
- **Python 3.6+**
- **Qwen Code CLI** installed (`qwen` command available)
- **Code_City_Unified** project structure

### Setup

The Qwen CLI integration is located at:
```
~/Code_City_Unified/tools/qwen_cli/
```

To enable shell aliases, add to `~/.bashrc`:
```bash
# Qwen CLI Aliases
alias qchat='python -m code_city.modmind_cli qwen_chat'
alias qquery='python -m code_city.modmind_cli qwen_query'
alias qmcp='python -m code_city.modmind_cli qwen_mcp'
alias qwen_start='bash ~/bin/qwen_start.sh'
alias qwen_end='bash ~/bin/qwen_end.sh'
alias ccity='cd ~/Code_City_Unified'
```

Then reload:
```bash
source ~/.bashrc
```

## Project Structure

```
Code_City_Unified/
├── tools/
│   └── qwen_cli/
│       ├── qwen_cli.py          # Core Qwen CLI wrapper
│       ├── qwen_cli_v1.py       # Versioned backup
│       ├── configs/             # Qwen configuration files
│       ├── prompts/             # Custom prompt templates
│       └── README.md            # This file
├── code_city/
│   └── modmind_cli.py           # Main CLI entry point (updated)
└── vertical_swarm/              # Boardroom orchestration
```

## Usage

### Interactive Chat Mode

Launch Qwen in interactive chat mode:

```bash
# Full command
python -m code_city.modmind_cli qwen_chat

# With alias
qchat

# With initial prompt
python -m code_city.modmind_cli qwen_chat "Help me debug this function"
```

### Single Query Mode

Run a non-interactive query:

```bash
# Full command
python -m code_city.modmind_cli qwen_query "What is the capital of France?"

# With alias
qquery "Explain this code pattern"

# Direct Qwen CLI
qwen "Your question here"
```

### MCP Server Management

Manage MCP (Model Context Protocol) servers:

```bash
# List MCP servers
python -m code_city.modmind_cli qwen_mcp list

# Add MCP server
python -m code_city.modmind_cli qwen_mcp add <server>

# With alias
qmcp
```

### Session Management

Start a new session with full context:

```bash
qwen_start
```

End session and save state:

```bash
qwen_end "Worked on X, next do Y"
```

## Shell Aliases

| Alias | Command | Description |
|-------|---------|-------------|
| `qchat` | `python -m code_city.modmind_cli qwen_chat` | Interactive chat |
| `qquery` | `python -m code_city.modmind_cli qwen_query` | Single query |
| `qmcp` | `python -m code_city.modmind_cli qwen_mcp` | MCP management |
| `ccity` | `cd ~/Code_City_Unified` | Navigate to project |
| `qcontext` | `cat ~/.qwen/qwen_context.md` | View context |
| `qlog` | `tail -50 ~/.qwen/session_log.md` | View session log |
| `qwen_start` | `bash ~/bin/qwen_start.sh` | Start session |
| `qwen_end` | `bash ~/bin/qwen_end.sh` | End session |

## Configuration

### Model Selection

Specify a model for Qwen commands:

```bash
qwen -m qwen2.5-coder:1.5b "Your prompt"
```

### Custom Prompts

Add custom prompt templates to `tools/qwen_cli/prompts/`:

```
prompts/
├── code_review.md
├── bug_fix.md
├── feature_request.md
└── architecture_design.md
```

### Settings

Qwen CLI settings are stored in `~/.qwen/settings.json`:

```json
{
  "model": "qwen2.5-coder:1.5b",
  "telemetry": {
    "enabled": false
  },
  "tools": {
    "sandbox": false
  }
}
```

## Integration with Code City

The Qwen CLI is integrated into the main `modmind_cli.py` entry point:

```python
# code_city/modmind_cli.py handles:
# - qwen_chat: Interactive Qwen sessions
# - qwen_query: Single-shot queries
# - qwen_mcp: MCP server management
# - Default: ModMind agent swarm
```

### Agent Swarm Fallback

If Qwen is unavailable, commands fall back to the ModMind agent swarm:

```bash
python -m code_city.modmind_cli "Analyze this codebase"
```

## Version Control

Tag versions of Qwen CLI files:

```bash
bash ~/tag_version.sh tools/qwen_cli/qwen_cli.py
```

This creates versioned backups:
```
qwen_cli_v1.py
qwen_cli_v2.py
...
```

## Synchronization

Sync between local and SD card instances:

```bash
bash ~/sync_gemini.sh
```

Locations:
- `~/Code_City_Unified/tools/qwen_cli/`
- `/sdcard/Code_City_Unified/tools/qwen_cli/`

## Troubleshooting

### Import Errors

If you see `modmind_architect not available`:

```bash
# Check the module exists
ls ~/Code_City_Unified/modmind_unified/src/modmind_architect.py

# The Qwen commands will still work - this is a known fallback behavior
```

### Qwen Command Not Found

```bash
# Verify Qwen CLI installation
which qwen

# Reinstall if needed
npm install -g @mmmbuto/qwen-code-termux
```

### Permission Issues

```bash
# Make scripts executable
chmod +x ~/bin/qwen_*.sh
chmod +x ~/Code_City_Unified/tools/qwen_cli/qwen_cli.py
```

## API Reference

### qwen_cli.py Functions

#### `qwen_chat(prompt=None, interactive=True, model=None)`
Launch Qwen in chat mode.

**Parameters:**
- `prompt` (str, optional): Initial prompt to send
- `interactive` (bool): Launch in interactive mode
- `model` (str, optional): Model to use

**Returns:** Exit code (int)

#### `qwen_query(query, model=None)`
Run a single query.

**Parameters:**
- `query` (str): The query/prompt
- `model` (str, optional): Model to use

**Returns:** Exit code (int)

#### `qwen_mcp(command=None)`
Manage MCP servers.

**Parameters:**
- `command` (str, optional): MCP subcommand

**Returns:** Exit code (int)

## Contributing

1. Make changes to `tools/qwen_cli/qwen_cli.py`
2. Test with `qchat` and `qquery`
3. Tag version: `bash ~/tag_version.sh tools/qwen_cli/qwen_cli.py`
4. Sync: `bash ~/sync_gemini.sh`
5. Update this README

## License

Part of Code City Unified project.

## Support

- Context: `~/.qwen/qwen_context.md`
- Session Log: `~/.qwen/session_log.md`
- Quick Ref: `~/.qwen/qwen_quickref.md`
