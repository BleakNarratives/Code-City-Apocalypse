# Author: BleakNarratives
# File: consumption_protocol.py
# Path: ~/Code_City_Unified/modmind_unified/src/consumption_protocol.py

class ConsumptionMixin:
    """
    Twoie Protocol: absorb_agent() extracts all public methods from
    a target agent and binds them to self. Target is then deleted.
    """
    def absorb_agent(self, target_agent):
        absorbed = []
        for attr_name in dir(target_agent):
            if not attr_name.startswith('_') and callable(getattr(target_agent, attr_name)):
                skill = getattr(target_agent, attr_name)
                setattr(self, attr_name, skill)
                absorbed.append(attr_name)
        role = getattr(target_agent, 'role', type(target_agent).__name__)
        del target_agent
        print(f"[Twoie] Consumed '{role}'. Skills absorbed: {absorbed}")
        return absorbed
