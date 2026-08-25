// FILENAME: ModeToggle.tsx
// FILE PATH: /syntax_extracted/syntax_main/src/components/ModeToggle.tsx

import React, { useState } from 'react';

// Define the three core modes for Syntax AI automation aggression
type SyntaxMode = 'Nanny Mode' | 'Baby Steps' | 'Gloves Off Mode';

interface ModeToggleProps {
  // Function to call when the mode changes
  onModeChange: (mode: SyntaxMode) => void;
}

/**
 * Component for selecting the Syntax AI automation aggression level.
 * This controls the risk profile, from conservative checks to aggressive automation.
 */
const ModeToggle: React.FC<ModeToggleProps> = ({ onModeChange }) => {
  // Default to Nanny Mode for safety and helpfulness
  const [currentMode, setCurrentMode] = useState<SyntaxMode>('Nanny Mode');

  const handleModeChange = (newMode: SyntaxMode) => {
    setCurrentMode(newMode);
    onModeChange(newMode);
  };

  const modeDefinitions: Record<SyntaxMode, { description: string, color: string }> = {
    'Nanny Mode': {
      [span_0](start_span)// Conservative, requires confirmation, helpful for fragile users[span_0](end_span)
      description: 'Conservative, runs tests automatically, requires confirmation for major changes.',
      color: 'bg-green-500 hover:bg-green-600',
    },
    'Baby Steps': {
      [span_1](start_span)// Small incremental patches, suggest but don't apply automatically[span_1](end_span)
      description: 'Small, incremental patches. Suggests changes with diff explanations but does not auto-apply.',
      color: 'bg-yellow-500 hover:bg-yellow-600',
    },
    'Gloves Off Mode': {
      [span_2](start_span)// Aggressive automation, applies patches and merges on green tests[span_2](end_span)
      description: 'Aggressive automation. Applies patches and merges on green tests (requires user policy set).',
      color: 'bg-red-500 hover:bg-red-600',
    },
  };

  return (
    <div className="p-4 border-b border-gray-700">
      <h3 className="text-lg font-semibold mb-2">🤖 AI Aggression Mode</h3>
      <div className="flex space-x-2">
        {(Object.keys(modeDefinitions) as SyntaxMode[]).map((mode) => (
          <button
            key={mode}
            onClick={() => handleModeChange(mode)}
            className={`
              px-3 py-1 text-sm font-medium rounded-full transition-all duration-200
              ${currentMode === mode 
                ? `${modeDefinitions[mode].color} text-white shadow-lg`
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }
            `}
            title={modeDefinitions[mode].description}
          >
            {mode}
          </button>
        ))}
      </div>
      <p className="mt-2 text-sm text-gray-400">
        **[span_3](start_span)Current Policy**: {modeDefinitions[currentMode].description}[span_3](end_span)
      </p>
    </div>
  );
};

export default ModeToggle;
