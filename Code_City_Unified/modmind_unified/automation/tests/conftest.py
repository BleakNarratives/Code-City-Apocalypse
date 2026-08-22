
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: automation_dna, pytest
# ROLE: Test fixtures and configuration for Automation DNA
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Script (2)
# [/DNA_TAG]

"""
Test fixtures and configuration for Automation DNA
"""
import pytest
from automation_dna.core.dna_process import ProcessDNA, StepDNA, ConnectionDNA
from automation_dna.core.evolution_engine import EvolutionEngine


@pytest.fixture
def sample_step():
    """Create a sample step for testing"""
    step = StepDNA(
        step_type="action",
        name="Initial Step",
        description="Test step for unit testing"
    )
    # Add parameters after creation
    step.parameters = {"param1": 1.0, "param2": "value"}
    return step


@pytest.fixture
def sample_connection():
    """Create a sample connection for testing"""
    return ConnectionDNA(
        source_id="step_1",
        target_id="step_2",
        condition="success",
        probability=0.95
    )


@pytest.fixture
def sample_dna():
    """Create a sample ProcessDNA for testing"""
    step1 = StepDNA(
        step_type="start",
        name="Start",
        description="Initial step"
    )
    step1.parameters = {}
    
    step2 = StepDNA(
        step_type="action", 
        name="Process",
        description="Processing step"
    )
    step2.parameters = {"action": "process"}
    
    connection = ConnectionDNA(
        source_step_id="step_1",
        target_step_id="step_2",
        condition="success"
    )
    connection.transition_probability = 1.0
    
    return ProcessDNA(
        process_type=ProcessType.CUSTOM,
        name="Test Process",
        description="Test process for unit testing"
    )


@pytest.fixture
def evolution_engine():
    """Create an evolution engine with small population for testing"""
    return EvolutionEngine(population_size=5)


@pytest.fixture
def mock_dna_data():
    """Mock DNA data for testing"""
    return {
        "name": "Mock Process",
        "version": "1.0",
        "steps": [
            {
                "id": "step_1",
                "name": "Mock Step",
                "step_type": "action",
                "parameters": {},
                "success_rate": 0.9,
                "efficiency": 0.8,
                "cost": 5.0,
                "speed": 7.0
            }
        ],
        "connections": [],
        "metadata": {}
    }
