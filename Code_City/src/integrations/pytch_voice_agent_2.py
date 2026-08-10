# pytch_voice_agent.py - The Action Layer (Pytch Integration)

class PytchVoiceAgent:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.COMMAND_MAP = {"DEPLOY_REFACTOR": self._deploy_refactor}

    def receive_dispatch(self, validated_command, target_component=None):
        if validated_command in self.COMMAND_MAP:
            action_method = self.COMMAND_MAP[validated_command]
            action_method(target_component)
        else:
            print(f"🚨 WARNING: Unrecognized command received: {validated_command}")

    def _deploy_refactor(self, target):
        print("🔥 ACTION: Refactor command received. Launching Arsonist class...")

    def start(self):
        pass

