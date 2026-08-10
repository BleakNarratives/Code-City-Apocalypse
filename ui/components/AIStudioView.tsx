import React, { useState } from 'react';
import ChatView from './studio/ChatView';
import ImageView from './studio/ImageView';
import VideoView from './studio/VideoView';
import TtsView from './studio/TtsView';

type StudioTab = 'chat' | 'image' | 'video' | 'tts';

const AIStudioView = () => {
    const [activeTab, setActiveTab] = useState<StudioTab>('chat');
    
    const renderTabContent = () => {
        switch (activeTab) {
            case 'chat': return <ChatView />;
            case 'image': return <ImageView />;
            case 'video': return <VideoView />;
            case 'tts': return <TtsView />;
            default: return <ChatView />;
        }
    };

    const tabs: {id: StudioTab, label: string}[] = [
        { id: 'chat', label: 'Chat' },
        { id: 'image', label: 'Image Generation' },
        { id: 'video', label: 'Video Generation' },
        { id: 'tts', label: 'Text-to-Speech' },
    ];

    return (
        <div className="p-4 h-full flex flex-col">
            <h2 className="text-2xl font-bold mb-4">AI Studio</h2>
            <div className="flex border-b border-gray-700 mb-4">
                {tabs.map(tab => (
                     <button 
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`py-2 px-4 ${activeTab === tab.id ? 'border-b-2 border-blue-500 text-white' : 'text-gray-400'}`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className="flex-1">
                {renderTabContent()}
            </div>
        </div>
    );
};

export default AIStudioView;
