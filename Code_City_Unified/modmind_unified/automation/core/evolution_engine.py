import logging

#!/usr/bin/env python3
"""
🧬 Automation DNA - Evolution Engine
Handles mutation, breeding, and selection of business processes
"""

import json
import random
from typing import List, Dict, Any, Tuple
from .dna_process import ProcessDNA, StepDNA, ConnectionDNA, ProcessType

class EvolutionEngine:
    """Core evolution engine for Automation DNA"""
    
    def __init__(self, 
                 population_size: int = 50,
                 mutation_rate: float = 0.2,
                 breeding_rate: float = 0.3,
                 elitism: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.breeding_rate = breeding_rate
        self.elitism = elitism
        self.population: List[ProcessDNA] = []
        self.generation = 0
        self.best_fitness_history: List[float] = []
        self.avg_fitness_history: List[float] = []
    
    def initialize_population(self, 
                             process_type: ProcessType,
                             base_process: ProcessDNA) -> None:
        """Initialize population with variations of base process"""
        self.population = [base_process]
        
        # Create initial variations
        for _ in range(self.population_size - 1):
            mutated = base_process.mutate()
            self.population.append(mutated)
        
        self.generation = 1
    
    def evaluate_fitness(self, fitness_metrics: Dict[str, Dict[str, float]]) -> None:
        """Evaluate fitness for all processes in population"""
        for i, process in enumerate(self.population):
            # Get metrics for this process (by index or DNA ID)
            metrics = fitness_metrics.get(str(i), fitness_metrics.get(process.dna_id, {}))
            process.calculate_fitness(metrics)
    
    def select_parents(self) -> List[ProcessDNA]:
        """Select parents for breeding using tournament selection"""
        tournament_size = 5
        parents = []
        
        for _ in range(int(self.population_size * self.breeding_rate)):
            # Tournament selection
            contestants = random.sample(self.population, tournament_size)
            winner = max(contestants, key=lambda p: p.fitness_score)
            parents.append(winner)
        
        return parents
    
    def create_offspring(self, parents: List[ProcessDNA]) -> List[ProcessDNA]:
        """Create offspring through breeding and mutation"""
        offspring = []
        
        # Breeding
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child = parents[i].breed(parents[i + 1])
                offspring.append(child)
        
        # Mutation
        for process in self.population:
            if random.random() < self.mutation_rate:
                mutated = process.mutate()
                offspring.append(mutated)
        
        return offspring
    
    def next_generation(self, fitness_metrics: Dict[str, Dict[str, float]]) -> None:
        """Evolve to the next generation"""
        # Evaluate fitness
        self.evaluate_fitness(fitness_metrics)
        
        # Record fitness statistics
        fitness_scores = [p.fitness_score for p in self.population]
        self.best_fitness_history.append(max(fitness_scores))
        self.avg_fitness_history.append(sum(fitness_scores) / len(fitness_scores))
        
        # Select parents
        parents = self.select_parents()
        
        # Create offspring
        offspring = self.create_offspring(parents)
        
        # Apply elitism - keep top performers
        elite_size = int(self.population_size * self.elitism)
        elites = sorted(self.population, key=lambda p: p.fitness_score, reverse=True)[:elite_size]
        
        # Create new population
        self.population = elites + offspring
        
        # Ensure population size
        if len(self.population) > self.population_size:
            self.population = self.population[:self.population_size]
        elif len(self.population) < self.population_size:
            # Fill with mutations of best performers
            while len(self.population) < self.population_size:
                parent = random.choice(elites)
                self.population.append(parent.mutate())
        
        self.generation += 1
    
    def get_best_process(self) -> ProcessDNA:
        """Get the best performing process"""
        return max(self.population, key=lambda p: p.fitness_score)
    
    def get_diversity_score(self) -> float:
        """Calculate diversity score of population"""
        # Simple diversity metric based on DNA IDs
        unique_steps = set()
        for process in self.population:
            for step in process.steps:
                unique_steps.add(step.dna_id)
        
        return len(unique_steps) / (self.population_size * 3)  # Average 3 steps per process
    
    def save_population(self, filename: str) -> None:
        """Save entire population to file"""
        population_data = {
            "generation": self.generation,
            "population": [p.to_dict() for p in self.population],
            "best_fitness_history": self.best_fitness_history,
            "avg_fitness_history": self.avg_fitness_history,
            "diversity_score": self.get_diversity_score()
        }
        
        with open(filename, 'w') as f:
            json.dump(population_data, f, indent=2)
    
    @classmethod
    def load_population(cls, filename: str) -> 'EvolutionEngine':
        """Load population from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        engine = cls()
        engine.generation = data['generation']
        engine.best_fitness_history = data['best_fitness_history']
        engine.avg_fitness_history = data['avg_fitness_history']
        
        # Recreate processes
        for process_data in data['population']:
            process = ProcessDNA.from_dict(process_data)
            engine.population.append(process)
        
        return engine
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current evolution statistics"""
        fitness_scores = [p.fitness_score for p in self.population]
        
        return {
            "generation": self.generation,
            "population_size": len(self.population),
            "best_fitness": max(fitness_scores),
            "avg_fitness": sum(fitness_scores) / len(fitness_scores),
            "worst_fitness": min(fitness_scores),
            "diversity_score": self.get_diversity_score(),
            "fitness_std_dev": (sum((x - sum(fitness_scores)/len(fitness_scores))**2 for x in fitness_scores) / len(fitness_scores))**0.5
        }

# Example usage
if __name__ == "__main__":
    logging.info("🧬 Automation DNA Evolution Engine - Initialized!")
    
    # Create a base process
    from dna_process import ProcessDNA, StepDNA, ConnectionDNA, ProcessType
    
    base_process = ProcessDNA(
        process_type=ProcessType.CUSTOMER_ONBOARDING,
        name="Base Onboarding",
        description="Base customer onboarding process"
    )
    
    # Add steps
    step1 = StepDNA("form", "Collect Info", "Gather customer data")
    step1.parameters = {"fields": ["name", "email"], "timeout": 300}
    
    step2 = StepDNA("verification", "Verify Email", "Confirm email address")
    step2.parameters = {"template": "welcome", "retries": 2}
    
    step3 = StepDNA("activation", "Activate Account", "Enable access")
    step3.parameters = {"role": "customer"}
    
    base_process.add_step(step1)
    base_process.add_step(step2)
    base_process.add_step(step3)
    
    # Add connections
    base_process.add_connection(ConnectionDNA(step1.dna_id, step2.dna_id, "success"))
    base_process.add_connection(ConnectionDNA(step2.dna_id, step3.dna_id, "verified"))
    
    # Create evolution engine
    engine = EvolutionEngine(population_size=20, mutation_rate=0.3, breeding_rate=0.4)
    engine.initialize_population(ProcessType.CUSTOMER_ONBOARDING, base_process)
    
    logging.info(f"✅ Initialized population: {len(engine.population)} processes")
    logging.info(f"🔢 Generation: {engine.generation}")
    
    # Simulate evolution for 10 generations
    logging.info("\n🧬 Evolving processes...")
    for gen in range(10):
        # Generate random fitness metrics for each process
        fitness_metrics = {}
        for i, process in enumerate(engine.population):
            # Random metrics based on generation
            base_efficiency = 0.7 + (gen * 0.02)
            base_success = 0.8 + (gen * 0.01)
            base_cost = 0.8 - (gen * 0.02)
            base_speed = 0.6 + (gen * 0.03)
            
            fitness_metrics[i] = {
                "efficiency": random.uniform(base_efficiency - 0.1, base_efficiency + 0.1),
                "success_rate": random.uniform(base_success - 0.1, base_success + 0.1),
                "cost": random.uniform(max(0.1, base_cost - 0.1), base_cost + 0.1),
                "speed": random.uniform(base_speed - 0.1, base_speed + 0.1)
            }
        
        engine.next_generation(fitness_metrics)
        
        stats = engine.get_statistics()
        logging.info(f"Generation {engine.generation}: Best={stats['best_fitness']:.3f}, Avg={stats['avg_fitness']:.3f}, Diversity={stats['diversity_score']:.3f}")
    
    # Get best process
    best = engine.get_best_process()
    logging.info(f"\n🎉 Evolution complete!")
    logging.info(f"🏆 Best process: {best.name}")
    logging.info(f"💪 Fitness score: {best.fitness_score:.3f}")
    logging.info(f"🔢 Generation: {best.generation}")
    logging.info(f"📊 Mutations: {len(best.mutations)}")
    
    # Save population
    engine.save_population("evolved_onboarding.json")
    logging.info("💾 Saved evolved population to evolved_onboarding.json")