from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class LogBase(BaseModel):
    file_path: Optional[str] = None
    process_name: Optional[str] = None
    entropy: Optional[float] = None
    prediction: Optional[float] = None
    cpu_usage: Optional[float] = None
    file_change_rate: Optional[float] = None
    detection_method: Optional[str] = None
    raw_data: Optional[str] = None

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True