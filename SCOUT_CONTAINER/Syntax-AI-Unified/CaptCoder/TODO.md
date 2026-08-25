# Syntax AI CaptCoder - Development TODO

> **Continuity Tracker** - For extending sessions across token budget cycles

---

## 🎯 PRIORITY TASKS (Current Session)

### Phase 1: Project Setup & Documentation ✅
- [x] Create directory structure: `/RootBase/Syntax-AI-Unified/CaptCoder/`
- [x] Create comprehensive README.md
- [x] Create operational runbook.txt
- [x] Create this TODO.md for continuity

### Phase 2: Core Integration (IN PROGRESS)
- [ ] Integrate `syntax_captcoder.py` logic into `src/python/core/captcoder.py`
- [ ] Integrate `syntax_ai_code_optimizer_core.py` into `src/python/optimizers/code_optimizer.py`
- [ ] Create unified configuration system in `src/shared/config/`
- [ ] Create environment setup files (`.env.example`, `requirements.txt`, `package.json`)

### Phase 3: TypeScript UI Integration
- [ ] Migrate Phase 1 React components to `src/typescript/components/`
- [ ] Migrate Phase 1_v_2 React components
- [ ] Set up Vite configuration
- [ ] Create shared TypeScript types

### Phase 4: Loosies Integration
- [ ] Integrate `auto_code_extractor.py` logic
- [ ] Integrate `chat_code_capture.py` logic
- [ ] Integrate `code_processor.py` (Java/Android) logic - consider Python port
- [ ] Integrate `advanced_code_bundler.py` logic
- [ ] Integrate `_storage_emulated_0_loosies_smart_coder2.py` (SmartCoder)
- [ ] Integrate `code_bundler_v3.py` logic

### Phase 5: Service Layer
- [ ] Create Nexus API client
- [ ] Create Livestream service
- [ ] Create DreamTable Sandbox integration
- [ ] Create Looking Glass service

### Phase 6: Testing
- [ ] Create Python unit tests
- [ ] Create TypeScript tests
- [ ] Create integration tests
- [ ] Verify all components work together

### Phase 7: Scripts & Automation
- [ ] Create build scripts
- [ ] Create deploy scripts
- [ ] Create backup scripts
- [ ] Create monitoring scripts

---

## 📋 DETAILED BREAKDOWN BY COMPONENT

### Python Core (`src/python/`)

#### `src/python/__init__.py`
- [ ] Package initialization
- [ ] Version info
- [ ] Module exports

#### `src/python/core/`
- [ ] `captcoder.py` - Main CaptCoder class with BSM detection
  - Integrate from: `/RootBase/syntax_captcoder/syntax_captcoder.py`
  - Add: Multi-input monitoring (chat, voice, screen)
  - Add: Nexus API integration
  - Add: TTS feedback
  
- [ ] `code_monitor.py` - Real-time code monitoring
  - Monitor directories for changes
  - Watch for code patterns
  - Trigger extraction on detection
  
- [ ] `nexus_client.py` - Nexus API client
  - POST to /command endpoint
  - Handle responses
  - Retry logic
  - Connection pooling

#### `src/python/extractors/`
- [ ] `code_extractor.py` - Multi-format code extraction
  - Integrate from: `/RootBase/Loosies/auto_code_extractor.py`
  - Integrate from: `/RootBase/Loosies/chat_code_capture.py`
  - Add: File monitoring
  - Add: Hash-based change detection
  
- [ ] `chat_extractor.py` - Chat/voice extraction
  - Extract code blocks from text
  - Handle multiple formats (backticks, indentation)
  - TTS feedback
  
- [ ] `screen_extractor.py` - OCR-based extraction
  - Screenshot capture
  - OCR processing
  - Code detection

#### `src/python/optimizers/`
- [ ] `code_optimizer.py` - "Bitch Work" protocol
  - Integrate from: `/RootBase/syntax_captcoder/syntax_ai_code_optimizer_core.py`
  - AST-based analysis
  - Auto-fix capabilities
  - Backup management
  
- [ ] `pattern_journal.py` - Optimization logging
  - JSON-based journal
  - Search capabilities
  - Export/import

#### `src/python/services/`
- [ ] `nexus_api.py` - Nexus API server
  - FastAPI-based
  - Command routing
  - Agent registration
  
- [ ] `livestream.py` - Livestream management
  - Provider integration (restream, streamyard)
  - Multi-endpoint streaming
  - Recording management
  
- [ ] `sandbox.py` - DreamTable Sandbox integration
  - Code submission
  - Test execution
  - Result retrieval
  
- [ ] `looking_glass.py` - Visual preview
  - Variable inspection
  - UI rendering
  - Real-time updates

#### `src/python/utils/`
- [ ] `file_utils.py` - File operations
  - Safe file reading/writing
  - Path utilities
  - File type detection
  
