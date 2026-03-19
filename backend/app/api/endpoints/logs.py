from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database.session import get_db
from ...models.log import Log
from ...schemas.log import LogCreate, LogResponse

router = APIRouter()

@router.post("/", response_model=LogResponse)
async def create_log(
    *,
    db: Session = Depends(get_db),
    log_in: LogCreate,
) -> Any:
    """
    Create a new log entry from the agent
    """
    log = Log(**log_in.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return {
        "id": log.id,
        "timestamp": log.timestamp,
        "file_path": log.file_path,
        "process_name": log.process_name,
        "entropy": log.entropy,
        "prediction": log.prediction,
        "cpu_usage": log.cpu_usage,
        "file_change_rate": log.file_change_rate,
        "detection_method": log.detection_method,
        "raw_data": log.raw_data,
    }

@router.get("/", response_model=List[LogResponse])
async def get_logs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve logs with pagination
    """
    logs = db.query(Log).offset(skip).limit(limit).all()
    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "file_path": log.file_path,
            "process_name": log.process_name,
            "entropy": log.entropy,
            "prediction": log.prediction,
            "cpu_usage": log.cpu_usage,
            "file_change_rate": log.file_change_rate,
            "detection_method": log.detection_method,
            "raw_data": log.raw_data,
        }
        for log in logs
    ]