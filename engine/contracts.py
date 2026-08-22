
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: abc
# ROLE: Generates audio data based on prompt and hive constraints.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

from abc import ABC, abstractmethod

class SynthesisProvider(ABC):
    @abstractmethod
    def synthesize(self, prompt: str, hive_state: dict) -> bytes:
        """Generates audio data based on prompt and hive constraints."""
        pass

class AudioInputProvider(ABC):
    @abstractmethod
    async def listen(self, callback: callable):
        """Monitors audio input and triggers callback on vocal detection."""
        pass
