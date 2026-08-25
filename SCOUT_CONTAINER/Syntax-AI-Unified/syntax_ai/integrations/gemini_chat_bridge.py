import logging

# gemini_chat_bridge.py - The interface for Gemini (Clipboard OSF handler)

class GeminiChatBridge:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.status = "Monitoring clipboard..."
        logging.info(f">> Gemini Bridge Initialized. {self.status}")

    def start(self):
        # Activation logic goes here (e.g., thread for listening)
        pass

    def send_context_to_gemini(self, context_summary):
        """
        The outbound security filter (OSF) is applied here via the Orchestrator.
        """
        logging.info(f"📦 Preparing context for OSF: {context_summary[:20]}...")
        # The Orchestrator handles the CJ-Encode and Termux clipboard set
        self.orchestrator.external_api_call('clipboard_set', context_summary)

