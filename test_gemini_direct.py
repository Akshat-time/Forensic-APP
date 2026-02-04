import os
from dotenv import load_dotenv
load_dotenv()

from app.gemini_explainer import generate_explanation

print(f"API KEY: {os.getenv('GEMINI_API_KEY')}")

features = {
    "pause_entropy": 0.5,
    "jitter": 0.001,
    "shimmer": 0.01,
    "noise_variance": 0.0,
    "prosody_drift": 0.0
}

result = generate_explanation(features, "AI_GENERATED", "Tamil")
print("\n--- Result ---")
print(result)
