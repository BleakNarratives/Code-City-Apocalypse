#!/usr/bin/env python3
import subprocess
import threading
import time

PERSONAS = [
    {"name": "CEO", "color": "33"},      # yellow
    {"name": "ADVERSARY", "color": "31"}, # red
    {"name": "ARCHITECT", "color": "34"}, # blue
    {"name": "CMO", "color": "32"},       # green
    {"name": "THREAT", "color": "35"},    # magenta
    {"name": "RAP GENIUS", "color": "33"},# yellow
    {"name": "PYTCH", "color": "35"},     # magenta
    {"name": "TWOIE", "color": "36"},     # cyan
]

def color_text(text, code):
    return f"\033[{code}m{text}\033[0m"

def persona_response(persona, idea):
    # Replace with actual Ollama call
    responses = [
        "That's not a business, it's a feature.",
        "Who pays for this? Be specific.",
        "The numbers don't add up.",
        "Interesting. Wrong market.",
        "Your competitors will crush you.",
        "yo this could actually work tho",
        "The spiral approves.",
        "Show me the TAM or shut up."
    ]
    import random
    time.sleep(random.uniform(1, 3))
    print(f"{color_text(persona['name'].ljust(12), persona['color'])} {random.choice(responses)}")

def main():
    print("\033[2J\033[H")  # clear screen
    print("┌─────────────────────────────────────────────┐")
    print("│ VERTICAL AI BOARDROOM // ARGUE MODE         │")
    print("├─────────────────────────────────────────────┤")
    
    while True:
        idea = input("\033[36m> your idea:\033[0m ")
        if not idea:
            continue
            
        print("├─────────────────────────────────────────────┤")
        
        threads = []
        for p in PERSONAS:
            t = threading.Thread(target=persona_response, args=(p, idea))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(0.3)  # stagger them a bit
        
        for t in threads:
            t.join()
        
        print("└─────────────────────────────────────────────┘")

if __name__ == "__main__":
    main()