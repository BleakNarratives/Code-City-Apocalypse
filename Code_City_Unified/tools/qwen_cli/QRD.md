# Qwen CLI - Quick RunDown (QRD)

**Version:** 1.0  
**Created:** 2026-03-25  
**Project:** Code City Unified  
**Author:** Qwen (with Mike)

---

## What This Is

Qwen CLI integration for Code City Unified. Lets you talk to Qwen AI directly from your terminal, inside your project structure.

**Two flavors:**
- **On-Road** (QRD.md) - This file. Quick, dirty, get-shit-done reference.
- **Off-Road** (QRD.html) - Visual, pretty, deep-dive walkthrough.

---

## The 30-Second Version

```bash
# Start session
qwen_start

# Chat with Qwen
qchat

# Ask a quick question
qquery "how do I fix this?"

# End session
qwen_end "did X, need to do Y"
```

Done. You're welcome.

---

## The Real Walkthrough

### Step 1: Setup (One Time)

```bash
# Navigate to project
ccity

# Check the integration exists
ls tools/qwen_cli/
# Should see: qwen_cli.py, configs/, prompts/

# Test it works
python -m code_city.modmind_cli qwen_query "2+2"
# Should print: 4
```

### Step 2: Daily Workflow

**Morning:**
```bash
qwen_start
```
This shows you:
- Git status (what changed)
- Recent commits
- Last session context
- Project structure

**During Work:**
```bash
# Stuck on code?
qchat "help me debug this function"

# Quick question?
qquery "what's the Python equivalent of JavaScript's map()?"

# Need to review code?
qchat "review @path/to/file.py for bugs"

# MCP servers?
qmcp list
```

**End of Session:**
```bash
qwen_end "fixed the auth bug, next: implement rate limiting"
```
This:
- Logs your changes
- Updates context file
- Saves session notes for future you

### Step 3: Recovery (When You Forget)

```bash
# What was I working on?
qcontext

# What did I do last session?
qlog

# Where am I?
ccity && git status
```

---

## Command Reference (Cheat Sheet)

### Core Commands

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `qchat` | Opens interactive Qwen chat | Pair programming, debugging, design |
| `qquery "X"` | Single question, single answer | Quick facts, explanations |
| `qmcp` | MCP server management | Advanced: managing AI tools |
| `qwen_start` | Load session context | Starting work |
| `qwen_end` | Save session state | Ending work |

### Navigation

| Command | What It Does |
|---------|-------------|
| `ccity` | CD to Code_City_Unified |
| `qcontext` | Show project context |
| `qlog` | Show session history |

### Direct Qwen CLI

```bash
qwen "prompt"              # Single query
qwen -i                    # Interactive mode
qwen -m model "prompt"     # Specific model
qwen mcp                   # MCP management
```

---

## File Structure (What's Where)

```
~/.qwen/
├── qwen_context.md      # Project memory (READ THIS)
├── qwen_quickref.md     # Quick commands
├── session_log.md       # Session history
└── AUTOMATION_KIT.md    # Tool documentation

~/bin/
├── qwen_start.sh        # Session starter
├── qwen_end.sh          # Session ender
└── qwen_env.sh          # Environment loader

~/Code_City_Unified/tools/qwen_cli/
├── qwen_cli.py          # Core integration
├── qwen_cli_v1.py       # Backup v1
├── configs/             # Settings
├── prompts/             # Templates
└── README.md            # Official docs
```

---

## Common Patterns

### Debugging Code

```bash
qchat "I'm getting an import error in modmind_cli.py. Here's the traceback: [paste]"
```

### Code Review

```bash
qchat "Review tools/qwen_cli/qwen_cli.py for:
1. Potential bugs
2. Style issues
3. Missing error handling"
```

### Generate Code

```bash
qchat "Create a Python function that:
- Takes a list of files
- Returns dict grouped by extension
- Include type hints and docstring"
```

### Explain Something

```bash
qquery "Explain how SwarmController routes tasks in modmind_architect.py"
```

### Architecture Design

```bash
qchat "Design a plugin system for Code City. Requirements:
- Hot-reload plugins
- Version compatibility check
- Dependency management"
```

---

## Troubleshooting (When Shit Breaks)

### "modmind_architect not available"
**Fix:** Ignore it. Qwen commands still work. This is a known fallback.

### "qwen command not found"
**Fix:**
```bash
which qwen
# If nothing: npm install -g @mmmbuto/qwen-code-termux
```

### "Permission denied"
**Fix:**
```bash
chmod +x ~/bin/qwen_*.sh
chmod +x ~/Code_City_Unified/tools/qwen_cli/*.py
```

### Session context lost
**Fix:**
```bash
cat ~/.qwen/session_log.md | tail -100
# Your work is logged there
```

---

## Pro Tips

### 1. Use @file References
```bash
qchat "Review @tools/qwen_cli/qwen_cli.py for optimization opportunities"
```

### 2. Chain Queries
```bash
qquery "What is a context manager?"
qquery "Show me an example"
qquery "When should I NOT use one?"
```

### 3. Save Good Prompts
```bash
# Save to prompts/ directory
echo "Review this code for security issues..." > prompts/security_review.md
```

### 4. Version Before Big Changes
```bash
bash ~/tag_version.sh tools/qwen_cli/qwen_cli.py
# Now you can rollback if needed
```

### 5. Sync to SD Card
```bash
bash ~/sync_gemini.sh
# Now both instances have same code
```

---

## The "Off-Road" Version

Want the **visual, deep-dive, pretty HTML version?**

```bash
# Open in browser
xdg-open ~/Code_City_Unified/tools/qwen_cli/QRD.html

# Or from sdcard
xdg-open /sdcard/Code_City_Unified/tools/qwen_cli/QRD.html
```

That's the **Off-Road** experience - formatted, styled, with diagrams.

This (**QRD.md**) is the **On-Road** - quick, terminal-friendly, no bullshit.

---

## Session Templates

### Morning Standup (With Yourself)
```bash
qwen_start
qchat "Here's what I'm working on today: [task list]. Help me prioritize."
```

### Code Review Session
```bash
qchat "I'm about to commit. Review these changes: [git diff]"
```

### Learning Session
```bash
qchat "Teach me about [topic]. Use examples from this codebase."
```

### Debugging Session
```bash
qchat "Debug this with me. Error: [error]. Code: [code]"
```

---

## Metrics That Matter

| Metric | Target | Check With |
|--------|--------|------------|
| Session start time | < 5 seconds | `time qwen_start` |
| Query response | < 3 seconds | `time qquery "test"` |
| Context file updated | Every session | `qwen_end` |
| Git commits | Daily | `git log --oneline` |

---

## Next Steps (Where to Go From Here)

1. **Run `qwen_start`** - See your context
2. **Try `qchat`** - Start a conversation
3. **End with `qwen_end`** - Save your state
4. **Repeat** - Build the habit

---

## Questions?

```bash
# Check context
qcontext

# Check log
qlog

# Ask Qwen
qquery "How do I use [X]?"

# Read the HTML version
cat ~/Code_City_Unified/tools/qwen_cli/QRD.html
```

---

**Remember:** The best documentation is the one you actually *use*. This is designed to be:
- ✅ Quick to scan
- ✅ Easy to remember
- ✅ Terminal-friendly
- ✅ Always available

Now go build something. 🚀
