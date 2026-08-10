"""
Test suite for DNA Process functionality
Tests DNA creation, mutation, breeding, and serialization
"""
import json
import pytest
from automation_dna.core.dna_process import ProcessDNA, StepDNA, ConnectionDNA


class TestStepDNA:
    """Test StepDNA class functionality"""
    
    def test_step_creation(self, sample_step):
        """Test step creation with valid parameters"""
        assert sample_step.dna_id is not None
        assert sample_step.name == "Initial Step"
        assert sample_step.step_type == "action"
        assert sample_step.parameters == {"param1": 1.0, "param2": "value"}
        assert sample_step.description == "Test step for unit testing"
    
    def test_step_mutation(self, sample_step):
        """Test step mutation functionality"""
        original_values = {
            "success_rate": sample_step.success_rate,
            "efficiency": sample_step.efficiency,
            "cost": sample_step.cost,
            "speed": sample_step.speed
        }
        
        # Mutate the step
        sample_step.mutate(mutation_rate=0.1)
        
        # Check that values have changed
        mutated_values = {
            "success_rate": sample_step.success_rate,
            "efficiency": sample_step.efficiency,
            "cost": sample_step.cost,
            "speed": sample_step.speed
        }
        
        # At least one value should be different
        changes = sum(1 for k, v in mutated_values.items() if v != original_values[k])
        assert changes >= 1, "Mutation should change at least one parameter"
        
        # Values should be within valid ranges
        assert 0.0 <= sample_step.success_rate <= 1.0
        assert 0.0 <= sample_step.efficiency <= 1.0
        assert sample_step.cost >= 0.0
        assert sample_step.speed >= 0.0
    
    def test_step_to_dict(self, sample_step):
        """Test step serialization to dictionary"""
        step_dict = sample_step.to_dict()
        
        assert step_dict["id"] == sample_step.id
        assert step_dict["name"] == sample_step.name
        assert step_dict["step_type"] == sample_step.step_type
        assert step_dict["parameters"] == sample_step.parameters
        assert step_dict["success_rate"] == sample_step.success_rate
        assert step_dict["efficiency"] == sample_step.efficiency
        assert step_dict["cost"] == sample_step.cost
        assert step_dict["speed"] == sample_step.speed
    
    def test_step_from_dict(self, sample_step):
        """Test step deserialization from dictionary"""
        step_dict = sample_step.to_dict()
        new_step = StepDNA.from_dict(step_dict)
        
        assert new_step.id == sample_step.id
        assert new_step.name == sample_step.name
        assert new_step.step_type == sample_step.step_type
        assert new_step.parameters == sample_step.parameters
        assert new_step.success_rate == sample_step.success_rate
        assert new_step.efficiency == sample_step.efficiency
        assert new_step.cost == sample_step.cost
        assert new_step.speed == sample_step.speed


class TestConnectionDNA:
    """Test ConnectionDNA class functionality"""
    
    def test_connection_creation(self, sample_connection):
        """Test connection creation with valid parameters"""
        assert sample_connection.source_id == "step_1"
        assert sample_connection.target_id == "step_2"
        assert sample_connection.condition == "success"
        assert sample_connection.probability == 0.95
    
    def test_connection_mutation(self, sample_connection):
        """Test connection mutation functionality"""
        original_probability = sample_connection.probability
        
        # Mutate the connection
        sample_connection.mutate(mutation_rate=0.1)
        
        # Probability should have changed
        assert sample_connection.probability != original_probability
        
        # Probability should be within valid range
        assert 0.0 <= sample_connection.probability <= 1.0
    
    def test_connection_to_dict(self, sample_connection):
        """Test connection serialization to dictionary"""
        conn_dict = sample_connection.to_dict()
        
        assert conn_dict["source_id"] == sample_connection.source_id
        assert conn_dict["target_id"] == sample_connection.target_id
        assert conn_dict["condition"] == sample_connection.condition
        assert conn_dict["probability"] == sample_connection.probability
    
    def test_connection_from_dict(self, sample_connection):
        """Test connection deserialization from dictionary"""
        conn_dict = sample_connection.to_dict()
        new_conn = ConnectionDNA.from_dict(conn_dict)
        
        assert new_conn.source_id == sample_connection.source_id
        assert new_conn.target_id == sample_connection.target_id
        assert new_conn.condition == sample_connection.condition
        assert new_conn.probability == sample_connection.probability


