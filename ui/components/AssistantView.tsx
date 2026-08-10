import React, { useState } from 'react';
import { ConversationTurn } from '../types';
import { INITIAL_MESSAGES } from '../data/context';
import ConversationLog from './ConversationLog';
import Composer from './Composer';
import { callGeminiApi } from '../services/api';

const AssistantView = () => {
    const [conversation, setConversation] = useState<ConversationTurn[]>(INITIAL_MESSAGES);
    const [isLoading, setIsLoading] = useState(false);

    const handleSendMessage = async (text: string, imageBase64?: string) => {
        if (!text.trim() && !imageBase64) return;

        const userTurn: ConversationTurn = { role: 'user', text, imageUrl: imageBase64 ? `data:image/jpeg;base64,${imageBase64}` : undefined };
        const newConversation = [...conversation, userTurn];
        setConversation(newConversation);
        setIsLoading(true);

        try {
            const responseText = await callGeminiApi(conversation, text, imageBase64);
            setConversation(prev => [...prev, { role: 'assistant', text: responseText }]);
        } catch (error) {
            console.error(error);
            const message = error instanceof Error ? error.message : "An unknown error occurred.";
            setConversation(prev => [...prev, { role: 'error', text: `Error: ${message}` }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-gray-900">
            <ConversationLog conversation={conversation} isLoading={isLoading} />
            <Composer onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
    );
};

export default AssistantView;
