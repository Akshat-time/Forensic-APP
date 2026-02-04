from app.utils import decode_base64_audio
from app.features import extract_features
from app.gemini_explainer import generate_explanation

def detect_voice(payload):
    audio_io = decode_base64_audio(payload["audioBase64"])

    features = extract_features(audio_io)
    
    # 1. Ask Gemini to classify based on features
    gemini_result = generate_explanation(
        features=features,
        language=payload["language"]
    )
    
    # 2. Use Gemini's result if successful
    if gemini_result["classification"] != "UNKNOWN":
        return {
            "status": "success",
            "language": payload["language"],
            "classification": gemini_result["classification"],
            "confidenceScore": gemini_result["confidenceScore"],
            "explanation": gemini_result["explanation"]
        }
    
    # 3. Fallback Heuristics (only if API fails)
    score = 0
    if features["pause_entropy"] < 1.2: score += 25
    if features["jitter"] < 0.008: score += 25
    if features["shimmer"] < 0.02: score += 20
    if features["noise_variance"] < 1e-6: score += 15
    if features["prosody_drift"] < 0.05: score += 15

    classification = "AI_GENERATED" if score >= 50 else "HUMAN"
    confidence = min(score / 100, 1.0)
    
    return {
        "status": "success",
        "language": payload["language"],
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": "Gemini unavailable. Fallback analysis based on acoustic thresholds."
    }