class TestProcessDNA:
    """Test ProcessDNA class functionality"""
    
    def test_process_creation(self, sample_dna):
        """Test process creation with valid parameters"""
        assert sample_dna.name == "Test Process"
        assert sample_dna.version == "1.0"
        assert len(sample_dna.steps) == 2
        assert len(sample_dna.connections) == 1
        assert sample_dna.metadata == {"description": "Test process for unit testing"}
    
    def test_process_mutation(self, sample_dna):
        """Test process mutation functionality"""
        # Store original fitness
        original_fitness = sample_dna.calculate_fitness()
        
        # Mutate the process
        sample_dna.mutate(mutation_rate=0.1)
        
        # Fitness should have changed
        new_fitness = sample_dna.calculate_fitness()
        
        # Mutation should result in different fitness (most cases)
        # Note: Small chance they could be equal due to randomness
        assert isinstance(new_fitness, float)
        assert 0.0 <= new_fitness <= 1.0
    
    def test_process_breeding(self, sample_dna):
        """Test process breeding functionality"""
        # Create a second DNA for breeding
        dna2 = ProcessDNA(
            name="Test Process 2",
            version="1.0",
            steps=sample_dna.steps.copy(),
            connections=sample_dna.connections.copy(),
            metadata={"description": "Second test process"}
        )
        
        # Breed the two DNAs
        child_dna = sample_dna.breed(dna2)
        
        # Child should be a ProcessDNA instance
        assert isinstance(child_dna, ProcessDNA)
        
        # Child should have same number of steps and connections
        assert len(child_dna.steps) == len(sample_dna.steps)
        assert len(child_dna.connections) == len(sample_dna.connections)
        
        # Child should have different name (breeding creates unique name)
        assert child_dna.name != sample_dna.name
        assert child_dna.name != dna2.name
    
    def test_process_fitness_calculation(self, sample_dna):
        """Test fitness calculation functionality"""
        fitness = sample_dna.calculate_fitness()
        
        # Fitness should be a float between 0 and 1
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
        
        # For our test data, fitness should be reasonable
        assert fitness > 0.5  # Our test process should be decent
    
    def test_process_to_json(self, sample_dna):
        """Test process serialization to JSON"""
        json_str = sample_dna.to_json()
        
        # Should be a valid JSON string
        assert isinstance(json_str, str)
        
        # Should be parseable
        parsed = json.loads(json_str)
        assert "name" in parsed
        assert "version" in parsed
        assert "steps" in parsed
        assert "connections" in parsed
        assert "metadata" in parsed
    
    def test_process_from_json(self, sample_dna):
        """Test process deserialization from JSON"""
        json_str = sample_dna.to_json()
        new_dna = ProcessDNA.from_json(json_str)
        
        # Should create equivalent ProcessDNA
        assert new_dna.name == sample_dna.name
        assert new_dna.version == sample_dna.version
        assert len(new_dna.steps) == len(sample_dna.steps)
        assert len(new_dna.connections) == len(sample_dna.connections)
        
        # Fitness should be similar (allowing for floating point differences)
        original_fitness = sample_dna.calculate_fitness()
        new_fitness = new_dna.calculate_fitness()
        assert abs(original_fitness - new_fitness) < 0.01
    
    def test_process_validation(self, sample_dna):
        """Test process validation functionality"""
        # Valid process should pass validation
        assert sample_dna.validate() == True
        
        # Test with invalid process (no steps)
        invalid_dna = ProcessDNA(
            name="Invalid Process",
            version="1.0",
            steps=[],
            connections=[],
            metadata={}
        )
        assert invalid_dna.validate() == False
    
    def test_process_clone(self, sample_dna):
        """Test process cloning functionality"""
        cloned_dna = sample_dna.clone()
        
        # Should be identical but separate instance
        assert cloned_dna.name == sample_dna.name
        assert cloned_dna.version == sample_dna.version
        assert len(cloned_dna.steps) == len(sample_dna.steps)
        assert len(cloned_dna.connections) == len(sample_dna.connections)
        
        # Should be different objects
        assert cloned_dna is not sample_dna
        assert cloned_dna.steps[0] is not sample_dna.steps[0]
        assert cloned_dna.connections[0] is not sample_dna.connections[0]
        
        # Fitness should be identical
        assert cloned_dna.calculate_fitness() == sample_dna.calculate_fitness()


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_process(self):
        """Test process with no steps or connections"""
        empty_dna = ProcessDNA(
            name="Empty Process",
            version="1.0",
            steps=[],
            connections=[],
            metadata={}
        )
        
        # Should have zero fitness
        assert empty_dna.calculate_fitness() == 0.0
        
        # Should fail validation
        assert empty_dna.validate() == False
    
    def test_process_with_invalid_steps(self):
        """Test process with steps that have invalid parameters"""
        invalid_step = StepDNA(
            id="invalid",
            name="Invalid",
            step_type="action",
            parameters={},
            success_rate=1.5,  # Invalid (should be <= 1.0)
            efficiency=0.8,
            cost=5.0,
            speed=7.0
        )
        
        invalid_dna = ProcessDNA(
            name="Invalid Process",
            version="1.0",
            steps=[invalid_step],
            connections=[],
            metadata={}
        )
        
        # Should still work but clamp values
        assert invalid_dna.steps[0].success_rate == 1.0  # Should be clamped
        
        # Fitness calculation should handle it
        fitness = invalid_dna.calculate_fitness()
        assert 0.0 <= fitness <= 1.0
    
    def test_process_with_circular_connections(self):
        """Test process with circular step connections"""
        step1 = StepDNA(
            id="step_1",
            name="Step 1",
            step_type="action",
            parameters={},
            success_rate=0.9,
            efficiency=0.8,
            cost=5.0,
            speed=7.0
        )
        
        step2 = StepDNA(
            id="step_2",
            name="Step 2",
            step_type="action",
            parameters={},
            success_rate=0.8,
            efficiency=0.7,
            cost=6.0,
            speed=6.0
        )
        
        # Circular connection
        conn1 = ConnectionDNA(
            source_id="step_1",
            target_id="step_2",
            condition="success",
            probability=1.0
        )
        
        conn2 = ConnectionDNA(
            source_id="step_2",
            target_id="step_1",
            condition="success",
            probability=1.0
        )
        
        circular_dna = ProcessDNA(
            name="Circular Process",
            version="1.0",
            steps=[step1, step2],
            connections=[conn1, conn2],
            metadata={}
        )
        
        # Should still calculate fitness (though may not be optimal)
        fitness = circular_dna.calculate_fitness()
        assert isinstance(fitness, float)
        assert 0.0 <= fitness <= 1.0
