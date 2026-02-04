# Audio Forensics Explanation Assistant

A specialized tool that combines **Signal Processing** (mathematics) with **Generative AI** (Google Gemini) to detect Deepfake Audio.

## 🚀 Deployment Status
*   **Live Endpoint:** `https://forensic-app-1jc0.onrender.com/api/voice-detection`
*   **Documentation:** `https://forensic-app-1jc0.onrender.com/docs`
*   **Platform:** Render (Cloud Docker Hosting)

## 🔑 Credentials
*   **Header Name:** `x-api-key`
*   **API Key:** `sk_test_123456789`
*   **Method:** `POST`

## 🛠️ Technology Stack
*   **Core Backend:** Python 3.11, FastAPI
*   **Audio Analysis:** Librosa, NumPy, SciPy (Extracts Jitter, Shimmer, Pause Entropy)
*   **Artificial Intelligence:** Google Gemini 2.0 Flash (Analyzes features for forensic verdict)
*   **Frontend:** React, TypeScript, Vite, Tailwind CSS (Interactive Dashboard)
*   **Containerization:** Docker

## 📂 Project Structure
*   `app/` - Core Python backend logic.
    *   `main.py` - API Server entry point.
    *   `detector.py` - Orchestrates logic between Math & AI.
    *   `features.py` - Raw mathematical audio feature extraction.
    *   `gemini_explainer.py` - Interface with Google Gemini AI.
*   `services/` & `components/` - key frontend UI logic.
*   `Dockerfile` - Production build instructions.

## 🔄 How It Works
1.  **Input:** User uploads audio (MP3).
2.  **Math:** System calculates Jitter, Shimmer, Pause Entropy, and Noise Variance.
3.  **Analysis:**
    *   If features are "too perfect" (Low Jitter/Entropy), it suspects AI.
    *   **Strict Bias:** Defaults to "HUMAN" unless metrics are unambiguously artificial.
    *   AI Prompt understands Studio Recording vs. Deepfake.
4.  **Output:** Returns Classification (AI/HUMAN), Confidence Score, and a Technical Explanation.
