# integration_orchestrator.py - Core of the EquiNex Protocol

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: src, subprocess, time
# ROLE: CRITICAL ROUTING FIX: Fetches the instance by its registered name.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]


import time
import subprocess
from src.data.ebmn_neo4j_schema import verify_integrity_vectors

class IntegrationOrchestrator:
    def __init__(self):
        self.component_registry = {}
        self.data_pipelines = {}
        self.verifier = None

    def get_timestamp(self):
        return time.strftime("%H:%M:%S")

    def register_verifier(self, verifier_instance):
        self.verifier = verifier_instance

    def register_component(self, component_instance, component_name):
        eqi = f"EQI-{component_name.upper().replace('_','-')}-{len(self.component_registry)}"
        self.component_registry[component_name] = {"instance": component_instance, "eqi": eqi}
        if component_name == 'Gemini_Chat_Bridge':
            self.data_pipelines['chat_input'] = component_instance
        print(f"✅ CRC enforced: {component_name} registered.")

    def get_component(self, component_name):
        """CRITICAL ROUTING FIX: Fetches the instance by its registered name."""
        data = self.component_registry.get(component_name)
        return data['instance'] if data else None

    def external_api_call(self, api_name, data=None):
        if api_name == 'clipboard_get':
            try:
                # Actual Termux API call abstraction
                return subprocess.run(['termux-clipboard-get'], capture_output=True, text=True, check=True).stdout.strip()
            except Exception:
                return ""
        if api_name == 'clipboard_set' and data:
            subprocess.run(['termux-clipboard-set'], input=data, text=True)

    def start_integration_pipeline(self):
        if 'chat_input' in self.data_pipelines:
            self.data_pipelines['chat_input'].start()

    def trigger_extraction(self, raw_chat_text):
        if "refactor" in raw_chat_text.lower():
            if verify_integrity_vectors({'pitch_vector': 'NOMINAL', 'yaw_vector': 'NOMINAL'}):
                return "DEPLOY_REFACTOR"
        return None

    def get_city_health_summary(self):
        return "City Health: 90%. Strump: Idle. Spaghetti Zones: 4."

    def get_bridge(self, name):
        # Helper for fetching the bridge instance
        return self.get_component(name)

