import React, { useState } from 'react';

const QuickTest: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const startTime = performance.now();
    setLoading(true);
    setError('');
    setResult('');
    setStatus('Sending request...');

    // Create an AbortController for the fetch timeout
    const controller = new AbortController();
    const timeout = setTimeout(() => {
      controller.abort();
      setStatus('Request timed out');
      console.log('Request aborted due to timeout');
    }, 7000); // 7 second timeout (slightly longer than backend)

    try {
      setStatus('Connecting to API...');
      const response = await fetch('http://localhost:8000/api/quick-test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
        signal: controller.signal
      });

      clearTimeout(timeout);
      const endTime = performance.now();
      const processingTime = (endTime - startTime) / 1000;

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Error response (${response.status}):`, errorText);
        
        if (response.status === 408) {
          throw new Error('Request timed out - try a simpler question');
        }
        throw new Error(`Server error (${response.status}): ${errorText}`);
      }

      setStatus('Processing response...');
      const data = await response.json();
      
      if (!data.result) {
        throw new Error('Empty response from server');
      }

      console.log(`Response received in ${processingTime.toFixed(2)}s:`, data);
      setResult(data.result);
      setStatus('Complete');

    } catch (err) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
      setStatus('Error');
    } finally {
      setLoading(false);
      clearTimeout(timeout);
    }
  };

  return (
    <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
      <h2 className="text-xl font-bold text-blue-300 mb-4">Quick Gemini Test</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter a simple question (e.g., what is 1 plus 1?)"
            className="w-full px-4 py-2 bg-slate-700 text-slate-200 border border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="flex items-center justify-between">
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
              loading || !question.trim()
                ? 'bg-slate-600 text-slate-300 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              'Test'
            )}
          </button>
          {status && (
            <span className={`text-sm ${
              status === 'Complete' ? 'text-green-400' :
              status === 'Error' ? 'text-red-400' :
              'text-slate-400'
            }`}>
              {status}
            </span>
          )}
        </div>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-900/20 text-red-400 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-slate-700/50 rounded-lg">
          <p className="text-slate-300 whitespace-pre-wrap">{result}</p>
          <p className="text-xs text-slate-400 mt-2">
            Response received at: {new Date().toLocaleTimeString()}
          </p>
        </div>
      )}
    </div>
  );
};

export default QuickTest; 