# Vertical AI – The Boardroom in Your Terminal

**Vertical AI** is a terminal-based, multi‑persona AI boardroom that debates your ideas, analyzes markets, evolves business models, and visualizes everything in a 3D city. It's designed to run entirely on your Android phone (Termux) or any Linux system, using local LLMs via Ollama.

## Why Vertical AI?

Most AI tools give you one answer. Vertical AI gives you **a council of disagreeing experts**—each with a distinct role—who challenge your assumptions, spot flaws, and sharpen your strategy. It's like having a CEO, CTO, CMO, Adversary, and a few eccentric geniuses in your pocket, ready to argue at 3am.

## Features

- 🧠 **8+ AI Personas** – CEO, Adversary, Architect, CMO, Threat Modeler, Rap Genius, Pytch (creative), Twoie (analytical). Each with unique prompts and biases.
- 🗳️ **Voting & Consensus** – Personas vote on ideas; you decide whether to execute.
- 📊 **Swarm Analytics** – Scouts gather market data, competitor intelligence, and trend signals (via free APIs or simulated data).
- 🧬 **Automation DNA** – Business models encoded as strings that mutate, crossover, and evolve based on swarm feedback.
- 🌆 **Code City Visualization** – A 3D city built with Three.js that represents your projects, agents, and data flows. Buildings glow when agents act.
- 📱 **Mobile‑First** – Runs in Termux on Android. No cloud required. All models local via Ollama.
- 🔁 **Context Memory** – ConTrailer integration gives personas persistent memory across sessions.
- 🎤 **Interruptible Interface** – Type your ideas, personas respond in real time. (Voice input planned.)

## Architecture


┌─────────────────────────────────────────────────────────────┐
│                     Vertical AI Ecosystem                   │
├───────────────┬───────────────────────────┬─────────────────┤
│  Boardroom    │  Swarm Scouts             │  Automation DNA │
│  (Personas)   │  (Market data, trends)    │  (Genetic algo) │
├───────────────┼───────────────────────────┼─────────────────┤
│  ConTrailer   │  Code City                 │  Molt (orchestrator)│
│  (Memory)     │  (3D visualization)        │  (Agent runner) │
└───────────────┴───────────────────────────┴─────────────────┘

```

## Installation (Termux)

```bash
# Update and install dependencies
pkg update && pkg upgrade
pkg install python git nodejs ollama

# Clone the repository
git clone https://github.com/BleakNarratives/vertical-ai.git
cd vertical-ai

# Install Python packages
pip install -r requirements.txt

# Pull a local model (Mistral 7B recommended)
ollama pull mistral:7b-instruct

# (Optional) Install Code City dependencies
cd code-city
npm install
```

Usage

1. Start the boardroom:
   ```bash
   python boardroom.py
   ```
   Type an idea, watch the personas argue. Press Ctrl+C to exit.
2. Run swarm scouts (simulated for now):
   ```bash
   python swarm.py --topic "AI in healthcare"
   ```
3. Evolve business models:
   ```bash
   python dna.py --population models.json --generations 10
   ```
4. Launch Code City:
   Open code-city/index.html in your browser (or use termux-open).

Configuration

Edit persona_registry.py to customize persona prompts. Add your own personas by placing a .py file in personas/ with a PROMPT variable.

For real market data, sign up for free API keys (NewsAPI, Yahoo Finance) and add them to .env.

Project Structure

```
vertical-ai/
├── boardroom.py          # Main TUI
├── persona_registry.py   # Loads all personas
├── context.py            # ConTrailer interface
├── swarm.py              # Scouts & analytics
├── dna.py                # Genetic business models
├── code-city/            # 3D visualization (submodule)
├── personas/             # Custom persona definitions
├── logs/                 # Session history
└── README.md
```

Why It Works on a Phone

· Local models via Ollama (no API costs).
· Lightweight TUI with curses.
· Minimal dependencies – Python + standard libraries.
· Offline‑capable – all data stays on device.

Roadmap

· Persona registry
· Basic boardroom TUI
· Voice input (Termux:API)
· Real swarm scouts (NewsAPI integration)
· Full genetic algorithm with evaluation
· Code City integration (live updates)
· Web dashboard (optional)

Contributing

This is a one‑man passion project, but ideas and PRs welcome. If you want to add a persona or improve the UI, fork and go for it.

License

MIT – because sharing is caring, and I want everyone to have their own arguing boardroom.

Acknowledgements

Built with blood, sweat, and Termux by Mikey. Inspired by the need to never trust a single AI again.

```