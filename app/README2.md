
Action: file_editor create /app/README.md --file-text "# 🌌 ModMind Command Center

**The Universal Hub for Autonomous Coding** - Transform your development workflow into an epic adventure!

---

## 🎯 What Is This?

ModMind Command Center is a revolutionary coding platform that combines:

1. **🏙️ Code City Visualization** - See your codebase as a living, breathing 3D city
2. **🌌 Blue Sky Meeting Extractor** - AI chat extraction and organization tool
3. **🎮 Gamified Development** - Turn debugging into boss battles

Built for **Termux/Android**, **free tier**, and designed to make coding **addictive and fun**.

---

## 🚀 Quick Start

### Access the App
**URL**: `https://meatsuite-local.preview.emergentagent.com`

### Three Ways to Use

1. **Home Page** (`/`) - Navigation hub
2. **Code City** (`/code-city`) - Visualize any codebase
3. **Blue Sky Extractor** (`/extractor`) - Extract & organize AI chats

---

## 🏙️ Code City - Visualize Your Code

### Features
- **Scan real codebases** from any path (SD card, internal storage, network)
- **3D-style visualization** with glassmorphism UI
- **Real-time health monitoring**
- **Interactive controls** - spawn monsters, repair buildings, pause animation
- **Zone classification** - Industry/Commerce/Residential

### How to Use

1. Navigate to `/code-city`
2. Click **Menu** button (top right)
3. Choose one:
   - **Refresh** - Scan current app
   - **Custom Path** - Enter any path:
     ```
     /sdcard/my_project
     /storage/emulated/0/coding
     /data/data/com.termux/files/home/projects
     ```

### Understanding the Visualization

| Element | Meaning |
|---------|---------|
| **Building** | A code file |
| **Height** | Lines of code (~10 lines per floor) |
| **Width** | File size |
| **Color** | Programming language |
| **Health Bar** | Code quality (100% = healthy) |
| **Windows Lit** | File is active/healthy |
| **Red Overlay** | Damaged/problematic code |

### Controls

- **🏗️ Generate City** - Rebuild from current data
- **👹 Spawn Monster** - Add a code monster
- **💀 Attack Random** - Damage a building
- **✨ Repair Random** - Fix damaged building
- **⏸️ Pause** - Pause/resume

---

## 🌌 Blue Sky Meeting Extractor

### What It Does

Extracts AI conversations and automatically:
1. **Removes all code blocks** from natural language
2. **Saves pure conversation** to organized folders
3. **Extracts code separately** with correct extensions
4. **Organizes by date and AI model**

### Perfect For

- **TTS listening** - No code blocks interrupting audio
- **Knowledge base** - Build searchable archives
- **Code reuse** - All snippets properly saved
- **Learning** - Review AI explanations later

### How to Use

1. Navigate to `/extractor`
2. Select **AI Model** (Claude, GPT-4, Gemini, etc.)
3. **Paste entire chat** into text area
4. Click **Extract & Save**
5. Files saved to `/app/blue_sky_sessions/`

### Output Structure

```
blue_sky_sessions/
└── 2025-01-15/
    └── Claude/
        ├── session_14-30-00_natural_language.txt  # Pure text
        └── code/
            ├── session_14-30-00_code_1.py
            ├── session_14-30-00_code_2.js
            └── session_14-30-00_code_3.html
```

---

## 🎨 Design Philosophy

### Not \"Late 90s AOL\" - Modern & Beautiful

- **Glassmorphism effects** - Frosted glass UI elements
- **Smooth animations** - 60fps canvas rendering
- **Depth & shadows** - 3D-style depth perception
- **Color gradients** - Cyberpunk aesthetic
- **Glow effects** - Neon highlights
- **Responsive design** - Works on all screen sizes

### Visual Language

- **Cyan/Teal** - System elements, UI
- **Green** - Healthy code, success
- **Yellow** - Warnings, attention
- **Red/Pink** - Errors, damage
- **Purple** - Special features

---

## 📁 File Structure

```
/app/
├── backend/
│   ├── server.py              # FastAPI main server
│   ├── code_scanner.py        # Analyzes real codebases
│   ├── chat_extractor.py      # Extracts AI conversations
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── App.js            # Home + routing
│       └── components/
│           ├── CodeCity.js           # Modern visualization
│           └── BlueSkyExtractor.js   # Chat tool
│
├── code_city_modern.html     # Standalone HTML version
└── blue_sky_sessions/        # Extracted chats (auto-created)
```

---

## 🔧 API Reference

### Scan Codebase
```bash
# Scan current app
GET /api/scan-current

# Scan custom path
POST /api/scan-codebase
Content-Type: application/json

{
  \"path\": \"/path/to/code\",
  \"max_files\": 500
}

# Response
{
  \"buildings\": [...],
  \"stats\": {
    \"total_files\": 42,
    \"total_lines\": 5234,
    \"by_zone\": {...},
    \"scan_time\": 0.34
  }
}
```

