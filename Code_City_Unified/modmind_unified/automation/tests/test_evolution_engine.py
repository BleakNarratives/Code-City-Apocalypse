"""
Test suite for Evolution Engine functionality
Tests population management, selection, breeding, and evolution
"""
import pytest
from automation_dna.core.dna_process import ProcessDNA
from automation_dna.core.evolution_engine import EvolutionEngine


class TestEvolutionEngineInitialization:
    """Test engine initialization and basic functionality"""
    
    def test_engine_creation(self, evolution_engine):
        """Test evolution engine creation"""
        assert evolution_engine.population_size == 5
        assert evolution_engine.generation == 0
        assert len(evolution_engine.population) == 0  # Starts empty
        assert evolution_engine.mutation_rate == 0.1
        assert evolution_engine.elitism_rate == 0.2
    
    def test_engine_with_custom_parameters(self):
        """Test engine with custom parameters"""
        engine = EvolutionEngine(
            population_size=10,
            mutation_rate=0.15,
            elitism_rate=0.25
        )
        
        assert engine.population_size == 10
        assert engine.mutation_rate == 0.15
        assert engine.elitism_rate == 0.25
    
    def test_initial_population_creation(self, evolution_engine, sample_dna):
        """Test initial population creation"""
        # Create initial population
        evolution_engine.create_initial_population(sample_dna)
        
        # Should have correct population size
        assert len(evolution_engine.population) == evolution_engine.population_size
        
        # All individuals should be ProcessDNA instances
        for individual in evolution_engine.population:
            assert isinstance(individual, ProcessDNA)
        
        # Generation should still be 0
        assert evolution_engine.generation == 0


class TestPopulationManagement:
    """Test population management functionality"""
    
    def test_add_individual(self, evolution_engine, sample_dna):
        """Test adding individual to population"""
        # Add individual
        evolution_engine.add_individual(sample_dna)
        
        # Should have one individual
        assert len(evolution_engine.population) == 1
        assert evolution_engine.population[0] == sample_dna
    
    def test_remove_individual(self, evolution_engine, sample_dna):
        """Test removing individual from population"""
        # Add then remove
        evolution_engine.add_individual(sample_dna)
        evolution_engine.remove_individual(0)
        
        # Should be empty
        assert len(evolution_engine.population) == 0
    
    def test_get_best_individual(self, evolution_engine, sample_dna):
        """Test getting best individual from population"""
        # Create population with varying fitness
        for i in range(3):
            dna = sample_dna.clone()
            # Modify fitness by changing parameters
            for step in dna.steps:
                step.success_rate = 0.5 + i * 0.2  # Varying success rates
            evolution_engine.add_individual(dna)
        
        # Get best individual
        best = evolution_engine.get_best_individual()
        
        # Should have highest fitness
        best_fitness = best.calculate_fitness()
        for individual in evolution_engine.population:
            assert individual.calculate_fitness() <= best_fitness
    
    def test_get_average_fitness(self, evolution_engine, sample_dna):
        """Test average fitness calculation"""
        # Add individuals with known fitness
        fitness_values = [0.5, 0.6, 0.7]
        for fitness_val in fitness_values:
            dna = sample_dna.clone()
            # Simulate specific fitness by setting parameters
            for step in dna.steps:
                step.success_rate = fitness_val
                step.efficiency = fitness_val
            evolution_engine.add_individual(dna)
        
        # Calculate average
        avg_fitness = evolution_engine.get_average_fitness()
        expected_avg = sum(fitness_values) / len(fitness_values)
        
        # Should be close to expected average
        assert abs(avg_fitness - expected_avg) < 0.1


class TestSelectionMethods:
    """Test selection algorithms"""
    
    def test_tournament_selection(self, evolution_engine, sample_dna):
        """Test tournament selection method"""
        # Create population
        for i in range(evolution_engine.population_size):
            dna = sample_dna.clone()
            # Vary fitness
            for step in dna.steps:
                step.success_rate = 0.5 + (i * 0.1)
            evolution_engine.add_individual(dna)
        
        # Perform tournament selection
        selected = evolution_engine._tournament_selection(tournament_size=2)
        
        # Should return an individual
        assert isinstance(selected, ProcessDNA)
        assert selected in evolution_engine.population
    
    def test_elitism_selection(self, evolution_engine, sample_dna):
        """Test elitism selection method"""
        # Create population
        for i in range(evolution_engine.population_size):
            dna = sample_dna.clone()
            # Vary fitness
            for step in dna.steps:
                step.success_rate = 0.5 + (i * 0.1)
            evolution_engine.add_individual(dna)
        
        # Get elites
        elites = evolution_engine._select_elites()
        
        # Should return correct number of elites
        expected_elites = int(evolution_engine.population_size * evolution_engine.elitism_rate)
        assert len(elites) == expected_elites
        
        # Elites should be the fittest individuals
        elite_fitnesses = [dna.calculate_fitness() for dna in elites]
        assert elite_fitnesses == sorted(elite_fitnesses, reverse=True)


