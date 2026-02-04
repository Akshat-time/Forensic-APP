import requests
import base64
import numpy as np
import soundfile as sf
import io

# 1. Generate synthetic audio (Pure Sine Wave -> High AI Score)
def generate_sine_wave():
    sample_rate = 22050
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = 0.5 * np.sin(2 * np.pi * 440.0 * t) # Pure 440Hz A4
    
    with io.BytesIO() as wav_io:
        sf.write(wav_io, wave, sample_rate, format='WAV')
        return base64.b64encode(wav_io.getvalue()).decode('utf-8')

audio_b64 = generate_sine_wave()

# 2. Define Request
url = "http://127.0.0.1:8000/api/voice-detection"
headers = {
    "x-api-key": "sk_test_123456789",
    "Content-Type": "application/json"
}
payload = {
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": audio_b64
}

# 3. Send Request
print("Sending request to Gemini-backed API...")
try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n--- Response Body ---")
        print(data)
        
        explanation = data.get("explanation", "")
        fallback_msg = "Detected unnaturally stable pitch and uniform pauses inconsistent with human speech."
        
        print("\n--- Verification ---")
        if explanation == fallback_msg:
            print("WARNING: API is using FALLBACK explanation (Gemini Key might be invalid or quota exceeded).")
        else:
            print("SUCCESS: Received a dynamic explanation from Gemini!")
            print(f"Explanation: '{explanation}'")
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Connection Failed: {e}")
