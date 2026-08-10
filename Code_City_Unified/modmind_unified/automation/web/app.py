import logging

#!/usr/bin/env python3
"""
🧬 Automation DNA - Web Interface
Flask-based dashboard for visualizing process evolution
"""

import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import sys

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from dna_process import ProcessDNA, StepDNA, ConnectionDNA, ProcessType
from evolution_engine import EvolutionEngine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global evolution engine
current_engine = None

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/evolution')
def evolution():
    """Evolution tracker page"""
    return render_template('evolution.html')

@app.route('/marketplace')
def marketplace():
    """Process DNA marketplace"""
    return render_template('marketplace.html')

@app.route('/editor')
def editor():
    """Process editor"""
    return render_template('editor.html')

@app.route('/api/init_engine', methods=['POST'])
def init_engine():
    """Initialize evolution engine"""
    global current_engine
    
    data = request.json
    process_type = ProcessType(data.get('process_type', 'customer_onboarding'))
    population_size = data.get('population_size', 20)
    mutation_rate = data.get('mutation_rate', 0.3)
    breeding_rate = data.get('breeding_rate', 0.4)
    
    # Create base process
    base_process = ProcessDNA(
        process_type=process_type,
        name=data.get('process_name', f"{process_type.value} Process"),
        description=data.get('description', "Base process")
    )
    
    # Add default steps if none provided
    if not data.get('steps'):
        step1 = StepDNA("form", "Collect Info", "Gather initial data")
        step1.parameters = {"fields": ["name", "email"], "timeout": 300}
        
        step2 = StepDNA("verification", "Verify Data", "Confirm information")
        step2.parameters = {"retries": 2, "method": "email"}
        
        step3 = StepDNA("activation", "Activate", "Enable access")
        step3.parameters = {"default_role": "user"}
        
        base_process.add_step(step1)
        base_process.add_step(step2)
        base_process.add_step(step3)
        
        # Add connections
        base_process.add_connection(ConnectionDNA(step1.dna_id, step2.dna_id, "success"))
        base_process.add_connection(ConnectionDNA(step2.dna_id, step3.dna_id, "verified"))
    
    # Initialize engine
    current_engine = EvolutionEngine(
        population_size=population_size,
        mutation_rate=mutation_rate,
        breeding_rate=breeding_rate
    )
    current_engine.initialize_population(process_type, base_process)
    
    return jsonify({
        'status': 'success',
        'generation': current_engine.generation,
        'population_size': len(current_engine.population),
        'message': 'Evolution engine initialized'
    })

@app.route('/api/evolve', methods=['POST'])
def evolve():
    """Run next generation of evolution"""
    global current_engine
    
    if not current_engine:
        return jsonify({'status': 'error', 'message': 'Engine not initialized'}), 400
    
    # Generate fitness metrics (in real app, these would come from actual process execution)
    fitness_metrics = {}
    for i, process in enumerate(current_engine.population):
        # Simulate metrics based on current generation
        gen = current_engine.generation
        fitness_metrics[i] = {
            "efficiency": random.uniform(0.7 + (gen * 0.01), 0.9),
            "success_rate": random.uniform(0.8 + (gen * 0.005), 0.95),
            "cost": random.uniform(max(0.2, 0.8 - (gen * 0.02)), 0.6),
            "speed": random.uniform(0.6 + (gen * 0.02), 0.9)
        }
    
    current_engine.next_generation(fitness_metrics)
    
    stats = current_engine.get_statistics()
    best_process = current_engine.get_best_process()
    
    return jsonify({
        'status': 'success',
        'generation': current_engine.generation,
        'stats': stats,
        'best_process': {
            'name': best_process.name,
            'fitness': best_process.fitness_score,
            'generation': best_process.generation,
            'dna_id': best_process.dna_id
        }
    })

@app.route('/api/get_population')
def get_population():
    """Get current population data"""
    global current_engine
    
    if not current_engine:
        return jsonify({'status': 'error', 'message': 'Engine not initialized'}), 400
    
    population_data = []
    for process in current_engine.population:
        population_data.append({
            'dna_id': process.dna_id,
            'name': process.name,
            'fitness': process.fitness_score,
            'generation': process.generation,
            'steps': len(process.steps),
            'connections': len(process.connections)
        })
    
    return jsonify({
        'status': 'success',
        'generation': current_engine.generation,
        'population': population_data,
        'history': {
            'best': current_engine.best_fitness_history,
            'avg': current_engine.avg_fitness_history
        }
    })

@app.route('/api/get_process/<dna_id>')
def get_process(dna_id):
    """Get detailed process information"""
    global current_engine
    
    if not current_engine:
        return jsonify({'status': 'error', 'message': 'Engine not initialized'}), 400
    
    # Find process by DNA ID
    for process in current_engine.population:
        if process.dna_id == dna_id:
            return jsonify({
                'status': 'success',
                'process': process.to_dict()
            })
    
    return jsonify({'status': 'error', 'message': 'Process not found'}), 404

@app.route('/api/save_engine')
def save_engine():
    """Save current engine state"""
    global current_engine
    
    if not current_engine:
        return jsonify({'status': 'error', 'message': 'Engine not initialized'}), 400
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"engine_{timestamp}.json"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    current_engine.save_population(filepath)
    
    return jsonify({
        'status': 'success',
        'filename': filename,
        'path': filepath
    })

