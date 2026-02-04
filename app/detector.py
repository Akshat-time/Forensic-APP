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
    ai_signals = []

    if features["pause_entropy"] < 0.7:
        ai_signals.append("pause_entropy")

    if features["jitter"] < 0.004:
        ai_signals.append("jitter")

    if features["shimmer"] < 0.015:
        ai_signals.append("shimmer")

    if features["noise_variance"] < 3e-7:
        ai_signals.append("noise_variance")

    if features["prosody_drift"] < 0.03:
        ai_signals.append("prosody_drift")

    # Strong AI signal: Flat amplitude
    if features.get("amplitude_variance", 1.0) < 1e-5:
        ai_signals.append("amplitude_variance")

    # FINAL DECISION
    if len(ai_signals) >= 3:
        classification = "AI_GENERATED"
    else:
        classification = "HUMAN"

    confidence = round(len(ai_signals) / 5, 2)
    
    # Cap confidence to avoid overconfidence
    confidence = min(confidence, 0.85)

    if classification == "HUMAN":
        explanation = "Natural speech variations detected with minor acoustic regularities."
    else:
        explanation = "Multiple synthetic speech artifacts detected including pitch stability and uniform pauses."

    return {
        "status": "success",
        "language": payload["language"],
        "classification": classification,
        "confidenceScore": confidence,
        "explanation": explanation
    }
