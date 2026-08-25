// FILENAME: App.tsx
import React, { useState } from 'react';
// NOTE: ModeToggle component file must also be created separately
// import ModeToggle from './components/ModeToggle'; 

type SyntaxMode = 'Nanny Mode' | 'Baby Steps' | 'Gloves Off Mode';

const App: React.FC = () => {
  const [activeMode, setActiveMode] = useState<SyntaxMode>('Nanny Mode');
  const [vibe, setVibe] = useState('');

  const handleModeChange = (mode: SyntaxMode) => {
    setActiveMode(mode);
    console.log(`Global AI Mode set to: ${mode}`);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans p-4">
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold text-blue-400">ModMind / EquiNex: Syntax AI</h1>
      </header>
      
      {/* <ModeToggle onModeChange={handleModeChange} /> */}
      
      <div className="p-4 bg-gray-800 rounded-xl shadow-xl">
        <h3 className="text-lg font-semibold mb-2">✨ Vibe Vault Input</h3>
        <textarea
          value={vibe}
          onChange={(e) => setVibe(e.target.value)}
          placeholder="Enter your vibe-and-intent..."
          rows={3}
          className="w-full p-2 text-sm text-white bg-gray-700 border border-gray-600 rounded-lg"
        />
        <p className="mt-4 text-gray-400">Current Mode: {activeMode}</p>
        <p className="text-gray-500 text-sm mt-2">
          This UI is now structurally ready. You can test directory access now.
        </p>
      </div>
    </div>
  );
};

export default App;
