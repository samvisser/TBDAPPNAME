# CS300 Lecture Processor - Backend

FastAPI backend service for processing lecture recordings into summaries and insights.

## 🚀 Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run server
python main.py
```

## 📡 API Endpoints

### POST `/api/upload-audio`
Upload audio file for processing
- **Body**: Multipart form data with `file` field
- **Returns**: `{job_id: string, message: string}`

### GET `/api/status/{job_id}`
Get processing status
- **Returns**: Processing status object with progress

### GET `/api/download/{job_id}`
Download processed PDF
- **Returns**: PDF file download

### GET `/api/sample-result`
Get sample processing result
- **Returns**: Sample summary and insights

## 🔧 Services

### AudioProcessor (`services/audio_processor.py`)
- Handles multiple transcription services
- Supports OpenAI Whisper, AssemblyAI, AWS Transcribe
- Fallback to mock data for demo

### SummaryGenerator (`services/summary_generator.py`)
- GPT-based summarization
- Hugging Face model support
- Educational insight extraction

### PDFGenerator (`services/pdf_generator.py`)
- Professional PDF creation
- Structured layout with ReportLab
- Custom styling and formatting

## 🏗 Architecture

```
Backend/
├── main.py              # FastAPI app
├── models/              # Pydantic models
├── services/            # Core business logic
├── uploads/             # Temporary file storage
└── outputs/             # Generated PDFs
```

## 🔐 Environment Variables

```bash
# Required for production
OPENAI_API_KEY=sk-...
ASSEMBLYAI_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Optional configuration
TRANSCRIPTION_METHOD=openai
SUMMARY_METHOD=openai
```

## 🛠 Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Test endpoints
curl -X POST "http://localhost:8000/api/upload-audio" \
     -F "file=@test.mp3"
``` 