from typing import Any, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ...database.session import get_db
from ...models.log import Log
from ...models.alert import Alert

router = APIRouter()

@router.get("/")
async def get_stats(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get system statistics
    """
    # Count total logs
    total_logs = db.query(func.count(Log.id)).scalar()

    # Count alerts by severity
    alert_stats = db.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).group_by(Alert.severity).all()

    severity_counts = {stat.severity: stat.count for stat in alert_stats}

    # Get recent activity (last 24 hours)
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)

    recent_logs = db.query(func.count(Log.id)).filter(
        Log.timestamp >= yesterday
    ).scalar()

    recent_alerts = db.query(func.count(Alert.id)).filter(
        Alert.timestamp >= yesterday
    ).scalar()

    return {
        "total_logs": total_logs or 0,
        "total_alerts": sum(severity_counts.values()),
        "alerts_by_severity": severity_counts,
        "recent_activity": {
            "logs_24h": recent_logs or 0,
            "alerts_24h": recent_alerts or 0,
        },
        "system_status": "normal" if (recent_alerts or 0) < 10 else "warning"
    }