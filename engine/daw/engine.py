
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: UnifiedCodeCity
# ROLE: DAWEngine class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

from UnifiedCodeCity.core.music_hive_service import MusicHiveService
from UnifiedCodeCity.engine.contracts import SynthesisProvider
from UnifiedCodeCity.engine.daw.graph_informer import GraphInformer

class DAWEngine:
    def __init__(self, synthesizer: SynthesisProvider, loomy_client):
        self.hive = MusicHiveService()
        self.synthesizer = synthesizer
        self.informer = GraphInformer(loomy_client)

    def generate_beat(self, prompt: str):
        state = self.hive.get_state()
        # Dynamically modulate prompt based on graph traversal
        next_key = self.informer.get_next_harmonic_step(state.get('key'))
        informed_prompt = f"{prompt}, modulate to {next_key}"
        
        return self.synthesizer.synthesize(informed_prompt, state)
