import React, { useState } from 'react';

const TestConnection: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testBackend = async () => {
    setLoading(true);
    setError('');
    try {
      console.log('Testing backend connection...');
      const response = await fetch('http://localhost:8000/api/test', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
      console.log('Response received:', response);
      const data = await response.json();
      console.log('Data:', data);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error('Connection error:', err);
      setError('Failed to connect to backend: ' + (err as Error).message + '\nMake sure the backend server is running on port 8000');
    } finally {
      setLoading(false);
    }
  };

  const testPost = async () => {
    setLoading(true);
    setError('');
    try {
      console.log('Testing POST request...');
      const response = await fetch('http://localhost:8000/api/test-post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ test: 'Hello from frontend!' }),
      });
      console.log('POST response received:', response);
      const data = await response.json();
      console.log('POST data:', data);
      setResult(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error('POST error:', err);
      setError('Failed to connect to backend: ' + (err as Error).message + '\nMake sure the backend server is running on port 8000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
      <h2 className="text-xl font-bold text-blue-300 mb-4">Backend Connection Test</h2>
      <div className="space-y-4">
        <div className="flex space-x-4">
          <button
            onClick={testBackend}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-600"
          >
            Test GET
          </button>
          <button
            onClick={testPost}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-600"
          >
            Test POST
          </button>
        </div>
        
        {loading && (
          <div className="text-slate-300">Testing connection...</div>
        )}
        
        {error && (
          <div className="text-red-400 bg-red-900/20 p-4 rounded-lg">
            <p className="font-bold mb-2">Error:</p>
            <pre className="whitespace-pre-wrap">{error}</pre>
          </div>
        )}
        
        {result && (
          <div className="bg-slate-700/50 p-4 rounded-lg">
            <p className="font-bold text-blue-300 mb-2">Response:</p>
            <pre className="text-slate-300 whitespace-pre-wrap">{result}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default TestConnection; 