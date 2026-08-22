
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: datetime, enum, hashlib, json, logging, random, typing
# ROLE: 🧬 Automation DNA - Core Process Representation
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import logging

#!/usr/bin/env python3
"""
🧬 Automation DNA - Core Process Representation
Represents business processes as evolvable genetic code
"""

import json
import hashlib
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class ProcessType(Enum):
    """Types of business processes"""
    CUSTOMER_ONBOARDING = "customer_onboarding"
    SALES_PIPELINE = "sales_pipeline"
    SUPPORT_TICKET = "support_ticket"
    INVOICING = "invoicing"
    INVENTORY_MANAGEMENT = "inventory_management"
    HR_ONBOARDING = "hr_onboarding"
    MARKETING_CAMPAIGN = "marketing_campaign"
    DATA_PROCESSING = "data_processing"
    REPORTING = "reporting"
    CUSTOM = "custom"

class DNABase:
    """Base class for all DNA components"""
    
    def __init__(self, dna_id: Optional[str] = None):
        self.dna_id = dna_id or self.generate_dna_id()
        self.created_at = datetime.now().isoformat()
        self.version = "1.0"
        self.generation = 1
        self.fitness_score = 0.0
        self.mutations = []
    
    def generate_dna_id(self) -> str:
        """Generate unique DNA identifier"""
        timestamp = datetime.now().timestamp()
        random_hash = hashlib.sha256(str(random.random()).encode()).hexdigest()[:8]
        return f"DNA-{timestamp}-{random_hash}"
    
    def mutate(self) -> 'DNABase':
        """Create a mutated version of this DNA"""
        raise NotImplementedError("Subclasses must implement mutate()")
    
    def breed(self, partner: 'DNABase') -> 'DNABase':
        """Breed with another DNA to create offspring"""
        raise NotImplementedError("Subclasses must implement breed()")
    
    def calculate_fitness(self, metrics: Dict[str, float]) -> float:
        """Calculate fitness score based on performance metrics"""
        raise NotImplementedError("Subclasses must implement calculate_fitness()")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DNA to dictionary for serialization"""
        return {
            "dna_id": self.dna_id,
            "type": self.__class__.__name__,
            "created_at": self.created_at,
            "version": self.version,
            "generation": self.generation,
            "fitness_score": self.fitness_score,
            "mutations": self.mutations
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'DNABase':
        """Create DNA from dictionary"""
        raise NotImplementedError("Subclasses must implement from_dict()")

class ProcessDNA(DNABase):
    """Represents a complete business process as DNA"""
    
    def __init__(self, 
                 process_type: ProcessType, 
                 name: str, 
                 description: str = "",
                 dna_id: Optional[str] = None):
        super().__init__(dna_id)
        self.process_type = process_type
        self.name = name
        self.description = description
        self.steps: List['StepDNA'] = []
        self.connections: List['ConnectionDNA'] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_step(self, step: 'StepDNA'):
        """Add a step to the process"""
        self.steps.append(step)
    
    def add_connection(self, connection: 'ConnectionDNA'):
        """Add a connection between steps"""
        self.connections.append(connection)
    
    def mutate(self) -> 'ProcessDNA':
        """Create a mutated version of this process"""
        # Create a copy
        mutated = ProcessDNA(
            process_type=self.process_type,
            name=f"{self.name} (Mutated)",
            description=self.description,
            dna_id=None  # Generate new ID
        )
        
        # Copy steps with potential mutations
        for step in self.steps:
            mutated_step = step.mutate()
            mutated.add_step(mutated_step)
        
        # Copy connections (might need adjustment based on mutated steps)
        for conn in self.connections:
            mutated.add_connection(conn)
        
        # Record mutation
        mutation_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "random_mutation",
            "description": "Random mutation of process steps"
        }
        mutated.mutations.append(mutation_record)
        mutated.generation = self.generation + 1
        
        return mutated
    
    def breed(self, partner: 'ProcessDNA') -> 'ProcessDNA':
        """Breed with another process to create hybrid offspring"""
        if self.process_type != partner.process_type:
            raise ValueError("Cannot breed different process types")
        
        # Create hybrid process
        hybrid = ProcessDNA(
            process_type=self.process_type,
            name=f"{self.name} × {partner.name} (Hybrid)",
            description=f"Hybrid of {self.name} and {partner.name}",
            dna_id=None  # Generate new ID
        )
        
        # Combine steps from both parents
        # Simple approach: alternate steps
        all_steps = []
        for i in range(max(len(self.steps), len(partner.steps))):
            if i < len(self.steps):
                all_steps.append(self.steps[i])
            if i < len(partner.steps):
                all_steps.append(partner.steps[i])
        
        # Add all steps to hybrid
        for step in all_steps:
            hybrid.add_step(step)
        
        # Record breeding
        breeding_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "breeding",
            "parent1": self.dna_id,
            "parent2": partner.dna_id,
            "description": f"Hybrid of {self.name} and {partner.name}"
        }
        hybrid.mutations.append(breeding_record)
        hybrid.generation = max(self.generation, partner.generation) + 1
        
        return hybrid
    
    def calculate_fitness(self, metrics: Dict[str, float]) -> float:
        """Calculate fitness score based on performance metrics"""
        # Empty processes have zero fitness
        if not self.steps:
            self.fitness_score = 0.0
            return self.fitness_score
        
        # Simple fitness calculation based on common metrics
        efficiency = metrics.get('efficiency', 0.5)  # 0-1 scale
        success_rate = metrics.get('success_rate', 0.8)  # 0-1 scale
        cost = metrics.get('cost', 1.0)  # Normalized cost (lower is better)
        speed = metrics.get('speed', 0.7)  # 0-1 scale
        
        # Weighted fitness score
        self.fitness_score = (
            efficiency * 0.3 +
            success_rate * 0.4 +
            (1 - cost) * 0.2 +
            speed * 0.1
        )
        
        return self.fitness_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert process DNA to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "process_type": self.process_type.value,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "connections": [conn.to_dict() for conn in self.connections],
            "metadata": self.metadata
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessDNA':
        """Create process DNA from dictionary"""
        process = cls(
            process_type=ProcessType(data['process_type']),
            name=data['name'],
            description=data.get('description', ''),
            dna_id=data['dna_id']
        )
        
        # Restore properties
        process.created_at = data['created_at']
        process.version = data['version']
        process.generation = data['generation']
        process.fitness_score = data['fitness_score']
        process.mutations = data['mutations']
        process.metadata = data.get('metadata', {})
        
        # Restore steps and connections
        for step_data in data.get('steps', []):
            step = StepDNA.from_dict(step_data)
            process.add_step(step)
            
        for conn_data in data.get('connections', []):
            conn = ConnectionDNA.from_dict(conn_data)
            process.add_connection(conn)
        
        return process

class StepDNA(DNABase):
    """Represents an individual step in a process"""
    
    def __init__(self, 
                 step_type: str,
                 name: str,
                 description: str = "",
                 dna_id: Optional[str] = None):
        super().__init__(dna_id)
        self.step_type = step_type
        self.name = name
        self.description = description
        self.parameters: Dict[str, Any] = {}
        self.conditions: List[Dict[str, Any]] = []
    
    def mutate(self) -> 'StepDNA':
        """Create a mutated version of this step"""
        mutated = StepDNA(
            step_type=self.step_type,
            name=f"{self.name} (Mutated)",
            description=self.description,
            dna_id=None  # Generate new ID
        )
        
        # Copy parameters with potential mutations
        mutated.parameters = self.parameters.copy()
        
        # Randomly mutate one parameter
        if self.parameters:
            param_to_mutate = random.choice(list(self.parameters.keys()))
            original_value = self.parameters[param_to_mutate]
            
            # Simple mutation logic based on type
            if isinstance(original_value, (int, float)):
                mutated.parameters[param_to_mutate] = original_value * random.uniform(0.8, 1.2)
            elif isinstance(original_value, str):
                mutated.parameters[param_to_mutate] = f"{original_value} (modified)"
            elif isinstance(original_value, bool):
                mutated.parameters[param_to_mutate] = not original_value
        
        # Record mutation
        mutation_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "parameter_mutation",
            "parameter": param_to_mutate,
            "original_value": original_value,
            "new_value": mutated.parameters.get(param_to_mutate)
        }
        mutated.mutations.append(mutation_record)
        mutated.generation = self.generation + 1
        
        return mutated
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step DNA to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "step_type": self.step_type,
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "conditions": self.conditions
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StepDNA':
        """Create step DNA from dictionary"""
        step = cls(
            step_type=data['step_type'],
            name=data['name'],
            description=data.get('description', ''),
            dna_id=data['dna_id']
        )
        
        # Restore properties
        step.created_at = data['created_at']
        step.version = data['version']
        step.generation = data['generation']
        step.fitness_score = data['fitness_score']
        step.mutations = data['mutations']
        step.parameters = data['parameters']
        step.conditions = data['conditions']
        
        return step

class ConnectionDNA(DNABase):
    """Represents a connection between process steps"""
    
    def __init__(self, 
                 source_step_id: str,
                 target_step_id: str,
                 condition: str = "always",
                 dna_id: Optional[str] = None):
        super().__init__(dna_id)
        self.source_step_id = source_step_id
        self.target_step_id = target_step_id
        self.condition = condition
        self.transition_probability = 1.0
    
    def mutate(self) -> 'ConnectionDNA':
        """Create a mutated version of this connection"""
        mutated = ConnectionDNA(
            source_step_id=self.source_step_id,
            target_step_id=self.target_step_id,
            condition=self.condition,
            dna_id=None  # Generate new ID
        )
        
        # Mutate transition probability
        mutated.transition_probability = max(0.1, min(1.0, self.transition_probability * random.uniform(0.8, 1.2)))
        
        # Record mutation
        mutation_record = {
            "timestamp": datetime.now().isoformat(),
            "type": "probability_mutation",
            "original_probability": self.transition_probability,
            "new_probability": mutated.transition_probability
        }
        mutated.mutations.append(mutation_record)
        mutated.generation = self.generation + 1
        
        return mutated
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert connection DNA to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "source_step_id": self.source_step_id,
            "target_step_id": self.target_step_id,
            "condition": self.condition,
            "transition_probability": self.transition_probability
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConnectionDNA':
        """Create connection DNA from dictionary"""
        conn = cls(
            source_step_id=data['source_step_id'],
            target_step_id=data['target_step_id'],
            condition=data.get('condition', 'always'),
            dna_id=data['dna_id']
        )
        
        # Restore properties
        conn.created_at = data['created_at']
        conn.version = data['version']
        conn.generation = data['generation']
        conn.fitness_score = data['fitness_score']
        conn.mutations = data['mutations']
        conn.transition_probability = data['transition_probability']
        
        return conn

# Example usage
if __name__ == "__main__":
    logging.info("🧬 Automation DNA Core Engine - Initialized!")
    
    # Create a simple customer onboarding process
    onboarding = ProcessDNA(
        process_type=ProcessType.CUSTOMER_ONBOARDING,
        name="Basic Customer Onboarding",
        description="Simple 3-step customer onboarding process"
    )
    
    # Add steps
    step1 = StepDNA(
        step_type="form",
        name="Collect Customer Info",
        description="Gather basic customer information"
    )
    step1.parameters = {"fields": ["name", "email", "phone"], "timeout": 300}
    
    step2 = StepDNA(
        step_type="verification",
        name="Verify Email",
        description="Send verification email and confirm"
    )
    step2.parameters = {"email_template": "welcome", "retries": 3}
    
    step3 = StepDNA(
        step_type="activation",
        name="Activate Account",
        description="Enable customer account access"
    )
    step3.parameters = {"default_role": "customer", "welcome_message": True}
    
    onboarding.add_step(step1)
    onboarding.add_step(step2)
    onboarding.add_step(step3)
    
    # Add connections
    conn1 = ConnectionDNA(step1.dna_id, step2.dna_id, "success")
    conn2 = ConnectionDNA(step2.dna_id, step3.dna_id, "verified")
    onboarding.add_connection(conn1)
    onboarding.add_connection(conn2)
    
    logging.info(f"✅ Created process: {onboarding.name}")
    logging.info(f"📊 DNA ID: {onboarding.dna_id}")
    logging.info(f"🔗 Steps: {len(onboarding.steps)}")
    logging.info(f"🔄 Connections: {len(onboarding.connections)}")
    
    # Calculate fitness
    metrics = {
        "efficiency": 0.85,
        "success_rate": 0.92,
        "cost": 0.3,
        "speed": 0.78
    }
    fitness = onboarding.calculate_fitness(metrics)
    logging.info(f"💪 Fitness Score: {fitness:.3f}")
    
    # Create a mutation
    mutated_process = onboarding.mutate()
    logging.info(f"🧬 Created mutation: {mutated_process.name}")
    logging.info(f"📊 New DNA ID: {mutated_process.dna_id}")
    logging.info(f"🔢 Generation: {mutated_process.generation}")
    
    # Save to file
    with open("onboarding_process.json", "w") as f:
        json.dump(onboarding.to_dict(), f, indent=2)
    
    logging.info("💾 Saved process DNA to onboarding_process.json")