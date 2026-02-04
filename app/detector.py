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
            "explanation": gemini_result["explanation"],
            "debug_features": features, # Exposed for tuning
        }
    
    # 3. Fallback Heuristics (only if API fails)
    ai_signals = 0

    if features["pause_entropy"] < 0.8:
        ai_signals += 1

    if features["jitter"] < 0.004:
        ai_signals += 1

    if features["shimmer"] < 0.015:
        ai_signals += 1

    if features["noise_variance"] < 5e-7:
        ai_signals += 1

    if features["prosody_drift"] < 0.03:
        ai_signals += 1

    # FINAL DECISION
    if ai_signals >= 3:
        classification = "AI_GENERATED"
    else:
        classification = "HUMAN"

    confidence = ai_signals / 5
    
    return {
        "status": "success",
        "language": payload["language"],
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": "Gemini unavailable. Fallback analysis based on acoustic thresholds."
    }
