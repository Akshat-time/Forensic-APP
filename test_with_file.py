import sys
import os
import base64
import requests
import json

def test_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f"Reading file: {file_path}...")
    with open(file_path, "rb") as f:
        audio_content = f.read()
        audio_b64 = base64.b64encode(audio_content).decode("utf-8")

    language = "English"
    if len(sys.argv) > 2:
        language = sys.argv[2]

    url = "http://127.0.0.1:8000/api/voice-detection"
    headers = {
        "x-api-key": "sk_test_123456789",
        "Content-Type": "application/json"
    }
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_b64
    }

    print(f"Sending request (Language: {language})...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n--- Analysis Result ---")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_with_file.py <path_to_audio_file> [Language]")
        print("Example: python test_with_file.py sample.mp3 Hindi")
    else:
        test_file(sys.argv[1])
