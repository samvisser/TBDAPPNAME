import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileAudio, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { ProcessingJob } from '../App';

interface FileUploadProps {
  onUploadSuccess: (job: ProcessingJob) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/api/upload-audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Create job object
      const job: ProcessingJob = {
        job_id: response.data.job_id,
        filename: file.name,
        status: 'uploaded',
        progress: 0,
      };

      onUploadSuccess(job);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Upload failed. Please try again.';
      setError(errorMessage);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.m4a'],
      'video/*': ['.mp4', '.avi', '.mov'],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  return (
    <div className="max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive && !isDragReject 
            ? 'border-blue-500 bg-blue-50' 
            : isDragReject 
            ? 'border-red-500 bg-red-50'
            : 'border-gray-300 hover:border-gray-400'
          }
          ${uploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="mb-4">
          {uploading ? (
            <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
          ) : (
            <Upload className="w-12 h-12 text-gray-400 mx-auto" />
          )}
        </div>

        {uploading ? (
          <div>
            <p className="text-lg font-medium text-gray-900 mb-2">Uploading...</p>
            <p className="text-gray-600">Please wait while we process your file</p>
          </div>
        ) : isDragActive ? (
          isDragReject ? (
            <div>
              <p className="text-lg font-medium text-red-600 mb-2">Invalid file type</p>
              <p className="text-red-500">Please upload an audio or video file</p>
            </div>
          ) : (
            <div>
              <p className="text-lg font-medium text-blue-600 mb-2">Drop your file here</p>
              <p className="text-blue-500">Release to upload</p>
            </div>
          )
        ) : (
          <div>
            <p className="text-lg font-medium text-gray-900 mb-2">
              Drop your lecture recording here
            </p>
            <p className="text-gray-600 mb-4">
              or click to browse files
            </p>
            <div className="flex justify-center space-x-4 text-sm text-gray-500">
              <span className="flex items-center">
                <FileAudio className="w-4 h-4 mr-1" />
                MP3, WAV, M4A
              </span>
              <span className="flex items-center">
                <FileAudio className="w-4 h-4 mr-1" />
                MP4, AVI, MOV
              </span>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      )}

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>
          <strong>Supported formats:</strong> MP3, WAV, M4A, MP4, AVI, MOV
        </p>
        <p className="mt-1">
          <strong>Max file size:</strong> 500MB
        </p>
      </div>
    </div>
  );
};

export default FileUpload; 