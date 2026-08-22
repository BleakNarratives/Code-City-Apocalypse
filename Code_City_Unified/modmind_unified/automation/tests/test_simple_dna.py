
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: automation_dna, json, pytest
# ROLE: Simple test suite for DNA Process functionality
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Test (0)
# [/DNA_TAG]

"""
Simple test suite for DNA Process functionality
Tests basic creation, mutation, and serialization
"""
import json
import pytest
from automation_dna.core.dna_process import ProcessDNA, StepDNA, ConnectionDNA, ProcessType


class TestSimpleDNA:
    """Simple tests for DNA functionality"""
    
    def test_step_creation(self):
        """Test basic step creation"""
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        
        assert step.step_type == "action"
        assert step.name == "Test Step"
        assert step.description == "A test step"
        assert step.dna_id is not None
        assert step.parameters == {}
        assert step.conditions == []
    
    def test_step_with_parameters(self):
        """Test step with parameters"""
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        step.parameters = {"param1": 1.0, "param2": "value"}
        
        assert step.parameters["param1"] == 1.0
        assert step.parameters["param2"] == "value"
    
    def test_step_serialization(self):
        """Test step serialization to dict"""
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        step.parameters = {"test": "value"}
        
        step_dict = step.to_dict()
        
        assert step_dict["step_type"] == "action"
        assert step_dict["name"] == "Test Step"
        assert step_dict["parameters"] == {"test": "value"}
        assert "dna_id" in step_dict
    
    def test_step_deserialization(self):
        """Test step deserialization from dict"""
        step_data = {
            "step_type": "action",
            "name": "Test Step",
            "description": "A test step",
            "parameters": {"test": "value"},
            "conditions": [],
            "dna_id": "test_id",
            "created_at": "2024-01-01T00:00:00",
            "version": "1.0",
            "generation": 1,
            "fitness_score": 0.0,
            "mutations": []
        }
        
        step = StepDNA.from_dict(step_data)
        
        assert step.step_type == "action"
        assert step.name == "Test Step"
        assert step.parameters == {"test": "value"}
    
    def test_connection_creation(self):
        """Test basic connection creation"""
        conn = ConnectionDNA(
            source_step_id="step_1",
            target_step_id="step_2",
            condition="success"
        )
        
        assert conn.source_step_id == "step_1"
        assert conn.target_step_id == "step_2"
        assert conn.condition == "success"
        assert conn.transition_probability == 1.0
    
    def test_process_creation(self):
        """Test basic process creation"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        assert process.process_type == ProcessType.CUSTOM
        assert process.name == "Test Process"
        assert process.description == "A test process"
        assert process.steps == []
        assert process.connections == []
    
    def test_process_with_steps(self):
        """Test process with steps and connections"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        step1 = StepDNA(
            step_type="start",
            name="Start",
            description="Initial step"
        )
        
        step2 = StepDNA(
            step_type="action",
            name="Action",
            description="Action step"
        )
        
        conn = ConnectionDNA(
            source_step_id="step_1",
            target_step_id="step_2",
            condition="success"
        )
        
        process.add_step(step1)
        process.add_step(step2)
        process.add_connection(conn)
        
        assert len(process.steps) == 2
        assert len(process.connections) == 1
        assert process.steps[0].name == "Start"
        assert process.steps[1].name == "Action"
    
    def test_process_serialization(self):
        """Test process serialization to JSON"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        process.add_step(step)
        
        json_str = process.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["name"] == "Test Process"
        assert parsed["process_type"] == "custom"
        assert len(parsed["steps"]) == 1
    
    def test_process_deserialization(self):
        """Test process deserialization from JSON"""
        process_data = {
            "process_type": "custom",
            "name": "Test Process",
            "description": "A test process",
            "steps": [],
            "connections": [],
            "metadata": {},
            "dna_id": "test_id",
            "created_at": "2024-01-01T00:00:00",
            "version": "1.0",
            "generation": 1,
            "fitness_score": 0.0,
            "mutations": []
        }
        
        process = ProcessDNA.from_json(json.dumps(process_data))
        
        assert process.name == "Test Process"
        assert process.process_type == ProcessType.CUSTOM
    
    def test_process_mutation(self):
        """Test process mutation"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        step.parameters = {"param1": 1.0}
        process.add_step(step)
        
        # Create mutated version
        mutated = process.mutate()
        
        assert mutated.name == "Test Process (Mutated)"
        assert mutated.process_type == ProcessType.CUSTOM
        assert len(mutated.steps) == 1
        assert mutated.generation == 2
    
    def test_process_cloning(self):
        """Test process cloning"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        process.add_step(step)
        
        cloned = process.clone()
        
        assert cloned.name == process.name
        assert cloned.process_type == process.process_type
        assert len(cloned.steps) == len(process.steps)
        assert cloned is not process
        assert cloned.steps[0] is not process.steps[0]
    
    def test_process_fitness_calculation(self):
        """Test process fitness calculation"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        # Add steps with different parameters
        step1 = StepDNA(
            step_type="action",
            name="Good Step",
            description="A good step"
        )
        step1.parameters = {
            "success_rate": 0.9,
            "efficiency": 0.8,
            "cost": 5.0,
            "speed": 7.0
        }
        
        process.add_step(step1)
        
        fitness = process.calculate_fitness()
        
        # Fitness should be a float between 0 and 1
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_process_validation(self):
        """Test process validation"""
        # Valid process
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Test Process",
            description="A test process"
        )
        
        step = StepDNA(
            step_type="action",
            name="Test Step",
            description="A test step"
        )
        process.add_step(step)
        
        assert process.validate() == True
        
        # Invalid process (no steps)
        empty_process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Empty Process",
            description="An empty process"
        )
        
        assert empty_process.validate() == False


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_process(self):
        """Test process with no steps"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Empty Process",
            description="An empty process"
        )
        
        assert len(process.steps) == 0
        assert len(process.connections) == 0
        assert process.calculate_fitness() == 0.0
        assert process.validate() == False
    
    def test_process_with_multiple_steps(self):
        """Test process with multiple steps"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Multi-Step Process",
            description="A process with multiple steps"
        )
        
        # Add multiple steps
        for i in range(5):
            step = StepDNA(
                step_type="action",
                name=f"Step {i+1}",
                description=f"Step number {i+1}"
            )
            step.parameters = {"order": i+1}
            process.add_step(step)
        
        assert len(process.steps) == 5
        assert process.steps[0].name == "Step 1"
        assert process.steps[4].name == "Step 5"
    
    def test_process_with_complex_parameters(self):
        """Test process with complex parameter structures"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Complex Process",
            description="A process with complex parameters"
        )
        
        step = StepDNA(
            step_type="action",
            name="Complex Step",
            description="A step with complex parameters"
        )
        
        # Add complex parameters
        step.parameters = {
            "nested": {
                "level1": {
                    "level2": "value"
                }
            },
            "list": [1, 2, 3, 4, 5],
            "mixed": [
                {"key": "value"},
                [1, 2, 3],
                "string"
            ]
        }
        
        process.add_step(step)
        
        # Should serialize and deserialize correctly
        json_str = process.to_json()
        parsed = json.loads(json_str)
        
        assert "nested" in parsed["steps"][0]["parameters"]
        assert "list" in parsed["steps"][0]["parameters"]
        assert "mixed" in parsed["steps"][0]["parameters"]
