import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to sys.path to allow running this script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, Header, Security, status
from pydantic import BaseModel, validator
from app.detector import detect_voice
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {
        "message": "Audio Forensics API is running",
        "docs": "/docs",
        "endpoint": "/api/voice-detection"
    }

# Secure API Key
API_KEY = os.getenv("SERVICE_API_KEY", "sk_test_123456789")

SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

class AudioPayload(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

    @validator("language")
    def validate_language(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language must be one of {SUPPORTED_LANGUAGES}")
        return v

    @validator("audioFormat")
    def validate_audio_format(cls, v):
        if v.lower() != "mp3":
            raise ValueError("audioFormat must be 'mp3'")
        return "mp3"

def get_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return x_api_key

@app.post("/api/voice-detection", dependencies=[Security(get_api_key)])
async def detect(payload: AudioPayload):
    try:
        result = detect_voice(payload.dict())
        return result
    except Exception as e:
        # Return error format as specified
        return {
            "status": "error",
            "message": str(e)
        }

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": f"Validation error: {exc}"
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        },
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
