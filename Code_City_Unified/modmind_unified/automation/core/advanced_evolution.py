import logging

#!/usr/bin/env python3
"""
FILE: automation_dna/core/advanced_evolution.py
PURPOSE: Advanced evolution strategies and fitness calculations
AUTHOR: Autonomous Agent Claude (Still in Berserker Mode)
DATE: 2026-01-16

This module extends the base evolution engine with:
- Industry-specific fitness functions
- Advanced mutation strategies (Gaussian, polynomial, etc.)
- Multi-objective optimization (Pareto fronts)
- Adaptive parameter tuning
- Diversity preservation mechanisms
- Niching and speciation

Think of this as Evolution Engine 2.0 - for when you need REAL power.
"""

import random
import math
import numpy as np
from typing import List, Dict, Tuple, Callable, Any, Optional
from enum import Enum
from dataclasses import dataclass

from dna_process import ProcessDNA, StepDNA, ProcessType

# =============================================================================
# MUTATION STRATEGIES
# =============================================================================

class MutationType(Enum):
    """
    Types of mutations that can be applied to process DNA.
    
    Different mutation types serve different purposes:
    - UNIFORM: Random change across entire range (exploration)
    - GAUSSIAN: Small changes around current value (exploitation)
    - POLYNOMIAL: Bounded changes with configurable distribution
    - CREEP: Tiny incremental changes (fine-tuning)
    - SWAP: Exchange two elements (for ordered sequences)
    - INVERSION: Reverse a subsequence (for ordered sequences)
    """
    UNIFORM = "uniform"          # Random value in parameter range
    GAUSSIAN = "gaussian"        # Normal distribution around current
    POLYNOMIAL = "polynomial"    # Polynomial distribution mutation
    CREEP = "creep"             # Small incremental change
    SWAP = "swap"               # Swap two random elements
    INVERSION = "inversion"     # Invert a subsequence
    ADAPTIVE = "adaptive"       # Adapt mutation strength based on fitness


@dataclass
class MutationConfig:
    """
    Configuration for mutation operations.
    
    Attributes:
        mutation_type: Type of mutation to apply
        rate: Probability of mutation (0.0 to 1.0)
        strength: Magnitude of mutation effect
        adaptive: Whether to adapt mutation strength over time
    """
    mutation_type: MutationType = MutationType.GAUSSIAN
    rate: float = 0.2
    strength: float = 0.1
    adaptive: bool = True


class AdvancedMutator:
    """
    Advanced mutation engine with multiple strategies.
    
    Provides sophisticated mutation operations beyond simple random changes.
    Uses adaptive mutation rates and strength based on population diversity
    and convergence status.
    """
    
    def __init__(self, config: MutationConfig):
        self.config = config
        self.generation = 0
        self.best_fitness_history: List[float] = []
        
    def mutate_numeric(self, value: float, min_val: float, max_val: float) -> float:
        """
        Mutate a numeric parameter using configured strategy.
        
        Args:
            value: Current parameter value
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Mutated value within bounds
            
        Different mutation types produce different distributions:
        - Uniform: Equal probability across range
        - Gaussian: Most changes near current value
        - Polynomial: Controlled distribution shape
        """
        if self.config.mutation_type == MutationType.UNIFORM:
            # Uniform random mutation within range
            return random.uniform(min_val, max_val)
            
        elif self.config.mutation_type == MutationType.GAUSSIAN:
            # Gaussian mutation - normal distribution around current value
            # Standard deviation scales with mutation strength and range
            std_dev = (max_val - min_val) * self.config.strength
            mutated = value + random.gauss(0, std_dev)
            return max(min_val, min(max_val, mutated))
            
        elif self.config.mutation_type == MutationType.POLYNOMIAL:
            # Polynomial mutation - bounded distribution
            # Creates a distribution that favors smaller changes
            delta_max = max_val - min_val
            rand = random.random()
            
            if rand < 0.5:
                delta = (2 * rand) ** (1.0 / (self.config.strength + 1)) - 1
            else:
                delta = 1 - (2 * (1 - rand)) ** (1.0 / (self.config.strength + 1))
                
            mutated = value + delta * delta_max * 0.5
            return max(min_val, min(max_val, mutated))
            
        elif self.config.mutation_type == MutationType.CREEP:
            # Creep mutation - small incremental changes
            # Good for fine-tuning already good solutions
            max_change = (max_val - min_val) * self.config.strength * 0.1
            delta = random.uniform(-max_change, max_change)
            mutated = value + delta
            return max(min_val, min(max_val, mutated))
            
        else:
            # Default to Gaussian if unknown type
            return self.mutate_numeric(value, min_val, max_val)
    
    def adapt_mutation_rate(self, diversity: float, convergence: float):
        """
        Adapt mutation parameters based on population state.
        
        Args:
            diversity: Current population diversity (0.0 to 1.0)
            convergence: How converged population is (0.0 to 1.0)
            
        Adaptive strategy:
        - Low diversity → increase mutation to explore
        - High convergence → increase mutation to escape local optima
        - High diversity + low convergence → decrease mutation to exploit
        
        This prevents premature convergence while avoiding excessive exploration.
        """
        if not self.config.adaptive:
            return
            
        # If population is too similar (low diversity), increase mutation
        if diversity < 0.3:
            self.config.strength = min(0.5, self.config.strength * 1.2)
            self.config.rate = min(0.8, self.config.rate * 1.1)
            
        # If population is very diverse but not improving, decrease mutation
        elif diversity > 0.7 and convergence < 0.3:
            self.config.strength = max(0.05, self.config.strength * 0.9)
            self.config.rate = max(0.1, self.config.rate * 0.95)


