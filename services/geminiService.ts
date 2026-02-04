
import { GoogleGenAI } from "@google/genai";
import { AudioFeatures, Classification } from "../types";

export const generateForensicJustification = async (
  features: AudioFeatures,
  classification: Classification
): Promise<string> => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  
  const prompt = `
    You are an audio forensics explanation assistant.
    Your role is strictly limited to converting numerical audio feature values into short, factual explanations.
    
    Audio analysis summary:
    Language: ${features.language}
    
    Extracted features:
    - Pause entropy: ${features.pauseEntropy.toFixed(3)}
    - Pitch jitter: ${features.pitchJitter.toFixed(3)}%
    - Amplitude shimmer: ${features.shimmer.toFixed(3)}%
    - Silence noise variance: ${features.silenceNoiseVariance.toFixed(4)}
    - Prosody drift score: ${features.prosodyDrift.toFixed(2)}
    
    Final classification: ${classification}
    
    RULES:
    - You do NOT analyze audio.
    - You do NOT decide classifications.
    - You do NOT invent features.
    - You do NOT speculate.
    - Generate a concise explanation (max 20 words) justifying the given classification using ONLY the provided features.
    - Use neutral, technical language.
    - Avoid mentioning AI models, neural networks, or proprietary systems.
  `;

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: prompt,
      config: {
        temperature: 0.1,
        topK: 1,
      },
    });

    return response.text?.trim() || "Unable to generate justification.";
  } catch (error) {
    console.error("Gemini Error:", error);
    throw new Error("Failed to communicate with the forensics engine.");
  }
};
