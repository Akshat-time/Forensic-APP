import requests
import base64
import numpy as np
import soundfile as sf
import io

def generate_sine_wave_base64(duration=2.0, sample_rate=22050, frequency=440.0):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    with io.BytesIO() as wav_io:
        sf.write(wav_io, wave, sample_rate, format='WAV')
        wav_bytes = wav_io.getvalue()
    
    return base64.b64encode(wav_bytes).decode('utf-8')

dummy_audio = generate_sine_wave_base64()
url = "http://127.0.0.1:8000/api/voice-detection"

def run_test(name, payload, headers, expected_status):
    print(f"\n--- Test: {name} ---")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:", response.json())
        if response.status_code == expected_status:
            print("PASS")
        else:
            print(f"FAIL (Expected {expected_status})")
    except Exception as e:
        print(f"Error: {e}")

# 1. Valid Request
run_test(
    "Valid Request",
    {"language": "Tamil", "audioFormat": "mp3", "audioBase64": dummy_audio},
    {"x-api-key": "sk_test_123456789", "Content-Type": "application/json"},
    200
)

# 2. Invalid API Key
run_test(
    "Invalid API Key",
    {"language": "Tamil", "audioFormat": "mp3", "audioBase64": dummy_audio},
    {"x-api-key": "WRONG_KEY", "Content-Type": "application/json"},
    401
)

# 3. Invalid Language
run_test(
    "Invalid Language",
    {"language": "Alien", "audioFormat": "mp3", "audioBase64": dummy_audio},
    {"x-api-key": "sk_test_123456789", "Content-Type": "application/json"},
    422  # Validation error
)

# 4. Invalid Audio Format
run_test(
    "Invalid Audio Format",
    {"language": "Tamil", "audioFormat": "wav", "audioBase64": dummy_audio},
    {"x-api-key": "sk_test_123456789", "Content-Type": "application/json"},
    422  # Validation error
)
