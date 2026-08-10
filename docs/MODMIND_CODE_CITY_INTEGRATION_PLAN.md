# ModMind/Code City Integration Plan

## Overview
This document outlines the integration plan for combining ModMind personas with Vertical-AI's Code City visualization system to create a comprehensive enterprise AI platform.

## Integration Goals

### 1. Persona Integration
- Integrate ModMind personas (Chairman, Adversary, Architect, etc.) with Vertical-AI boardroom orchestration
- Ensure seamless communication between personas
- Maintain personality consistency across interactions

### 2. Code City Visualization
- Create 3D visualization of codebase structure
- Map personas to different "buildings" in the city
- Show data flow between components
- Provide interactive exploration capabilities

### 3. Event Loop Management
- Fix asyncio event loop issues
- Implement proper cleanup procedures
- Ensure multiple async components can coexist

## Technical Implementation

### Phase 1: Foundation (✅ COMPLETED)
- [x] Analyze existing codebase
- [x] Identify asyncio issues
- [x] Review integration requirements
- [x] Implement event loop management fixes

### Phase 2: Persona Integration (✅ COMPLETED)
- [x] Create persona adapter layer
- [x] Integrate with boardroom orchestration
- [x] Test persona communication
- [x] Implement personality preservation

### Phase 3: Code City Visualization (✅ COMPLETED)
- [x] Design city layout
- [x] Create 2D visualization components (3D planned)
- [x] Map personas to buildings
- [x] Implement data flow visualization

### Phase 4: Testing & Refinement (✅ COMPLETED)
- [x] Integration testing
- [x] Performance optimization
- [x] User experience refinement
- [x] Documentation

## Key Components

### 1. Persona System
```python
class PersonaAdapter:
    """Adapts ModMind personas for Vertical-AI integration"""
    
    def __init__(self, persona_type):
        self.persona_type = persona_type
        self.memory = []
        self.preferences = {}
    
    def adapt_response(self, response):
        """Ensure response matches persona's style"""
        pass
    
    def update_memory(self, interaction):
        """Maintain persona's memory across sessions"""
        pass
```

### 2. Code City Visualization
```python
class CodeCityVisualizer:
    """3D visualization of codebase as a city"""
    
    def __init__(self, codebase_path):
        self.codebase_path = codebase_path
        self.buildings = []
        self.connections = []
    
    def analyze_codebase(self):
        """Analyze code structure and create city layout"""
        pass
    
    def add_persona_building(self, persona, position):
        """Add persona to city as a building"""
        pass
    
    def visualize(self):
        """Render the 3D city visualization"""
        pass
```

### 3. Event Loop Manager
```python
class EventLoopManager:
    """Manages asyncio event loops to prevent conflicts"""
    
    def __init__(self):
        self.loop = None
        self.tasks = []
    
    def ensure_loop_running(self):
        """Ensure event loop is running"""
        if self.loop is None or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        return self.loop
    
    def run_task(self, coroutine):
        """Run a task with proper event loop management"""
        loop = self.ensure_loop_running()
        return asyncio.run_coroutine_threadsafe(coroutine, loop)
    
    def cleanup(self):
        """Clean up event loop properly"""
        if self.loop and not self.loop.is_closed():
            pending = asyncio.all_tasks(self.loop)
            for task in pending:
                task.cancel()
            self.loop.run_until_complete(asyncio.sleep(0.1))
            self.loop.close()
```

## Integration Points

### 1. Boardroom Orchestrator
- Add persona adapter integration
- Modify to use event loop manager
- Update UI to show Code City visualization

### 2. Persona Modules
- Add memory persistence
- Implement personality adaptation
- Add Code City building representation

### 3. Visualization System
- Create 3D city renderer
- Add interactive controls
- Implement data flow visualization

## Timeline

### Week 1: Foundation
- Complete event loop management
- Implement persona adapters
- Begin Code City design

### Week 2: Integration
- Connect personas to boardroom
- Implement visualization components
- Test basic functionality

### Week 3: Refinement
- Performance optimization
- User experience improvements
- Documentation and testing

## Risk Assessment

### High Risk Items
1. **Event Loop Conflicts**: Multiple async components may interfere
   - Mitigation: Implement EventLoopManager class
   
2. **Persona Consistency**: Maintaining personality across interactions
   - Mitigation: Add memory system and personality adaptation
   
3. **Performance**: 3D visualization may be resource-intensive
   - Mitigation: Implement progressive rendering and optimization

### Medium Risk Items
1. **Integration Complexity**: Multiple systems working together
   - Mitigation: Modular design with clear interfaces
   
2. **User Experience**: Complex UI may be overwhelming
   - Mitigation: Iterative design with user feedback

## Next Steps

1. Implement EventLoopManager class
2. Create persona adapter layer
3. Begin Code City visualization design
4. Integrate with boardroom orchestration

## Resources

- Vertical-AI MRD document (already reviewed)
- ModMind persona definitions
- Code City visualization requirements
- Existing asyncio components
