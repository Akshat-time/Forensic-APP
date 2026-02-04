import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_explanation(features: dict, language: str):
    prompt_text = f"""
You are an audio forensics expert AI.
Your task is to analyze acoustic features to DETECT if an audio clip is likely AI-Generated or Human.

CRITICAL INSTRUCTION: BIAS TOWARDS "HUMAN".
Real human voices are diverse. AI voices are "mathematically perfect".
Unless the audio is **unambiguously** artificial across ALL metrics, classify as **HUMAN**.

Analysis Logic:
1. **The "Human" Signal**:
   - If Jitter > 0.005 OR Shimmer > 0.015, it is almost certainly **HUMAN**, even if other metrics are low.
   - Natural pitch fluctuation (Jitter) is the strongest indicator of a human vocal fold.

2. **Common False Positives (Do NOT classify as AI for these)**:
   - **Low Noise**: Studio recordings have 0 noise. This is NOT a sign of AI on its own.
   - **Low Pause Entropy**: Humans reading a script pause regularly. This is NOT a sign of AI on its own.

3. **The "AI" Signal (Deepfake)**:
   - Classify as AI **ONLY IF**: 
     - Jitter is Extremely Low (< 0.003) AND 
     - Shimmer is Low (< 0.01) AND 
     - Prosody/Pauses are machine-perfect.

Return your analysis in JSON format ONLY:
{{
    "classification": "AI_GENERATED" or "HUMAN",
    "confidenceScore": float (0.0 to 1.0),
    "explanation": "string (max 20 words)"
}}

Analyze this audio sample:
Language: {language}

Extracted Acoustic Features:
- Pause Entropy: {features['pause_entropy']:.4f}
- Pitch Jitter: {features['jitter']:.4f}
- Amplitude Shimmer: {features['shimmer']:.4f}
- Silence Noise Variance: {features['noise_variance']:.9f}
- Prosody Drift: {features['prosody_drift']:.4f}
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }

    import time
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(URL, headers=headers, json=payload)
            
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)
                    print(f"Gemini 429 (Rate Limit). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    # Log final failure to console
                    print(f"GEMINI ERROR BODY (Final): {response.text}")
                    raise Exception(f"API returned status {response.status_code} after retries")

            if response.status_code != 200:
                print(f"GEMINI ERROR BODY: {response.text}")
                raise Exception(f"API returned status {response.status_code}")

            response_data = response.json()
            
            # Check if candidate exists
            if not response_data.get('candidates'):
                # Safety check for empty candidates
                if response_data.get('promptFeedback'):
                    print(f"GEMINI BLOCKED: {response_data['promptFeedback']}")
                raise Exception("No candidates returned")

            # Extract text content
            text_content = response_data['candidates'][0]['content']['parts'][0]['text']
            
            if text_content.startswith("```"):
                text_content = text_content.replace("```json", "").replace("```", "").strip()
                
            return json.loads(text_content)

        except Exception as e:
            print(f"GEMINI EXCEPTION (Attempt {attempt+1}): {e}")
            if attempt == max_retries - 1:
                return {
                    "classification": "UNKNOWN",
                    "confidenceScore": 0.0,
                    "explanation": "Gemini API unavailable."
                }
