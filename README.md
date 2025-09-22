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
- Node.js 16+ and npm
- Python 3.8+ and pip
- API keys for AI services (optional for demo)

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (optional for demo)
# The app works with mock data if no API keys are provided

# Start the server
python main.py
```

The backend API will be available at `http://localhost:4321`

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

## 🆘 Support

For questions or issues:
1. Check the sample results for expected output
2. Verify your environment variables
3. Ensure all dependencies are installed
4. Review the console for error messages

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