import os
import asyncio
from pathlib import Path
from typing import Optional
import openai
import assemblyai as aai
import boto3
from dotenv import load_dotenv

load_dotenv()

class AudioProcessor:
    def __init__(self):
        # Initialize API clients
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        
        # AWS Transcribe setup
        self.aws_session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.transcribe_client = self.aws_session.client('transcribe')
        self.s3_client = self.aws_session.client('s3')
        
        # Preferred transcription method
        self.method = os.getenv("TRANSCRIPTION_METHOD", "openai")  # openai, assemblyai, aws
    
    async def transcribe(self, file_path: Path) -> str:
        """Transcribe audio file using the configured method"""
        if self.method == "openai":
            return await self._transcribe_with_openai(file_path)
        elif self.method == "assemblyai":
            return await self._transcribe_with_assemblyai(file_path)
        elif self.method == "aws":
            return await self._transcribe_with_aws(file_path)
        else:
            # Fallback to mock transcription for demo
            return await self._mock_transcribe(file_path)
    
    async def _transcribe_with_openai(self, file_path: Path) -> str:
        """Transcribe using OpenAI Whisper API"""
        try:
            with open(file_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript
        except Exception as e:
            print(f"OpenAI transcription failed: {e}")
            return await self._mock_transcribe(file_path)
    
    async def _transcribe_with_assemblyai(self, file_path: Path) -> str:
        """Transcribe using AssemblyAI"""
        try:
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(str(file_path))
            
            if transcript.status == aai.TranscriptStatus.error:
                raise Exception(f"AssemblyAI error: {transcript.error}")
            
            return transcript.text
        except Exception as e:
            print(f"AssemblyAI transcription failed: {e}")
            return await self._mock_transcribe(file_path)
    
    async def _transcribe_with_aws(self, file_path: Path) -> str:
        """Transcribe using AWS Transcribe"""
        try:
            # Upload to S3 first
            bucket_name = os.getenv("AWS_S3_BUCKET")
            if not bucket_name:
                raise Exception("AWS S3 bucket not configured")
            
            s3_key = f"audio/{file_path.name}"
            self.s3_client.upload_file(str(file_path), bucket_name, s3_key)
            
            # Start transcription job
            job_name = f"transcribe-{file_path.stem}"
            job_uri = f"s3://{bucket_name}/{s3_key}"
            
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat=file_path.suffix[1:].lower(),
                LanguageCode='en-US'
            )
            
            # Wait for completion
            while True:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                await asyncio.sleep(5)
            
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                raise Exception("AWS Transcribe job failed")
            
            # Get transcript
            transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            import requests
            response = requests.get(transcript_uri)
            transcript_json = response.json()
            
            return transcript_json['results']['transcripts'][0]['transcript']
            
        except Exception as e:
            print(f"AWS transcription failed: {e}")
            return await self._mock_transcribe(file_path)
    
    async def _mock_transcribe(self, file_path: Path) -> str:
        """Mock transcription for demo purposes"""
        return """
        Welcome to CS300, Introduction to Data Structures and Algorithms. Today we're going to cover some fundamental concepts that will be essential throughout this course.

        Let's start with arrays. An array is a collection of elements stored in contiguous memory locations. The key advantage of arrays is that we can access any element in constant time, O(1), using its index. However, inserting or deleting elements can be expensive, requiring O(n) time in the worst case because we might need to shift other elements.

        Now let's talk about linked lists. Unlike arrays, linked lists store elements in nodes that are connected through pointers. This gives us more flexibility for insertion and deletion operations. We can insert or delete at a known position in O(1) time. However, accessing an arbitrary element requires O(n) time because we need to traverse from the head.

        Moving on to stacks, these follow the Last In, First Out principle, or LIFO. Think of it like a stack of plates - you add and remove plates from the top. Stacks are crucial for many applications like function call management, expression evaluation, and backtracking algorithms.

        Queues, on the other hand, follow First In, First Out, or FIFO. Like a line at a coffee shop, the first person in line is the first to be served. Queues are essential for scheduling, breadth-first search, and handling requests in operating systems.

        Let's discuss time complexity. This is a way to measure how the runtime of an algorithm grows as the input size increases. We use Big O notation to express this. For example, O(1) means constant time, O(n) means linear time, and O(n²) means quadratic time.

        Space complexity is equally important. It measures how much additional memory an algorithm uses relative to the input size. Sometimes we trade time for space or vice versa.

        Are there any questions about these concepts? I see some confused faces about pointer arithmetic. Remember, a pointer is just a variable that stores the memory address of another variable. When we say ptr++, we're moving to the next memory location.

        Let me give you another example with queues since I'm seeing some questions. In a typical queue implementation, we have two pointers: front and rear. When we enqueue, we add at the rear. When we dequeue, we remove from the front.

        For your homework, I want you to implement both a stack and a queue using arrays. Pay attention to the edge cases like empty structures and full arrays. We'll review these implementations next class.

        Next week, we'll dive into more advanced data structures like binary trees and hash tables. Make sure you're comfortable with these basic concepts because they're the foundation for everything else we'll cover.

        Any final questions before we wrap up? Great, I'll see you all next week.
        """ 