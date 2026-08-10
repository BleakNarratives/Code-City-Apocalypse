# pytch_voice_agent.py - The Action Layer (FINAL VERIFIED VERSION with SORT_LOOSIES)

class PytchVoiceAgent:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.COMMAND_MAP = {
            "DEPLOY_REFACTOR": self._deploy_refactor,
            "STATUS_REPORT": self._status_report,
            "SORT_LOOSIES": self._sort_loosies # CRITICAL FIX: The command is now registered
        }

    def receive_dispatch(self, validated_command, target_component=None):
        if validated_command in self.COMMAND_MAP:
            action_method = self.COMMAND_MAP[validated_command]
            action_method(target_component)
        else:
            print(f"🚨 WARNING: Unrecognized command received: {validated_command}")

    def _deploy_refactor(self, target):
        print("🔥 ACTION: Refactor command received. Launching Arsonist class...")

    def _status_report(self, target):
        summary = self.orchestrator.get_city_health_summary()
        self.orchestrator.get_component('Gemini_Chat_Bridge').send_context_to_gemini(summary)
        print("✅ Status report dispatched via OSF.")

    def _sort_loosies(self, target):
        """Triggers the file organizer to sort the root_2025/loosies directory."""
        print("📁 DISPATCH: Triggering Loosie Sorter...")
        sorter = self.orchestrator.get_component('Loosie_Sorter')
        if sorter:
            sorter.sort_loosies()
        else:
            print("🚨 ERROR: Loosie Sorter component not found in registry.")

    def start(self):
        pass