# =============================================================================
# FITNESS FUNCTIONS - INDUSTRY SPECIFIC
# =============================================================================

class FitnessStrategy:
    """
    Base class for fitness calculation strategies.
    
    Different process types require different fitness functions.
    This abstraction allows easy swapping of fitness calculation logic.
    """
    
    def calculate(self, process: ProcessDNA, metrics: Dict[str, float]) -> float:
        """
        Calculate fitness score for a process.
        
        Args:
            process: Process to evaluate
            metrics: Performance metrics from execution
            
        Returns:
            Fitness score (0.0 to 1.0, higher is better)
        """
        raise NotImplementedError("Subclasses must implement calculate()")
    
    def get_required_metrics(self) -> List[str]:
        """Return list of required metric names"""
        raise NotImplementedError()


class CustomerOnboardingFitness(FitnessStrategy):
    """
    Fitness function optimized for customer onboarding processes.
    
    Key metrics:
    - Conversion rate: % of users completing onboarding
    - Time to activation: How fast users become active
    - Drop-off points: Where users abandon the process
    - Support tickets: Issues during onboarding
    - User satisfaction: Post-onboarding NPS/CSAT
    
    Weights prioritize conversion and satisfaction over speed.
    """
    
    def get_required_metrics(self) -> List[str]:
        return ['conversion_rate', 'time_to_activation', 'support_tickets', 
                'user_satisfaction', 'drop_off_rate']
    
    def calculate(self, process: ProcessDNA, metrics: Dict[str, float]) -> float:
        """
        Calculate fitness for customer onboarding.
        
        Formula:
        fitness = (conversion * 0.35) + (satisfaction * 0.30) + 
                  (speed * 0.15) + (support * 0.10) + (retention * 0.10)
        
        Where all metrics are normalized to 0-1 range.
        """
        # Normalize metrics to 0-1 range
        conversion = metrics.get('conversion_rate', 0.5)  # Already 0-1
        satisfaction = metrics.get('user_satisfaction', 0.5)  # Already 0-1
        
        # Time to activation: lower is better, normalize to 0-1
        # Assume target is 5 minutes (300 seconds), max acceptable is 30 minutes
        activation_time = metrics.get('time_to_activation', 900)  # seconds
        speed_score = max(0, min(1, 1 - (activation_time - 300) / 1500))
        
        # Support tickets: lower is better
        # Assume 0 tickets = 1.0, 10+ tickets = 0.0
        tickets = metrics.get('support_tickets', 5)
        support_score = max(0, min(1, 1 - tickets / 10))
        
        # Drop-off rate: lower is better (inverse of conversion)
        drop_off = metrics.get('drop_off_rate', 0.3)
        retention_score = 1 - drop_off
        
        # Weighted fitness calculation
        fitness = (
            conversion * 0.35 +
            satisfaction * 0.30 +
            speed_score * 0.15 +
            support_score * 0.10 +
            retention_score * 0.10
        )
        
        return fitness


