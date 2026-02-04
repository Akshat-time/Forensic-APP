import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    with open("models_list.txt", "w", encoding="utf-8") as f:
        f.write("Listing models:\n")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(m.name + "\n")
    print("Models written to models_list.txt")
except Exception as e:
    print(f"Error listing models: {e}")
