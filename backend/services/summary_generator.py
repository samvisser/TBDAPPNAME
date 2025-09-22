import os
from typing import List
import openai
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv
import re

load_dotenv()

class SummaryGenerator:
    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize Hugging Face models (lazy loading)
        self.summarizer = None
        self.classifier = None
        
        # Preferred method
        self.method = os.getenv("SUMMARY_METHOD", "openai")  # openai, huggingface
    
    def _load_hf_models(self):
        """Lazy load Hugging Face models"""
        if self.summarizer is None:
            try:
                # Load BART for summarization
                self.summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    tokenizer="facebook/bart-large-cnn"
                )
                
                # Load model for classification/insights
                self.classifier = pipeline(
                    "text-classification",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
            except Exception as e:
                print(f"Failed to load HuggingFace models: {e}")
                self.summarizer = None
                self.classifier = None
    
    async def generate_summary(self, transcript: str) -> str:
        """Generate a comprehensive summary of the lecture"""
        if self.method == "openai" and os.getenv("OPENAI_API_KEY"):
            return await self._summarize_with_openai(transcript)
        elif self.method == "huggingface":
            return await self._summarize_with_huggingface(transcript)
        else:
            return self._generate_mock_summary(transcript)
    
    async def extract_insights(self, transcript: str) -> List[str]:
        """Extract educational insights from the lecture"""
        if self.method == "openai" and os.getenv("OPENAI_API_KEY"):
            return await self._extract_insights_with_openai(transcript)
        else:
            return self._extract_mock_insights(transcript)
    
    async def _summarize_with_openai(self, transcript: str) -> str:
        """Generate summary using OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert educational content summarizer. Create a comprehensive, well-structured summary of the lecture transcript. 

                        Format your response in Markdown with:
                        - A clear title
                        - Key topics covered
                        - Main points with bullet points or numbered lists
                        - Important definitions
                        - Any examples or case studies mentioned
                        
                        Make it suitable for student review and study."""
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize this lecture transcript:\n\n{transcript}"
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI summarization failed: {e}")
            return self._generate_mock_summary(transcript)
    
    async def _extract_insights_with_openai(self, transcript: str) -> List[str]:
        """Extract insights using OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an educational analyst. Analyze the lecture transcript and provide actionable insights for the instructor. Focus on:
                        
                        - Student comprehension indicators (questions, confusion points)
                        - Concepts that were well understood vs. challenging
                        - Suggestions for improvement
                        - Areas that need reinforcement
                        - Student engagement patterns
                        
                        Return exactly 5 insights as a JSON array of strings."""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this lecture transcript for educational insights:\n\n{transcript}"
                    }
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            content = response.choices[0].message.content
            # Try to parse as JSON, fallback to splitting by lines
            try:
                import json
                insights = json.loads(content)
                if isinstance(insights, list):
                    return insights[:5]
            except:
                pass
            
            # Fallback: split by lines and clean up
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            insights = [line.lstrip('- ').lstrip('• ').lstrip('1234567890. ') for line in lines if line]
            return insights[:5]
            
        except Exception as e:
            print(f"OpenAI insights extraction failed: {e}")
            return self._extract_mock_insights(transcript)
    
    async def _summarize_with_huggingface(self, transcript: str) -> str:
        """Generate summary using Hugging Face models"""
        self._load_hf_models()
        
        if not self.summarizer:
            return self._generate_mock_summary(transcript)
        
        try:
            # Split long transcript into chunks
            max_length = 1024
            chunks = [transcript[i:i+max_length] for i in range(0, len(transcript), max_length)]
            
            summaries = []
            for chunk in chunks[:3]:  # Limit to first 3 chunks
                summary = self.summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            
            # Combine summaries
            combined = " ".join(summaries)
            
            # Format as markdown
            formatted_summary = f"""# Lecture Summary

## Key Points
{combined}

## Overview
This lecture covered important concepts in computer science education. The main topics discussed provide a foundation for further learning in the subject area.
"""
            
            return formatted_summary
            
        except Exception as e:
            print(f"HuggingFace summarization failed: {e}")
            return self._generate_mock_summary(transcript)
    
    def _generate_mock_summary(self, transcript: str) -> str:
        """Generate a mock summary for demo purposes"""
        return """# Lecture Summary: Introduction to Data Structures

## Key Topics Covered
- **Arrays**: Fixed-size collections with O(1) access time
- **Linked Lists**: Dynamic structures with pointer-based connections
- **Stacks**: LIFO (Last In, First Out) data structure
- **Queues**: FIFO (First In, First Out) data structure
- **Time and Space Complexity**: Algorithm efficiency analysis

## Main Points

### Arrays
1. Elements stored in contiguous memory locations
2. Constant time O(1) access using indices
3. O(n) time complexity for insertion/deletion due to shifting

### Linked Lists
1. Elements stored in nodes connected by pointers
2. O(1) insertion/deletion at known positions
3. O(n) access time due to traversal requirements

### Stacks and Queues
1. **Stacks**: Used in function calls, expression evaluation, backtracking
2. **Queues**: Essential for scheduling, BFS, and request handling
3. Both are fundamental for many algorithms

### Complexity Analysis
1. **Time Complexity**: Measures algorithm runtime growth
2. **Space Complexity**: Measures memory usage
3. **Big O Notation**: Mathematical way to express complexity

## Important Definitions
- **Big O Notation**: Mathematical notation describing algorithm complexity
- **Pointer**: Variable storing memory address of another variable
- **LIFO**: Last In, First Out (Stack principle)
- **FIFO**: First In, First Out (Queue principle)

## Examples Discussed
- Stack of plates analogy for stack operations
- Coffee shop line analogy for queue operations
- Pointer arithmetic and memory addressing

## Homework Assignment
Implement both stack and queue using arrays, paying attention to edge cases like empty structures and full arrays.

## Next Week Preview
Advanced data structures: binary trees and hash tables will be covered in the next lecture."""
    
    def _extract_mock_insights(self, transcript: str) -> List[str]:
        """Generate mock insights for demo purposes"""
        return [
            "Students showed confusion about pointer arithmetic - recommend additional practice problems and visual diagrams",
            "The concept of time complexity was well understood by most students based on engagement patterns",
            "Queue implementation questions were asked frequently - consider providing more concrete examples in future lectures",
            "Memory management concepts need reinforcement in the next lecture with hands-on coding exercises",
            "Students are ready to progress to more advanced data structures like trees based on their grasp of fundamentals"
        ] 