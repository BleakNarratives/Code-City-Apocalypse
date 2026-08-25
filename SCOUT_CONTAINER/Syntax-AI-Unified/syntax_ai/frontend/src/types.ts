// FILENAME: types.ts

// Defines the structure of the Blueprint returned by the Blueprint Engine
export interface SyntaxBlueprint {
  id: string;
  sourceVibe: string;
  kernelModule: { language: string; description: string; };
  networkModule: { protocol: string; endpoints: string[]; };
  uiModule: { framework: string; components: string[]; };
  persona: { tone: string; style: string; };
  confidenceScore: number;
}

// Defines the API response structure
export interface BlueprintResponse {
  success: boolean;
  blueprint?: SyntaxBlueprint;
  error?: string;
}
