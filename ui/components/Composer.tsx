import React, { useState, useRef, useEffect } from 'react';
import { SendIcon, MicrophoneIcon, CameraIcon } from './Icons';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';

interface ComposerProps {
    onSendMessage: (text: string, imageBase64?: string) => void;
    isLoading: boolean;
}

const Composer: React.FC<ComposerProps> = ({ onSendMessage, isLoading }) => {
    const [text, setText] = useState('');
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [imageBase64, setImageBase64] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const { isListening, startListening, stopListening, text: speechText, hasRecognitionSupport } = useSpeechRecognition();
    
    useEffect(() => {
        if(speechText) {
            setText(speechText);
        }
    }, [speechText]);

    const handleSend = () => {
        if (isLoading || (!text.trim() && !imageBase64)) return;
        onSendMessage(text, imageBase64 ?? undefined);
        setText('');
        setImagePreview(null);
        setImageBase64(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };
    
    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result as string);
                // remove the data URL prefix
                const base64String = (reader.result as string).split(',')[1];
                setImageBase64(base64String);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleMicClick = () => {
        if(isListening) {
            stopListening();
        } else {
            startListening();
        }
    }

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [text]);

    return (
        <div className="p-4 bg-gray-800 border-t border-gray-700">
            {imagePreview && (
                <div className="relative w-32 h-32 mb-2">
                    <img src={imagePreview} alt="Preview" className="w-full h-full object-cover rounded-lg" />
                    <button 
                        onClick={() => {
                            setImagePreview(null); 
                            setImageBase64(null);
                            if (fileInputRef.current) fileInputRef.current.value = "";
                        }} 
                        className="absolute top-1 right-1 bg-red-500 text-white rounded-full h-6 w-6 flex items-center justify-center text-xs"
                    >&times;</button>
                </div>
            )}
            <div className="flex items-start gap-2">
                 <button onClick={() => fileInputRef.current?.click()} className="p-2 rounded-full hover:bg-gray-700 self-end">
                    <CameraIcon />
                </button>
                <input type="file" accept="image/*" ref={fileInputRef} onChange={handleImageChange} className="hidden" />
                {hasRecognitionSupport && (
                    <button onClick={handleMicClick} className={`p-2 rounded-full hover:bg-gray-700 self-end ${isListening ? 'text-red-500 animate-pulse' : ''}`}>
                        <MicrophoneIcon />
                    </button>
                )}
                <textarea
                    ref={textareaRef}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask Sovereign Assistant..."
                    className="flex-1 bg-gray-700 text-white rounded-lg p-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 max-h-40"
                    rows={1}
                    disabled={isLoading}
                />
                <button
                    onClick={handleSend}
                    disabled={isLoading || (!text.trim() && !imageBase64)}
                    className="bg-blue-600 text-white p-2 rounded-full disabled:bg-gray-600 disabled:cursor-not-allowed hover:bg-blue-500 self-end"
                >
                    <SendIcon />
                </button>
            </div>
        </div>
    );
};

export default Composer;
