// 🧬 Automation DNA - Main JavaScript

// Global variables
let currentEngine = null;
let evolutionInterval = null;

// DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🧬 Automation DNA Web Interface loaded!');
    
    // Initialize page-specific functionality
    const page = document.body.getAttribute('data-page');
    if (page) {
        switch(page) {
            case 'evolution':
                initEvolutionPage();
                break;
            case 'marketplace':
                initMarketplacePage();
                break;
            case 'editor':
                initEditorPage();
                break;
        }
    }
});

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Evolution Page Functions
function initEvolutionPage() {
    console.log('Initializing Evolution Page');
    
    // Set up event listeners
    document.getElementById('startEvolutionBtn')?.addEventListener('click', openStartEvolutionModal);
    document.getElementById('closeStartModal')?.addEventListener('click', () => closeModal('startEvolutionModal'));
    document.getElementById('cancelStartEvolution')?.addEventListener('click', () => closeModal('startEvolutionModal'));
    document.getElementById('confirmStartEvolution')?.addEventListener('click', startEvolution);
    document.getElementById('evolveNextGen')?.addEventListener('click', evolveNextGeneration);
    document.getElementById('stopEvolution')?.addEventListener('click', stopEvolution);
    
    // Load any existing engine
    loadEngineState();
}

async function startEvolution() {
    const processType = document.getElementById('processType').value;
    const processName = document.getElementById('processName').value;
    const populationSize = document.getElementById('populationSize').value;
    const mutationRate = document.getElementById('mutationRate').value;
    const breedingRate = document.getElementById('breedingRate').value;
    const description = document.getElementById('description').value;
    
    try {
        const response = await fetch('/api/init_engine', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                process_type: processType,
                process_name: processName,
                population_size: parseInt(populationSize),
                mutation_rate: parseFloat(mutationRate),
                breeding_rate: parseFloat(breedingRate),
                description: description
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            currentEngine = {
                generation: data.generation,
                populationSize: data.population_size
            };
            
            updateEvolutionUI();
            addActivityLog('Evolution started', `Initialized ${processType} evolution with ${populationSize} processes`);
            
            closeModal('startEvolutionModal');
            
            // Start auto-evolution
            startAutoEvolution();
        } else {
            showError('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error starting evolution:', error);
        showError('Failed to start evolution: ' + error.message);
    }
}

async function evolveNextGeneration() {
    if (!currentEngine) {
        showError('Please start an evolution first!');
        return;
    }
    
    try {
        const response = await fetch('/api/evolve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            currentEngine.generation = data.generation;
            updateEvolutionUI();
            updateEvolutionChart(data.stats);
            addActivityLog('Generation completed', `Reached generation ${data.generation} with best fitness ${data.stats.best_fitness.toFixed(3)}`);
        } else {
            showError('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error evolving:', error);
        showError('Failed to evolve: ' + error.message);
    }
}

function startAutoEvolution() {
    if (evolutionInterval) {
        stopEvolution();
    }
    
    // Evolve every 2 seconds for demo
    evolutionInterval = setInterval(evolveNextGeneration, 2000);
    
    document.getElementById('evolveNextGen').disabled = true;
    document.getElementById('stopEvolution').disabled = false;
    addActivityLog('Auto-evolution started', 'Processes will evolve automatically every 2 seconds');
}

function stopEvolution() {
    if (evolutionInterval) {
        clearInterval(evolutionInterval);
        evolutionInterval = null;
    }
    
    document.getElementById('evolveNextGen').disabled = false;
    document.getElementById('stopEvolution').disabled = true;
    addActivityLog('Auto-evolution stopped', 'Manual evolution control restored');
}

async function updateEvolutionUI() {
    try {
        const response = await fetch('/api/get_population');
        const data = await response.json();
        
        if (data.status === 'success') {
            // Update stats
            document.getElementById('currentGeneration').textContent = data.generation;
            document.getElementById('populationSize').textContent = data.population.length;
            document.getElementById('bestFitness').textContent = data.history.best[data.history.best.length - 1].toFixed(3);
            document.getElementById('avgFitness').textContent = data.history.avg[data.history.avg.length - 1].toFixed(3);
            
            // Update population list
            updatePopulationList(data.population);
        }
    } catch (error) {
        console.error('Error updating UI:', error);
        showError('Failed to update UI: ' + error.message);
    }
}

function updatePopulationList(population) {
    const populationList = document.getElementById('populationList');
    populationList.innerHTML = '';
    
    // Sort by fitness (highest first)
    population.sort((a, b) => b.fitness - a.fitness);
    
    population.forEach(process => {
        const processItem = document.createElement('div');
        processItem.className = 'process-item';
        processItem.innerHTML = `
            <div class="process-info">
                <div class="process-name">${process.name}</div>
                <div class="process-dna">DNA: ${process.dna_id.substring(0, 16)}...</div>
            </div>
            <div class="process-fitness">
                Fitness: <span class="fitness-value">${process.fitness.toFixed(3)}</span>
            </div>
            <div class="process-actions">
                <button class="btn btn-sm btn-secondary" onclick="viewProcess('${process.dna_id}')">
                    <i class="fas fa-eye"></i> View
                </button>
                <button class="btn btn-sm btn-primary" onclick="getAISuggestions('${process.dna_id}')">
                    <i class="fas fa-robot"></i> AI Suggest
                </button>
            </div>
        `;
        
        // Add color based on fitness
        const fitnessValue = processItem.querySelector('.fitness-value');
        if (process.fitness > 0.9) {
            fitnessValue.classList.add('high-fitness');
        } else if (process.fitness > 0.7) {
            fitnessValue.classList.add('medium-fitness');
        } else {
            fitnessValue.classList.add('low-fitness');
        }
        
        populationList.appendChild(processItem);
    });
}

function updateEvolutionChart(stats) {
    // This would be implemented with Chart.js
    console.log('Update chart with stats:', stats);
}

async function viewProcess(dnaId) {
    try {
        const response = await fetch(`/api/get_process/${dnaId}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            showProcessDetails(data.process);
        } else {
            showError('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error viewing process:', error);
        showError('Failed to view process: ' + error.message);
    }
}

function showProcessDetails(process) {
    // Display process details in a modal
    const modalContent = document.getElementById('processDetailsContent');
    
    let html = `
        <h3>${process.name}</h3>
        <p class="process-dna-id">DNA ID: ${process.dna_id}</p>
        <p class="process-description">${process.description}</p>
        
        <div class="process-metrics">
            <div class="metric">
                <span class="metric-label">Generation:</span>
                <span class="metric-value">${process.generation}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Fitness:</span>
                <span class="metric-value">${process.fitness_score.toFixed(3)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Steps:</span>
                <span class="metric-value">${process.steps.length}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Connections:</span>
                <span class="metric-value">${process.connections.length}</span>
            </div>
        </div>
        
        <h4>Steps:</h4>
        <div class="steps-list">
    `;
    
    process.steps.forEach(step => {
        html += `
            <div class="step-item">
                <div class="step-name">${step.name}</div>
                <div class="step-type">${step.step_type}</div>
                <div class="step-description">${step.description}</div>
                <div class="step-parameters">
                    Parameters: ${JSON.stringify(step.parameters)}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    if (process.mutations.length > 0) {
        html += '<h4>Mutations:</h4><div class="mutations-list">';
        process.mutations.forEach(mutation => {
            html += `
                <div class="mutation-item">
                    <div class="mutation-type">${mutation.type}</div>
                    <div class="mutation-time">${mutation.timestamp}</div>
                    <div class="mutation-description">${mutation.description}</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    modalContent.innerHTML = html;
    openModal('processDetailsModal');
}

// Marketplace Functions
function initMarketplacePage() {
    console.log('Initializing Marketplace Page');
    loadMarketplaceItems();
}

async function loadMarketplaceItems() {
    try {
        const response = await fetch('/api/marketplace/list');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayMarketplaceItems(data.processes);
        } else {
            showError('Error: ' + data.message);
        }
    } catch (error) {
        console.error('Error loading marketplace:', error);
        showError('Failed to load marketplace: ' + error.message);
    }
}

function displayMarketplaceItems(processes) {
    const marketplaceGrid = document.getElementById('marketplaceGrid');
    marketplaceGrid.innerHTML = '';
    
    processes.forEach(process => {
        const processCard = document.createElement('div');
        processCard.className = 'marketplace-card';
        processCard.innerHTML = `
            <div class="marketplace-card-header">
                <div class="marketplace-card-type">${formatProcessType(process.type)}</div>
                <div class="marketplace-card-rating">
                    <i class="fas fa-star"></i> ${process.rating}
                </div>
            </div>
            <div class="marketplace-card-body">
                <h3 class="marketplace-card-title">${process.name}</h3>
                <p class="marketplace-card-description">${process.description}</p>
                <div class="marketplace-card-metrics">
                    <span><i class="fas fa-chart-line"></i> Fitness: ${process.fitness}</span>
                    <span><i class="fas fa-download"></i> ${process.downloads} downloads</span>
                </div>
            </div>
            <div class="marketplace-card-footer">
                <div class="marketplace-card-price">$${process.price.toFixed(2)}</div>
                <button class="btn btn-primary" onclick="purchaseProcess('${process.id}')">
                    <i class="fas fa-shopping-cart"></i> Purchase
                </button>
            </div>
        `;
        
        marketplaceGrid.appendChild(processCard);
    });
}

function formatProcessType(type) {
    return type.replace(/_/g, ' ').replace(/\w\S*/g, txt => 
        txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    );
}

function purchaseProcess(processId) {
    alert(`Process ${processId} purchased! (Demo only)`);
    addActivityLog('Process purchased', `Acquired process ${processId} from marketplace`);
}

// Editor Functions
function initEditorPage() {
    console.log('Initializing Editor Page');
    
    // Set up editor functionality
    document.getElementById('addStepBtn')?.addEventListener('click', addStepToProcess);
    document.getElementById('saveProcessBtn')?.addEventListener('click', saveProcess);
}

function addStepToProcess() {
    alert('Add step functionality (to be implemented)');
}

function saveProcess() {
    alert('Save process functionality (to be implemented)');
}

// Utility Functions
function updateDashboardStats() {
    if (currentEngine) {
        document.getElementById('currentGeneration')?.textContent = currentEngine.generation;
        document.getElementById('populationSize')?.textContent = currentEngine.populationSize;
    }
}

function addActivityLog(title, description) {
    const activityList = document.getElementById('activityList');
    if (!activityList) return;
    
    const time = new Date().toLocaleTimeString();
    
    const activityItem = document.createElement('div');
    activityItem.className = 'activity-item';
    activityItem.innerHTML = `
        <div class="activity-icon">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="activity-content">
            <div class="activity-title">${title}</div>
            <div class="activity-time">${time}</div>
            <div class="activity-description">${description}</div>
        </div>
    `;
    
    activityList.insertBefore(activityItem, activityList.firstChild);
}

function loadEngineState() {
    // In a real app, this would load from localStorage or API
    // For demo, we'll just set some default values
    updateDashboardStats();
}

function showError(message) {
    alert(`Error: ${message}`);
    console.error(message);
}

// Export for other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initEvolutionPage,
        initMarketplacePage,
        initEditorPage
    };
}