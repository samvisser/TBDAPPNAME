import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import SampleResults from './components/SampleResults';
import Header from './components/Header';
import './App.css';

export interface ProcessingJob {
  job_id: string;
  filename: string;
  status: string;
  progress: number;
  error_message?: string;
}

function App() {
  const [currentJob, setCurrentJob] = useState<ProcessingJob | null>(null);
  const [showSample, setShowSample] = useState(false);

  const handleUploadSuccess = (job: ProcessingJob) => {
    setCurrentJob(job);
    setShowSample(false);
  };

  const handleReset = () => {
    setCurrentJob(null);
    setShowSample(false);
  };

  const handleShowSample = () => {
    setShowSample(true);
    setCurrentJob(null);
  };

  return (
    <div className="App">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!currentJob && !showSample && (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                CS300 Lecture Processor
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Transform your lecture recordings into comprehensive summaries and actionable insights
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleShowSample}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  View Sample Results
                </button>
              </div>
            </div>
            
            <FileUpload onUploadSuccess={handleUploadSuccess} />
            
            <div className="mt-12">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                How It Works
              </h2>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🎤</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">1. Upload Audio</h3>
                  <p className="text-gray-600">
                    Drop your lecture recording (MP3, WAV, M4A, MP4) into our secure dropbox
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">🤖</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">2. AI Processing</h3>
                  <p className="text-gray-600">
                    Our AI transcribes, summarizes, and extracts educational insights automatically
                  </p>
                </div>
                <div className="text-center">
                  <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl">📄</span>
                  </div>
                  <h3 className="text-lg font-semibold mb-2">3. Get Results</h3>
                  <p className="text-gray-600">
                    Download a professional PDF with summary and actionable teaching insights
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {currentJob && (
          <ProcessingStatus 
            job={currentJob} 
            onReset={handleReset}
            onJobUpdate={setCurrentJob}
          />
        )}

        {showSample && (
          <SampleResults onBack={handleReset} />
        )}
      </main>

      <footer className="bg-gray-50 border-t mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p>CS300 Lecture Processor - Automated Educational Analysis Tool</p>
            <p className="mt-2">Built with React, TypeScript, Python, and AI</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 