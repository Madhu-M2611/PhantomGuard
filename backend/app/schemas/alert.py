from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AlertBase(BaseModel):
    severity: str
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    process_name: Optional[str] = None
    detection_method: Optional[str] = None
    prediction_score: Optional[float] = None
    raw_data: Optional[str] = None
    status: Optional[str] = "active"

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    is_acknowledged: Optional[int] = None

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True