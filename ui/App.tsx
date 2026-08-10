import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import AssistantView from './components/AssistantView';
import DashboardView from './components/DashboardView';
import ParticipantsView from './components/ParticipantsView';
import TechnicalView from './components/TechnicalView';
import PhilosophyView from './components/PhilosophyView';
import LiveAnalysisView from './components/LiveAnalysisView';
import AIStudioView from './components/AIStudioView';
import ProView from './components/ProView';
import GuidedAssistantView from './components/GuidedAssistantView';
import SettingsView from './components/SettingsView';
import LiveCameraView from './components/LiveCameraView';

export type View = 'assistant' | 'dashboard' | 'pro' | 'aistudio' | 'settings' | 'participants' | 'technical' | 'philosophy' | 'live-analysis' | 'live-camera' | 'guided-assistant';

const App = () => {
  const [currentView, setCurrentView] = useState<View>('assistant');

  const renderView = () => {
    switch (currentView) {
      case 'assistant': return <AssistantView />;
      case 'dashboard': return <DashboardView />;
      case 'participants': return <ParticipantsView />;
      case 'technical': return <TechnicalView />;
      case 'philosophy': return <PhilosophyView />;
      case 'live-analysis': return <LiveAnalysisView />;
      case 'aistudio': return <AIStudioView />;
      case 'pro': return <ProView />;
      case 'guided-assistant': return <GuidedAssistantView />;
      case 'settings': return <SettingsView />;
      case 'live-camera': return <LiveCameraView />;
      default: return <AssistantView />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans">
      <Sidebar setCurrentView={setCurrentView} />
      <main className="flex-1 flex flex-col">
        {renderView()}
      </main>
    </div>
  );
};

export default App;
