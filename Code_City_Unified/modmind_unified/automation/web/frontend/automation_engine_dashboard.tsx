import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, TrendingUp, Dna, Zap, Users, Award } from 'lucide-react';

const AutomationDNADashboard = () => {
  const [generation, setGeneration] = useState(0);
  const [isEvolving, setIsEvolving] = useState(false);
  const [population, setPopulation] = useState([]);
  const [fitnessHistory, setFitnessHistory] = useState([]);
  const [bestProcess, setBestProcess] = useState(null);
  const [stats, setStats] = useState({
    bestFitness: 0,
    avgFitness: 0,
    diversity: 0,
    populationSize: 20
  });

  // Initialize population
  useEffect(() => {
    initializePopulation();
  }, []);

  const initializePopulation = () => {
    const pop = Array(20).fill(null).map((_, i) => ({
      id: `DNA-${Date.now()}-${i}`,
      name: `Process ${i + 1}`,
      fitness: Math.random() * 0.5 + 0.3,
      generation: 0,
      mutations: 0,
      genes: {
        efficiency: Math.random(),
        successRate: Math.random(),
        cost: Math.random(),
        speed: Math.random()
      }
    }));
    
    setPopulation(pop);
    updateStats(pop);
    setFitnessHistory([{ gen: 0, best: Math.max(...pop.map(p => p.fitness)), avg: pop.reduce((s, p) => s + p.fitness, 0) / pop.length }]);
  };

  const updateStats = (pop) => {
    const fitnesses = pop.map(p => p.fitness);
    const best = pop.reduce((a, b) => a.fitness > b.fitness ? a : b);
    
    setStats({
      bestFitness: Math.max(...fitnesses),
      avgFitness: fitnesses.reduce((a, b) => a + b, 0) / fitnesses.length,
      diversity: new Set(pop.map(p => Math.floor(p.fitness * 100))).size / 100,
      populationSize: pop.length
    });
    
    setBestProcess(best);
  };

  const evolveGeneration = () => {
    setPopulation(prev => {
      // Selection - keep top 20%
      const sorted = [...prev].sort((a, b) => b.fitness - a.fitness);
      const elites = sorted.slice(0, 4);
      
      // Breeding and mutation
      const newPop = [...elites];
      
      while (newPop.length < 20) {
        // Select two parents
        const p1 = sorted[Math.floor(Math.random() * 10)];
        const p2 = sorted[Math.floor(Math.random() * 10)];
        
        // Create offspring
        const child = {
          id: `DNA-${Date.now()}-${newPop.length}`,
          name: `Gen${generation + 1}-${newPop.length}`,
          generation: generation + 1,
          mutations: p1.mutations + 1,
          genes: {
            efficiency: (p1.genes.efficiency + p2.genes.efficiency) / 2 + (Math.random() - 0.5) * 0.1,
            successRate: (p1.genes.successRate + p2.genes.successRate) / 2 + (Math.random() - 0.5) * 0.1,
            cost: (p1.genes.cost + p2.genes.cost) / 2 + (Math.random() - 0.5) * 0.1,
            speed: (p1.genes.speed + p2.genes.speed) / 2 + (Math.random() - 0.5) * 0.1
          }
        };
        
        // Calculate fitness
        child.fitness = (
          Math.max(0, Math.min(1, child.genes.efficiency)) * 0.3 +
          Math.max(0, Math.min(1, child.genes.successRate)) * 0.4 +
          (1 - Math.max(0, Math.min(1, child.genes.cost))) * 0.2 +
          Math.max(0, Math.min(1, child.genes.speed)) * 0.1
        );
        
        newPop.push(child);
      }
      
      updateStats(newPop);
      setGeneration(g => g + 1);
      
      const fitnesses = newPop.map(p => p.fitness);
      setFitnessHistory(h => [...h, {
        gen: generation + 1,
        best: Math.max(...fitnesses),
        avg: fitnesses.reduce((a, b) => a + b, 0) / fitnesses.length
      }]);
      
      return newPop;
    });
  };

  const toggleEvolution = () => {
    setIsEvolving(!isEvolving);
  };

  const reset = () => {
    setGeneration(0);
    setIsEvolving(false);
    initializePopulation();
  };

  // Auto-evolve
  useEffect(() => {
    if (isEvolving) {
      const timer = setInterval(() => {
        evolveGeneration();
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [isEvolving, generation]);

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{label}</p>
          <p className={`text-2xl font-bold ${color}`}>{value}</p>
        </div>
        <Icon className={`w-8 h-8 ${color} opacity-60`} />
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Dna className="w-10 h-10 text-purple-600" />
            <h1 className="text-4xl font-bold text-gray-900">Automation DNA</h1>
          </div>
          <p className="text-gray-600">Business Process Evolution Engine</p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={toggleEvolution}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
                  isEvolving
                    ? 'bg-red-500 hover:bg-red-600 text-white'
                    : 'bg-green-500 hover:bg-green-600 text-white'
                }`}
              >
                {isEvolving ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                {isEvolving ? 'Pause' : 'Start'} Evolution
              </button>
              
              <button
                onClick={evolveGeneration}
                disabled={isEvolving}
                className="flex items-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg font-semibold transition-all"
              >
                <Zap className="w-5 h-5" />
                Single Step
              </button>
              
              <button
                onClick={reset}
                className="flex items-center gap-2 px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-lg font-semibold transition-all"
              >
                <RotateCcw className="w-5 h-5" />
                Reset
              </button>
            </div>
            
            <div className="text-right">
              <p className="text-sm text-gray-600">Current Generation</p>
              <p className="text-3xl font-bold text-purple-600">{generation}</p>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <StatCard
            icon={Award}
            label="Best Fitness"
            value={stats.bestFitness.toFixed(3)}
            color="text-green-600"
          />
          <StatCard
            icon={TrendingUp}
            label="Avg Fitness"
            value={stats.avgFitness.toFixed(3)}
            color="text-blue-600"
          />
          <StatCard
            icon={Users}
            label="Diversity"
            value={stats.diversity.toFixed(3)}
            color="text-purple-600"
          />
          <StatCard
            icon={Dna}
            label="Population"
            value={stats.populationSize}
            color="text-orange-600"
          />
        </div>

        {/* Fitness Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900">Fitness Evolution</h2>
          <div className="relative h-64">
            <svg width="100%" height="100%" viewBox="0 0 800 200" preserveAspectRatio="none">
              {/* Grid */}
              {[0, 0.25, 0.5, 0.75, 1].map(y => (
                <line
                  key={y}
                  x1="0"
                  y1={200 - y * 200}
                  x2="800"
                  y2={200 - y * 200}
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
              ))}
              
              {/* Best Fitness Line */}
              {fitnessHistory.length > 1 && (
                <polyline
                  points={fitnessHistory.map((h, i) => 
                    `${(i / Math.max(fitnessHistory.length - 1, 1)) * 800},${200 - h.best * 200}`
                  ).join(' ')}
                  fill="none"
                  stroke="#10b981"
                  strokeWidth="3"
                />
              )}
              
              {/* Avg Fitness Line */}
              {fitnessHistory.length > 1 && (
                <polyline
                  points={fitnessHistory.map((h, i) => 
                    `${(i / Math.max(fitnessHistory.length - 1, 1)) * 800},${200 - h.avg * 200}`
                  ).join(' ')}
                  fill="none"
                  stroke="#3b82f6"
                  strokeWidth="2"
                  strokeDasharray="5,5"
                />
              )}
            </svg>
            <div className="absolute top-2 right-2 flex gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-1 bg-green-500"></div>
                <span className="text-gray-600">Best</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-1 bg-blue-500" style={{borderTop: '2px dashed'}}></div>
                <span className="text-gray-600">Average</span>
              </div>
            </div>
          </div>
        </div>

        {/* Best Process Card */}
        {bestProcess && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl shadow-lg p-6 mb-6 border-2 border-green-200">
            <div className="flex items-center gap-3 mb-4">
              <Award className="w-8 h-8 text-green-600" />
              <h2 className="text-2xl font-bold text-gray-900">Best Process</h2>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div>
                <p className="text-sm text-gray-600">ID</p>
                <p className="font-mono text-sm text-gray-900">{bestProcess.id.slice(0, 16)}...</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Fitness</p>
                <p className="text-xl font-bold text-green-600">{bestProcess.fitness.toFixed(3)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Generation</p>
                <p className="text-xl font-bold text-purple-600">{bestProcess.generation}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Mutations</p>
                <p className="text-xl font-bold text-orange-600">{bestProcess.mutations}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Efficiency</p>
                <p className="text-xl font-bold text-blue-600">{bestProcess.genes.efficiency.toFixed(2)}</p>
              </div>
            </div>
          </div>
        )}

        {/* Population List */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900">Population ({population.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-h-96 overflow-y-auto">
            {population.slice().sort((a, b) => b.fitness - a.fitness).map((proc, idx) => (
              <div
                key={proc.id}
                className={`p-4 rounded-lg border-2 transition-all ${
                  idx === 0
                    ? 'bg-green-50 border-green-300'
                    : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-700">{proc.name}</span>
                  {idx === 0 && <Award className="w-4 h-4 text-green-600" />}
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-600">Fitness</span>
                    <span className="font-bold text-gray-900">{proc.fitness.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-600">Gen</span>
                    <span className="font-mono text-gray-700">{proc.generation}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div
                      className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all"
                      style={{ width: `${proc.fitness * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-600 text-sm">
          <p>🧬 Automation DNA: Business processes that EVOLVE!</p>
          <p className="mt-1">Made with ❤️ for the future of business automation</p>
        </div>
      </div>
    </div>
  );
};

export default AutomationDNADashboard;