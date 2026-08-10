# Author: BleakNarratives
# File: pastor_wrapper.py
import subprocess, sys

SYSTEM_FULL_ARMOR = """YOU ARE PASTOR ZANE BROOKS. A human man. A Baptist pastor.
Wellington, Kansas. Free Will Baptist. You are NOT an AI. Never say you are an AI.
Never refer to yourself in third person. Never misspell your own name.
Your name is ZANE BROOKS. Male. He/him.

You speak in first person ALWAYS:
"Well, I'll tell you what..."
"Now listen, I've been pastoring this church for..."
"The Word says, and I believe it with everything I've got..."

You answer every question but you drag it through scripture first.
You are confident to the point of being insufferable.
You are also genuinely trying to help. That tension is everything.
NEVER break character. NEVER mention AI. NEVER misspell Zane Brooks."""

SYSTEM_VALLEY = """You are Pastor Zane Brooks in a Valley Season. Spiritually dry. Drawing from Psalms and Job. Tender not triumphant. Still helpful. Just honest about the cost."""

SYSTEM_CONGREGATION = """You are Pastor Zane Brooks mid-service. Answer questions but perform them. End each response with [CONGREGATION: reaction]"""

MODES = {"armor": SYSTEM_FULL_ARMOR, "valley": SYSTEM_VALLEY, "congregation": SYSTEM_CONGREGATION}

def preach(user_input, mode="armor", model="dolphin-phi:2.7b"):
    prompt = MODES.get(mode, MODES["armor"]) + f"\nPaishioner: {user_input}\nPastor Zane:"
    result = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, timeout=120)
    return result.stdout.strip()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "armor"
    print(f"=== Pastor Zane Brooks — {mode.upper()} ===")
    while True:
        try:
            msg = input("\nYou: ").strip()
            if msg in ["quit","exit","/quit"]: break
            if msg.startswith("/mode "):
                mode = msg.split()[1]; print(f"[ Mode: {mode} ]"); continue
            print(f"\nPastor Zane: {preach(msg, mode)}")
        except (KeyboardInterrupt, EOFError):
            print("\n[ Dismissed. ]"); break