### Extract Chat
```bash
POST /api/extract-chat
Content-Type: application/json

{
  \"message\": \"Your full chat conversation...\",
  \"model_name\": \"Claude\",
  \"session_id\": \"optional\"
}

# Response
{
  \"session_id\": \"session_14-30-00\",
  \"natural_language_file\": \"/app/blue_sky_sessions/.../file.txt\",
  \"code_files\": [\"file1.py\", \"file2.js\"],
  \"stats\": {
    \"code_blocks_found\": 3,
    \"natural_language_chars\": 1523
  }
}
```

### Get Sessions
```bash
GET /api/sessions

# Response
{
  \"sessions\": [
    {
      \"date\": \"2025-01-15\",
      \"model\": \"Claude\",
      \"path\": \"/app/blue_sky_sessions/2025-01-15/Claude\"
    }
  ]
}
```

---

## 🎮 Code City Zones

### Industry Zone (Backend)
- **Color**: Blues, Teals
- **Files**: `.py`, `.go`, `.java`, `.c`, `.cpp`, `.php`, `.sql`
- **Paths**: `/api/`, `/service/`, `/db/`, `/models/`, `/core/`
- **Agent**: Architect (defends core logic)

### Commerce Zone (Frontend)
- **Color**: Yellows, Oranges
- **Files**: `.js`, `.ts`, `.html`, `.css`, `.vue`, `.jsx`
- **Paths**: `/ui/`, `/app/`, `/components/`, `/views/`
- **Agent**: Refactorer (beautifies UI)

### Residential Zone (Config/Docs)
- **Color**: Greens, Purples
- **Files**: `.json`, `.yaml`, `.md`, `.txt`, `.env`, `.sh`
- **Paths**: `/config/`, `/tests/`, `/docs/`, `/scripts/`
- **Agent**: Defender (protects infrastructure)

---

## 💡 Use Cases

### Daily Workflow
```bash
1. Morning: Open Code City → See what needs attention
2. Coding: Use AI assistant, extract conversations
3. Evening: Review Blue Sky sessions, natural language summaries
```

### Learning & Documentation
- Extract AI tutorials without code clutter
- Build searchable knowledge base
- Perfect for audio review (TTS-friendly)

### Code Reviews
- Visualize file complexity instantly
- Identify problematic areas
- Track health over time

### Team Collaboration
- Share Code City screenshots
- Standardized AI conversation archives
- Knowledge transfer

---

## 🛠️ Technical Stack

- **Backend**: FastAPI + Python 3
- **Frontend**: React 19 + Tailwind CSS
- **Database**: MongoDB (for sessions)
- **Canvas**: HTML5 Canvas API
- **Styling**: CSS3 + Glassmorphism

### Service Management
```bash
# Restart services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status

# View logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/frontend.out.log
```

---

## 📱 Android/Termux Tips

### Storage Access
```bash
# Setup storage access
termux-setup-storage

# Common paths
/sdcard/                          # SD card root
/storage/emulated/0/              # Internal storage
/data/data/com.termux/files/home/ # Termux home
```

### Performance Optimization
- Limit scans to 200-300 files for large projects
- Use specific subfolders instead of root
- Pause animation when not viewing

---

## 🌟 Roadmap

### Code City
- [ ] Real-time file watching
- [ ] AI agent battles (Architect vs Spaghetti Beast)
- [ ] Boss fights (Memory Leak Dragon)
- [ ] Multiple camera angles
- [ ] Export city images/videos

### Blue Sky Extractor
- [ ] Browser extension (auto-capture)
- [ ] Real-time monitoring
- [ ] Git integration
- [ ] Code compilation & execution
- [ ] Search across sessions

---

## 🎯 The ModMind Vision

> **\"Turn code management into an addictive, winnable video game\"**

This is more than a tool—it's a new way to experience code:

1. **Visual** - See patterns, not just text
2. **Gamified** - Bugs become monsters to defeat
3. **Organized** - Knowledge automatically captured
4. **Beautiful** - Coding should look as good as it feels
5. **Free** - Built for everyone, everywhere

---

## 📖 Examples

### Scanning a Project
```bash
# Via UI
1. Open /code-city
2. Enter path: /sdcard/my_app
3. Click Scan

# Via API
curl -X POST https://meatsuite-local.preview.emergentagent.com/api/scan-codebase \
  -H \"Content-Type: application/json\" \
  -d '{\"path\": \"/sdcard/my_app\", \"max_files\": 300}'
```

### Extracting a Chat
```bash
# Via UI
1. Open /extractor
2. Select model: \"Claude\"
3. Paste conversation
4. Click Extract

# Result
✅ Natural language saved
✅ 3 code files extracted
✅ Session: session_14-30-00
```

---

## 🤝 Support

Built by a homeless coder on Android, entirely in Termux, with AI assistants.

**Proof that amazing things can be built anywhere, on any device.**

---

## 📄 License

MIT - Free to use, modify, and distribute

---

## 🔗 Quick Links

- **Home**: `/`
- **Code City**: `/code-city`
- **Blue Sky Extractor**: `/extractor`
- **API Docs**: `/docs` (FastAPI auto-generated)
- **Standalone HTML**: `/app/code_city_modern.html`

---

**\"From chaos to city, from conversation to code—this is ModMind.\"** 🌌✨
"
Observation: Create successful: /app/README.md