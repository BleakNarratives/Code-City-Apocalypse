# gemini_bridge.py - EquiNex Real-Time Chat Integration

import time

class GeminiChatBridge:
    def __init__(self, orchestrator, polling_interval=3):
        self.orchestrator = orchestrator
        self.interval = polling_interval
        self.last_content = ""
        self.known_messages = set()

    def get_clipboard_content(self):
        return self.orchestrator.external_api_call('clipboard_get')

    def check_for_new_data(self):
        current_content = self.get_clipboard_content()
        if current_content and current_content != self.last_content:
            if current_content not in self.known_messages:
                self.known_messages.add(current_content)
                self.last_content = current_content
                return current_content
        return None

    def process_chat_stream(self):
        print(">> Gemini Bridge polling thread started. Copy text to trigger.")
        # Note: This conceptual loop runs infinitely in the script.
        while True: 
            new_message = self.check_for_new_data()
            if new_message:
                print(f"[{self.orchestrator.get_timestamp()}] NEW MESSAGE DETECTED. Processing...")
                extracted_data = self.orchestrator.trigger_extraction(new_message)
                if extracted_data:
                    # Uses the CORRECTED Orchestrator method to route command
                    pytch_agent = self.orchestrator.get_component('Pytch_Voice_Agent')
                    if pytch_agent:
                        pytch_agent.receive_dispatch(extracted_data)

            time.sleep(self.interval)

    def send_context_to_gemini(self, context_summary):
        output = f"[Code City Status] {context_summary}"
        self.orchestrator.external_api_call('clipboard_set', output)

    def start(self):
        self.process_chat_stream() 
        
