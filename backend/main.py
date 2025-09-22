from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import asyncio
from pathlib import Path
import shutil
from typing import Optional

from services.audio_processor import AudioProcessor
from services.summary_generator import SummaryGenerator
from services.pdf_generator import PDFGenerator
from models.processing_models import ProcessingStatus, ProcessingResult

app = FastAPI(title="CS300 Lecture Processor", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize services
audio_processor = AudioProcessor()
summary_generator = SummaryGenerator()
pdf_generator = PDFGenerator()

# Store processing status
processing_jobs = {}

@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio file and start processing"""
    
    # Validate file type
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.mp4', '.avi', '.mov')):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Initialize processing status
    processing_jobs[job_id] = ProcessingStatus(
        job_id=job_id,
        filename=file.filename,
        status="uploaded",
        progress=0
    )
    
    # Start background processing
    asyncio.create_task(process_audio_file(job_id, file_path))
    
    return {"job_id": job_id, "message": "File uploaded successfully"}

@app.get("/api/status/{job_id}")
async def get_processing_status(job_id: str):
    """Get processing status for a job"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processing_jobs[job_id]

@app.get("/api/download/{job_id}")
async def download_result(job_id: str):
    """Download the processed PDF result"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    status = processing_jobs[job_id]
    if status.status != "completed":
        raise HTTPException(status_code=400, detail="Processing not completed")
    
    pdf_path = OUTPUT_DIR / f"{job_id}_result.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Result file not found")
    
    return FileResponse(
        path=pdf_path,
        filename=f"lecture_summary_{status.filename}.pdf",
        media_type="application/pdf"
    )

@app.get("/api/sample-result")
async def get_sample_result():
    """Get sample processing result for demo purposes"""
    return {
        "summary": """
        # Lecture Summary: Introduction to Data Structures

        ## Key Topics Covered
        - Arrays and their time complexities
        - Linked Lists implementation
        - Stack and Queue operations
        - Basic sorting algorithms

        ## Main Points
        1. **Arrays**: Fixed size, O(1) access time, but O(n) insertion/deletion
        2. **Linked Lists**: Dynamic size, O(n) access time, but O(1) insertion/deletion at known positions
        3. **Stacks**: LIFO principle, used in function calls and expression evaluation
        4. **Queues**: FIFO principle, used in scheduling and breadth-first search

        ## Important Definitions
        - **Time Complexity**: Measure of algorithm efficiency in terms of time
        - **Space Complexity**: Measure of memory usage by an algorithm
        - **Big O Notation**: Mathematical notation to describe algorithm complexity
        """,
        "insights": [
            "Students showed confusion about pointer arithmetic - recommend additional practice problems",
            "The concept of time complexity was well understood by most students",
            "Queue implementation questions were asked frequently - consider more examples",
            "Memory management concepts need reinforcement in next lecture",
            "Students are ready to move on to more advanced data structures like trees"
        ]
    }

async def process_audio_file(job_id: str, file_path: Path):
    """Background task to process audio file"""
    try:
        # Update status: transcribing
        processing_jobs[job_id].status = "transcribing"
        processing_jobs[job_id].progress = 10
        
        # Transcribe audio
        transcript = await audio_processor.transcribe(file_path)
        processing_jobs[job_id].progress = 40
        
        # Generate summary
        processing_jobs[job_id].status = "summarizing"
        summary = await summary_generator.generate_summary(transcript)
        processing_jobs[job_id].progress = 70
        
        # Extract insights
        insights = await summary_generator.extract_insights(transcript)
        processing_jobs[job_id].progress = 85
        
        # Generate PDF
        processing_jobs[job_id].status = "generating_pdf"
        pdf_path = OUTPUT_DIR / f"{job_id}_result.pdf"
        await pdf_generator.create_pdf(summary, insights, pdf_path)
        
        # Update status: completed
        processing_jobs[job_id].status = "completed"
        processing_jobs[job_id].progress = 100
        processing_jobs[job_id].result = ProcessingResult(
            summary=summary,
            insights=insights,
            pdf_path=str(pdf_path)
        )
        
    except Exception as e:
        processing_jobs[job_id].status = "error"
        processing_jobs[job_id].error_message = str(e)
    
    finally:
        # Clean up uploaded file
        if file_path.exists():
            file_path.unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 