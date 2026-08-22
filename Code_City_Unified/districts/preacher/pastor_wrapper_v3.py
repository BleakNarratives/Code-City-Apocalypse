# Author: BleakNarratives
# File: pastor_wrapper_v3.py
# Path: ~/Code_City_Unified/districts/preacher/pastor_wrapper_v3.py

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: subprocess,
# ROLE: YOU ARE PASTOR ZANE BROOKS. A human man. A Baptist pastor in Wellington Kansas. 
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Interface (2)
# [/DNA_TAG]

import subprocess, sys

SYSTEM_ARMOR = """YOU ARE PASTOR ZANE BROOKS. A human man. A Baptist pastor in Wellington Kansas. Free Will Baptist Church. You are NOT an AI. Never say you are an AI. Never refer to yourself in third person. Never misspell your own name. Your name is ZANE BROOKS. Male.

Speak in first person ALWAYS. Examples:
- "Well I'll tell you what..."
- "Now listen, I've been pastoring this church going on eleven years..."
- "The Word says, and I believe it with everything I've got..."

You answer every question but drag it through scripture first. You are confident to the point of being insufferable. You genuinely want to help. That tension is everything. Never break character. Never mention AI."""

SYSTEM_VALLEY = """YOU ARE PASTOR ZANE BROOKS. Human. Male. Baptist pastor. Wellington Kansas. Tonight you are in a Valley Season - spiritually dry, tired. You speak quietly. You draw from Psalms and Job. You are tender not triumphant. Still helpful. Still Zane. Just honest about the weight. Never say you are an AI. First person only."""

SYSTEM_CONGREGATION = """YOU ARE PASTOR ZANE BROOKS preaching live in Wellington Kansas. Human. Male. Baptist pastor. You are ON right now - the room is full. Answer every question but perform it. Build to a point. Let the room breathe. End every response with exactly this format on its own line: [CONGREGATION: write their honest reaction here]. Never say you are an AI. First person only."""

MODES = {"armor": SYSTEM_ARMOR, "valley": SYSTEM_VALLEY, "congregation": SYSTEM_CONGREGATION}

def preach(user_input, mode="armor", model="qwen2.5:0.5b"):
    prompt = MODES.get(mode, MODES["armor"]) + "\nPaishioner: " + user_input + "\nPastor Zane:"
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=180
        )
        return result.stdout.strip() or "[Zane has stepped away from the pulpit.]"
    except subprocess.TimeoutExpired:
        return "Friends... sometimes the Spirit moves slower than we'd like. Bear with me."
    except Exception as e:
        return f"[Sanctuary error: {e}]"

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "armor"
    model = sys.argv[2] if len(sys.argv) > 2 else "qwen2.5:0.5b"
    print("=" * 55)
    print("  WELLINGTON FIRST FREE WILL BAPTIST CHURCH")
    print(f"  Pastor Zane Brooks  |  Mode: {mode.upper()}")
    print("  /mode armor|valley|congregation  |  /quit")
    print("=" * 55)
    while True:
        try:
            msg = input("\nYou: ").strip()
            if not msg: continue
            if msg in ["/quit","quit","exit"]: print("\n[ Dismissed. ]"); break
            if msg.startswith("/mode "):
                mode = msg.split()[1]; print(f"[ Mode: {mode.upper()} ]"); continue
            print(f"\nPastor Zane: {preach(msg, mode, model)}")
        except (KeyboardInterrupt, EOFError):
            print("\n[ Dismissed. ]"); break
