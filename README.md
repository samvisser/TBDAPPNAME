# CS300 Lecture Processor

An automated educational analysis tool that transforms lecture recordings into comprehensive summaries and actionable insights using AI.

## 🎯 Features

- **Audio Upload**: Drag-and-drop interface for lecture recordings (MP3, WAV, M4A, MP4, AVI, MOV)
- **AI Transcription**: Multiple options - OpenAI Whisper, AssemblyAI, AWS Transcribe
- **Smart Summarization**: GPT and Hugging Face models for content analysis
- **Educational Insights**: AI-powered recommendations for teaching improvement
- **PDF Generation**: Professional reports with summaries and insights
- **Real-time Processing**: Live status updates and progress tracking

## 🛠 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Dropzone** for file uploads
- **Lucide React** for icons
- **Axios** for API communication

### Backend
- **FastAPI** (Python) for REST API
- **OpenAI Whisper** for transcription
- **AssemblyAI** for alternative transcription
- **AWS Transcribe** for cloud transcription
- **GPT-3.5** for summarization and insights
- **Hugging Face Transformers** for local AI models
- **ReportLab** for PDF generation

## 🚀 Quick Start

### Prerequisites
- **Node.js 16+** and npm (for frontend)
- **Python 3.8+** and pip (for backend)
- **Google API Key** (for Gemini AI processing)

### 📦 Complete Setup Process

#### Step 1: Clone and Navigate
```bash
git clone <your-repo-url>
cd TBDAPPNAME
```

#### Step 2: Frontend Setup
```bash
# Install frontend dependencies
npm install

# Start frontend development server
npm start
```
The frontend will be available at `http://localhost:3000`

#### Step 3: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Run automated setup script
python setup.py
```

The setup script will:
- ✅ Create Python virtual environment (`venv/`)
- ✅ Install all required dependencies
- ✅ Create `.env` file template
- ✅ Set up proper project structure

#### Step 4: Configure API Key
```bash
# Edit the .env file and add your Google API key
nano .env  # or use your preferred editor
```

Add your Google API key:
```
GOOGLE_API_KEY=your_actual_google_api_key_here
```

#### Step 5: Start Backend Server
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the backend server
python main.py
```

The backend API will be available at `http://localhost:8000`

### 🎯 Ready to Use!
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (FastAPI auto-generated docs)

### 🔧 Manual Setup (Alternative)
If you prefer manual setup instead of using the setup script:

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Start server
python main.py
```

### ⚠️ Important Notes
- **Virtual environment is excluded** from version control (`.gitignore`)
- **Each developer** must run `python setup.py` to create their own environment
- **API key is required** for text processing functionality
- **Both servers** (frontend and backend) must be running for full functionality

## 🔧 Configuration

### Environment Variables (.env)

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AssemblyAI Configuration  
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
AWS_S3_BUCKET=your_s3_bucket_name

# Processing Configuration
TRANSCRIPTION_METHOD=openai  # Options: openai, assemblyai, aws, mock
SUMMARY_METHOD=openai        # Options: openai, huggingface, mock
```

### API Service Options

1. **OpenAI Whisper** (Recommended)
   - Most accurate transcription
   - Requires OpenAI API key
   - Supports multiple languages

2. **AssemblyAI**
   - Fast and accurate
   - Requires AssemblyAI API key
   - Good for long recordings

3. **AWS Transcribe**
   - Enterprise-grade
   - Requires AWS credentials and S3 bucket
   - Scalable for large volumes

4. **Mock Mode** (Default)
   - No API keys required
   - Uses sample data for demo
   - Perfect for testing

## 📁 Project Structure

```
TBDAPPNAME/
├── src/                    # React frontend
│   ├── components/         # React components
│   │   ├── FileUpload.tsx     # Drag-and-drop upload
│   │   ├── ProcessingStatus.tsx # Real-time status
│   │   ├── SampleResults.tsx   # Demo preview
│   │   └── Header.tsx         # App header
│   ├── App.tsx            # Main app component
│   └── index.tsx          # App entry point
├── backend/               # Python backend
│   ├── services/          # Core services
│   │   ├── audio_processor.py  # Transcription
│   │   ├── summary_generator.py # AI summarization
│   │   └── pdf_generator.py    # PDF creation
│   ├── models/            # Data models
│   │   └── processing_models.py
│   └── main.py           # FastAPI server
├── public/               # Static assets
└── package.json          # Frontend dependencies
```

## 🎮 Usage

### 1. Upload Audio File
- Drag and drop your lecture recording
- Supported formats: MP3, WAV, M4A, MP4, AVI, MOV
- Maximum file size: 500MB

### 2. Monitor Processing
- Real-time progress updates
- Step-by-step status tracking
- Estimated completion time

### 3. Download Results
- Professional PDF report
- Comprehensive lecture summary
- Actionable teaching insights

### 4. Sample Results
- Click "View Sample Results" to see demo output
- Preview without uploading files
- Understand the analysis format

## 🔄 Processing Pipeline

1. **Upload**: Secure file upload and validation
2. **Transcription**: Convert audio to text using AI
3. **Analysis**: Generate summary and extract insights
4. **PDF Creation**: Format results into professional document
5. **Download**: Provide downloadable PDF report

## 📊 Sample Output

The generated PDF includes:

### Lecture Summary
- Key topics covered
- Main concepts and definitions
- Important examples
- Structured markdown format

### Educational Insights
- Student comprehension analysis
- Areas of confusion
- Engagement patterns
- Improvement recommendations
- Next steps suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support & Troubleshooting

### Common Setup Issues

#### ❌ "python: command not found"
```bash
# Try using python3 instead
python3 setup.py
python3 main.py
```

#### ❌ "No module named uvicorn"
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### ❌ "GOOGLE_API_KEY not found"
```bash
# Make sure .env file exists in backend directory
cd backend
ls -la .env  # Should show the file
# Edit .env and add your API key
```

#### ❌ "Failed to fetch" in frontend
```bash
# Make sure backend is running
cd backend
source venv/bin/activate
python main.py
# Should show "Uvicorn running on http://0.0.0.0:8000"
```

#### ❌ "Permission denied" on setup.py
```bash
# Make the script executable
chmod +x setup.py
python setup.py
```

### Getting Help

1. **Check logs**: Look at console output for error messages
2. **Verify setup**: Ensure both frontend (port 3000) and backend (port 8000) are running
3. **Test API**: Visit `http://localhost:8000/docs` to see API documentation
4. **Check environment**: Make sure you're in the virtual environment when running backend

### Debug Steps
1. Run `python setup.py` and check for any errors
2. Verify `.env` file exists and has your API key
3. Test backend with: `curl http://localhost:8000/api/test`
4. Check browser console for frontend errors
5. Review backend logs in terminal

## 🚀 Deployment

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy the build/ directory
```

### Backend (Heroku/Railway/DigitalOcean)
```bash
# Add your API keys as environment variables
# Deploy the backend/ directory
```

---

Built with ❤️ for CS300 students and educators