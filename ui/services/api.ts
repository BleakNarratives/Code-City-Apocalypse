import { GoogleGenAI } from "@google/genai";
import { ConversationTurn } from "../types";
import { SYSTEM_PROMPT } from "../data/context";

// This is a simplified, stateless function.
// A stateful chat service could be built on top of this.
export const callGeminiApi = async (
    history: ConversationTurn[],
    prompt: string,
    imageBase64?: string
): Promise<string> => {
    
    if (!process.env.API_KEY) {
        throw new Error("API_KEY is not configured. Please ensure it is set in your environment variables.");
    }
    // FIX: Initialize GoogleGenAI with named apiKey parameter
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

    // FIX: Use recommended model name
    const modelName = imageBase64 ? 'gemini-2.5-flash' : 'gemini-2.5-pro';

    // Map conversation history to Gemini's format
    const contents = history
        .filter(turn => turn.role === 'user' || turn.role === 'assistant')
        .map(turn => ({
            role: turn.role === 'assistant' ? 'model' : 'user',
            parts: [{ text: turn.text }], // This simplifies history, assuming no images in history for now
        }));

    // Add current user turn
    const userParts: any[] = [{ text: prompt }];
    if (imageBase64) {
        // A simple way to infer mimeType from base64 string
        const mimeType = imageBase64.charAt(0) === '/' ? 'image/jpeg' : 'image/png';
        userParts.unshift({ // Add image before text
            inlineData: {
                mimeType: mimeType,
                data: imageBase64,
            },
        });
    }
    contents.push({ role: 'user', parts: userParts });

    try {
        const response = await ai.models.generateContent({
            model: modelName,
            contents: contents,
            config: {
              systemInstruction: SYSTEM_PROMPT,
            }
        });
        
        // FIX: Extract text directly from response.text
        return response.text;
    } catch (error) {
        console.error("Error calling Gemini API:", error);
        if (error instanceof Error) {
            throw new Error(`API Error: ${error.message}`);
        }
        throw new Error("An unknown error occurred while contacting the API.");
    }
};
