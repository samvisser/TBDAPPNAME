import React, { useState } from 'react';

interface TextInputProps {
  onSubmit: (text: string) => void;
  isProcessing: boolean;
}

const TextInput: React.FC<TextInputProps> = ({ onSubmit, isProcessing }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text);
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="transcript" className="block text-blue-300 font-medium mb-2">
            Enter Meeting Transcript
          </label>
          <textarea
            id="transcript"
            className="w-full h-64 px-4 py-3 bg-slate-700 text-slate-200 border border-slate-600 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Paste your meeting transcript here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={isProcessing}
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isProcessing || !text.trim()}
            className={`px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
              isProcessing || !text.trim()
                ? 'bg-slate-600 text-slate-300 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105'
            }`}
          >
            {isProcessing ? 'Processing...' : 'Process Transcript'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TextInput; 