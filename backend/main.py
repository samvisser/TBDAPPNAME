from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import logging

from config import API_HOST, API_PORT, API_RELOAD
from services.gemini_service import GeminiService

# Configure logging
class InfoFilter(logging.Filter):
    def filter(self, record):
        # Filter out AFC and other initialization messages
        return not record.getMessage().startswith('AFC')

# Create logger
logger = logging.getLogger('gemini_api')
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler('gemini_api.log')
console_handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add filter to both handlers
info_filter = InfoFilter()
file_handler.addFilter(info_filter)
console_handler.addFilter(info_filter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Initialize Gemini service
gemini_service = GeminiService()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptInput(BaseModel):
    text: str
    is_audio_transcript: bool = False

class SimpleQuestion(BaseModel):
    question: str

# Quick test endpoint for Gemini
@app.post("/api/quick-test")
async def quick_test(data: SimpleQuestion):
    try:
        # Simple test using the gemini service
        result = await gemini_service.process_text(data.question)
        return {"result": result["summary"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_with_gemini(text: str) -> dict:
    """
    Process text using the Gemini service.
    
    Args:
        text: The text to process
        
    Returns:
        Dict containing 'summary' and 'insights' keys
    """
    try:
        logger.info("Starting text processing with Gemini service")
        result = await gemini_service.process_text(text)
        logger.info(f"Processing completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in process_with_gemini: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

# Simple test endpoint
@app.get("/api/test")
async def test_endpoint():
    return {"message": "Backend is working!", "status": "success"}

# Test endpoint that accepts POST data
@app.post("/api/test-post")
async def test_post(data: dict):
    return {
        "message": "Received your data!",
        "received_data": data,
        "status": "success"
    }

@app.post("/api/process-transcript")
async def process_transcript(input_data: TranscriptInput):
    try:
        result = await process_with_gemini(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=API_RELOAD) 