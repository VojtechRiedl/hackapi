from sqlalchemy import Column,Text, TIMESTAMP,DateTime,Date, Float, ForeignKey, Integer, String, Boolean,Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Messages(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(TIMESTAMP, index=True, default=func.current_date(), nullable=False)
    size = Column(Integer, index=True, nullable=False)
    topic = Column(String(255), nullable=False)
        