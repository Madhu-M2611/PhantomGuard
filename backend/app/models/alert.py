from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from ..database.session import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(String, nullable=False)  # 'critical', 'high', 'medium', 'low'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)
    process_name = Column(String, nullable=True)
    detection_method = Column(String, nullable=True)  # 'bilstm', 'rule', 'honeyfile'
    prediction_score = Column(Float, nullable=True)
    raw_data = Column(Text, nullable=True)  # JSON string of additional data
    status = Column(String, default="active")  # 'active', 'resolved', 'dismissed'
    resolved_at = Column(DateTime(timezone=True), nullable=True)