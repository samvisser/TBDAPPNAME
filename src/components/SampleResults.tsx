import React, { useState, useEffect } from 'react';
import { ArrowLeft, Download, FileText, Lightbulb } from 'lucide-react';
import axios from 'axios';

interface SampleResultsProps {
  onBack: () => void;
}

interface SampleData {
  summary: string;
  insights: string[];
}

const SampleResults: React.FC<SampleResultsProps> = ({ onBack }) => {
  const [sampleData, setSampleData] = useState<SampleData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSampleData = async () => {
      try {
        const response = await axios.get('/api/sample-result');
        setSampleData(response.data);
      } catch (error) {
        console.error('Failed to fetch sample data:', error);
        // Fallback to static data
        setSampleData({
          summary: `# Lecture Summary: Introduction to Data Structures

## Key Topics Covered
- Arrays and their time complexities
- Linked Lists implementation  
- Stack and Queue operations
- Basic sorting algorithms

## Main Points
1. **Arrays**: Fixed size, O(1) access time, but O(n) insertion/deletion
2. **Linked Lists**: Dynamic size, O(n) access time, but O(1) insertion/deletion at known positions
3. **Stacks**: LIFO principle, used in function calls and expression evaluation
4. **Queues**: FIFO principle, used in scheduling and breadth-first search

## Important Definitions
- **Time Complexity**: Measure of algorithm efficiency in terms of time
- **Space Complexity**: Measure of memory usage by an algorithm
- **Big O Notation**: Mathematical notation to describe algorithm complexity`,
          insights: [
            "Students showed confusion about pointer arithmetic - recommend additional practice problems",
            "The concept of time complexity was well understood by most students",
            "Queue implementation questions were asked frequently - consider more examples",
            "Memory management concepts need reinforcement in next lecture",
            "Students are ready to move on to more advanced data structures like trees"
          ]
        });
      } finally {
        setLoading(false);
      }
    };

    fetchSampleData();
  }, []);

  const formatSummary = (summary: string) => {
    const lines = summary.split('\n');
    return lines.map((line, index) => {
      const trimmedLine = line.trim();
      
      if (trimmedLine.startsWith('# ')) {
        return <h1 key={index} className="text-2xl font-bold text-gray-900 mt-6 mb-4">{trimmedLine.slice(2)}</h1>;
      } else if (trimmedLine.startsWith('## ')) {
        return <h2 key={index} className="text-xl font-semibold text-gray-800 mt-5 mb-3">{trimmedLine.slice(3)}</h2>;
      } else if (trimmedLine.startsWith('### ')) {
        return <h3 key={index} className="text-lg font-medium text-gray-700 mt-4 mb-2">{trimmedLine.slice(4)}</h3>;
      } else if (trimmedLine.startsWith('- ')) {
        return <li key={index} className="ml-4 mb-1 text-gray-600">{trimmedLine.slice(2)}</li>;
      } else if (trimmedLine.match(/^\d+\./)) {
        return <li key={index} className="ml-4 mb-1 text-gray-600">{trimmedLine}</li>;
      } else if (trimmedLine) {
        return <p key={index} className="text-gray-600 mb-2">{trimmedLine}</p>;
      } else {
        return <br key={index} />;
      }
    });
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={onBack}
          className="flex items-center text-blue-600 hover:text-blue-800 font-medium transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Upload
        </button>
        
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">Sample Results</h1>
          <p className="text-gray-600 mt-2">Preview of processed lecture analysis</p>
        </div>
        
        <div className="w-24"></div> {/* Spacer for alignment */}
      </div>

      {/* Results Grid */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Summary Section */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-blue-50 px-6 py-4 border-b">
            <div className="flex items-center">
              <FileText className="w-6 h-6 text-blue-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">Lecture Summary</h2>
            </div>
          </div>
          
          <div className="p-6 max-h-96 overflow-y-auto">
            <div className="prose prose-sm max-w-none">
              {sampleData && formatSummary(sampleData.summary)}
            </div>
          </div>
        </div>

        {/* Insights Section */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-green-50 px-6 py-4 border-b">
            <div className="flex items-center">
              <Lightbulb className="w-6 h-6 text-green-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">Educational Insights</h2>
            </div>
          </div>
          
          <div className="p-6">
            <p className="text-gray-600 mb-6 text-sm">
              AI-generated insights to help improve teaching effectiveness and student learning outcomes.
            </p>
            
            <div className="space-y-4">
              {sampleData?.insights.map((insight, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-4 border-l-4 border-green-500">
                  <div className="flex items-start">
                    <div className="bg-green-100 rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-1">
                      <span className="text-green-600 font-semibold text-sm">{index + 1}</span>
                    </div>
                    <p className="text-gray-700 text-sm leading-relaxed">{insight}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Download Section */}
      <div className="mt-12 text-center">
        <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-8 border">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Get Your Complete Analysis
          </h3>
          <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
            In the real application, you would receive a professionally formatted PDF containing 
            the complete summary, detailed insights, and actionable recommendations for improving 
            your lectures.
          </p>
          
          <div className="flex justify-center space-x-4">
            <button 
              onClick={onBack}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium flex items-center transition-colors"
            >
              <Download className="w-5 h-5 mr-2" />
              Try with Your Own Audio
            </button>
          </div>
        </div>
      </div>

      {/* Features Preview */}
      <div className="mt-12 grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🎯</span>
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">Accurate Transcription</h4>
          <p className="text-sm text-gray-600">
            Powered by OpenAI Whisper, AssemblyAI, or AWS Transcribe for high-accuracy speech-to-text
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">📊</span>
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">Smart Analysis</h4>
          <p className="text-sm text-gray-600">
            AI-powered summarization and insight extraction using GPT and advanced NLP models
          </p>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">📋</span>
          </div>
          <h4 className="font-semibold text-gray-900 mb-2">Professional Output</h4>
          <p className="text-sm text-gray-600">
            Clean, formatted PDF reports with actionable insights for educational improvement
          </p>
        </div>
      </div>
    </div>
  );
};

export default SampleResults; 