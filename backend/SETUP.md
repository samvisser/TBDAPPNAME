# Backend Setup Instructions

## Project Structure

The backend is now organized into proper modules:

```
backend/
├── config.py              # Configuration settings
├── main.py                # FastAPI application entry point
├── .env                   # Environment variables (create this file)
├── services/
│   ├── __init__.py
│   └── gemini_service.py  # Gemini AI service
├── models/
│   ├── __init__.py
│   └── processing_models.py
└── requirements.txt
```

## Setup Steps

1. **Create the `.env` file** in the backend directory:
   ```bash
   cd backend
   touch .env
   ```

2. **Add your Google API key** to the `.env` file:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

3. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python main.py
   ```

## Key Changes

- **Modular structure**: Code is now organized into services and config modules
- **Environment variables**: All configuration is centralized in `config.py`
- **Service layer**: Gemini API logic is separated into `GeminiService` class
- **Clean imports**: Main.py is much cleaner and focused on API routes

## Configuration

All configuration is now in `config.py`:
- API host/port settings
- Gemini model parameters
- Environment variable loading

The `.env` file should be placed in the `backend/` directory, not the root project directory.
