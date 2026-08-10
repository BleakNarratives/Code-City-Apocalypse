import React, { useRef, useEffect } from 'react';
import { ConversationTurn } from '../types';
import { BotIcon, UserIcon } from './Icons';
import ReactMarkdown from 'react-markdown';

interface ConversationLogProps {
    conversation: ConversationTurn[];
    isLoading: boolean;
}

const ConversationLog: React.FC<ConversationLogProps> = ({ conversation, isLoading }) => {
    const endOfMessagesRef = useRef<null | HTMLDivElement>(null);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [conversation, isLoading]);

    const renderTurn = (turn: ConversationTurn, index: number) => {
        const isUser = turn.role === 'user';
        const isError = turn.role === 'error';

        const containerClasses = `flex items-start gap-4 p-4 ${isUser ? 'justify-end' : ''}`;
        const bubbleClasses = `max-w-2xl p-3 rounded-lg ${isUser ? 'bg-blue-600' : isError ? 'bg-red-800' : 'bg-gray-700'}`;
        const textClasses = "prose prose-invert prose-sm max-w-none";

        return (
            <div key={index} className={containerClasses}>
                {!isUser && (
                    <div className="flex-shrink-0 h-8 w-8 rounded-full bg-gray-600 flex items-center justify-center">
                        <BotIcon />
                    </div>
                )}
                <div className={bubbleClasses}>
                    {turn.imageUrl && <img src={turn.imageUrl} alt="User upload" className="mb-2 rounded-lg max-w-sm"/>}
                    <div className={textClasses}>
                        <ReactMarkdown>{turn.text}</ReactMarkdown>
                    </div>
                </div>
                {isUser && (
                     <div className="flex-shrink-0 h-8 w-8 rounded-full bg-gray-600 flex items-center justify-center">
                        <UserIcon />
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="flex-1 overflow-y-auto p-4">
            {conversation.map(renderTurn)}
            {isLoading && (
                <div className="flex items-start gap-4 p-4">
                     <div className="flex-shrink-0 h-8 w-8 rounded-full bg-gray-600 flex items-center justify-center">
                        <BotIcon />
                    </div>
                    <div className="max-w-xl p-3 rounded-lg bg-gray-700">
                        <div className="flex items-center gap-2">
                           <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                           <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                           <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce"></div>
                        </div>
                    </div>
                </div>
            )}
            <div ref={endOfMessagesRef} />
        </div>
    );
};

export default ConversationLog;