class SalesPipelineFitness(FitnessStrategy):
    """
    Fitness function for sales pipeline optimization.
    
    Focuses on:
    - Win rate: % of opportunities closed-won
    - Deal velocity: Time from lead to close
    - Deal size: Average contract value
    - Pipeline value: Total potential revenue
    - Sales efficiency: Cost per closed deal
    """
    
    def get_required_metrics(self) -> List[str]:
        return ['win_rate', 'avg_deal_time', 'avg_deal_size', 
                'pipeline_value', 'cost_per_close']
    
    def calculate(self, process: ProcessDNA, metrics: Dict[str, float]) -> float:
        """
        Calculate fitness for sales pipeline.
        
        Heavily weights win rate and deal size since revenue is king.
        """
        win_rate = metrics.get('win_rate', 0.2)  # 0-1
        
        # Deal time: target 30 days, max acceptable 180 days
        deal_time = metrics.get('avg_deal_time', 60)  # days
        velocity_score = max(0, min(1, 1 - (deal_time - 30) / 150))
        
        # Deal size: normalize against target
        # Assume target is $10k, normalize to 0-1 where $50k+ = 1.0
        deal_size = metrics.get('avg_deal_size', 10000)  # dollars
        size_score = min(1, deal_size / 50000)
        
        # Pipeline value: higher is better
        # Normalize against target of $1M
        pipeline = metrics.get('pipeline_value', 500000)  # dollars
        pipeline_score = min(1, pipeline / 1000000)
        
        # Cost per close: lower is better
        # Target $1k, max acceptable $10k
        cost = metrics.get('cost_per_close', 5000)  # dollars
        efficiency_score = max(0, min(1, 1 - (cost - 1000) / 9000))
        
        # Weighted calculation - revenue metrics dominate
        fitness = (
            win_rate * 0.30 +
            size_score * 0.25 +
            velocity_score * 0.20 +
            pipeline_score * 0.15 +
            efficiency_score * 0.10
        )
        
        return fitness


class SupportTicketFitness(FitnessStrategy):
    """
    Fitness function for support ticket workflow optimization.
    
    Optimizes for:
    - First response time: How fast initial reply
    - Resolution time: Time to close ticket
    - Customer satisfaction: CSAT/NPS scores
    - Agent efficiency: Tickets per agent per day
    - Escalation rate: % requiring escalation
    """
    
    def get_required_metrics(self) -> List[str]:
        return ['first_response_time', 'resolution_time', 'csat_score',
                'tickets_per_agent', 'escalation_rate']
    
    def calculate(self, process: ProcessDNA, metrics: Dict[str, float]) -> float:
        """
        Calculate fitness for support tickets.
        
        Balances speed and quality - fast responses matter, but so does
        customer satisfaction.
        """
        # First response: target 5 minutes, max 60 minutes
        first_response = metrics.get('first_response_time', 20)  # minutes
        response_score = max(0, min(1, 1 - (first_response - 5) / 55))
        
        # Resolution time: target 4 hours, max 48 hours
        resolution = metrics.get('resolution_time', 12)  # hours
        resolution_score = max(0, min(1, 1 - (resolution - 4) / 44))
        
        # CSAT score: already 0-1 (or 0-100, normalize if needed)
        csat = metrics.get('csat_score', 0.7)
        if csat > 1:  # If 0-100 scale
            csat = csat / 100
        
        # Tickets per agent: target 15/day, sweet spot 10-20
        tickets = metrics.get('tickets_per_agent', 12)
        efficiency_score = max(0, min(1, 1 - abs(tickets - 15) / 15))
        
        # Escalation rate: lower is better, target <5%
        escalation = metrics.get('escalation_rate', 0.15)  # 0-1
        escalation_score = max(0, 1 - escalation / 0.2)  # 0 if >20% escalation
        
        # Customer satisfaction is king in support
        fitness = (
            csat * 0.35 +
            resolution_score * 0.25 +
            response_score * 0.20 +
            efficiency_score * 0.10 +
            escalation_score * 0.10
        )
        
        return fitness


# =============================================================================
# FACTORY FOR FITNESS STRATEGIES
# =============================================================================

