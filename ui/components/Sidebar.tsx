import React from 'react';
import { View } from '../App';


interface SidebarProps {
    setCurrentView: (view: View) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ setCurrentView }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'assistant', label: 'Assistant' },
    { id: 'guided-assistant', label: 'Guided Assistant' },
    { id: 'pro', label: 'Pro View' },
    { id: 'aistudio', label: 'AI Studio' },
    { id: 'live-analysis', label: 'Live Analysis' },
    { id: 'live-camera', label: 'Live Camera' },
    { id: 'participants', label: 'Participants' },
    { id: 'technical', label: 'Technical' },
    { id: 'philosophy', label: 'Philosophy' },
    { id: 'settings', label: 'Settings' },
  ];
  
  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col">
      <h1 className="text-2xl font-bold mb-8 text-center">Sovereign Assistant</h1>
      <nav className="flex-1">
        <ul>
          {navItems.map(item => (
            <li key={item.id} className="mb-2">
              <button 
                onClick={() => setCurrentView(item.id as View)} 
                className="w-full text-left text-gray-300 hover:text-white hover:bg-gray-700 p-2 rounded"
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
