from sqlalchemy import Column,Text, TIMESTAMP,DateTime,Date, Float, ForeignKey, Integer, String, Boolean,Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Topics(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    level = Column(Integer, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('topics.id'))

    children = relationship("Topic")
    message = relationship("Message", back_populates="topic")

class Messages(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(TIMESTAMP, index=True, default=func.current_date(), nullable=False)
    size = Column(Integer, index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    
    topic = relationship("Topics", back_populates="message")
    