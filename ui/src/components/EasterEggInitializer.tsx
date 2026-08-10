import React, { useEffect, useState } from 'react';
import { fetchSystemStatus } from '../services/apiService';

const EasterEggInitializer = () => {
  const [isEasterEggActive, setIsEasterEggActive] = useState(false);
  const [systemStatus, setSystemStatus] = useState<any>(null);

  useEffect(() => {
    const initSystem = async () => {
        const status = await fetchSystemStatus();
        setSystemStatus(status);
    };
    initSystem();

    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === 'q' && e.ctrlKey) {
        setIsEasterEggActive(true);
        console.log("Initializing Whorl Core: Deep Resonance Sequence...");
      }
    };
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    <div className="system-status">
      {isEasterEggActive ? (
        <div className="glitch-overlay">
          <h2>SYSTEM CORE AWAKENED</h2>
          <p>The Swarm is listening...</p>
          <pre>{JSON.stringify(systemStatus, null, 2)}</pre>
        </div>
      ) : (
        <p>System Initialized - Ready for connection</p>
      )}
    </div>
  );
};

export default EasterEggInitializer;
