"""
Test script to verify all connections (backend server, frontend, and Gemini LLM).
"""
import requests
import json
from google import genai
from config import API_KEY, API_PORT

def test_backend_connection():
    """Test if backend server is running and responding."""
    try:
        response = requests.get(f'http://localhost:{API_PORT}/api/test')
        print(f"\n✅ Backend server test:")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"\n❌ Backend server error:")
        print(f"Error: {str(e)}")
        return False

def test_gemini_connection():
    """Test if Gemini LLM is connected and responding."""
    try:
        print(f"\n🔄 Testing Gemini connection with API key: {API_KEY[:4]}...{API_KEY[-4:]}")
        
        client = genai.Client(api_key=API_KEY)
        model = "gemini-2.5-flash"
        
        # Simple test prompt
        test_prompt = "Say 'Hello, testing Gemini connection!' in one short sentence."
        
        print("\n📤 Sending test prompt to Gemini...")
        response = client.models.generate_content(
            model=model,
            contents=test_prompt
        )
        
        print(f"\n✅ Gemini test successful:")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"\n❌ Gemini connection error:")
        print(f"Error: {str(e)}")
        return False

def test_process_endpoint():
    """Test the main text processing endpoint."""
    try:
        test_text = "This is a test message to check if the text processing is working."
        response = requests.post(
            f'http://localhost:{API_PORT}/api/process-transcript',
            json={"text": test_text, "is_audio_transcript": False}
        )
        
        print(f"\n✅ Process endpoint test:")
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"\n❌ Process endpoint error:")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🔍 Starting connection tests...")
    
    # Test backend server
    server_ok = test_backend_connection()
    
    if server_ok:
        # Test Gemini connection
        gemini_ok = test_gemini_connection()
        
        # Test process endpoint
        if gemini_ok:
            process_ok = test_process_endpoint()
    
    print("\n📋 Test Summary:")
    print(f"Backend Server: {'✅' if server_ok else '❌'}")
    print(f"Gemini LLM: {'✅' if 'gemini_ok' in locals() and gemini_ok else '❌'}")
    print(f"Process Endpoint: {'✅' if 'process_ok' in locals() and process_ok else '❌'}")
