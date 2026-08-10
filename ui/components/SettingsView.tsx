import React from 'react';
import ApiKeyManager from './ApiKeyManager';

const SettingsView = () => {
    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Settings</h2>
            <div className="space-y-4">
                <ApiKeyManager />
                {/* Other settings would go here */}
            </div>
        </div>
    );
};

export default SettingsView;
