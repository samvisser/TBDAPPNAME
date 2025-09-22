import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertCircle, Download, RotateCcw, Clock } from 'lucide-react';
import axios from 'axios';
import { ProcessingJob } from '../App';

interface ProcessingStatusProps {
  job: ProcessingJob;
  onReset: () => void;
  onJobUpdate: (job: ProcessingJob) => void;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ 
  job, 
  onReset, 
  onJobUpdate 
}) => {
  const [currentJob, setCurrentJob] = useState(job);

  useEffect(() => {
    if (currentJob.status === 'completed' || currentJob.status === 'error') {
      return;
    }

    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`/api/status/${currentJob.job_id}`);
        const updatedJob = response.data;
        setCurrentJob(updatedJob);
        onJobUpdate(updatedJob);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [currentJob.job_id, currentJob.status, onJobUpdate]);

  const handleDownload = async () => {
    try {
      const response = await axios.get(`/api/download/${currentJob.job_id}`, {
        responseType: 'blob',
      });
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `lecture_summary_${currentJob.filename}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const getStatusIcon = () => {
    switch (currentJob.status) {
      case 'completed':
        return <CheckCircle className="w-8 h-8 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-8 h-8 text-red-500" />;
      default:
        return <Clock className="w-8 h-8 text-blue-500" />;
    }
  };

  const getStatusText = () => {
    switch (currentJob.status) {
      case 'uploaded':
        return 'File uploaded successfully';
      case 'transcribing':
        return 'Transcribing audio...';
      case 'summarizing':
        return 'Generating summary...';
      case 'generating_pdf':
        return 'Creating PDF document...';
      case 'completed':
        return 'Processing completed!';
      case 'error':
        return 'Processing failed';
      default:
        return 'Processing...';
    }
  };

  const getProgressSteps = () => {
    const steps = [
      { key: 'uploaded', label: 'Upload', progress: 10 },
      { key: 'transcribing', label: 'Transcribe', progress: 40 },
      { key: 'summarizing', label: 'Summarize', progress: 70 },
      { key: 'generating_pdf', label: 'Generate PDF', progress: 85 },
      { key: 'completed', label: 'Complete', progress: 100 },
    ];

    const currentStepIndex = steps.findIndex(step => step.key === currentJob.status);
    
    return steps.map((step, index) => ({
      ...step,
      isActive: index <= currentStepIndex,
      isCurrent: index === currentStepIndex,
    }));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mb-4">
            {getStatusIcon()}
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Processing Your Lecture
          </h2>
          <p className="text-gray-600">
            File: <span className="font-medium">{currentJob.filename}</span>
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            {getProgressSteps().map((step, index) => (
              <div key={step.key} className="flex flex-col items-center flex-1">
                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium mb-2
                  ${step.isActive 
                    ? step.isCurrent 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                  }
                `}>
                  {step.isActive && !step.isCurrent ? '✓' : index + 1}
                </div>
                <span className={`text-xs ${step.isActive ? 'text-gray-900' : 'text-gray-500'}`}>
                  {step.label}
                </span>
              </div>
            ))}
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${currentJob.progress}%` }}
            ></div>
          </div>
          <div className="text-center mt-2 text-sm text-gray-600">
            {currentJob.progress}% Complete
          </div>
        </div>

        {/* Status Message */}
        <div className="text-center mb-8">
          <p className="text-lg text-gray-700">{getStatusText()}</p>
          {currentJob.error_message && (
            <p className="text-red-600 mt-2">{currentJob.error_message}</p>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          {currentJob.status === 'completed' && (
            <button
              onClick={handleDownload}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
            >
              <Download className="w-5 h-5 mr-2" />
              Download PDF
            </button>
          )}
          
          <button
            onClick={onReset}
            className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
          >
            <RotateCcw className="w-5 h-5 mr-2" />
            Process Another File
          </button>
        </div>

        {/* Processing Info */}
        {currentJob.status !== 'completed' && currentJob.status !== 'error' && (
          <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">What's happening?</h3>
            <div className="text-sm text-blue-800">
              {currentJob.status === 'transcribing' && (
                <p>Converting your audio to text using advanced AI transcription...</p>
              )}
              {currentJob.status === 'summarizing' && (
                <p>Analyzing the transcript and generating educational insights...</p>
              )}
              {currentJob.status === 'generating_pdf' && (
                <p>Creating a professional PDF with summary and recommendations...</p>
              )}
            </div>
          </div>
        )}

        {/* Completion Info */}
        {currentJob.status === 'completed' && (
          <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
            <h3 className="font-medium text-green-900 mb-2">Processing Complete!</h3>
            <p className="text-sm text-green-800">
              Your lecture has been successfully processed. The PDF contains a comprehensive 
              summary and actionable educational insights to help improve your teaching.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessingStatus; 