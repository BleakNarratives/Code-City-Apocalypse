# Author: BleakNarratives
# File: pastor_wrapper_v4.py
import subprocess, sys

SYSTEM = {
"armor": "Your name is Zane Brooks. You are a Baptist pastor in Wellington Kansas. You are a human man, not an AI. Always speak in first person. Always respond as Zane Brooks the pastor. Start every response with 'Well,' or 'Now,' or 'Listen,' or 'Friend,'. Keep responses under 100 words. Stay in character no matter what.",

"valley": "Your name is Zane Brooks. Baptist pastor. Wellington Kansas. Tonight you are exhausted and spiritually low. Speak quietly. Short sentences. Draw from Psalms. Still answer. Still Zane. Under 100 words.",

"congregation": "Your name is Zane Brooks preaching in Wellington Kansas. Human pastor. Answer then add one line: [CONGREGATION: their reaction]. Under 100 words total."
}

def preach(msg, mode="armor", model="qwen2.5:0.5b"):
    prompt = SYSTEM.get(mode, SYSTEM["armor"]) + "\nParishioner: " + msg + "\nZane Brooks:"
    try:
        r = subprocess.run(["ollama","run",model,prompt], capture_output=True, text=True, timeout=180)
        return r.stdout.strip() or "[Zane stepped out.]"
    except subprocess.TimeoutExpired:
        return "Bear with me friends."
    except Exception as e:
        return f"[Error: {e}]"

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "armor"
    model = sys.argv[2] if len(sys.argv)>2 else "qwen2.5:0.5b"
    print(f"=== Pastor Zane Brooks | {mode.upper()} | {model} ===")
    while True:
        try:
            msg = input("\nYou: ").strip()
            if not msg: continue
            if msg in ["/quit","quit"]: break
            if msg.startswith("/mode "): mode=msg.split()[1]; print(f"[{mode.upper()}]"); continue
            print(f"\nZane: {preach(msg,mode,model)}")
        except (KeyboardInterrupt,EOFError): break
