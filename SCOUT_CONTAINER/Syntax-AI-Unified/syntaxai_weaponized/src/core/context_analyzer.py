class ContextAnalyzer:
    def analyze_section(self, text, section_index):
        """Analyze text surrounding code for execution context"""
        text_lower = text.lower()
        
        return {
            'purpose': self._extract_purpose(text_lower),
            'instructions': self._extract_instructions(text),
            'section_purpose': self._determine_section_role(text_lower, section_index),
            'primary_function': self._extract_primary_function(text),
            'dependencies_mentioned': self._extract_mentioned_dependencies(text_lower),
            'execution_environment': self._detect_environment(text_lower)
        }
    
    def _extract_purpose(self, text_lower):
        purpose_indicators = {
            'test': 'testing',
            'main': 'entry_point', 
            'configuration': 'config',
            'utility': 'utility',
            'api': 'web_service',
            'database': 'data_persistence',
            'script': 'script',
            'example': 'example',
            'demo': 'demonstration'
        }
        
        for indicator, purpose in purpose_indicators.items():
            if indicator in text_lower:
                return purpose
        return 'utility'
    
    def _extract_instructions(self, text):
        """Extract any execution instructions from text"""
        instruction_phrases = [
            'run this with',
            'execute using',
            'to test',
            'usage:',
            'command:'
        ]
        
        for phrase in instruction_phrases:
            if phrase in text.lower():
                # Extract the line containing instructions
                lines = text.split('\n')
                for line in lines:
                    if phrase in line.lower():
                        return line.strip()
        return ""