class TestBreedingMethods:
    """Test breeding and crossover functionality"""
    
    def test_crossover_breeding(self, evolution_engine, sample_dna):
        """Test crossover breeding method"""
        # Create two parent DNAs
        parent1 = sample_dna.clone()
        parent2 = sample_dna.clone()
        
        # Modify parents to be different
        parent1.steps[0].success_rate = 0.9
        parent2.steps[0].success_rate = 0.7
        
        # Perform crossover
        child = evolution_engine._crossover_breeding(parent1, parent2)
        
        # Child should be ProcessDNA instance
        assert isinstance(child, ProcessDNA)
        
        # Child should have same structure
        assert len(child.steps) == len(parent1.steps)
        assert len(child.connections) == len(parent1.connections)
        
        # Child should be different from both parents
        assert child != parent1
        assert child != parent2
    
    def test_create_new_generation(self, evolution_engine, sample_dna):
        """Test creation of new generation"""
        # Create initial population
        for i in range(evolution_engine.population_size):
            dna = sample_dna.clone()
            # Vary fitness
            for step in dna.steps:
                step.success_rate = 0.5 + (i * 0.05)
            evolution_engine.add_individual(dna)
        
        # Create new generation
        new_population = evolution_engine._create_new_generation()
        
        # Should have same population size
        assert len(new_population) == evolution_engine.population_size
        
        # All should be ProcessDNA instances
        for individual in new_population:
            assert isinstance(individual, ProcessDNA)


class TestEvolutionProcess:
    """Test complete evolution process"""
    
    def test_single_evolution_step(self, evolution_engine, sample_dna):
        """Test single evolution step"""
        # Create initial population
        evolution_engine.create_initial_population(sample_dna)
        initial_fitness = evolution_engine.get_average_fitness()
        
        # Perform evolution step
        evolution_engine.evolve()
        
        # Generation should increment
        assert evolution_engine.generation == 1
        
        # Population size should remain same
        assert len(evolution_engine.population) == evolution_engine.population_size
        
        # Fitness should potentially improve (or at least not be worse)
        new_fitness = evolution_engine.get_average_fitness()
        assert isinstance(new_fitness, float)
    
    def test_multiple_evolution_steps(self, evolution_engine, sample_dna):
        """Test multiple evolution steps"""
        # Create initial population
        evolution_engine.create_initial_population(sample_dna)
        initial_fitness = evolution_engine.get_average_fitness()
        
        # Perform multiple steps
        steps = 5
        for i in range(steps):
            evolution_engine.evolve()
        
        # Generation should be correct
        assert evolution_engine.generation == steps
        
        # Final fitness
        final_fitness = evolution_engine.get_average_fitness()
        
        # Should have ProcessDNA instances
        for individual in evolution_engine.population:
            assert isinstance(individual, ProcessDNA)
    
    def test_evolution_with_convergence(self, evolution_engine, sample_dna):
        """Test evolution until convergence"""
        # Create initial population
        evolution_engine.create_initial_population(sample_dna)
        
        # Evolve until convergence or max generations
        max_generations = 20
        for i in range(max_generations):
            prev_fitness = evolution_engine.get_average_fitness()
            evolution_engine.evolve()
            current_fitness = evolution_engine.get_average_fitness()
            
            # Check for convergence (small fitness change)
            if abs(current_fitness - prev_fitness) < 0.001:
                break
        
        # Should have evolved for at least some generations
        assert evolution_engine.generation > 0
        
        # Population should still be valid
        assert len(evolution_engine.population) == evolution_engine.population_size


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_evolution_with_empty_population(self, evolution_engine):
        """Test evolution with empty population"""
        # Should handle gracefully
        try:
            evolution_engine.evolve()
            # If it doesn't raise exception, should still work
            assert True
        except Exception as e:
            # Should raise appropriate exception
            assert "population" in str(e).lower() or "empty" in str(e).lower()
    
    def test_evolution_with_single_individual(self, evolution_engine, sample_dna):
        """Test evolution with only one individual"""
        # Add single individual
        evolution_engine.add_individual(sample_dna)
        
        # Should handle gracefully
        try:
            evolution_engine.evolve()
            # Check that population is still valid
            assert len(evolution_engine.population) >= 1
        except Exception as e:
            # Should raise appropriate exception
            assert "population" in str(e).lower() or "size" in str(e).lower()
    
    def test_evolution_with_identical_individuals(self, evolution_engine, sample_dna):
        """Test evolution when all individuals are identical"""
        # Add identical individuals
        for i in range(evolution_engine.population_size):
            evolution_engine.add_individual(sample_dna.clone())
        
        # All should have same fitness initially
        fitnesses = [ind.calculate_fitness() for ind in evolution_engine.population]
        assert all(f == fitnesses[0] for f in fitnesses)
        
        # Evolution should still work (mutation will create diversity)
        evolution_engine.evolve()
        
        # Should have evolved
        assert evolution_engine.generation == 1
        
        # Population should still be valid
        assert len(evolution_engine.population) == evolution_engine.population_size


class TestPerformance:
    """Test performance characteristics"""
    
    def test_evolution_performance(self, evolution_engine, sample_dna):
        """Test that evolution runs in reasonable time"""
        import time
        
        # Create population
        evolution_engine.create_initial_population(sample_dna)
        
        # Time evolution step
        start_time = time.time()
        evolution_engine.evolve()
        end_time = time.time()
        
        # Should complete in reasonable time (< 1 second for small population)
        assert (end_time - start_time) < 1.0
    
    def test_large_population_creation(self):
        """Test creation of larger population"""
        import time
        
        engine = EvolutionEngine(population_size=50)
        sample_dna = ProcessDNA(
            name="Test",
            version="1.0",
            steps=[],
            connections=[],
            metadata={}
        )
        
        # Time population creation
        start_time = time.time()
        engine.create_initial_population(sample_dna)
        end_time = time.time()
        
        # Should complete in reasonable time
        assert (end_time - start_time) < 2.0
        
        # Should have correct size
        assert len(engine.population) == 50
