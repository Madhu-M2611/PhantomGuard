from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from ..database.session import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=True)
    process_name = Column(String, nullable=True)
    entropy = Column(Float, nullable=True)
    prediction = Column(Float, nullable=True)  # BiLSTM prediction score
    cpu_usage = Column(Float, nullable=True)
    file_change_rate = Column(Float, nullable=True)
    detection_method = Column(String, nullable=True)  # 'bilstm', 'rule', 'honeyfile'
    raw_data = Column(Text, nullable=True)  # JSON string of additional data