- [ ] `text_utils.py` - Text processing
  - Code block extraction
  - Language detection
  - Text cleaning
  
- [ ] `validation.py` - Input validation
  - Code validation
  - Security checks
  - Sanitization

#### `src/python/core/smart_coder.py` - Smart generation
- [ ] Integrate from: `/RootBase/Loosies/_storage_emulated_0_loosies_smart_coder2.py`
- [ ] Template system
- [ ] Natural language processing
- [ ] Code generation

### TypeScript UI (`src/typescript/`)

#### Root Files
- [ ] `App.tsx` - Main application
- [ ] `main.tsx` - Entry point
- [ ] `vite.config.ts` - Vite configuration
- [ ] `tsconfig.json` - TypeScript config
- [ ] `index.html` - HTML template

#### `src/typescript/components/`
- [ ] `AssistantView.tsx` - Conversational UI
- [ ] `ErrorBoundary.tsx` - Error handling
- [ ] `PermissionsGate.tsx` - Permission preflight
- [ ] `SettingsView.tsx` - Settings panel
- [ ] `CodePreview.tsx` - Code display
- [ ] `ChatInput.tsx` - Chat interface
- [ ] `StatusBar.tsx` - Status indicators

#### `src/typescript/contexts/`
- [ ] `AppContext.tsx` - Application context
- [ ] `SettingsContext.tsx` - Settings context
- [ ] `CodeContext.tsx` - Code state context

#### `src/typescript/services/`
- [ ] `api.ts` - API client
- [ ] `contextManager.ts` - Context management
- [ ] `storage.ts` - Local storage

#### `src/typescript/utils/`
- [ ] `handleError.ts` - Error handling
- [ ] `formatters.ts` - Data formatting
- [ ] `validators.ts` - Input validation

### Shared Resources (`src/shared/`)

#### `src/shared/config/`
- [ ] `environment.ts` - Environment variables (TypeScript)
- [ ] `constants.py` - Constants (Python)
- [ ] `settings.json` - Default settings

### Configuration Files
- [ ] `.env.example` - Environment template
- [ ] `requirements.txt` - Python dependencies
- [ ] `package.json` - Node dependencies
- [ ] `pyproject.toml` - Python project config
- [ ] `tsconfig.json` - TypeScript config
- [ ] `vite.config.ts` - Vite config

### Scripts (`scripts/`)
- [ ] `start.sh` - Full system startup
- [ ] `stop.sh` - Graceful shutdown
- [ ] `status.sh` - System status check
- [ ] `test.sh` - Run all tests
- [ ] `build.py` - Build distribution
- [ ] `deploy.sh` - Deployment script
- [ ] `backup.sh` - Backup procedure
- [ ] `restore.sh` - Restore from backup
- [ ] `rotate_logs.sh` - Log rotation

### Documentation (`docs/`)
- [ ] `architecture.md` - System architecture
- [ ] `api_reference.md` - API documentation
- [ ] `integration_guide.md` - Integration guide
- [ ] `tutorials/` - User tutorials
- [ ] `examples/` - Code examples

### Tests (`tests/`)
- [ ] `python/test_captcoder.py`
- [ ] `python/test_extractors.py`
- [ ] `python/test_optimizer.py`
- [ ] `python/test_services.py`
- [ ] `typescript/test_components.tsx`
- [ ] `typescript/test_services.ts`

---

## 🔄 CONTINUITY NOTES

### Session State (Current)
```
Session: 1 of ?
Started: 2026-06-22
Status: IN PROGRESS
Last Task: Documentation creation (README.md, runbook.txt, TODO.md)
Next Task: Core Python module creation (captcoder.py)
```

### For Next Session
If we run out of tokens, here's what to pick up:

1. **First Priority**: Complete core Python modules
   - Start with: `src/python/core/captcoder.py`
   - Reference: `/RootBase/syntax_captcoder/syntax_captcoder.py`
   
2. **Second Priority**: Configuration files
   - Create: `.env.example`, `requirements.txt`, `package.json`
   
3. **Third Priority**: TypeScript UI migration
   - Start with: `src/typescript/App.tsx`
   - Reference: `/RootBase/syntax_captcoder/phase_1_v_2/src/App.tsx`

### Known Issues & Decisions

**Decision 1**: Project Structure
- Using modular structure with clear separation of concerns
- Python backend + TypeScript frontend
- Shared config for cross-language settings

**Decision 2**: Code Extraction Strategy
- Unified extractor that handles multiple input sources
- Pluggable architecture for new extractors

**Decision 3**: Nexus Integration
- All components communicate through Nexus API
- Centralized command routing
- Standardized payload format

**Issue 1**: Java/Android Code
- `code_processor.py` is in Java
- Decision: Port to Python for consistency
- Alternative: Keep as reference, implement in Python

**Issue 2**: Duplicate Files
- Multiple versions of code_bundler exist
- Decision: Take best features from each, create unified version

