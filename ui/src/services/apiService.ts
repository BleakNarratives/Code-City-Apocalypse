// API Service for UnifiedCodeCity using real Gemini API
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

export const fetchSystemStatus = async () => {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent("Return a short JSON object representing system status with fields: status (online), swarm_active (true), node_count (42), and active_processes (array of 3 items).");
    const response = await result.response;
    const text = response.text();
    // Assuming the response is clean JSON
    return JSON.parse(text);
  } catch (error) {
    console.error("Failed to fetch system status from Gemini:", error);
    return { status: 'offline', error: 'API connection failed' };
  }
};
