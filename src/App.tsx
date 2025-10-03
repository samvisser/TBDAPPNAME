import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import SampleResults from './components/SampleResults';
import TextInput from './components/TextInput';
import Header from './components/Header';
import './App.css';

export interface ProcessingJob {
  job_id: string;
  filename: string;
  status: string;
  progress: number;
  error_message?: string;
}

interface ProcessingResult {
  summary: string;
  insights: string[];
}

function App() {
  const [currentJob, setCurrentJob] = useState<ProcessingJob | null>(null);
  const [showSample, setShowSample] = useState(false);
  const [processingResult, setProcessingResult] = useState<ProcessingResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeTab, setActiveTab] = useState<'upload' | 'text'>('upload');

  const handleUploadSuccess = (job: ProcessingJob) => {
    setCurrentJob(job);
    setShowSample(false);
    setProcessingResult(null);
  };

  const handleReset = () => {
    setCurrentJob(null);
    setShowSample(false);
    setProcessingResult(null);
  };

  const handleShowSample = () => {
    setShowSample(true);
    setCurrentJob(null);
    setProcessingResult(null);
  };

  const handleTextSubmit = async (text: string) => {
    console.log('Starting text submission...');
    setIsProcessing(true);
    try {
      console.log('Sending request to backend...');
      const requestBody = {
        text,
        is_audio_transcript: false,
      };
      console.log('Request body:', requestBody);

      const response = await fetch('http://localhost:8000/api/process-transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`Failed to process transcript: ${response.status} ${errorText}`);
      }

      const result = await response.json();
      console.log('API Response:', result);
      
      // Check if result has the expected structure
      if (!result.summary && !result.insights) {
        console.error('Unexpected API response structure:', result);
        throw new Error('Invalid API response format');
      }
      
      setProcessingResult(result);
    } catch (err: any) {
      const error = err as Error;
      console.error('Error processing transcript:', error);
      console.error('Full error details:', {
        message: error?.message || 'Unknown error',
        stack: error?.stack || '',
        response: (error as any)?.response || null
      });
      setProcessingResult({
        summary: `Error: ${error?.message || 'Failed to process text'}`,
        insights: []
      });
    } finally {
      setIsProcessing(false);
    }
  };


  return (
    <div className="App">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!currentJob && !showSample && !processingResult && (
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16 pt-12">
              <h1 className="text-6xl font-bold hero-text mb-6">
                Learning Centered Meeting Note Taker
              </h1>
              <p className="text-2xl text-slate-300 mb-8 max-w-3xl mx-auto">
                Transform your meetings into actionable insights with AI-powered note-taking and learning analytics
              </p>
              <div className="flex justify-center space-x-6">
                <button
                  onClick={handleShowSample}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-4 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 shadow-lg"
                >
                  View Sample Results
                </button>
                <button
                  onClick={async () => {
                    try {
                      console.log('Testing backend connection...');
                      const response = await fetch('http://localhost:8000/api/test');
                      const data = await response.json();
                      console.log('Backend test response:', data);
                      alert('Backend is connected! Response: ' + JSON.stringify(data));
                    } catch (err) {
                      console.error('Backend test error:', err);
                      alert('Failed to connect to backend. Check console for details.');
                    }
                  }}
                  className="bg-slate-700 hover:bg-slate-600 text-white px-8 py-4 rounded-xl font-medium transition-all duration-300"
                >
                  Test Backend Connection
                </button>
              </div>
            </div>
            
            <div className="grid md:grid-cols-3 gap-8 mb-16">
              <div className="feature-card">
                <div className="bg-blue-900/30 w-16 h-16 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-3xl">🎯</span>
                </div>
                <h3 className="text-xl font-semibold mb-3 text-blue-300">Smart Summarization</h3>
                <p className="text-slate-300">
                  Advanced AI extracts key points and action items from your meetings automatically
                </p>
              </div>
              <div className="feature-card">
                <div className="bg-purple-900/30 w-16 h-16 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-3xl">🧠</span>
                </div>
                <h3 className="text-xl font-semibold mb-3 text-blue-300">Learning Analytics</h3>
                <p className="text-slate-300">
                  Track learning patterns and generate insights from your meeting discussions
                </p>
              </div>
              <div className="feature-card">
                <div className="bg-blue-900/30 w-16 h-16 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-3xl">📊</span>
                </div>
                <h3 className="text-xl font-semibold mb-3 text-blue-300">Smart Organization</h3>
                <p className="text-slate-300">
                  Automatically categorize and tag content for easy reference and knowledge management
                </p>
              </div>
            </div>
            
            <div id="upload-section" className="gradient-border p-8 bg-slate-800/50 backdrop-blur-sm">
              <div className="flex justify-center mb-6">
                <div className="inline-flex rounded-lg border border-slate-700 p-1">
                  <button
                    onClick={() => setActiveTab('upload')}
                    className={`px-4 py-2 rounded-md transition-all ${
                      activeTab === 'upload'
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-300 hover:text-white'
                    }`}
                  >
                    Upload Audio
                  </button>
                  <button
                    onClick={() => setActiveTab('text')}
                    className={`px-4 py-2 rounded-md transition-all ${
                      activeTab === 'text'
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-300 hover:text-white'
                    }`}
                  >
                    Enter Text
                  </button>
                </div>
              </div>
              
              {activeTab === 'upload' ? (
                <FileUpload onUploadSuccess={handleUploadSuccess} />
              ) : (
                <TextInput onSubmit={handleTextSubmit} isProcessing={isProcessing} />
              )}
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

        {processingResult && (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Quick Summary Box */}
            <div className="bg-gradient-to-r from-blue-900/50 to-indigo-900/50 backdrop-blur-sm p-6 rounded-xl border border-blue-500/30">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-blue-300">Quick Summary</h2>
                <button
                  onClick={handleReset}
                  className="text-slate-300 hover:text-white transition-colors"
                >
                  ← Back
                </button>
              </div>
              <div className="prose prose-invert max-w-none">
                <div className="text-xl text-slate-200 leading-relaxed font-medium">
                  {processingResult.summary || 'No summary available'}
                </div>
              </div>
            </div>

            {/* Key Insights Box */}
            <div className="bg-slate-800/50 backdrop-blur-sm p-6 rounded-xl border border-slate-700">
              <h3 className="text-xl font-bold text-blue-300 mb-4">Key Insights</h3>
              <div className="prose prose-invert max-w-none">
                <div className="text-slate-200 leading-relaxed">
                  {processingResult.insights.map((insight: string, index: number) => (
                    <div key={index} className="mb-3 flex items-start">
                      <span className="text-blue-400 mr-3">•</span>
                      <span>{insight}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="bg-slate-800/30 border-t border-slate-700 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-slate-400">
            <p className="text-sm">Learning Centered Meeting Note Taker - Powered by Advanced AI</p>
            <p className="mt-2 text-sm">Built with React, TypeScript, and State-of-the-Art Machine Learning</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 