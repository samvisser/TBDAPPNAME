from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ProcessingStatusEnum(str, Enum):
    UPLOADED = "uploaded"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    GENERATING_PDF = "generating_pdf"
    COMPLETED = "completed"
    ERROR = "error"

class ProcessingResult(BaseModel):
    summary: str
    insights: List[str]
    pdf_path: str

class ProcessingStatus(BaseModel):
    job_id: str
    filename: str
    status: ProcessingStatusEnum
    progress: int
    error_message: Optional[str] = None
    result: Optional[ProcessingResult] = None 