import React from 'react';

const ApiKeyManager = () => {
    const isApiKeySet = !!process.env.API_KEY;

    return (
        <div className="p-4 bg-gray-800 rounded-lg">
            <h3 className="font-bold">API Key Status</h3>
            <p className={isApiKeySet ? 'text-green-400' : 'text-red-400'}>
                {isApiKeySet 
                    ? "API Key is configured via environment variable." 
                    : "API Key is not configured. The application will not function."
                }
            </p>
        </div>
    );
};

export default ApiKeyManager;