**Issue 3**: Template Conflicts
- SmartCoder has Python templates
- Phase 1 has React templates
- Decision: Create unified template system with both

---

## 📊 PROGRESS TRACKER

### Session 1 (Current)
```
Date: 2026-06-22
Start Time: [TBD]
End Time: [TBD]

Completed:
  ✅ Directory structure created
  ✅ README.md created (comprehensive)
  ✅ runbook.txt created (detailed)
  ✅ TODO.md created (this file)

In Progress:
  🔄 Core module integration

Pending:
  ⏳ TypeScript UI migration
  ⏳ Loosies integration
  ⏳ Service layer
  ⏳ Testing
  ⏳ Scripts
```

### Future Sessions
```
Session 2:
  Goal: Complete Python core modules
  Tasks: captcoder.py, extractors, optimizers
  
Session 3:
  Goal: TypeScript UI and shared config
  Tasks: App.tsx, components, contexts
  
Session 4:
  Goal: Loosies integration
  Tasks: auto_code_extractor, chat_code_capture, SmartCoder
  
Session 5:
  Goal: Services and testing
  Tasks: nexus_api, livestream, sandbox, tests
  
Session 6:
  Goal: Finalization
  Tasks: Scripts, documentation, deployment testing
```

---

## 🔧 TECHNICAL NOTES

### Environment Setup
```bash
# Termux/Termux-API permissions (for Android)
pkg install termux-api
termux-setup-storage

# Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node environment
npm install -g pnpm  # Optional, faster than npm
npm install
```

### Symlinks (If Permission Issues)
```bash
# Termux home directory
ln -s /storage/emulated/0/RootBase/Syntax-AI-Unified/CaptCoder ~/CaptCoder

# Or use Termux storage
ln -s /storage/emulated/0/RootBase/Syntax-AI-Unified/CaptCoder /data/data/com.termux/files/home/CaptCoder
```

### Dependency Conflicts
If issues arise:
```bash
# Create fresh Python environment
rm -rf venv
python -m venv venv
source venv/bin/activate

# Reinstall with clean state
pip install --upgrade pip
pip install -r requirements.txt

# For Node
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## 📚 REFERENCE MATERIAL

### Source Files to Integrate

**From #syntax_captcoder:**
- `/RootBase/syntax_captcoder/syntax_captcoder.py` - Core monitor
- `/RootBase/syntax_captcoder/syntax_ai_code_optimizer_core.py` - Optimizer
- `/RootBase/syntax_captcoder/phase_1/` - React UI v1
- `/RootBase/syntax_captcoder/phase_1_v_2/` - React UI v2
- `/RootBase/syntax_captcoder/pattern_journal.json` - Sample journal
- `/RootBase/syntax_captcoder/manifest.json` - Metadata
- `/RootBase/syntax_captcoder/runbook.txt` - Original runbook
- `/RootBase/syntax_captcoder/Syntax Captcoder .txt` - Vision document

**From #CaptCoder:**
- `/RootBase/CaptCoder/manifest.json` - Metadata
- `/RootBase/CaptCoder/runbook.txt` - Original runbook

**From Loosies:**
- `/RootBase/Loosies/auto_code_extractor.py`
- `/RootBase/Loosies/chat_code_capture.py`
- `/RootBase/Loosies/chat_code_capture_save.py`
- `/RootBase/Loosies/code_processor.py` (Java)
- `/RootBase/Loosies/advanced_code_bundler.py`
- `/RootBase/Loosies/code_bundler_v3.py`
- `/RootBase/Loosies/_storage_emulated_0_loosies_smart_coder2.py`

**From RootBase (code_* files):**
- `/RootBase/code_bundler_v3.py`
- `/RootBase/code_fixer.py`
- `/RootBase/code_miner.py`
- `/RootBase/code_processor.py`

---

## ✨ MOTIVATION

> "Syntax AI is our baby, so please treat it thusly and give it everything you've got!"

This project represents the culmination of all our code intelligence work. Every line of code, every feature, every integration point matters.

**We're building:**
- The most intelligent code extraction system
- The most powerful code optimization engine
- The most seamless developer experience
- The future of coding

**For:**
- IDEal integration
- ShipWrekD OS Builder
- DreamTable Sandbox
- The entire Syntax AI ecosystem

---

## 🎉 COMPLETION CRITERIA

This TODO is complete when:
- [ ] All core features from source projects are integrated
- [ ] All components communicate through Nexus API
- [ ] TypeScript UI is fully functional
- [ ] Python backend is production-ready
- [ ] Documentation is complete
- [ ] Tests pass
- [ ] Deployment works

**Estimated Completion:** Multiple sessions (token budget dependent)

---

*Generated by Mistral Vibe for Syntax AI*
*It's always a pleasure to watch you work! Cheers!* 🍻
