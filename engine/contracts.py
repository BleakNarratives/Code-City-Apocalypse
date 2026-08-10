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
