from typing import List, Any
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ...database.session import get_db
from ...models.alert import Alert
from ...schemas.alert import AlertCreate, AlertResponse

router = APIRouter()

@router.post("/", response_model=AlertResponse)
async def create_alert(
    *,
    db: Session = Depends(get_db),
    alert_in: AlertCreate,
) -> Any:
    """
    Create an alert entry from the agent
    """
    alert = Alert(**alert_in.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {
        "id": alert.id,
        "timestamp": alert.timestamp,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "file_path": alert.file_path,
        "process_name": alert.process_name,
        "prediction_score": alert.prediction_score,
        "status": alert.status,
        "resolved_at": alert.resolved_at,
    }

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=100, le=1000),
    severity: str = Query(None, description="Filter by severity: critical, high, medium, low"),
) -> Any:
    """
    Retrieve alerts with optional filtering
    """
    query = db.query(Alert)

    if severity:
        query = query.filter(Alert.severity == severity)

    alerts = query.offset(skip).limit(limit).all()
    return [
        {
            "id": alert.id,
            "timestamp": alert.timestamp,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "file_path": alert.file_path,
            "process_name": alert.process_name,
            "prediction_score": alert.prediction_score,
            "status": alert.status,
            "resolved_at": alert.resolved_at,
        }
        for alert in alerts
    ]

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
) -> Any:
    """
    Get a specific alert by ID
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {
        "id": alert.id,
        "timestamp": alert.timestamp,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "file_path": alert.file_path,
        "process_name": alert.process_name,
        "prediction_score": alert.prediction_score,
        "status": alert.status,
        "resolved_at": alert.resolved_at,
    }