@app.route('/api/load_engine', methods=['POST'])
def load_engine():
    """Load engine from file"""
    global current_engine
    
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    current_engine = EvolutionEngine.load_population(filepath)
    
    return jsonify({
        'status': 'success',
        'generation': current_engine.generation,
        'population_size': len(current_engine.population),
        'message': 'Engine loaded successfully'
    })

@app.route('/api/ai_suggestion', methods=['POST'])
def ai_suggestion():
    """Get AI-powered mutation suggestions"""
    global current_engine
    
    if not current_engine:
        return jsonify({'status': 'error', 'message': 'Engine not initialized'}), 400
    
    data = request.json
    process_id = data.get('process_id')
    
    # Find the process
    target_process = None
    for process in current_engine.population:
        if process.dna_id == process_id:
            target_process = process
            break
    
    if not target_process:
        return jsonify({'status': 'error', 'message': 'Process not found'}), 404
    
    # Generate AI suggestions (simple version - in real app would use ML)
    suggestions = []
    
    # Analyze each step
    for step in target_process.steps:
        # Suggest parameter optimizations
        for param_name, param_value in step.parameters.items():
            if isinstance(param_value, (int, float)):
                suggestions.append({
                    'type': 'parameter_optimization',
                    'step_id': step.dna_id,
                    'step_name': step.name,
                    'parameter': param_name,
                    'current_value': param_value,
                    'suggested_value': param_value * random.uniform(0.9, 1.1),
                    'reason': f'Optimize {param_name} for better performance',
                    'impact': random.choice(['low', 'medium', 'high'])
                })
            elif isinstance(param_value, list):
                suggestions.append({
                    'type': 'list_optimization',
                    'step_id': step.dna_id,
                    'step_name': step.name,
                    'parameter': param_name,
                    'current_value': param_value,
                    'suggested_value': param_value + [f"new_field_{random.randint(1, 100)}"],
                    'reason': f'Add additional field to {param_name}',
                    'impact': 'medium'
                })
    
    # Suggest new steps
    if len(target_process.steps) < 5:  # Don't suggest too many
        suggestions.append({
            'type': 'new_step',
            'suggested_step': {
                'step_type': random.choice(['notification', 'approval', 'delay', 'integration']),
                'name': random.choice(['Send Notification', 'Manager Approval', 'Wait Period', 'CRM Sync']),
                'description': 'Enhance process with additional functionality',
                'parameters': {}
            },
            'reason': 'Add more robust process handling',
            'impact': 'high'
        })
    
    # Suggest connection optimizations
    if len(target_process.connections) > 1:
        suggestions.append({
            'type': 'connection_optimization',
            'reason': 'Optimize process flow between steps',
            'suggested_changes': [
                {'connection_type': 'parallel', 'description': 'Run steps in parallel for speed'},
                {'connection_type': 'conditional', 'description': 'Add conditional branching'}
            ],
            'impact': 'medium'
        })
    
    return jsonify({
        'status': 'success',
        'process_id': process_id,
        'process_name': target_process.name,
        'suggestions': suggestions,
        'confidence': random.uniform(0.7, 0.95)
    })

@app.route('/api/marketplace/list')
def marketplace_list():
    """List available process DNA in marketplace"""
    # In a real app, this would query a database
    # For demo, return some sample data
    
    sample_processes = [
        {
            'id': 'MP-001',
            'name': 'E-Commerce Onboarding',
            'type': 'customer_onboarding',
            'fitness': 0.92,
            'price': 49.99,
            'vendor': 'AutomationDNA Inc.',
            'description': 'Optimized e-commerce customer onboarding with 30% higher conversion',
            'industry': 'E-Commerce',
            'downloads': 1284,
            'rating': 4.8
        },
        {
            'id': 'MP-002',
            'name': 'Enterprise Sales Pipeline',
            'type': 'sales_pipeline',
            'fitness': 0.89,
            'price': 99.99,
            'vendor': 'SalesGenius',
            'description': 'High-performance sales pipeline with AI-powered lead scoring',
            'industry': 'Sales',
            'downloads': 872,
            'rating': 4.6
        },
        {
            'id': 'MP-003',
            'name': 'SaaS Support Workflow',
            'type': 'support_ticket',
            'fitness': 0.95,
            'price': 79.99,
            'vendor': 'SupportDNA',
            'description': 'Optimized support workflow reducing resolution time by 40%',
            'industry': 'Customer Support',
            'downloads': 2156,
            'rating': 4.9
        },
        {
            'id': 'MP-004',
            'name': 'Manufacturing QA Process',
            'type': 'data_processing',
            'fitness': 0.87,
            'price': 149.99,
            'vendor': 'IndustryDNA',
            'description': 'Quality assurance process for manufacturing with defect detection',
            'industry': 'Manufacturing',
            'downloads': 432,
            'rating': 4.5
        },
        {
            'id': 'MP-005',
            'name': 'HR Onboarding Automation',
            'type': 'hr_onboarding',
            'fitness': 0.91,
            'price': 39.99,
            'vendor': 'HRDNA Solutions',
            'description': 'Complete HR onboarding with document management and compliance',
            'industry': 'Human Resources',
            'downloads': 1768,
            'rating': 4.7
        }
    ]
    
    return jsonify({
        'status': 'success',
        'processes': sample_processes,
        'total': len(sample_processes)
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    logging.info("🧬 Automation DNA Web Interface - Starting...")
    logging.info("🌐 Open your browser to: http://localhost:5000")
    logging.info("🚀 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)