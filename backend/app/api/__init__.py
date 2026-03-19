from fastapi import APIRouter

from .endpoints import auth, logs, alerts, stats

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(stats.router, prefix="/stats", tags=["statistics"])