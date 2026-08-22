
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: automation_dna, json, pytest
# ROLE: Working test suite for DNA Process functionality
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Test (0)
# [/DNA_TAG]

"""
Working test suite for DNA Process functionality
Tests basic creation, mutation, and serialization using actual DNA class methods
"""
import json
import pytest
from automation_dna.core.dna_process import ProcessDNA, StepDNA, ConnectionDNA, ProcessType


class TestWorkingDNA:
    """Working tests for DNA functionality using actual class methods"""
    
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
        """Test process serialization to dict"""
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
        
        process_dict = process.to_dict()
        
        assert process_dict["name"] == "Test Process"
        assert process_dict["process_type"] == "custom"
        assert len(process_dict["steps"]) == 1
        assert process_dict["steps"][0]["name"] == "Test Step"
    
    def test_process_deserialization(self):
        """Test process deserialization from dict"""
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
        
        process = ProcessDNA.from_dict(process_data)
        
        assert process.name == "Test Process"
        assert process.process_type == ProcessType.CUSTOM
        assert len(process.steps) == 0
    
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
    
    def test_process_fitness_calculation(self):
        """Test process fitness calculation with metrics"""
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
        
        # Calculate fitness with metrics
        metrics = {
            "success_rate": 0.4,
            "efficiency": 0.3,
            "cost": 0.2,
            "speed": 0.1
        }
        
        fitness = process.calculate_fitness(metrics)
        
        # Fitness should be a float between 0 and 1
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
    
    def test_process_with_multiple_steps(self):
        """Test process with multiple steps"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Multi-Step Process",
            description="A process with multiple steps"
        )
        
        # Add multiple steps
        for i in range(3):
            step = StepDNA(
                step_type="action",
                name=f"Step {i+1}",
                description=f"Step number {i+1}"
            )
            step.parameters = {"order": i+1}
            process.add_step(step)
        
        assert len(process.steps) == 3
        assert process.steps[0].name == "Step 1"
        assert process.steps[2].name == "Step 3"
    
    def test_process_json_roundtrip(self):
        """Test process JSON serialization roundtrip"""
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
        step.parameters = {"test": "value"}
        process.add_step(step)
        
        # Convert to dict, then to JSON, then back
        process_dict = process.to_dict()
        json_str = json.dumps(process_dict)
        parsed_dict = json.loads(json_str)
        restored_process = ProcessDNA.from_dict(parsed_dict)
        
        assert restored_process.name == process.name
        assert restored_process.process_type == process.process_type
        assert len(restored_process.steps) == len(process.steps)
        assert restored_process.steps[0].name == process.steps[0].name
    
    def test_empty_process(self):
        """Test process with no steps"""
        process = ProcessDNA(
            process_type=ProcessType.CUSTOM,
            name="Empty Process",
            description="An empty process"
        )
        
        assert len(process.steps) == 0
        assert len(process.connections) == 0
        
        # Calculate fitness with metrics (should handle empty process)
        metrics = {"success_rate": 0.5, "efficiency": 0.5}
        fitness = process.calculate_fitness(metrics)
        
        # Empty process should have zero fitness
        assert fitness == 0.0
    
    def test_process_cloning_behavior(self):
        """Test that process mutation creates independent copies"""
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
        step.parameters = {"value": 1.0}
        process.add_step(step)
        
        # Create mutated version
        mutated = process.mutate()
        
        # Modify original step
        process.steps[0].parameters["value"] = 2.0
        
        # Mutated version should not be affected (independent copy)
        assert mutated.steps[0].parameters["value"] != 2.0
    
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
        process_dict = process.to_dict()
        
        assert "nested" in process_dict["steps"][0]["parameters"]
        assert "list" in process_dict["steps"][0]["parameters"]
        assert "mixed" in process_dict["steps"][0]["parameters"]
        
        # Should be able to restore
        restored = ProcessDNA.from_dict(process_dict)
        assert "nested" in restored.steps[0].parameters
        assert "list" in restored.steps[0].parameters
        assert "mixed" in restored.steps[0].parameters