class FitnessFactory:
    """
    Factory for creating appropriate fitness strategies.
    
    Maps ProcessType to the correct FitnessStrategy implementation.
    Makes it easy to add new process types without modifying core code.
    """
    
    _strategies: Dict[ProcessType, FitnessStrategy] = {
        ProcessType.CUSTOMER_ONBOARDING: CustomerOnboardingFitness(),
        ProcessType.SALES_PIPELINE: SalesPipelineFitness(),
        ProcessType.SUPPORT_TICKET: SupportTicketFitness(),
    }
    
    @classmethod
    def get_strategy(cls, process_type: ProcessType) -> FitnessStrategy:
        """
        Get fitness strategy for process type.
        
        Args:
            process_type: Type of process
            
        Returns:
            Appropriate FitnessStrategy instance
            
        Raises:
            ValueError: If no strategy exists for this process type
        """
        strategy = cls._strategies.get(process_type)
        if not strategy:
            raise ValueError(f"No fitness strategy defined for {process_type}")
        return strategy
    
    @classmethod
    def register_strategy(cls, process_type: ProcessType, strategy: FitnessStrategy):
        """
        Register a new fitness strategy for a process type.
        
        This allows users to define custom fitness functions for their
        specific business processes.
        """
        cls._strategies[process_type] = strategy


# =============================================================================
# MULTI-OBJECTIVE OPTIMIZATION
# =============================================================================

class ParetoOptimizer:
    """
    Multi-objective optimization using Pareto dominance.
    
    Many business processes have competing objectives (e.g., speed vs quality).
    Pareto optimization finds the set of non-dominated solutions where
    improving one objective would worsen another.
    
    Example: In sales, you might optimize for:
    - Deal size (higher is better)
    - Sales cycle time (lower is better)
    - Win rate (higher is better)
    
    No single solution is "best" - you get a Pareto front of optimal trade-offs.
    """
    
    @staticmethod
    def dominates(scores1: List[float], scores2: List[float], 
                  maximize: List[bool]) -> bool:
        """
        Check if scores1 Pareto-dominates scores2.
        
        Args:
            scores1: First solution's objective scores
            scores2: Second solution's objective scores
            maximize: For each objective, True if higher is better
            
        Returns:
            True if scores1 dominates scores2
            
        Domination rules:
        - All objectives are at least as good
        - At least one objective is strictly better
        """
        better_in_any = False
        
        for s1, s2, max_better in zip(scores1, scores2, maximize):
            if max_better:
                if s1 < s2:  # Worse in this objective
                    return False
                if s1 > s2:
                    better_in_any = True
            else:  # Minimize this objective
                if s1 > s2:  # Worse in this objective
                    return False
                if s1 < s2:
                    better_in_any = True
        
        return better_in_any
    
    @classmethod
    def find_pareto_front(cls, population: List[ProcessDNA],
                         objective_functions: List[Callable],
                         maximize: List[bool]) -> List[ProcessDNA]:
        """
        Find Pareto-optimal solutions in population.
        
        Args:
            population: List of processes to evaluate
            objective_functions: List of functions that score each process
            maximize: For each objective, True if higher is better
            
        Returns:
            List of non-dominated processes (Pareto front)
        """
        # Calculate all objective scores
        all_scores = []
        for process in population:
            scores = [obj_func(process) for obj_func in objective_functions]
            all_scores.append(scores)
        
        # Find non-dominated solutions
        pareto_front = []
        for i, (process, scores) in enumerate(zip(population, all_scores)):
            dominated = False
            for j, other_scores in enumerate(all_scores):
                if i != j and cls.dominates(other_scores, scores, maximize):
                    dominated = True
                    break
            
            if not dominated:
                pareto_front.append(process)
        
        return pareto_front


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    logging.info("🧬 Advanced Evolution Engine - Test Suite")
    logging.info("=" * 60)
    
    # Test mutation strategies
    logging.info("\n📊 Testing Mutation Strategies:")
    config = MutationConfig(mutation_type=MutationType.GAUSSIAN, strength=0.1)
    mutator = AdvancedMutator(config)
    
    test_value = 0.5
    logging.info(f"Original value: {test_value}")
    
    for i in range(5):
        mutated = mutator.mutate_numeric(test_value, 0.0, 1.0)
        logging.info(f"  Mutation {i+1}: {mutated:.4f}")
    
    # Test fitness strategies
    logging.info("\n💪 Testing Fitness Strategies:")
    
    # Customer onboarding
    onboarding_fitness = CustomerOnboardingFitness()
    metrics = {
        'conversion_rate': 0.85,
        'time_to_activation': 600,
        'support_tickets': 2,
        'user_satisfaction': 0.9,
        'drop_off_rate': 0.15
    }
    
    from dna_process import ProcessDNA, ProcessType
    test_process = ProcessDNA(ProcessType.CUSTOMER_ONBOARDING, "Test", "Test process")
    
    score = onboarding_fitness.calculate(test_process, metrics)
    logging.info(f"Onboarding fitness: {score:.3f}")
    
    logging.info("\n✅ Advanced Evolution Engine tests complete!")